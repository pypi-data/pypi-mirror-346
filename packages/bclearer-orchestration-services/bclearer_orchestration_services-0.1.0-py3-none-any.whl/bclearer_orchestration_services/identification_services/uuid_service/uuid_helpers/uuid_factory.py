import base64
import uuid


def create_new_uuid_string():
    new_uuid = uuid.uuid1()

    uuid_as_base85 = base64.b85encode(
        new_uuid.bytes,
    )

    uuid_as_base85_string = (
        uuid_as_base85.decode()
    )

    return uuid_as_base85_string


def create_new_uuid() -> str:
    new_uuid = str(uuid.uuid1())

    return new_uuid


def create_uuid_from_base85_string(
    uuid_as_base85_string,
):
    uuid_as_bytes = base64.b85decode(
        uuid_as_base85_string,
    )

    uuid_from_bytes = uuid.UUID(
        bytes=uuid_as_bytes,
    )

    return uuid_from_bytes


def create_uuid_from_canonical_format_string(
    canonical_format_string,
):
    uuid_from_canonical_format = (
        uuid.UUID(
            canonical_format_string,
        )
    )

    return uuid_from_canonical_format
