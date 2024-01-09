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
import random
import shutil
import string
import tempfile
import time
from functools import wraps
from importlib import import_module
from typing import Callable, Dict, List, Optional

from cushy_storage import CushyOrmCache

__all__ = [
    "get_cache",
    "get_default_storage_path",
    "record_time",
    "generate_conversation_id",
    "generate_run_id",
    "generate_unique_id",
    "listdict_to_string",
]
logger = logging.getLogger(__name__)


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.

    Args:
        dotted_path: eg promptulate.schema.MessageSet

    Returns:
        Class corresponding to dotted path.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(
            'Module "%s" does not define a "%s" attribute/class'
            % (module_path, class_name)
        ) from err


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


def generate_unique_id() -> str:
    timestamp = int(time.time() * 1000)
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=6))

    unique_id = f"pne-{timestamp}-{random_string}"
    return unique_id


def generate_run_id() -> str:
    return generate_unique_id()


def generate_conversation_id() -> str:
    """Generating a new conversation_id when a conversation initialize"""
    return generate_unique_id()


def get_cache():
    return cache


def set_openai_api_key(value: str):
    cache["OPENAI_API_KEY"] = value


def convert_backslashes(path: str):
    """Convert all \\ to / of file path."""
    return path.replace("\\", "/")


def get_default_storage_path(module_name: str = "") -> str:
    storage_path = os.path.expanduser("~/.pne")

    if module_name:
        storage_path = os.path.join(storage_path, module_name)

    # Try to create the storage path (with module subdirectory if specified)
    # Use a temporary directory instead if permission is denied,
    try:
        os.makedirs(storage_path, exist_ok=True)
    except PermissionError:
        storage_path = os.path.join(tempfile.gettempdir(), "pne", module_name)
        os.makedirs(storage_path, exist_ok=True)

    return convert_backslashes(storage_path)


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
            logger.debug(f"[pne timer] <{fn.__name__}> run {duration}s")
            return ret

        return wrapper

    return decorator


def delete_cache(specified_module: str = None):
    """Delete cache or specified cache module"""
    cache_path = get_default_storage_path("cache")
    if specified_module:
        cache_path = f"{cache_path}/{specified_module[:2]}"
    shutil.rmtree(cache_path)


cache = CushyOrmCache(get_default_storage_path("cache"))
