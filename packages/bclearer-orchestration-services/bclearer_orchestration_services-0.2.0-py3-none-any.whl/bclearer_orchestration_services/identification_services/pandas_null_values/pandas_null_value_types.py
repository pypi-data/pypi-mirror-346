from enum import Enum, auto

import numpy


class PandasNullValueTypes(Enum):
    NOT_SET = auto()

    EMPTY_STRING = auto()

    EMPTY_CELL = auto()

    NONE_CELL_AS_STRING_VALUE = auto()

    # NOTE - we think these are superfluous - this needs checking
    # LOWER_NUMPY_NAN_CELL = \
    #     auto()

    NUMPY_NAN_CELL = auto()

    NAN_AS_STRING_VALUE = auto()

    NULL_AS_STRING_VALUE = auto()

    NUMPY_DATETIME_64_EMPTY_CELL = (
        auto()
    )

    NUMPY_DATETIME_64_AS_STRING_VALUE = (
        auto()
    )

    def __data_policy_value(
        self,
    ) -> str:
        data_policy_value = data_policy_name_to_value_mapping[
            self
        ]

        return data_policy_value

    value = property(
        fget=__data_policy_value,
    )


data_policy_name_to_value_mapping = {
    PandasNullValueTypes.EMPTY_STRING: "",
    PandasNullValueTypes.EMPTY_CELL: None,
    # NullDataPoliciesValues.LOWER_NUMPY_NAN_CELL: numpy.nan,
    PandasNullValueTypes.NUMPY_NAN_CELL: numpy.nan,
    PandasNullValueTypes.NUMPY_DATETIME_64_EMPTY_CELL: numpy.datetime64(),
    PandasNullValueTypes.NUMPY_DATETIME_64_AS_STRING_VALUE: "nat",
    PandasNullValueTypes.NONE_CELL_AS_STRING_VALUE: "none",
    PandasNullValueTypes.NAN_AS_STRING_VALUE: "nan",
    PandasNullValueTypes.NULL_AS_STRING_VALUE: "null",
}
