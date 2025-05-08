import json

import pandas
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from nf_common.code.services.static_code_analysis_service.pylint_code_analysis.common_knowledge.enum_pylint_code_analysis_types import (
    EnumPylintCodeAnalysisTypes,
)
from nf_common.code.services.static_code_analysis_service.pylint_code_analysis.pylint_configuration.objects.pylint_configurations import (
    PylintConfigurations,
)
from pylint import epylint


def analyse_code_using_pylint(
    b_pylint_configuration: PylintConfigurations,
) -> dict:
    pylint_options_string = __get_pylint_options_string_from_configuration(
        b_pylint_configuration=b_pylint_configuration,
    )

    pylint_results_as_json = __get_pylint_analysis_as_json(
        pylint_options_string=pylint_options_string,
    )

    analysis_dictionary_of_dataframes = __transform_pylint_results_json_to_dictionary_of_pylint_result_dataframes(
        pylint_results_as_json=pylint_results_as_json,
    )

    return analysis_dictionary_of_dataframes


def __get_pylint_options_string_from_configuration(
    b_pylint_configuration: PylintConfigurations,
) -> str:
    input_file_system_object_paths_list = (
        []
    )

    for (
        input_file_system_object
    ) in (
        b_pylint_configuration.common_configuration.input_file_system_objects
    ):
        input_file_system_object_paths_list.append(
            input_file_system_object.absolute_path_string,
        )

    pylint_options = (
        input_file_system_object_paths_list
        + [
            "--output-format="
            + b_pylint_configuration.pylint_output_file_type,
            "--reports="
            + b_pylint_configuration.pylint_report_flag,
            "--disable="
            + ",".join(
                b_pylint_configuration.excluded_pylint_check_codes,
            ),
        ]
    )

    pylint_options_string = " ".join(
        pylint_options,
    )

    return pylint_options_string


def __get_pylint_analysis_as_json(
    pylint_options_string: str,
) -> json:
    log_message(
        message="Code is being analysed by pylint.",
    )

    (
        pylint_analysis_output,
        pylint_analysis_errors,
    ) = epylint.py_run(
        pylint_options_string,
        return_std=True,
    )

    pylint_results_as_json = (
        pylint_analysis_output
    )

    return pylint_results_as_json


def __transform_pylint_results_json_to_dictionary_of_pylint_result_dataframes(
    pylint_results_as_json: json,
) -> dict:
    pylint_results_as_dataframe = (
        pandas.read_json(
            pylint_results_as_json,
        )
    )

    pylint_results_as_dataframe.rename(
        columns={
            "message-id": "message_id",
        },
        inplace=True,
    )

    pylint_analysis_dataframes_dictionary = {
        EnumPylintCodeAnalysisTypes.REPORT: pylint_results_as_dataframe,
    }

    return pylint_analysis_dataframes_dictionary
