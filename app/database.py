# -*- coding: utf-8 -*-
"""database.py —— 只管数据库。

这个文件的规矩：**只有 SQL，没有 HTTP**。

判断标准：
    函数里出现 conn.execute(...)     -> 放这个文件
    函数里出现 @router.get(...)      -> 不该放这个文件
    函数里出现 HTTPException         -> 不该放这个文件

为什么要把数据库单独放一个文件？
    1. 测试时可以单独测数据库层，不用启动整个 web 服务
    2. 将来换数据库（SQLite -> PostgreSQL），只改这一个文件
    3. 路由文件会变得很短，一眼能看完
"""

import sqlite3
from pathlib import Path

# ============================================================
# 数据库放在哪
# ============================================================
#
# __file__ 是"当前这个文件"的路径，即 app/database.py
# .parent        -> app/
# .parent.parent -> doc-assistant/
#
# 所以 BASE_DIR 永远是 doc-assistant/，不管你在哪个目录运行 python。
# 这就是为什么用 __file__ 而不是 "." —— "." 是"你敲命令时所在的目录"，
# 换个目录跑就找不到数据库了。

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / ".tmp" / "app_courses.db"


def get_conn(db_path=DB_PATH):
    """打开一个连接，并让查出来的行可以按列名取值。

    参数 db_path 有默认值，所以平时直接 get_conn() 就行。
    测试时传临时路径进来，避免弄脏真正的数据库。
    """
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    # row_factory = sqlite3.Row 之后，row["name"] 和 row[0] 都能用
    conn.row_factory = sqlite3.Row
    return conn


def create_table(conn):
    """建表。已存在就跳过。"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT    NOT NULL UNIQUE,
            score REAL    NOT NULL
        )
    """)
    conn.commit()


# ============================================================
# 增删改查
# ============================================================
#
# 注意每个函数都是"收一个 conn，干活，返回结果"。
# 它**自己不开连接、也不关连接** —— 开关连接是调用方（路由）的责任。
#
# 这个分工很重要：如果这里自己开连接，那么路由想在一个请求里
# 连续做三件事，就会开三个连接，还可能互相看不见对方没提交的数据。

def add_course(conn, name, score):
    """新增一门课。返回 True。"""
    conn.execute("INSERT INTO courses (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    return True


def get_all(conn):
    """返回全部课程，按分数从高到低。

    返回形状：[("英语", 100.0), ("数学", 80.0), ...]  —— 元组列表
    """
    rows = conn.execute(
        "SELECT name, score FROM courses ORDER BY score DESC"
    ).fetchall()
    return [(row["name"], row["score"]) for row in rows]


def get_one(conn, name):
    """查一门课的分数。查不到返回 None。

    ⚠️ 注意：分数为 0 时返回 0.0，不是 None。
    所以调用方判断"有没有"必须用 `if score is None`，不能用 `if not score`。
    """
    row = conn.execute(
        "SELECT score FROM courses WHERE name = ?", (name,)
    ).fetchone()
    if row is None:
        return None
    return row["score"]


def update_score(conn, name, score):
    """改一门课的分数。课程不存在返回 False。"""
    cur = conn.execute(
        "UPDATE courses SET score = ? WHERE name = ?", (score, name)
    )
    conn.commit()
    # rowcount 是"这次操作影响了几行"。0 就是没找到这门课。
    return cur.rowcount > 0


def delete_course(conn, name):
    """删一门课。课程不存在返回 False。"""
    cur = conn.execute("DELETE FROM courses WHERE name = ?", (name,))
    conn.commit()
    return cur.rowcount > 0


def stats(conn):
    """统计：几门、平均分、最高分那门。

    返回 {"count": 3, "average": 90.0, "best": "英语"}
    空表时返回 {"count": 0, "average": 0, "best": None}
    """
    row = conn.execute(
        "SELECT COUNT(*) AS n, AVG(score) AS avg FROM courses"
    ).fetchone()

    count = row["n"]
    if count == 0:
        return {"count": 0, "average": 0, "best": None}

    # 平均值保留两位小数，避免 90.33333333333333 这种
    average = round(row["avg"], 2)

    # 最高分那门课。空表已在上面 return 了，所以这里一定有行。
    best_row = conn.execute(
        "SELECT name FROM courses ORDER BY score DESC LIMIT 1"
    ).fetchone()

    return {"count": count, "average": average, "best": best_row["name"]}
