def create_b_identity_sum_from_b_identities(
    b_identities: list,
) -> int:
    b_identity_sum = 0

    for b_identity in b_identities:
        b_identity_sum = __add_b_identity_to_b_identity_sum(
            b_identity_sum=b_identity_sum,
            b_identity=b_identity,
        )

    return b_identity_sum


def __add_b_identity_to_b_identity_sum(
    b_identity_sum: int,
    b_identity: int,
) -> int:
    if not isinstance(b_identity, int):
        raise TypeError

    b_identity_sum += b_identity

    return b_identity_sum
