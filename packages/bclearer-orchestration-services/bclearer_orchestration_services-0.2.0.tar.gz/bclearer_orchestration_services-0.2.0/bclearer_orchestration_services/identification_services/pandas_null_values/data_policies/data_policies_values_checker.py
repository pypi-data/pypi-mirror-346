import os

import pandas
from bclearer_orchestration_services.identification_services.pandas_null_values.data_policies.column_value_null_data_policy_checker import (
    check_column_value_null_data_policy,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.data_policies.grouped_data_policy_getter import (
    get_grouped_data_policy,
)
from pandas import DataFrame


def check_data_policies_values(
    table_configuration,
    input_dataframe: DataFrame,
) -> DataFrame:
    data_policy_counts_as_table = input_dataframe.apply(
        lambda row: check_column_value_null_data_policy(
            row,
        ),
    )

    if (
        data_policy_counts_as_table.shape
        != input_dataframe.shape
    ):
        raise ValueError(
            "DataFrames have different shapes: data_policy_counts vs input table",
        )

    applied_data_policy_results_as_table = get_grouped_data_policy(
        data_policy_counts_as_table=data_policy_counts_as_table,
    )

    applied_data_policy_results_as_table = __add_missing_columns(
        table_configuration=table_configuration,
        applied_data_policy_results_as_table=applied_data_policy_results_as_table,
    )

    return applied_data_policy_results_as_table


# this code needs cleaning - maybe create a new object
def __add_missing_columns(
    table_configuration,
    applied_data_policy_results_as_table: DataFrame,
):
    applied_data_policy_results_as_table[
        "data_policy_names"
    ] = applied_data_policy_results_as_table[
        "data_policy_names"
    ].astype(
        str,
    )

    matched_rows_count = len(
        applied_data_policy_results_as_table,
    )

    applied_data_policy_results_as_table.columns = [
        "column_names",
        "data_policy_names",
        "data_policy_match_counts",
    ]

    applied_data_policy_results_as_table[
        "bie_ids_tables"
    ] = pandas.Series(
        [
            table_configuration.bie_table_id,
        ]
        * matched_rows_count,
    )

    # TODO: added temporary fix - to delete this column later
    applied_data_policy_results_as_table[
        "data_policy_values"
    ] = pandas.Series(
        [""] * matched_rows_count,
    )

    applied_data_policy_results_as_table[
        "table_names"
    ] = pandas.Series(
        [table_configuration.table_name]
        * matched_rows_count,
    )

    applied_data_policy_results_as_table[
        "source_extension_types"
    ] = pandas.Series(
        [
            table_configuration.source_extension_type,
        ]
        * matched_rows_count,
    )

    applied_data_policy_results_as_table[
        "table_source_folders"
    ] = pandas.Series(
        [
            table_configuration.table_source_folder,
        ]
        * matched_rows_count,
    )

    applied_data_policy_results_as_table[
        "sigraph_stages"
    ] = pandas.Series(
        [
            table_configuration.table_source_relative_path.split(
                os.sep,
            )[
                -1
            ],
        ]
        * matched_rows_count,
    )

    return applied_data_policy_results_as_table
