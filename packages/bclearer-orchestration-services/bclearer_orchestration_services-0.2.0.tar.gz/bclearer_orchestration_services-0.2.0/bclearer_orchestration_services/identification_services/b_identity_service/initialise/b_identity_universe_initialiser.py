from bclearer_orchestration_services.identification_services.b_identity_service.b_identity_registries import (
    BIdentityRegistries,
)
from bclearer_orchestration_services.identification_services.b_identity_service.initialise.b_identity_types_table_creator import (
    create_b_identity_types_table,
)


def initialise_b_identity_universe(
    b_identity_universe,
) -> None:
    from bclearer_orchestration_services.identification_services.b_identity_service.b_identity_universes import (
        BIdentityUniverses,
    )

    if not isinstance(
        b_identity_universe,
        BIdentityUniverses,
    ):
        raise TypeError

    b_identity_registry = (
        b_identity_universe.b_identity_registry
    )

    __create_tables(
        b_identity_registry=b_identity_registry,
    )


def __create_tables(
    b_identity_registry: BIdentityRegistries,
) -> None:
    b_identity_registry.table_dictionary[
        "b_identity_types_table"
    ] = create_b_identity_types_table()
