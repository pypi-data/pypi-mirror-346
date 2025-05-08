from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_files import (
    BEngFiles,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_folders import (
    BEngFolders,
)


class BEngPythonReferenceDictionaries:
    def __init__(self):
        self.__dictionary = {}

    def add_b_eng_folder_reference(
        self,
        b_eng_folder: BEngFolders,
    ):
        reference_string = (
            b_eng_folder.alternative_name
        )

        self.__dictionary[
            reference_string
        ] = b_eng_folder

    def add_b_eng_file_reference(
        self,
        b_eng_file: BEngFiles,
    ):
        reference_string = (
            b_eng_file.alternative_name
        )

        self.__dictionary[
            reference_string
        ] = b_eng_file

    def get_reference(
        self,
        reference_string: str,
    ):
        if (
            reference_string
            not in self.__dictionary.keys()
        ):
            return None

        reference = self.__dictionary[
            reference_string
        ]

        return reference
