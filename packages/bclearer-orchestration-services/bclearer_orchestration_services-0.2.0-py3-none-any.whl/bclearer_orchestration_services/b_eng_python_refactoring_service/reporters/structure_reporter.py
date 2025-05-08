from bclearer_interop_services.hdf5_service.dataframe_dictionary_to_hdf5_file_writer import (
    write_dataframe_dictionary_to_hdf5_file,
)
from nf_common.code.services.b_eng_python_refactoring_service.b_eng_structure_and_contents.b_eng_structure_and_content_collectors import (
    collect_structure_and_content,
)
from nf_common.code.services.b_eng_python_refactoring_service.reporters.object_reporters import (
    report_objects,
)
from nf_common.code.services.b_eng_python_refactoring_service.reporters.relation_reporters import (
    report_relations,
)


def report_structure(
    workspace_paths: list,
    hdf5_file_name: str,
):
    collect_structure_and_content(
        workspace_paths=workspace_paths,
    )

    objects_table = report_objects()

    relations_table = report_relations()

    dataframes_dictionary = {
        "objects_table": objects_table,
        "relations_table": relations_table,
    }

    write_dataframe_dictionary_to_hdf5_file(
        hdf5_file_name=hdf5_file_name,
        dataframes_dictionary=dataframes_dictionary,
    )
