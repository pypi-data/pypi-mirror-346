import glob

from nf_common.code.services.b_eng_python_refactoring_service.b_eng_structure_and_contents.b_eng_structure.b_eng_child_file_structure_collectors import (
    collect_child_files_structure,
)
from nf_common.code.services.b_eng_python_refactoring_service.b_eng_structure_and_contents.b_eng_structure.b_eng_file_system_alternative_name_getters import (
    get_b_eng_folder_alternative_name,
)
from nf_common.code.services.b_eng_python_refactoring_service.b_eng_structure_and_contents.b_eng_structure.b_eng_folder_type_getters import (
    get_b_eng_folder_type,
)
from nf_common.code.services.b_eng_python_refactoring_service.common_knowledge.enum_b_eng_folder_types import (
    EnumBEngFolderTypes,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_folders import (
    BEngFolders,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_python_reference_dictionaries import (
    BEngPythonReferenceDictionaries,
)


def collect_child_folders_structure(
    parent_folder: BEngFolders,
    b_eng_python_reference_dictionary: BEngPythonReferenceDictionaries,
):
    child_folder_names = [
        child_folder_name
        for child_folder_name in glob.glob(
            parent_folder.absolute_path_string
            + "/**/",
            recursive=False,
        )
    ]

    for (
        child_folder_name
    ) in child_folder_names:
        __collect_folder_if_required(
            child_folder_name=child_folder_name,
            parent_folder=parent_folder,
            b_eng_python_reference_dictionary=b_eng_python_reference_dictionary,
        )


def __collect_folder_if_required(
    child_folder_name: str,
    parent_folder: BEngFolders,
    b_eng_python_reference_dictionary: BEngPythonReferenceDictionaries,
):
    b_eng_folder_type = get_b_eng_folder_type(
        child_folder_name=child_folder_name,
        parent_folder=parent_folder,
    )

    is_required = __check_is_required(
        folder_name=child_folder_name,
        b_eng_folder_type=b_eng_folder_type,
        parent_folder=parent_folder,
    )

    if not is_required:
        return

    alternative_name = get_b_eng_folder_alternative_name(
        folder_name=child_folder_name,
        parent_folder=parent_folder,
    )

    folder = BEngFolders(
        absolute_path_string=child_folder_name,
        parent_folder=parent_folder,
        b_eng_folder_type=b_eng_folder_type,
        alternative_name=alternative_name,
    )

    if (
        b_eng_folder_type
        == EnumBEngFolderTypes.CODE_FOLDER
    ):
        b_eng_python_reference_dictionary.add_b_eng_folder_reference(
            b_eng_folder=folder,
        )

    if (
        b_eng_folder_type
        == EnumBEngFolderTypes.REPOSITORY_ROOT_FOLDER
    ):
        b_eng_python_reference_dictionary.add_b_eng_folder_reference(
            b_eng_folder=folder,
        )

    collect_child_files_structure(
        parent_folder=folder,
        b_eng_python_reference_dictionary=b_eng_python_reference_dictionary,
    )

    collect_child_folders_structure(
        parent_folder=folder,
        b_eng_python_reference_dictionary=b_eng_python_reference_dictionary,
    )


def __check_is_required(
    folder_name: str,
    b_eng_folder_type: EnumBEngFolderTypes,
    parent_folder: BEngFolders,
) -> bool:
    if ".ideas" in folder_name:
        return False

    if ".git" in folder_name:
        return False

    if "__pycache__" in folder_name:
        return False

    if (
        parent_folder.b_eng_folder_type
        == EnumBEngFolderTypes.BITBUCKET_PROJECT
        and b_eng_folder_type
        != EnumBEngFolderTypes.GIT_REPOSITORIES
    ):
        return False

    return True
