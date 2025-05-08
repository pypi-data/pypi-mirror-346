from bclearer_interop_services.delimited_text.utf_8_csv_reader import (
    convert_utf_8_csv_with_header_file_to_dataframe,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_orchestration_services.bclearer_load_service.bclearer_load_hashify_and_summarize_orchestrator import (
    orchestrate_bclearer_load_hashify_and_summarize,
)


def orchestrate_bclearer_load_hashify_and_summarize_using_csvs(
    target_file: Files,
    configuration_file: Files,
) -> tuple:
    target_dataframe = convert_utf_8_csv_with_header_file_to_dataframe(
        target_file,
    )

    configuration_dataframe = convert_utf_8_csv_with_header_file_to_dataframe(
        configuration_file,
    )

    (
        hashified_dataframe,
        summary_dataframe,
    ) = orchestrate_bclearer_load_hashify_and_summarize(
        target_dataframe=target_dataframe,
        configuration_dataframe=configuration_dataframe,
    )

    return (
        hashified_dataframe,
        summary_dataframe,
    )
