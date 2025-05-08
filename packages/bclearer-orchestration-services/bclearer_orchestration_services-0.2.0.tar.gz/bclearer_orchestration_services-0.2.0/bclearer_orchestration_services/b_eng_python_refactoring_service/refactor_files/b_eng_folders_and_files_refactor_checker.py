from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_project_folder_lists import (
    BEngProjectFolderLists,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_project_folders import (
    BEngProjectFolders,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_folders import (
    BEngWorkspaceFolders,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def b_eng_folders_and_files_refactor_checks(
    b_eng_workspace_folder: BEngWorkspaceFolders,
    in_scope_b_eng_project_folder_list: BEngProjectFolderLists,
) -> bool:
    check_result = __check_b_eng_workspace_folder_exists(
        b_eng_workspace_folder=b_eng_workspace_folder,
    )

    if not check_result:
        return check_result

    check_result = __check_b_eng_project_folders_exist(
        b_eng_project_folder_list=in_scope_b_eng_project_folder_list,
    )

    return check_result


def __check_b_eng_workspace_folder_exists(
    b_eng_workspace_folder: BEngWorkspaceFolders,
) -> bool:
    workspace_exists = (
        b_eng_workspace_folder.exists()
    )

    if not workspace_exists:
        __report_file_system_object_does_not_exist(
            type_name="bEng workspace folder",
            file_system_object=b_eng_workspace_folder,
        )

    return workspace_exists


def __check_b_eng_project_folders_exist(
    b_eng_project_folder_list: BEngProjectFolderLists,
) -> bool:
    for (
        b_eng_project_folder
    ) in b_eng_project_folder_list.list:
        b_eng_project_exists = __check_b_eng_project_folder_exists(
            b_eng_project_folder=b_eng_project_folder,
        )

        if not b_eng_project_exists:
            return False

    return True


def __check_b_eng_project_folder_exists(
    b_eng_project_folder: BEngProjectFolders,
) -> bool:
    bitbucket_project_exists = (
        b_eng_project_folder.exists()
    )

    if not bitbucket_project_exists:
        __report_file_system_object_does_not_exist(
            type_name="bEng project folder",
            file_system_object=b_eng_project_folder,
        )

    return bitbucket_project_exists


def __report_file_system_object_does_not_exist(
    type_name: str,
    file_system_object: FileSystemObjects,
):
    message = (
        type_name
        + " does not exist: "
        + file_system_object.absolute_path_string
    )

    log_message(message)
