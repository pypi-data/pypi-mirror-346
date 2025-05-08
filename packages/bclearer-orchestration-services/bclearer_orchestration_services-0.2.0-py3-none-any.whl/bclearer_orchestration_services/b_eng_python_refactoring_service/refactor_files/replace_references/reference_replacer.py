from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_project_folder_lists import (
    BEngProjectFolderLists,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_file_system_object_couples import (
    BEngWorkspaceFileSystemObjectCouples,
)
from nf_common.code.services.b_eng_python_refactoring_service.refactor_files.replace_references.b_eng_projects_python_reference_replacer import (
    replace_python_reference_in_b_eng_projects,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def replace_references_in_python_code(
    source_target_path_couple: BEngWorkspaceFileSystemObjectCouples,
    in_scope_b_eng_project_folder_list: BEngProjectFolderLists,
):
    source_reference = (
        source_target_path_couple.place_1_b_eng_workspace_file_system_object.get_reference_from_b_eng_workspace_file_system_object()
    )

    target_reference = (
        source_target_path_couple.place_2_b_eng_workspace_file_system_object.get_reference_from_b_eng_workspace_file_system_object()
    )

    log_message("Updating references:")

    log_message(
        "\tfrom: " + source_reference,
    )

    log_message(
        "\t  to: " + target_reference,
    )

    replace_python_reference_in_b_eng_projects(
        source_reference=source_reference,
        target_reference=target_reference,
        in_scope_b_eng_project_folder_list=in_scope_b_eng_project_folder_list,
    )
