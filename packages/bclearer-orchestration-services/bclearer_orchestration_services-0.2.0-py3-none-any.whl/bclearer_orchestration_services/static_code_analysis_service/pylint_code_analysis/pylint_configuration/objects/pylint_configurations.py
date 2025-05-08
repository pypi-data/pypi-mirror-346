from nf_common.code.services.static_code_analysis_service.common_knowledge.configuration.objects.static_code_analysis_common_configurations import (
    StaticCodeAnalysisCommonConfigurations,
)
from nf_common.code.services.static_code_analysis_service.common_knowledge.configuration.objects.static_code_analysis_configurations import (
    StaticCodeAnalysisConfigurations,
)
from nf_common.code.services.static_code_analysis_service.pylint_code_analysis.pylint_configuration.objects.pylint_analysis_type_to_table_names_mapping import (
    PYLINT_ANALYSIS_TYPES_TO_TABLE_NAMES_MAPPING,
)


class PylintConfigurations(
    StaticCodeAnalysisConfigurations,
):
    def __init__(
        self,
        common_configuration: StaticCodeAnalysisCommonConfigurations,
        excluded_pylint_check_codes: list,
        report_flag: bool,
        pylint_output_file_type: str,
    ):
        StaticCodeAnalysisConfigurations.__init__(
            self,
            common_configuration=common_configuration,
            enum_code_analysis_types_to_table_names_mapping=PYLINT_ANALYSIS_TYPES_TO_TABLE_NAMES_MAPPING,
        )

        self.excluded_pylint_check_codes = (
            excluded_pylint_check_codes
        )

        self.pylint_report_flag = self.__get_pylint_report_flag(
            report_flag=report_flag,
        )

        self.pylint_output_file_type = (
            pylint_output_file_type
        )

    @staticmethod
    def __get_pylint_report_flag(
        report_flag: bool,
    ):
        if report_flag:
            return "y"

        return "n"
