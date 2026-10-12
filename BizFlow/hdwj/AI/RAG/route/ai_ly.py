#BizFlow 智能业务协作平台
#调用RAG路由文件
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from BizFlow.shujuku.Management import get_db
from BizFlow.hdwj.AI.RAG.model import call_ai,ai_cx
from BizFlow.hdwj.tool.rag import add
from sqlalchemy.orm import Session
from fastapi import Depends
import time
routerk=APIRouter()

last_request_time = {}

@routerk.post('/ai/{id}')
async def ai(
    request: add,
    id: int,
    db: Session = Depends(get_db)
):
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
        call_ai(request.premot, id, db),
        media_type="text/event-stream",
        headers={"X-Accel-Buffering": "no"}
    )
#访问ai页面展示ai记录
@routerk.get('/ai_jl/{id}')
def ai_jl(
        id:int,db:Session=Depends(get_db)
):
    return [{"HumanMessage":i.HumanMessage,"AIMessage":i.AIMessage} for i in ai_cx(db,id)]