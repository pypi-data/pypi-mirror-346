from os import path

from bclearer_orchestration_services.datetime_service.time_helpers.time_getter import (
    now_time_as_string_for_files,
)


class LogFiles:
    log_file = None

    folder_path = None

    first_open_time = None

    @staticmethod
    def open_log_file(
        folder_path=None,
        now_time=now_time_as_string_for_files(),
    ):
        LogFiles.folder_path = (
            folder_path
        )

        LogFiles.first_open_time = (
            now_time
        )

        file_name = (
            "log_file"
            + LogFiles.first_open_time
            + ".txt"
        )

        file_path = path.join(
            folder_path,
            file_name,
        )

        LogFiles.log_file = open(
            file_path,
            "w+",
        )

    @staticmethod
    def close_log_file():
        LogFiles.log_file.close()

    @staticmethod
    def write_to_log_file(
        message: str,
        folder_path=None,
        now_time=now_time_as_string_for_files(),
    ):
        if LogFiles.log_file is None:
            LogFiles.open_log_file(
                folder_path,
                now_time,
            )

        LogFiles.log_file.write(message)
