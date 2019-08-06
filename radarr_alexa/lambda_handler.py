
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.dispatch_components import AbstractResponseInterceptor

from .launch_request_handler import LaunchRequestHandler
from .download_request_handler import DownloadRequestHandler
from .downloaded_request_handler import DownloadedRequestHandler
from .all_exception_handler import AllExceptionHandler

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LoggingRequestInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        req = handler_input.request_envelope.request
        if req.object_type == "IntentRequest":
            logger.info(f"Entering {req.intent.name}\n")
        else:
            logger.info(f"Entering {req.object_type}\n")


class LoggingResponseInterceptor(AbstractResponseInterceptor):
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        req = handler_input.request_envelope.request
        if req.object_type == "IntentRequest":
            logger.info(f"Response from {req.intent.name}: {response}\n")
        else:
            logger.info(f"Response from {req.object_type}: {response}\n")


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(DownloadRequestHandler())
sb.add_request_handler(DownloadedRequestHandler())
sb.add_global_request_interceptor(LoggingRequestInterceptor())
sb.add_global_response_interceptor(LoggingResponseInterceptor())
sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()
