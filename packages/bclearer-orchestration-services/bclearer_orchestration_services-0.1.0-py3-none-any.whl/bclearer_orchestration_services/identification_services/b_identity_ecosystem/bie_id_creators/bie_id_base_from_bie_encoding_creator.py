import hashlib

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def create_bie_id_base_from_bie_encoding(
    bie_encoding: bytes,
    digest_size: int = 8,
) -> BieIds:
    hash_blake2b = hashlib.blake2b(
        bie_encoding,
        digest_size=digest_size,
    )

    hash_as_hex_string = (
        hash_blake2b.hexdigest()
    )

    hash_as_integer = int(
        hash_as_hex_string,
        16,
    )

    bie_id = BieIds(
        int_value=hash_as_integer,
    )

    return bie_id
