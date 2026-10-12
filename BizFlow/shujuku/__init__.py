# BizFlow/shujuku/__init__.py

# 把 Base 暴露出去，让 env.py 能导入
from BizFlow.shujuku.Management import Base, engine, SessionLocal  # noqa: F401

# 把模型导入进来，让 Alembic 能扫到你的表
from BizFlow.shujuku.user import users, task,employees,yg_tjs,notice,yynj,yyygb