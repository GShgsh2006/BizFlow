#BizFlow 智能业务协作平台
#Agent大脑后端函数（SSE 流式返回）
import json

from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage

from BizFlow.hdwj.LangGarph.picture.pictureaa import pictures


async def apps(request: str, db: Session,token: dict):
    graph, config = pictures(db,token)
    # stream_mode="messages"：每个事件是 (message_chunk, metadata)
    async for chunk, metadata in graph.astream(
        {"messages": [HumanMessage(request)]},
        config=config,
        stream_mode="messages",
    ):
        # 只转发 ai 节点产出的文本，工具执行过程不对外输出
        node = metadata.get("langgraph_node") if isinstance(metadata, dict) else None
        if node != "ai":
            continue

        content = getattr(chunk, "content", "")
        if not content:
            continue

        payload = json.dumps(
            {"type": "content", "content": content},
            ensure_ascii=False,
        )
        yield f"data:{payload}\n\n"
