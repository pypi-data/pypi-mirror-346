import json

from nf_common.code.services.static_code_analysis_service.radon_code_metrics.radon_configuration_getters.cyclomatic_complexity_radon_configuration_getter import (
    get_cyclomatic_complexity_configuration,
)
from radon import cli


def get_cyclomatic_complexity_radon_json_results(
    folders_to_analyse: list,
):
    cyclomatic_complexity_configuration = (
        get_cyclomatic_complexity_configuration()
    )

    paths = []

    for (
        folder_to_analyse
    ) in folders_to_analyse:
        paths.append(
            folder_to_analyse.absolute_path_string,
        )

    cyclomatic_complexity_havester = cli.CCHarvester(
        paths=paths,
        config=cyclomatic_complexity_configuration,
    )

    cyclomatic_complexity_results_as_json_string = (
        cyclomatic_complexity_havester.as_json()
    )

    cyclomatic_complexity_results_as_json = json.loads(
        s=cyclomatic_complexity_results_as_json_string,
    )

    return cyclomatic_complexity_results_as_json
