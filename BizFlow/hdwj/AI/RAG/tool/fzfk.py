#BizFlow 智能业务协作平台
#RAG父子分块

from fastapi import HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

# 配置日志
logger = logging.getLogger(__name__)


async def fzqk(request):
    try:
        qg = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
        xh = []
        zk = []
        for idx, text in enumerate(request):
            fk_qg = qg.split_documents([text])
            for doc in fk_qg:
                zk.append(doc.page_content)
                xh.append(idx)
        return {"xh": xh, "zk": zk}
    except Exception as e:
        logger.error(f"父子分块处理失败: {str(e)}", exc_info=True)

        raise HTTPException(
            status_code=500,
            detail=f"分块失败: {str(e)}" 
        )


