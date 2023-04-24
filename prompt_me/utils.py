# Copyright (c) 2023 Zeeland
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
# Project Link: https://github.com/Undertone0809/prompt-me
# Contact Email: zeeland@foxmail.com

import os
import sys
import logging
import platform
import datetime
from functools import wraps
from cushy_storage import CushyDict

__all__ = ['get_cache', 'get_logger', 'enable_log', 'enable_log_no_file']
logger = logging.getLogger(__name__)


def get_cache():
    return cache


def get_logger():
    return logger


def get_project_root_path() -> str:
    project_path = os.getcwd()
    max_depth = 10
    count = 0
    while not os.path.exists(os.path.join(project_path, 'README.md')):
        project_path = os.path.split(project_path)[0]
        count += 1
        if count > max_depth:
            return os.getcwd()
    return project_path


def _check_log_path():
    log_path = os.path.join(get_project_root_path(), 'log')
    if not os.path.exists(log_path):
        os.makedirs(log_path)


def get_log_name() -> str:
    _check_log_path()
    cur_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{get_project_root_path()}/log/log_{cur_time}.log"


def enable_log():
    if platform.system() == 'Windows':
        logging.basicConfig(
            level=logging.DEBUG,
            format='[%(levelname)s] %(asctime)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(f"{get_log_name()}", mode='w', encoding='utf-8'),
                logging.StreamHandler()
            ],
        )


def enable_log_no_file():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] %(asctime)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )


def hint(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        ret = fn(*args, **kwargs)
        logger.debug(f'function {fn.__name__} is running now')
        return ret

    return wrapper


cache = CushyDict(get_project_root_path() + "/cache")
