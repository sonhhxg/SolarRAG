import re
from datetime import datetime
from loguru import logger
from fastapi import APIRouter

from solargs.api import settings
from solargs._private.config import Config

from solargs.api.model import RetCode
from solargs.api.apps.db import UserTenantRole,FileType
from solargs.api.apps.openapi.api_view_model import Result
from solargs.api.apps.user.request.request import UserRequest

from solargs.services.api_service.user_service import UserService,TenantService, UserTenantService
from solargs.services.api_service.llm_service import TenantLLMService,LLMService
from solargs.services.api_service.file_service import FileService
from solargs.api.utils import (
    get_uuid,
    get_format_time,
    decrypt,
    download_img,
    current_timestamp,
    datetime_format,
    bs64_encoded
)


CFG = Config()
router = APIRouter()

def user_register(user_id, user):
    user["id"] = user_id
    tenant = {
        "id": user_id,
        "name": user["nickname"] + "‘s Kingdom",
        "llm_id": settings.CHAT_MDL,
        "embd_id": settings.EMBEDDING_MDL,
        "asr_id": settings.ASR_MDL,
        "parser_ids": settings.PARSERS,
        "img2txt_id": settings.IMAGE2TEXT_MDL,
        "rerank_id": settings.RERANK_MDL,
    }
    usr_tenant = {
        "tenant_id": user_id,
        "user_id": user_id,
        "invited_by": user_id,
        "role": UserTenantRole.OWNER,
    }
    file_id = get_uuid()
    file = {
        "id": file_id,
        "parent_id": file_id,
        "tenant_id": user_id,
        "created_by": user_id,
        "name": "/",
        "type": FileType.FOLDER.value,
        "size": 0,
        "location": "",
    }
    tenant_llm = []
    for llm in LLMService.query(fid=settings.LLM_FACTORY):
        tenant_llm.append(
            {
                "tenant_id": user_id,
                "llm_factory": settings.LLM_FACTORY,
                "llm_name": llm.llm_name,
                "model_type": llm.model_type,
                "api_key": settings.API_KEY,
                "api_base": settings.LLM_BASE_URL,
                "max_tokens": llm.max_tokens if llm.max_tokens else 8192
            }
        )

    if not UserService.save(**user):
        return

    TenantService.insert(**tenant)
    UserTenantService.insert(**usr_tenant)
    TenantLLMService.insert_many(tenant_llm)
    FileService.insert(file)
    return UserService.query(email=user["email"])

@router.post("/user/register")
def user_add(user:UserRequest):
    email_address = user.email
    if not re.match(r"^[\w\._-]+@([\w_-]+\.)+[\w-]{2,5}$", email_address):
        return Result.failed(
            message=f"Invalid email address: {email_address}!",
            code=RetCode.DATA_ERROR.value,
        )
    if UserService.query(email=email_address):
        return Result.failed(
            message=f"Email: {email_address} has already registered!",
            code=RetCode.DATA_ERROR.value,
        )
    user_dict = {
        "access_token": get_uuid(),
        "email": email_address,
        "nickname": user.nickname,
        "password": bs64_encoded(user.password),
        "login_channel": "password",
        "last_login_time": get_format_time(),
        "is_superuser": False,
    }
    # logger.info(f"user_dict:{user_dict}")

    user_id = get_uuid()
    try:
        users = user_register(user_id, user_dict)

        if not users:
            raise Exception(f"Fail to register {email_address}.")
        if len(users) > 1:
            raise Exception(f"Same email: {email_address} exists!")
        user = users[0]
        # logger.info(f"user:{user.to_json()}")
        return Result.succ(
            data=user.to_json(),
            message=f"{user.nickname}, welcome aboard!",
        )
    except Exception as e:
        return Result.failed(
            message=f"User registration failure, error: {str(e)}",
            code=RetCode.EXCEPTION_ERROR.value,
        )


@router.post("/user/login")
def login(user:UserRequest):
    """
    User login endpoint.
    ---
    tags:
      - User
    parameters:
      - in: body
        name: body
        description: Login credentials.
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: User email.
            password:
              type: string
              description: User password.
    responses:
      200:
        description: Login successful.
        schema:
          type: object
      401:
        description: Authentication failed.
        schema:
          type: object
    """
    # if not request.json:
    #     return Result.failed(
    #         data=False, code=settings.RetCode.AUTHENTICATION_ERROR, message="Unauthorized!"
    #     )

    email = user.email
    users = UserService.query(email=email)
    if not users:
        return Result.failed(
            code=settings.RetCode.AUTHENTICATION_ERROR,
            message=f"Email: {email} is not registered!",
        )

    try:
        password = bs64_encoded(user.password)
    except BaseException:
        return Result.failed(code=settings.RetCode.SERVER_ERROR, message="Fail to crypt password"
        )

    user = UserService.query_user(email, password)
    if user:
        response_data = user.to_json()
        user.access_token = get_uuid()
        # login_user(user)
        user.update_time = (current_timestamp(),)
        user.update_date = (datetime_format(datetime.now()),)
        user.save()
        msg = "Welcome back!"
        return Result.succ(data={"user":response_data,"auth":user.get_id()}, message=msg)
    else:
        return Result.failed(
            code=RetCode.AUTHENTICATION_ERROR,
            message="Email and password do not match!",
        )