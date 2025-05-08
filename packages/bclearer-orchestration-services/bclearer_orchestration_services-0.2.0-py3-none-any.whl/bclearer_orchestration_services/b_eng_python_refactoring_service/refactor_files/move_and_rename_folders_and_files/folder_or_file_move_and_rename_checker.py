from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_file_system_object_couples import (
    BEngWorkspaceFileSystemObjectCouples,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_file_system_objects import (
    BEngWorkspaceFileSystemObjects,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def move_and_rename_file_or_folder_checks(
    source_target_b_eng_workspace_file_system_object_couple: BEngWorkspaceFileSystemObjectCouples,
) -> bool:
    source_b_eng_workspace_file_system_object = (
        source_target_b_eng_workspace_file_system_object_couple.place_1_b_eng_workspace_file_system_object
    )

    source_exists = __check_b_eng_workspace_file_system_object_exists(
        b_eng_workspace_file_system_object=source_b_eng_workspace_file_system_object,
    )

    if not source_exists:
        return False

    return True


def __check_b_eng_workspace_file_system_object_exists(
    b_eng_workspace_file_system_object: BEngWorkspaceFileSystemObjects,
) -> bool:
    b_eng_workspace_file_system_object_exists = (
        b_eng_workspace_file_system_object.exists()
    )

    if (
        not b_eng_workspace_file_system_object_exists
    ):
        __report_file_system_object_does_not_exist(
            type_name="bEng workspace file system object",
            file_system_object=b_eng_workspace_file_system_object,
        )

    return b_eng_workspace_file_system_object_exists


def __report_file_system_object_does_not_exist(
    type_name: str,
    file_system_object: FileSystemObjects,
):
    message = (
        type_name
        + " does not exist: "
        + file_system_object.absolute_path_string
    )

    log_message(message)
