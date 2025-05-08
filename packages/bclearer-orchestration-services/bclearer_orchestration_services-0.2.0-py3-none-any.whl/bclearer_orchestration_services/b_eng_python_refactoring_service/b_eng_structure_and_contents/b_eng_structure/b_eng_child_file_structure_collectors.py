import os

from nf_common.code.services.b_eng_python_refactoring_service.b_eng_structure_and_contents.b_eng_structure.b_eng_file_system_alternative_name_getters import (
    get_b_eng_file_alternative_name,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_files import (
    BEngFiles,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_folders import (
    BEngFolders,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_python_reference_dictionaries import (
    BEngPythonReferenceDictionaries,
)


def collect_child_files_structure(
    parent_folder: BEngFolders,
    b_eng_python_reference_dictionary: BEngPythonReferenceDictionaries,
):
    file_names = [
        file_name
        for file_name in os.listdir(
            parent_folder.absolute_path_string,
        )
        if os.path.isfile(
            os.path.join(
                parent_folder.absolute_path_string,
                file_name,
            ),
        )
    ]

    for file_name in file_names:
        __collect_child_file_if_required(
            file_name=file_name,
            parent_folder=parent_folder,
            b_eng_python_reference_dictionary=b_eng_python_reference_dictionary,
        )


def __collect_child_file_if_required(
    file_name: str,
    parent_folder: BEngFolders,
    b_eng_python_reference_dictionary: BEngPythonReferenceDictionaries,
):
    file_is_required = (
        __check_if_file_is_required(
            file_name=file_name,
        )
    )

    if not file_is_required:
        return

    alternative_name = (
        get_b_eng_file_alternative_name(
            file_name=file_name,
            parent_folder=parent_folder,
        )
    )

    b_eng_file = BEngFiles(
        absolute_path_string=os.path.join(
            parent_folder.absolute_path_string,
            file_name,
        ),
        parent_folder=parent_folder,
        alternative_name=alternative_name,
    )

    b_eng_python_reference_dictionary.add_b_eng_file_reference(
        b_eng_file=b_eng_file,
    )


def __check_if_file_is_required(
    file_name: str,
) -> bool:
    if file_name.startswith("__"):
        return False

    if file_name.endswith(".py"):
        return True

    return False
