from typing import List

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def create_sum_bie_id_from_multiple_bie_ids(
    bie_ids: list[BieIds],
) -> BieIds:
    bie_id_sum_value = 0

    for bie_id in bie_ids:
        bie_id_sum_value = __add_bie_id_value_to_bie_id_sum_value(
            bie_id_sum_value=bie_id_sum_value,
            bie_id=bie_id,
        )

    bie_id = BieIds(
        int_value=bie_id_sum_value,
    )

    return bie_id


def __add_bie_id_value_to_bie_id_sum_value(
    bie_id_sum_value: int,
    bie_id: BieIds,
) -> int:
    if not isinstance(bie_id, BieIds):
        raise TypeError

    bie_id_sum_value += bie_id.int_value

    return bie_id_sum_value
