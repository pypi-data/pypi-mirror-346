from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from nf_common.code.services.static_code_analysis_service.common_processes.analysis_results_exporters.analysis_dataframes_access_exporter import (
    export_analysis_dataframes_to_access,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.configuration.objects.radon_configurations import (
    RadonConfigurations,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.radon_json_results_getters.radon_json_results_getter import (
    get_radon_json_results,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.radon_json_to_dataframe_converters.radon_json_to_dataframe_converter import (
    convert_radon_json_to_dataframes,
)


def calculate_and_store_radon_code_metrics(
    radon_configuration: RadonConfigurations,
):
    radon_code_metrics_dataframes_dictionary = calculate_code_metrics(
        radon_configuration=radon_configuration,
    )

    store_code_metrics(
        code_metrics_dataframes_dictionary=radon_code_metrics_dataframes_dictionary,
        configuration=radon_configuration,
    )


def calculate_code_metrics(
    radon_configuration: RadonConfigurations,
):
    log_message(
        message="Retrieving results as JSON",
    )

    results_as_json = get_radon_json_results(
        folders_to_analyse=radon_configuration.common_configuration.input_file_system_objects,
    )

    log_message(
        message="Converting results to dataframes",
    )

    code_metrics_dataframes_dictionary = convert_radon_json_to_dataframes(
        results_as_json=results_as_json,
    )

    return code_metrics_dataframes_dictionary


def store_code_metrics(
    code_metrics_dataframes_dictionary: dict,
    configuration: RadonConfigurations,
):
    log_message(
        message="Exporting results to Access",
    )

    export_analysis_dataframes_to_access(
        common_configuration=configuration.common_configuration,
        analysis_dataframes_dictionary=code_metrics_dataframes_dictionary,
        enum_code_analysis_types_to_table_names_mapping=configuration.enum_code_analysis_types_to_table_names_mapping,
    )
