#rag路由模板、
from pydantic import BaseModel, Field
from datetime import datetime
class add(BaseModel):
    premot:str=Field(...)
