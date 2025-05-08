RFC_4648_SYMBOL_SET_BASE32_CHARS = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
)

RFC_4648_SYMBOL_SET_BASE32_ALPHABET = list(
    RFC_4648_SYMBOL_SET_BASE32_CHARS,
)


def convert_int_to_base32(
    int_value: int,
) -> str:
    binary = bin(int_value)[2:]

    binary = binary.zfill(
        (len(binary) + 4) // 5 * 5,
    )

    return "".join(
        RFC_4648_SYMBOL_SET_BASE32_ALPHABET[
            int(binary[i : i + 5], 2)
        ]
        for i in range(
            0,
            len(binary),
            5,
        )
    )
