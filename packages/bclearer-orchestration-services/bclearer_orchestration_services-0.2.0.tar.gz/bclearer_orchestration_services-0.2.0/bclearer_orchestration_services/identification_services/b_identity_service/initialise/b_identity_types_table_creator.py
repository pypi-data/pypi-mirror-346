from bclearer_orchestration_services.identification_services.b_identity_service.b_identity_creators.b_identity_base_from_string_creator import (
    create_b_identity_base_from_string,
)
from bclearer_orchestration_services.identification_services.b_identity_service.common_knowledge.b_identity_types import (
    BIdentityTypes,
)


def create_b_identity_types_table() -> (
    dict
):
    b_identity_types_table_as_dictionary = (
        dict()
    )

    for (
        b_identity_type
    ) in BIdentityTypes:
        __add_b_identity_type_if_required(
            b_identity_types_table_as_dictionary=b_identity_types_table_as_dictionary,
            b_identity_type=b_identity_type,
        )

    return b_identity_types_table_as_dictionary


def __add_b_identity_type_if_required(
    b_identity_types_table_as_dictionary: dict,
    b_identity_type: BIdentityTypes,
) -> None:
    if (
        b_identity_type
        == BIdentityTypes.NOT_SET
    ):
        return

    b_identity_type_name = (
        b_identity_type.b_identity_name
    )

    b_identity = create_b_identity_base_from_string(
        b_identity_type_name,
    )

    b_identity_types_table_as_dictionary[
        b_identity
    ] = {
        "b_identities": b_identity,
        "b_identity_type_names": b_identity_type_name,
        "b_identity_type_ckids": b_identity_type,
    }
