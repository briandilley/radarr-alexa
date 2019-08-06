
from ask_sdk_core.skill_builder import SkillBuilder

from .launch_request_handler import LaunchRequestHandler
from .cancel_request_handler import CancelAndStopIntentHandler
from .download_request_handler import DownloadRequestHandler
from .downloaded_request_handler import DownloadedRequestHandler
from .all_exception_handler import AllExceptionHandler

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(DownloadRequestHandler())
sb.add_request_handler(DownloadedRequestHandler())
sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()
