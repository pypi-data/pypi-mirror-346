from bclearer_core.constants.standard_constants import (
    UTF_8_ENCODING_NAME,
)
from bclearer_orchestration_services.identification_services.b_identity_service.b_identity_creators.b_identity_base_from_bytes_creator import (
    create_b_identity_base_from_bytes,
)


def create_b_identity_base_from_string(
    input_string: str,
    digest_size: int = 8,
) -> int:
    input_bytes = input_string.encode(
        UTF_8_ENCODING_NAME,
    )

    hash_as_integer = create_b_identity_base_from_bytes(
        input_bytes=input_bytes,
        digest_size=digest_size,
    )

    return hash_as_integer
