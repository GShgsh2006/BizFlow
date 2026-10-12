#BizFlow 智能业务协作平台
#RAG向量查询
from BizFlow.hdwj.AI.RAG.tool.yyqga import get_embeddings
from BizFlow.hdwj.AI.RAG.tool import database
from langchain_chroma import Chroma
from BizFlow.hdwj.AI.RAG import file_interoperability
async def xlcx(request:str):
    emn=get_embeddings()
    db=Chroma(
        collection_name="employee_manual",
        embedding_function=emn,
        persist_directory=database._db_dir
    )
    retriever = db.as_retriever(search_kwargs={"k": 20})
    vector_results = retriever.invoke(request)
    seg=file_interoperability.semantic_segmentation
    xlcx_zd={}
    for text in vector_results[:10]:
        flid=text.metadata.get("idx")
        if flid is None or seg is None or flid < 0 or flid >= len(seg):
            continue
        # 子块 metadata['idx'] 指向父块索引，映射回父块正文；
        # 用父块索引做 key，多个子块指向同一父块时自动去重并保留最高排名。
        xlcx_zd[flid]=seg[flid].page_content

    return xlcx_zd
