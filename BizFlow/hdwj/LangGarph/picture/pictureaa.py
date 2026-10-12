##BizFlow 智能业务协作平台
# 图函数：把节点组装成 LangGraph 状态图
from langgraph.graph import StateGraph, START
from BizFlow.hdwj.LangGarph.tool.state import State
from BizFlow.hdwj.LangGarph.node.nodes import dall_model, judge
from BizFlow.hdwj.LangGarph.model.model import _tool_node


def _build_graph():
    g = StateGraph(State)
    g.add_node("ai", dall_model)
    g.add_node("tool", _tool_node)
    g.add_edge(START, "ai")
    # judge 返回 "tool" 或 END，直接作为路由目标
    g.add_conditional_edges("ai", judge)
    g.add_edge("tool", "ai")
    return g


_GRAPH = _build_graph().compile()


# 供 LangGarph/app.py 调用的入口：把数据库会话注入到工具的 configurable 里
def pictures(db,token:dict):
    name=token["role"]
    id=token["id"]
    config = {
        "configurable": {
            "db": db,
            "token_zw": name,
            "token_id": id  }}
    return _GRAPH, config
