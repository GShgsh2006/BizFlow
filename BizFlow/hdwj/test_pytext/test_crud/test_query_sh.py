# 管理员审核测试
# 文件名：test_query_sh.py

import pytest

from BizFlow.hdwj.test_pytext.test_tools.test_shujuku import (
    client,
    db_session,
)

from BizFlow.hdwj.function.sign_in_ly import (
    sign_yz,
    CHAIRMAN_KEY,
)

from BizFlow.hdwj.tool.sc_token import create_token


QUERY_SH_URL = "/query_sh_ly"


def test_query_sh_chairman_can_see_pending(client, db_session):
    """董事长带合法 token 查询，能看到审核中的任务"""

    # 测试时再加载数据库模型
    from BizFlow.shujuku.user import yg_tjs


    # 1. 注册董事长
    res = sign_yz(
        name="chairman_test",
        password="ChairmanPass123!",
        employee_id=900001,
        position="董事长",
        yz=CHAIRMAN_KEY,
        db=db_session,
    )

    assert res["role"] == "董事长"


    # 2. 创建 token
    token = create_token({
        "username": "chairman_test",
        "role": "董事长",
    })


    # 3. 创建审核任务
    task = yg_tjs(
        name="chairman_test",
        name_rw="测试任务-审核中",
        content="这是一条测试任务内容",
        assignee_id=900001,
        zt="审核中",
    )

    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)


    # 4. 调接口
    response = client.get(
        QUERY_SH_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
    )


    # 5. 验证
    assert response.status_code == 200, response.text

    data = response.json()

    assert any(
        item["id"] == task.id
        for item in data
    )

    assert all(
        item["zt"] == "审核中"
        for item in data
    )



def test_query_sh_employee_forbidden(client, db_session):
    """员工 token 查询审核 → 403"""


    token = create_token({
        "username": "some_employee",
        "role": "员工",
    })


    response = client.get(
        QUERY_SH_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
    )


    assert response.status_code == 403

    assert "无权" in response.json()["detail"]



def test_query_sh_no_token(client):
    """没有 token → 401"""


    response = client.get(
        QUERY_SH_URL
    )


    assert response.status_code == 401



def test_query_sh_bad_token(client):
    """非法 token → 401"""


    response = client.get(
        QUERY_SH_URL,
        headers={
            "Authorization": "Bearer not.a.real.token"
        },
    )


    assert response.status_code == 401