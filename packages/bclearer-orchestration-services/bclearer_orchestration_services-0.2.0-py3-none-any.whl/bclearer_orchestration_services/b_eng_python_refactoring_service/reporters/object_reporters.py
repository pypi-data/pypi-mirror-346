import pandas
from nf_common.code.services.b_eng_python_refactoring_service.reporters.file_objects_reporters import (
    add_files_to_nodes,
)
from nf_common.code.services.b_eng_python_refactoring_service.reporters.folder_node_reporters import (
    add_folders_to_nodes,
)


def report_objects():
    objects_table = pandas.DataFrame()

    objects_table = (
        add_folders_to_nodes(
            node_table=objects_table,
        )
    )

    objects_table = add_files_to_nodes(
        objects_table=objects_table,
    )

    return objects_table
