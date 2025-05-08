from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_files import (
    BEngFiles,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_python_reference_dictionaries import (
    BEngPythonReferenceDictionaries,
)


def collect_content(
    b_eng_python_reference_dictionary: BEngPythonReferenceDictionaries,
):
    files = (
        BEngFiles.registry_keyed_on_full_paths.values()
    )

    for file in files:
        __add_references_from_file(
            file=file,
            b_eng_python_reference_dictionary=b_eng_python_reference_dictionary,
        )


def __add_references_from_file(
    file: BEngFiles,
    b_eng_python_reference_dictionary: BEngPythonReferenceDictionaries,
):
    lines = __get_lines(
        file_path=file.absolute_path_string,
    )

    for line in lines:
        trimmed_line = line.lstrip()

        if trimmed_line.startswith(
            "import ",
        ) or trimmed_line.startswith(
            "from ",
        ):
            line_parts = (
                trimmed_line.split(" ")
            )

            reference_string = (
                line_parts[1].rstrip()
            )

            referenced_file = b_eng_python_reference_dictionary.get_reference(
                reference_string=reference_string,
            )

            __add_reference(
                file_that_uses_reference=file,
                referenced_file=referenced_file,
            )


def __get_lines(file_path):
    file_content = open(file_path, "r+")

    file_content_lines = (
        file_content.readlines()
    )

    file_content.close()

    return file_content_lines


def __add_reference(
    file_that_uses_reference: BEngFiles,
    referenced_file: BEngFiles,
):
    if referenced_file is None:
        return

    file_that_uses_reference.uses.append(
        referenced_file,
    )

    referenced_file.used_by.append(
        file_that_uses_reference,
    )
