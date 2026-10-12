#BizFlow 智能业务协作平台
#工资结算路由

from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from BizFlow.shujuku.Management import get_db
from BizFlow.hdwj.function.Salary_hs import salary
from BizFlow.hdwj.tool.jx_token import get_current_user
router_gz = APIRouter()

#注意：路径里声明的是 {id}，函数参数也必须叫 id。
#以前函数参数写成 ids，FastAPI 会把它当成必填的「查询参数」，
#于是 /salary/2 固定报 422，而 /salary?ids=2 又匹配不到路径。
@router_gz.get('/salary/{id}')
def add_employee(id:int, db:Session=Depends(get_db), token:dict=Depends(get_current_user)):
    if token["role"] != "董事长" and token["id"] != id:
        raise HTTPException(status_code=403, detail="只能查询自己的工资")
    gz=salary(id,db)
    return gz



