import psutil
from bclearer_orchestration_services.log_environment_utility_service.common_knowledge.constants import *
from bclearer_orchestration_services.log_environment_utility_service.common_knowledge.constants import (
    ENVIRONMENT_PREFIX,
)
from bclearer_orchestration_services.log_environment_utility_service.helpers.logger_helper import (
    print_header,
)
from bclearer_orchestration_services.log_environment_utility_service.helpers.units_converter import (
    convert_units,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def log_network_information():
    print_header(
        header_title="Network Information",
    )

    if_addrs = psutil.net_if_addrs()

    for (
        interface_name,
        interface_addresses,
    ) in if_addrs.items():
        for (
            address
        ) in interface_addresses:
            log_message(
                message=ENVIRONMENT_PREFIX
                + " "
                + NETWORK_INFORMATION_INTERFACE
                + " "
                + NAME_VALUE_DELIMITER
                + f" {interface_name} ===",
            )
            if (
                str(address.family)
                == "AddressFamily.AF_INET"
            ):
                log_message(
                    message=ENVIRONMENT_PREFIX
                    + " "
                    + NETWORK_INFORMATION_IP_ADDRESS
                    + " "
                    + NAME_VALUE_DELIMITER
                    + f" {address.address}",
                )

                log_message(
                    message=ENVIRONMENT_PREFIX
                    + " "
                    + NETWORK_INFORMATION_NETMASK
                    + " "
                    + NAME_VALUE_DELIMITER
                    + f" {address.netmask}",
                )

                log_message(
                    message=ENVIRONMENT_PREFIX
                    + " "
                    + NETWORK_INFORMATION_BROADCAST_IP
                    + " "
                    + NAME_VALUE_DELIMITER
                    + f" {address.broadcast}",
                )

            elif (
                str(address.family)
                == "AddressFamily.AF_PACKET"
            ):
                log_message(
                    message=ENVIRONMENT_PREFIX
                    + " "
                    + NETWORK_INFORMATION_MAC_ADDRESS
                    + " "
                    + NAME_VALUE_DELIMITER
                    + f" {address.address}",
                )

                log_message(
                    message=ENVIRONMENT_PREFIX
                    + " "
                    + NETWORK_INFORMATION_NETMASK
                    + " "
                    + NAME_VALUE_DELIMITER
                    + f" {address.netmask}",
                )

                log_message(
                    message=ENVIRONMENT_PREFIX
                    + " "
                    + NETWORK_INFORMATION_BROADCAST_MAC
                    + " "
                    + NAME_VALUE_DELIMITER
                    + f" {address.broadcast}",
                )

    net_io = psutil.net_io_counters()

    log_message(
        message=ENVIRONMENT_PREFIX
        + " "
        + NETWORK_INFORMATION_TOTAL_BYTES_SENT
        + " "
        + NAME_VALUE_DELIMITER
        + f" {convert_units(net_io.bytes_sent)}",
    )

    log_message(
        message=ENVIRONMENT_PREFIX
        + " "
        + NETWORK_INFORMATION_TOTAL_BYTES_RECEIVED
        + " "
        + NAME_VALUE_DELIMITER
        + f" {convert_units(net_io.bytes_recv)}",
    )
