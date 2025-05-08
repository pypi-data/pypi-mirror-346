from enum import Enum, auto

from bclearer_orchestration_services.identification_services.pandas_null_values.pandas_null_value_types import (
    PandasNullValueTypes,
)


class PandasNullValueSwapBetweenTypes(
    Enum,
):
    NOT_SET = auto()

    EMPTY_STRING_TO_EMPTY_CELL = auto()

    UPPER_NUMPY_NAN_CELL_TO_EMPTY_CELL = (
        auto()
    )

    def __from_pandas_null_value(
        self,
    ) -> PandasNullValueTypes:
        from_to = pandas_null_value_type_to_string_mapping[
            self
        ]

        return from_to[0]

    def __to_pandas_null_value(
        self,
    ) -> PandasNullValueTypes:
        from_to = pandas_null_value_type_to_string_mapping[
            self
        ]

        return from_to[1]

    from_pandas_null_value = property(
        fget=__from_pandas_null_value,
    )

    to_pandas_null_value = property(
        fget=__to_pandas_null_value,
    )


pandas_null_value_type_to_string_mapping = {
    PandasNullValueSwapBetweenTypes.EMPTY_STRING_TO_EMPTY_CELL: (
        PandasNullValueTypes.EMPTY_STRING,
        PandasNullValueTypes.EMPTY_CELL,
    ),
    PandasNullValueSwapBetweenTypes.UPPER_NUMPY_NAN_CELL_TO_EMPTY_CELL: (
        PandasNullValueTypes.NUMPY_NAN_CELL,
        PandasNullValueTypes.EMPTY_CELL,
    ),
}
