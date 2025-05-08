import pandas
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_files import (
    BEngFiles,
)
from nf_common.code.services.b_eng_python_refactoring_service.reporters.levelled_uuids_getters import (
    get_levelled_uuids,
)
from nf_common.code.services.b_eng_python_refactoring_service.reporters.node_adders import (
    add_object_to_objects,
)


def add_files_to_nodes(
    objects_table: pandas.DataFrame,
):
    files = (
        BEngFiles.registry_keyed_on_full_paths.values()
    )

    for file in files:
        objects_table = __add_file_to_objects(
            object_table=objects_table,
            file=file,
        )

    return objects_table


def __add_file_to_objects(
    object_table: pandas.DataFrame,
    file: BEngFiles,
):
    levelled_uuids = get_levelled_uuids(
        parent_folder=file.parent_folder,
    )

    object_table = add_object_to_objects(
        objects_table=object_table,
        uuid=file.uuid,
        base_name=file.base_name,
        alternative_name=file.alternative_name,
        absolute_path=file.absolute_path_string,
        object_type="File",
        bitbucket_team_name=file.bitbucket_team_name,
        bitbucket_project_name=file.bitbucket_project_name,
        git_repository_name=file.git_repository_name,
        folder_type="",
        absolute_level=file.absolute_level,
        repository_root_uuid=levelled_uuids[
            0
        ],
        level_1_uuid=levelled_uuids[1],
        level_2_uuid=levelled_uuids[2],
        level_3_uuid=levelled_uuids[3],
        level_4_uuid=levelled_uuids[4],
    )

    return object_table
