import os
from pathlib import Path

from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.datetime_service.time_helpers.time_getter import (
    now_time_as_string_for_files,
)
from bclearer_orchestration_services.reporting_service.reporters.log_file import (
    LogFiles,
)


def set_up_output_folder_and_logger(
    output_root_folder: Folders,
    output_folder_prefix: str,
    output_folder_suffix: str,
):
    output_folder_path = __get_output_folder_path(
        output_root_folder=output_root_folder,
        output_folder_prefix=output_folder_prefix,
        output_folder_suffix=output_folder_suffix,
    )

    Path(output_folder_path).mkdir(
        parents=True,
        exist_ok=True,
    )

    LogFiles.open_log_file(
        folder_path=output_folder_path,
    )

    return output_root_folder


def __get_output_folder_path(
    output_root_folder: Folders,
    output_folder_prefix: str,
    output_folder_suffix: str,
) -> str:
    output_folder_name = __get_output_folder_name(
        output_folder_prefix=output_folder_prefix,
        output_folder_suffix=output_folder_suffix,
    )

    output_folder_path = os.path.join(
        output_root_folder.absolute_path_string,
        output_folder_name,
    )

    return output_folder_path


def __get_output_folder_name(
    output_folder_prefix: str,
    output_folder_suffix: str,
) -> str:
    datetime_stamp = (
        now_time_as_string_for_files()
    )

    output_folder_name = datetime_stamp

    if output_folder_prefix:
        output_folder_name = (
            output_folder_prefix
            + "_"
            + output_folder_name
        )

    if output_folder_suffix:
        output_folder_name = (
            output_folder_name
            + "_"
            + output_folder_suffix
        )

    return output_folder_name
