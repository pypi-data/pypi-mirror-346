from nf_common.code.services.b_eng_python_refactoring_service.b_eng_structure_and_contents.b_eng_content.b_eng_content_collectors import (
    collect_content,
)
from nf_common.code.services.b_eng_python_refactoring_service.b_eng_structure_and_contents.b_eng_structure.b_eng_structure_collectors import (
    collect_structure,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_python_reference_dictionaries import (
    BEngPythonReferenceDictionaries,
)


def collect_structure_and_content(
    workspace_paths: list,
) -> list:
    workspace_root_folders = []

    b_eng_python_reference_dictionary = (
        BEngPythonReferenceDictionaries()
    )

    for (
        workspace_path
    ) in workspace_paths:
        workspace_root_folders.append(
            collect_structure(
                workspace_path=workspace_path,
                b_eng_python_reference_dictionary=b_eng_python_reference_dictionary,
            ),
        )

    collect_content(
        b_eng_python_reference_dictionary=b_eng_python_reference_dictionary,
    )

    return workspace_root_folders
