#员工提交审核表测试文件
# tests/test_employee_sh_http.py
import random

import pytest

from BizFlow.shujuku.user import yg_tjs
from BizFlow.hdwj.pytext.tools.shujuku import client, TestingSessionLocal

from BizFlow.hdwj.function.sign_in_ly import sign_yz, CHAIRMAN_KEY       # 董事长注册
from BizFlow.hdwj.tool.sc_token import create_token                   # 生成 token


EMPLOYEE_URL = "/Employee"                  # 按你 app.include_router 的前缀改


# ----------------------------------------------------------
@pytest.fixture
def db_session(client):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------------------------------------
# helper
# ----------------------------------------------------------
def _make_user_and_token(db, role="员工"):
    """
    造一个用户拿 token。
    employee_sh 里不校验 role，所以随便什么 role 都行；
    但 token 必须合法，否则 get_current_user 抛 401。
    """
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
        # 如果你有普通注册接口，用它；没有就直接塞 users 表
        from BizFlow.shujuku.user import users
        from passlib.context import CryptContext
        pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        db.add(users(
            name=name,
            password=pwd_ctx.hash("EmpPass123!"),
            employee_ID=emp_id,
            position="员工",
        ))
        db.commit()

    token = create_token({"username": name, "role": role})
    return name, emp_id, token


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


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
    name, emp_id, token = _make_user_and_token(db_session, role="员工")

    task_name = f"task_{random.randint(100000, 999999)}"
    content = "这是员工提交的任务内容"

    resp = client.post(
        EMPLOYEE_URL,
        json=_body(name=name, task_name=task_name, content=content, assignee_id=emp_id),
        headers=_auth(token),
    )

    assert resp.status_code == 200, resp.text
    assert resp.json()["message"] == "提交审核成功"

    # 查库
    saved = (
        db_session.query(yg_tjs)
        .filter(yg_tjs.name_rw == task_name)
        .first()
    )
    assert saved is not None
    assert saved.name == name
    assert saved.name_rw == task_name
    assert saved.content == content
    assert saved.assignee_id == emp_id
    assert saved.zt == "审核中"      # 关键断言


# ----------------------------------------------------------
# 无 token → 401
# ----------------------------------------------------------
def test_employee_sh_http_no_token(client):
    resp = client.post(
        EMPLOYEE_URL,
        json=_body(name="x", task_name="y", content="z", assignee_id=1),
    )
    assert resp.status_code == 401


# ----------------------------------------------------------
# 非法 token → 401
# ----------------------------------------------------------
def test_employee_sh_http_bad_token(client):
    resp = client.post(
        EMPLOYEE_URL,
        json=_body(name="x", task_name="y", content="z", assignee_id=1),
        headers={"Authorization": "Bearer not.a.real.token"},
    )
    assert resp.status_code == 401


# ----------------------------------------------------------
# body 缺字段 → 422（FastAPI/Pydantic 自动校验）
# ----------------------------------------------------------
def test_employee_sh_http_missing_field(client, db_session):
    _, _, token = _make_user_and_token(db_session, role="员工")

    resp = client.post(
        EMPLOYEE_URL,
        json={"name": "x", "task_name": "y"},   # 缺 content 和 id
        headers=_auth(token),
    )
    assert resp.status_code == 422


# ----------------------------------------------------------
# body 字段类型错 → 422
# ----------------------------------------------------------
def test_employee_sh_http_wrong_type(client, db_session):
    _, _, token = _make_user_and_token(db_session, role="员工")

    resp = client.post(
        EMPLOYEE_URL,
        json={"id": "not-an-int", "name": "x",
              "task_name": "y", "content": "z"},
        headers=_auth(token),
    )
    assert resp.status_code == 422


# ----------------------------------------------------------
# 可多次提交：同一 task_name 会新增多条记录（目前没唯一约束）
# ----------------------------------------------------------
def test_employee_sh_http_duplicate_task_name(client, db_session):
    name, emp_id, token = _make_user_and_token(db_session, role="员工")
    task_name = f"task_{random.randint(100000, 999999)}"

    for _ in range(2):
        resp = client.post(
            EMPLOYEE_URL,
            json=_body(name, task_name, "内容", emp_id),
            headers=_auth(token),
        )
        assert resp.status_code == 200

    cnt = (
        db_session.query(yg_tjs)
        .filter(yg_tjs.name_rw == task_name)
        .count()
    )
    assert cnt == 2        # 说明现在没有唯一性约束