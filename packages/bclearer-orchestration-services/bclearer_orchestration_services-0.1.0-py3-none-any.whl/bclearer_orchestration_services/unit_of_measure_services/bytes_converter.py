import math

from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)

magnitude_order_to_suffix_conversion_map = {
    0: "B",
    1: "KB",
    2: "MB",
    3: "GB",
    4: "TB",
    5: "PB",
}

round_digit_number = 3


def convert_bytes_to_byte_units(
    bytes: int,
) -> str:
    if bytes < 0:
        return DEFAULT_NULL_VALUE

    if bytes == 0:
        return "0 B"

    bytes_exponent_value = math.log2(
        bytes,
    )

    bytes_unit_value = __get_byte_unit_value(
        bytes=bytes,
        bytes_exponent_value=bytes_exponent_value,
    )

    byte_unit_suffix = __get_byte_unit_suffix(
        bytes_exponent_value=bytes_exponent_value,
    )

    byte_units = (
        bytes_unit_value
        + " "
        + byte_unit_suffix
    )

    return byte_units


def __get_byte_unit_suffix(
    bytes_exponent_value: float,
) -> str:
    bytes_magnitude_order = int(
        bytes_exponent_value // 10,
    )

    if (
        bytes_magnitude_order
        not in magnitude_order_to_suffix_conversion_map
    ):
        return "OUT OF RANGE"

    byte_unit_suffix = magnitude_order_to_suffix_conversion_map[
        bytes_magnitude_order
    ]

    return byte_unit_suffix


def __get_byte_unit_value(
    bytes: int,
    bytes_exponent_value: float,
) -> str:
    bytes_magnitude_order = int(
        bytes_exponent_value // 10,
    )

    bytes_multiple_value = bytes / (
        2
        ** (10 * bytes_magnitude_order)
    )

    rounded_bytes_multiple_value = (
        round(
            bytes_multiple_value,
            round_digit_number,
        )
    )

    byte_unit_value = str(
        rounded_bytes_multiple_value,
    )

    return byte_unit_value
