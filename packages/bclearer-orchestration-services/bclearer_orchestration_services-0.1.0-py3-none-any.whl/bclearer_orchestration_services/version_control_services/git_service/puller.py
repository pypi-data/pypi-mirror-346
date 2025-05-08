from pathlib import Path

import git
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def pull_git_repository(
    repository_folder_path: Path,
    branch_name: str,
):
    log_message(
        message="Pulling: "
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

    pull_command = "git pull"

    repository.git.execute(
        command=pull_command,
    )
