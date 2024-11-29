from fastapi import APIRouter

from loguru import logger
from solargs.api.model import RetCode
from solargs._private.config import Config
from solargs.api.apps.openapi.api_view_model import Result
from solargs.api.apps.embeddings.service import EmbeddingService
from solargs.api.apps.embeddings.request.request import EmbeddingRequest

CFG = Config()
router = APIRouter()

embedding_service = EmbeddingService()

@router.post("/embeddings/ollama/query")
def emb_query(request:EmbeddingRequest):
    logger.info(f"/api/v1/embeddings/ollama/query params: {request}")
    try:
        ves = embedding_service.embedding_for_prompt(request)
        return Result.succ(data=ves)
    except Exception as e:
        return Result.failed(code=RetCode.EXCEPTION_ERROR.value, message=f"emb_query error {e}")