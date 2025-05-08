from bclearer_orchestration_services.identification_services.pandas_null_values.pandas_null_value_swap_between_types import (
    PandasNullValueSwapBetweenTypes,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.pandas_null_value_types import (
    PandasNullValueTypes,
)

# TODO - Oscar to add the ones we need
PandasNullValueTypeToStringMappings = {
    PandasNullValueSwapBetweenTypes.EMPTY_STRING_TO_EMPTY_CELL: (
        PandasNullValueTypes.EMPTY_STRING,
        PandasNullValueTypes.EMPTY_CELL,
    ),
    PandasNullValueSwapBetweenTypes.UPPER_NUMPY_NAN_CELL_TO_EMPTY_CELL: (
        PandasNullValueTypes.NUMPY_NAN_CELL,
        PandasNullValueTypes.EMPTY_CELL,
    ),
}
