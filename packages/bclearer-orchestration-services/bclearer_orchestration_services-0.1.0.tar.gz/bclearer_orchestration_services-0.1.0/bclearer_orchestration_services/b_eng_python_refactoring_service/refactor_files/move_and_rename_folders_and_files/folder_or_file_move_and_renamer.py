from bclearer_interop_services.file_system_service.file_or_folder_mover import (
    move_file_or_folder_and_create_sub_folders,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_file_system_object_couples import (
    BEngWorkspaceFileSystemObjectCouples,
)
from nf_common.code.services.b_eng_python_refactoring_service.refactor_files.move_and_rename_folders_and_files.folder_or_file_move_and_rename_checker import (
    move_and_rename_file_or_folder_checks,
)
from nf_common.code.services.b_eng_python_refactoring_service.refactor_files.move_and_rename_folders_and_files.folders_init_adder import (
    add_init_files_if_required,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def move_and_rename_file_or_folder(
    source_target_b_eng_workspace_file_system_object_couple: BEngWorkspaceFileSystemObjectCouples,
):
    check_results = move_and_rename_file_or_folder_checks(
        source_target_b_eng_workspace_file_system_object_couple=source_target_b_eng_workspace_file_system_object_couple,
    )

    if not check_results:
        return

    source_object = (
        source_target_b_eng_workspace_file_system_object_couple.place_1_b_eng_workspace_file_system_object
    )

    target_object = (
        source_target_b_eng_workspace_file_system_object_couple.place_2_b_eng_workspace_file_system_object
    )

    log_message("Moving:")

    log_message(
        "\t  from: "
        + source_object.absolute_path_string,
    )

    log_message(
        "\t    to: "
        + target_object.absolute_path_string,
    )

    move_file_or_folder_and_create_sub_folders(
        source_object=source_object,
        target_object=target_object,
    )

    add_init_files_if_required(
        target_object=target_object,
    )
