from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from nf_common.code.services.static_code_analysis_service.common_knowledge.configuration.objects.static_code_analysis_common_configurations import (
    StaticCodeAnalysisCommonConfigurations,
)
from nf_common.code.services.static_code_analysis_service.pylint_code_analysis.pylint_configuration.objects.pylint_configurations import (
    PylintConfigurations,
)

B_EXCLUDED_CHECK_CODES = [
    "C0301",
    "C0111",
    "R0903",
]


def get_b_pylint_configuration(
    input_folders: list,
    database_template_folder_relative_path: str,
    output_database_name: str,
    output_folder: Folders,
) -> PylintConfigurations:
    log_message(
        message="Getting pylint configuration.",
    )

    common_configuration = StaticCodeAnalysisCommonConfigurations(
        input_file_system_objects=input_folders,
        database_template_folder_relative_path=database_template_folder_relative_path,
        output_database_name=output_database_name,
        output_folder=output_folder,
    )

    b_pylint_configuration = PylintConfigurations(
        common_configuration=common_configuration,
        excluded_pylint_check_codes=B_EXCLUDED_CHECK_CODES,
        report_flag=True,
        pylint_output_file_type="json_service",
    )

    return b_pylint_configuration


def get_pylint_configuration_from_common_configuration(
    common_configuration: StaticCodeAnalysisCommonConfigurations,
) -> PylintConfigurations:
    log_message(
        message="Getting pylint configuration.",
    )

    b_pylint_configuration = PylintConfigurations(
        common_configuration=common_configuration,
        excluded_pylint_check_codes=B_EXCLUDED_CHECK_CODES,
        report_flag=True,
        pylint_output_file_type="json_service",
    )

    return b_pylint_configuration
