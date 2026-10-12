#BizFlow 智能业务协作平台
#调用ai模型实现RAG检索
from langchain_ollama import ChatOllama
from sqlalchemy.orm import Session
from BizFlow.hdwj.AI.RAG.rag import rag_b
from BizFlow.hdwj.AI.RAG.pormpt.prompt_RAG_ai import Prompts
import json
from BizFlow.shujuku.user import ai_jl
llm = ChatOllama(
    model="qwen3:1.7b",
    base_url="http://localhost:11434",
    temperature=0.7,
    reasoning=True
)

async def call_ai(
        user_question: str,rw_id:int,db:Session
):
    """
    system_role:
        AI角色设定

    user_question:
        用户输入的问题
    """
    rag=await rag_b(user_question)
    # 记忆直接从库里按登录人 id 取（最近 10 条），不再依赖 ai_ly 的模块级全局 a：
    # 全局是所有请求共享的，多个人同时用会互相串号
    aijiyi= [
        {"HumanMessage":i.HumanMessage,"AIMessage":i.AIMessage}
        for i in ai_cx(db,rw_id)
    ]

    # 创建调用链
    chain = Prompts|llm

    # 调用模型
    answer_parts = []
    async for chunk in chain.astream({
        "jiyi":aijiyi,
        "zsd": rag,
        "request_ku": user_question
    }):

        # 1. 思考过程
        reasoning = chunk.additional_kwargs.get("reasoning_content", "")
        if reasoning:
            yield f"data: {json.dumps({'type': 'thinking', 'content': reasoning}, ensure_ascii=False)}\n\n"

        # ChatOllama 的 content 是 str；判一下类型，
        # 避免多模态返回 list 时把它当字符串拼
        if isinstance(chunk.content, str) and chunk.content:
                answer_parts.append(chunk.content)
                yield f"data: {json.dumps({'type': 'answer', 'content': chunk.content}, ensure_ascii=False)}\n\n"

    # 一次问答只落一行。原来把 db.add/commit 写在循环里，
    # 每吐一个 token 就插一行，ai_jl 历史会被切成一堆碎片。
    db.add(ai_jl(name_id=rw_id, HumanMessage=user_question, AIMessage="".join(answer_parts)))
    db.commit()

    yield "data: [DONE]\n\n"

#查询ai记录函数
def ai_cx(db:Session,name_id:int):
    # 取最近 10 条，再翻成时间正序，直接当对话上下文用
    rows = (
        db.query(ai_jl)
        .filter(ai_jl.name_id == name_id)
        .order_by(ai_jl.id.desc())
        .limit(10)
        .all()
    )
    rows.reverse()
    return rows


