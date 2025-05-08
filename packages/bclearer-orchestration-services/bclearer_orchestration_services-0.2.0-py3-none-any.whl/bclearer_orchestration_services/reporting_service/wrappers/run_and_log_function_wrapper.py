import time

import psutil
from bclearer_orchestration_services.log_environment_utility_service.common_knowledge.constants import *
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def log_timing_header():
    column_names = [
        TIMING_PREFIX,
        "action",
        "function",
        "total_cpu_usage (%)",
        "total_memory (GB)",
        "available_memory (GB)",
        "used_memory (GB)",
        "duration (s)",
    ]

    log_message(
        message=NAME_VALUE_DELIMITER.join(
            column_names,
        ),
    )


def run_and_log_function(function):
    def timed(*args, **kwargs):
        start_time = time.time()

        __log_start(function=function)

        return_value = function(
            *args,
            **kwargs,
        )

        __log_finish(
            start_time=start_time,
            function=function,
        )

        return return_value

    return timed


def __log_start(function):
    message_list = __get_standard_list(
        action="start",
        function=function,
    )

    log_message(
        message=NAME_VALUE_DELIMITER.join(
            message_list,
        ),
    )


def __log_finish(
    start_time: time,
    function,
):
    message_list = __get_standard_list(
        action="end",
        function=function,
    )

    end_time = time.time()

    duration = (
        f"{end_time - start_time:.2f}"
    )

    message_list.append(duration)

    log_message(
        message=NAME_VALUE_DELIMITER.join(
            message_list,
        ),
    )


def __get_standard_list(
    action: str,
    function,
):
    total_cpu_usage = (
        f"{psutil.cpu_percent()}%"
    )

    svmem = psutil.virtual_memory()

    total_memory = f"{__get_gigabytes(byte_count=svmem.total):.2f}"

    available_memory = f"{__get_gigabytes(byte_count=svmem.available):.2f}"

    used_memory = f"{__get_gigabytes(byte_count=svmem.used):.2f}"

    standard_list = [
        TIMING_PREFIX,
        action,
        function.__name__,
        total_cpu_usage,
        total_memory,
        available_memory,
        used_memory,
    ]

    return standard_list


def __get_gigabytes(byte_count: int):
    gigabytes = (
        byte_count / 1024 / 1024 / 1024
    )

    return gigabytes
