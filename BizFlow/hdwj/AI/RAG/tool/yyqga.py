# BizFlow 智能业务协作平台
# RAG 语义切割 + 本地 embedding

import os

# 强制离线：模型已下载到本地，禁止 huggingface_hub 联网检查元数据。
# 否则即便模型已缓存，sentence-transformers 仍会发 HEAD 请求去 HuggingFace
# 校验文件，连不通就报 WinError 10060 超时并不断重试。
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings


class LocalEmbeddings(Embeddings):
    def __init__(self, model_name=None):
        # 优先读本地路径(可用 TEXT2VEC_MODEL_PATH 指定)，否则用模型 id 从本地缓存离线加载
        model_name = model_name or os.getenv("TEXT2VEC_MODEL_PATH", "shibing624/text2vec-base-chinese")
        self.model = SentenceTransformer(model_name, local_files_only=True)

    def embed_documents(self, texts):
        vectors = self.model.encode(texts, normalize_embeddings=True)
        return vectors.tolist()

    def embed_query(self, text):
        vector = self.model.encode([text], normalize_embeddings=True)
        return vector[0].tolist()


# 惰性初始化：模型和切割器在首次真正使用时才加载，避免 import 阶段就触发下载/连接超时
_emnn = None
_parent_splitter = None


def get_embeddings():
    """返回全局缓存的 embedding 实例，避免每次检索都重新加载模型。"""
    global _emnn
    if _emnn is None:
        _emnn = LocalEmbeddings()
    return _emnn


def _get_parent_splitter():
    global _parent_splitter
    if _parent_splitter is None:
        # SemanticChunker 在 langchain 1.x 已移除，这里用递归字符切割器做父块划分
        _parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", "?", "！", "。", " ", ""],
        )
    return _parent_splitter


def load_embedding_model():
    """在应用生命周期(lifespan)中调用，预热加载 embedding 模型与切割器。"""
    get_embeddings()
    _get_parent_splitter()
    return True


async def rag_yyqg_dg(request):
    """
    request: LangChain Document 列表（粗切割结果）
    返回：进一步切分后的父块 Document 列表
    """
    return _get_parent_splitter().split_documents(request)
