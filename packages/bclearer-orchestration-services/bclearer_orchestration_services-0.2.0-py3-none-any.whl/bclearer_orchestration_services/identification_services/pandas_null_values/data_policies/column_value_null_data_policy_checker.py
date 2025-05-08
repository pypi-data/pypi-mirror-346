import pandas
from bclearer_orchestration_services.identification_services.pandas_null_values.cell_pandas_null_value_type_getter import (
    get_cell_pandas_null_value_type,
)


def check_column_value_null_data_policy(
    cell_values: pandas.Series,
) -> pandas.Series:
    column_values_data_policy = cell_values.apply(
        lambda cell_value: get_cell_pandas_null_value_type(
            cell_value,
        ),
    )

    return column_values_data_policy
