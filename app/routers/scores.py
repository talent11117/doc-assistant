# -*- coding: utf-8 -*-
"""routers/scores.py —— 只管路由。

判断标准：
    有 @router.get / @router.post 的      -> 放这个文件
    有 SQL 的                              -> 不该放（去 database.py）
    有 Pydantic 类的                      -> 不该放（去 models.py）

这个文件的规矩：**每个函数都很短，因为它只做三件事**
    1. 开连接
    2. 调 database.py 里的函数
    3. 关连接，把结果转成 JSON

真正的活儿都在 database.py 里。路由不该写 SQL。

⚠️ 注意这里用的是 router，不是 app：
    router = APIRouter()      ← 小一号的 app
    @router.get("/scores")    ← 用 router 装饰

    app 在 main.py 里，router 挂到 app 上。
    这样 routers/scores.py 不需要 import main.py（否则就循环 import 了）。
"""

from fastapi import APIRouter, HTTPException

from app.database import (
    add_course,
    create_table,
    delete_course,
    get_all,
    get_conn,
    get_one,
    stats,
    update_score,
)
from app.models import ScoreIn

# 小一号的 app。可以加前缀和标签，让 /docs 分组更清楚。
router = APIRouter(
    prefix="/scores",       # 这个文件里所有路径前面都自动加 /scores
    tags=["成绩"],           # /docs 里归到"成绩"这一组
)


def db():
    """每次请求开一个新连接。

    为什么不在文件顶部开一个全局的？
        因为 sqlite3 的连接默认不能跨线程用。FastAPI 处理请求是并发的，
        共用一个连接会报 "SQLite objects created in a thread can only be
        used in that same thread"。

    为什么不在这里建表？
        建表只需要一次，放在 main.py 启动时做。
        每个请求都 CREATE TABLE IF NOT EXISTS 也行，但没必要。
    """
    return get_conn()


# ============================================================
# 已经给你写好的第一个：照着它的形状写下面 4 个
# ============================================================

@router.get("")
def list_scores():
    """GET /scores —— 返回全部课程，按分数从高到低。

    返回格式：
        [{"course": "英语", "score": 100.0}, {"course": "数学", "score": 80.0}]

    注意：
        @router.get("") 而不是 @router.get("/")
        因为 router 有 prefix="/scores"，空字符串拼出来正好是 /scores。
        写 "/" 会变成 /scores/ ，多一个斜杠，测试就对不上了。

    这段就是标准形状：
        conn = db()
        rows = get_all(conn)        ← database.py 的函数
        conn.close()
        return [...]
    """
    conn = db()
    rows = get_all(conn)
    conn.close()

    # rows 是 [("英语", 100.0), ...]，要转成字典列表
    return [{"course": name, "score": score} for name, score in rows]


# ============================================================
# 下面 4 个要你写
# ============================================================

@router.get("/{course}")
def get_one_score(course: str):
    """GET /scores/{course} —— 查一门课。

    返回格式：
        {"course": "数学", "score": 80.0}

    找不到时：
        raise HTTPException(status_code=404, detail="没有这门课")

    要做的事：
        1. conn = db()
        2. score = get_one(conn, course)     ← 找不到返回 None
        3. conn.close()
        4. 如果 score is None -> raise HTTPException(404, ...)
        5. 返回 {"course": course, "score": score}

    ⚠️ 必须用 `if score is None`，不能写 `if not score`。
       0 分是合法成绩，`not 0.0` 是 True，会把 0 分误判成"没这门课"。

    提示：
        你第 11 天写过一模一样的，只是那时路径写全了 /scores/{course}，
        现在 prefix 帮你加了 /scores，这里只写 /{course}。
    """
    # TODO: 在这里写代码（大约 6 行）
    conn = db()
    score = get_one(conn,course)
    conn.close()
    if score is None:
        raise HTTPException(404,"没有这门课")

    return {"course":course,"score":score}


@router.post("")
def set_score(item: ScoreIn):
    """POST /scores —— 新增或修改。

    返回格式：
        {"course": "数学", "score": 95.0, "updated": True}
        updated=True 表示改的，False 表示新加的。

    要做的事：
        1. conn = db()
        2. old = get_one(conn, item.course)
        3. 如果 old is None:
               add_course(conn, item.course, item.score)
               updated = False
           否则:
               update_score(conn, item.course, item.score)
               updated = True
        4. conn.close()
        5. 返回 {"course": ..., "score": ..., "updated": ...}

    提示：
        item 是 ScoreIn 对象，用 item.course / item.score 取值，不是 item["course"]。
        分数范围已经由 ScoreIn 的 Field 拦住了，你不用再判断。
    """
    # TODO: 在这里写代码（大约 10 行）
    conn = db()
    old = get_one(conn,item.course)
    if old is None:
        add_course(conn,item.course,item.score)
        updated = False
    else:
        update_score(conn,item.course,item.score)
        updated = True
    conn.close()
    return {"course":item.course,"score":item.score,"updated":updated}



@router.delete("/{course}")
def remove_score(course: str):
    """DELETE /scores/{course} —— 删一门课。

    返回格式：
        {"deleted": True, "course": "数学"}

    找不到时：
        raise HTTPException(status_code=404, detail="没有这门课")

    要做的事：
        1. conn = db()
        2. ok = delete_course(conn, course)    ← 返回 True/False
        3. conn.close()
        4. 如果 not ok -> raise HTTPException(404, ...)
        5. 返回 {"deleted": True, "course": course}

    这是第 11 天没有的新接口。加它是因为：
        拆完包之后，正好验证一下"加新功能是不是变容易了"。
        在单文件时代，你要在 250 行里找地方插；
        现在只要在 routers/scores.py 里加一个函数。

    提示：
        delete_course 已经 import 了，直接用。
    """
    # TODO: 在这里写代码（大约 7 行）
    conn = db()
    ok = delete_course(conn,course)
    conn.close()
    if not ok:
        raise HTTPException(status_code=404, detail="没有这门课")
    return {"deleted":True,"course":course}


@router.get("/stats/summary")
def get_stats():
    """GET /scores/stats/summary —— 统计。

    返回格式：
        {"count": 3, "average": 95.0, "best": "英语"}

    要做的事：
        1. conn = db()
        2. result = stats(conn)      ← database.py 里已经写好了
        3. conn.close()
        4. return result

    就 4 行。这是"复用"的极致：统计逻辑一行都不用重写。

    ⚠️ 路径为什么是 /stats/summary 而不是 /stats？
        因为上面有个 @router.get("/{course}")。
        FastAPI 按**注册顺序**匹配，如果这里写 "/stats"，
        访问 /scores/stats 会先被 /{course} 抓住，course="stats"，
        然后返回 404「没有这门课」。

        加个 /summary 段，路径就不会和单参数路由冲突了。
        （另一种办法是把 /stats 写在 /{course} 前面，也能work。
          但"路径不重叠"比"依赖注册顺序"更不容易出错。）
    """
    # TODO: 在这里写代码（大约 4 行）
    conn = db()
    result = stats(conn)
    conn.close()
    return result
