#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from pathlib import Path
from datetime import date
from dotenv import load_dotenv

import solargs
from solargs.utils.singleton import Singleton
from solargs.api.utils import get_base_config,decrypt_database_config



class Config(metaclass=Singleton):
    """Configuration class to store the state of bools for different scripts access"""


    def __init__(self) -> None:
        # 加载 .env 文件
        load_dotenv()
        self.LANGUAGE = os.getenv("LANGUAGE", "cn")
        # self.WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT", 7520))

        self.SOLARGS_SERVICE_NAME = "solargs"

        self.VERSION = solargs.__version__
        self.API_VERSION = os.getenv("API_VERSION", "v1")
        self.WORKERS = int(os.getenv("WORKERS", 2))

        self.DEBUG = os.getenv("DEBUG", True)

        # project dir
        self.PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
        if not os.path.exists(self.PROJECT_DIR/"logs"):
            os.mkdir(self.PROJECT_DIR/"logs")

        # log file
        self.LOG_FILE = self.PROJECT_DIR / "logs/solargs_app.log"

        # server host and port
        self.HOST = get_base_config(self.SOLARGS_SERVICE_NAME, {}).get("host", "127.0.0.1")
        self.HTTP_PORT = get_base_config(self.SOLARGS_SERVICE_NAME, {}).get("http_port")
        self.SECRET_KEY = get_base_config(self.SOLARGS_SERVICE_NAME,{}).get("secret_key", str(date.today()))

        # ES config
        self.ES_NAME = "es"
        self.ES = get_base_config(self.ES_NAME, {})

        # minio config
        self.MINIO_NAME = "minio"
        self.MINIO = get_base_config(self.MINIO_NAME, {})

        # DB config
        self.DATABASE_TYPE = os.getenv("DB_TYPE", 'mysql')
        self.DATABASE = decrypt_database_config(name=self.DATABASE_TYPE)

        self.DOC_ENGINE = "elasticsearch"
        # redis
        self.SVR_QUEUE_RETENTION = 60 * 60
        try:
            self.REDIS = decrypt_database_config(name="redis")
        except Exception:
            self.REDIS = {}

        self.SVR_QUEUE_NAME = "rag_flow_svr_queue"

        self.LIGHTEN = int(os.environ.get('LIGHTEN', "0"))

