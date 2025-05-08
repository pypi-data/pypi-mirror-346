def split_string_by_separators(
    string_content: str,
    separators: list,
) -> list:
    split_stage_string_tuples = list()

    strings_to_split = [string_content]

    for separator_position in range(
        len(separators),
    ):
        split_list = __split_list_of_strings_by_separator(
            split_stage_string_tuples=split_stage_string_tuples,
            separators=separators,
            current_separator_position=separator_position,
            strings_to_split=strings_to_split,
        )

        strings_to_split = split_list

    separated_list = [
        split_stage_string_tuple[1]
        for split_stage_string_tuple in split_stage_string_tuples
        if split_stage_string_tuple[0]
        == len(separators) - 1
    ]

    return separated_list


def __split_list_of_strings_by_separator(
    split_stage_string_tuples: list,
    separators: list,
    current_separator_position: int,
    strings_to_split: list,
) -> list:
    complete_split_list = list()

    for (
        string_to_split
    ) in strings_to_split:
        split_list = __split_string_by_separator(
            split_stage_string_tuples=split_stage_string_tuples,
            separators=separators,
            current_separator_position=current_separator_position,
            string_to_split=string_to_split,
        )

        complete_split_list += (
            split_list
        )

    return complete_split_list


def __split_string_by_separator(
    split_stage_string_tuples: list,
    separators: list,
    current_separator_position: int,
    string_to_split: str,
) -> list:
    split_list = string_to_split.split(
        separators[
            current_separator_position
        ],
    )

    for split_string in split_list:
        split_stage_string_tuples.append(
            (
                current_separator_position,
                split_string,
            ),
        )

    return split_list
