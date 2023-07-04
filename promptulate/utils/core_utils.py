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

import logging
import os
import platform
import shutil
import tempfile
import time
from functools import wraps
from typing import Callable, Dict, List, Optional

from cushy_storage import CushyOrmCache

__all__ = [
    "get_cache",
    "get_project_root_path",
    "get_default_storage_path",
    "record_time",
    "generate_conversation_id",
    "listdict_to_string",
]
logger = logging.getLogger(__name__)


def listdict_to_string(
        data: List[Dict],
        prefix: Optional[str] = "",
        suffix: Optional[str] = "\n",
        item_prefix: Optional[str] = "",
        item_suffix: Optional[str] = ";\n\n",
        is_wrap: bool = True,
) -> str:
    """Convert List[Dict] type data to string type"""
    wrap_ch = "\n" if is_wrap else ""
    result = f"{prefix}"
    for item in data:
        temp_list = ["{}:{} {}".format(k, v, wrap_ch) for k, v in item.items()]
        result += f"{item_prefix}".join(temp_list) + f"{item_suffix}"
    result += suffix
    return result[:-2]


def generate_conversation_id() -> str:
    """Generating a new conversation_id when a conversation initialize"""
    return str(int(time.time()))


def get_cache():
    return cache


def get_project_root_path() -> str:
    """get project root path or current path"""
    project_path = os.getcwd()
    max_depth = 10
    count = 0
    while not os.path.exists(os.path.join(project_path, "README.md")):
        project_path = os.path.split(project_path)[0]
        count += 1
        if count > max_depth:
            return os.getcwd()
    return project_path


def set_openai_api_key(value: str):
    cache["OPENAI_API_KEY"] = value


def get_default_storage_path(file_name: str = "") -> str:
    if platform.system() == "Windows":
        return f"{get_project_root_path()}/{file_name}"
    elif platform.system() == "Linux" or "Darwin":
        dir_path = os.environ.get("TMPDIR")
        if not dir_path:
            dir_path = tempfile.gettempdir()
        dir_path = os.path.join(dir_path, "promptulate")
        return f"{dir_path}/{file_name}"
    else:
        return f"./{file_name}"


def hint(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        ret = fn(*args, **kwargs)
        logger.debug(f"function {fn.__name__} is running now")
        return ret

    return wrapper


def record_time():
    def decorator(fn: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            start_time = time.time()
            ret = fn(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"[promptulate timer] <{fn.__name__}> run {duration}s")
            return ret

        return wrapper

    return decorator


def delete_cache(specified_module: str = None):
    """Delete cache or specified cache module"""
    cache_path = get_default_storage_path("cache")
    if specified_module:
        cache_path = f"{get_project_root_path()}/{specified_module[:2]}"
    shutil.rmtree(cache_path)


cache = CushyOrmCache(get_default_storage_path("cache"))
