from bclearer_orchestration_services.identification_services.b_identity_service.b_identity_creators.b_identity_base_from_string_creator import (
    create_b_identity_base_from_string,
)


def create_b_identity_from_sorted_list_of_b_identities(
    b_identities: list,
) -> int:
    sorted_b_identities = sorted(
        b_identities,
        key=int,
    )

    sorted_b_identities_as_str = str(
        sorted_b_identities,
    )

    b_identity_base_from_bytes = create_b_identity_base_from_string(
        input_string=sorted_b_identities_as_str,
    )

    return b_identity_base_from_bytes
