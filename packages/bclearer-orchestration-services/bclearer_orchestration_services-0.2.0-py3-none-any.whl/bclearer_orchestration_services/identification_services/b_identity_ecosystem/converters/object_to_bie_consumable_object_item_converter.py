from bclearer_orchestration_services.identification_services.b_identity_ecosystem.converters.non_null_object_to_bie_consumable_object_item_converter import (
    convert_non_null_object_to_bie_consumable_object_item,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.converters.null_processed_input_object_getter import (
    get_null_processed_input_object,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_identity_spaces import (
    BieIdentitySpaces,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.cell_pandas_null_value_type_getter import (
    get_cell_pandas_null_value_type,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.pandas_null_value_types import (
    PandasNullValueTypes,
)


def convert_object_to_bie_consumable_object_item(
    input_object: object,
    bie_identity_space: BieIdentitySpaces,
) -> str:
    cell_pandas_null_value_type = (
        get_cell_pandas_null_value_type(
            cell=input_object,
        )
    )

    if (
        cell_pandas_null_value_type
        == PandasNullValueTypes.NOT_SET
    ):
        return convert_non_null_object_to_bie_consumable_object_item(
            input_object=input_object,
            bie_identity_space=bie_identity_space,
        )

    null_processed_input_object = get_null_processed_input_object(
        input_object=input_object,
        bie_identity_space=bie_identity_space,
        cell_pandas_null_value_type=cell_pandas_null_value_type,
    )

    return null_processed_input_object
