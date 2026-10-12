# tests/test_query_task.py

import pytest
from datetime import datetime

# ✅ 关键1：导入统一标准的 client 和 db_session
from BizFlow.hdwj.test_pytext.test_tools.test_shujuku import client, db_session
from BizFlow.shujuku.user import users
from BizFlow.shujuku.user import task  # ⚠️ 换成真实路径


# ==========================================
# fixture：插张三 + 一个任务
# ✅ 关键2：fixture 名字改为 task_data，参数使用 db_session
# ==========================================

@pytest.fixture
def task_data(db_session):
    employee = users(
        name="张三",
        password="not_used",
        employee_ID=1001,
        position="员工",
    )
    db_session.add(employee)
    db_session.commit()
    db_session.refresh(employee)

    new_task = task(
        name="测试任务A",
        Deadline=datetime(2026, 1, 1, 12, 0, 0),
        content="这是测试任务A的内容",
        assignor="张三",
        assignee_id=employee.id,   # ← 关键
        status="未完成",
        amount=100,
    )
    db_session.add(new_task)
    db_session.commit()
    db_session.refresh(new_task)

    return {
        "name": "测试任务A",
        "assignor": "张三",
        "content": "这是测试任务A的内容",
    }


# ==========================================
# 测试用例
# ✅ 关键3：参数统一为 client 和 task_data
# ==========================================

def test_query_by_name_success(client, task_data):
    response = client.get("/query", params={"name": "张三"})
    assert response.status_code == 200, response.text
    result = response.json()
    assert len(result) == 1
    assert result[0]["name"] == "测试任务A"


def test_query_by_task_success(client, task_data):
    response = client.get("/query", params={"task": "测试任务A"})
    assert response.status_code == 200, response.text
    result = response.json()
    assert len(result) == 1
    assert result[0]["name"] == "测试任务A"


def test_query_by_name_not_employee(client, task_data):
    response = client.get("/query", params={"name": "不存在的人"})
    assert response.status_code == 404
    assert "还不是公司员工" in response.json()["detail"]


def test_query_by_task_not_found(client, task_data):
    response = client.get("/query", params={"task": "不存在的任务"})
    assert response.status_code == 404


def test_query_no_params(client):
    response = client.get("/query")
    assert response.status_code == 404
    assert "请输入" in response.json()["detail"]


def test_query_employee_without_task(client, db_session):
    # ✅ 关键4：这里不需要 task_data，直接利用 db_session 插入新数据
    db_session.add(users(
        name="李四",
        password="not_used",
        employee_ID=1002,
        position="员工",
    ))
    db_session.commit()

    response = client.get("/query", params={"name": "李四"})
    assert response.status_code == 404
    assert "还没有任何任务" in response.json()["detail"]