#BizFlow 智能业务协作平台
#RAG粗切割
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_community.document_loaders import TextLoader
def cj(wj):
    lj=os.path.dirname(os.path.abspath(__file__))
    ydlj=os.path.dirname(lj)
    return os.path.join(ydlj,wj)

async def Rough_cut(request):
    file_path=cj(request)
    qg_wj=TextLoader(
        file_path,
        encoding="utf-8"
    )
    qg_road=qg_wj.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", "?", "！", "。", " ", ""],
        length_function=len
    )
    llm_qg=text_splitter.split_documents(qg_road)
    return llm_qg
