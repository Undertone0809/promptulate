import datetime
import logging
import sys
import traceback
from logging.handlers import TimedRotatingFileHandler

from promptulate.utils.core_utils import get_default_storage_path


class LogManager:
    def __init__(self, framework: str) -> None:
        self.logger = logging.getLogger(framework)
        self.logger.setLevel(logging.DEBUG)

        log_dir = get_default_storage_path("logs")
        cur_time = datetime.datetime.now().strftime("%Y%m%d")
        log_file = f"{log_dir}/{cur_time}.log"

        file_handler = TimedRotatingFileHandler(
            filename=log_file, when="midnight", interval=1, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",  # noqa
            "%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        sys.excepthook = self.exception_handler

    def exception_handler(self, exc_type, exc_value, exc_traceback):
        """
        Handles uncaught exceptions in the program.

        This function is designed to be used as a custom exception handler. It logs the
        details of uncaught exceptions and allows the program to continue running.
        Exceptions derived from KeyboardInterrupt are not handled by this function and 
        are instead passed to the default Python exception handler.

        Args:
            exc_type: The type of the exception.
            exc_value: The instance of the exception.
            exc_traceback: A traceback object encapsulating the call stack at
            the point where the exception originally occurred.
        """
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        tb_info = "".join(
            traceback.format_exception(exc_type, exc_value, exc_traceback)
        )
        self.logger.error(f"Uncaught exception: {tb_info}")

        sys.__excepthook__(exc_type, exc_value, exc_traceback)


logger = LogManager("pne").logger
