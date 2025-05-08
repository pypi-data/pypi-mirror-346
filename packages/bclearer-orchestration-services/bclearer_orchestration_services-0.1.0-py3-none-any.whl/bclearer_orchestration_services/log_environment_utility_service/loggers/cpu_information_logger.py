import psutil
from bclearer_orchestration_services.log_environment_utility_service.common_knowledge.constants import *
from bclearer_orchestration_services.log_environment_utility_service.helpers.logger_helper import (
    log_environment_section,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def log_all_cpu_information():
    names = list(
        __get_name_values().keys(),
    )

    __log_cpu_information(
        names_to_log=list(names),
    )


@run_and_log_function
def log_filtered_cpu_information():
    names = [
        CPU_INFORMATION_PHYSICAL_CORES,
        CPU_INFORMATION_TOTAL_CORES,
        CPU_INFORMATION_TOTAL_CPU_USAGE,
    ]

    __log_cpu_information(
        names_to_log=names,
    )


@run_and_log_function
def __log_cpu_information(
    names_to_log: list,
):
    name_values = __get_name_values()

    log_environment_section(
        header_title="CPU Information",
        names_to_log=names_to_log,
        name_values=name_values,
    )


def __get_name_values() -> dict:
    cpufreq = psutil.cpu_freq()

    name_values = {
        CPU_INFORMATION_PHYSICAL_CORES: f"{psutil.cpu_count(logical=False)}",
        CPU_INFORMATION_TOTAL_CORES: f"{psutil.cpu_count(logical=True)}",
        CPU_INFORMATION_MAX_FREQUENCY: f"{cpufreq.max:.2f}Mhz",
        CPU_INFORMATION_MIN_FREQUENCY: f"{cpufreq.min:.2f}Mhz",
        CPU_INFORMATION_CURRENT_FREQUENCY: f"{cpufreq.current:.2f}Mhz",
        CPU_INFORMATION_TOTAL_CPU_USAGE: f"{psutil.cpu_percent()}%",
    }

    for i, percentage in enumerate(
        psutil.cpu_percent(
            percpu=True,
            interval=1,
        ),
    ):
        name_values[
            CPU_INFORMATION_CORE_PREFIX
            + f" {i}"
        ] = f" {percentage}%"

    return name_values
