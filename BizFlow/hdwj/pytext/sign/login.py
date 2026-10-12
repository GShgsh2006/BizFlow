#登入测试接口
# tests/test_login.py
# tests/test_login.py

import pytest

from BizFlow.hdwj.pytext.tools.shujuku import client,TestingSessionLocal
from BizFlow.shujuku.user import users
# ==========================================
# 4. 向测试数据库插入一个测试用户
# ==========================================
# 使用项目原有的密码工具
from BizFlow.shujuku.yanzheng import get_password_hash

@pytest.fixture
def test_user(client):
    # 这是登录时使用的明文密码
    plain_password = "TestPassword123!"

    # 先加密，再存入临时数据库
    hashed_password = get_password_hash(plain_password)

    with TestingSessionLocal() as db:
        test_user = users(
            name="test_user_001",
            password=hashed_password,
            employee_ID=100001,
            position="测试员工",
        )

        db.add(test_user)
        db.commit()

    # 返回登录需要的明文密码
    return {
        "name": "test_user_001",
        "password": plain_password,
    }
# ==========================================
# 5. 测试登录成功
# ==========================================

def test_login_success(client, test_user):

    # 调用登录路由
    response = client.post(
        "/sign_in",
        json={
            "name": test_user["name"],
            "password": test_user["password"],
        },
    )

    # 检查登录是否成功
    assert response.status_code == 200

    # 检查是否返回了响应内容
    result = response.json()

    assert isinstance(result, dict)
    assert result


# ==========================================
# 6. 测试密码错误
# ==========================================

def test_login_wrong_password(client, test_user):

    response = client.post(
        "/sign_in",
        json={
            "name": test_user["name"],
            "password": "WrongPassword123!",
        },
    )

    # 假设登录失败返回 HTTP 401
    assert response.status_code == 401