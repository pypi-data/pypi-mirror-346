from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from nf_common.code.services.b_eng_python_refactoring_service.common_knowledge.enum_b_eng_folder_types import (
    EnumBEngFolderTypes,
)


class BEngFolders(Folders):
    registry_keyed_on_full_paths = (
        dict()
    )

    def __init__(
        self,
        absolute_path_string: str,
        parent_folder: Folders = None,
        b_eng_folder_type: EnumBEngFolderTypes = EnumBEngFolderTypes.NOT_SET,
        alternative_name: str = None,
    ):
        super().__init__(
            absolute_path_string=absolute_path_string,
            parent_folder=parent_folder,
        )

        self.b_eng_folder_type = (
            b_eng_folder_type
        )

        self.alternative_name = (
            alternative_name
        )

        BEngFolders.registry_keyed_on_full_paths[
            absolute_path_string
        ] = self

        self.uses = []

        self.used_by = []

    @property
    def bitbucket_team_name(
        self,
    ) -> str:
        if (
            self.b_eng_folder_type
            == EnumBEngFolderTypes.BITBUCKET_TEAM
        ):
            return self.base_name

        if (
            self.b_eng_folder_type
            == EnumBEngFolderTypes.WORKSPACE
        ):
            return ""

        return (
            self.parent_folder.bitbucket_team_name
        )

    @property
    def bitbucket_project_name(
        self,
    ) -> str:
        if (
            self.b_eng_folder_type
            == EnumBEngFolderTypes.BITBUCKET_PROJECT
        ):
            return self.base_name

        if (
            self.b_eng_folder_type
            == EnumBEngFolderTypes.WORKSPACE
        ):
            return ""

        return (
            self.parent_folder.bitbucket_project_name
        )

    @property
    def git_repository_name(
        self,
    ) -> str:
        if (
            self.b_eng_folder_type
            == EnumBEngFolderTypes.CODE_REPOSITORY
        ):
            return self.base_name

        if (
            self.b_eng_folder_type
            == EnumBEngFolderTypes.CREATED_DATA_REPOSITORY
        ):
            return self.base_name

        if (
            self.b_eng_folder_type
            == EnumBEngFolderTypes.ORIGINAL_DATA_REPOSITORY
        ):
            return self.base_name

        if (
            self.b_eng_folder_type
            == EnumBEngFolderTypes.WORKSPACE
        ):
            return ""

        return (
            self.parent_folder.git_repository_name
        )
