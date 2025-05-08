from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_project_folder_lists import (
    BEngProjectFolderLists,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_workspace_with_file_system_object_couples_ordered_indexed_lists import (
    BEngWorkspaceWithFileSystemObjectCouplesOrderedIndexedLists,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.configurations.move_and_replace_configuration_flag_sets import (
    MoveAndReplaceConfigurationFlagSets,
)


class MoveAndReplaceConfigurations:
    def __init__(
        self,
        b_eng_workspace_with_file_system_object_couples_ordered_indexed_list: BEngWorkspaceWithFileSystemObjectCouplesOrderedIndexedLists,
        branch_name: str,
        move_and_replace_configuration_flag_set: MoveAndReplaceConfigurationFlagSets,
        in_scope_b_eng_project_folder_list: BEngProjectFolderLists,
        commit_message: str,
    ):
        self.b_eng_workspace_with_file_system_object_couples_ordered_indexed_list = b_eng_workspace_with_file_system_object_couples_ordered_indexed_list

        self.branch_name = branch_name

        self.move_and_replace_configuration_flag_set = move_and_replace_configuration_flag_set

        self.in_scope_b_eng_project_folder_list = in_scope_b_eng_project_folder_list

        self.commit_message = (
            commit_message
        )
