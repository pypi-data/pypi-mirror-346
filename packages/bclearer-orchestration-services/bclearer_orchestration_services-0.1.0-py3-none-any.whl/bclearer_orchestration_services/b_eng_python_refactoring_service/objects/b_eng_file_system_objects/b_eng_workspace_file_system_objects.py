from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from nf_common.code.services.b_eng_python_refactoring_service.constants.b_eng_file_system_constants import (
    RELATIVE_PATH_ROOT_CODE_FOLDER_POSITION,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_folders import (
    BEngWorkspaceFolders,
)


class BEngWorkspaceFileSystemObjects(
    FileSystemObjects,
):
    def __init__(
        self,
        b_eng_workspace_folder: BEngWorkspaceFolders,
        relative_path_from_workspace_string: str,
    ):
        self.b_eng_workspace_folder = (
            b_eng_workspace_folder
        )

        absolute_path_string = b_eng_workspace_folder.extend_path(
            path_extension=relative_path_from_workspace_string,
        )

        super().__init__(
            absolute_path_string=absolute_path_string,
        )

    def get_code_folders(self):
        b_eng_workspace_folder_index = (
            self.b_eng_workspace_folder.item_count()
        )

        code_start_index = (
            b_eng_workspace_folder_index
            + RELATIVE_PATH_ROOT_CODE_FOLDER_POSITION
        )

        code_folder_components = (
            self.list_of_components()[
                code_start_index:
            ]
        )

        if code_folder_components[
            -1
        ].endswith(".py"):
            code_folder_components = (
                code_folder_components[
                    :-1
                ]
            )

        relative_code_folder_path_strings = (
            []
        )

        relative_path_from_workspace_string = "/".join(
            self.list_of_components()[
                b_eng_workspace_folder_index:code_start_index
            ],
        )

        for (
            code_folder_component
        ) in code_folder_components:
            relative_path_from_workspace_string = "/".join(
                [
                    relative_path_from_workspace_string,
                    code_folder_component,
                ],
            )

            relative_code_folder_path_strings.append(
                relative_path_from_workspace_string,
            )

        code_folders = []

        for relative_code_folder_path_string in relative_code_folder_path_strings:
            code_folder = BEngWorkspaceFileSystemObjects(
                b_eng_workspace_folder=self.b_eng_workspace_folder,
                relative_path_from_workspace_string=relative_code_folder_path_string,
            )

            code_folders.append(
                code_folder,
            )

        return code_folders

    def get_reference_from_b_eng_workspace_file_system_object(
        self,
    ) -> str:
        b_eng_workspace_folder_index = (
            self.b_eng_workspace_folder.item_count()
        )

        code_start_index = (
            b_eng_workspace_folder_index
            + RELATIVE_PATH_ROOT_CODE_FOLDER_POSITION
        )

        code_folder_components = (
            self.list_of_components()[
                code_start_index:
            ]
        )

        reference_string = ".".join(
            code_folder_components,
        )

        if reference_string.endswith(
            ".py",
        ):
            reference_string = (
                reference_string[:-3]
            )

        return reference_string
