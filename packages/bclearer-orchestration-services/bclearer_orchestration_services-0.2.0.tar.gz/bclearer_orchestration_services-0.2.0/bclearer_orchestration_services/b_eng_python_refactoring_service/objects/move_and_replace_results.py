from nf_common.code.services.b_eng_python_refactoring_service.common_knowledge.enum_move_and_replace_result_types import (
    EnumMoveAndReplaceResultTypes,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_file_system_object_couples import (
    BEngWorkspaceFileSystemObjectCouples,
)


class MoveAndReplaceResults:
    def __init__(
        self,
        b_eng_workspace_file_system_object_couple: BEngWorkspaceFileSystemObjectCouples,
        result_type: EnumMoveAndReplaceResultTypes,
        reason: str,
    ):
        self.b_eng_workspace_file_system_object_couple = b_eng_workspace_file_system_object_couple

        self.result_type = result_type

        self.reason = reason
