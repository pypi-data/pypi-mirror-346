from bclearer_orchestration_services.identification_services.b_identity_service.b_identity_creators.b_identity_base_from_string_creator import (
    create_b_identity_base_from_string,
)
from bclearer_orchestration_services.identification_services.b_identity_service.b_identity_creators.b_identity_from_sorted_list_of_b_identities_creator import (
    create_b_identity_from_sorted_list_of_b_identities,
)
from bclearer_orchestration_services.identification_services.b_identity_service.b_identity_creators.b_identity_sum_from_b_identities_creator import (
    create_b_identity_sum_from_b_identities,
)


def create_b_identity_using_role_based_ids(
    role_based_type_instance: object,
    b_identity_components: tuple,
) -> int:
    b_identity_role_components = list()

    for (
        b_identity_component
    ) in b_identity_components:
        __add_component_to_components(
            role_based_type_instance=role_based_type_instance,
            b_identity_component=b_identity_component,
            b_identity_role_components=b_identity_role_components,
        )

    b_identity = create_b_identity_from_sorted_list_of_b_identities(
        b_identities=b_identity_role_components,
    )

    return b_identity


def __add_component_to_components(
    role_based_type_instance,
    b_identity_component,
    b_identity_role_components: list,
):
    role_type = b_identity_component[0]

    role_value = b_identity_component[1]

    if not isinstance(
        role_type,
        role_based_type_instance,
    ):
        raise TypeError

    if not role_value:
        role_value = 0

    if not isinstance(role_value, int):
        raise TypeError

    role_type_b_identity = create_b_identity_base_from_string(
        input_string=role_type.name,
    )

    role_based_b_identity = create_b_identity_sum_from_b_identities(
        b_identities=[
            role_type_b_identity,
            role_value,
        ],
    )

    b_identity_role_components.append(
        role_based_b_identity,
    )
