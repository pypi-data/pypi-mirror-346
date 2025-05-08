import logging
import sys
from logging import Logger
from logging.handlers import (
    TimedRotatingFileHandler,
)

import pandas
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from nf_common.code.services.log_environment_utility_service.loggers.environment_logger import (
    log_filtered_environment,
)
from nf_common.code.services.reporting_service.reporters.log_file import (
    LogFiles,
)
from nf_common.code.services.reporting_service.wrappers.run_and_log_function_wrapper import (
    log_timing_header,
)

LOG_FORMAT = "%(asctime)s: %(name)s - %(levelname)s - %(threadName)s - %(message)s"


class CommonLoggers(Logger):
    def __init__(
        self,
        log_file_path=None,
        log_format=LOG_FORMAT,
        *args,
        **kwargs,
    ):
        Logger.__init__(
            self,
            level=logging.DEBUG,
            *args,
            **kwargs,
        )

        self.formatter = (
            logging.Formatter(
                log_format,
                "%Y-%m-%d %H:%M:%S",
            )
        )

        self.log_file_path = (
            log_file_path
        )

        self.addHandler(
            self.get_console_handler(),
        )

        if log_file_path:
            self.addHandler(
                self.get_file_handler(),
            )

        self.propagate = True

        log_timing_header()

        log_filtered_environment()

        # note: the log file has to be closed because it just save the logs when it is closed.
        LogFiles.log_file.close()

    def get_console_handler(
        self,
    ) -> logging.StreamHandler:
        console_handler = (
            logging.StreamHandler(
                sys.stdout,
            )
        )

        console_handler.setFormatter(
            self.formatter,
        )

        return console_handler

    def get_file_handler(
        self,
    ) -> TimedRotatingFileHandler:
        file_handler = (
            TimedRotatingFileHandler(
                self.log_file_path,
                when="midnight",
            )
        )

        file_handler.setFormatter(
            self.formatter,
        )

        return file_handler

    def read_log_file_content(self):
        file_handler_path = (
            self.get_file_handler().baseFilename
        )

        file_handler = Files(
            absolute_path_string=file_handler_path,
        )

        with open(
            file_handler.absolute_path_string,
        ) as text_io_wrapper_file:
            log_lines = (
                text_io_wrapper_file.readlines()
            )

            text_io_wrapper_file.close()

        return log_lines

    def get_error_messages_by_log_type(
        self,
        log_type: str,
    ) -> pandas.DataFrame:
        log_lines = (
            self.read_log_file_content()
        )

        log_datatable = (
            pandas.DataFrame(
                log_lines,
                columns=["log_message"],
            )
        )

        log_datatable_by_error_type = log_datatable[
            log_datatable.log_message.str.contains(
                log_type.upper(),
            )
        ]

        return (
            log_datatable_by_error_type
        )
