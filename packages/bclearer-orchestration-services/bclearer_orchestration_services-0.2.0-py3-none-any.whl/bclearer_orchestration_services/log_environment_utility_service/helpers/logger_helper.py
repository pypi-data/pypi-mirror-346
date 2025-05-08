from bclearer_orchestration_services.log_environment_utility_service.common_knowledge.constants import (
    ENVIRONMENT_PREFIX,
    NAME_VALUE_DELIMITER,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def print_header(
    header_title: str,
) -> None:
    log_message(
        message="=" * 40
        + " "
        + header_title
        + " "
        + "=" * 40,
    )


def log_environment_name_value_pair(
    name: str,
    value: str,
) -> None:
    message_list = [
        ENVIRONMENT_PREFIX,
        name,
        value,
    ]

    log_message(
        message=NAME_VALUE_DELIMITER.join(
            message_list,
        ),
    )


def log_environment_section(
    header_title: str,
    names_to_log: list,
    name_values: dict,
) -> None:
    print_header(
        header_title=header_title,
    )

    for name in names_to_log:
        __log_environment_name_if_required(
            name=name,
            name_values=name_values,
        )


def __log_environment_name_if_required(
    name: str,
    name_values: dict,
) -> None:
    if name not in name_values:
        return

    log_environment_name_value_pair(
        name=name,
        value=name_values[name],
    )
