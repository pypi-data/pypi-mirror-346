from bclearer_orchestration_services.identification_services.b_identity_service.b_identity_registries import (
    BIdentityRegistries,
)
from bclearer_orchestration_services.identification_services.b_identity_service.initialise.b_identity_universe_initialiser import (
    initialise_b_identity_universe,
)


class BIdentityUniverses:
    def __init__(self):
        self.b_identity_registry = (
            BIdentityRegistries(self)
        )

        initialise_b_identity_universe(
            b_identity_universe=self,
        )

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type,
        exception_value,
        traceback,
    ):
        pass
