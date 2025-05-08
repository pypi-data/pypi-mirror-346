import hashlib

from bclearer_core.constants.standard_constants import (
    UTF_8_ENCODING_NAME,
)


def create_tiny_hash_string(
    inputs: list,
) -> str:
    hash_string = __create_hash_string(
        inputs=inputs,
        digest_size=3,
    )

    return hash_string


def create_hash_with_sorted_inputs(
    inputs: list,
) -> str:
    sorted_inputs = sorted(
        inputs,
        key=str,
    )

    hash_string = create_hash(
        inputs=sorted_inputs,
    )

    return hash_string


def create_hash(inputs: list) -> str:
    hash_string = __create_hash_string(
        inputs=inputs,
        digest_size=8,
    )

    return hash_string


def create_identity_hash_string(
    inputs: list,
) -> str:
    hash_string = create_hash(
        inputs=inputs,
    )

    return hash_string


def __create_hash_string(
    inputs: list,
    digest_size: int,
) -> str:
    hash_blake2b = hashlib.blake2b(
        str(inputs).encode(
            UTF_8_ENCODING_NAME,
        ),
        digest_size=digest_size,
    )

    hash_string = (
        hash_blake2b.hexdigest()
    )

    return hash_string
