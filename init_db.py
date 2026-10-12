# -*- coding: utf-8 -*-
"""一键建库建表脚本（BizFlow）

根据 `BizFlow/shujuku/user.py` 中定义的 ORM 模型，在 MySQL 里自动创建数据库和 6 张表。

用法（在项目根目录 fastapixxxmmm 下执行）：
    python init_db.py

前置条件：
    1. MySQL 服务已启动；
    2. BizFlow/.env 中的 HOSTNAME / PORT / USERNAME / PASSWORD / DATABASE 配置正确。
"""
import sys
from pathlib import Path

# 保证项目根目录在 sys.path，使 `import BizFlow.xxx` 能正常解析
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy import create_engine as _create_engine  # noqa: E402
from sqlalchemy import text  # noqa: E402

# 必须先导入模型模块，让 6 张表注册到 Base.metadata，
# 否则 create_all 会认为没有表、什么都不建。
import BizFlow.shujuku.user  # noqa: E402,F401
from BizFlow.shujuku.Management import (  # noqa: E402
    Base,
    engine,
    HOSTNAME,
    PORT,
    USERNAME,
    PASSWORD,
    DATABASE,
)


def ensure_database() -> None:
    """目标数据库不存在时自动创建（CREATE DATABASE IF NOT EXISTS）。"""
    server_url = (
        f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/"
        "?charset=utf8mb4"
    )
    server_engine = _create_engine(server_url, echo=False, pool_pre_ping=True)
    with server_engine.connect() as conn:
        conn.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{DATABASE}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )
        conn.commit()
    server_engine.dispose()
    print(f"[OK] 数据库 `{DATABASE}` 已就绪")


def create_tables() -> None:
    tables = sorted(Base.metadata.tables)
    print("将创建以下数据表：")
    for name in tables:
        print(f"  - {name}")
    Base.metadata.create_all(bind=engine)
    print(f"[OK] 建表完成，共 {len(tables)} 张表")


if __name__ == "__main__":
    ensure_database()
    create_tables()
