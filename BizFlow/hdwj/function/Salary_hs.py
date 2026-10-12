#BizFlow 智能业务协作平台
#工资结算函数
from sqlalchemy.orm import Session
from BizFlow.shujuku.user import users,task
from fastapi import HTTPException
def salary(ids:int,db:Session):

    name=db.query(users.name).filter(users.id == ids).scalar()
    if name:
        renwu=db.query(task).filter(task.assignee_id == ids,task.status=="已完成").all()
        Salary=sum([i.amount for i in renwu])
        return Salary
    else:
        raise HTTPException(status_code=404,detail="数据库中找不到名字请重新输入")

