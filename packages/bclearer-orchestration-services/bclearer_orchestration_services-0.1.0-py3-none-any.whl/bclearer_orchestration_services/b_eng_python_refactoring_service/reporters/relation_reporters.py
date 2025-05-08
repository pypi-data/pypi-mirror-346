import pandas
from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_files import (
    BEngFiles,
)
from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_folders import (
    BEngFolders,
)


def report_relations():
    relations_table = pandas.DataFrame()

    relations_table = __add_folder_relations_to_relations(
        relations_table=relations_table,
    )

    relations_table = __add_file_relations_to_relations(
        relations_table=relations_table,
    )

    return relations_table


def __add_folder_relations_to_relations(
    relations_table: pandas.DataFrame,
):
    folders = (
        BEngFolders.registry_keyed_on_full_paths.values()
    )

    for folder in folders:
        relations_table = __add_relation_to_relations(
            relation_table=relations_table,
            source_object=folder,
            target_object=folder.parent_folder,
            relation_type="contained_in",
        )

    return relations_table


def __add_file_relations_to_relations(
    relations_table: pandas.DataFrame,
):
    files = (
        BEngFiles.registry_keyed_on_full_paths.values()
    )

    for file in files:
        relations_table = __add_relation_to_relations(
            relation_table=relations_table,
            source_object=file,
            target_object=file.parent_folder,
            relation_type="contained_in",
        )

        for use in file.uses:
            relations_table = __add_relation_to_relations(
                relation_table=relations_table,
                source_object=file,
                target_object=use,
                relation_type="uses",
            )

    return relations_table


def __add_relation_to_relations(
    relation_table: pandas.DataFrame,
    source_object: FileSystemObjects,
    target_object: FileSystemObjects,
    relation_type: str,
):
    if target_object is None:
        return relation_table

    if source_object is None:
        return relation_table

    relation_table = relation_table.append(
        {
            "source_objects": source_object.uuid,
            "target_objects": target_object.uuid,
            "relation_types": relation_type,
        },
        ignore_index=True,
    )

    return relation_table
