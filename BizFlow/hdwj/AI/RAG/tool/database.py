#BizFlow 智能业务协作平台
#数据库存储（ChromaDB）
import os
import chromadb
from BizFlow.hdwj.AI.RAG.tool.yyqga import get_embeddings
# 数据库目录建在 RAG 下，与 ys 同级
_db_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "chroma"
)

client = None

async def shk(idx, text):
    global client
    client = chromadb.PersistentClient(path=_db_dir)

    collection_name = "employee_manual"

    # 每次启动都重建向量库：知识库文本是静态的，重建很快；
    # 若复用旧数据，一旦上游切割逻辑变化，旧向量里 metadata["idx"]
    # 会指向错误的父块索引，导致检索牛头不对马嘴。
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    collection = client.create_collection(collection_name)
    print("向量库已重建")

    ids = [str(i) for i in range(len(idx))]
    metadatas = [{"idx": int(idx_value)} for idx_value in idx]
    documents = [str(text_value) for text_value in text]
    a=get_embeddings()
    embedding=a.embed_documents(documents)

    if documents:
        collection.add(ids=ids, documents=documents, metadatas=metadatas,embeddings=embedding)
        print(f"{collection_name} 写入 {len(documents)} 条记录成功")
    else:
        print("没有需要写入的数据")

    return collection