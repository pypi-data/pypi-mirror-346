from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_folders import (
    BEngFolders,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_folders import (
    BEngWorkspaceFolders,
)


class BEngProjectFolders(BEngFolders):
    def __init__(
        self,
        b_eng_workspace_folder: BEngWorkspaceFolders,
        b_eng_project_name: str,
        parent_folder: Folders = None,
    ):
        self.b_eng_workspace_folder = (
            b_eng_workspace_folder
        )

        self.b_eng_project_name = (
            b_eng_project_name
        )

        absolute_path_string = b_eng_workspace_folder.extend_path(
            b_eng_project_name,
        )

        super().__init__(
            absolute_path_string=absolute_path_string,
            parent_folder=parent_folder,
        )
