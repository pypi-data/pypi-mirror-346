import pandas
from bclearer_orchestration_services.identification_services.uuid_service.uuid_from_list_factory import (
    create_uuid_from_list,
)


def convert_raw_radon_json_to_dataframe(
    results_as_json: dict,
) -> pandas.DataFrame:
    raw_dataframe = (
        __create_empty_raw_dataframe()
    )

    if not results_as_json:
        return raw_dataframe

    for (
        full_file_path,
        result,
    ) in results_as_json.items():
        raw_dataframe = __append_result_to_dataframe(
            full_file_path=full_file_path,
            result=result,
            raw_dataframe=raw_dataframe,
        )

    ordered_raw_dataframe = raw_dataframe.sort_values(
        by=[
            "total_lines_of_code_count",
        ],
        ascending=False,
    )

    return ordered_raw_dataframe


def __create_empty_raw_dataframe():
    columns = [
        "file_uuid",
        "full_file_path",
        "total_lines_of_code_count",
        "logical_lines_of_code_count",
        "source_lines_of_code_count",
        "lines_of_comments_count",
        "lines_of_multi_line_strings_count",
        "blank_lines_count",
        "single_lines_of_comments_count",
    ]

    empty_raw_dataframe = (
        pandas.DataFrame(
            columns=columns,
        )
    )

    return empty_raw_dataframe


def __append_result_to_dataframe(
    full_file_path: str,
    result: dict,
    raw_dataframe: pandas.DataFrame,
) -> pandas.DataFrame:
    file_uuid = create_uuid_from_list(
        objects=[full_file_path],
    )

    raw_dataframe = raw_dataframe.append(
        {
            "file_uuid": file_uuid,
            "full_file_path": full_file_path,
            "total_lines_of_code_count": result[
                "loc"
            ],
            "logical_lines_of_code_count": result[
                "lloc"
            ],
            "source_lines_of_code_count": result[
                "sloc"
            ],
            "lines_of_comments_count": result[
                "comments"
            ],
            "lines_of_multi_line_strings_count": result[
                "multi"
            ],
            "blank_lines_count": result[
                "blank"
            ],
            "single_lines_of_comments_count": result[
                "single_comments"
            ],
        },
        ignore_index=True,
    )

    return raw_dataframe
