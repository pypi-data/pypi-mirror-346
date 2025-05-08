from pathlib import Path

import git
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def add_commit_and_push_local_repository(
    repository_folder_path: Path,
    branch_name: str,
    commit_message: str,
):
    log_message(
        message="Adding, Committing and Pushing: "
        + str(
            repository_folder_path.parts[
                -1
            ],
        ),
    )

    repository = git.Repo.init(
        str(repository_folder_path),
    )

    active_branch_is_required_branch = (
        repository.active_branch.name
        == branch_name
    )

    if (
        not active_branch_is_required_branch
    ):
        return

    __add_all_files_to_stage(
        repository=repository,
    )

    __commit_stage(
        repository=repository,
        commit_message=commit_message,
    )

    __push_stage(
        repository=repository,
        branch_name=branch_name,
    )


def __add_all_files_to_stage(
    repository: git.Repo,
):
    add_files_command = "git add -A"

    repository.git.execute(
        command=add_files_command,
    )


def __commit_stage(
    repository: git.Repo,
    commit_message: str,
):
    commit_command = (
        'git commit -am "'
        + commit_message
        + '"'
    )

    try:
        repository.git.execute(
            commit_command,
        )

    except Exception as exception:
        log_message(
            message="Cannot commit "
            + str(repository)
            + " because "
            + str(exception),
        )


def __push_stage(
    repository: git.Repo,
    branch_name: str,
):
    add_push_command = (
        "git push -u "
        + " origin "
        + " "
        + branch_name
        + " "
    )

    repository.git.execute(
        add_push_command,
    )
