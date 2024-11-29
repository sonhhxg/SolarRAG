
from solargs.api.apps.db.db_models import DB
from solargs.api.apps.db.db_models import LLM,LLMFactories,TenantLLM

from solargs.services.api_service.base_service import BaseService


class LLMFactoriesService(BaseService):
    model = LLMFactories


class LLMService(BaseService):
    model = LLM

class TenantLLMService(BaseService):
    model = TenantLLM

    @classmethod
    @DB.connection_context()
    def get_api_key(cls, tenant_id, model_name):
        arr = model_name.split("@")
        if len(arr) < 2:
            objs = cls.query(tenant_id=tenant_id, llm_name=model_name)
        else:
            objs = cls.query(tenant_id=tenant_id, llm_name=arr[0], llm_factory=arr[1])
        if not objs:
            return
        return objs[0]

    @classmethod
    @DB.connection_context()
    def get_my_llms(cls, tenant_id):
        fields = [
            cls.model.llm_factory,
            LLMFactories.logo,
            LLMFactories.tags,
            cls.model.model_type,
            cls.model.llm_name,
            cls.model.used_tokens
        ]
        objs = cls.model.select(*fields).join(LLMFactories, on=(cls.model.llm_factory == LLMFactories.name)).where(
            cls.model.tenant_id == tenant_id, ~cls.model.api_key.is_null()).dicts()

        return list(objs)

    @classmethod
    @DB.connection_context()
    def get_openai_models(cls):
        objs = cls.model.select().where(
            (cls.model.llm_factory == "OpenAI"),
            ~(cls.model.llm_name == "text-embedding-3-small"),
            ~(cls.model.llm_name == "text-embedding-3-large")
        ).dicts()
        return list(objs)