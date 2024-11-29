from langchain_community.embeddings import OllamaEmbeddings
from solargs.api.apps.embeddings.request.request import EmbeddingRequest


class EmbeddingService:
    """DatabaseService
    """
    def __init__(self):
        pass
    def embedding_for_prompt(self,request:EmbeddingRequest):
        oembed = OllamaEmbeddings(base_url=request.url, model=request.model)
        return {"embeddings":oembed.embed_query(request.prompt)}

