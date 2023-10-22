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

import pathlib

import setuptools

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="promptulate",
    version="1.8.0",
    author="Zeeland",
    author_email="zeeland@foxmail.com",
    description="A powerful LLM Application development framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Undertone0809/promptulate",
    packages=setuptools.find_packages(),
    install_requires=[
        "cushy-storage",
        "dotenv~=1.0.0",
        "pydantic~=1.10.0",
        "requests",
        "duckduckgo_search",
        "broadcast-service==1.3.2",
        "arxiv",
        "click",
        "numexpr",
        "questionary~=2.0.0",
    ],
    license="Apache 2.0",
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords="promptulate, pne, prompt, chatgpt, gpt, chatbot, llm, openai",
    entry_points={"console_scripts": ["pne-chat=promptulate.client.chat:main"]},
)
