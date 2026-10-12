#es引擎
from elasticsearch import Elasticsearch
from llama_index.core.indices.vector_store.retrievers import retriever

es=Elasticsearch("http://localhost:9200")

INDEX_NAME = "rag_documents"
def index():
  if not es.indices.create(index=INDEX_NAME):
      es.search(
          index=INDEX_NAME,
          mappings={
              "properties":{
                  "content":{"type":"text"},
                  "embedding": {
                      "type": "dense_vector",
                      "dims": 384
              }
              }
          }
      )
  else:
      return
es.index(index=INDEX_NAME,
         document={
             "content":{}
         }
         )
def hhjs(request:str):
    es.create(index=INDEX_NAME,
              retriever={
        "rrf":{
            "retrievers":[
            {
                "standard":{
                    "query":{
                        "match":{
                            "content":request
                        }
                    }
                }
            },

            {
                "knn":{
                    "field":"embding",
                    "query":"query",
                    "k":5,
                    "num_candidates":10
                }
            }
        ],"rank_window_size": 50,

            "rank_constant": 20
               }
    }
              )