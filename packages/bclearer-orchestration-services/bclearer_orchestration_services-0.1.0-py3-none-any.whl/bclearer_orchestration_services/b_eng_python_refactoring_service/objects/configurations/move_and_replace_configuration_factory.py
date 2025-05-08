from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_project_folder_lists import (
    BEngProjectFolderLists,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_project_folders import (
    BEngProjectFolders,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_file_system_object_couple_ordered_indexed_lists import (
    BEngWorkspaceFileSystemObjectCouplesOrderedIndexedLists,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_file_system_object_couples import (
    BEngWorkspaceFileSystemObjectCouples,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_file_system_objects import (
    BEngWorkspaceFileSystemObjects,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_folders import (
    BEngWorkspaceFolders,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_workspace_with_file_system_object_couples_ordered_indexed_lists import (
    BEngWorkspaceWithFileSystemObjectCouplesOrderedIndexedLists,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.configurations.move_and_replace_configuration_flag_sets import (
    MoveAndReplaceConfigurationFlagSets,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.configurations.move_and_replace_configurations import (
    MoveAndReplaceConfigurations,
)


def create_move_and_replace_configuration(
    workspace_path_string: str,
    branch_name: str,
    dictionary_of_relative_path_string_couples: dict,
    list_of_in_scope_b_eng_project_names: list,
    create_new_folders_flag: bool,
    check_source_exists: bool,
    check_target_exists: bool,
    check_workspace_exists: bool,
    commit_changes_flag: bool,
    commit_message: str,
) -> MoveAndReplaceConfigurations:
    b_eng_workspace_folder = (
        BEngWorkspaceFolders(
            workspace_path_string,
        )
    )

    path_couples_ordered_indexed_list = get_path_couples_ordered_indexed_list(
        b_eng_workspace_folder=b_eng_workspace_folder,
        dictionary_of_relative_path_string_couples=dictionary_of_relative_path_string_couples,
    )

    b_eng_workspace_with_file_system_object_couples_ordered_indexed_list = BEngWorkspaceWithFileSystemObjectCouplesOrderedIndexedLists(
        b_eng_workspace_folder=b_eng_workspace_folder,
        b_eng_workspace_file_system_object_couples_ordered_indexed_list=path_couples_ordered_indexed_list,
    )

    move_and_replace_configuration_flag_set = MoveAndReplaceConfigurationFlagSets(
        create_new_folders_flag=create_new_folders_flag,
        check_source_exists=check_source_exists,
        check_target_exists=check_target_exists,
        check_workspace_exists=check_workspace_exists,
        commit_changes_flag=commit_changes_flag,
    )

    in_scope_bitbucket_project_list = get_in_scope_b_eng_project_list(
        b_eng_workspace_folder=b_eng_workspace_folder,
        list_of_in_scope_b_eng_project_names=list_of_in_scope_b_eng_project_names,
    )

    move_and_replace_configuration = MoveAndReplaceConfigurations(
        b_eng_workspace_with_file_system_object_couples_ordered_indexed_list=b_eng_workspace_with_file_system_object_couples_ordered_indexed_list,
        branch_name=branch_name,
        move_and_replace_configuration_flag_set=move_and_replace_configuration_flag_set,
        in_scope_b_eng_project_folder_list=in_scope_bitbucket_project_list,
        commit_message=commit_message,
    )

    return (
        move_and_replace_configuration
    )


def get_path_couples_ordered_indexed_list(
    b_eng_workspace_folder: BEngWorkspaceFolders,
    dictionary_of_relative_path_string_couples: dict,
) -> BEngWorkspaceFileSystemObjectCouplesOrderedIndexedLists:
    ordered_indexed_list = {}

    for (
        index,
        relative_path_string_couple,
    ) in (
        dictionary_of_relative_path_string_couples.items()
    ):
        ordered_indexed_list[index] = (
            BEngWorkspaceFileSystemObjectCouples(
                place_1_b_eng_workspace_file_system_object=BEngWorkspaceFileSystemObjects(
                    b_eng_workspace_folder=b_eng_workspace_folder,
                    relative_path_from_workspace_string=relative_path_string_couple[
                        0
                    ],
                ),
                place_2_b_eng_workspace_file_system_object=BEngWorkspaceFileSystemObjects(
                    b_eng_workspace_folder=b_eng_workspace_folder,
                    relative_path_from_workspace_string=relative_path_string_couple[
                        1
                    ],
                ),
            )
        )

    path_couples_ordered_indexed_list = BEngWorkspaceFileSystemObjectCouplesOrderedIndexedLists(
        ordered_indexed_list=ordered_indexed_list,
    )

    return path_couples_ordered_indexed_list


def get_in_scope_b_eng_project_list(
    b_eng_workspace_folder: BEngWorkspaceFolders,
    list_of_in_scope_b_eng_project_names: list,
) -> BEngProjectFolderLists:
    list_of_b_eng_project_folders = []

    for (
        in_scope_b_eng_project_name
    ) in list_of_in_scope_b_eng_project_names:
        list_of_b_eng_project_folders.append(
            BEngProjectFolders(
                b_eng_workspace_folder=b_eng_workspace_folder,
                b_eng_project_name=in_scope_b_eng_project_name,
            ),
        )

    in_scope_b_eng_project_folder_list = BEngProjectFolderLists(
        list_items=list_of_b_eng_project_folders,
    )

    return in_scope_b_eng_project_folder_list
