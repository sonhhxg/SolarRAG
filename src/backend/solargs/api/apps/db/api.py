from fastapi import APIRouter
import re
import flask
from loguru import logger
from solargs._private.config import Config
from solargs.api.apps.openapi.api_view_model import Result


from solargs.rag import STORAGE_IMPL
from solargs.api.apps.db import FileType
from solargs.api.apps.db.service import DatabaseService
from solargs.services.api_service.file_service import FileService
from solargs.services.api_service.file2document_service import File2DocumentService


CFG = Config()
router = APIRouter()

database_service = DatabaseService()


@router.get('/db/file/{file_id}')
def get_file(file_id):
    logger.info(f"/api/v1/db/file/ file_id: {file_id}")
    try:
        e, file = FileService.get_by_id(file_id)
        if not e:
            return Result.failed(msg="Document not found!")
        b, n = File2DocumentService.get_storage_address(file_id=file_id)
        response = flask.make_response(STORAGE_IMPL.get(b, n))
        ext = re.search(r"\.([^.]+)$", file.name)
        if ext:
            if file.type == FileType.VISUAL.value:
                response.headers.set('Content-Type', 'image/%s' % ext.group(1))
            else:
                response.headers.set(
                    'Content-Type',
                    'application/%s' %
                    ext.group(1))
        return response
    except Exception as e:
        return Result.failed(msg=e)



