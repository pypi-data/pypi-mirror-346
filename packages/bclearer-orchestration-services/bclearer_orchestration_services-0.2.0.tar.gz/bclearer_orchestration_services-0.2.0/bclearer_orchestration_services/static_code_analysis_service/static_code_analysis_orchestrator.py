from bclearer_interop_services.b_dictionary_service.python_extension_services import (
    join_dictionaries,
)
from nf_common.code.services.static_code_analysis_service.common_knowledge.configuration.objects.static_code_analysis_flow_configurations import (
    StaticCodeAnalysisFlowConfigurations,
)
from nf_common.code.services.static_code_analysis_service.pylint_code_analysis.pylint_analysers.pylint_analyser import (
    analyse_code_using_pylint,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.radon_orchestrator import (
    calculate_code_metrics,
)


def orchestrate_static_code_analysis(
    static_code_analysis_flow_configuration: StaticCodeAnalysisFlowConfigurations,
) -> dict:
    radon_code_metrics_dataframes_dictionary = calculate_code_metrics(
        radon_configuration=static_code_analysis_flow_configuration.radon_configuration,
    )

    pylint_analysis_dataframes_dictionary = analyse_code_using_pylint(
        b_pylint_configuration=static_code_analysis_flow_configuration.pylint_configuration,
    )

    all_analysis_dataframes_dictionary = join_dictionaries(
        dictionaries=[
            radon_code_metrics_dataframes_dictionary,
            pylint_analysis_dataframes_dictionary,
        ],
    )

    return all_analysis_dataframes_dictionary
