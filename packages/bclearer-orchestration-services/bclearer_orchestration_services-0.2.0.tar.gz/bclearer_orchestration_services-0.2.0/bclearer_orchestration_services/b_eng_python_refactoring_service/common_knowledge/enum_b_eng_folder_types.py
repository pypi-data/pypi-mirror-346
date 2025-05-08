from enum import Enum, auto, unique


@unique
class EnumBEngFolderTypes(Enum):
    NOT_SET = auto()

    WORKSPACE = auto()

    BITBUCKET_TEAM = auto()

    BITBUCKET_PROJECT = auto()

    GIT_REPOSITORIES = auto()

    CODE_REPOSITORY = auto()

    ORIGINAL_DATA_REPOSITORY = auto()

    CREATED_DATA_REPOSITORY = auto()

    DATABASE_OUTPUTS_REPOSITORY = auto()

    REPOSITORY_ROOT_FOLDER = auto()

    CODE_FOLDER = auto()

    DATA_FOLDER = auto()

    SANDPIT_FOLDER = auto()

    EXECUTABLES_FOLDER = auto()

    DATABASE_OUTPUTS_FOLDER = auto()
