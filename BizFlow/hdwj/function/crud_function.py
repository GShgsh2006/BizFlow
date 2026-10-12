#BizFlow 智能业务协作平台
#crud函数接口
from BizFlow.hdwj.tool.Software_crud import gets,Employee_zs,add,add_Administrator,EmployeeSubmit
from BizFlow.shujuku.user import task,users,employees,yg_tjs,notice
from fastapi import  HTTPException, status
from sqlalchemy.orm import Session

#查询
def query_hs(a:gets,db:Session):
     if a.name:
         uid = db.query(users.id).filter(users.name == a.name).scalar()
         if not uid:
             raise HTTPException(status_code=404, detail=f"{a.name}还不是公司员工")
         query=db.query(task).filter(task.assignee_id==uid).all()
         if query:
            return query
         else:
            raise HTTPException(status_code=404,
                             detail=f"{a.name}还没有任何任务哦")

     elif a.task:
         query=db.query(task).filter(task.name==a.task).all()
         if query:
             return query
         else:
             raise HTTPException(status_code=404,
                                 detail=f"{a.task}任务还没有分配给让任何人或者还没有创建该任务")
     else:
         raise HTTPException(status_code=404,


                     detail="请输入正确的任务名字或者人物名字哦")


#管理员审核任务数据
def query_sh(db:Session,token:dict):
    if token["role"]=="董事长":
        db=db
        shuju=db.query(yg_tjs).filter(yg_tjs.zt=="审核中").all()
        return shuju
    else:
        raise HTTPException(status_code=403,detail="你还无权访问！")



# 管理员是否同意
def gly_sh(
    task_id: int,
    query: str,
    db: Session,
    token: dict
):
    if token["role"] != "董事长":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您无权访问该接口"
        )
    query = query.strip()
    status_map = {
        "通过审核": ("审核通过", "已完成"),
        "审核不通过": ("审核未通过", "审核未通过"),
    }
    if query not in status_map:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的审核指令"
        )

    shuju = db.query(yg_tjs).filter(yg_tjs.id == task_id).first()
    if not shuju:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到对应的任务记录"
        )

    task_rw = db.query(task).filter(task.name == shuju.name_rw).first()
    if not task_rw:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="关联的主任务不存在"
        )

    new_zt, new_status = status_map[query]
    shuju.zt = new_zt
    task_rw.status = new_status


    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="数据库更新失败，请稍后重试"
        )
    return {"message": query}

#员工提交提交审核接口
#我们在写vue的时候这个要根据token自动将人物的id和name传入这个页面中并且是固定的
def employee_sh(a:EmployeeSubmit,db:Session):
    tj=yg_tjs(
        name=a.name,
        name_rw=a.task_name,
        content=a.content,
        assignee_id=a.id,
        zt="审核中"
    )
    try:
        db.add(tj)
        db.commit()
        return {"message": "提交审核成功"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500,detail="提交接口失败")


# #员工信息函接口
def employee_query(a:Employee_zs,db:Session):
    db=db
    if a.name:
        uid = db.query(users.id).filter(users.name == a.name).scalar()
        if not uid:
            raise HTTPException(status_code=404, detail=f"{a.name}还不是公司员工")
        query=db.query(task).filter(task.assignee_id==uid).all()
        if query:
            return query
        else:
            raise HTTPException(status_code=404,
                                detail="他现在还没有任何任务哦！")
    else:
        query_rw=db.query(users.id,users.name,users.employee_ID,users.position).all()
        n=[]
        if query_rw:
                return [{"id":i.id,"name":i.name,"employee_ID":i.employee_ID,"position":i.position} for i in query_rw]

        else:
            raise HTTPException(status_code=404
                                ,detail="数据库中还没有任何人物哦")

#数据添加接口（员工自己添加的任务）
#一条提交就是一行记录，同一个人可以建多条。
#a.id 是登录人 id，用它反查 user 表拿到权威姓名，避免前端篡改 name 导致归属错乱；
#employee.id 保持自增，只当任务行号用，不再当人 id 用。
def add_employee(a:add,db:Session):
    yg = db.query(users).filter(users.id == a.id).first()
    if not yg:
        raise HTTPException(status_code=400,detail="登录人 id 不存在，请重新登录")

    rw = employees(
        name=yg.name,
        name_rw=a.name_rw,
        content=a.task,
        status=a.status,
        progress=a.progress,
    )
    try:
        db.add(rw)
        db.commit()
        db.refresh(rw)
        return {"message":"添加任务完成","id":rw.id}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400,detail="添加任务失败，请稍后重试")

#自建任务查询函数
#路由 id 是登录人 id，通过 user.name 关联到 employee.name，查出本人名下的全部任务。
def cx_employee(id:int,db:Session):
    answer=(db.query(employees)
            .join(users, users.name == employees.name)
            .filter(users.id == id)
            .all())
    return answer
#董事长分配任务
def add_gly(a:add_Administrator,db:Session,token:dict):
    if token["role"] != "董事长":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您无权访问该接口"
        )
    else:
        add_rw=task(
           name=a.name,
           Deadline=a.Deadline,
           content=a.content,
           assignor="董事长（管理员）",
           assignee_id=a.assignee,
           status="待完成",
           amount=a.amount
        )
        assignee_name = db.query(users.name).filter(users.id == a.assignee).scalar()
        if not assignee_name:
            raise HTTPException(status_code=404, detail="找不到对应的接收人")
        Read=notice(
            name_id=a.assignee,
            name=a.name,
            assignee=assignee_name,
            Read="未读"
        )
        try:
            db.add(add_rw)
            db.add(Read)
            db.commit()
            return "分配任务完成"
        except Exception:
            db.rollback()
            raise HTTPException(status_code=400, detail="获取不到数据")
#删除接口(删除员工自己创造的任务)
#id 是 employee 表的任务行号（cx_employee 返回的 item.id），不是登录人 id。
def delete_yg(id:int,db:Session):
        yg = db.query(employees) \
            .filter(employees.id == id) \
            .first()
        if not yg:
            raise HTTPException(status_code=404, detail="该任务不存在")
        try:
            db.delete(yg)
            db.commit()
            return "删除成功"
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"删除失败了原因是：{e}")


#显示所有员工表
#管理员分配任务中能查询所有人的姓名下拉框
#返回 [{"id": 用户id, "name": 姓名}]，前端下拉框选中后直接把 id 赋给 assignee_id
def all_stall(db:Session):
    rows=db.query(users.id,users.name).all()
    return [{"id": uid, "name": name} for uid, name in rows]
