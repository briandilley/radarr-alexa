
import logging

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Response
from ask_sdk_model.ui import StandardCard, SimpleCard, Image

from .radar_client import add_movie_to_download, search_movie_for_download

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DownloadRequestHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DownloadIntent")(handler_input) \
            or self.is_yes(handler_input) \
            or self.is_no(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        attr = handler_input.attributes_manager.session_attributes
        is_yes = self.is_yes(handler_input)
        is_no = self.is_no(handler_input)
        is_searching = not is_yes and not is_no
        is_confirming = self.is_confirming(handler_input)

        logger.info("is_yes: " + str(is_yes))
        logger.info("is_no: " + str(is_no))
        logger.info("is_searching: " + str(is_searching))
        logger.info("is_confirming: " + str(is_confirming))

        # search for it, ask them to confirm
        if is_searching:
            movie_name = slots["movie_name"].value
            movie_year = slots["movie_year"].value if 'movie_year' in slots.keys() else None

            (speech_text, record) = search_movie_for_download(movie_name, movie_year)

            if not record:
                return handler_input.response_builder.speak(speech_text) \
                    .set_card(SimpleCard("Download", speech_text)) \
                    .set_should_end_session(True) \
                    .response

            attr['movie'] = record

            return handler_input.response_builder.speak(speech_text) \
                .set_card(StandardCard(record['title'], speech_text, self.movie_image(record))) \
                .set_should_end_session(False) \
                .response

        # it was confirmed
        if is_confirming and is_yes:
            movie = attr['movie']

            speech_text = add_movie_to_download(movie)

            return handler_input.response_builder.speak(speech_text) \
                .set_card(StandardCard(movie['title'], speech_text, self.movie_image(movie))) \
                .set_should_end_session(True) \
                .response

        # it was not confirmed
        if is_confirming and is_no:
            return handler_input.response_builder.speak("Ok, I wont tell Radar to grab that movie") \
                .set_should_end_session(True) \
                .response

        # canceled or something
        if is_no:
            return handler_input.response_builder.speak("Ok, goodbye") \
                .set_should_end_session(True) \
                .response

        return handler_input.response_builder.speak("Sorry, I'm a bit confused.  Please try again.") \
            .set_should_end_session(True) \
            .response

    @staticmethod
    def is_yes(handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    @staticmethod
    def is_no(handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.NoIntent")(handler_input) \
               or is_intent_name("AMAZON.CancelIntent")(handler_input) \
               or is_intent_name("AMAZON.StopIntent")(handler_input)

    @staticmethod
    def is_confirming(handler_input):
        # type: (HandlerInput) -> bool
        return 'movie' in handler_input.attributes_manager.session_attributes

    @staticmethod
    def movie_image(movie):
        # type: (dict) -> Image | None
        images = movie.get("images", []) if movie and 'images' in movie else list()
        if len(images) == 0:
            return None
        url = images[0]['url']
        return Image(large_image_url=url.replace("http:", "https:", 1))


