import pandas
from bclearer_orchestration_services.bclearer_load_service.common_knowledge.bclearer_load_constants import (
    ALTERNATIVE_IDENTITY_HASHES_CONFIGURATION_NAME,
    CONTENT_HASHES_CONFIGURATION_NAME,
    CORE_CONTENT_HASHES_CONFIGURATION_NAME,
    IDENTITY_HASHES_CONFIGURATION_NAME,
)


def filter_hashified_target_dataframe(
    hashified_target_dataframe: pandas.DataFrame,
    columns_in_scope_configuration_list: list,
) -> pandas.DataFrame:
    hashified_and_filtered_target_dataframe = (
        hashified_target_dataframe.copy()
    )

    hashified_and_filtered_target_dataframe = __filter_columns(
        hashified_and_filtered_target_dataframe=hashified_and_filtered_target_dataframe,
        columns_in_scope_configuration_list=columns_in_scope_configuration_list,
    )

    return hashified_and_filtered_target_dataframe


def __filter_columns(
    hashified_and_filtered_target_dataframe: pandas.DataFrame,
    columns_in_scope_configuration_list: list,
) -> pandas.DataFrame:
    if (
        not columns_in_scope_configuration_list
    ):
        return hashified_and_filtered_target_dataframe

    hash_column_names = [
        IDENTITY_HASHES_CONFIGURATION_NAME,
        ALTERNATIVE_IDENTITY_HASHES_CONFIGURATION_NAME,
        CORE_CONTENT_HASHES_CONFIGURATION_NAME,
        CONTENT_HASHES_CONFIGURATION_NAME,
    ]

    column_names = (
        columns_in_scope_configuration_list
        + hash_column_names
    )

    hashified_and_filtered_target_dataframe = hashified_and_filtered_target_dataframe.filter(
        items=column_names,
    )

    return hashified_and_filtered_target_dataframe
