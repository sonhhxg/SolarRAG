from pydantic import BaseModel

class DatabaseRequest(BaseModel):
    """query: knowledge query"""
    db_type: str = "mysql"
    database: str = None
    username: str = None
    host: str = None
    port: int = None
    password: str = None
