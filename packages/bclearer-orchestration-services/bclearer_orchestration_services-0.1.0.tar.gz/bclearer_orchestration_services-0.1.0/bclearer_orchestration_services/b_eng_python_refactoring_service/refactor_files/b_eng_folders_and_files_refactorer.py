from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_project_folder_lists import (
    BEngProjectFolderLists,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_workspace_with_file_system_object_couples_ordered_indexed_lists import (
    BEngWorkspaceWithFileSystemObjectCouplesOrderedIndexedLists,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.configurations.move_and_replace_configurations import (
    MoveAndReplaceConfigurations,
)
from nf_common.code.services.b_eng_python_refactoring_service.refactor_files.b_eng_folder_or_file_refactorer import (
    move_and_rename_file_or_folder_then_find_and_replace_references_in_python_code,
)
from nf_common.code.services.b_eng_python_refactoring_service.refactor_files.b_eng_folders_and_files_refactor_checker import (
    b_eng_folders_and_files_refactor_checks,
)
from nf_common.code.services.b_eng_python_refactoring_service.refactor_files.commit_and_push_refactors.refactor_commiter import (
    commit_refactors,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def move_and_rename_files_or_folders_then_find_and_replace_references_in_python_code(
    move_and_replace_configuration: MoveAndReplaceConfigurations,
) -> bool:
    check_result = b_eng_folders_and_files_refactor_checks(
        b_eng_workspace_folder=move_and_replace_configuration.b_eng_workspace_with_file_system_object_couples_ordered_indexed_list.b_eng_workspace_folder,
        in_scope_b_eng_project_folder_list=move_and_replace_configuration.in_scope_b_eng_project_folder_list,
    )

    if not check_result:
        return False

    __iterate_through_path_couples_in_index_order(
        b_eng_workspace_with_file_system_object_couples_ordered_indexed_list=move_and_replace_configuration.b_eng_workspace_with_file_system_object_couples_ordered_indexed_list,
        in_scope_b_eng_project_folder_list=move_and_replace_configuration.in_scope_b_eng_project_folder_list,
    )

    if (
        move_and_replace_configuration.move_and_replace_configuration_flag_set.commit_changes_flag
    ):
        commit_refactors(
            branch_name=move_and_replace_configuration.branch_name,
            in_scope_b_eng_project_folder_list=move_and_replace_configuration.in_scope_b_eng_project_folder_list,
            commit_message=move_and_replace_configuration.commit_message,
        )

    return True


def __initial_checks():
    pass


def __iterate_through_path_couples_in_index_order(
    b_eng_workspace_with_file_system_object_couples_ordered_indexed_list: BEngWorkspaceWithFileSystemObjectCouplesOrderedIndexedLists,
    in_scope_b_eng_project_folder_list: BEngProjectFolderLists,
):
    path_couples_ordered_indexed_list = (
        b_eng_workspace_with_file_system_object_couples_ordered_indexed_list.b_eng_workspace_file_system_object_couples_ordered_indexed_list
    )

    path_couples_index_ordered_iterator = (
        path_couples_ordered_indexed_list.get_ordered_iterator()
    )

    for (
        path_couples_index
    ) in path_couples_index_ordered_iterator:
        __process_path_couples_index(
            workspace_path_couples_ordered_indexed_list=b_eng_workspace_with_file_system_object_couples_ordered_indexed_list,
            path_couples_index=path_couples_index,
            in_scope_bitbucket_project_list=in_scope_b_eng_project_folder_list,
        )


def __process_path_couples_index(
    workspace_path_couples_ordered_indexed_list: BEngWorkspaceWithFileSystemObjectCouplesOrderedIndexedLists,
    path_couples_index: int,
    in_scope_bitbucket_project_list: BEngProjectFolderLists,
):
    log_message(
        "Processing index:"
        + str(path_couples_index),
    )

    source_target_path_couple = workspace_path_couples_ordered_indexed_list.get_indexed_file_system_object_couple(
        index=path_couples_index,
    )

    move_and_rename_file_or_folder_then_find_and_replace_references_in_python_code(
        source_target_path_couple=source_target_path_couple,
        in_scope_bitbucket_project_list=in_scope_bitbucket_project_list,
    )
