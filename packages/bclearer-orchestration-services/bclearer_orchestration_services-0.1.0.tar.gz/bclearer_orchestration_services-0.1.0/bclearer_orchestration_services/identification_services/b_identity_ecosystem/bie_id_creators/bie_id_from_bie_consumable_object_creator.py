from typing import List

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creators.bie_id_for_single_bie_consumable_object_creator import (
    create_bie_id_for_single_bie_consumable_object,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creators.sum_bie_id_from_multiple_bie_ids_creator import (
    create_sum_bie_id_from_multiple_bie_ids,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_consumable_objects import (
    BieConsumableObjects,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def create_bie_id_from_bie_consumable_object(
    bie_consumable_object: BieConsumableObjects,
) -> BieIds:
    bie_ids = list()

    for (
        bie_consumable_object_item
    ) in (
        bie_consumable_object.bie_consumable_object_list
    ):
        __add_bie_consumable_object_to_bie_ids(
            bie_ids=bie_ids,
            bie_consumable_object_item=bie_consumable_object_item,
        )

    bie_id_sum = create_sum_bie_id_from_multiple_bie_ids(
        bie_ids=bie_ids,
    )

    return bie_id_sum


def __add_bie_consumable_object_to_bie_ids(
    bie_ids: list[BieIds],
    bie_consumable_object_item: str,
) -> None:
    bie_id = create_bie_id_for_single_bie_consumable_object(
        bie_consumable_object_item=bie_consumable_object_item,
    )

    bie_ids.append(bie_id)
