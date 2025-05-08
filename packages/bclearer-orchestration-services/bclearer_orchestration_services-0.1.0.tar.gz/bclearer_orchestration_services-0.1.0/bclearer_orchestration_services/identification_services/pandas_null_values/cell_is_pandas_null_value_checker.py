from bclearer_orchestration_services.identification_services.pandas_null_values.cell_pandas_null_value_type_getter import (
    get_cell_pandas_null_value_type,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.pandas_null_value_types import (
    PandasNullValueTypes,
)


def check_cell_is_pandas_null_value(
    cell: object,
) -> bool:
    cell_pandas_null_value_type = (
        get_cell_pandas_null_value_type(
            cell=cell,
        )
    )

    cell_is_pandas_null_value = (
        cell_pandas_null_value_type
        != PandasNullValueTypes.NOT_SET
    )

    return cell_is_pandas_null_value
