from bclearer_interop_services.b_dictionary_service.python_extension_services import (
    join_dictionaries,
)
from nf_common.code.services.static_code_analysis_service.common_knowledge.configuration.objects.static_code_analysis_common_configurations import (
    StaticCodeAnalysisCommonConfigurations,
)
from nf_common.code.services.static_code_analysis_service.pylint_code_analysis.pylint_configuration.objects.pylint_configurations import (
    PylintConfigurations,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.configuration.objects.radon_configurations import (
    RadonConfigurations,
)


class StaticCodeAnalysisFlowConfigurations:
    def __init__(
        self,
        pylint_configuration: PylintConfigurations,
        radon_configuration: RadonConfigurations,
        flow_common_configuration: StaticCodeAnalysisCommonConfigurations,
    ):
        self.pylint_configuration = (
            pylint_configuration
        )

        self.radon_configuration = (
            radon_configuration
        )

        self.flow_common_configuration = (
            flow_common_configuration
        )

        self.joined_enum_code_analysis_types_to_table_names_mapping = join_dictionaries(
            dictionaries=[
                pylint_configuration.enum_code_analysis_types_to_table_names_mapping,
                radon_configuration.enum_code_analysis_types_to_table_names_mapping,
            ],
        )
