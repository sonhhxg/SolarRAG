from fastapi import APIRouter

from solargs.api.apps.openapi.api_view_model import Result

router = APIRouter()



@router.post("/chat/completions")
def chat_completions():
    try:
        params = []
        return Result.succ(params)
        if not worker_instance:
            return Result.failed(code="E000X", message=f"can not find worker manager")
    except Exception as e:
        return Result.failed(code="E000X", message=f"model stop failed {e}")











