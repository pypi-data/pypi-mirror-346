from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from nf_common.code.services.datetime_service.time_helpers.time_getter import (
    now_time_as_string_yyyymmddhhmm,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from nf_common.code.services.static_code_analysis_service.common_knowledge.configuration.objects.static_code_analysis_common_configurations import (
    StaticCodeAnalysisCommonConfigurations,
)
from nf_common.code.services.static_code_analysis_service.common_knowledge.configuration.objects.static_code_analysis_flow_configurations import (
    StaticCodeAnalysisFlowConfigurations,
)
from nf_common.code.services.static_code_analysis_service.pylint_code_analysis.pylint_configuration.getters.b_pylint_configuration_getter import (
    get_pylint_configuration_from_common_configuration,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.configuration.getters.b_radon_configuration_getter import (
    get_radon_configuration_from_common_configuration,
)


def get_static_code_configuration(
    paths_of_code_to_analyse: list,
    results_folder: Folders,
) -> (
    StaticCodeAnalysisFlowConfigurations
):
    log_message(
        message="Getting configuration for flow of static analysis.",
    )

    output_database_name = (
        "static_code_analysis"
        + "_"
        + now_time_as_string_yyyymmddhhmm()
        + ".accdb"
    )

    database_template_folder_relative_path = "nf_common.resources.static_code_analysis"

    common_configuration = StaticCodeAnalysisCommonConfigurations(
        input_file_system_objects=paths_of_code_to_analyse,
        database_template_folder_relative_path=database_template_folder_relative_path,
        output_database_name=output_database_name,
        output_folder=results_folder,
    )

    radon_configuration = get_radon_configuration_from_common_configuration(
        common_configuration=common_configuration,
    )

    pylint_configuration = get_pylint_configuration_from_common_configuration(
        common_configuration=common_configuration,
    )

    static_code_flow_configuration = StaticCodeAnalysisFlowConfigurations(
        pylint_configuration=pylint_configuration,
        radon_configuration=radon_configuration,
        flow_common_configuration=common_configuration,
    )

    return (
        static_code_flow_configuration
    )
