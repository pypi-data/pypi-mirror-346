from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.b_app_runner_service.logging.output_folder_and_logger_set_upper import (
    set_up_output_folder_and_logger,
)
from bclearer_orchestration_services.log_environment_utility_service.common_knowledge.environment_log_level_types import (
    EnvironmentLogLevelTypes,
)
from bclearer_orchestration_services.log_environment_utility_service.loggers.environment_logger import (
    log_filtered_environment,
    log_full_environment,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    log_timing_header,
)


def initialise_logger(
    environment_log_level_type: EnvironmentLogLevelTypes,
    output_folder_prefix: str,
    output_folder_suffix: str,
    output_root_folder: Folders,
) -> None:
    __set_up_logger(
        output_folder_prefix=output_folder_prefix,
        output_folder_suffix=output_folder_suffix,
        output_root_folder=output_root_folder,
    )

    __log_initial_logs(
        environment_log_level_type=environment_log_level_type,
    )


def __set_up_logger(
    output_folder_prefix: str,
    output_folder_suffix: str,
    output_root_folder: Folders,
) -> None:
    set_up_output_folder_and_logger(
        output_root_folder=output_root_folder,
        output_folder_prefix=output_folder_prefix,
        output_folder_suffix=output_folder_suffix,
    )


def __log_initial_logs(
    environment_log_level_type: EnvironmentLogLevelTypes,
) -> None:
    log_timing_header()

    match environment_log_level_type:
        case (
            EnvironmentLogLevelTypes.FILTERED
        ):
            log_filtered_environment()

        case (
            EnvironmentLogLevelTypes.FULL
        ):
            log_full_environment()

        case (
            EnvironmentLogLevelTypes.NONE
        ):
            pass

        case _:
            raise NotImplementedError
