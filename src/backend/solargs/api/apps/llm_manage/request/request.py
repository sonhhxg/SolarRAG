from pydantic import BaseModel


class DeleteLlmRequest(BaseModel):
    """query: knowledge query"""
    id: str = None
    llm_factory: str = "Tongyi-Qianwen"
    """top_k: return topK documents"""
    llm_name:  str = "qwen-plus"


class ChatCompletionRequest(BaseModel):
    """ModelRequest"""
    conversation_id: str = None
    messages: list = None

class DeleteFactoryRequest(BaseModel):
    id: str = None
    llm_factory: str = "Tongyi-Qianwen"


class LlmListRequest(BaseModel):
    id: str = None
    model_type: str = "chat"