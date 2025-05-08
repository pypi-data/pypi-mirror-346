from nf_common.code.services.static_code_analysis_service.common_processes.analysis_results_exporters.analysis_dataframes_access_exporter import (
    export_analysis_dataframes_to_access,
)
from nf_common.code.services.static_code_analysis_service.pylint_code_analysis.pylint_analysers.pylint_analyser import (
    analyse_code_using_pylint,
)
from nf_common.code.services.static_code_analysis_service.pylint_code_analysis.pylint_configuration.objects.pylint_configurations import (
    PylintConfigurations,
)


def orchestrate_pylint_analysis(
    b_pylint_configuration: PylintConfigurations,
):
    pylint_analysis_dataframes_dictionary = analyse_code_using_pylint(
        b_pylint_configuration=b_pylint_configuration,
    )

    export_analysis_dataframes_to_access(
        analysis_dataframes_dictionary=pylint_analysis_dataframes_dictionary,
        common_configuration=b_pylint_configuration.common_configuration,
        enum_code_analysis_types_to_table_names_mapping=b_pylint_configuration.enum_code_analysis_types_to_table_names_mapping,
    )
