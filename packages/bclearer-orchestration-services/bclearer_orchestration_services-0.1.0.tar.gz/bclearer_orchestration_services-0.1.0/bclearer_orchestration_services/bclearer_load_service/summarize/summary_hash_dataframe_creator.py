import pandas
from bclearer_orchestration_services.bclearer_load_service.common_knowledge.bclearer_load_constants import (
    ALTERNATIVE_IDENTITY_HASH_SET_CONTENT_HASH_NAME,
    ALTERNATIVE_IDENTITY_HASHES_CONFIGURATION_NAME,
    CONTENT_HASH_SET_CONTENT_HASH_NAME,
    CONTENT_HASHES_CONFIGURATION_NAME,
    CORE_CONTENT_HASHES_CONFIGURATION_NAME,
    CORE_CONTENT_SET_CONTENT_HASH_NAME,
    HASHES_SUMMARY_COLUMN_NAME,
    IDENTITY_HASH_SET_CONTENT_HASH_NAME,
    IDENTITY_HASHES_CONFIGURATION_NAME,
    NAMES_SUMMARY_COLUMN_NAME,
)
from bclearer_orchestration_services.identification_services.hash_service.hash_creator import (
    create_hash_with_sorted_inputs,
)


def create_summary_hash_dataframe(
    hashified_and_filtered_target_dataframe: pandas.DataFrame,
) -> pandas.DataFrame:
    summary_hash_dataframe = pandas.DataFrame(
        columns=[
            NAMES_SUMMARY_COLUMN_NAME,
            HASHES_SUMMARY_COLUMN_NAME,
        ],
    )

    summary_hash_dataframe = __add_summary_row_if_required(
        hashified_and_filtered_target_dataframe=hashified_and_filtered_target_dataframe,
        summary_hash_dataframe=summary_hash_dataframe,
        source_column_name=IDENTITY_HASHES_CONFIGURATION_NAME,
        summary_row_name=IDENTITY_HASH_SET_CONTENT_HASH_NAME,
    )

    summary_hash_dataframe = __add_summary_row_if_required(
        hashified_and_filtered_target_dataframe=hashified_and_filtered_target_dataframe,
        summary_hash_dataframe=summary_hash_dataframe,
        source_column_name=ALTERNATIVE_IDENTITY_HASHES_CONFIGURATION_NAME,
        summary_row_name=ALTERNATIVE_IDENTITY_HASH_SET_CONTENT_HASH_NAME,
    )

    summary_hash_dataframe = __add_summary_row_if_required(
        hashified_and_filtered_target_dataframe=hashified_and_filtered_target_dataframe,
        summary_hash_dataframe=summary_hash_dataframe,
        source_column_name=CORE_CONTENT_HASHES_CONFIGURATION_NAME,
        summary_row_name=CORE_CONTENT_SET_CONTENT_HASH_NAME,
    )

    summary_hash_dataframe = __add_summary_row_if_required(
        hashified_and_filtered_target_dataframe=hashified_and_filtered_target_dataframe,
        summary_hash_dataframe=summary_hash_dataframe,
        source_column_name=CONTENT_HASHES_CONFIGURATION_NAME,
        summary_row_name=CONTENT_HASH_SET_CONTENT_HASH_NAME,
    )

    return summary_hash_dataframe


def __add_summary_row_if_required(
    hashified_and_filtered_target_dataframe: pandas.DataFrame,
    summary_hash_dataframe: pandas.DataFrame,
    source_column_name: str,
    summary_row_name: str,
) -> pandas.DataFrame:
    if (
        source_column_name
        not in hashified_and_filtered_target_dataframe
    ):
        return summary_hash_dataframe

    hash_components = list(
        hashified_and_filtered_target_dataframe[
            source_column_name
        ],
    )

    hash_string = (
        create_hash_with_sorted_inputs(
            inputs=hash_components,
        )
    )

    row_data = {
        NAMES_SUMMARY_COLUMN_NAME: summary_row_name,
        HASHES_SUMMARY_COLUMN_NAME: hash_string,
    }

    summary_row_dataframe = (
        pandas.DataFrame([row_data])
    )

    dataframes = [
        summary_hash_dataframe,
        summary_row_dataframe,
    ]

    summary_hash_dataframe = (
        pandas.concat(
            dataframes,
            ignore_index=True,
        )
    )

    return summary_hash_dataframe
