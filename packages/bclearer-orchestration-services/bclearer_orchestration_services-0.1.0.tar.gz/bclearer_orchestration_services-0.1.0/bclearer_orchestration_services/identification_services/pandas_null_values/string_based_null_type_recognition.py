from enum import Enum, auto


class StringBasedNullTypeRecognition(
    Enum,
):
    NOT_SET = auto()

    RECOGNISE_STRING_BASED_NULL_AS_NULL = (
        auto()
    )

    DO_NOT_RECOGNISE_STRING_BASED_NULL_AS_NULL = (
        auto()
    )
