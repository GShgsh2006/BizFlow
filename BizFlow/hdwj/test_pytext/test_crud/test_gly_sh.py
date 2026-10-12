# 管理员同意测试文件
# 文件名请保持为 test_gly_sh_http.py

import random
from datetime import datetime, timedelta

import pytest

from BizFlow.shujuku.user import task, yg_tjs
# ✅ 关键1：从统一的 test_shujuku.py 导入标准的 client 和 db_session
from BizFlow.hdwj.test_pytext.test_tools.test_shujuku import client, db_session

from BizFlow.hdwj.function.sign_in_ly import sign_yz, CHAIRMAN_KEY  # 董事长注册
from BizFlow.hdwj.tool.sc_token import create_token  # 生成 token

# 确认 router 前缀是否包含在 app.include_router 里
GLY_SH_URL = "/gly_sh_ly"

# ----------------------------------------------------------
# 注意：删除了这里原有的 db_session fixture 定义。
# 因为 test_shujuku.py 已经全局定义了标准的 db_session，pytest 会自动注入。
# ----------------------------------------------------------

# ----------------------------------------------------------
# helper 辅助函数
# ----------------------------------------------------------
def _make_chairman(db):
    """注册董事长，返回 (name, employee_id, token)"""
    name = f"chairman_{random.randint(100000, 999999)}"
    emp = random.randint(1000000, 9999999)

    res = sign_yz(
        name=name,
        password="ChairmanPass123!",
        employee_id=emp,
        position="董事长",
        yz=CHAIRMAN_KEY,
        db=db,
    )
    assert res["role"] == "董事长"

    # token 里必须带 role="董事长"，get_current_user 会把它 decode 出来给 gly_sh 用
    token = create_token({"username": name, "role": "董事长"})
    return name, emp, token


def _make_task_pair(db, chairman_name, assignee_id):
    """造一条 task + 对应的 yg_tjs，要求 yg_tjs.name_rw == task.name"""
    rw_name = f"rw_{random.randint(100000, 999999)}"

    t = task(
        name=rw_name,
        Deadline=datetime.now() + timedelta(days=7),
        content="这是一个测试任务的正文内容",
        assignor=chairman_name,
        assignee_id=assignee_id,
        status="待审核",
        amount=1000,
    )
    db.add(t)
    db.commit()
    db.refresh(t)

    y = yg_tjs(
        name=chairman_name,
        name_rw=rw_name,
        content="提交上来的任务内容",
        assignee_id=assignee_id,
        zt="审核中",
    )
    db.add(y)
    db.commit()
    db.refresh(y)

    return y, t


def _auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


# ----------------------------------------------------------
# 阶段一：通过审核
# ----------------------------------------------------------
def test_gly_sh_http_pass(client, db_session):  # ✅ 参数统一为 client
    name, emp, token = _make_chairman(db_session)
    y, t = _make_task_pair(db_session, chairman_name=name, assignee_id=emp)

    # 走 HTTP
    resp = client.get(  # ✅ client
        f"{GLY_SH_URL}/{y.id}",
        params={"querya": "通过审核"},
        headers=_auth_headers(token),
    )

    assert resp.status_code == 200, resp.text
    assert resp.json()["message"] == "通过审核"

    # 查库确认
    db_session.refresh(y)
    db_session.refresh(t)
    assert y.zt == "审核通过"
    assert t.status == "已完成"


# ----------------------------------------------------------
# 阶段二：审核不通过
# ----------------------------------------------------------
def test_gly_sh_http_reject(client, db_session):  # ✅ 参数统一为 client
    name, emp, token = _make_chairman(db_session)
    y, t = _make_task_pair(db_session, chairman_name=name, assignee_id=emp)

    resp = client.get(  # ✅ client
        f"{GLY_SH_URL}/{y.id}",
        params={"querya": "审核不通过"},
        headers=_auth_headers(token),
    )

    assert resp.status_code == 200, resp.text
    assert resp.json()["message"] == "审核不通过"

    db_session.refresh(y)
    db_session.refresh(t)
    assert y.zt == "审核未通过"
    assert t.status == "审核未通过"


# ----------------------------------------------------------
# 反向用例
# ----------------------------------------------------------
def test_gly_sh_http_no_token(client, db_session):  # ✅ 参数统一为 client
    """不带 token → 401"""
    name, emp, _ = _make_chairman(db_session)
    y, _ = _make_task_pair(db_session, chairman_name=name, assignee_id=emp)

    resp = client.get(f"{GLY_SH_URL}/{y.id}", params={"querya": "通过审核"})  # ✅ client
    assert resp.status_code == 401


def test_gly_sh_http_wrong_role(client, db_session):  # ✅ 参数统一为 client
    """员工 token → 403"""
    # 只造 yg_tjs，够走到权限检查即可
    y = yg_tjs(name="x", name_rw="y", content="z",
               assignee_id=1, zt="审核中")
    db_session.add(y)
    db_session.commit()
    db_session.refresh(y)

    token = create_token({"username": "emp", "role": "员工"})
    resp = client.get(  # ✅ client
        f"{GLY_SH_URL}/{y.id}",
        params={"querya": "通过审核"},
        headers=_auth_headers(token),
    )
    assert resp.status_code == 403
    assert "无权" in resp.json()["detail"]


def test_gly_sh_http_bad_query(client, db_session):  # ✅ 参数统一为 client
    """query 不合法 → 400"""
    name, emp, token = _make_chairman(db_session)
    y, _ = _make_task_pair(db_session, chairman_name=name, assignee_id=emp)

    resp = client.get(  # ✅ client
        f"{GLY_SH_URL}/{y.id}",
        params={"querya": "随便写"},
        headers=_auth_headers(token),
    )
    assert resp.status_code == 400


def test_gly_sh_http_task_not_found(client, db_session):  # ✅ 参数统一为 client
    """task_id 不存在 → 404"""
    name, emp, token = _make_chairman(db_session)

    resp = client.get(  # ✅ client
        f"{GLY_SH_URL}/99999999",
        params={"querya": "通过审核"},
        headers=_auth_headers(token),
    )
    assert resp.status_code == 404


def test_gly_sh_http_rw_not_found(client, db_session):  # ✅ 参数统一为 client
    """yg_tjs 有，但 task 表里没有对应 name_rw → 404"""
    name, emp, token = _make_chairman(db_session)

    y = yg_tjs(
        name=name,
        name_rw="task 表里没有这个名字",
        content="x",
        assignee_id=emp,
        zt="审核中",
    )
    db_session.add(y)
    db_session.commit()
    db_session.refresh(y)

    resp = client.get(  # ✅ client
        f"{GLY_SH_URL}/{y.id}",
        params={"querya": "通过审核"},
        headers=_auth_headers(token),
    )
    assert resp.status_code == 404