#BizFlow 智能业务协作平台
#RAG检索文件互通
from BizFlow.hdwj.AI.RAG.tool.cqg import cj,Rough_cut
from BizFlow.hdwj.AI.RAG.tool.yyqga import rag_yyqg_dg
from BizFlow.hdwj.AI.RAG.tool.fzfk import fzqk
from BizFlow.hdwj.AI.RAG.tool.database import shk
import logging
semantic_segmentation=None
async def file():
    global semantic_segmentation
    lj=cj("ys")
    cqgs=await Rough_cut(lj)
    seg=await rag_yyqg_dg(cqgs)
    parent_child=await fzqk(seg)
    await shk(parent_child["xh"],parent_child["zk"])
    # 向量库建好之后才发布 semantic_segmentation，
    # 否则 /ai 请求会在向量库未就绪时检索，报 collection 不存在。
    semantic_segmentation=seg
    logging.info("数据库存储完成")
    return "数据库存储完成"




