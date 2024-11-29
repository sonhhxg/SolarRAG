from pydantic import BaseModel


class DocUploadRequest(BaseModel):
    """query: knowledge query"""
    id: str = None
    kb_id: str = None
    name: str = "test"

class DocInfosdRequest(BaseModel):
    """query: knowledge query"""
    id: str = "989d2551ab0611efb1580242ac120006"
    doc_ids: list = ["b6f11a7dab9111efaa090242ac120006","b6e33c42ab9111ef990a0242ac120006"]

class DocThumbnailsRequest(BaseModel):
    """query: knowledge query"""
    id: str = "989d2551ab0611efb1580242ac120006"
    doc_ids: str = "b6f11a7dab9111efaa090242ac120006,b6e33c42ab9111ef990a0242ac120006"