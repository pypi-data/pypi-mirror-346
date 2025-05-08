import pandas
from bclearer_orchestration_services.identification_services.pandas_null_values.data_policies.data_policies_values_checker import (
    check_data_policies_values,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def get_pandas_dataframe_data_policy_report(
    table_configuration,
    table: DataFrame,
) -> DataFrame:
    data_policy_counts_as_table = (
        pandas.DataFrame()
    )

    data_policy_counts_as_table = __get_pandas_dataframe_data_policy_report_hard_crash_wrapper(
        data_policy_counts_as_table=data_policy_counts_as_table,
        table_configuration=table_configuration,
        pandas_dataframe=table,
    )

    return data_policy_counts_as_table


def __get_pandas_dataframe_data_policy_report_hard_crash_wrapper(
    data_policy_counts_as_table: DataFrame,
    table_configuration,
    pandas_dataframe: DataFrame,
) -> DataFrame:
    try:
        applied_data_policy_results_as_table = check_data_policies_values(
            table_configuration=table_configuration,
            input_dataframe=pandas_dataframe,
        )

        data_policy_counts_as_table = pandas.concat(
            [
                data_policy_counts_as_table,
                applied_data_policy_results_as_table,
            ],
            axis=0,
        ).reset_index(
            drop=True,
        )

        return (
            data_policy_counts_as_table
        )

    except Exception as error:
        log_message(
            message=f"ERROR running table data policy report for table: {table_configuration.table_name} and data policy: {type(error)}{error!s}.",
        )

    return data_policy_counts_as_table
