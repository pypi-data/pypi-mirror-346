def get_hash_sum_from_hash_string_list(
    hash_string_list: list,
) -> int:
    hash_sum = 0

    for hash_string in hash_string_list:
        hash_sum = __add_hash_string_to_hash_sum(
            hash_string=hash_string,
            hash_sum=hash_sum,
        )

    return hash_sum


def __add_hash_string_to_hash_sum(
    hash_string: str,
    hash_sum: int,
) -> int:
    hash_integer = int(
        hash_string,
        base=16,
    )

    hash_sum += hash_integer

    return hash_sum
