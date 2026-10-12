##BizFlow 智能业务协作平台
#节点函数
from langgraph.graph import END
from BizFlow.hdwj.LangGarph.model.model import _model_with_tools
from BizFlow.hdwj.LangGarph.tool.state import State


# 调用模型
def dall_model(state: State):
    request = state["messages"]
    answer = _model_with_tools.invoke(request)
    # 直接把模型返回的 AIMessage（含 tool_calls）放回 messages，
    # 不要再用 AIMessage(content=answer) 二次包裹，否则会把对象塞进 content
    return {"messages": [answer]}


# 判断是否需要使用 tool 工具
# 条件边的路由函数必须返回“下一个节点名”或 END（字符串），不能返回 dict
def judge(state: State):
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "tool"
    return END
