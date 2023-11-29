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

from loguru import logger as _logger

from promptulate.utils.core_utils import get_default_storage_path
from promptulate.utils.singleton import Singleton


def get_log_path() -> str:
    log_directory = get_default_storage_path("logs")
    current_time = datetime.datetime.now().strftime("%Y%m%d")
    return f"{log_directory}/{current_time}.log"


def enable_log():
    logger.remove()

    logger.add(get_log_path(), level="DEBUG")
    logger.add(sys.stderr, level="DEBUG")


class Logger(metaclass=Singleton):
    def __init__(self) -> None:
        self.logger = _logger

        self.logger.remove()

        self.logger.add(get_log_path(), level="DEBUG")
        self.logger.add(sys.stderr, level="WARNING")


logger = Logger().logger
