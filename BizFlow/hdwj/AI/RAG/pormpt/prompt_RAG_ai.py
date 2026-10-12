#BizFlow 智能业务协作平台
#prompt工程
from langchain_core.prompts import ChatPromptTemplate

Prompts = ChatPromptTemplate.from_messages([
    (
        "system",
        "你是一个企业问答助手，你的职责是根据客户的问题进行细心回答，"
        "并且要根据我给你的知识点进行检索回答"
        "并且你要根据我给你传的记忆进行思考"
    ),
    (
        "human",
        "你要拥有的记忆：{jiyi}\n"
        "参考知识点是：{zsd}\n"
        "客户的问题是：{request_ku}"
    )
])




