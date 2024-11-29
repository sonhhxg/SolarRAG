#
#  Copyright 2024 The InfiniFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import dotenv
import typing


def get_versions() -> typing.Mapping[str, typing.Any]:
    dotenv.load_dotenv(dotenv.find_dotenv())
    return dotenv.dotenv_values()


def get_solargs_version() -> typing.Optional[str]:
    return get_versions().get("SOLARGS_IMAGE", "sonhhxg0529/solargs:dev").split(":")[-1]

def is_pre_release(v: str) -> bool:
    """Whether the version is a pre-release version.

    Returns a boolean indicating whether the version is a pre-release version,
    as per the definition of a pre-release segment from PEP 440.
    """
    return any(label in v for label in ["a", "b", "rc"])


def is_nightly(v: str) -> bool:
    """Whether the version is a dev (nightly) version.

    Returns a boolean indicating whether the version is a dev (nightly) version,
    as per the definition of a dev segment from PEP 440.
    """
    return "dev" in v


version = get_solargs_version()