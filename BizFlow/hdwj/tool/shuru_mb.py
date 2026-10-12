
from pydantic import BaseModel, Field

class SignInRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)
    password: str = Field(..., min_length=3, max_length=20)

class SignUpRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)
    password: str = Field(..., min_length=3, max_length=20)
    employee_ID: int

    position: str = Field(..., min_length=1, max_length=30)  # 建议加上长度限制