import platform

from bclearer_orchestration_services.log_environment_utility_service.common_knowledge.constants import *
from bclearer_orchestration_services.log_environment_utility_service.helpers.logger_helper import (
    log_environment_section,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def log_all_system_items():
    names = list(
        __get_name_values().keys(),
    )

    __log_system_information(
        names_to_log=list(names),
    )


@run_and_log_function
def log_filtered_system_items():
    names = [
        SYSTEM_INFORMATION_SYSTEM,
        SYSTEM_INFORMATION_RELEASE,
        SYSTEM_INFORMATION_VERSION,
    ]

    __log_system_information(
        names_to_log=names,
    )


@run_and_log_function
def __log_system_information(
    names_to_log: list,
):
    name_values = __get_name_values()

    log_environment_section(
        header_title="System Information",
        names_to_log=names_to_log,
        name_values=name_values,
    )


def __get_name_values() -> dict:
    uname = platform.uname()

    name_values = {
        SYSTEM_INFORMATION_SYSTEM: uname.system,
        SYSTEM_INFORMATION_NODE_NAME: uname.node,
        SYSTEM_INFORMATION_RELEASE: uname.release,
        SYSTEM_INFORMATION_VERSION: uname.version,
        SYSTEM_INFORMATION_MACHINE: uname.machine,
        SYSTEM_INFORMATION_PROCESSOR: uname.processor,
    }

    return name_values
