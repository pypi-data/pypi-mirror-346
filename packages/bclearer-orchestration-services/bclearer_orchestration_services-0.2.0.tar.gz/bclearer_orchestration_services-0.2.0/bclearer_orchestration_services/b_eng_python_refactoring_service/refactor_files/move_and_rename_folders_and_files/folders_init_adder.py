import os

from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_file_system_objects import (
    BEngWorkspaceFileSystemObjects,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def add_init_files_if_required(
    target_object: BEngWorkspaceFileSystemObjects,
):
    code_folders = (
        target_object.get_code_folders()
    )

    for code_folder in code_folders:
        __add_init_file_in_required(
            b_eng_workspace_file_system_object=code_folder,
        )


def __add_init_file_in_required(
    b_eng_workspace_file_system_object: BEngWorkspaceFileSystemObjects,
):
    if (
        not b_eng_workspace_file_system_object.exists()
    ):
        return

    init_file_path = b_eng_workspace_file_system_object.extend_path(
        path_extension="__init__.py",
    )

    if os.path.exists(
        path=str(init_file_path),
    ):
        return

    init_file = open(
        file=str(init_file_path),
        mode="w",
    )

    log_message(
        "\tadding: "
        + str(init_file_path),
    )

    init_file.close()
