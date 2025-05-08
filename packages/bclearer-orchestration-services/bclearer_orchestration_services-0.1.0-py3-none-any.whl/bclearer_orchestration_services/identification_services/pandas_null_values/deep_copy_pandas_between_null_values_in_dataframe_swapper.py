import copy

from bclearer_orchestration_services.identification_services.pandas_null_values.pandas_between_null_values_in_dataframe_swapper import (
    swap_between_pandas_null_values_in_dataframe,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.pandas_null_value_swap_between_types import (
    PandasNullValueSwapBetweenTypes,
)
from pandas import DataFrame


def deep_copy_swap_between_pandas_null_values_in_dataframe(
    to_be_processed_dataframe: DataFrame,
    pandas_null_value_swap_between_type: PandasNullValueSwapBetweenTypes,
) -> DataFrame:
    processed_dataframe = copy.deepcopy(
        to_be_processed_dataframe,
    )

    swap_between_pandas_null_values_in_dataframe(
        dataframe=processed_dataframe,
        pandas_null_value_swap_between_type=pandas_null_value_swap_between_type,
    )

    return processed_dataframe
