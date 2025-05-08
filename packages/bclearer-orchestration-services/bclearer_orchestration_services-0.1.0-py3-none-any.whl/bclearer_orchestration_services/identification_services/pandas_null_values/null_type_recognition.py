from enum import Enum, auto


class NullTypeRecognition(Enum):
    NOT_SET = auto()

    COARSE_GRAINED_SINGLE_VALUE = auto()

    FINE_GRAINED = auto()
