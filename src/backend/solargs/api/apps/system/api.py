from fastapi import APIRouter
from timeit import default_timer as timer

from solargs.api import settings
from solargs._private.config import Config
from solargs.api.model import RetCode
from solargs.api.apps.openapi.api_view_model import Result
from solargs.rag.db_conn.storage_factory import STORAGE_IMPL,STORAGE_IMPL_TYPE
from solargs.services.api_service.base_service import BaseService

CFG = Config()
router = APIRouter()



@router.get('/system/version')
def version():
    try:
        return Result.succ(data=CFG.VERSION)
    except Exception as e:
        return Result.failed(code=RetCode.EXCEPTION_ERROR.value, message=f"get version failed {e}")


@router.get('/system/status')
def status():
    res = {}
    st = timer()
    try:
        res["es"] = settings.docStoreConn.health()
        res["es"]["elapsed"] = "{:.1f}".format((timer() - st)*1000.)
    except Exception as e:
        res["es"] = {"status": "red", "elapsed": "{:.1f}".format((timer() - st)*1000.), "error": str(e)}

    st = timer()
    try:
        STORAGE_IMPL.health()
        res["storage"] = {"storage": STORAGE_IMPL_TYPE.lower(), "status": "green", "elapsed": "{:.1f}".format((timer() - st)*1000.)}
    except Exception as e:
        res["storage"] = {"storage": STORAGE_IMPL_TYPE.lower(), "status": "red", "elapsed": "{:.1f}".format((timer() - st)*1000.), "error": str(e)}

    st = timer()
    try:
        BaseService.get_by_id("x")
        res["database"] = {"database": CFG.DATABASE_TYPE.lower(), "status": "green","elapsed": "{:.1f}".format((timer() - st) * 1000.)}
    except Exception as e:
        res["database"] = {"database": CFG.DATABASE_TYPE.lower(), "status": "red",
                           "elapsed": "{:.1f}".format((timer() - st) * 1000.), "error": str(e)}


    return Result.succ(data=res)