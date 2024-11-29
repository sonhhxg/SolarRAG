from pydantic import BaseModel

class EmbeddingRequest(BaseModel):
    """embedding request"""
    url: str = r"http://localhost:11434"
    model: str = "bge-m3"
    prompt: str = "hello"
