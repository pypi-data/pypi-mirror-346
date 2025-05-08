from typing import List

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creators.bie_id_from_bie_consumable_object_creator import (
    create_bie_id_from_bie_consumable_object,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.converters.multiple_objects_to_bie_consumable_object_converter import (
    convert_multiple_objects_to_bie_consumable_object,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_identity_spaces import (
    BieIdentitySpaces,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def create_bie_id_for_multiple_objects(
    input_objects: list[object],
    bie_identity_space: BieIdentitySpaces = BieIdentitySpaces(),
) -> BieIds:
    bie_consumable_object = convert_multiple_objects_to_bie_consumable_object(
        list_of_objects=input_objects,
        bie_identity_space=bie_identity_space,
    )

    bie_id = create_bie_id_from_bie_consumable_object(
        bie_consumable_object=bie_consumable_object,
    )

    return bie_id
