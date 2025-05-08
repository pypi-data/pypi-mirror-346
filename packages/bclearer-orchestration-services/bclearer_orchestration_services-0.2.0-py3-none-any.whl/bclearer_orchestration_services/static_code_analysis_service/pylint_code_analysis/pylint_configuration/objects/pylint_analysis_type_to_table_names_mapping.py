from nf_common.code.services.static_code_analysis_service.pylint_code_analysis.common_knowledge.enum_pylint_code_analysis_types import (
    EnumPylintCodeAnalysisTypes,
)

PYLINT_ANALYSIS_TYPES_TO_TABLE_NAMES_MAPPING = {
    EnumPylintCodeAnalysisTypes.REPORT: "pylint_issues",
}
