import os

from nf_common.code.services.b_eng_python_refactoring_service.common_knowledge.enum_b_eng_folder_types import (
    EnumBEngFolderTypes,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_folders import (
    BEngFolders,
)


def get_b_eng_folder_alternative_name(
    folder_name: str,
    parent_folder: BEngFolders,
) -> str:
    folder_base_name = os.path.basename(
        os.path.normpath(folder_name),
    )

    name_list = [folder_base_name]

    b_eng_folder_alternative_name = (
        __get_alternative_name(
            name_list=name_list,
            parent_folder=parent_folder,
        )
    )

    return b_eng_folder_alternative_name


def get_b_eng_file_alternative_name(
    file_name: str,
    parent_folder: BEngFolders,
) -> str:
    name_list = [file_name[:-3]]

    b_eng_folder_alternative_name = (
        __get_alternative_name(
            name_list=name_list,
            parent_folder=parent_folder,
        )
    )

    return b_eng_folder_alternative_name


def __get_alternative_name(
    name_list: list,
    parent_folder: BEngFolders,
) -> str:
    if (
        parent_folder.b_eng_folder_type
        == EnumBEngFolderTypes.WORKSPACE
    ):
        return ""

    alternative_name_reverse_list = __get_alternative_name_reverse_list(
        name_list=name_list,
        parent_folder=parent_folder,
    )

    alternative_name_list = reversed(
        alternative_name_reverse_list,
    )

    alternative_name = ".".join(
        alternative_name_list,
    )

    return alternative_name


def __get_alternative_name_reverse_list(
    name_list: list,
    parent_folder: BEngFolders,
) -> list:
    if (
        parent_folder.b_eng_folder_type
        == EnumBEngFolderTypes.CODE_REPOSITORY
    ):
        return name_list

    if (
        parent_folder.b_eng_folder_type
        == EnumBEngFolderTypes.WORKSPACE
    ):
        return []

    name_list.append(
        parent_folder.base_name,
    )

    alternative_name_reverse_list = __get_alternative_name_reverse_list(
        name_list=name_list,
        parent_folder=parent_folder.parent_folder,
    )

    return alternative_name_reverse_list
