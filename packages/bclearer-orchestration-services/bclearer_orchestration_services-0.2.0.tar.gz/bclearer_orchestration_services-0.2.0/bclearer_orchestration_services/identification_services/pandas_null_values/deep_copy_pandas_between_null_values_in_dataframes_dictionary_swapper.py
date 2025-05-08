from bclearer_orchestration_services.identification_services.pandas_null_values.deep_copy_pandas_between_null_values_in_dataframe_swapper import (
    deep_copy_swap_between_pandas_null_values_in_dataframe,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.pandas_null_value_swap_between_types import (
    PandasNullValueSwapBetweenTypes,
)


def deep_copy_swap_between_pandas_null_values_in_dataframes_dictionary(
    to_be_processed_dataframe_dictionary: dict,
    pandas_null_value_swap_between_type: PandasNullValueSwapBetweenTypes,
) -> dict:
    processed_dataframe_dictionary = (
        dict()
    )

    for (
        dataframe_dictionary_key,
        dataframe_dictionary_value,
    ) in (
        to_be_processed_dataframe_dictionary.items()
    ):
        processed_dataframe_dictionary[
            dataframe_dictionary_key
        ] = deep_copy_swap_between_pandas_null_values_in_dataframe(
            to_be_processed_dataframe=dataframe_dictionary_value,
            pandas_null_value_swap_between_type=pandas_null_value_swap_between_type,
        )

    return (
        processed_dataframe_dictionary
    )
