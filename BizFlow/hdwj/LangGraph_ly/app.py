#BizFlow 智能业务协作平台
#Agent大脑路由函数
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse
from BizFlow.hdwj.tool.LangGraph import appskk
from BizFlow.shujuku.Management import get_db
from BizFlow.hdwj.tool.jx_token import get_current_user
from BizFlow.hdwj.LangGarph.app import apps
import time
routeragent=APIRouter()
last_request_time = {}
#token 必须用 Depends 注入。直接写 token:dict，FastAPI 会把它当成「第二个请求体字段」，
#于是 /agent 要求 body 变成 {"a": {...}, "token": {...}}，前端发 {request} 直接 422。
@routeragent.post("/agent")
async def chat(a:appskk, token:dict=Depends(get_current_user),db: Session = Depends(get_db)):
    now = time.time()

    last_time = last_request_time.get("ids")

    if last_time is not None:
        if now - last_time < 1:
            raise HTTPException(
                status_code=429,
                detail="请求过于频繁"
            )

    # 记录本次请求时间
    last_request_time["ids"] = now

    return StreamingResponse(
            apps(a.request, db,token),
            media_type="text/event-stream"
        )

