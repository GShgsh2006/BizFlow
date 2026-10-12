# BizFlow/hdwj/test_pytext/tools/test_shujuku.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from BizFlow.hdwj.app import app
from BizFlow.shujuku.Management import Base, get_db


# ==========================================
# 1. 创建临时 SQLite 数据库
# ==========================================

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False,
)


# ==========================================
# 2. 测试数据库依赖（普通生成器函数，不能加 test_ 前缀）
# ==========================================

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# 3. 自动建表与销毁表（autouse=True 表示每个测试用例自动执行）
# ==========================================

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


# ==========================================
# 4. 测试客户端（fixture 命名为 client，不能加 test_ 前缀）
# ==========================================

@pytest.fixture
def client():
    old_overrides = app.dependency_overrides.copy()
    # 将真实的数据库依赖替换为测试用的
    app.dependency_overrides[get_db] = override_get_db

    # 实例化 TestClient，带上假的 Authorization 头绕过中间件
    test_client_instance = TestClient(
        app,
        headers={"Authorization": "Bearer fake_test_token"},
    )

    try:
        yield test_client_instance
    finally:
        test_client_instance.close()
        app.dependency_overrides.clear()
        app.dependency_overrides.update(old_overrides)


# ==========================================
# 5. 便捷 fixture：直接拿到测试 session（命名为 db_session）
# ==========================================

@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()