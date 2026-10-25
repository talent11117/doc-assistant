# learning/ —— 学习过程存档

这里是按 20 周学习计划推进时，每天写的练习文件。**不是项目代码**，保留是为了留痕：能看出从「变量和循环」到「FastAPI + SQLite + pytest」的完整路径。

## 特点

每个文件都能**独立运行**，自带自测。即使题目没做完，也能跑起来、只报 `[未通过]` 而不崩溃——这样练习时可以一条一条改。

## 文件清单

### 第一阶段：Python 基础

| 文件 | 主题 |
|---|---|
| `week01_start_here.py` | 变量、列表、循环、字典、函数、`try/except`、文件读写 |
| `week01_advanced.py` | 进阶：`sorted(key=)`、字典推导式、`collections.Counter` |
| `practice01.py` | 6 个填空函数：`add` / `count_items` / `find_max` / `count_above` / `make_dict` / `safe_divide` |
| `day03_split_functions.py` | 把挤在一起的逻辑拆成三个职责单一的函数 |
| `day04_files_json.py` | 文件读写、JSON、`ensure_ascii=False`、`FileNotFoundError` |

### 第二阶段：面向对象与网络

| 文件 | 主题 |
|---|---|
| `day05_class_intro.py` | 类与对象入门：`self`、`__init__` |
| `day05_classes.py` | 类属性 vs 实例属性的经典陷阱 |
| `day06_api_intro.py` | HTTP 请求入门 |
| `day06_api.py` | 状态码、`timeout`、用类封装 `ApiClient` |
| `mock_api.py` | 本地假服务器：不用 API key、不花钱、断网也能跑 |

### 第三阶段：Web 服务与数据库

| 文件 | 主题 |
|---|---|
| `day07_fastapi.py` | FastAPI 路由、Pydantic 校验、`404` / `422` |
| `day10_sqlite.py` | SQLite 建表、增删改查、**SQL 注入对照演示** |
| `day11_sqlite_api.py` | 把 SQLite 接进 FastAPI |

### 第四阶段：测试

| 文件 | 主题 |
|---|---|
| `day12_parse.py` | 被测试的函数本体 |
| `test_day12_parse.py` | pytest 入门：`fixture`、`parametrize` |

### 操作手册

| 文件 | 主题 |
|---|---|
| `day08_git_详细步骤.md` | Git 基础：`init` / `add` / `commit` / `diff` / `restore` / `.gitignore` |
| `day09_github_详细步骤.md` | GitHub：建远程仓库、`remote add`、`push -u` |

## 怎么跑

```bash
# 单个练习（在项目根目录执行）
.\.venv\Scripts\python.exe learning\day10_sqlite.py

# learning/ 下的测试需要显式指定路径
.\.venv\Scripts\python.exe -m pytest learning\test_day12_parse.py -q
```

> 默认的 `pytest` 只跑 `tests/test_app.py`（项目接口测试）。
> `learning/` 里的测试是练习用的，需要显式指定。
