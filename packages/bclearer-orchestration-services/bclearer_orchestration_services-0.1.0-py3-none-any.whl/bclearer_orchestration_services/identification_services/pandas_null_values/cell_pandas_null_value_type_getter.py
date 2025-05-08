import numpy
from bclearer_orchestration_services.identification_services.pandas_null_values.pandas_null_value_types import (
    PandasNullValueTypes,
)
from nf_common.code.services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def get_cell_pandas_null_value_type(
    cell: object,
) -> PandasNullValueTypes:
    try:
        if isinstance(
            cell,
            numpy.ndarray,
        ) or isinstance(cell, list):
            return (
                PandasNullValueTypes.NOT_SET
            )

        null_data_policy = (
            __get_null_data_policy(
                cell=cell,
            )
        )
        return null_data_policy

    except Exception as error:
        log_message(
            message=f"ERROR occurred trying to process a data policy for cell value: {cell!s} - {error!s}",
        )
        return (
            PandasNullValueTypes.NOT_SET
        )


def __get_null_data_policy(
    cell,
) -> PandasNullValueTypes:
    for (
        null_data_policy
    ) in PandasNullValueTypes:
        if (
            null_data_policy
            is PandasNullValueTypes.NOT_SET
            or not isinstance(
                null_data_policy,
                PandasNullValueTypes,
            )
        ):
            continue
        null_data_policy_value_type = (
            type(null_data_policy.value)
        )
        # TODO: Need to check we can capture all the null data policies
        if isinstance(
            cell,
            null_data_policy_value_type,
        ):
            match null_data_policy_value_type.__name__:
                case "str":
                    if (
                        cell.casefold()
                        == null_data_policy.value
                    ):
                        return null_data_policy

                case "NoneType":
                    return (
                        null_data_policy
                    )

                case "float":
                    if numpy.isnan(
                        cell,
                    ) and numpy.isnan(
                        null_data_policy.value,
                    ):
                        return null_data_policy

                case "datetime64":
                    if numpy.isnat(
                        cell,
                    ):
                        return null_data_policy

    return PandasNullValueTypes.NOT_SET
