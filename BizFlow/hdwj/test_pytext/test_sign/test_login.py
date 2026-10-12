#登入测试接口
# BizFlow/hdwj/test_pytext/test_sign/test_login.py 或类似路径
import pytest
from BizFlow.hdwj.test_pytext.test_tools.test_shujuku import client, db_session
from BizFlow.shujuku.user import users


from BizFlow.shujuku.yanzheng import get_password_hash
@pytest.fixture
def test_user(client, db_session):
    # 这是登录时使用的明文密码
    plain_password = "TestPassword123!"

    # 先加密，再存入临时数据库
    hashed_password = get_password_hash(plain_password)

    # 使用 db_session 插入数据
    test_user_obj = users(
        name="test_user_001",
        password=hashed_password,
        employee_ID=100001,
        position="测试员工",
    )
    db_session.add(test_user_obj)
    db_session.commit()

    # 返回登录需要的明文密码
    return {
        "name": "test_user_001",
        "password": plain_password,
    }



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

# ✅ 关键4：参数名统一为 client
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