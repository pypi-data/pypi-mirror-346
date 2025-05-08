from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.data_type_recognition import (
    DataTypeRecognition,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.null_type_recognition import (
    NullTypeRecognition,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.string_based_null_type_recognition import (
    StringBasedNullTypeRecognition,
)


class BieIdentitySpaces:
    def __init__(
        self,
        null_type_recognition: NullTypeRecognition = NullTypeRecognition.COARSE_GRAINED_SINGLE_VALUE,
        string_based_null_type_recognition: StringBasedNullTypeRecognition = StringBasedNullTypeRecognition.DO_NOT_RECOGNISE_STRING_BASED_NULL_AS_NULL,
        data_type_recognition: DataTypeRecognition = DataTypeRecognition.DO_NOT_INCLUDE_DATA_TYPES_IN_BIE_CALCULATION,
        digest_size: int = 8,
    ):
        self.null_type_recognition = (
            null_type_recognition
        )

        self.string_based_null_type_recognition = string_based_null_type_recognition

        self.digest_size = digest_size

        self.data_type_recognition = (
            data_type_recognition
        )
