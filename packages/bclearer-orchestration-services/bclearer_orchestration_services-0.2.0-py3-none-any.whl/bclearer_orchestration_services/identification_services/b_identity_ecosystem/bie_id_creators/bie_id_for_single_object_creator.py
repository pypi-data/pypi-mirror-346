from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creators.bie_id_from_bie_consumable_object_creator import (
    create_bie_id_from_bie_consumable_object,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_consumable_objects import (
    BieConsumableObjects,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_identity_spaces import (
    BieIdentitySpaces,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def create_bie_id_for_single_object(
    input_object: object,
    bie_identity_space: BieIdentitySpaces = BieIdentitySpaces(),
) -> BieIds:
    bie_consumable_object = BieConsumableObjects(
        bie_identity_space=bie_identity_space,
    )

    bie_consumable_object.add_to_bie_consumable_object(
        input_object=input_object,
    )

    bie_id = create_bie_id_from_bie_consumable_object(
        bie_consumable_object=bie_consumable_object,
    )

    return bie_id
