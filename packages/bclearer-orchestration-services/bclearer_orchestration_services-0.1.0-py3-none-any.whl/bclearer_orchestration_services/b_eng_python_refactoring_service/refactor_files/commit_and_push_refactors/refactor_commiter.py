import os
from pathlib import Path

from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_project_folder_lists import (
    BEngProjectFolderLists,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_project_folders import (
    BEngProjectFolders,
)
from nf_common.code.services.version_control_services.git_service.commit_and_pusher import (
    add_commit_and_push_local_repository,
)


def commit_refactors(
    branch_name: str,
    in_scope_b_eng_project_folder_list: BEngProjectFolderLists,
    commit_message: str,
):
    for (
        b_eng_project_folder
    ) in (
        in_scope_b_eng_project_folder_list.list
    ):
        __commit_refactors_in_b_eng_project_folder(
            branch_name=branch_name,
            b_eng_project_folder=b_eng_project_folder,
            commit_message=commit_message,
        )


def __commit_refactors_in_b_eng_project_folder(
    branch_name: str,
    b_eng_project_folder: BEngProjectFolders,
    commit_message: str,
):
    local_git_repositories_folder_name = Path(
        b_eng_project_folder.absolute_path_string,
        "local_git_repositories",
    )

    folder_paths = [
        os_object.path
        for os_object in os.scandir(
            str(
                local_git_repositories_folder_name,
            ),
        )
        if os_object.is_dir()
    ]

    for folder_path in folder_paths:
        __commit_refactors_in_git_repository(
            local_git_repository_folder_path=folder_path,
            branch_name=branch_name,
            commit_message=commit_message,
        )


def __commit_refactors_in_git_repository(
    local_git_repository_folder_path: str,
    branch_name: str,
    commit_message: str,
):
    add_commit_and_push_local_repository(
        repository_folder_path=Path(
            local_git_repository_folder_path,
        ),
        branch_name=branch_name,
        commit_message=commit_message,
    )
