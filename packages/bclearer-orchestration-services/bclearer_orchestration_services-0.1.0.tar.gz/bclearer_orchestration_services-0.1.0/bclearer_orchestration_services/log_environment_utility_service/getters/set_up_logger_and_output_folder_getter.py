from pathlib import Path

from nf_common.code.services.reporting_service.reporters.log_file import (
    LogFiles,
)


def get_set_up_logger_and_output_folder(
    output_folder_name: str,
    now_time: str,
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
        now_time=now_time,
    )

    return output_folder
