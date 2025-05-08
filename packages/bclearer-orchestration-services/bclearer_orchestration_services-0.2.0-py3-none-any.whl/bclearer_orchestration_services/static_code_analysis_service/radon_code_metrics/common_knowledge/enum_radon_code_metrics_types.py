from enum import auto, unique

from nf_common.code.services.static_code_analysis_service.common_knowledge.enum_code_analysis_types import (
    EnumCodeAnalysisTypes,
)


@unique
class EnumRadonCodeMetricsTypes(
    EnumCodeAnalysisTypes,
):
    NOT_SET = auto()

    CYCLOMATIC_COMPLEXITY = auto()

    MAINTAINABILITY_INDEX = auto()

    RAW = auto()
