from typing import List, Optional

# from solargs._private.pydantic import BaseModel
from pydantic import BaseModel

class UserRequest(BaseModel):
    """query: knowledge query"""
    email: str = "sonhhxg0529@163.com"
    nickname: str = "sonhhxg0529"
    password: str = "123456"
