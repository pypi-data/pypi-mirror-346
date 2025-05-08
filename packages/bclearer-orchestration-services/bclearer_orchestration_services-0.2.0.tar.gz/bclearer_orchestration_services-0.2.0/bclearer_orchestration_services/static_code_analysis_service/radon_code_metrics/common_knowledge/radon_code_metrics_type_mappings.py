from nf_common.code.services.static_code_analysis_service.radon_code_metrics.common_knowledge.enum_radon_code_metrics_types import (
    EnumRadonCodeMetricsTypes,
)

RADON_CODE_METRICS_TYPE_TO_NAME_MAPPING = {
    EnumRadonCodeMetricsTypes.CYCLOMATIC_COMPLEXITY: "cyclomatic_complexities",
    EnumRadonCodeMetricsTypes.MAINTAINABILITY_INDEX: "maintainability_indices",
    EnumRadonCodeMetricsTypes.RAW: "raw_metrics",
}
