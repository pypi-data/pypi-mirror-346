# from code import end_logging, initialise_logger

from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.b_app_runner_service.logging.logger_initialiser import (
    initialise_logger,
)
from bclearer_orchestration_services.b_app_runner_service.logging.logging_ender import (
    end_logging,
)
from bclearer_orchestration_services.log_environment_utility_service.common_knowledge.environment_log_level_types import (
    EnvironmentLogLevelTypes,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def run_b_app(
    app_startup_method,
    environment_log_level_type: EnvironmentLogLevelTypes,
    output_folder_prefix: str = "",
    output_folder_suffix: str = "",
    output_root_folder: Folders = None,
    **kwargs,
) -> None:
    initialise_logger(
        environment_log_level_type=environment_log_level_type,
        output_folder_prefix=output_folder_prefix,
        output_folder_suffix=output_folder_suffix,
        output_root_folder=output_root_folder,
    )

    __run_app_startup_hard_crash_catch_wrapper(
        app_startup_method=app_startup_method,
        **kwargs,
    )


def __run_app_startup_hard_crash_catch_wrapper(
    app_startup_method,
    **kwargs,
) -> None:
    try:
        app_startup_method(**kwargs)

        end_logging()

    except Exception as error:
        log_message(
            type(error).__name__
            + " occurred when running app",
        )

        if str(error):
            log_message(
                "Error message:"
                + str(error),
            )

        end_logging()

        exit(1)
