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
import logging
import os

from promptulate import utils

logger = logging.getLogger(__name__)


def get_logger():
    return logger


def get_default_log_path():
    return utils.get_default_storage_path("log")


def get_log_name() -> str:
    log_path = get_default_log_path()
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    cur_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{log_path}/log_{cur_time}.log"


def enable_log(level=logging.DEBUG):
    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(f"{get_log_name()}", mode="w", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def enable_log_no_file():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] %(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
