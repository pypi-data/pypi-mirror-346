from enum import Enum, auto, unique


@unique
class EnumMoveAndReplaceResultTypes(
    Enum,
):
    SUCCESS = auto()

    FAILURE = auto()
