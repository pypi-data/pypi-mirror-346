from bclearer_orchestration_services.identification_services.b_identity_service.b_identity_creators.b_identity_base_from_string_creator import (
    create_b_identity_base_from_string,
)
from bclearer_orchestration_services.identification_services.b_identity_service.b_identity_creators.b_identity_sum_from_b_identities_creator import (
    create_b_identity_sum_from_b_identities,
)


def create_b_identity_sum_from_strings(
    strings: list,
) -> int:
    b_identities = list()

    for string in strings:
        __add_string_to_b_identities(
            b_identities=b_identities,
            string=string,
        )

    b_identity_sum = create_b_identity_sum_from_b_identities(
        b_identities=b_identities,
    )

    return b_identity_sum


def __add_string_to_b_identities(
    b_identities: list,
    string: str,
) -> None:
    if not isinstance(string, str):
        raise TypeError

    b_identity = create_b_identity_base_from_string(
        input_string=string,
    )

    b_identities.append(b_identity)
