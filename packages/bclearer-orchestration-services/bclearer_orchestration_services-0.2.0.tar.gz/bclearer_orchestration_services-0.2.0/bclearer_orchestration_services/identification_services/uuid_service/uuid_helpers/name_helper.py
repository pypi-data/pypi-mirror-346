from bclearer_orchestration_services.identification_services.uuid_service.constants.uuidification_constants import (
    UUID_COLUMN_NAME_SEPARATOR,
    UUIDIFIED_DATAFRAME_PREFIX,
)


def get_uuidified_dataframe_name(
    dataframe_name: str,
):
    uuidified_dataframe_name = (
        __get_separated_uuid_column(
            UUIDIFIED_DATAFRAME_PREFIX,
            dataframe_name,
        )
    )

    return uuidified_dataframe_name


def get_common_uuidification_table_name(
    prefix: str,
    table_type_name: str,
):
    common_uuidification_table_name = (
        __get_separated_uuid_column(
            prefix,
            table_type_name,
        )
    )

    return (
        common_uuidification_table_name
    )


def __get_separated_uuid_column(
    prefix: str,
    suffix: str,
):
    separated_uuid_column = (
        prefix
        + UUID_COLUMN_NAME_SEPARATOR
        + suffix
    )

    return separated_uuid_column
