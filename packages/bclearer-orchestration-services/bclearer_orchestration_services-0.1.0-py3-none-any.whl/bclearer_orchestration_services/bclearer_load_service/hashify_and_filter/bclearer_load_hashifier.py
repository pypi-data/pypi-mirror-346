import pandas
from bclearer_orchestration_services.bclearer_load_service.hashify_and_filter.configuration.bclearer_load_configuration_creator import (
    create_bclearer_load_configuration,
)
from bclearer_orchestration_services.bclearer_load_service.hashify_and_filter.hashified_target_dataframe_filterer import (
    filter_hashified_target_dataframe,
)
from bclearer_orchestration_services.bclearer_load_service.hashify_and_filter.target_dataframe_hashifier import (
    hashify_target_dataframe,
)


def hashify_bclearer_load(
    target_dataframe: pandas.DataFrame,
    configuration_dataframe: pandas.DataFrame,
) -> pandas.DataFrame:
    bclearer_load_configuration = create_bclearer_load_configuration(
        configuration_dataframe=configuration_dataframe,
    )

    hashified_target_dataframe = hashify_target_dataframe(
        target_dataframe=target_dataframe,
        bclearer_load_configuration=bclearer_load_configuration,
    )

    hashified_and_filtered_target_dataframe = filter_hashified_target_dataframe(
        hashified_target_dataframe=hashified_target_dataframe,
        columns_in_scope_configuration_list=bclearer_load_configuration.columns_in_scope_configuration_list,
    )

    return hashified_and_filtered_target_dataframe
