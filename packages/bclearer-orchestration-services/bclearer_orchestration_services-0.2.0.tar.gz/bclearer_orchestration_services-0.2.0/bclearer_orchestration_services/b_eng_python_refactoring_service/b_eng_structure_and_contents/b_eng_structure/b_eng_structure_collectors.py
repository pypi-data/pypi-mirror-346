from nf_common.code.services.b_eng_python_refactoring_service.b_eng_structure_and_contents.b_eng_structure.b_eng_child_folder_structure_collectors import (
    collect_child_folders_structure,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_python_reference_dictionaries import (
    BEngPythonReferenceDictionaries,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_folders import (
    BEngWorkspaceFolders,
)


def collect_structure(
    workspace_path: str,
    b_eng_python_reference_dictionary: BEngPythonReferenceDictionaries,
) -> BEngWorkspaceFolders:
    workspace_root_folder = BEngWorkspaceFolders(
        absolute_path_string=workspace_path,
    )

    collect_child_folders_structure(
        parent_folder=workspace_root_folder,
        b_eng_python_reference_dictionary=b_eng_python_reference_dictionary,
    )

    return workspace_root_folder
