from pathlib import Path

from pydantic import BaseModel, Field

from solargs._private.config import Config

CFG = Config()

class HeartbeatResult(BaseModel):

    is_alive: bool = Field(default=True, description="Is the server alive?")
    version: str = Field(default=CFG.VERSION, description="Server version")
    # 是否开发生产环境
    is_debug: bool = Field(default=CFG.DEBUG, description="is debug")
    project_path: Path = Field(default=CFG.PROJECT_DIR)