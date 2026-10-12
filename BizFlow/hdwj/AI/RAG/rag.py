#BizFlow 智能业务协作平台
#RAG 混合检索：BM25 关键字 + 向量语义，RRF 融合取 top2 父块
from BizFlow.hdwj.AI.RAG.tool.Keyword_Search import BM25
from BizFlow.hdwj.AI.RAG import file_interoperability
from BizFlow.hdwj.AI.RAG.tool.vector_search import xlcx


async def rag_b(request: str):
    seg = file_interoperability.semantic_segmentation
    if not seg:
        raise RuntimeError("知识库尚未初始化完成，请稍后重试")
    bm25 = BM25(seg)
    bm25_ku = bm25.kh(request)
    xlcxz = await xlcx(request)
    rrf = {}
    for rank, (idx, _score) in enumerate(bm25_ku):
        rrf[idx] = rrf.get(idx, 0.0) + 1.0 / (rank + 1)
    for rank, idx in enumerate(xlcxz.keys()):
        rrf[idx] = rrf.get(idx, 0.0) + 1.0 / (rank + 1)
    top = sorted(rrf.items(), key=lambda x: x[1], reverse=True)[:2]
    return [seg[idx].page_content for idx, _score in top]
