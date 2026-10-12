#BizFlow 智能业务协作平台
#员工接受任务路由文件（已读未读表）
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from BizFlow.shujuku.Management import get_db
from BizFlow.hdwj.function.notice_hs import notice_wd, judge
from BizFlow.hdwj.tool.jx_token import get_current_user
router_notice=APIRouter()

#接受已读未读表
@router_notice.get("/notice_wd")
def notice_ly(db:Session=Depends(get_db) ,token=Depends(get_current_user)):
        a=notice_wd(db,token)
        return a

#点击任务看详情时调用：把这条任务对应的通知从「未读」改成「已读」
#task_id 是 task 表的主键（任务查询页列表里每条的 id）
@router_notice.get("/judge/{task_id}")
def judge_ly(task_id:int, db:Session=Depends(get_db), token=Depends(get_current_user)):
        return judge(task_id, db, token)
