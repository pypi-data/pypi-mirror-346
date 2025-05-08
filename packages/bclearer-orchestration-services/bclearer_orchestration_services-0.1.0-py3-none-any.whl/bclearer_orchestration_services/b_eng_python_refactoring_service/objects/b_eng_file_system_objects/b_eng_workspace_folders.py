from nf_common.code.services.b_eng_python_refactoring_service.common_knowledge.enum_b_eng_folder_types import (
    EnumBEngFolderTypes,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_folders import (
    BEngFolders,
)


class BEngWorkspaceFolders(BEngFolders):
    def __init__(
        self,
        absolute_path_string: str,
    ):
        super().__init__(
            absolute_path_string=absolute_path_string,
        )

        self.b_eng_folder_type = (
            EnumBEngFolderTypes.WORKSPACE
        )
