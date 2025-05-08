import psutil
from bclearer_orchestration_services.log_environment_utility_service.common_knowledge.constants import *
from bclearer_orchestration_services.log_environment_utility_service.helpers.logger_helper import (
    log_environment_section,
)
from bclearer_orchestration_services.log_environment_utility_service.helpers.units_converter import (
    convert_units,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def log_all_memory_information():
    names = list(
        __get_name_values().keys(),
    )

    __log_memory_information(
        names_to_log=list(names),
    )


@run_and_log_function
def log_filtered_memory_information():
    names = [
        MEMORY_INFORMATION_VIRTUAL_TOTAL,
        MEMORY_INFORMATION_VIRTUAL_AVAILABLE,
        MEMORY_INFORMATION_VIRTUAL_USED,
    ]

    __log_memory_information(
        names_to_log=names,
    )


@run_and_log_function
def __log_memory_information(
    names_to_log: list,
):
    name_values = __get_name_values()

    log_environment_section(
        header_title="Memory Information",
        names_to_log=names_to_log,
        name_values=name_values,
    )


def __get_name_values() -> dict:
    svmem = psutil.virtual_memory()

    swap = psutil.swap_memory()

    name_values = {
        MEMORY_INFORMATION_VIRTUAL_TOTAL: f"{convert_units(svmem.total)}",
        MEMORY_INFORMATION_VIRTUAL_AVAILABLE: f"{convert_units(svmem.available)}",
        MEMORY_INFORMATION_VIRTUAL_USED: f"{convert_units(svmem.used)}",
        MEMORY_INFORMATION_VIRTUAL_PERCENTAGE: f"{svmem.percent}%",
        MEMORY_INFORMATION_SWAP_TOTAL: f"{convert_units(swap.total)}",
        MEMORY_INFORMATION_SWAP_FREE: f"{convert_units(swap.free)}",
        MEMORY_INFORMATION_SWAP_USED: f"{convert_units(swap.used)}",
        MEMORY_INFORMATION_SWAP_PERCENTAGE: f"{swap.percent}%",
    }

    return name_values
