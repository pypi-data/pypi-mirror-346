from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from nf_common.code.services.static_code_analysis_service.common_knowledge.configuration.objects.static_code_analysis_common_configurations import (
    StaticCodeAnalysisCommonConfigurations,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.configuration.objects.radon_configurations import (
    RadonConfigurations,
)


def get_b_radon_configuration(
    input_folders: list,
    database_template_folder_relative_path: str,
    output_database_name: str,
    output_folder: Folders,
) -> RadonConfigurations:
    log_message(
        message="Getting radon configuration.",
    )

    common_configuration = StaticCodeAnalysisCommonConfigurations(
        input_file_system_objects=input_folders,
        database_template_folder_relative_path=database_template_folder_relative_path,
        output_database_name=output_database_name,
        output_folder=output_folder,
    )

    b_radon_configuration = RadonConfigurations(
        common_configuration=common_configuration,
    )

    return b_radon_configuration


def get_radon_configuration_from_common_configuration(
    common_configuration: StaticCodeAnalysisCommonConfigurations,
) -> RadonConfigurations:
    log_message(
        message="Getting radon configuration.",
    )

    b_radon_configuration = RadonConfigurations(
        common_configuration=common_configuration,
    )

    return b_radon_configuration
