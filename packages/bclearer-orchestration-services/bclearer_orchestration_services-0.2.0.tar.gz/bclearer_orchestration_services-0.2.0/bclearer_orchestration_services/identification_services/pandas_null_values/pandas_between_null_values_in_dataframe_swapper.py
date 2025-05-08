from bclearer_orchestration_services.identification_services.pandas_null_values.pandas_null_value_swap_between_types import (
    PandasNullValueSwapBetweenTypes,
)
from pandas import DataFrame


def swap_between_pandas_null_values_in_dataframe(
    dataframe: DataFrame,
    pandas_null_value_swap_between_type: PandasNullValueSwapBetweenTypes,
) -> None:
    from_pandas_null_value = (
        pandas_null_value_swap_between_type.from_pandas_null_value
    )

    to_pandas_null_value = (
        pandas_null_value_swap_between_type.to_pandas_null_value
    )

    dataframe.replace(
        from_pandas_null_value.value,
        to_pandas_null_value.value,
        inplace=True,
    )
