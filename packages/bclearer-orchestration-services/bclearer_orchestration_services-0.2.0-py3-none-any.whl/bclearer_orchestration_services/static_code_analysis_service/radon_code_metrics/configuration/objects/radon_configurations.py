from nf_common.code.services.static_code_analysis_service.common_knowledge.configuration.objects.static_code_analysis_common_configurations import (
    StaticCodeAnalysisCommonConfigurations,
)
from nf_common.code.services.static_code_analysis_service.common_knowledge.configuration.objects.static_code_analysis_configurations import (
    StaticCodeAnalysisConfigurations,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.common_knowledge.radon_code_metrics_type_mappings import (
    RADON_CODE_METRICS_TYPE_TO_NAME_MAPPING,
)


class RadonConfigurations(
    StaticCodeAnalysisConfigurations,
):
    def __init__(
        self,
        common_configuration: StaticCodeAnalysisCommonConfigurations,
    ):
        StaticCodeAnalysisConfigurations.__init__(
            self,
            common_configuration=common_configuration,
            enum_code_analysis_types_to_table_names_mapping=RADON_CODE_METRICS_TYPE_TO_NAME_MAPPING,
        )
