from pydantic import BaseModel


class KBRequest(BaseModel):
    """query: knowledge query"""
    id: str = None
    name: str = "test"

class KBDetailRequest(BaseModel):
    """query: knowledge query"""
    id: str = None
    kb_id: str = None

class KBListRequest(BaseModel):
    """query: knowledge query"""
    id: str = None
    page: int = 1
    page_size: int = 150
    orderby: str = "create_time"
    desc: bool = True

class KBRMRequest(BaseModel):
    """query: knowledge query"""
    id: str = None
    kb_id: str = None
