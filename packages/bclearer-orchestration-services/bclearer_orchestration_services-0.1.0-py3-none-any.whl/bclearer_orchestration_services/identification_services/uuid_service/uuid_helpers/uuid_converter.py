import base64

from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_uuid_from_base85_string,
    create_uuid_from_canonical_format_string,
)


def convert_base85_to_canonical_format(
    uuid_as_base85,
):
    uuid = (
        create_uuid_from_base85_string(
            uuid_as_base85,
        )
    )

    return uuid


def convert_canonical_format_to_base85(
    uuid_as_canonical_format,
):
    uuid_from_canonical_format = create_uuid_from_canonical_format_string(
        uuid_as_canonical_format,
    )

    uuid_as_base85 = base64.b85encode(
        uuid_from_canonical_format.bytes,
    )

    uuid_as_base85_string = (
        uuid_as_base85.decode()
    )

    return uuid_as_base85_string
