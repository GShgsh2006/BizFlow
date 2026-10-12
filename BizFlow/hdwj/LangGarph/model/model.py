from langchain_ollama import ChatOllama
from BizFlow.hdwj.LangGarph.tool.tools import tools
from langgraph.prebuilt import ToolNode
model = ChatOllama(
    model="qwen3:4b",
    temperature=0.7,

)

_tool_node = ToolNode(tools)
_model_with_tools = model.bind_tools(tools)     # ← 不再用 global

