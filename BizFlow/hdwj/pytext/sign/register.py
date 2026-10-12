#注册测试
import pytest

from BizFlow.hdwj.pytext.tools.shujuku import client,TestingSessionLocal
# 5. 提供测试数据库会话，供测试函数查询数据
@pytest.fixture
def db_session(client):
    db = TestingSessionLocal()
    try:
        
        yield db
    finally:
        db.close()
# tests/test_register.py

import bcrypt

from BizFlow.shujuku.user import users


# 改成你的注册接口实际完整路由
REGISTER_URL = "/sign_up"


def get_register_data():
    """生成一份测试注册数据。"""
    return {
        "name": "test_register_001",
        "password": "TestPassword123!",
        "employee_ID": 100001,
        "position": "员工",
    }


def test_register_success(client, db_session):
    """测试注册成功，并检查数据库中是否真的保存了用户。"""

    # 第一步：准备注册数据
    data = get_register_data()

    # 第二步：调用原来的注册接口
    response = client.post(
        REGISTER_URL,
        json=data,
    )

    # 第三步：检查 HTTP 响应
    assert response.status_code in (200, 201), (
        f"注册失败：状态码={response.status_code}，"
        f"返回内容={response.text}"
    )

    # 第四步：直接查询测试数据库
    saved_user = (
        db_session.query(users)
        .filter(users.name == data["name"])
        .first()
    )

    # 第五步：检查用户是否真正写入数据库
    assert saved_user is not None

    # 第六步：检查注册信息是否保存正确
    assert saved_user.name == data["name"]
    assert saved_user.employee_ID == data["employee_ID"]
    assert saved_user.position == data["position"]

    # 第七步：检查数据库存储的密码不是明文
    assert saved_user.password != data["password"]

    # 验证数据库中的 bcrypt 哈希确实对应输入的密码
    assert bcrypt.checkpw(
        data["password"].encode("utf-8"),
        saved_user.password.encode("utf-8"),
    )