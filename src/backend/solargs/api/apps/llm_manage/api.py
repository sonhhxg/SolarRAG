from fastapi import APIRouter

from solargs._private.config import Config
from solargs.api.model import RetCode
from solargs.api.apps.db import StatusEnum, LLMType
from solargs.api.apps.db.db_models import TenantLLM
from solargs.api.apps.openapi.api_view_model import Result
from solargs.services.api_service.llm_service import LLMFactoriesService, LLMService,TenantLLMService
from solargs.api.apps.llm_manage.request.request import DeleteLlmRequest,DeleteFactoryRequest,LlmListRequest


CFG = Config()
router = APIRouter()


@router.get("/worker/model/params")
async def model_params():
    print(f"/worker/model/params")
    try:
        params = []
        return Result.succ(params)
        if not worker_instance:
            return Result.failed(code=RetCode.EXCEPTION_ERROR.value, message=f"can not find worker manager")
    except Exception as e:
        return Result.failed(code=RetCode.EXCEPTION_ERROR.value, message=f"model stop failed {e}")


@router.get('/llm/factories')
def factories():
    try:
        fac = LLMFactoriesService.get_all()
        fac = [f.to_dict() for f in fac if f.name not in ["Youdao", "FastEmbed", "BAAI"]]
        llms = LLMService.get_all()
        mdl_types = {}
        for m in llms:
            if m.status != StatusEnum.VALID.value:
                continue
            if m.fid not in mdl_types:
                mdl_types[m.fid] = set([])
            mdl_types[m.fid].add(m.model_type)
        for f in fac:
            f["model_types"] = list(mdl_types.get(f["name"], [LLMType.CHAT, LLMType.EMBEDDING, LLMType.RERANK,
                                                              LLMType.IMAGE2TEXT, LLMType.SPEECH2TEXT, LLMType.TTS]))
        return Result.succ(data=fac)
    except Exception as e:
        return Result.failed(code=RetCode.EXCEPTION_ERROR.value, message=f"llm_factories {e}")


# @router.post('/chat/completions')
# def completion(request:ChatCompletionResponse):
#     req = request
#     msg = []
#     for m in req["messages"]:
#         if m["role"] == "system":
#             continue
#         if m["role"] == "assistant" and not msg:
#             continue
#         msg.append(m)
#     message_id = msg[-1].get("id")
#     try:
#         e, conv = ConversationService.get_by_id(req["conversation_id"])
#         if not e:
#             return get_data_error_result(message="Conversation not found!")
#         conv.message = deepcopy(req["messages"])
#         e, dia = DialogService.get_by_id(conv.dialog_id)
#         if not e:
#             return get_data_error_result(message="Dialog not found!")
#         del req["conversation_id"]
#         del req["messages"]
#
#         if not conv.reference:
#             conv.reference = []
#         conv.message.append({"role": "assistant", "content": "", "id": message_id})
#         conv.reference.append({"chunks": [], "doc_aggs": []})
#
#         def fillin_conv(ans):
#             nonlocal conv, message_id
#             if not conv.reference:
#                 conv.reference.append(ans["reference"])
#             else:
#                 conv.reference[-1] = ans["reference"]
#             conv.message[-1] = {"role": "assistant", "content": ans["answer"],
#                                 "id": message_id, "prompt": ans.get("prompt", "")}
#             ans["id"] = message_id
#
#         def stream():
#             nonlocal dia, msg, req, conv
#             try:
#                 for ans in chat(dia, msg, True, **req):
#                     fillin_conv(ans)
#                     yield "data:" + json.dumps({"code": 0, "message": "", "data": ans}, ensure_ascii=False) + "\n\n"
#                 ConversationService.update_by_id(conv.id, conv.to_dict())
#             except Exception as e:
#                 traceback.print_exc()
#                 yield "data:" + json.dumps({"code": 500, "message": str(e),
#                                             "data": {"answer": "**ERROR**: " + str(e), "reference": []}},
#                                            ensure_ascii=False) + "\n\n"
#             yield "data:" + json.dumps({"code": 0, "message": "", "data": True}, ensure_ascii=False) + "\n\n"
#
#         if req.get("stream", True):
#             resp = Response(stream(), mimetype="text/event-stream")
#             resp.headers.add_header("Cache-control", "no-cache")
#             resp.headers.add_header("Connection", "keep-alive")
#             resp.headers.add_header("X-Accel-Buffering", "no")
#             resp.headers.add_header("Content-Type", "text/event-stream; charset=utf-8")
#             return resp
#
#         else:
#             answer = None
#             for ans in chat(dia, msg, **req):
#                 answer = ans
#                 fillin_conv(ans)
#                 ConversationService.update_by_id(conv.id, conv.to_dict())
#                 break
#             return get_json_result(data=answer)
#     except Exception as e:
#         return server_error_response(e)


@router.post('/llm/delete_llm')
def delete_llm(request:DeleteLlmRequest):
    try:
        TenantLLMService.filter_delete(
            [TenantLLM.tenant_id == request.id, TenantLLM.llm_factory == request.llm_factory,
             TenantLLM.llm_name == request.llm_name])
        return Result.succ(data=True,message=f"use_id is {request.id} delete llm name is success")
    except Exception as e:
        return Result.failed(code=RetCode.EXCEPTION_ERROR.value, message=e)

@router.post('/llm/delete_factory')
def delete_factory(request:DeleteFactoryRequest):
    try:
        TenantLLMService.filter_delete(
            [TenantLLM.tenant_id == request.id, TenantLLM.llm_factory == request.llm_factory])
        return Result.succ(data=True,message=f"use_id is {request.id} delete llm factory is success")
    except Exception as e:
        return Result.failed(code=RetCode.EXCEPTION_ERROR.value, message=e)


@router.get('/llm/my_llms')
def my_llms(id:str):
    try:
        res = {}
        for o in TenantLLMService.get_my_llms(id):
            if o["llm_factory"] not in res:
                res[o["llm_factory"]] = {
                    "tags": o["tags"],
                    "llm": []
                }
            res[o["llm_factory"]]["llm"].append({
                "type": o["model_type"],
                "name": o["llm_name"],
                "used_token": o["used_tokens"]
            })
        return Result.succ(data=res)
    except Exception as e:
        return Result.failed(code=RetCode.EXCEPTION_ERROR.value, message=e)


@router.get('/llm/list')
def list_app(request:LlmListRequest):
    self_deploied = ["Youdao", "FastEmbed", "BAAI", "Ollama", "Xinference", "LocalAI", "LM-Studio"]
    weighted = ["Youdao", "FastEmbed", "BAAI"] if CFG.LIGHTEN != 0 else []
    model_type = request.model_type
    try:
        objs = TenantLLMService.query(tenant_id=request.id)
        facts = set([o.to_dict()["llm_factory"] for o in objs if o.api_key])
        llms = LLMService.get_all()
        llms = [m.to_dict()
                for m in llms if m.status == StatusEnum.VALID.value and m.fid not in weighted]
        for m in llms:
            m["available"] = m["fid"] in facts or m["llm_name"].lower() == "flag-embedding" or m["fid"] in self_deploied

        llm_set = set([m["llm_name"] + "@" + m["fid"] for m in llms])
        for o in objs:
            if not o.api_key: continue
            if o.llm_name + "@" + o.llm_factory in llm_set: continue
            llms.append({"llm_name": o.llm_name, "model_type": o.model_type, "fid": o.llm_factory, "available": True})

        res = {}
        for m in llms:
            if model_type and m["model_type"].find(model_type) < 0:
                continue
            if m["fid"] not in res:
                res[m["fid"]] = []
            res[m["fid"]].append(m)

        return Result.succ(data=res)
    except Exception as e:
        return Result.failed(code=RetCode.EXCEPTION_ERROR.value, message=e)


