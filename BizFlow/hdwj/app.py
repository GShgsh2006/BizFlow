#BizFlow 智能业务协作平台
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import threading
logging.basicConfig(level=logging.INFO)
from BizFlow.hdwj.tool.token_yz import auth_middleware
from BizFlow.hdwj.Route.crud_Route import router
from BizFlow.hdwj.Route.sign_in_up import routers
from BizFlow.hdwj.Route.notice_ly import router_notice
from BizFlow.hdwj.Route.Salary_ly import router_gz
from BizFlow.hdwj.tool.zjj import LoggingMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
# AI/RAG/LangGraph 依赖较重(需要下载模型 / 连 Ollama / Milvus 等)。
# 这里容错导入:装好且可用才挂载，失败只跳过，不影响核心业务启动。
routerk = None
routeragent = None
file = None

try:
    from BizFlow.hdwj.AI.RAG.route.ai_ly import routerk
except Exception as e:
    logging.error("AI(RAG) 路由导入失败，已跳过: %s", e)

try:
    from BizFlow.hdwj.LangGraph_ly.app import routeragent
except Exception as e:
    logging.error("LangGraph Agent 路由导入失败，已跳过: %s", e)

try:
    from BizFlow.hdwj.AI.RAG.file_interoperability import file
except Exception as e:
    logging.error("RAG 知识库链路导入失败，已跳过: %s", e)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 项目启动时先自动对齐数据库结构（只加表/加列，幂等，反复跑也没事）。
    # 没这一步的话：模型里加了字段但 MySQL 没迁移，SQLAlchemy 会把它插进
    # SELECT 里，接口直接 500（踩过的坑：notice.name_id -> Unknown column）。
    try:
        from BizFlow.shujuku.migrate import migrate

        created, added, manual = migrate()
        if created or added:
            logging.info("数据库结构已自动补齐 | 新建表=%s | 新增列=%s", created, added)
        else:
            logging.info("数据库结构已是最新，无需迁移")
        if manual:
            logging.warning("以下列需人工处理(NOT NULL 且无默认值): %s", manual)
    except Exception as e:
        # 迁移失败不让服务起不来，只是接口该报错还是会报错，日志里能看到原因
        logging.error("数据库自动迁移失败(不影响启动): %s", e)

    # 项目启动时执行一次
    # RAG 初始化放到后台线程，避免阻塞服务启动：
    # 否则 embedding/向量库下载模型会把整个启动卡住，导致登录、注册等接口无响应。
    if file is not None:
        def _init_rag():
            try:
                from BizFlow.hdwj.AI.RAG.tool.yyqga import load_embedding_model
                load_embedding_model()
                logging.info("Embedding 模型加载完成")
            except Exception as e:
                logging.error("Embedding 模型加载失败: %s", str(e))
            try:
                import asyncio as _asyncio
                _asyncio.run(file())
            except Exception as e:
                logging.error("RAG 知识库初始化失败: %s", str(e))

        threading.Thread(target=_init_rag, daemon=True).start()

    yield

    # 项目关闭执行
    print("项目关闭")


app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(routers)
if routerk is not None:
    app.include_router(routerk)
if routeragent is not None:
    app.include_router(routeragent)
app.include_router(router_notice)
app.include_router(router_gz)

app.add_middleware(LoggingMiddleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:2020"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
