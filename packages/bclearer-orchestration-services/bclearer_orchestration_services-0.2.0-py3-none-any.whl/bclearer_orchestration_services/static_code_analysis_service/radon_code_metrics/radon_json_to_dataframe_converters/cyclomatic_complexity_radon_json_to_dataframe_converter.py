import pandas
from bclearer_orchestration_services.identification_services.uuid_service.uuid_from_list_factory import (
    create_uuid_from_list,
)


def convert_cyclomatic_complexity_radon_json_to_dataframe(
    results_as_json: dict,
) -> pandas.DataFrame:
    cyclomatic_complexity_dataframe = (
        __create_empty_cyclomatic_complexity_dataframe()
    )

    if not results_as_json:
        return cyclomatic_complexity_dataframe

    for (
        full_file_path,
        list_of_results,
    ) in results_as_json.items():
        cyclomatic_complexity_dataframe = __append_list_of_results_from_file_to_dataframe(
            full_file_path=full_file_path,
            list_of_results=list_of_results,
            cyclomatic_complexity_dataframe=cyclomatic_complexity_dataframe,
        )

    ordered_cyclomatic_complexity_dataframe = cyclomatic_complexity_dataframe.sort_values(
        by=["complexity"],
        ascending=False,
    )

    return ordered_cyclomatic_complexity_dataframe


def __append_list_of_results_from_file_to_dataframe(
    full_file_path: str,
    list_of_results: list,
    cyclomatic_complexity_dataframe: pandas.DataFrame,
):
    for result in list_of_results:
        cyclomatic_complexity_dataframe = __append_result_to_dataframe(
            full_file_path=full_file_path,
            result=result,
            cyclomatic_complexity_dataframe=cyclomatic_complexity_dataframe,
        )

    return (
        cyclomatic_complexity_dataframe
    )


def __create_empty_cyclomatic_complexity_dataframe():
    columns = [
        "file_uuid",
        "full_file_path",
        "type",
        "rank",
        "complexity",
        "name",
        "lineno",
        "col_offset",
        "endline",
    ]

    empty_cyclomatic_complexity_dataframe = pandas.DataFrame(
        columns=columns,
    )

    return empty_cyclomatic_complexity_dataframe


def __append_result_to_dataframe(
    full_file_path: str,
    result: dict,
    cyclomatic_complexity_dataframe: pandas.DataFrame,
) -> pandas.DataFrame:
    file_uuid = create_uuid_from_list(
        objects=[full_file_path],
    )

    cyclomatic_complexity_dataframe = cyclomatic_complexity_dataframe.append(
        {
            "file_uuid": file_uuid,
            "full_file_path": full_file_path,
            "type": result["type"],
            "rank": result["rank"],
            "complexity": result[
                "complexity"
            ],
            "name": result["name"],
            "lineno": result["lineno"],
            "col_offset": result[
                "col_offset"
            ],
            "endline": result[
                "endline"
            ],
        },
        ignore_index=True,
    )

    return (
        cyclomatic_complexity_dataframe
    )
