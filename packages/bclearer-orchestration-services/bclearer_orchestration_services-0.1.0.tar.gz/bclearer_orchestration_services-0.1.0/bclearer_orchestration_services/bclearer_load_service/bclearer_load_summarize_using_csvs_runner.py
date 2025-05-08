from bclearer_interop_services.delimited_text.utf_8_csv_reader import (
    convert_utf_8_csv_with_header_file_to_dataframe,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.bclearer_load_service.bclearer_load_summarize_orchestrator import (
    orchestrate_bclearer_load_summarize,
)
from bclearer_orchestration_services.bclearer_load_service.summarize.summary_table_reporter import (
    report_summary_table,
)


def run_bclearer_load_summarize_using_csvs(
    target_file: Files,
    output_root_folder: Folders,
    run_suffix: str,
) -> None:
    target_dataframe = convert_utf_8_csv_with_header_file_to_dataframe(
        target_file,
    )

    summary_dataframe = orchestrate_bclearer_load_summarize(
        target_dataframe=target_dataframe,
    )

    report_summary_table(
        output_root_folder=output_root_folder,
        summary_dataframe=summary_dataframe,
        run_suffix=run_suffix,
    )
