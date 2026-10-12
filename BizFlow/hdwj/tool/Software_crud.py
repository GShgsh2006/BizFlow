
#crud的添加和输出模板
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy.orm import Session

#查询模板（函数）
class gets(BaseModel):
    name: str |None= None
    task: str |None= None

#员工展示模板(函数)
class Employee_zs(BaseModel):
    name: str |None= None

#员工添加任务模板(员工自己)
class add(BaseModel):
    id : int =Field(...)
    name: str =Field(...)
    name_rw: str =Field(...)
    task: str =Field(...)
    status: str =Field(...)#完成状态
    progress: int =Field(...)
#分配任务（管理员）
class add_Administrator(BaseModel):
    name: str =Field(...)
    Deadline:datetime =Field(...)
    content:str =Field(...)
    assignee:int =Field(...)#接收接收人id
    amount:int =Field(...)

#员工提交审核接口
# id/name 由前端根据当前登录人自动带出（只读框），task_name 从下拉框选择，content 为员工填写内容
class EmployeeSubmit(BaseModel):
    id:int =Field(...)
    name: str =Field(...)
    task_name: str =Field(...)
    content:str =Field(...)


