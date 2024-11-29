import logging
import os
import re
import tempfile
from typing import List

from fastapi import APIRouter, File, Form, UploadFile

from solargs.api.model import RetCode
from solargs._private.config import Config
from solargs.api.apps.knowledge.request.request import (
    ChunkQueryRequest,
    DocumentQueryRequest,
    DocumentSummaryRequest,
    DocumentSyncRequest,
    EntityExtractRequest,
    KnowledgeDocumentRequest,
    KnowledgeQueryRequest,
    KnowledgeQueryResponse,
    KnowledgeSpaceRequest,
    KnowledgeSyncRequest,
    SpaceArgumentRequest,
)

from solargs.api.apps.openapi.api_view_model import Result

logger = logging.getLogger(__name__)

CFG = Config()
router = APIRouter()


@router.get("/knowledge/query/list")
def space_list():
    print(f"/space/list params:")
    try:
        return Result.succ({"query":"hello","top_k":5})
    except Exception as e:
        return Result.failed(code=RetCode.EXCEPTION_ERROR.value, msg=f"space list error {e}")



@router.get("/knowledge/kb/create")
def kb_create():
    pass




#
# @router.post('/knowledge/document/upload')
# def upload(kb_name: str):
#     tenant_id = objs[0].tenant_id
#
#     try:
#         e, kb = KnowledgebaseService.get_by_name(kb_name, tenant_id)
#         if not e:
#             return Result.failed(
#                 msg="Can't find this knowledgebase!")
#         kb_id = kb.id
#     except Exception as e:
#         return Result.failed(msg=e)
#
#     if 'file' not in request.files:
#         return Result.failed(msg='No file part!')
#
#     file = request.files['file']
#     if file.filename == '':
#         return get_json_result(
#             data=False, retmsg='No file selected!', retcode=RetCode.ARGUMENT_ERROR)
#
#     root_folder = FileService.get_root_folder(tenant_id)
#     pf_id = root_folder["id"]
#     FileService.init_knowledgebase_docs(pf_id, tenant_id)
#     kb_root_folder = FileService.get_kb_folder(tenant_id)
#     kb_folder = FileService.new_a_file_from_kb(kb.tenant_id, kb.name, kb_root_folder["id"])
#
#     try:
#         if DocumentService.get_doc_count(kb.tenant_id) >= int(os.environ.get('MAX_FILE_NUM_PER_USER', 8192)):
#             return Result.failed(msg="Exceed the maximum file number of a free user!")
#
#         filename = duplicate_name(
#             DocumentService.query,
#             name=file.filename,
#             kb_id=kb_id)
#         filetype = filename_type(filename)
#         if not filetype:
#             return Result.failed(msg="This type of file has not been supported yet!")
#
#         location = filename
#         while STORAGE_IMPL.obj_exist(kb_id, location):
#             location += "_"
#         blob = request.files['file'].read()
#         STORAGE_IMPL.put(kb_id, location, blob)
#         doc = {
#             "id": get_uuid(),
#             "kb_id": kb.id,
#             "parser_id": kb.parser_id,
#             "parser_config": kb.parser_config,
#             "created_by": kb.tenant_id,
#             "type": filetype,
#             "name": filename,
#             "location": location,
#             "size": len(blob),
#             "thumbnail": thumbnail(filename, blob)
#         }
#
#         form_data = request.form
#         if "parser_id" in form_data.keys():
#             if request.form.get("parser_id").strip() in list(vars(ParserType).values())[1:-3]:
#                 doc["parser_id"] = request.form.get("parser_id").strip()
#         if doc["type"] == FileType.VISUAL:
#             doc["parser_id"] = ParserType.PICTURE.value
#         if doc["type"] == FileType.AURAL:
#             doc["parser_id"] = ParserType.AUDIO.value
#         if re.search(r"\.(ppt|pptx|pages)$", filename):
#             doc["parser_id"] = ParserType.PRESENTATION.value
#         if re.search(r"\.(eml)$", filename):
#             doc["parser_id"] = ParserType.EMAIL.value
#
#         doc_result = DocumentService.insert(doc)
#         FileService.add_file_from_kb(doc, kb_folder["id"], kb.tenant_id)
#     except Exception as e:
#         return Result.failed(msg=e)
#
#     if "run" in form_data.keys():
#         if request.form.get("run").strip() == "1":
#             try:
#                 info = {"run": 1, "progress": 0}
#                 info["progress_msg"] = ""
#                 info["chunk_num"] = 0
#                 info["token_num"] = 0
#                 DocumentService.update_by_id(doc["id"], info)
#                 # if str(req["run"]) == TaskStatus.CANCEL.value:
#                 tenant_id = DocumentService.get_tenant_id(doc["id"])
#                 if not tenant_id:
#                     return get_data_error_result(retmsg="Tenant not found!")
#
#                 # e, doc = DocumentService.get_by_id(doc["id"])
#                 TaskService.filter_delete([Task.doc_id == doc["id"]])
#                 e, doc = DocumentService.get_by_id(doc["id"])
#                 doc = doc.to_dict()
#                 doc["tenant_id"] = tenant_id
#                 bucket, name = File2DocumentService.get_storage_address(doc_id=doc["id"])
#                 queue_tasks(doc, bucket, name)
#             except Exception as e:
#                 return Result.failed(msg=e)
#
#     return Result.succ(data=doc_result.to_json())




