import pandas
from bclearer_interop_services.relational_database_services.access_service.access import (
    write_dataframes_to_access,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from nf_common.code.services.static_code_analysis_service.common_knowledge.configuration.objects.static_code_analysis_common_configurations import (
    StaticCodeAnalysisCommonConfigurations,
)
from nf_common.code.services.static_code_analysis_service.common_knowledge.enum_code_analysis_types import (
    EnumCodeAnalysisTypes,
)
from nf_common.code.services.static_code_analysis_service.common_processes.analysis_results_exporters.analysis_results_database_creator import (
    create_results_database_file,
)


def export_analysis_dataframes_to_access(
    common_configuration: StaticCodeAnalysisCommonConfigurations,
    enum_code_analysis_types_to_table_names_mapping: dict,
    analysis_dataframes_dictionary: dict,
):
    log_message(
        message="Analysis results are being stored.",
    )

    dataframes_dictionary_keyed_on_name_string = __convert_dictionary_to_keyed_on_name_string(
        analysis_dataframes_dictionary=analysis_dataframes_dictionary,
        enum_code_analysis_types_to_table_names_mapping=enum_code_analysis_types_to_table_names_mapping,
    )

    results_database_file = create_results_database_file(
        results_folder=common_configuration.output_folder,
        database_template_folder_path=common_configuration.database_template_folder_relative_path,
        database_template_name="static_code_analysis_template.accdb",
        results_database_name=common_configuration.output_database_name,
    )

    write_dataframes_to_access(
        dataframes_dictionary_keyed_on_string=dataframes_dictionary_keyed_on_name_string,
        database_file=results_database_file,
        temporary_csv_folder=common_configuration.output_folder,
    )


def __convert_dictionary_to_keyed_on_name_string(
    analysis_dataframes_dictionary: dict,
    enum_code_analysis_types_to_table_names_mapping: dict,
) -> dict:
    dataframes_dictionary_keyed_on_name_string = (
        {}
    )

    for (
        code_analysis_type,
        dataframe,
    ) in (
        analysis_dataframes_dictionary.items()
    ):
        __add_dataframe_to_dictionary(
            dataframes_dictionary_keyed_on_name_string=dataframes_dictionary_keyed_on_name_string,
            enum_code_analysis_types_to_table_names_mapping=enum_code_analysis_types_to_table_names_mapping,
            code_analysis_type=code_analysis_type,
            dataframe=dataframe,
        )

    return dataframes_dictionary_keyed_on_name_string


def __add_dataframe_to_dictionary(
    dataframes_dictionary_keyed_on_name_string: dict,
    enum_code_analysis_types_to_table_names_mapping: dict,
    code_analysis_type: EnumCodeAnalysisTypes,
    dataframe: pandas.DataFrame,
):
    dataframe_name = enum_code_analysis_types_to_table_names_mapping[
        code_analysis_type
    ]

    dataframes_dictionary_keyed_on_name_string[
        dataframe_name
    ] = dataframe
