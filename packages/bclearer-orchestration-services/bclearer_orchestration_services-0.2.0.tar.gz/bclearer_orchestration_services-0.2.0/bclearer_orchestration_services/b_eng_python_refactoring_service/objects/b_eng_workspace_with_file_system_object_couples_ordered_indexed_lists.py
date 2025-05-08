from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_file_system_object_couple_ordered_indexed_lists import (
    BEngWorkspaceFileSystemObjectCouplesOrderedIndexedLists,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_folders import (
    BEngWorkspaceFolders,
)


class BEngWorkspaceWithFileSystemObjectCouplesOrderedIndexedLists:
    def __init__(
        self,
        b_eng_workspace_folder: BEngWorkspaceFolders,
        b_eng_workspace_file_system_object_couples_ordered_indexed_list: BEngWorkspaceFileSystemObjectCouplesOrderedIndexedLists,
    ):
        self.b_eng_workspace_folder = (
            b_eng_workspace_folder
        )

        self.b_eng_workspace_file_system_object_couples_ordered_indexed_list = b_eng_workspace_file_system_object_couples_ordered_indexed_list

    def get_indexed_file_system_object_couple(
        self,
        index,
    ):
        indexed_file_system_object_couple = self.b_eng_workspace_file_system_object_couples_ordered_indexed_list.get_path_couple_with_index(
            index,
        )

        return indexed_file_system_object_couple
