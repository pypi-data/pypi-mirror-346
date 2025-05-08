import time
from time import gmtime, strftime


def now_time_as_string() -> str:
    now_as_datetime_string = strftime(
        "%Y-%m-%d %H:%M:%S",
        gmtime(),
    )

    return now_as_datetime_string


def now_time_as_string_for_files() -> (
    str
):
    return strftime(
        "%Y_%m_%d_%H_%M_%S",
        gmtime(),
    )


def time_as_string_yyyymmddhhmm(
    structured_time: time.struct_time,
) -> str:
    formatted_string = strftime(
        "%Y%m%d%H%M",
        structured_time,
    )

    return formatted_string


def now_time_as_string_yyyymmddhhmm() -> (
    str
):
    time_now = gmtime()

    formatted_string = (
        time_as_string_yyyymmddhhmm(
            structured_time=time_now,
        )
    )

    return formatted_string


def __get_formatted_string_from_structured_time(
    format: str,
    structured_time: time.struct_time,
) -> str:
    formatted_string = strftime(
        format,
        structured_time,
    )

    return formatted_string
