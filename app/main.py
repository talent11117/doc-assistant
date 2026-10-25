# -*- coding: utf-8 -*-
"""main.py —— 只管"启动"。

判断标准：这个文件应该只有 20 行左右。
    有 FastAPI()          -> 对，放这里
    有 include_router     -> 对，放这里
    有 SQL                -> 错，去 database.py
    有 @app.get 业务逻辑   -> 错，去 routers/

为什么要有一个 main.py？
    因为 uvicorn 需要一个"入口"告诉它：app 对象在哪。
        uvicorn app.main:app
                  ↑    ↑
                  │    └── 这个模块里名叫 app 的变量
                  └─────── 模块路径 app/main.py

    这就是 "app.main:app" 这串东西的全部含义。
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from app.database import create_table, get_conn
from app.routers import scores

# app/static 目录的绝对路径。
# __file__ 是当前文件的路径，.parent 是 app/ 目录，再拼 static。
STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """服务的"生命周期钩子"。

    yield 之前  = 服务启动时跑一次（这里：建表）
    yield 之后  = 服务关闭时跑一次（这里没写，因为不需要清理）

    为什么必须写 async 和 yield？
        因为 FastAPI 要支持"启动时建立连接池、关闭时释放"这种成对的操作，
        所以用一个能"暂停"的函数把启动和关闭包在一起。
        asynccontextmanager 就是把这种写法变简单的工具。
    """
    conn = get_conn()
    create_table(conn)
    conn.close()

    yield          # ← 服务在这里"开始对外提供服务"


app = FastAPI(
    title="课程成绩管理服务",
    description="第 13 天的重构成果：单文件拆成 app/ 包",
    version="1.0.0",
    lifespan=lifespan,
    # 关掉 FastAPI 自带的 /docs。
    # 自带的那份从 cdn.jsdelivr.net 加载 Swagger UI，而国内经常连不上，
    # 结果就是打开 /docs 一片空白。下面我们自己写一个用本地文件的版本。
    docs_url=None,
    redoc_url=None,
)

# 把 app/static 目录挂到 /static 路径上。
# 挂上之后，浏览器请求 /static/swagger-ui.css 就能拿到 app/static/swagger-ui.css。
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui():
    """自己写的 /docs 页面：Swagger UI 从本地 /static 加载，不碰外网 CDN。"""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
    )


# ============================================================
# 启动时建表（已在上面用 lifespan 完成）
# ============================================================
#
# 老写法是 @app.on_event("startup")，但新版 FastAPI 已标记为 deprecated。
# 现在统一用 lifespan，写在上面的 asynccontextmanager 里。
#
# 两种写法的区别：
#     on_event   —— 只能"启动时做一件事"，没法配对做清理
#     lifespan   —— 一个函数里同时管启动和关闭（yield 前 / 后），成对出现
#
# 这就是为什么官方要换：真实项目经常需要"启动时开连接池，关闭时关掉"，
# on_event 得写两个函数，还容易漏掉关闭那一半。


# ============================================================
# 把路由挂上来
# ============================================================
#
# include_router 就是"把小的挂到大的上"。
# scores.router 里有 prefix="/scores"，所以最终路径是：
#       /scores          GET   -> list_scores
#       /scores/{course} GET   -> get_one_score
#       /scores          POST  -> set_score
#       /scores/{course} DELETE-> remove_score
#       /scores/stats/summary  -> get_stats
#
# 想加统一前缀（比如所有接口都变成 /api/scores）：
#       app.include_router(scores.router, prefix="/api")

app.include_router(scores.router)


@app.get("/")
def read_root():
    """根路径。访问 http://127.0.0.1:8000/ 时返回这句话。"""
    return {"message": "成绩服务已启动", "docs": "/docs"}
