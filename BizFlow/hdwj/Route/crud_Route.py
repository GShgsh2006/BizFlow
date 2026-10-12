#BizFlow 智能业务协作平台
#增删改查路由接口
from sqlalchemy.orm import Session
from BizFlow.hdwj.tool.Software_crud import gets,Employee_zs,add,add_Administrator,EmployeeSubmit
from fastapi import APIRouter,Depends
from BizFlow.shujuku.Management import get_db
from BizFlow.hdwj.tool.jx_token import get_current_user
from BizFlow.hdwj.function.crud_function import (query_hs,employee_query,
                                                 add_employee,add_gly,
                                                 employee_sh,query_sh,
                                                 gly_sh,delete_yg,cx_employee,all_stall)
router = APIRouter()
#查询
@router.get("/query")
async def query(name: str|None = None, task: str|None = None, db:Session=Depends(get_db)):
    data=query_hs(gets(name=name, task=task), db)
    return data
@router.get("/employee")
async def employee_ly(name: str|None = None, db:Session=Depends(get_db)):
    data=employee_query(Employee_zs(name=name), db)
    return data
#员工提交接口
@router.post("/Employee")
async def employee_tj(request: EmployeeSubmit, db:Session=Depends(get_db), token:dict=Depends(get_current_user)):
    jg=employee_sh(request, db)
    return jg

#管理员审核数据路由接口
@router.get("/query_sh_ly")
async def query_sh_ly(db:Session=Depends(get_db),token:dict=Depends(get_current_user)):
    data=query_sh(db,token)
    return data
#管理员是同意
@router.get("/gly_sh_ly/{task_id}")
async def gly_sh_ly(task_id:int,querya:str,db:Session=Depends(get_db),token: dict = Depends(get_current_user)):
    data=gly_sh(task_id,querya,db,token)
    return data
#添加
@router.post("/added")
async def added(request: add,db:Session=Depends(get_db)):
        data=add_employee(request,db)
        return data
@router.post("/added_cx/{id}")
async def added_cx(id:int,db:Session=Depends(get_db)):
       data=cx_employee(id,db)
       return data
#管理员分配任务
@router.put("/addgly")
async def addgly(request: add_Administrator,db:Session=Depends(get_db),token: dict = Depends(get_current_user)):
        data=add_gly(request,db,token)
        return data
#删除接口
@router.delete("/delete_ly/{id}")
async def delete_ly(id:int,db:Session=Depends(get_db)):
    data=delete_yg(id,db)
    return data
#管理员分配任务中能查询所有人的姓名下拉框
#注意：路由函数不要命名为 all_stall，否则会遮蔽从 crud_function 导入的同名函数，
#变成「自己调自己」无限递归。查询用 GET。
@router.get("/all_stall")
async def get_all_stall(db:Session=Depends(get_db)):
    data=all_stall(db)
    return data