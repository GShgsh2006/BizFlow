#BizFlow 智能业务协作平台
#RAG关键字查询
from rank_bm25 import BM25Okapi
import jieba
class BM25:
    def __init__(self,request:list):
        self.Semantic_Chunk= request
        self.documents_doc = [(list(jieba.cut(doc.page_content)))
            for doc in self.Semantic_Chunk
        ]
        self.BM25 = BM25Okapi(self.documents_doc)
    def kh(self,request:str,fh:int=3):
        kh_wt=list(jieba.cut(request))
        kh_bm25 =self.BM25.get_scores(kh_wt)
        # 返回 (父块索引, 分数) 列表，按分数降序，供上层做 RRF 融合
        bm25_px=sorted(enumerate(kh_bm25),key=lambda x:x[1],reverse=True)
        return bm25_px[:fh]



