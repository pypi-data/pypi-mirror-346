from enum import Enum, auto


class BIdentityTypes(Enum):
    NOT_SET = auto()

    DATA_ITEM_IDENTITIES = auto()

    DATA_ITEM_IMMUTABLE_STAGE_IDENTITIES = (
        auto()
    )

    DATA_ITEM_B_UNIT_STAGE_IDENTITIES = (
        auto()
    )

    DATASET_IDENTITIES = auto()

    DATASET_IMMUTABLE_STAGE_IDENTITIES = (
        auto()
    )

    DATASET_B_UNIT_STAGE_IDENTITIES = (
        auto()
    )

    B_UNIT_STAGE_IDENTITIES = auto()

    B_CLEARER_RUN_IDENTITIES = auto()

    DATA_IDENTITIES = auto()

    DATA_IMMUTABLE_STAGE_IDENTITIES = (
        auto()
    )

    DATA_B_UNIT_STAGE_IDENTITIES = (
        auto()
    )

    def __b_identity_type_name(
        self,
    ) -> str:
        app_type_name = (
            app_type_to_name_mapping[
                self
            ]
        )

        return app_type_name

    b_identity_name = property(
        fget=__b_identity_type_name,
    )


app_type_to_name_mapping = {
    BIdentityTypes.NOT_SET: "",
    BIdentityTypes.DATA_ITEM_IDENTITIES: "data_item_identities",
    BIdentityTypes.DATA_ITEM_IMMUTABLE_STAGE_IDENTITIES: "data_item_immutable_stage_identities",
    BIdentityTypes.DATA_ITEM_B_UNIT_STAGE_IDENTITIES: "data_item_b_unit_stage_identities",
    BIdentityTypes.DATASET_IDENTITIES: "dataset_identities",
    BIdentityTypes.DATASET_IMMUTABLE_STAGE_IDENTITIES: "dataset_immutable_stage_identities",
    BIdentityTypes.DATASET_B_UNIT_STAGE_IDENTITIES: "dataset_b_unit_stage_identities",
    BIdentityTypes.B_UNIT_STAGE_IDENTITIES: "b_unit_stage_identities",
    BIdentityTypes.B_CLEARER_RUN_IDENTITIES: "b_clearer_run_identities",
    BIdentityTypes.DATA_IDENTITIES: "data_identities",
    BIdentityTypes.DATA_IMMUTABLE_STAGE_IDENTITIES: "data_immutable_stage_identities",
    BIdentityTypes.DATA_B_UNIT_STAGE_IDENTITIES: "data_b_unit_stage_identities",
}
