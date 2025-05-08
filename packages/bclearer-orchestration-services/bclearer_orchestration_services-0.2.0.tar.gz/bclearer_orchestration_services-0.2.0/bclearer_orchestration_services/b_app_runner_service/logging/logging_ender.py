# from code import LogFiles

from bclearer_orchestration_services.reporting_service.reporters.log_file import (
    LogFiles,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def end_logging():
    log_message("DONE")

    LogFiles.close_log_file()
