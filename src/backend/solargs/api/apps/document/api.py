import os
import re
from loguru import logger
from fastapi import APIRouter
from typing import Annotated
from fastapi import File, UploadFile,Form,Response
from solargs._private.config import Config
from solargs.api.model import RetCode
from solargs.api.apps.db import FileType
from solargs.api.contants import IMG_BASE64_PREFIX
from solargs.api.apps.openapi.api_view_model import Result
from solargs.rag.db_conn.storage_factory import STORAGE_IMPL

from solargs.api.apps.document.request.request import DocUploadRequest,DocInfosdRequest,DocThumbnailsRequest
from solargs.services.api_service.knowledgebase_service import KnowledgebaseService
from solargs.services.api_service.file_service import FileService
from solargs.services.api_service.document_service import DocumentService
from solargs.services.api_service.file2document_service import File2DocumentService

CFG = Config()
router = APIRouter()


@router.post('/document/upload')
async def document_upload(id: Annotated[str, Form()],kb_id: Annotated[str, Form()],files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ]):
    if not kb_id:
        return Result.failed(
            message='Lack of "KB ID"', code=RetCode.ARGUMENT_ERROR)
    # if 'file' not in files:
    #     return Result.failed(
    #      message='No file part!', code=RetCode.ARGUMENT_ERROR)
    file_objs = []
    for file in files:
        file_content = await file.read()
        file_objs.append({"file":file,"file_content":file_content})

    # file_objs = [file for file in files]
    # logger.info(f"file_objs:{file_objs}")
    for file_obj in file_objs:
        if file_obj["file"].filename == '':
            return Result.failed(
                 message='No file selected!', code=RetCode.ARGUMENT_ERROR)

    e, kb = KnowledgebaseService.get_by_id(kb_id)
    if not e:
        raise LookupError("Can't find this knowledgebase!")
    # logger.info(f'kb:{kb.to_dict()}')

    err, _ = FileService.upload_document(kb, file_objs, id)
    if err:
        return Result.failed(
            message="\n".join(err), code=RetCode.SERVER_ERROR)
    return Result.succ(data=True)


@router.post('/document/infos')
def document_infos(request:DocInfosdRequest):
    doc_ids = request.doc_ids
    for doc_id in doc_ids:
        if not DocumentService.accessible(doc_id, request.id):
            return Result.failed(
                message='No authorization.',
                code=RetCode.AUTHENTICATION_ERROR
            )
    docs = DocumentService.get_by_ids(doc_ids)
    return Result.succ(data=list(docs.dicts()))



@router.get('/document/thumbnails')
def document_thumbnails(doc_ids:str="b6e33c42ab9111ef990a0242ac120006,b6f11a7dab9111efaa090242ac120006"):
    doc_ids = doc_ids.split(",")
    if not doc_ids:
        return Result.failed(
            message='Lack of "Document ID"', code=RetCode.ARGUMENT_ERROR)

    try:
        docs = DocumentService.get_thumbnails(doc_ids)
        logger.info(docs)

        for doc_item in docs:
            if doc_item['thumbnail'] and not doc_item['thumbnail'].startswith(IMG_BASE64_PREFIX):
                doc_item['thumbnail'] = f"/v1/document/image/{doc_item['kb_id']}-{doc_item['thumbnail']}"

        return Result.succ(data={d["id"]: d["thumbnail"] for d in docs})
    except Exception as e:
        return Result.failed(code=RetCode.EXCEPTION_ERROR.value, message=e)



@router.get('/document/get/{doc_id}', response_class=Response)
def get_document(doc_id:str):
    try:
        e, doc = DocumentService.get_by_id(doc_id)
        if not e:
            return Result.failed(message="Document not found!")

        b, n = File2DocumentService.get_storage_address(doc_id=doc_id)
        # response = flask.make_response(STORAGE_IMPL.get(b, n))
        # bin_content = STORAGE_IMPL.get(b, n)
        # ext = re.search(r"\.([^.]+)$", doc.name)
        # if ext:
        #     if doc.type == FileType.VISUAL.value:
        #         response.headers.set('Content-Type', 'image/%s' % ext.group(1))
        #     else:
        #         response.headers.set(
        #             'Content-Type',
        #             'application/%s' %
        #             ext.group(1))
        return Response(content=STORAGE_IMPL.get(b, n), media_type="Content-Type")
    except Exception as e:
        return Result.failed(code=RetCode.EXCEPTION_ERROR.value, message=e)



@router.post('/document/parse')
async def document_parse(id: Annotated[str, Form()],url: Annotated[str, Form()],files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ]):
    # url = request.json.get("url") if request.json else ""
    # if url:
    #     if not is_valid_url(url):
    #         return get_json_result(
    #             data=False, message='The URL format is invalid', code=settings.RetCode.ARGUMENT_ERROR)
    #     download_path = os.path.join(get_project_base_directory(), "logs/downloads")
    #     os.makedirs(download_path, exist_ok=True)
    #     from seleniumwire.webdriver import Chrome, ChromeOptions
    #     options = ChromeOptions()
    #     options.add_argument('--headless')
    #     options.add_argument('--disable-gpu')
    #     options.add_argument('--no-sandbox')
    #     options.add_argument('--disable-dev-shm-usage')
    #     options.add_experimental_option('prefs', {
    #         'download.default_directory': download_path,
    #         'download.prompt_for_download': False,
    #         'download.directory_upgrade': True,
    #         'safebrowsing.enabled': True
    #     })
    #     driver = Chrome(options=options)
    #     driver.get(url)
    #     res_headers = [r.response.headers for r in driver.requests]
    #     if len(res_headers) > 1:
    #         sections = RAGFlowHtmlParser().parser_txt(driver.page_source)
    #         driver.quit()
    #         return Result.succ(data="\n".join(sections))
    #
    #     class File:
    #         filename: str
    #         filepath: str
    #
    #         def __init__(self, filename, filepath):
    #             self.filename = filename
    #             self.filepath = filepath
    #
    #         def read(self):
    #             with open(self.filepath, "rb") as f:
    #                 return f.read()
    #
    #     r = re.search(r"filename=\"([^\"]+)\"", str(res_headers))
    #     if not r or not r.group(1):
    #         return Result.failed(
    #             message="Can't not identify downloaded file", code=RetCode.ARGUMENT_ERROR)
    #     f = File(r.group(1), os.path.join(download_path, r.group(1)))
    #     txt = FileService.parse_docs([f], id)
    #     return Result.succ(data=txt)

    if not files:
        return Result.failed(
            message='No file part!', code=RetCode.ARGUMENT_ERROR)
    file_objs = []
    for file in files:
        file_content = await file.read()
        file_objs.append({"file":file,"file_content":file_content})

    txt = FileService.parse_docs(file_objs, id)

    return Result.succ(data=txt)