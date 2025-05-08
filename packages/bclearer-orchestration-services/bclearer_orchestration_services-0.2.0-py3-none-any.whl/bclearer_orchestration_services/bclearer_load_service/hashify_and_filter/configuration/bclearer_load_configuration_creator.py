import pandas
from bclearer_orchestration_services.bclearer_load_service.common_knowledge.bclearer_load_constants import (
    ALTERNATIVE_IDENTITY_HASHES_CONFIGURATION_NAME,
    COLUMNS_IN_SCOPE_CONFIGURATION_NAME,
    CONTENT_HASHES_CONFIGURATION_NAME,
    CORE_CONTENT_HASHES_CONFIGURATION_NAME,
    IDENTITY_HASHES_CONFIGURATION_NAME,
    KEY_NAMES_CONFIGURATION_COLUMN_NAME,
    VALUES_CONFIGURATION_COLUMN_NAME,
)
from bclearer_orchestration_services.bclearer_load_service.hashify_and_filter.configuration.bclearer_load_configurations import (
    BclearerLoadConfigurations,
)


def create_bclearer_load_configuration(
    configuration_dataframe: pandas.DataFrame,
) -> BclearerLoadConfigurations:
    identity_hash_configuration_list = __get_list_from_configuration(
        configuration_dataframe=configuration_dataframe,
        key_name=IDENTITY_HASHES_CONFIGURATION_NAME,
    )

    alternative_identity_hash_configuration_list = __get_list_from_configuration(
        configuration_dataframe=configuration_dataframe,
        key_name=ALTERNATIVE_IDENTITY_HASHES_CONFIGURATION_NAME,
    )

    core_content_hash_configuration_list = __get_list_from_configuration(
        configuration_dataframe=configuration_dataframe,
        key_name=CORE_CONTENT_HASHES_CONFIGURATION_NAME,
    )

    content_hash_configuration_list = __get_list_from_configuration(
        configuration_dataframe=configuration_dataframe,
        key_name=CONTENT_HASHES_CONFIGURATION_NAME,
    )

    columns_in_scope_configuration_list = __get_list_from_configuration(
        configuration_dataframe=configuration_dataframe,
        key_name=COLUMNS_IN_SCOPE_CONFIGURATION_NAME,
    )

    bclearer_load_configuration = BclearerLoadConfigurations(
        identity_hash_configuration_list=identity_hash_configuration_list,
        alternative_identity_hash_configuration_list=alternative_identity_hash_configuration_list,
        core_content_hash_configuration_list=core_content_hash_configuration_list,
        content_hash_configuration_list=content_hash_configuration_list,
        columns_in_scope_configuration_list=columns_in_scope_configuration_list,
    )

    return bclearer_load_configuration


def __get_list_from_configuration(
    configuration_dataframe: pandas.DataFrame,
    key_name: str,
) -> list:
    if key_name not in set(
        configuration_dataframe[
            KEY_NAMES_CONFIGURATION_COLUMN_NAME
        ],
    ):
        return list()

    configuration_value = configuration_dataframe.loc[
        configuration_dataframe[
            KEY_NAMES_CONFIGURATION_COLUMN_NAME
        ]
        == key_name,
        VALUES_CONFIGURATION_COLUMN_NAME,
    ].iloc[
        0
    ]

    configuration_list = (
        configuration_value.split(",")
    )

    return configuration_list
