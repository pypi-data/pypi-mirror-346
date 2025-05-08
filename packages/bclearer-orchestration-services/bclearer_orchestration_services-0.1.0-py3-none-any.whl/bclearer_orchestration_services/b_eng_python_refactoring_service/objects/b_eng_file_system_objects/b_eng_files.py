from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


class BEngFiles(Files):
    registry_keyed_on_full_paths = (
        dict()
    )

    def __init__(
        self,
        absolute_path_string: str,
        parent_folder: Folders = None,
        alternative_name: str = None,
    ):
        super().__init__(
            absolute_path_string=absolute_path_string,
            parent_folder=parent_folder,
        )

        self.alternative_name = (
            alternative_name
        )

        BEngFiles.registry_keyed_on_full_paths[
            absolute_path_string
        ] = self

        self.uses = []

        self.used_by = []

    @property
    def bitbucket_team_name(
        self,
    ) -> str:
        return (
            self.parent_folder.bitbucket_team_name
        )

    @property
    def bitbucket_project_name(
        self,
    ) -> str:
        return (
            self.parent_folder.bitbucket_project_name
        )

    @property
    def git_repository_name(
        self,
    ) -> str:
        return (
            self.parent_folder.git_repository_name
        )
