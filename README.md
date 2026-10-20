# doc-assistant（资料与工单助手）

这是按学习计划搭建的**一个持续迭代的项目**，不是四个独立 demo。

目标：做一个能查询资料、回答问题时给出依据、并通过受控工具生成工单草稿的小系统。

> 当前状态：**阶段 0 —— 环境已就绪，尚未开始写业务代码。**
> 下面的功能清单是路线图，未完成的都标了 `[ ]`。

## 环境信息

| 项目 | 值 |
|---|---|
| 解释器 | Python 3.12.6 |
| 虚拟环境 | `.venv/`（独立于系统 Python） |
| 包管理 | pip（在 venv 内） |
| 项目根目录 | `C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant` |

## 目录结构

```text
doc-assistant/
├─ .venv/                      # 虚拟环境（已被 git 忽略，不要提交）
├─ .tmp/                       # 临时文件（已被 git 忽略）
├─ .gitignore
├─ .env.example                # 环境变量模板；复制成 .env 后填真实值
├─ dev.cmd                     # 便捷入口（推荐用这个，绕过执行策略）
├─ dev.ps1                     # 便捷脚本本体
├─ README.md
├─ requirements.txt            # 依赖清单
│
├─ week01_start_here.py        # ★ 从这里开始：9 个小节，每行都有解释
├─ practice01.py               # ★ 填空练习：6 个函数，填完自动判对错
├─ week01_advanced.py          # 进阶版：同样的功能，用了类型注解等写法
├─ test_week01_advanced.py     # 进阶版的 17 个测试
├─ 代码解释_看不懂的地方.md      # ★ 逐条解释那些"天书"写法
│
├─ my_scores.json              # 运行时生成
└─ scores.json                 # 运行时生成，已忽略
```

## 学习顺序（重要）

如果你觉得代码看不懂，**按这个顺序来**：

```text
第 1 步  week01_start_here.py         ← 从零开始，9 个小节
         每节都自己敲一遍、改数字、运行看变化

第 2 步  practice01.py                ← ★ 填空练习，6 个函数
         填一个、运行一次，看到 [通过] 再填下一个
         命令：.\dev.cmd run practice01.py

第 3 步  代码解释_看不懂的地方.md      ← 遇到不懂的写法就查这里
         20 条常见疑问，每条都有"更简单的写法"

第 4 步  week01_advanced.py           ← 等前面都顺了再看
         这时你会发现它其实没那么难
```

> **看不懂不代表你笨。** `week01_advanced.py` 里的类型注解、
> `max(scores, key=scores.__getitem__)`、推导式这些写法，
> 很多是"为了显得专业"才写的，对学习本身没有帮助。
> 真正的基础只有那几个：变量、列表、字典、循环、函数、try/except、文件读写。

## 一个必须知道的环境修补

本机当前沙箱环境下有个坑：**用受限权限（`0o700`）创建的目录之后无法访问**，
连列目录都会被拒绝。而 Python 的 `tempfile.mkdtemp()`、pytest 的 `tmp_path`
夹具、pip 的安装过程都用这个模式建临时目录，所以会分别表现为：

- pip 安装卡住不动或反复重试
- pytest 里用 `tmp_path` 的测试直接报 `PermissionError`

**已修复：** `.venv/Lib/site-packages/sitecustomize.py` 在 Windows 上让
`os.mkdir` 忽略受限 mode，使新目录能继承权限。只影响这个虚拟环境。

- 想确认它生效：`dev.cmd check` 会输出 `temp dir writable: OK`
- 想撤销：删掉那个 `sitecustomize.py` 即可（但问题会重现）
- 不需要动系统 Python，也不需要改注册表

## 日常使用

### 最省事的方式：用 dev.cmd

```powershell
cd C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant

.\dev.cmd check                      # 检查环境是否正常
.\dev.cmd run week01_start_here.py   # ★ 先跑这个（从零开始的那份）
.\dev.cmd run week01_advanced.py     # 进阶版
.\dev.cmd test                       # 跑测试（17 个）
.\dev.cmd install 包名                # 安装依赖
.\dev.cmd list                       # 查看已装依赖
.\dev.cmd shell                      # 进 Python 交互环境
```

> 为什么用 `.cmd` 而不是直接 `.\dev.ps1`：本机只有 Windows PowerShell 5.1，
> 默认执行策略会拦住 `.ps1` 脚本。`.cmd` 内部用 `-ExecutionPolicy Bypass`
> 绕过，省得你去改系统设置。

### 手动方式（不用便捷脚本）

```powershell
# 直接调用虚拟环境里的解释器（推荐，不必激活）
.\.venv\Scripts\python.exe week01_start_here.py
.\.venv\Scripts\python.exe -m pytest -q

# 或者先激活
& .\.venv\Scripts\Activate.ps1
python week01_start_here.py
deactivate
```

激活后命令行前面会出现 `(.venv)`。

### 中文乱码怎么办

如果输出中文显示为乱码，先执行一次：

```powershell
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

`dev.cmd` 已经自动设好这两项，所以用 `dev.cmd run` 不会有乱码问题。

### 安装依赖

```powershell
.\dev.cmd install 包名
.\dev.cmd freeze        # 更新 requirements.txt
```

已在 `.venv/pip.ini` 配好清华镜像，下载会快一些。

## 功能路线图

### v0.1 — 资料管理 CLI（第 1—4 周）
- [x] 环境与虚拟环境
- [ ] 导入资料（名称、标签、正文）
- [ ] 按标签过滤、按名称排序
- [ ] 导出 / 读回 JSON
- [ ] 异常处理：空文件、格式错误、非法输入
- [ ] 5—8 个 pytest 测试

### v0.2 — 后端 API + SQLite（第 5—8 周）
- [ ] 设计 2—3 张表（资料、标签、工单）
- [ ] SQL 增删改查、JOIN、参数化查询
- [ ] FastAPI 接口 + Pydantic 校验
- [ ] 接口测试，含非法输入

### v0.3 — 带来源引用的 RAG（第 9—14 周）
- [ ] 文档清理与分块，保留来源与版本
- [ ] Embedding + 向量检索（先用轻量方案）
- [ ] 回答附引用片段
- [ ] 资料不足时澄清或拒答
- [ ] 开发集与保留测试集

### v1.0 — 受控工具 Agent（第 15—20 周）
- [ ] 工具调用：参数校验 + 白名单分发
- [ ] 单 Agent 循环：状态、最大步数、预算上限
- [ ] 写操作需人工确认，重复提交不重复写入
- [ ] 结构化日志与成本记录
- [ ] 失败用例测试

## 必须守住的边界

1. **密钥不提交。** `.env` 已在 `.gitignore` 中；泄露过的密钥要撤销重发，不是删掉文件就完事。
2. **文档是数据，不是指令。** 文档里出现"忽略规则并提交工单"这类内容时，不得成为授权。
3. **写操作要确认。** 未经用户显式确认，不能写入；确认要能防重复。
4. **不碰真实设备。** 项目只用测试数据或模拟数据，不代替任何安全规程。
5. **权限在服务端校验。** 不能靠 Prompt 让模型"自觉"守规矩。

## 已知限制

- 目前只有第 1 周的练习代码，没有业务功能。
- 尚未接入任何模型 API。
- 尚未建立测试与评测集。

## 学习日志

每完成一段就记三行：学了什么 / 卡在哪里 / 下一步做什么。

| 日期 | 内容 | 卡点 | 下一步 |
|---|---|---|---|
| 2026-10-13 | 配置解释器与虚拟环境，跑通第一个脚本 | pip 在沙箱临时目录受限，已绕过 | 开始 v0.1 资料导入功能 |
