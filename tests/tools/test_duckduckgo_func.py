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
# Project Link: https://github.com/Undertone0809/promptulate
# Contact Email: zeeland@foxmail.com

from typing import List, Optional
from duckduckgo_search import DDGS


def search() -> List:
    max_num_of_result = 5
    with DDGS(proxies="socks5://localhost:7890", timeout=20) as ddgs:
        results = ddgs.text(
            "LLM",
            region="cn-zh",
            safesearch="moderate",
            timelimit="y",
            backend="api",
        )
        if results is None or next(results, None) is None:
            return []
        snippets = []
        for i, res in enumerate(results, 1):
            snippets.append(res)
            if i == max_num_of_result:
                break
        return snippets


def main():
    results = search()
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
