from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.bclearer_load_service.bclearer_load_hashify_and_summarize_using_csvs_orchestrator import (
    orchestrate_bclearer_load_hashify_and_summarize_using_csvs,
)
from bclearer_orchestration_services.bclearer_load_service.common.hashed_and_summarised_tables_reporter import (
    report_hashed_and_summarised_tables,
)


def run_bclearer_load_hashify_and_summarize_using_csvs_and_report(
    target_file: Files,
    configuration_file: Files,
    output_root_folder: Folders,
    run_suffix: str,
) -> None:
    (
        hashified_dataframe,
        summary_dataframe,
    ) = orchestrate_bclearer_load_hashify_and_summarize_using_csvs(
        target_file=target_file,
        configuration_file=configuration_file,
    )

    report_hashed_and_summarised_tables(
        output_root_folder=output_root_folder,
        hashified_dataframe=hashified_dataframe,
        summary_dataframe=summary_dataframe,
        run_suffix=run_suffix,
    )
