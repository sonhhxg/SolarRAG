import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html

# fastapi import time cost about 0.05s
from fastapi.staticfiles import StaticFiles
from loguru import logger

from solargs._private.config import Config
from solargs.api import settings
from solargs.core.custom_logging import init_logging
from solargs.core.event_handlers import start_app_handler, stop_app_handler
from solargs.api.middlewares import CorrelationMiddleware, ProcessTimeHeaderMiddleware


CFG = Config()

init_logging()
settings.init_settings()

sys.tracebacklimit = 3  #
logger.add(str(CFG.LOG_FILE), rotation="100 MB", backtrace=False)
logger.add(str(CFG.PROJECT_DIR / "logs/solargs_error.log"), level="ERROR", rotation="50 MB", backtrace=False)

app = FastAPI(
    title="SOLARGS OPEN API",
    description="This is solargs, with auto docs for the API and everything",
    version="0.5.0",
    openapi_tags=[],
)

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)

static_file_path = os.path.join(ROOT_PATH, "solargs", "api/apps/static")
# logger.info(f'static_file_path:{static_file_path}')



@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Custom Swagger UI",
        swagger_js_url="/swagger_static/swagger-ui-bundle.js",
        swagger_css_url="/swagger_static/swagger-ui.css",
    )




def mount_routers(app: FastAPI):
    # ��Ӿ�̬�ļ�
    app.mount(
        "/swagger_static",
        StaticFiles(directory=static_file_path),
        name="swagger_static",
    )
    # ���ӿ����м��
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    """Lazy import to avoid high time cost"""
    from solargs.api.apps.knowledge.api import router as knowledge_router
    from solargs.api.heartbeat import health_router
    from solargs.api.apps.openapi.api_v1.api_v1 import router as api_v1
    from solargs.api.apps.llm_manage.api import router as llm_manage_api
    from solargs.api.apps.embeddings.api import router as embeddings_api
    from solargs.api.apps.system.api import router as system_api
    from solargs.api.apps.db.api import router as db_router
    from solargs.api.apps.kb.api import router as kb_router
    from solargs.api.apps.user.api import router as user_router
    from solargs.api.apps.document.api import router as document_router



    app.include_router(user_router, prefix=f"/api/{CFG.API_VERSION}", tags=["User"])
    app.include_router(system_api, prefix=f"/api/{CFG.API_VERSION}", tags=["System"])
    app.include_router(kb_router, prefix=f"/api/{CFG.API_VERSION}", tags=["Knowledge Base"])
    app.include_router(document_router, prefix=f"/api/{CFG.API_VERSION}", tags=["Document"])
    app.include_router(db_router, prefix=f"/api/{CFG.API_VERSION}", tags=["Database"])
    app.include_router(llm_manage_api, prefix=f"/api/{CFG.API_VERSION}", tags=["LLM Manage"])

    app.include_router(api_v1, prefix=f"/api/{CFG.API_VERSION}", tags=["Chat"])
    app.include_router(embeddings_api, prefix=f"/api/{CFG.API_VERSION}", tags=["Embeddings"])
    app.include_router(knowledge_router,prefix=f'/api/{CFG.API_VERSION}', tags=["Knowledge"])

    app.include_router(health_router, prefix="/health")

    # add lifespan event handler
    app.add_event_handler("startup", start_app_handler(app))
    app.add_event_handler("shutdown", stop_app_handler(app))

    if CFG.DEBUG:
        app.add_middleware(CorrelationMiddleware)
        app.add_middleware(ProcessTimeHeaderMiddleware)


def run_webserver():
    print(r"""
     _____         _                          
    /  ___|       | |                         
    \ `--.   ___  | |  __ _  _ __   __ _  ___ 
     `--. \ / _ \ | | / _` || '__| / _` |/ __|
    /\__/ /| (_) || || (_| || |   | (_| |\__ \
    \____/  \___/ |_| \__,_||_|    \__, ||___/
                                    __/ |     
                                   |___/      
            """, flush=True)
    mount_routers(app)
    return app

app = run_webserver()

if __name__ == "__main__":
    run_webserver()
