from pathlib import Path

from nf_common.code.services.reporting_service.reporters.log_file import (
    LogFiles,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def set_up_logger_and_output_folder(
    output_folder_name: str,
):
    output_folder = Path(
        output_folder_name,
    )

    output_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    LogFiles.open_log_file(
        folder_path=output_folder_name,
    )

    return output_folder


def end_test():
    log_message("DONE")

    LogFiles.close_log_file()
