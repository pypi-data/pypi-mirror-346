import hashlib


def create_b_identity_base_from_bytes(
    input_bytes: bytes,
    digest_size: int = 8,
) -> int:
    hash_blake2b = hashlib.blake2b(
        input_bytes,
        digest_size=digest_size,
    )

    hash_as_hex_string = (
        hash_blake2b.hexdigest()
    )

    hash_as_integer = int(
        hash_as_hex_string,
        16,
    )

    return hash_as_integer
