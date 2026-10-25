# -*- coding: utf-8 -*-
r"""
第 11 天：把数据库接进 FastAPI
===============================

运行方式（在 doc-assistant 目录下）：
    .\dev.cmd run day11_sqlite_api.py

这个文件会 import 你昨天写的 day10_sqlite.py。
如果昨天的函数写错了，今天会直接报错——这是故意的。

你要写的是 4 个路由：

    GET  /scores          返回所有课程
    GET  /scores/{course} 返回一门课，没有则 404
    POST /scores          新增或修改，返回改后的数据
    GET  /stats           返回统计信息
"""

import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

# 复用第 10 天的函数
from day10_sqlite import (
    stats,
    add_course,
    get_all,
    get_one,
    get_conn,
    create_table,
    update_score,
)


# ============================================================
# 准备
# ============================================================

BASE_DIR = Path(__file__).parent
TMP_DIR = BASE_DIR / ".tmp"
DB_PATH = TMP_DIR / "day11_courses.db"

app = FastAPI(title="课程成绩管理")


class ScoreIn(BaseModel):
    """POST 请求的请求体。

    Field(...) 是校验规则，和第 7 天一样：
        ge=0 / le=100  →  分数必须在 0 到 100 之间
        min_length=1   →  课程名不能是空字符串
    """
    course: str = Field(min_length=1, max_length=20)
    score: float = Field(ge=0, le=100)


def db():
    """每次请求开一个新连接。

    为什么不用模块级的全局 conn？
        FastAPI 默认用线程池处理请求，同一个 sqlite3.Connection
        被多个线程同时用会出问题（sqlite3 默认禁止跨线程）。
        每次开一个新的最简单、最不容易错。
    """
    conn = get_conn(DB_PATH)
    create_table(conn)
    return conn


# ============================================================
# 你的任务：4 个路由
# ============================================================
#
# 每个路由都要自己做三件事：
#   1. conn = db()            开连接
#   2. 干活（调第 10 天的函数）
#   3. conn.close()           关连接
#
# 别忘了 finally 或干脆在每个 return 前关。
# 简单起见，可以写成：
#   conn = db()
#   try:
#       ...你的代码...
#   finally:
#       conn.close()


@app.get("/scores")
def list_scores():
    """返回所有课程，按分数从高到低。

    返回格式：
        [{"course": "英语", "score": 100.0}, ...]

    要做的事：
        1. conn = db()
        2. rows = get_all(conn)          ← 第 10 天的函数，返回 [("英语", 100.0), ...]
        3. 把每个元组转成字典 {"course": 名字, "score": 分数}
        4. conn.close()
        5. return 那个列表

    提示：
        result = []
        for name, score in rows:
            result.append({"course": name, "score": score})
    """
    # TODO: 在这里写代码
    conn = db()
    rows = get_all(conn)
    result = []
    for name,score in rows:
        result.append({"course":name,"score":score})
    conn.close()
    return result




@app.get("/scores/{course}")
def get_one_score(course: str):
    """返回一门课。

    返回格式：
        {"course": "数学", "score": 80.0}

    找不到时：
        抛 HTTPException(status_code=404, detail="没有这门课")
        → 客户端收到 {"detail": "没有这门课"}，状态码 404

    要做的事：
        1. conn = db()
        2. score = get_one(conn, course)   ← 第 10 天的函数，找不到返回 None
        3. 如果 score is None → raise HTTPException(404, ...)
        4. 否则返回 {"course": course, "score": score}

    注意：
        这里的 course 参数来自 URL，比如 /scores/数学 就会传进来 "数学"。
        FastAPI 自动帮你从 URL 里取，不用自己解析。
    """
    # TODO: 在这里写代码

    conn = db()
    score = get_one(conn,course)
    if score is None:
        raise HTTPException(status_code=404,detail="没有这门课")
    return {"course":course,"score":score}





@app.post("/scores")
def set_score(item: ScoreIn):
    """新增或修改一门课的成绩。

    返回格式：
        {"course": "数学", "score": 95.0, "updated": True}

        updated 是 True 表示"改的"，False 表示"新加的"。

    要做的事：
        1. conn = db()
        2. 先看这门课在不在：old = get_one(conn, item.course)
        3. 如果 old is None → add_course(conn, item.course, item.score)，updated = False
           否则            → update_score(conn, item.course, item.score)，updated = True
        4. 返回 {"course": ..., "score": ..., "updated": ...}

    注意：
        item 是 ScoreIn 对象，用 item.course 和 item.score 取值，不是 item["course"]。
        （因为它是 Pydantic 模型，不是字典）

        分数范围已经由 ScoreIn 的 Field 校验了：
        传 150 分会被 FastAPI 自动拦成 422，根本进不到这个函数。
    """
    # TODO: 在这里写代码
    conn = db()
    old = get_one(conn,item.course)
    if old is None:
        add_course(conn,item.course,item.score)
        code = False
    else:
        update_score(conn,item.course,item.score)
        code = True
    conn.close()
    return {"course":item.course,"score":item.score,"updated":code}


@app.get("/stats")
def get_stats():
    """返回统计信息。

    返回格式：
        {"count": 3, "average": 95.0, "best": "英语"}

    要做的事：
        1. conn = db()
        2. 直接调用第 10 天写的 stats(conn)   ← 注意要先 import 它
        3. conn.close()
        4. return 那个字典

    提示：
        这个路由最短。如果你写的 stats 是对的，这里只需要两行。
        需要把 stats 加到文件顶部的 import 里。
    """
    # TODO: 在这里写代码
    conn = db()
    result = stats(conn)
    conn.close()
    return result


# ============================================================
# 自测（不用改）
# ============================================================

def reset_db():
    """清空数据库，让每次测试从干净状态开始。"""
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = db()
    conn.close()


def run_tests():
    print("=" * 60)
    print("自测")
    print("=" * 60)

    client = TestClient(app)
    passed = 0
    failed = 0

    def check(label, cond, extra=""):
        nonlocal passed, failed
        if cond:
            print(f"  [通过] {label}")
            passed += 1
        else:
            print(f"  [未通过] {label}")
            if extra:
                print(f"      {extra}")
            failed += 1

    def j(r):
        """安全地取 JSON。路由还没写时返回的是 null，r.json() 会是 None，
        直接 .get() 会崩掉整个自测，所以统一在这里兜一下。"""
        try:
            data = r.json()
        except Exception:
            return {}
        return data if data is not None else {}

    def run(label, fn):
        """跑一步，出错只记一条，不中断后面的测试。"""
        try:
            return fn()
        except Exception as e:
            check(f"{label} 执行时报错", False, f"{type(e).__name__}: {e}")
            return None

    # ---------- 1. 空数据库 ----------
    print("\n1. 空数据库")
    reset_db()
    r = run("GET /scores", lambda: client.get("/scores"))
    if r is not None:
        check("GET /scores 状态码 200", r.status_code == 200, f"实际 {r.status_code}")
        check("空数据库返回空列表", j(r) == [], f"实际 {r.text}")

    r = run("GET /stats", lambda: client.get("/stats"))
    if r is not None:
        check(
            "空数据库的统计",
            j(r) == {"count": 0, "average": 0, "best": None},
            f"实际 {r.text}",
        )

    # ---------- 2. 新增 ----------
    print("\n2. POST 新增")
    r = run("POST 数学", lambda: client.post("/scores", json={"course": "数学", "score": 80}))
    if r is not None:
        check("新增数学 200", r.status_code == 200, f"实际 {r.status_code}")
        check(
            "新增返回 updated=False",
            r.status_code == 200 and j(r).get("updated") is False,
            f"实际 {r.text}",
        )

    r = run("POST 物理", lambda: client.post("/scores", json={"course": "物理", "score": 90}))
    if r is not None:
        check("新增物理 200", r.status_code == 200, f"实际 {r.status_code}")
    r = run("POST 英语", lambda: client.post("/scores", json={"course": "英语", "score": 100}))
    if r is not None:
        check("新增英语 200", r.status_code == 200, f"实际 {r.status_code}")

    # ---------- 3. 查询全部 ----------
    print("\n3. GET /scores")
    r = run("GET /scores", lambda: client.get("/scores"))
    if r is not None:
        data = j(r)
        if not isinstance(data, list):
            check("GET /scores 返回的是列表", False, f"实际 {r.text}")
        else:
            check("三门课", len(data) == 3, f"实际 {r.text}")
            check(
                "按分数从高到低",
                [x.get("course") for x in data] == ["英语", "物理", "数学"],
                f"实际 {[x.get('course') for x in data]}",
            )
            check(
                "字段名是 course/score",
                bool(data) and set(data[0].keys()) == {"course", "score"},
                f"实际 {data[0] if data else None}",
            )

    # ---------- 4. 查询单门 ----------
    print("\n4. GET /scores/{course}")
    r = run("GET /scores/数学", lambda: client.get("/scores/数学"))
    if r is not None:
        check("查数学 200", r.status_code == 200, f"实际 {r.status_code}")
        check(
            "数学是 80",
            r.status_code == 200 and j(r).get("score") == 80.0,
            f"实际 {r.text}",
        )

    r = run("GET /scores/化学", lambda: client.get("/scores/化学"))
    if r is not None:
        check("查不存在的化学 404", r.status_code == 404, f"实际 {r.status_code}")

    # ---------- 5. 修改 ----------
    print("\n5. POST 修改")
    r = run("POST 数学 95", lambda: client.post("/scores", json={"course": "数学", "score": 95}))
    if r is not None:
        check("改数学 200", r.status_code == 200, f"实际 {r.status_code}")
        check(
            "修改返回 updated=True",
            r.status_code == 200 and j(r).get("updated") is True,
            f"实际 {r.text}",
        )
    r = run("GET /scores/数学", lambda: client.get("/scores/数学"))
    if r is not None:
        check(
            "改完是 95",
            r.status_code == 200 and j(r).get("score") == 95.0,
            f"实际 {r.text}",
        )
    r = run("GET /scores", lambda: client.get("/scores"))
    if r is not None:
        data = j(r)
        check(
            "改分后还是三门（不是新增）",
            isinstance(data, list) and len(data) == 3,
            f"实际 {r.text}",
        )

    # ---------- 6. 校验 ----------
    print("\n6. 参数校验（这些应该由 FastAPI 自动拦下）")
    for label, payload in [
        ("150 分", {"course": "作弊", "score": 150}),
        ("-5 分", {"course": "负数", "score": -5}),
        ("空课程名", {"course": "", "score": 60}),
        ("缺 course 字段", {"score": 60}),
    ]:
        r = run(f"POST {label}", lambda p=payload: client.post("/scores", json=p))
        if r is not None:
            check(f"{label}被拦成 422", r.status_code == 422, f"实际 {r.status_code}")

    # ---------- 7. 统计 ----------
    print("\n7. GET /stats")
    r = run("GET /stats", lambda: client.get("/stats"))
    if r is not None:
        check(
            "统计结果",
            j(r) == {"count": 3, "average": 95.0, "best": "英语"},
            f"实际 {r.text}",
        )

    # ---------- 8. 数据持久化 ----------
    print("\n8. 数据真的写进磁盘了吗")
    check("数据库文件存在", DB_PATH.exists())
    if DB_PATH.exists():
        conn = get_conn(DB_PATH)
        row = conn.execute("SELECT COUNT(*) AS n FROM courses").fetchone()
        conn.close()
        check("文件里有 3 条记录", row["n"] == 3, f"实际 {row['n']}")

    # ---------- 收尾 ----------
    print("\n" + "=" * 60)
    print(f"通过 {passed} 条，失败 {failed} 条")
    if failed == 0:
        print("全部通过，第 11 天完成。")
    else:
        print("还有失败项，按上面的提示改。")
    print("=" * 60)

    # 清理
    if DB_PATH.exists():
        DB_PATH.unlink()


if __name__ == "__main__":
    run_tests()
