from bclearer_orchestration_services.identification_services.pandas_null_values.pandas_null_value_types import (
    PandasNullValueTypes,
)

set_of_string_based_null_value_types = {
    PandasNullValueTypes.NAN_AS_STRING_VALUE,
    PandasNullValueTypes.NULL_AS_STRING_VALUE,
    PandasNullValueTypes.NUMPY_DATETIME_64_AS_STRING_VALUE,
    PandasNullValueTypes.NONE_CELL_AS_STRING_VALUE,
}
