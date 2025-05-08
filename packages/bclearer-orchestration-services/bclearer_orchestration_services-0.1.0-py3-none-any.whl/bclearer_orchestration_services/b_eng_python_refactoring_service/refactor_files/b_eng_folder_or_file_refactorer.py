from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_project_folder_lists import (
    BEngProjectFolderLists,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_file_system_object_couples import (
    BEngWorkspaceFileSystemObjectCouples,
)
from nf_common.code.services.b_eng_python_refactoring_service.refactor_files.move_and_rename_folders_and_files.folder_or_file_move_and_renamer import (
    move_and_rename_file_or_folder,
)
from nf_common.code.services.b_eng_python_refactoring_service.refactor_files.replace_references.reference_replacer import (
    replace_references_in_python_code,
)


def move_and_rename_file_or_folder_then_find_and_replace_references_in_python_code(
    source_target_path_couple: BEngWorkspaceFileSystemObjectCouples,
    in_scope_bitbucket_project_list: BEngProjectFolderLists,
):
    move_and_rename_file_or_folder(
        source_target_b_eng_workspace_file_system_object_couple=source_target_path_couple,
    )

    replace_references_in_python_code(
        source_target_path_couple=source_target_path_couple,
        in_scope_b_eng_project_folder_list=in_scope_bitbucket_project_list,
    )
