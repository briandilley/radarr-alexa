from ask_sdk_core.dispatch_components import AbstractExceptionHandler


class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Sorry, there was an error.  Please try again!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response
