from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard


class LaunchRequestHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input) \
            or is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = """
        Welcome to Radarr Alexa,  You can use this to control your Radarr installation.
        Say download movie Avengers, or What movies have I downloaded lately?
        """

        handler_input.response_builder.speak(speech_text)\
            .set_card(SimpleCard("Welcome", speech_text))\
            .set_should_end_session(False)

        return handler_input.response_builder.response

