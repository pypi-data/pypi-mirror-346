import pandas
from bclearer_interop_services.delimited_text import (
    write_dataframe_to_csv_file,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.bclearer_load_service.common.output_folder_creator import (
    create_output_folder,
)
from bclearer_orchestration_services.bclearer_load_service.common_knowledge.bclearer_load_constants import (
    HASHIFIED_OUTPUT_TABLE_NAME,
    SUMMARY_OUTPUT_TABLE_NAME,
)


def report_hashed_and_summarised_tables(
    output_root_folder: Folders,
    hashified_dataframe: pandas.DataFrame,
    summary_dataframe: pandas.DataFrame,
    run_suffix: str,
) -> None:
    output_folder_path = create_output_folder(
        output_root_folder=output_root_folder,
        run_suffix=run_suffix,
    )

    write_dataframe_to_csv_file(
        folder_name=output_folder_path,
        dataframe_name=HASHIFIED_OUTPUT_TABLE_NAME,
        dataframe=hashified_dataframe,
    )

    write_dataframe_to_csv_file(
        folder_name=output_folder_path,
        dataframe_name=SUMMARY_OUTPUT_TABLE_NAME,
        dataframe=summary_dataframe,
    )
