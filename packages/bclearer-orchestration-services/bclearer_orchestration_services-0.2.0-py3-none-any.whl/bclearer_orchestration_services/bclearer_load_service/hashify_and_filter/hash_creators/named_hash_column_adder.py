import pandas
from bclearer_orchestration_services.identification_services.hash_service.hash_creator import (
    create_hash_with_sorted_inputs,
)


def add_named_hash_column(
    hashified_target_dataframe: pandas.DataFrame,
    column_name: str,
    configuration_list: list,
) -> None:
    hashified_target_dataframe[
        column_name
    ] = hashified_target_dataframe.apply(
        lambda row: __get_hash(
            row,
            configuration_list,
        ),
        axis=1,
    )


def __get_hash(
    row,
    configuration_list,
) -> str:
    hash_components = list()

    for (
        configuration
    ) in configuration_list:
        __add_component(
            hash_components=hash_components,
            configuration=configuration,
            row=row,
        )

    hash_string = (
        create_hash_with_sorted_inputs(
            inputs=hash_components,
        )
    )

    return hash_string


def __add_component(
    hash_components: list,
    configuration: str,
    row,
) -> None:
    if configuration[0] == "'":
        hash_components.append(
            configuration,
        )

    else:
        hash_components.append(
            row[configuration],
        )
