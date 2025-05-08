from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_project_folder_lists import (
    BEngProjectFolderLists,
)
from nf_common.code.services.b_eng_python_refactoring_service.refactor_files.replace_references.b_eng_project_python_reference_replacer import (
    replace_python_reference_in_b_eng_project,
)


def replace_python_reference_in_b_eng_projects(
    source_reference: str,
    target_reference: str,
    in_scope_b_eng_project_folder_list: BEngProjectFolderLists,
):
    for (
        b_eng_project_folder
    ) in (
        in_scope_b_eng_project_folder_list.list
    ):
        replace_python_reference_in_b_eng_project(
            source_reference=source_reference,
            target_reference=target_reference,
            b_eng_project_folder=b_eng_project_folder,
        )
