import pandas
from pandas import DataFrame


def get_grouped_data_policy(
    data_policy_counts_as_table: DataFrame,
) -> DataFrame:
    grouped_dictionaries = list()

    for (
        column_name
    ) in (
        data_policy_counts_as_table.columns
    ):
        __add_grouped_dictionary(
            grouped_dictionaries=grouped_dictionaries,
            data_policy_counts_as_table=data_policy_counts_as_table,
            column_name=column_name,
        )

    result = pandas.DataFrame(
        grouped_dictionaries,
    )

    return result


def __add_grouped_dictionary(
    grouped_dictionaries: list,
    data_policy_counts_as_table: DataFrame,
    column_name: str,
):
    unique_data_policy_names = (
        data_policy_counts_as_table[
            column_name
        ].unique()
    )

    for (
        unique_data_policy_name
    ) in unique_data_policy_names:
        count = len(
            list(
                data_policy_counts_as_table[
                    data_policy_counts_as_table[
                        column_name
                    ]
                    == unique_data_policy_name
                ][
                    column_name
                ],
            ),
        )

        grouped_dictionaries.append(
            {
                "column_names": column_name,
                "data_policy_names": unique_data_policy_name,
                "data_policy_match_counts": count,
            },
        )
