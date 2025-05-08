import pandas
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_folders import (
    BEngFolders,
)
from nf_common.code.services.b_eng_python_refactoring_service.reporters.levelled_uuids_getters import (
    get_levelled_uuids,
)
from nf_common.code.services.b_eng_python_refactoring_service.reporters.node_adders import (
    add_object_to_objects,
)


def add_folders_to_nodes(
    node_table: pandas.DataFrame,
):
    folders = (
        BEngFolders.registry_keyed_on_full_paths.values()
    )

    for folder in folders:
        node_table = (
            __add_folder_to_nodes(
                node_table=node_table,
                folder=folder,
            )
        )

    return node_table


def __add_folder_to_nodes(
    node_table: pandas.DataFrame,
    folder: BEngFolders,
):
    levelled_uuids = get_levelled_uuids(
        parent_folder=folder.parent_folder,
    )

    node_table = add_object_to_objects(
        objects_table=node_table,
        uuid=folder.uuid,
        base_name=folder.base_name,
        alternative_name=folder.alternative_name,
        absolute_path=folder.absolute_path_string,
        object_type="Folder",
        bitbucket_team_name=folder.bitbucket_team_name,
        bitbucket_project_name=folder.bitbucket_project_name,
        git_repository_name=folder.git_repository_name,
        folder_type=folder.b_eng_folder_type,
        absolute_level=folder.absolute_level,
        repository_root_uuid=levelled_uuids[
            0
        ],
        level_1_uuid=levelled_uuids[1],
        level_2_uuid=levelled_uuids[2],
        level_3_uuid=levelled_uuids[3],
        level_4_uuid=levelled_uuids[4],
    )

    return node_table
