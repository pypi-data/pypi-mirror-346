from bclearer_core.constants.standard_constants import (
    CODE_FOLDER_NAME,
    EXECUTABLES_FOLDER_NAME,
    FOLDER_DELIMITER,
    LOCAL_GIT_REPOSITORY_FOLDER_NAME,
    SANDPIT_FOLDER_NAME,
)
from nf_common.code.services.b_eng_python_refactoring_service.common_knowledge.enum_b_eng_folder_types import (
    EnumBEngFolderTypes,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_folders import (
    BEngFolders,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_folders import (
    BEngWorkspaceFolders,
)


def get_b_eng_folder_type(
    child_folder_name: str,
    parent_folder: BEngFolders,
) -> EnumBEngFolderTypes:
    if __is_bitbucket_team_folder(
        parent_folder=parent_folder,
    ):
        return (
            EnumBEngFolderTypes.BITBUCKET_TEAM
        )

    if (
        parent_folder.b_eng_folder_type
        is EnumBEngFolderTypes.BITBUCKET_TEAM
    ):
        return (
            EnumBEngFolderTypes.BITBUCKET_PROJECT
        )

    if __is_git_repositories_folder(
        child_folder_name=child_folder_name,
    ):
        return (
            EnumBEngFolderTypes.GIT_REPOSITORIES
        )

    if (
        parent_folder.b_eng_folder_type
        is EnumBEngFolderTypes.GIT_REPOSITORIES
    ):
        return __get_git_repository_folder_type(
            child_folder_name=child_folder_name,
        )

    if (
        parent_folder.b_eng_folder_type
        is EnumBEngFolderTypes.CREATED_DATA_REPOSITORY
    ):
        return (
            EnumBEngFolderTypes.DATA_FOLDER
        )

    if (
        parent_folder.b_eng_folder_type
        is EnumBEngFolderTypes.ORIGINAL_DATA_REPOSITORY
    ):
        return (
            EnumBEngFolderTypes.DATA_FOLDER
        )

    if child_folder_name.endswith(
        FOLDER_DELIMITER
        + CODE_FOLDER_NAME
        + FOLDER_DELIMITER,
    ):
        return (
            EnumBEngFolderTypes.CODE_FOLDER
        )

    if child_folder_name.endswith(
        FOLDER_DELIMITER
        + SANDPIT_FOLDER_NAME
        + FOLDER_DELIMITER,
    ):
        return (
            EnumBEngFolderTypes.SANDPIT_FOLDER
        )

    if child_folder_name.endswith(
        FOLDER_DELIMITER
        + EXECUTABLES_FOLDER_NAME
        + FOLDER_DELIMITER,
    ):
        return (
            EnumBEngFolderTypes.EXECUTABLES_FOLDER
        )

    if (
        parent_folder.b_eng_folder_type
        is EnumBEngFolderTypes.CODE_REPOSITORY
    ):
        return (
            EnumBEngFolderTypes.REPOSITORY_ROOT_FOLDER
        )

    if (
        parent_folder.b_eng_folder_type
        is EnumBEngFolderTypes.DATABASE_OUTPUTS_REPOSITORY
    ):
        return (
            EnumBEngFolderTypes.DATABASE_OUTPUTS_FOLDER
        )

    if (
        parent_folder.b_eng_folder_type
        is EnumBEngFolderTypes.CODE_FOLDER
    ):
        return (
            EnumBEngFolderTypes.CODE_FOLDER
        )

    if (
        parent_folder.b_eng_folder_type
        is EnumBEngFolderTypes.SANDPIT_FOLDER
    ):
        return (
            EnumBEngFolderTypes.SANDPIT_FOLDER
        )

    if (
        parent_folder.b_eng_folder_type
        is EnumBEngFolderTypes.EXECUTABLES_FOLDER
    ):
        return (
            EnumBEngFolderTypes.EXECUTABLES_FOLDER
        )

    return EnumBEngFolderTypes.NOT_SET


def __is_bitbucket_team_folder(
    parent_folder: BEngFolders,
) -> bool:
    if isinstance(
        parent_folder,
        BEngWorkspaceFolders,
    ):
        return True

    if (
        parent_folder.b_eng_folder_type
        is EnumBEngFolderTypes.WORKSPACE
    ):
        return True

    return False


def __is_git_repositories_folder(
    child_folder_name: str,
) -> bool:
    return child_folder_name.endswith(
        LOCAL_GIT_REPOSITORY_FOLDER_NAME
        + FOLDER_DELIMITER,
    )


def __get_git_repository_folder_type(
    child_folder_name: str,
) -> EnumBEngFolderTypes:
    if child_folder_name.endswith(
        "_cd" + FOLDER_DELIMITER,
    ):
        return (
            EnumBEngFolderTypes.CREATED_DATA_REPOSITORY
        )

    if child_folder_name.endswith(
        "_od" + FOLDER_DELIMITER,
    ):
        return (
            EnumBEngFolderTypes.ORIGINAL_DATA_REPOSITORY
        )

    if child_folder_name.endswith(
        "_database_templates"
        + FOLDER_DELIMITER,
    ):
        return (
            EnumBEngFolderTypes.DATABASE_OUTPUTS_REPOSITORY
        )

    return (
        EnumBEngFolderTypes.CODE_REPOSITORY
    )
