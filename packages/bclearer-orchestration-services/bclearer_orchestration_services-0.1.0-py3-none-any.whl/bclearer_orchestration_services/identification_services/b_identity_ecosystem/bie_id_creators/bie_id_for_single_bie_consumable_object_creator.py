from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creators.bie_id_base_from_bie_encoding_creator import (
    create_bie_id_base_from_bie_encoding,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.converters.bie_consumable_object_to_bie_encoding_converter import (
    convert_bie_consumable_object_to_bie_encoding,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_identity_spaces import (
    BieIdentitySpaces,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def create_bie_id_for_single_bie_consumable_object(
    bie_consumable_object_item: str,
    bie_identity_space: BieIdentitySpaces = BieIdentitySpaces(),
) -> BieIds:
    if not isinstance(
        bie_consumable_object_item,
        str,
    ):
        raise TypeError

    bie_encoding = convert_bie_consumable_object_to_bie_encoding(
        bie_consumable_object_item=bie_consumable_object_item,
    )

    bie_id_base = create_bie_id_base_from_bie_encoding(
        bie_encoding=bie_encoding,
        digest_size=bie_identity_space.digest_size,
    )

    return bie_id_base
