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
def log_all_disk_information():
    names = list(
        __get_name_values().keys(),
    )

    __log_disk_information(
        names_to_log=list(names),
    )


@run_and_log_function
def __log_disk_information(
    names_to_log: list,
):
    name_values = __get_name_values()

    log_environment_section(
        header_title="Disk Information",
        names_to_log=names_to_log,
        name_values=name_values,
    )


def __get_name_values() -> dict:
    disk_io = psutil.disk_io_counters()

    name_values = {
        DISK_INFORMATION_TOTAL_READ: f"{convert_units(disk_io.read_bytes)}",
        DISK_INFORMATION_TOTAL_WRITE: f"{convert_units(disk_io.write_bytes)}",
    }

    partitions = (
        psutil.disk_partitions()
    )

    for partition in partitions:
        __add_partition_name_values(
            name_values=name_values,
            partition=partition,
        )

    return name_values


def __add_partition_name_values(
    name_values: dict,
    partition,
) -> dict:
    mountpoint = (
        f"{partition.mountpoint}"
    )

    fstype = f"{partition.fstype}"

    prefix = (
        "("
        + mountpoint
        + " "
        + fstype
        + ")"
    )

    try:
        partition_usage = (
            psutil.disk_usage(
                partition.mountpoint,
            )
        )
    except PermissionError:
        return name_values

    partition_name_values = {
        prefix
        + " "
        + DISK_INFORMATION_TOTAL_SIZE: f"{convert_units(partition_usage.total)}",
        prefix
        + " "
        + DISK_INFORMATION_USED: f"{convert_units(partition_usage.used)}",
        prefix
        + " "
        + DISK_INFORMATION_FREE: f"{convert_units(partition_usage.free)}",
        prefix
        + " "
        + DISK_INFORMATION_PERCENTAGE: f"{partition_usage.percent}%",
    }

    name_values.update(
        partition_name_values,
    )

    return name_values
