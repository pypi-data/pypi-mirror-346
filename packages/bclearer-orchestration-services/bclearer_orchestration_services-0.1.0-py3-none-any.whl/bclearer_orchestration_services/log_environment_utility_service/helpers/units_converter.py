def convert_units(
    byte_count,
    suffix="B",
):
    factor = 1024

    for unit in [
        "",
        "K",
        "M",
        "G",
        "T",
        "P",
    ]:
        if byte_count < factor:
            return f"{byte_count:.2f}{unit}{suffix}"

        byte_count /= factor
