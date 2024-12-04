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

from typing import Optional

from promptulate.config import Config

PROXY_MODE = ["off", "custom", "promptulate"]


def set_proxy_mode(mode: str, proxies: Optional[dict] = None):
    """
    Set proxy mode. Promptulate offer three proxy mode ['off', 'custom', 'promptulate']
    'off' disables your proxy mode. This is the normal status.
    'custom' means you can set your custom proxy. Moreover, you must pass proxies
    'promptulate' provide free proxy you can use it.

    Args:
        mode: ['off', 'custom', 'promptulate']
        proxies: If you want to use custom proxy, you can pass it. An example
        proxies is {'http': 'http://127.0.0.1:7890'}
    """
    if mode not in PROXY_MODE:
        raise ValueError("proxy mode must in ['off', 'custom', 'promptulate']")

    if mode == "promptulate":
        raise ValueError(
            "Current promptulate free proxy mode is not supported yet. A better solution will be provided soon."  # noqa
        )

    if mode == "custom" and not proxies:
        raise ValueError("proxies must be passed when proxy mode is custom")

    Config().set_proxy_mode(mode, proxies)
