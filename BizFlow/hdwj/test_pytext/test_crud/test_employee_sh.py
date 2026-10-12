# 员工提交审核表测试文件
# 文件名：test_employee_sh_http.py

import random
import pytest
from passlib.context import CryptContext

from BizFlow.hdwj.function.sign_in_ly import (
    sign_yz,
    CHAIRMAN_KEY,
)

from BizFlow.hdwj.tool.sc_token import create_token

# 导入统一测试 fixture
from BizFlow.hdwj.test_pytext.test_tools.test_shujuku import (
    client,
    db_session,
)


EMPLOYEE_URL = "/Employee"


# 密码加密上下文
pwd_ctx = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# ----------------------------------------------------------
# helper 辅助函数
# ----------------------------------------------------------

def _make_user_and_token(db, role="员工"):
    """
    创建用户并生成 token
    """

    # 延迟导入数据库模型
    from BizFlow.shujuku.user import users


    name = f"emp_{random.randint(100000, 999999)}"
    emp_id = random.randint(1000000, 9999999)


    if role == "董事长":

        sign_yz(
            name=name,
            password="ChairmanPass123!",
            employee_id=emp_id,
            position="董事长",
            yz=CHAIRMAN_KEY,
            db=db,
        )

    else:

        db.add(
            users(
                name=name,
                password=pwd_ctx.hash("EmpPass123!"),
                employee_ID=emp_id,
                position="员工",
            )
        )

        db.commit()


    token = create_token(
        {
            "username": name,
            "role": role,
        }
    )


    return name, emp_id, token



def _auth(token):
    return {
        "Authorization": f"Bearer {token}"
    }



def _body(name, task_name, content, assignee_id):

    return {
        "id": assignee_id,
        "name": name,
        "task_name": task_name,
        "content": content,
    }



# ----------------------------------------------------------
# 主路径：提交成功
# ----------------------------------------------------------

def test_employee_sh_http_success(client, db_session):

    from BizFlow.shujuku.user import yg_tjs


    name, emp_id, token = _make_user_and_token(
        db_session,
        role="员工",
    )


    task_name = f"task_{random.randint(100000, 999999)}"

    content = "这是员工提交的任务内容"



    resp = client.post(
        EMPLOYEE_URL,
        json=_body(
            name=name,
            task_name=task_name,
            content=content,
            assignee_id=emp_id,
        ),
        headers=_auth(token),
    )


    assert resp.status_code == 200, resp.text

    assert resp.json()["message"] == "提交审核成功"



    saved = (
        db_session.query(yg_tjs)
        .filter(
            yg_tjs.name_rw == task_name
        )
        .first()
    )


    assert saved is not None

    assert saved.name == name

    assert saved.name_rw == task_name

    assert saved.content == content

    assert saved.assignee_id == emp_id

    assert saved.zt == "审核中"



# ----------------------------------------------------------
# 无 token
# ----------------------------------------------------------

def test_employee_sh_http_no_token(client):

    resp = client.post(
        EMPLOYEE_URL,
        json=_body(
            name="x",
            task_name="y",
            content="z",
            assignee_id=1,
        ),
    )


    assert resp.status_code == 401



# ----------------------------------------------------------
# 非法 token
# ----------------------------------------------------------

def test_employee_sh_http_bad_token(client):

    resp = client.post(
        EMPLOYEE_URL,
        json=_body(
            name="x",
            task_name="y",
            content="z",
            assignee_id=1,
        ),
        headers={
            "Authorization": "Bearer not.a.real.token"
        },
    )


    assert resp.status_code == 401



# ----------------------------------------------------------
# body 缺字段
# ----------------------------------------------------------

def test_employee_sh_http_missing_field(
    client,
    db_session,
):

    _, _, token = _make_user_and_token(
        db_session,
        role="员工",
    )


    resp = client.post(
        EMPLOYEE_URL,
        json={
            "name": "x",
            "task_name": "y",
        },
        headers=_auth(token),
    )


    assert resp.status_code == 422



# ----------------------------------------------------------
# body 类型错误
# ----------------------------------------------------------

def test_employee_sh_http_wrong_type(
    client,
    db_session,
):

    _, _, token = _make_user_and_token(
        db_session,
        role="员工",
    )


    resp = client.post(
        EMPLOYEE_URL,
        json={
            "id": "not-an-int",
            "name": "x",
            "task_name": "y",
            "content": "z",
        },
        headers=_auth(token),
    )


    assert resp.status_code == 422



# ----------------------------------------------------------
# 重复提交
# ----------------------------------------------------------

def test_employee_sh_http_duplicate_task_name(
    client,
    db_session,
):

    from BizFlow.shujuku.user import yg_tjs


    name, emp_id, token = _make_user_and_token(
        db_session,
        role="员工",
    )


    task_name = f"task_{random.randint(100000, 999999)}"



    for _ in range(2):

        resp = client.post(
            EMPLOYEE_URL,
            json=_body(
                name,
                task_name,
                "内容",
                emp_id,
            ),
            headers=_auth(token),
        )


        assert resp.status_code == 200



    cnt = (
        db_session.query(yg_tjs)
        .filter(
            yg_tjs.name_rw == task_name
        )
        .count()
    )


    assert cnt == 2