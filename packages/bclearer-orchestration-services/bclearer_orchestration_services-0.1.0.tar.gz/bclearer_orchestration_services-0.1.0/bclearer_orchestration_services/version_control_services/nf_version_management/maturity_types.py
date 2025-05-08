from enum import Enum


class MaturityTypes(Enum):
    NOT_SET = "not_set"

    RELEASE = "release"

    RELEASE_TEST = "release_test"

    RELEASE_LIVE = "release_live"

    DEVELOPMENT = "development"
