from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.common_knowledge.enum_radon_code_metrics_types import (
    EnumRadonCodeMetricsTypes,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.radon_json_to_dataframe_converters.cyclomatic_complexity_radon_json_to_dataframe_converter import (
    convert_cyclomatic_complexity_radon_json_to_dataframe,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.radon_json_to_dataframe_converters.maintainability_index_radon_json_to_dataframe_converter import (
    convert_maintainability_index_radon_json_to_dataframe,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.radon_json_to_dataframe_converters.raw_radon_json_to_dataframe_converter import (
    convert_raw_radon_json_to_dataframe,
)


def convert_radon_json_to_dataframes(
    results_as_json: dict,
) -> dict:
    log_message(
        message="\tConverting cyclomatic complexity results",
    )

    cyclomatic_complexity_radon_dataframe = convert_cyclomatic_complexity_radon_json_to_dataframe(
        results_as_json=results_as_json[
            EnumRadonCodeMetricsTypes.CYCLOMATIC_COMPLEXITY
        ],
    )

    log_message(
        message="\tConverting maintainability index results",
    )

    maintainability_index_radon_dataframe = convert_maintainability_index_radon_json_to_dataframe(
        results_as_json=results_as_json[
            EnumRadonCodeMetricsTypes.MAINTAINABILITY_INDEX
        ],
    )

    log_message(
        message="\tConverting raw results",
    )

    raw_radon_dataframe = convert_raw_radon_json_to_dataframe(
        results_as_json=results_as_json[
            EnumRadonCodeMetricsTypes.RAW
        ],
    )

    radon_dataframes = {
        EnumRadonCodeMetricsTypes.CYCLOMATIC_COMPLEXITY: cyclomatic_complexity_radon_dataframe,
        EnumRadonCodeMetricsTypes.MAINTAINABILITY_INDEX: maintainability_index_radon_dataframe,
        EnumRadonCodeMetricsTypes.RAW: raw_radon_dataframe,
    }

    return radon_dataframes
