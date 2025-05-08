from bclearer_core.constants.standard_constants import (
    UTF_8_ENCODING_NAME,
)


def convert_bie_consumable_object_to_bie_encoding(
    bie_consumable_object_item: str,
) -> bytes:
    bie_encoding = bie_consumable_object_item.encode(
        UTF_8_ENCODING_NAME,
    )

    return bie_encoding
