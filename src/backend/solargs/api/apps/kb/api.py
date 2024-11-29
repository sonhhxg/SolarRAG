from loguru import logger
from fastapi import APIRouter
from solargs._private.config import Config

from solargs.api.model import RetCode
from solargs.api.apps.db import StatusEnum
from solargs.api.utils import get_uuid
from solargs.api.apps.openapi.api_view_model import Result
from solargs.api.apps.kb.request.request import (KBRequest,
                                                 KBDetailRequest,
                                                 KBListRequest,
                                                 KBRMRequest)

from solargs.services import duplicate_name
from solargs.services.api_service.user_service import TenantService,UserTenantService
from solargs.services.api_service.file2document_service import File2DocumentService
from solargs.services.api_service.knowledgebase_service import KnowledgebaseService
from solargs.services.api_service.document_service import DocumentService


CFG = Config()
router = APIRouter()


@router.post("/kb/create")
def kb_create(request:KBRequest):
    req = {}
    req["name"] = request.name.strip()
    req["name"] = duplicate_name(
        KnowledgebaseService.query,
        name=req["name"],
        tenant_id=request.id,
        status=StatusEnum.VALID.value)
    try:
        req["id"] = get_uuid()
        req["tenant_id"] = request.id
        req["created_by"] = request.id
        e, t = TenantService.get_by_id(request.id)
        if not e:
            return Result.failed(message="Tenant not found.")
        req["embd_id"] = t.embd_id
        if not KnowledgebaseService.save(**req):
            return Result.failed(code=RetCode.DATA_ERROR.value, message=None)
        return Result.succ(data={"kb_id": req["id"]})
    except Exception as e:
        return Result.failed(code=RetCode.EXCEPTION_ERROR.value, message=e)


# 知识库描述
@router.get('/kb/detail')
def kb_detail(request:KBDetailRequest):
    logger.info(f"/api/v1/kb/detail/ param: {request}")
    kb_id = request.kb_id
    try:
        tenants = UserTenantService.query(user_id=request.id)
        for tenant in tenants:
            if KnowledgebaseService.query(
                    tenant_id=tenant.tenant_id, id=kb_id):
                break
        else:
            return Result.failed(
                message='Only owner of knowledgebase authorized for this operation.',
                code=RetCode.OPERATING_ERROR)
        kb = KnowledgebaseService.get_detail(kb_id)
        if not kb:
            return Result.failed(
                message="Can't find this knowledgebase!")
        return Result.succ(data=kb)
    except Exception as e:
        return Result.failed(code=RetCode.EXCEPTION_ERROR.value, message=e)

# 知识库列表
@router.get('/kb/list')
def kb_list(request:KBListRequest):
    logger.info(f"/api/v1/kb/list param: {request}")
    page_number = request.page
    items_per_page = request.page_size
    orderby = request.orderby
    desc = request.desc
    try:
        tenants = TenantService.get_joined_tenants_by_user_id(request.id)
        kbs = KnowledgebaseService.get_by_tenant_ids(
            [m["tenant_id"] for m in tenants], request.id, page_number, items_per_page, orderby, desc)
        return Result.succ(data=kbs)
    except Exception as e:
        return Result.failed(msg=e)

# 删除知识库
@router.post('/kb/rm')
def kb_rm(request:KBRMRequest):
    logger.info(f"/api/v1/kb/rm param: {request}")
    req = request.json
    if not KnowledgebaseService.accessible4deletion(request.kb_id, request.id):
        return Result.failed(
            message='No authorization.',
            code=RetCode.AUTHENTICATION_ERROR
        )
    try:
        kbs = KnowledgebaseService.query(
                created_by=request.id, id=request.kb_id)
        if not kbs:
            return Result.failed(
                message='Only owner of knowledgebase authorized for this operation.', code=RetCode.OPERATING_ERROR)

        for doc in DocumentService.query(kb_id=req["kb_id"]):
            if not DocumentService.remove_document(doc, kbs[0].tenant_id):
                return Result.failed(
                    message="Database error (Document removal)!")
            f2d = File2DocumentService.get_by_document_id(doc.id)
            # FileService.filter_delete([File.source_type == FileSource.KNOWLEDGEBASE, File.id == f2d[0].file_id])
            File2DocumentService.delete_by_document_id(doc.id)

        if not KnowledgebaseService.delete_by_id(req["kb_id"]):
            return Result.failed(
                message="Database error (Knowledgebase removal)!")
        # settings.docStoreConn.delete({"kb_id": req["kb_id"]}, search.index_name(kbs[0].tenant_id), req["kb_id"])
        return Result.succ(data=True)
    except Exception as e:
        return Result.failed(code=RetCode.EXCEPTION_ERROR.value, message=e)



