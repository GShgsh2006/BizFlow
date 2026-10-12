#LangHraph文件路由输入模板
from pydantic import BaseModel,Field


class appskk(BaseModel):
    request: str=Field(...)
