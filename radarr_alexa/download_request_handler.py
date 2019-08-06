from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard


class DownloadRequestHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DownloadIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = """
        Lets download some movies!
        """

        handler_input.response_builder.speak(speech_text)\
            .set_card(SimpleCard("Download", speech_text))\
            .set_should_end_session(True)

        return handler_input.response_builder.response

