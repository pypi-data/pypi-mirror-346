from nf_common.code.services.static_code_analysis_service.common_knowledge.configuration.objects.static_code_analysis_flow_configurations import (
    StaticCodeAnalysisFlowConfigurations,
)
from nf_common.code.services.static_code_analysis_service.common_processes.analysis_results_exporters.analysis_dataframes_access_exporter import (
    export_analysis_dataframes_to_access,
)


def orchestrate_static_code_analysis_and_store_analysis_results(
    configuration: StaticCodeAnalysisFlowConfigurations,
    analysis_dataframes_dictionary: dict,
):
    export_analysis_dataframes_to_access(
        common_configuration=configuration.flow_common_configuration,
        analysis_dataframes_dictionary=analysis_dataframes_dictionary,
        enum_code_analysis_types_to_table_names_mapping=configuration.joined_enum_code_analysis_types_to_table_names_mapping,
    )
