from nf_common.code.services.static_code_analysis_service.common_knowledge.configuration.objects.static_code_analysis_common_configurations import (
    StaticCodeAnalysisCommonConfigurations,
)


class StaticCodeAnalysisConfigurations:
    def __init__(
        self,
        common_configuration: StaticCodeAnalysisCommonConfigurations,
        enum_code_analysis_types_to_table_names_mapping: dict,
    ):
        self.common_configuration = (
            common_configuration
        )

        self.enum_code_analysis_types_to_table_names_mapping = enum_code_analysis_types_to_table_names_mapping
