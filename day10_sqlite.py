# -*- coding: utf-8 -*-
r"""
第 10 天：SQLite —— 把数据从 JSON 文件搬进数据库
================================================

运行方式（在 doc-assistant 目录下）：
    .\dev.cmd run day10_sqlite.py

这个文件分三段：

    演示 1   最小的建表 / 插入 / 查询        ← 读懂，不用改
    演示 2   为什么绝对不能用 f-string 拼 SQL  ← 读懂，这一段最重要
    你的任务  6 个函数                        ← 你来写

写完之后，最后会自动跑 12 条自测。
"""

import sqlite3
from pathlib import Path


# ============================================================
# 准备：数据库文件放哪
# ============================================================

# Path(__file__).parent 就是"本文件所在的目录"
# 这样不管你在哪个目录运行，数据库文件都建在同一个地方
BASE_DIR = Path(__file__).parent
TMP_DIR = BASE_DIR / ".tmp"
DB_PATH = TMP_DIR / "day10_courses.db"


def get_conn(db_path=DB_PATH):
    """打开一个数据库连接，并且让查出来的行可以用列名取值。

    参数 db_path 有默认值，所以大多数时候直接 get_conn() 就行。
    自测会传一个临时路径进来，避免弄脏真正的数据库。
    """
    # 目录可能还不存在（.tmp 被删掉的情况），先确保它存在
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)

    # row_factory = sqlite3.Row 之后：
    #   查出来的每一行既能 row[0] 按位置取值，也能 row["name"] 按列名取值
    # 不加的话，查出来是普通元组，只能 row[0]
    conn.row_factory = sqlite3.Row

    return conn


def create_table(conn):
    """建表。如果表已经存在就跳过（IF NOT EXISTS）。"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT    NOT NULL UNIQUE,
            score REAL    NOT NULL
        )
    """)
    conn.commit()


# ============================================================
# 演示 1：最小的建表 / 插入 / 查询
# ============================================================

def demo_basic():
    print("=" * 60)
    print("演示 1：最小的建表 / 插入 / 查询")
    print("=" * 60)

    conn = get_conn()
    create_table(conn)

    # 清空，保证每次运行结果一样
    conn.execute("DELETE FROM courses")
    conn.commit()

    # 插入：? 是占位符，第二个参数是元组，按顺序填进去
    conn.execute("INSERT INTO courses (name, score) VALUES (?, ?)", ("数学", 80))
    conn.execute("INSERT INTO courses (name, score) VALUES (?, ?)", ("物理", 90))
    conn.execute("INSERT INTO courses (name, score) VALUES (?, ?)", ("英语", 100))
    conn.commit()          # ← 忘了这一句，数据就只在内存里，关掉连接就没了

    print("\n插入 3 条之后，全部查出来：")
    rows = conn.execute("SELECT name, score FROM courses").fetchall()
    for row in rows:
        # 因为设了 row_factory = sqlite3.Row，这里可以按列名取值
        print(f"  {row['name']}  {row['score']}")

    print("\n只看分数 >= 90 的：")
    rows = conn.execute(
        "SELECT name, score FROM courses WHERE score >= ? ORDER BY score DESC",
        (90,),
    ).fetchall()
    for row in rows:
        print(f"  {row['name']}  {row['score']}")

    print("\n只看一门课：")
    row = conn.execute(
        "SELECT name, score FROM courses WHERE name = ?", ("物理",)
    ).fetchone()
    if row is None:
        print("  没找到")
    else:
        print(f"  找到了：{row['name']} = {row['score']}")

    print("\n统计：")
    row = conn.execute(
        "SELECT COUNT(*) AS n, AVG(score) AS avg, MAX(score) AS mx FROM courses"
    ).fetchone()
    print(f"  共 {row['n']} 门，平均 {row['avg']}，最高 {row['mx']}")

    conn.close()
    print()


# ============================================================
# 演示 2：为什么绝对不能用 f-string 拼 SQL
# ============================================================

def demo_injection():
    print("=" * 60)
    print("演示 2：SQL 注入 —— 为什么必须用 ? 占位符")
    print("=" * 60)

    conn = get_conn()
    create_table(conn)
    conn.execute("DELETE FROM courses")
    conn.execute("INSERT INTO courses (name, score) VALUES (?, ?)", ("数学", 80))
    conn.execute("INSERT INTO courses (name, score) VALUES (?, ?)", ("物理", 90))
    conn.execute("INSERT INTO courses (name, score) VALUES (?, ?)", ("英语", 100))
    conn.commit()

    # ---------- 先看正确的写法 ----------
    print("\n【正确】用 ? 占位符，查 name = 数学：")
    rows = conn.execute(
        "SELECT name, score FROM courses WHERE name = ?", ("数学",)
    ).fetchall()
    print(f"  查到 {len(rows)} 条")
    for row in rows:
        print(f"    {row['name']}  {row['score']}")

    # ---------- 再看错误写法会被攻破 ----------
    # 假设这个变量来自用户的输入（比如 URL 里的 ?course=xxx）
    user_input = "数学' OR '1'='1"

    print(f"\n【错误】用 f-string 拼接，用户输入是：{user_input}")
    bad_sql = f"SELECT name, score FROM courses WHERE name = '{user_input}'"
    print(f"  实际执行的 SQL：")
    print(f"    {bad_sql}")

    try:
        rows = conn.execute(bad_sql).fetchall()
        print(f"  查到 {len(rows)} 条：")
        for row in rows:
            print(f"    {row['name']}  {row['score']}")
        print("\n  >>> 看明白了吗？本来只想查'数学'，结果把全部 3 门都查出来了。")
        print("  >>> 因为 '1'='1' 永远成立，OR 一下就把 WHERE 条件废掉了。")
    except sqlite3.Error as e:
        print(f"  出错了：{e}")

    print(f"\n【正确】同样的输入，用 ? 占位符：")
    rows = conn.execute(
        "SELECT name, score FROM courses WHERE name = ?", (user_input,)
    ).fetchall()
    print(f"  查到 {len(rows)} 条")
    if len(rows) == 0:
        print("  >>> 一条都没有。因为 ? 会把整个字符串当成一个'值'去比较，")
        print("  >>> 而不是当成 SQL 语句的一部分。这就是它能防注入的原因。")

    print("\n  记住一句话：")
    print("    用户输入永远是数据，不是代码。")
    print("    ? 占位符保证它只是数据。")
    print("    f-string 会把数据当成代码拼进去。")

    conn.close()
    print()


# ============================================================
# 你的任务：6 个函数
# ============================================================
#
# 规则：
#   1. 每个函数都用传进来的 conn 参数，不要自己 get_conn()
#   2. 写完一个就运行一次，别一口气写 6 个
#   3. SQL 里必须用 ? 占位符，不许用 f-string 拼
#
# 提示：下面几个 SQL 你大概率会用到
#   SELECT ... FROM courses
#   INSERT INTO courses (name, score) VALUES (?, ?)
#   UPDATE courses SET score = ? WHERE name = ?
#   DELETE FROM courses WHERE name = ?
#   COUNT(*) / AVG(score) / MAX(score)


def add_course(conn, name, score):
    """新增一门课。

    参数：
        conn   数据库连接
        name   课程名，字符串
        score  分数，数字
    返回：
        没有返回值（return None 或不写 return）

    要做的事：
        1. 往 courses 表插一条记录
        2. 记得 commit()
        3. 如果课程名已经存在会怎样？—— UNIQUE 约束会抛 sqlite3.IntegrityError。
           这一条先不用管，让它抛出去就行（自测不会测这个）。

    提示：
        conn.execute("INSERT INTO courses (name, score) VALUES (?, ?)", (name, score))
        conn.commit()
    """
    # TODO: 在这里写代码
    pass


def get_all(conn):
    """查出所有课程，按分数从高到低排序。

    返回：
        一个列表，每个元素是 (课程名, 分数) 的元组
        例如 [("英语", 100.0), ("物理", 90.0), ("数学", 80.0)]

    要做的事：
        1. 写 SELECT 语句，ORDER BY score DESC
        2. fetchall() 拿到结果
        3. 把每一行转成普通元组 (row["name"], row["score"])

    为什么最后要转成普通元组？
        因为自测要和 [("英语", 100.0), ...] 这样的列表比较。
        sqlite3.Row 对象不能直接和元组比大小。

    提示：
        rows = conn.execute("SELECT name, score FROM courses ORDER BY score DESC").fetchall()
        result = []
        for row in rows:
            result.append((row["name"], row["score"]))
        return result
    """
    # TODO: 在这里写代码
    pass


def get_one(conn, name):
    """查一门课的分数。

    返回：
        找到就返回分数（数字），找不到返回 None

    要做的事：
        1. SELECT score FROM courses WHERE name = ?
        2. fetchone()
        3. 如果结果是 None，返回 None；否则返回 row["score"]

    提示：
        注意区分：fetchone() 返回 None 表示"没这行"，
        而不是"这行的分数是 0"。所以不能写成 row["score"] if row else 0
    """
    # TODO: 在这里写代码
    pass


def update_score(conn, name, score):
    """把一门课的分数改成新的值。

    返回：
        改成功了返回 True，课程不存在返回 False

    要做的事：
        1. UPDATE courses SET score = ? WHERE name = ?
        2. commit()
        3. 怎么知道改没改到？
           cursor = conn.execute(...)
           cursor.rowcount  ← 受影响的行数，0 表示没找到这门课

    提示：
        cur = conn.execute("UPDATE courses SET score = ? WHERE name = ?", (score, name))
        conn.commit()
        return cur.rowcount > 0
    """
    # TODO: 在这里写代码
    pass


def delete_course(conn, name):
    """删掉一门课。

    返回：
        删掉了返回 True，课程不存在返回 False

    要做的事：
        和 update_score 几乎一样，只是 SQL 换成 DELETE
    """
    # TODO: 在这里写代码
    pass


def stats(conn):
    """统计信息。

    返回：
        一个字典，三个键：
        {"count": 课程数, "average": 平均分, "best": 最高分的课程名}

        如果一门课都没有，返回：
        {"count": 0, "average": 0, "best": None}

    要做的事：
        1. 用 COUNT(*) / AVG(score) 查数量和平均分
        2. 用 ORDER BY score DESC LIMIT 1 查最高分的课程名
        3. 组装成字典返回

    提示：
        COUNT(*) 在没有数据时返回 0（不是 None）
        AVG(score) 在没有数据时返回 None（不是 0）← 这个坑要注意
        所以空表要单独判断，或者用 avg or 0

    这是第 3 天"空字典返回什么"那个问题的续集。
    """
    # TODO: 在这里写代码
    pass


# ============================================================
# 自测（不用改）
# ============================================================

def check(label, got, want):
    if got == want:
        print(f"  [通过] {label}")
    else:
        print(f"  [未通过] {label}")
        print(f"      你写的：{got!r}")
        print(f"      应该是：{want!r}")


def safe(label, want, fn):
    """跑一个函数并比较结果。函数报错时只记一条 [报错]，不中断整个自测。"""
    try:
        got = fn()
    except Exception as e:
        print(f"  [报错] {label}")
        print(f"      {type(e).__name__}: {e}")
        return
    check(label, got, want)


def run_tests():
    print("=" * 60)
    print("自测")
    print("=" * 60)

    # 用一个独立的测试数据库，不碰真正的 day10_courses.db
    test_db = TMP_DIR / "day10_test.db"
    if test_db.exists():
        test_db.unlink()

    conn = get_conn(test_db)
    create_table(conn)

    print("\n1. add_course：加三门课")
    safe("加数学 80", None, lambda: add_course(conn, "数学", 80))
    safe("加物理 90", None, lambda: add_course(conn, "物理", 90))
    safe("加英语 100", None, lambda: add_course(conn, "英语", 100))

    print("\n2. get_all：按分数从高到低")
    safe(
        "三门课的顺序",
        [("英语", 100.0), ("物理", 90.0), ("数学", 80.0)],
        lambda: get_all(conn),
    )

    print("\n3. get_one：查单门")
    safe("查数学", 80.0, lambda: get_one(conn, "数学"))
    safe("查不存在的化学", None, lambda: get_one(conn, "化学"))

    print("\n4. update_score：改分")
    safe("改数学为 95 返回 True", True, lambda: update_score(conn, "数学", 95))
    safe("改完再查是 95", 95.0, lambda: get_one(conn, "数学"))
    safe("改不存在的课返回 False", False, lambda: update_score(conn, "化学", 60))

    print("\n5. stats：统计")
    safe(
        "三门课的统计",
        {"count": 3, "average": 95.0, "best": "英语"},
        lambda: stats(conn),
    )

    print("\n6. delete_course：删课")
    safe("删英语返回 True", True, lambda: delete_course(conn, "英语"))
    safe("删完只剩两门", 2, lambda: stats(conn)["count"] if stats(conn) else None)
    safe("删不存在的课返回 False", False, lambda: delete_course(conn, "英语"))

    print("\n7. 空表的边界情况")
    safe("删物理", True, lambda: delete_course(conn, "物理"))
    safe("删数学", True, lambda: delete_course(conn, "数学"))
    safe(
        "空表统计",
        {"count": 0, "average": 0, "best": None},
        lambda: stats(conn),
    )
    safe("空表 get_all", [], lambda: get_all(conn))

    conn.close()
    if test_db.exists():
        test_db.unlink()

    print("\n" + "=" * 60)
    print("全 [通过] 就算完成第 10 天。")
    print("有 [未通过] 的话，上面会同时打印'你写的'和'应该是'。")
    print("=" * 60)


if __name__ == "__main__":
    demo_basic()
    demo_injection()
    run_tests()
