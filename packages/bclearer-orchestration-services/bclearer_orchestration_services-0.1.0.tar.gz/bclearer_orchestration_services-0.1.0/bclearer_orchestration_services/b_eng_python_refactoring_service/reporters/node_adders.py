import pandas


def add_object_to_objects(
    objects_table: pandas.DataFrame,
    uuid: str,
    base_name: str,
    alternative_name: str,
    absolute_path: str,
    object_type: str,
    bitbucket_team_name: str,
    bitbucket_project_name: str,
    git_repository_name: str,
    folder_type: str,
    absolute_level: int,
    repository_root_uuid: str,
    level_1_uuid: str,
    level_2_uuid: str,
    level_3_uuid: str,
    level_4_uuid: str,
):
    objects_table = objects_table.append(
        {
            "uuids": uuid,
            "base_names": base_name,
            "alternative_names": alternative_name,
            "absolute_paths": absolute_path,
            "object_types": object_type,
            "bitbucket_team_names": bitbucket_team_name,
            "bitbucket_project_names": bitbucket_project_name,
            "git_repository_names": git_repository_name,
            "folder_types": folder_type,
            "absolute_level": str(
                absolute_level,
            ),
            "repository_root_uuids": repository_root_uuid,
            "level_1_uuids": level_1_uuid,
            "level_2_uuids": level_2_uuid,
            "level_3_uuids": level_3_uuid,
            "level_4_uuids": level_4_uuid,
        },
        ignore_index=True,
    )

    return objects_table
