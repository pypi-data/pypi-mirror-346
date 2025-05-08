from nf_common.code.services.version_control_services.nf_version_management.constants import (
    FILE_NAME_COMPONENTS_SEPARATOR,
)
from nf_common.code.services.version_control_services.nf_version_management.data_types import (
    DataTypes,
)
from nf_common.code.services.version_control_services.nf_version_management.maturity_types import (
    MaturityTypes,
)


def get_repository_name_adapted_to_data_type_and_maturity_type(
    repo_name: str,
    data_type: DataTypes,
    maturity_type: MaturityTypes,
    code_identifier: str,
    sources_set_joint_identifier: str,
    source_identifiers_map: dict,
) -> str:
    repository_name_adapted_to_data_type_and_maturity_type = (
        repo_name
    )

    if (
        data_type
        == DataTypes.SOURCE_DATA
    ):
        if (
            maturity_type
            == MaturityTypes.DEVELOPMENT
            or maturity_type
            == MaturityTypes.NOT_SET
        ):
            repository_name_adapted_to_data_type_and_maturity_type = (
                repo_name
            )
        else:
            source_identifier = (
                source_identifiers_map[
                    repo_name
                ]
            )

            repository_name_adapted_to_data_type_and_maturity_type = (
                maturity_type.value
                + FILE_NAME_COMPONENTS_SEPARATOR
                + source_identifier
                + FILE_NAME_COMPONENTS_SEPARATOR
                + repo_name
            )

    if (
        data_type
        == DataTypes.INTERNAL_DATA
    ):
        if (
            maturity_type
            == MaturityTypes.RELEASE_TEST
        ):
            repository_name_adapted_to_data_type_and_maturity_type = (
                maturity_type.value
                + FILE_NAME_COMPONENTS_SEPARATOR
                + code_identifier
                + FILE_NAME_COMPONENTS_SEPARATOR
                + repo_name
            )

        if (
            maturity_type
            == MaturityTypes.RELEASE_LIVE
        ):
            repository_name_adapted_to_data_type_and_maturity_type = (
                maturity_type.value
                + FILE_NAME_COMPONENTS_SEPARATOR
                + code_identifier
                + FILE_NAME_COMPONENTS_SEPARATOR
                + sources_set_joint_identifier
                + FILE_NAME_COMPONENTS_SEPARATOR
                + repo_name
            )

        if (
            maturity_type
            == MaturityTypes.DEVELOPMENT
        ):
            repository_name_adapted_to_data_type_and_maturity_type = (
                repo_name
            )

    return repository_name_adapted_to_data_type_and_maturity_type
