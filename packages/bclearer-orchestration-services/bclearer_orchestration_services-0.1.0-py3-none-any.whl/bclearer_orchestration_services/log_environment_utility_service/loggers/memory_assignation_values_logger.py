import psutil
from nf_common.code.services.log_environment_utility_service.common_knowledge.constants import *
from nf_common.code.services.log_environment_utility_service.common_loggers import (
    CommonLoggers,
)
from nf_common.code.services.log_environment_utility_service.helpers.units_converter import (
    convert_units,
)


def log_memory_assignation_values(
    logger: CommonLoggers,
) -> None:
    virtual_memory_information = (
        psutil.virtual_memory()
    )

    swap = psutil.swap_memory()

    names = [
        MEMORY_INFORMATION_VIRTUAL_TOTAL,
        MEMORY_INFORMATION_VIRTUAL_AVAILABLE,
        MEMORY_INFORMATION_VIRTUAL_USED,
    ]

    name_values = {
        MEMORY_INFORMATION_VIRTUAL_TOTAL: f"{convert_units(virtual_memory_information.total)}",
        MEMORY_INFORMATION_VIRTUAL_AVAILABLE: f"{convert_units(virtual_memory_information.available)}",
        MEMORY_INFORMATION_VIRTUAL_USED: f"{convert_units(virtual_memory_information.used)}",
        MEMORY_INFORMATION_VIRTUAL_PERCENTAGE: f"{virtual_memory_information.percent}%",
        MEMORY_INFORMATION_SWAP_TOTAL: f"{convert_units(swap.total)}",
        MEMORY_INFORMATION_SWAP_FREE: f"{convert_units(swap.free)}",
        MEMORY_INFORMATION_SWAP_USED: f"{convert_units(swap.used)}",
        MEMORY_INFORMATION_SWAP_PERCENTAGE: f"{swap.percent}%",
    }

    __log_environment_section(
        logger=logger,
        header_title="Memory Information",
        names_to_log=names,
        name_values=name_values,
    )


def __log_environment_section(
    logger: CommonLoggers,
    header_title: str,
    names_to_log: list,
    name_values: dict,
) -> None:
    logger.info(
        msg="=" * 40
        + " "
        + header_title
        + " "
        + "=" * 40,
    )

    for name in names_to_log:
        __log_environment_name_if_required(
            logger=logger,
            name=name,
            name_values=name_values,
        )


def __log_environment_name_if_required(
    logger: CommonLoggers,
    name: str,
    name_values: dict,
) -> None:
    if name not in name_values:
        return

    __log_environment_name_value_pair(
        logger=logger,
        name=name,
        value=name_values[name],
    )


def __log_environment_name_value_pair(
    logger: CommonLoggers,
    name: str,
    value: str,
) -> None:
    message_list = [
        ENVIRONMENT_PREFIX,
        name,
        value,
    ]

    logger.info(
        msg=NAME_VALUE_DELIMITER.join(
            message_list,
        ),
    )
