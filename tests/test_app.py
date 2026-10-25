# -*- coding: utf-8 -*-
"""test_app.py —— 验证拆分后的服务行为和拆分前完全一样。

这是"重构"的验收标准：
    **行为不变，结构变好。**

拆完之后这里全绿，就证明你没在拆分过程中改坏任何东西。

运行：
    .\\dev.cmd test test_app.py
"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent))

import app.database as dbmod
from app.database import create_table
from app.main import app
import app.routers.scores as scores_router


@pytest.fixture
def client(tmp_path, monkeypatch):
    """每个测试都用一个全新的空数据库。

    tmp_path 是 pytest 给的临时目录，每个测试都不一样，跑完自动删。

    这里的关键是替换 `app.routers.scores.db` 这个函数。
    路由里所有地方都调 db() 拿连接，所以换掉 db()，
    整个服务就都指向临时数据库了 —— 不用改任何业务代码。

    这就是"依赖注入"的雏形：
        路由不自己决定用哪个数据库，它只是"调用 db()"，
        谁提供 db() 谁说了算。测试就利用了这一点。
    """
    db_file = tmp_path / "test.db"

    def _db():
        return dbmod.get_conn(db_file)

    # 让路由用临时数据库
    monkeypatch.setattr(scores_router, "db", _db)

    # 建表
    conn = _db()
    create_table(conn)
    conn.close()

    # 不用 with，避免触发 main.py 的 startup 去连真实数据库
    yield TestClient(app)


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["message"] == "成绩服务已启动"


def test_empty_list(client):
    """空数据库返回 []，不是 {}，也不是 None。"""
    r = client.get("/scores")
    assert r.status_code == 200
    assert r.json() == []


def test_add_then_list(client):
    r = client.post("/scores", json={"course": "数学", "score": 80})
    assert r.status_code == 200
    assert r.json() == {"course": "数学", "score": 80.0, "updated": False}

    r = client.get("/scores")
    assert r.status_code == 200
    assert r.json() == [{"course": "数学", "score": 80.0}]


def test_order_by_score_desc(client):
    """列表按分数从高到低。"""
    for name, score in [("数学", 80), ("英语", 100), ("物理", 90)]:
        client.post("/scores", json={"course": name, "score": score})
    r = client.get("/scores")
    assert [x["course"] for x in r.json()] == ["英语", "物理", "数学"]


def test_update_returns_updated_true(client):
    client.post("/scores", json={"course": "数学", "score": 80})
    r = client.post("/scores", json={"course": "数学", "score": 95})
    assert r.json()["updated"] is True
    assert r.json()["score"] == 95.0
    # 改分不该新增一门
    assert len(client.get("/scores").json()) == 1


def test_get_one(client):
    client.post("/scores", json={"course": "数学", "score": 80})
    r = client.get("/scores/数学")
    assert r.status_code == 200
    assert r.json() == {"course": "数学", "score": 80.0}


def test_get_one_404(client):
    r = client.get("/scores/化学")
    assert r.status_code == 404
    assert r.json()["detail"] == "没有这门课"


def test_get_zero_score_is_not_404(client):
    """0 分是合法成绩，不能当成"没这门课"。"""
    client.post("/scores", json={"course": "数学", "score": 0})
    r = client.get("/scores/数学")
    assert r.status_code == 200
    assert r.json() == {"course": "数学", "score": 0.0}


def test_delete(client):
    client.post("/scores", json={"course": "数学", "score": 80})
    r = client.delete("/scores/数学")
    assert r.status_code == 200
    assert r.json() == {"deleted": True, "course": "数学"}
    assert client.get("/scores").json() == []


def test_delete_404(client):
    r = client.delete("/scores/化学")
    assert r.status_code == 404


def test_stats(client):
    for name, score in [("数学", 80), ("英语", 100)]:
        client.post("/scores", json={"course": name, "score": score})
    r = client.get("/scores/stats/summary")
    assert r.status_code == 200
    assert r.json() == {"count": 2, "average": 90.0, "best": "英语"}


def test_stats_empty(client):
    """空表统计：count=0，average=0，best=None。"""
    r = client.get("/scores/stats/summary")
    assert r.status_code == 200
    assert r.json() == {"count": 0, "average": 0, "best": None}


def test_validation(client):
    """自动校验：超范围的进不来。"""
    assert client.post("/scores", json={"course": "体育", "score": 150}).status_code == 422
    assert client.post("/scores", json={"course": "体育", "score": -5}).status_code == 422
    assert client.post("/scores", json={"course": "", "score": 60}).status_code == 422
    assert client.post("/scores", json={"score": 60}).status_code == 422
    # 被拦下的不该进数据库
    assert client.get("/scores").json() == []


def test_openapi_available(client):
    """/docs 能打开的前提：openapi.json 能生成。"""
    r = client.get("/openapi.json")
    assert r.status_code == 200
    paths = r.json()["paths"]
    assert "/scores" in paths
    assert "/scores/{course}" in paths
    assert "/scores/stats/summary" in paths
