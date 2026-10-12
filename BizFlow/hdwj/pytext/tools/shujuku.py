# BizFlow/hdwj/pytext/tools/shujuku.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from BizFlow.hdwj.app import app
from BizFlow.shujuku.Management import Base, get_db
from BizFlow.shujuku.user import users


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
# 2. 测试数据库依赖
# ==========================================

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# 3. 测试客户端（自动带假 token，绕过中间件）
# ==========================================

@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    old_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = override_get_db

    # ✅ 关键：全局默认带 Authorization 头，绕过中间件
    test_client = TestClient(
        app,
        headers={"Authorization": "Bearer fake_test_token"},
    )

    try:
        yield test_client
    finally:
        test_client.close()
        app.dependency_overrides.clear()
        app.dependency_overrides.update(old_overrides)
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()


# ==========================================
# 4. 便捷 fixture：直接拿到测试 session
# ==========================================

@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()