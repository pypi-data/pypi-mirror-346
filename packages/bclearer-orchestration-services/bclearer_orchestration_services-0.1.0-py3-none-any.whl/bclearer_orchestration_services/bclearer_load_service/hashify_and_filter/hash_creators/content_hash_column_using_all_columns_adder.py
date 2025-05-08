import pandas
from bclearer_orchestration_services.bclearer_load_service.common_knowledge.bclearer_load_constants import (
    CONTENT_HASHES_CONFIGURATION_NAME,
)
from bclearer_orchestration_services.identification_services.hash_service.hash_creator import (
    create_hash_with_sorted_inputs,
)


def add_content_hash_column_using_all_columns(
    hashified_target_dataframe: pandas.DataFrame,
) -> None:
    hashified_target_dataframe[
        CONTENT_HASHES_CONFIGURATION_NAME
    ] = hashified_target_dataframe.apply(
        lambda row: __get_content_hash(
            row,
        ),
        axis=1,
    )


def __get_content_hash(
    row: pandas.Series,
) -> str:
    hash_components = list()

    column_names = row.index.values

    for column_name in column_names:
        __add_hash_component(
            hash_components=hash_components,
            row=row,
            column_name=column_name,
        )

    hash_string = (
        create_hash_with_sorted_inputs(
            inputs=hash_components,
        )
    )

    return hash_string


def __add_hash_component(
    hash_components: list,
    row: pandas.Series,
    column_name: str,
) -> None:
    hash_component = row[column_name]

    if not isinstance(
        hash_component,
        str,
    ):
        hash_component = str(
            hash_component,
        )

    hash_components.append(
        hash_component,
    )
