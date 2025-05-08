import os

from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from nf_common.code.services.datetime_service.time_helpers.time_getter import (
    now_time_as_string_for_files,
)


def create_output_folder(
    output_root_folder: Folders,
    run_suffix: str,
) -> str:
    if not os.path.exists(
        output_root_folder.absolute_path_string,
    ):
        os.mkdir(
            output_root_folder.absolute_path_string,
        )

    output_folder_name = (
        now_time_as_string_for_files()
        + "_"
        + run_suffix
    )

    output_folder_path = os.path.join(
        output_root_folder.absolute_path_string,
        output_folder_name,
    )

    os.mkdir(output_folder_path)

    return output_folder_path
