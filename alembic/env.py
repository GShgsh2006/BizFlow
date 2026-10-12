# alembic/env.py
"""Alembic 运行入口。

作用：
1. 让 Alembic 能找到项目里的 BizFlow 包；
2. 从 .env 读 DATABASE_URL；
3. 把 Base.metadata 作为对比目标；
4. 支持 autogenerate 和 upgrade。
"""

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ---------------------------------------------------------------------------
# 1. 把项目根目录加入 sys.path，否则 import BizFlow 会失败
# ---------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ---------------------------------------------------------------------------
# 2. 读取 .env
# ---------------------------------------------------------------------------
from dotenv import load_dotenv

load_dotenv(os.path.join(BASE_DIR, ".env"))

# ---------------------------------------------------------------------------
# 3. 导入 Base 和所有模型
#    BizFlow.shujuku.__init__ 里要 import 所有模型
# ---------------------------------------------------------------------------
from BizFlow.shujuku import Base  # noqa: E402
import BizFlow.shujuku  # noqa: E402,F401 触发所有模型注册

# ---------------------------------------------------------------------------
# 4. Alembic 配置
# ---------------------------------------------------------------------------
config = context.config

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("环境变量 DATABASE_URL 未设置，请检查 .env")

config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# autogenerate 的对比目标
target_metadata = Base.metadata


# ---------------------------------------------------------------------------
# 5. 离线模式：只生成 SQL，不连库
# ---------------------------------------------------------------------------
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------------
# 6. 在线模式：真正连库执行
# ---------------------------------------------------------------------------
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()