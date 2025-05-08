import pandas
from bclearer_orchestration_services.bclearer_load_service.summarize.summary_hash_dataframe_creator import (
    create_summary_hash_dataframe,
)


def orchestrate_bclearer_load_summarize(
    target_dataframe: pandas.DataFrame,
) -> pandas.DataFrame:
    summary_hash_dataframe = create_summary_hash_dataframe(
        hashified_and_filtered_target_dataframe=target_dataframe,
    )

    return summary_hash_dataframe
