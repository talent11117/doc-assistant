# 课程成绩管理服务

一个用 FastAPI + SQLite 写的课程成绩管理后端，支持增删改查和统计。

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.144-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![pytest](https://img.shields.io/badge/tests-14%20passed-brightgreen?logo=pytest&logoColor=white)](#测试)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## 功能

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/scores` | 查询所有课程成绩，按分数从高到低 |
| `GET` | `/scores/{course}` | 查询单门成绩，不存在返回 `404` |
| `POST` | `/scores` | 新增或修改成绩，自动校验分数在 0—100 |
| `DELETE` | `/scores/{course}` | 删除指定课程，不存在返回 `404` |
| `GET` | `/scores/stats/summary` | 统计课程数、平均分、最高分课程 |

字段校验由 Pydantic 自动完成，非法输入返回 `422` 并说明具体原因：

```json
{
  "detail": [{
    "type": "string_too_short",
    "loc": ["body", "course"],
    "msg": "String should have at least 1 character",
    "input": ""
  }]
}
```

## 技术栈

| 组件 | 版本 | 用途 |
|---|---|---|
| Python | 3.12.6 | 运行环境 |
| FastAPI | 0.144.0 | Web 框架、自动生成 OpenAPI 文档 |
| Pydantic | 2.14.1 | 请求/响应模型与字段校验 |
| SQLite | 3（标准库 `sqlite3`） | 数据存储，无需额外安装 |
| pytest | 9.1.1 | 接口测试 |
| uvicorn | 0.54.0 | ASGI 服务器 |

## 怎么跑起来

### 前置要求

- Python 3.12 或更高版本
- 不需要单独安装数据库，SQLite 是 Python 标准库自带的

### 步骤

```bash
# 1. 克隆仓库
git clone https://github.com/talent11117/doc-assistant.git
cd doc-assistant

# 2. 建虚拟环境并安装依赖
python -m venv .venv

# Windows:
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# macOS / Linux:
# ./.venv/bin/python -m pip install -r requirements.txt

# 3. 启动服务
# Windows:
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
# macOS / Linux:
# ./.venv/bin/python -m uvicorn app.main:app --reload --port 8000
```

Windows 下也可以直接双击 `run_server.cmd`。

启动后访问 **http://127.0.0.1:8000/docs** 打开交互式接口文档。

> **Windows 用户注意：** 如果你的终端提示「无法将 python 项识别为 cmdlet」，
> 说明 Python 没有加进 PATH。把 `python -m venv .venv` 换成你本机 Python 的完整路径即可，
> 后续命令都用 `.venv\Scripts\python.exe`，不受影响。

## 接口文档

服务启动后访问 **http://127.0.0.1:8000/docs**，可以在网页上直接发请求测试每个接口。

> Swagger UI 的静态资源已下载到 `app/static/`，从本地加载。
> FastAPI 默认从 `cdn.jsdelivr.net` 加载，国内网络经常连不上，表现为 `/docs` 一片空白。
> 排查过程见 `_notes/docs打不开_排查记录.md`。

## 项目结构

```text
doc-assistant/
├── app/
│   ├── main.py              # 入口：创建 app、挂路由、lifespan 里建表
│   ├── database.py          # 全部 SQL 都在这里，换数据库只改这一个文件
│   ├── models.py            # Pydantic 模型：定义请求/响应字段与校验规则
│   ├── routers/
│   │   └── scores.py        # 成绩相关的 5 个路由
│   └── static/              # Swagger UI 静态资源（本地加载，不依赖 CDN）
├── tests/
│   └── test_app.py          # 14 条接口测试
├── learning/                # 学习过程存档（可独立运行，不是项目代码）
├── _notes/                  # 个人笔记（已 gitignore，不进版本库）
├── run_server.cmd           # Windows 一键启动
├── pytest.ini               # pytest 配置：默认只跑 tests/
├── requirements.txt         # 依赖清单
├── .env.example             # 环境变量模板
├── .gitignore
├── LICENSE
└── README.md
```

**分层原则：**

| 文件 | 只放 | 不放 |
|---|---|---|
| `app/main.py` | 创建 `app`、挂路由、生命周期钩子 | 业务逻辑、SQL |
| `app/database.py` | 所有 SQL 与连接管理 | HTTP 相关的东西 |
| `app/models.py` | Pydantic 模型 | 业务逻辑 |
| `app/routers/scores.py` | 路由函数、参数校验、HTTP 状态码 | 手写 SQL |

改数据库实现时只动 `app/database.py`，接口层一行都不用改。

## 测试

```bash
# Windows
.\.venv\Scripts\python.exe -m pytest

# macOS / Linux
./.venv/bin/python -m pytest
```

```text
..............                                    [100%]
14 passed in 0.69s
```

覆盖范围：增删改查、`404`（课程不存在）、`422`（分数越界、课程名为空）、统计接口、空表边界、0 分不等于「没这门课」。

测试用 `monkeypatch` 把数据库连接替换成临时文件，每个测试跑完自动清理，不污染开发数据库。

## 设计要点

### 1. 参数化查询，杜绝 SQL 注入

所有 SQL 都用 `?` 占位符，不拼字符串：

```python
# 正确
conn.execute("SELECT * FROM courses WHERE name = ?", (name,))

# 错误：用户输入 '); DROP TABLE courses; -- 会毁掉整张表
conn.execute(f"SELECT * FROM courses WHERE name = '{name}'")
```

`learning/day10_sqlite.py` 里有这两种写法的对照演示，可以直接跑。

### 2. 路由顺序影响匹配

`/{course}` 是通配路径。如果统计接口写成 `/scores/stats`，它会被 `/{course}` 抢先匹配，
`stats` 就被当成课程名了。所以统计接口必须多一层路径段：`/scores/stats/summary`。

### 3. `APIRouter` 的路径不能写 `"/"`

```python
router = APIRouter(prefix="/scores")

@router.get("")        # 正确 → /scores
@router.get("/")       # 错误 → /scores/（多一个斜杠，跟 /scores 对不上）
```

### 4. 空表统计返回 0 而不是报错

```json
{"count": 0, "average": 0, "best": null}
```

`best` 用 `null` 而不是 `""`，因为「没有最高分课程」和「最高分课程叫空字符串」是两回事。

### 5. 测试替换依赖，而不是改代码

路由函数里统一调用 `db()` 拿连接。测试时用 `monkeypatch` 把 `db` 换成指向临时数据库的版本，
业务代码一行都不用改——这是「依赖注入」的最小可用形态。

## 已知限制

这是一个学习阶段的练习项目，**不是生产级服务**。以下几点是明确没做的：

- **没有用户体系与鉴权**：所有接口匿名可访问，没有 JWT / OAuth。
- **SQLite 单文件**：不支持并发写入，不适合多进程部署。
- **无分页**：`GET /scores` 一次返回全部记录。
- **无日志与监控**：没有结构化日志，没有指标上报。
- **无 CI**：测试需要手动跑，没配 GitHub Actions。
- **无 Docker**：没有容器化，只能在本机跑。

## 开发过程

这个仓库是按 20 周学习计划推进的项目，`learning/` 下每天一个可独立运行的练习文件，
自带自测（不填也能跑，只报 `[未通过]` 不崩溃）。

<details>
<summary>展开查看已完成的学习模块</summary>

| 文件 | 主题 |
|---|---|
| `week01_start_here.py` | 变量、列表、循环、字典、函数、`try/except`、文件读写 |
| `week01_advanced.py` | `sorted(key=)`、字典推导式、`collections.Counter` |
| `practice01.py` | 6 个填空函数 |
| `day03_split_functions.py` | 把挤在一起的逻辑拆成三个函数 |
| `day04_files_json.py` | 文件读写、JSON、`ensure_ascii=False` |
| `day05_class_intro.py` / `day05_classes.py` | 类与对象、`self`、类属性陷阱 |
| `day06_api.py` | HTTP 请求、状态码、`timeout`、`ApiClient` 类 |
| `day07_fastapi.py` | FastAPI 路由、Pydantic 校验、`404` / `422` |
| `mock_api.py` | 本地假服务器（不用 key、不花钱、断网可用） |
| `day10_sqlite.py` | SQLite 建表、增删改查、SQL 注入演示 |
| `day11_sqlite_api.py` | 把 SQLite 接进 FastAPI |
| `day12_parse.py` + `test_day12_parse.py` | pytest 入门：`fixture`、`parametrize` |

详见 [`learning/README.md`](learning/README.md)。

</details>

## 路线图

- [x] **v0.1** 环境搭建、JSON 读写、异常处理
- [x] **v0.2** FastAPI 接口、Pydantic 校验、SQLite 增删改查、14 条测试、包结构重构
- [ ] **v0.3** 带来源引用的 RAG（文档分块、向量检索、回答附引用、拒答机制）
- [ ] **v1.0** 受控工具 Agent（工具白名单、状态机、人工确认、成本记录）

## License

[MIT](LICENSE)
