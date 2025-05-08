import os

from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from nf_common.code.services.datetime_service.time_helpers.time_getter import (
    now_time_as_string_for_files,
)
from nf_common.code.services.log_environment_utility_service.common_loggers import (
    CommonLoggers,
)
from nf_common.code.services.log_environment_utility_service.getters.set_up_logger_and_output_folder_getter import (
    get_set_up_logger_and_output_folder,
)
from nf_common.code.services.reporting_service.reporters.log_file import (
    LogFiles,
)


def get_common_logger(
    output_folder: Folders,
    logger_name: str,
) -> CommonLoggers:
    if LogFiles.first_open_time:
        LogFiles.close_log_file()

    output_folder_path = os.path.join(
        output_folder.absolute_path_string,
        "logging",
    )

    get_set_up_logger_and_output_folder(
        output_folder_name=output_folder_path,
        now_time=now_time_as_string_for_files(),
    )

    log_file_path = (
        LogFiles.log_file.name
    )

    logger = CommonLoggers(
        log_file_path=log_file_path,
        name=logger_name,
    )

    return logger
