##BizFlow 智能业务协作平台
#登入和注册路由接口
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from BizFlow.shujuku.Management import get_db
from BizFlow.hdwj.tool.shuru_mb import SignInRequest, SignUpRequest
from BizFlow.hdwj.function.sign_in_ly import sign_up,sign_in,sign_yz
routers = APIRouter()

# 登入路由接口
@routers.post("/sign_in")
def sign_in_ly(data: SignInRequest, db: Session = Depends(get_db)):
    Result = sign_in(name=data.name, password=data.password, db=db)
    return Result

# 注册路由接口
@routers.post("/sign_up")
def sign_up_ly(data: SignUpRequest, db: Session = Depends(get_db)):
    Result = sign_up(name=data.name, password=data.password, employee_id=data.employee_ID
                     , position=data.position, db=db)
    return Result
#董事长验证页面
@routers.post("/sign_up_yz")
def sign_ly_yz(data: SignUpRequest,yz:str, db: Session = Depends(get_db)):
    Result = sign_yz(name=data.name, password=data.password, employee_id=data.employee_ID
                     , position=data.position,yz=yz, db=db)
    return Result