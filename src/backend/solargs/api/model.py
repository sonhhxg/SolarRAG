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
import os
from datetime import date
from enum import IntEnum, Enum

class CustomEnum(Enum):
    @classmethod
    def valid(cls, value):
        try:
            cls(value)
            return True
        except BaseException:
            return False

    @classmethod
    def values(cls):
        return [member.value for member in cls.__members__.values()]

    @classmethod
    def names(cls):
        return [member.name for member in cls.__members__.values()]

class PythonDependenceName(CustomEnum):
    Rag_Source_Code = "python"
    Python_Env = "miniconda"


class ModelStorage(CustomEnum):
    REDIS = "redis"
    MYSQL = "mysql"


class RetCode(IntEnum, CustomEnum):
    """
    成功=200
    无效=10
    异常错误=100
    ARGUMENT_ERROR=101
    数据错误=102
    操作错误=103
    连接错误=105
    跑步=106
    允许错误=108
    身份验证错误=109
    未经授权=401
    服务器错误=500
    禁止=403
    未找到=404
    """
    SUCCESS = 200
    NOT_EFFECTIVE = 10
    EXCEPTION_ERROR = 100
    ARGUMENT_ERROR = 101
    DATA_ERROR = 102
    OPERATING_ERROR = 103
    CONNECTION_ERROR = 105
    RUNNING = 106
    PERMISSION_ERROR = 108
    AUTHENTICATION_ERROR = 109
    UNAUTHORIZED = 401
    SERVER_ERROR = 500
    FORBIDDEN = 403
    NOT_FOUND = 404