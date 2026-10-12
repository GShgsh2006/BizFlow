#工具类实现员工信息查询
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from BizFlow.shujuku.user import yynj
@tool
def yyxx(name:str,config:RunnableConfig):
    """根据员工姓名查询其年假剩余天数。"""
    db = config["configurable"]["db"]
    token_zw = config["configurable"]["token_zw"]
    token_id = config["configurable"]["token_id"]
    if token_zw == "董事长":
        nj=db.query(yynj.days).filter(yynj.name==name).scalar()
        if nj is not None:
            return f"{name} 的年假剩余天数为 {nj} 天"
        return f"数据库中没有 {name} 的年假记录"
    else:
        name_id = db.query(yynj.name).filter(yynj.id == token_id).scalar()
        if name_id!=name:
            raise HTTPException(status_code=500,detail="你只能访问自己的数据，无权访问别人的数据")
        else:
            nj = db.query(yynj.days).filter(yynj.id==token_id).scalar()
            if nj is not None:
                return f"{name} 的年假剩余天数为 {nj} 天"
            return f"数据库中没有 {name} 的年假记录"

##工具类实现员工工资查询
from BizFlow.shujuku.user import users,task
from fastapi import HTTPException

@tool
def salary(ids:int,config:RunnableConfig):
    """根据员工 id 查询其已完成任务的工资总额。"""
    db = config["configurable"]["db"]
    token_zw=config["configurable"]["token_zw"]
    token_id=config["configurable"]["token_id"]
    if token_zw=="董事长":
        name=db.query(users.name).filter(users.id == ids).scalar()
        if name:
            renwu=db.query(task).filter(task.assignee_id == ids,task.status=="已完成").all()
            Salary=sum([i.amount for i in renwu])
            return f"{name} 的工资总额为 {Salary} 元"
        else:
            raise HTTPException(status_code=404,detail="数据库中找不到名字请重新输入")
    else:
        if token_id!=ids:
            return "你只能查询你自己的工资，无权查看别人的工资!"
        else:
            name = db.query(users.name).filter(users.id == ids).scalar()
            if name:
                renwu = db.query(task).filter(task.assignee_id == ids, task.status == "已完成").all()
                Salary = sum([i.amount for i in renwu])
                return f"{name} 的工资总额为 {Salary} 元"
            else:
                raise HTTPException(status_code=404, detail="数据库中找不到名字请重新输入")



@tool
def distribute(rename:str,rwname:str,tasks:str,time:str,amount:int,config:RunnableConfig):
    """把任务分配给指定员工：rename 员工姓名，rwname 任务名，tasks 任务内容，time 截止时间，amount 金额。"""
    db = config["configurable"]["db"]
    token_zw = config["configurable"]["token_zw"]
    if token_zw == "董事长":
        uid = db.query(users.id).filter(users.name==rename).scalar()
        if uid:
            new_task = task(
                name=rwname,
                Deadline=time,
                content=tasks,
                assignor="董事长",
                assignee_id=uid,
                status="未完成",
                amount=amount
            )
            db.add(new_task)
            db.commit()
            return f"已把任务「{rwname}」分配给 {rename}"
        else:
            raise HTTPException(
                status_code=404,
                detail="数据库中没有此人物"
            )
    else:
        raise HTTPException(status_code=500,detail="你无权使用这个能力")
tools = [
    salary, yyxx, distribute
]