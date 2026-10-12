# BizFlow/hdwj/test_pytext/tools/test_shujuku.py

import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


# ==========================================
# 1. 创建测试 SQLite 数据库
# ==========================================

test_engine = create_engine(
    "sqlite://",
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool,
)


TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False,
)


# ==========================================
# 2. 覆盖 FastAPI 数据库依赖
# ==========================================

def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================================
# 3. 测试数据库生命周期
# ==========================================

@pytest.fixture(autouse=True)
def setup_database():

    # 必须提前导入模型
    # 让 SQLAlchemy 的 Base.metadata 注册所有表
    from BizFlow.shujuku import user

    from BizFlow.shujuku.Management import Base


    # 创建 SQLite 临时表
    Base.metadata.create_all(
        bind=test_engine
    )


    yield


    # 测试结束删除所有表
    Base.metadata.drop_all(
        bind=test_engine
    )


# ==========================================
# 4. FastAPI 测试客户端
# ==========================================

@pytest.fixture
def client():

    from BizFlow.hdwj.app import app
    from BizFlow.shujuku.Management import get_db


    # 保存原来的依赖
    old_overrides = app.dependency_overrides.copy()


    # 替换真实 MySQL 数据库
    app.dependency_overrides[get_db] = override_get_db


    test_client = TestClient(
        app,
        headers={
            "Authorization": "Bearer fake_test_token"
        }
    )


    try:

        yield test_client


    finally:

        test_client.close()


        # 恢复原来的依赖
        app.dependency_overrides.clear()

        app.dependency_overrides.update(
            old_overrides
        )


# ==========================================
# 5. 测试时直接操作 SQLite
# ==========================================

@pytest.fixture
def db_session():

    session = TestingSessionLocal()

    try:

        yield session

    finally:

        session.close()