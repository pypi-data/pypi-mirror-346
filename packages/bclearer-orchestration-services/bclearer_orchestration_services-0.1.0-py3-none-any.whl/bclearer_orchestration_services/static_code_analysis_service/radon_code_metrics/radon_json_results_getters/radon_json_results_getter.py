from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.common_knowledge.enum_radon_code_metrics_types import (
    EnumRadonCodeMetricsTypes,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.radon_json_results_getters.cyclomatic_complexity_radon_json_results_getter import (
    get_cyclomatic_complexity_radon_json_results,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.radon_json_results_getters.maintainability_index_radon_json_results_getter import (
    get_maintainability_index_radon_json_results,
)
from nf_common.code.services.static_code_analysis_service.radon_code_metrics.radon_json_results_getters.raw_radon_json_results_getter import (
    get_raw_radon_json_results,
)


def get_radon_json_results(
    folders_to_analyse: list,
) -> dict:
    log_message(
        message="\tRetrieving cyclomatic complexity results",
    )

    cyclomatic_complexity_radon_json_results = get_cyclomatic_complexity_radon_json_results(
        folders_to_analyse=folders_to_analyse,
    )

    log_message(
        message="\tRetrieving maintainability index results",
    )

    maintainability_index_radon_json_results = get_maintainability_index_radon_json_results(
        folders_to_analyse=folders_to_analyse,
    )

    log_message(
        message="\tRetrieving raw results",
    )

    raw_radon_json_results = get_raw_radon_json_results(
        folders_to_analyse=folders_to_analyse,
    )

    radon_json_results = {
        EnumRadonCodeMetricsTypes.CYCLOMATIC_COMPLEXITY: cyclomatic_complexity_radon_json_results,
        EnumRadonCodeMetricsTypes.MAINTAINABILITY_INDEX: maintainability_index_radon_json_results,
        EnumRadonCodeMetricsTypes.RAW: raw_radon_json_results,
    }

    return radon_json_results
