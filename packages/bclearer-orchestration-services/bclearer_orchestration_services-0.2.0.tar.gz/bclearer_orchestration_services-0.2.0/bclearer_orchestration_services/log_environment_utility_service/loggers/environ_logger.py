import os

from bclearer_orchestration_services.log_environment_utility_service.common_knowledge.constants import (
    ENVIRON_INFORMATION_COMPUTERNAME,
    ENVIRON_INFORMATION_NUMBER_OF_PROCESSORS,
    ENVIRON_INFORMATION_PROCESSOR_ARCHITECTURE,
    ENVIRON_INFORMATION_PROCESSOR_IDENTIFIER,
    ENVIRON_INFORMATION_USERNAME,
    ENVIRON_INFORMATION_VIRTUAL_ENV,
)
from bclearer_orchestration_services.log_environment_utility_service.helpers.logger_helper import (
    log_environment_section,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def log_all_environ_items():
    names = os.environ.keys()

    __log_environ_items(
        names_to_log=list(names),
    )


@run_and_log_function
def log_filtered_environ_items():
    names = [
        ENVIRON_INFORMATION_USERNAME,
        ENVIRON_INFORMATION_COMPUTERNAME,
        ENVIRON_INFORMATION_NUMBER_OF_PROCESSORS,
        ENVIRON_INFORMATION_VIRTUAL_ENV,
        ENVIRON_INFORMATION_PROCESSOR_ARCHITECTURE,
        ENVIRON_INFORMATION_PROCESSOR_IDENTIFIER,
    ]

    __log_environ_items(
        names_to_log=names,
    )


@run_and_log_function
def __log_environ_items(
    names_to_log: list,
):
    log_environment_section(
        header_title="Environment Information",
        names_to_log=names_to_log,
        name_values=dict(os.environ),
    )
