import pandas
from bclearer_orchestration_services.bclearer_load_service.common_knowledge.bclearer_load_constants import (
    ALTERNATIVE_IDENTITY_HASHES_CONFIGURATION_NAME,
    CONTENT_HASHES_CONFIGURATION_NAME,
    CORE_CONTENT_HASHES_CONFIGURATION_NAME,
    IDENTITY_HASHES_CONFIGURATION_NAME,
)
from bclearer_orchestration_services.bclearer_load_service.hashify_and_filter.configuration.bclearer_load_configurations import (
    BclearerLoadConfigurations,
)
from bclearer_orchestration_services.bclearer_load_service.hashify_and_filter.hash_creators.content_hash_column_using_all_columns_adder import (
    add_content_hash_column_using_all_columns,
)
from bclearer_orchestration_services.bclearer_load_service.hashify_and_filter.hash_creators.named_hash_column_adder import (
    add_named_hash_column,
)


def hashify_target_dataframe(
    target_dataframe: pandas.DataFrame,
    bclearer_load_configuration: BclearerLoadConfigurations,
) -> pandas.DataFrame:
    hashified_target_dataframe = (
        target_dataframe.copy()
    )

    if (
        bclearer_load_configuration.content_hash_configuration_list
    ):
        add_named_hash_column(
            hashified_target_dataframe=hashified_target_dataframe,
            column_name=CONTENT_HASHES_CONFIGURATION_NAME,
            configuration_list=bclearer_load_configuration.identity_hash_configuration_list,
        )

    else:
        add_content_hash_column_using_all_columns(
            hashified_target_dataframe=hashified_target_dataframe,
        )

    add_named_hash_column(
        hashified_target_dataframe=hashified_target_dataframe,
        column_name=IDENTITY_HASHES_CONFIGURATION_NAME,
        configuration_list=bclearer_load_configuration.identity_hash_configuration_list,
    )

    if (
        bclearer_load_configuration.alternative_identity_hash_configuration_list
    ):
        add_named_hash_column(
            hashified_target_dataframe=hashified_target_dataframe,
            column_name=ALTERNATIVE_IDENTITY_HASHES_CONFIGURATION_NAME,
            configuration_list=bclearer_load_configuration.alternative_identity_hash_configuration_list,
        )

    if (
        bclearer_load_configuration.core_content_hash_configuration_list
    ):
        add_named_hash_column(
            hashified_target_dataframe=hashified_target_dataframe,
            column_name=CORE_CONTENT_HASHES_CONFIGURATION_NAME,
            configuration_list=bclearer_load_configuration.core_content_hash_configuration_list,
        )

    return hashified_target_dataframe
