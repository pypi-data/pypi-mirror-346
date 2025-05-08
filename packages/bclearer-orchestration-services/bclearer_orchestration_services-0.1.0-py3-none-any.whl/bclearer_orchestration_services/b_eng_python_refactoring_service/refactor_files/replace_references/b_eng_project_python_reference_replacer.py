import os
from pathlib import Path

from bclearer_interop_services.file_system_service.file_content_replacer import (
    replace_string_in_file,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_project_folders import (
    BEngProjectFolders,
)


def replace_python_reference_in_b_eng_project(
    source_reference: str,
    target_reference: str,
    b_eng_project_folder: BEngProjectFolders,
):
    local_git_repositories_folder = Path(
        b_eng_project_folder.absolute_path_string,
        "local_git_repositories",
    )

    for path, folders, files in os.walk(
        str(
            local_git_repositories_folder,
        ),
    ):
        __replace_reference_in_folder(
            path=path,
            files=files,
            source_reference=source_reference,
            target_reference=target_reference,
        )


def __replace_reference_in_folder(
    path: str,
    files: list,
    source_reference: str,
    target_reference: str,
):
    if ".git" in path:
        return

    if "__pycache__" in path:
        return

    for file_name in files:
        __replace_reference_in_file(
            file_path=Path(
                path,
                file_name,
            ),
            source_reference=source_reference,
            target_reference=target_reference,
        )


def __replace_reference_in_file(
    file_path: Path,
    source_reference: str,
    target_reference: str,
):
    __replace_reference_with_prefix_in_file(
        file_path=file_path,
        source_reference=source_reference,
        target_reference=target_reference,
        prefix="from",
        file_extension="py",
    )

    __replace_reference_with_prefix_in_file(
        file_path=file_path,
        source_reference=source_reference,
        target_reference=target_reference,
        prefix="import",
        file_extension="py",
    )

    __replace_reference_with_prefix_in_file(
        file_path=file_path,
        source_reference=source_reference,
        target_reference=target_reference,
        prefix="include",
        file_extension="in",
    )


def __replace_reference_with_prefix_in_file(
    file_path: Path,
    source_reference: str,
    target_reference: str,
    prefix: str,
    file_extension: str,
):
    replace_string_in_file(
        file_path=file_path,
        source_string=prefix
        + " "
        + source_reference,
        target_string=prefix
        + " "
        + target_reference,
        file_extension=file_extension,
    )
