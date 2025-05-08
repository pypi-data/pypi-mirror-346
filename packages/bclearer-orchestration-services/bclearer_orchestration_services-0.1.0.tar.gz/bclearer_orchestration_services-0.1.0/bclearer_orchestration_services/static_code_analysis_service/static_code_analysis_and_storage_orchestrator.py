from nf_common.code.services.static_code_analysis_service.common_knowledge.configuration.objects.static_code_analysis_flow_configurations import (
    StaticCodeAnalysisFlowConfigurations,
)
from nf_common.code.services.static_code_analysis_service.common_processes.analysis_results_exporters.analysis_dataframes_access_exporter import (
    export_analysis_dataframes_to_access,
)
from nf_common.code.services.static_code_analysis_service.static_code_analysis_orchestrator import (
    orchestrate_static_code_analysis,
)


def orchestrate_static_code_analysis_and_store_analysis_results(
    static_code_analysis_flow_configuration: StaticCodeAnalysisFlowConfigurations,
):
    all_analysis_dataframes_dictionary = orchestrate_static_code_analysis(
        static_code_analysis_flow_configuration=static_code_analysis_flow_configuration,
    )

    export_analysis_dataframes_to_access(
        common_configuration=static_code_analysis_flow_configuration.flow_common_configuration,
        analysis_dataframes_dictionary=all_analysis_dataframes_dictionary,
        enum_code_analysis_types_to_table_names_mapping=static_code_analysis_flow_configuration.joined_enum_code_analysis_types_to_table_names_mapping,
    )
