# BizFlow/hdwj/test_pytext/test_sign/test_login.py

import pytest

from BizFlow.hdwj.test_pytext.test_tools.test_shujuku import (
    client,
    db_session,
)

from BizFlow.shujuku.yanzheng import get_password_hash


@pytest.fixture
def test_user(client, db_session):

    # 测试时再导入模型，避免提前加载数据库
    from BizFlow.shujuku.user import users

    # 登录使用的明文密码
    plain_password = "TestPassword123!"

    # 生成密码哈希
    hashed_password = get_password_hash(plain_password)


    # 创建测试用户
    test_user_obj = users(
        name="test_user_001",
        password=hashed_password,
        employee_ID=100001,
        position="测试员工",
    )


    # 写入临时 SQLite 数据库
    db_session.add(test_user_obj)
    db_session.commit()


    return {
        "name": "test_user_001",
        "password": plain_password,
    }



def test_login_success(client, test_user):

    response = client.post(
        "/sign_in",
        json={
            "name": test_user["name"],
            "password": test_user["password"],
        },
    )


    assert response.status_code == 200


    result = response.json()

    assert isinstance(result, dict)
    assert result



def test_login_wrong_password(client, test_user):

    response = client.post(
        "/sign_in",
        json={
            "name": test_user["name"],
            "password": "WrongPassword123!",
        },
    )


    assert response.status_code == 401