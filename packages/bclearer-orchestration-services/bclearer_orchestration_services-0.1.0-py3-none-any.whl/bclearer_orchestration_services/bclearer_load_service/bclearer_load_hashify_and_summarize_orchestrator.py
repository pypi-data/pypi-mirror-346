import pandas
from bclearer_orchestration_services.bclearer_load_service.hashify_and_filter.bclearer_load_hashifier import (
    hashify_bclearer_load,
)
from bclearer_orchestration_services.bclearer_load_service.summarize.summary_hash_dataframe_creator import (
    create_summary_hash_dataframe,
)


def orchestrate_bclearer_load_hashify_and_summarize(
    target_dataframe: pandas.DataFrame,
    configuration_dataframe: pandas.DataFrame,
) -> tuple:
    hashified_and_filtered_target_dataframe = hashify_bclearer_load(
        target_dataframe=target_dataframe,
        configuration_dataframe=configuration_dataframe,
    )

    summary_hash_dataframe = create_summary_hash_dataframe(
        hashified_and_filtered_target_dataframe=hashified_and_filtered_target_dataframe,
    )

    return (
        hashified_and_filtered_target_dataframe,
        summary_hash_dataframe,
    )
