import json

from nf_common.code.services.static_code_analysis_service.radon_code_metrics.radon_configuration_getters.raw_radon_configuration_getter import (
    get_raw_configuration,
)
from radon import cli


def get_raw_radon_json_results(
    folders_to_analyse: list,
):
    raw_configuration = (
        get_raw_configuration()
    )

    paths = []

    for (
        folder_to_analyse
    ) in folders_to_analyse:
        paths.append(
            folder_to_analyse.absolute_path_string,
        )

    raw_havester = cli.RawHarvester(
        paths=paths,
        config=raw_configuration,
    )

    raw_results_as_json_string = (
        raw_havester.as_json()
    )

    raw_results_as_json = json.loads(
        s=raw_results_as_json_string,
    )

    return raw_results_as_json
