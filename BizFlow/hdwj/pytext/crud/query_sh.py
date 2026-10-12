#管理员审核测试

import pytest
from datetime import datetime

from BizFlow.shujuku.user import users
from BizFlow.shujuku.user import yg_tjs   # 改成你实际的模块路径
from BizFlow.hdwj.pytext.tools.shujuku import client, TestingSessionLocal

# 你的业务函数导入
from BizFlow.hdwj.function.sign_in_ly import sign_yz, CHAIRMAN_KEY       # 董事长注册
from BizFlow.hdwj.tool.sc_token import create_token                # 生成 token
# query_sh 是路由里的函数，测试走 HTTP，不需要直接导入

QUERY_SH_URL = "/query_sh_ly"


@pytest.fixture
def db_session(client):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_query_sh_chairman_can_see_pending(client, db_session):
    """董事长带合法 token 查询，能看到审核中的任务"""

    # 1. 注册董事长（走 sign_yz，用 CHAIRMAN_KEY 过验证）
    res = sign_yz(
        name="chairman_test",
        password="ChairmanPass123!",
        employee_id=900001,
        position="董事长",
        yz=CHAIRMAN_KEY,
        db=db_session,
    )
    assert res["role"] == "董事长"

    # 2. 生成 token —— 关键：payload 里要带 role
    token = create_token({
        "username": "chairman_test",
        "role": "董事长",
    })

    # 3. 造一条"审核中"的任务
    task = yg_tjs(
        name="chairman_test",  # 或别的标识
        name_rw="测试任务-审核中",
        content="这是一条测试任务内容",
        assignee_id=900001,  # 和你注册的董事长工号/员工 id 对应
        zt="审核中",
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    # 4. 带 token 调接口
    response = client.get(
        QUERY_SH_URL,
        headers={"Authorization": f"Bearer {token}"},
    )

    # 5. 断言
    assert response.status_code == 200, response.text
    data = response.json()
    assert any(item["id"] == task.id for item in data)
    assert all(item["zt"] == "审核中" for item in data)


def test_query_sh_employee_forbidden(client, db_session):
    """员工 token 查审核 → 403"""

    # 直接用注册接口造一个员工（role 不是董事长）
    # 或者直接往 db_session 塞一个也行
    token = create_token({
        "username": "some_employee",
        "role": "员工",
    })

    response = client.get(
        QUERY_SH_URL,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
    assert "无权" in response.json()["detail"]


def test_query_sh_no_token(client):
    """不带 token → 401"""

    response = client.get(QUERY_SH_URL)
    assert response.status_code == 401


def test_query_sh_bad_token(client):
    """token 伪造 → 401"""

    response = client.get(
        QUERY_SH_URL,
        headers={"Authorization": "Bearer not.a.real.token"},
    )
    assert response.status_code == 401