from bclearer_orchestration_services.identification_services.b_identity_ecosystem.converters.non_null_object_to_bie_consumable_object_item_converter import (
    convert_non_null_object_to_bie_consumable_object_item,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_identity_spaces import (
    BieIdentitySpaces,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.cell_is_string_based_null_value_checker import (
    check_cell_is_string_based_null_value,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.null_type_recognition import (
    NullTypeRecognition,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.pandas_null_value_types import (
    PandasNullValueTypes,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.string_based_null_type_recognition import (
    StringBasedNullTypeRecognition,
)


def get_null_processed_input_object(
    input_object: object,
    bie_identity_space: BieIdentitySpaces,
    cell_pandas_null_value_type: PandasNullValueTypes,
) -> str:
    if (
        bie_identity_space.string_based_null_type_recognition
        is StringBasedNullTypeRecognition.DO_NOT_RECOGNISE_STRING_BASED_NULL_AS_NULL
    ):
        cell_pandas_is_null_based_string = check_cell_is_string_based_null_value(
            cell=input_object,
        )

        if cell_pandas_is_null_based_string:
            bie_consumable_object = convert_non_null_object_to_bie_consumable_object_item(
                input_object=input_object,
                bie_identity_space=bie_identity_space,
            )

            return bie_consumable_object

    bie_consumable_string = __get_bie_consumable_string(
        bie_identity_space=bie_identity_space,
        cell_pandas_null_value_type=cell_pandas_null_value_type,
    )

    return bie_consumable_string


def __get_bie_consumable_string(
    bie_identity_space: BieIdentitySpaces,
    cell_pandas_null_value_type: PandasNullValueTypes,
):
    null_conversion_prefix = (
        "<RECOGNISED AS NULL OBJECT>"
    )

    if (
        bie_identity_space.null_type_recognition
        is NullTypeRecognition.FINE_GRAINED
    ):
        return (
            null_conversion_prefix
            + str(
                cell_pandas_null_value_type,
            )
        )

    return null_conversion_prefix + str(
        NullTypeRecognition.COARSE_GRAINED_SINGLE_VALUE,
    )
