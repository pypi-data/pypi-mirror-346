from typing import List

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_consumable_objects import (
    BieConsumableObjects,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_identity_spaces import (
    BieIdentitySpaces,
)


def convert_multiple_objects_to_bie_consumable_object(
    list_of_objects: list[object],
    bie_identity_space: BieIdentitySpaces = BieIdentitySpaces(),
) -> BieConsumableObjects:
    bie_consumable_object = BieConsumableObjects(
        bie_identity_space=bie_identity_space,
    )

    for input_object in list_of_objects:
        bie_consumable_object.add_to_bie_consumable_object(
            input_object=input_object,
        )

    return bie_consumable_object
