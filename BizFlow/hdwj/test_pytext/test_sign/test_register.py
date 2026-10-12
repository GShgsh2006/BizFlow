# BizFlow/hdwj/test_pytext/test_sign/test_register.py

import bcrypt

# 从测试工具中导入临时数据库相关 fixture
from BizFlow.hdwj.test_pytext.test_tools.test_shujuku import (
    client,
    db_session,
)


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
    """测试注册成功，并检查测试数据库中是否保存用户。"""

    # 测试时再导入模型，避免 pytest 收集阶段提前加载数据库
    from BizFlow.shujuku.user import users

    # 第一步：准备注册数据
    data = get_register_data()

    # 第二步：调用注册接口
    response = client.post(
        REGISTER_URL,
        json=data,
    )

    # 第三步：检查接口响应
    assert response.status_code in (200, 201), (
        f"注册失败：状态码={response.status_code}, "
        f"返回内容={response.text}"
    )

    # 第四步：查询测试 SQLite 数据库
    saved_user = (
        db_session.query(users)
        .filter(users.name == data["name"])
        .first()
    )

    # 第五步：确认用户写入数据库
    assert saved_user is not None

    # 第六步：检查字段
    assert saved_user.name == data["name"]
    assert saved_user.employee_ID == data["employee_ID"]
    assert saved_user.position == data["position"]

    # 第七步：检查密码不是明文
    assert saved_user.password != data["password"]

    # 第八步：验证 bcrypt 哈希
    assert bcrypt.checkpw(
        data["password"].encode("utf-8"),
        saved_user.password.encode("utf-8"),
    )