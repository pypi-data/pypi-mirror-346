import json

from nf_common.code.services.static_code_analysis_service.radon_code_metrics.radon_configuration_getters.maintainability_index_radon_configuration_getter import (
    get_maintainability_index_configuration,
)
from radon import cli


def get_maintainability_index_radon_json_results(
    folders_to_analyse: list,
):
    maintainability_index_configuration = (
        get_maintainability_index_configuration()
    )

    paths = []

    for (
        folder_to_analyse
    ) in folders_to_analyse:
        paths.append(
            folder_to_analyse.absolute_path_string,
        )

    maintainability_index_havester = cli.MIHarvester(
        paths=paths,
        config=maintainability_index_configuration,
    )

    maintainability_index_results_as_json_string = (
        maintainability_index_havester.as_json()
    )

    maintainability_index_results_as_json = json.loads(
        s=maintainability_index_results_as_json_string,
    )

    return maintainability_index_results_as_json
