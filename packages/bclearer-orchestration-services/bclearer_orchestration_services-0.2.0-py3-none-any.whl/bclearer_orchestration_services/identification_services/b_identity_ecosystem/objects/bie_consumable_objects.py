from bclearer_orchestration_services.identification_services.b_identity_ecosystem.converters.object_to_bie_consumable_object_item_converter import (
    convert_object_to_bie_consumable_object_item,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_identity_spaces import (
    BieIdentitySpaces,
)


class BieConsumableObjects:
    def __init__(
        self,
        bie_identity_space: BieIdentitySpaces,
    ):
        self.bie_consumable_object_list = (
            list()
        )

        self.bie_identity_space = (
            bie_identity_space
        )

    def add_to_bie_consumable_object(
        self,
        input_object: object,
    ) -> None:
        bie_consumable_object_item = convert_object_to_bie_consumable_object_item(
            input_object=input_object,
            bie_identity_space=self.bie_identity_space,
        )

        self.bie_consumable_object_list.append(
            bie_consumable_object_item,
        )
