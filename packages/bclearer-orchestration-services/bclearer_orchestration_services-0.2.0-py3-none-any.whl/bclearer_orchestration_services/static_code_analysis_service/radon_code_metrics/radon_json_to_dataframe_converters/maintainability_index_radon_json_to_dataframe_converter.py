import pandas
from bclearer_orchestration_services.identification_services.uuid_service.uuid_from_list_factory import (
    create_uuid_from_list,
)


def convert_maintainability_index_radon_json_to_dataframe(
    results_as_json: dict,
) -> pandas.DataFrame:
    maintainability_index_dataframe = (
        __create_empty_maintainability_index_dataframe()
    )

    if not results_as_json:
        return maintainability_index_dataframe

    for (
        full_file_path,
        result,
    ) in results_as_json.items():
        maintainability_index_dataframe = __append_result_to_dataframe(
            full_file_path=full_file_path,
            result=result,
            maintainability_index_dataframe=maintainability_index_dataframe,
        )

    ordered_maintainability_index_dataframe = maintainability_index_dataframe.sort_values(
        by=["maintainability_index"],
        ascending=True,
    )

    return ordered_maintainability_index_dataframe


def __create_empty_maintainability_index_dataframe():
    columns = [
        "file_uuid",
        "full_file_path",
        "maintainability_index",
        "rank",
    ]

    empty_maintainability_index_dataframe = pandas.DataFrame(
        columns=columns,
    )

    return empty_maintainability_index_dataframe


def __append_result_to_dataframe(
    full_file_path: str,
    result: dict,
    maintainability_index_dataframe: pandas.DataFrame,
) -> pandas.DataFrame:
    file_uuid = create_uuid_from_list(
        objects=[full_file_path],
    )

    maintainability_index_dataframe = maintainability_index_dataframe.append(
        {
            "file_uuid": file_uuid,
            "full_file_path": full_file_path,
            "maintainability_index": result[
                "mi"
            ],
            "rank": result["rank"],
        },
        ignore_index=True,
    )

    return (
        maintainability_index_dataframe
    )
