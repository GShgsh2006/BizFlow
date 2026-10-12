#BizFlow 智能业务协作平台
#员工接受任务（已读未读表）
from sqlalchemy.orm import Session
from BizFlow.shujuku.user import notice, task,users

from fastapi import Depends, HTTPException
import logging


def notice_wd(db: Session, token: dict ):
    if token["role"] == "员工":
        try:
            unread_list = db.query(notice).filter(
                notice.Read == "未读",
                notice.assignee == token["Full_Name"]
            ).all()

            #显式拼字典，不要直接返回 ORM 对象：
            #否则模型里新加的列（比如 name_id）会一起漏给前端，两个分支结构也不一致。
            rw = [
                {
                    "id": i.id,
                    "name": i.name,
                    "assignee": i.assignee,
                    "Read": i.Read,
                }
                for i in unread_list
            ]

            if rw:
                logging.info("返回未读列表，共 %d 条", len(rw))
                return {"notifications": rw}
            else:
                return {"message": "您暂无未读信息"}
        except Exception as e:
            logging.error("查询未读通知失败: %s", str(e))
            raise HTTPException(status_code=500, detail="查询未读信息失败")
    elif token["role"] == "董事长":
        try:
            unread_list = db.query(notice).filter(
                notice.Read == "未读",
            ).all()

            #notice 表只有 id / name(任务名) / assignee(接收人) / Read(状态) 这四列，
            #压根没有 name_id，写 i.name_id 会直接 AttributeError，
            #再被下面的 except 吃掉，就变成 500「查询未读信息失败」。
            #这里显式拼成和「员工」分支一样的 {notifications: [...]}，
            #前端只认一种结构，也顺带把接收人带出去。
            rw = [
                {
                    "id": i.id,
                    "name": i.name,
                    "assignee": i.assignee,
                    "Read": i.Read,
                }
                for i in unread_list
            ]

            if rw:
                logging.info("返回未读列表，共 %d 条", len(rw))
                return {"notifications": rw}
            else:
                return {"message": "您暂无未读信息"}
        except Exception as e:
            logging.error("查询未读通知失败: %s", str(e))
            raise HTTPException(status_code=500, detail="查询未读信息失败")
    else:
        raise HTTPException(status_code=500,detail="数据库里没有定义该职位，你无权访问")

#判断未读是否变成已读
#传进来的是 task 表的任务 id（任务查询页点开哪条就传哪条）。
#notice 表里存的是任务名 + 接收人，所以先拿任务名，再按「任务名 + 接收人」定位通知行。
#token 传了的话就限定只能是自己的通知，避免同名任务把别人的通知也标成已读。
def judge(id:int, db: Session, token: dict | None = None):
    rw = db.query(task).filter(task.id == id).first()
    if not rw:
        raise HTTPException(status_code=404, detail="找不到这个任务")

    query = db.query(notice).filter(notice.name == rw.name)
    if token:
        query = query.filter(notice.assignee == token["Full_Name"])
    unread_list = query.first()

    if not unread_list:
        return {"message": "这条任务没有对应的通知"}
    if unread_list.Read == "未读":
        unread_list.Read = "已读"
        #原来这里少了 commit，session 一关就被回滚，所以一直是未读
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail="标记已读失败，请稍后重试")
        return {"message": "已标记为已读"}
    return {"message": "这条任务已经是已读"}




