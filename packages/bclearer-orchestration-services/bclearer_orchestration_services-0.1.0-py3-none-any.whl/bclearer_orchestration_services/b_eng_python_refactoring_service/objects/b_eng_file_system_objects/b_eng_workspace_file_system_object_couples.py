from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_file_system_objects import (
    BEngWorkspaceFileSystemObjects,
)


class BEngWorkspaceFileSystemObjectCouples:
    def __init__(
        self,
        place_1_b_eng_workspace_file_system_object: BEngWorkspaceFileSystemObjects,
        place_2_b_eng_workspace_file_system_object: BEngWorkspaceFileSystemObjects,
    ):
        self.place_1_b_eng_workspace_file_system_object = place_1_b_eng_workspace_file_system_object

        self.place_2_b_eng_workspace_file_system_object = place_2_b_eng_workspace_file_system_object
