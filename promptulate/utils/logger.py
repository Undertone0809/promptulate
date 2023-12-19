# Copyright (c) 2023 promptulate
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright Owner: Zeeland
# GitHub Link: https://github.com/Undertone0809/
# Project Link: https://github.com/Undertone0809/promptulate
# Contact Email: zeeland@foxmail.com

import datetime
import sys
import traceback

from loguru import logger as _logger

from promptulate.utils.core_utils import get_default_storage_path
from promptulate.utils.singleton import Singleton


def get_log_path() -> str:
    log_directory = get_default_storage_path("logs")
    current_time = datetime.datetime.now().strftime("%Y%m%d")
    return f"{log_directory}/{current_time}.log"


def enable_log():
    """
    Enables the logging system to see log information.

    This function configures the logging system to write logs to a file and stderr.
    The log file is located at the path returned by the get_log_path function, and the
    log level for the file is set to DEBUG. The log level for stderr is also set to
    DEBUG.
    """
    logger.remove()

    logger.add(get_log_path(), level="DEBUG", rotation="1 day", filter=pne_log_filter)
    logger.add(sys.stderr, level="DEBUG")


def pne_log_filter(record) -> bool:
    """
    Filter function for the logging system.

    This function is used to filter out log records based on their name.
    Only records whose name starts with "promptulate" are allowed through the filter.

    Args:
        record (dict): A log record, which is a dictionary that the logging system
        uses to store information about the event being logged. The 'name' key in the
        record dictionary contains the name of the logger that created the record.

    Returns:
        bool: True if the record's name starts with "promptulate", False otherwise.
    """
    return record["name"].startswith("promptulate")


class Logger(metaclass=Singleton):
    """
    Logger class that uses the Singleton design pattern.

    This class is responsible for managing the application's logging system. It uses
    the loguru library for logging. The logger is configured to write logs to a file
    and stderr. The log file is located at the path returned by the get_log_path
    function, and the log level for the file is set to DEBUG. The log level for
    stderr is set to WARNING.

    Attributes:
        logger: An instance of the loguru logger.
    """

    def __init__(self) -> None:
        self.logger = _logger

        self.logger.remove()

        self.logger.add(
            get_log_path(), level="DEBUG", rotation="1 day", filter=pne_log_filter
        )
        self.logger.add(sys.stderr, level="WARNING")


def exception_handler(exc_type, exc_value, exc_traceback):
    """
    Handles uncaught exceptions in the program.

    This function is designed to be used as a custom exception handler. It logs the
    details of uncaught exceptions and allows the program to continue running.
    Exceptions derived from KeyboardInterrupt are not handled by this function and are
    instead passed to the default Python exception handler.

    Args:
        exc_type: The type of the exception.
        exc_value: The instance of the exception.
        exc_traceback: A traceback object encapsulating the call stack at
        the point where the exception originally occurred.

    Returns:
        None
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    tb_info = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logger.error(f"Uncaught exception: {tb_info}")


logger = Logger().logger
sys.excepthook = exception_handler
