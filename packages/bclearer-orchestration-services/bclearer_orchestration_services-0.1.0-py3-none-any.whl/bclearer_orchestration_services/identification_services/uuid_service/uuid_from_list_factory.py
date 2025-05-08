import hashlib
import uuid

from bclearer_core.constants.standard_constants import (
    UTF_8_ENCODING_NAME,
)


def create_uuid_from_list(
    objects: list,
):
    hashing_method = hashlib.md5()

    stringified_objects = str(
        objects,
    ).encode(UTF_8_ENCODING_NAME)

    hashing_method.update(
        stringified_objects,
    )

    md5_hash = str(
        hashing_method.digest(),
    )

    md5_uuid = uuid.uuid5(
        uuid.NAMESPACE_DNS,
        md5_hash,
    )

    return md5_uuid
