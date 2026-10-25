# 第 9 天：GitHub · 详细操作手册

> 配套文件：`check_day09.py`
> 日期：2026-10-20 周二
> 目标时长：读 30 分钟 + 动手 80 分钟 + 检查 10 分钟
> 前置：第 8 天全部完成（`check_day08.py` 全绿）

---

## 先纠正我昨天说错的一件事

昨天我在一周计划里写了「**github.com 从你这台机器连不上**」，让你改用 Gitee。

**这个判断是错的。** 今天实测：

```
git ls-remote https://github.com/octocat/Hello-World.git HEAD   → 成功
git clone --depth 1 https://github.com/octocat/Hello-World.git  → 成功，3 秒
```

**GitHub 完全可用。** 之前测出"连不上"有两个原因：

1. 那次是 `ReadTimeout`——**网络波动**，不是墙。GitHub 在国内时快时慢，重试就好
2. 我用 Python `requests` 测的时候报 `SSLError: CERTIFICATE_VERIFY_FAILED`——这是 **Python 的证书链问题**，不是网络问题。Git 用的是它自己带的证书包，不受影响

**结论：用 GitHub，不用 Gitee。** 校招时 GitHub 的认可度明显更高。

> 如果今天推送时真的很卡，再退回 Gitee（命令完全一样，只换网址）。但先试 GitHub。

---

## 第 0 步：想清楚"推上去"意味着什么（5 分钟）

### 昨天 vs 今天

| | 昨天（Git） | 今天（GitHub） |
|---|---|---|
| 仓库在哪 | 你自己的硬盘 | 微软/亚马逊的服务器 |
| 谁能看 | 只有你 | 全世界（Public 仓库） |
| 电脑坏了 | 全没了 | 还在 |
| 面试官能看 | 不能 | 能 |

### 一个必须提前想清楚的问题

推上去之后，**你的代码就是公开的**。包括：

- 你写的 `day03_split_functions.py` 里那些 `pass` 留下的痕迹
- 你第一次写 `load_scores` 时把 `FileNotFoundError` 写成 `FileExistsError`
- 所有中文注释

**这不丢人。** 面试官看 GitHub 不是看"你写得多完美"，是看：

1. 有没有持续提交（证明你真的在学，不是临时抱佛脚）
2. 代码有没有基本结构（文件分得清不清楚）
3. README 写得怎么样（第 14 天会做）

**反而，一个全是 `pass` 但有 20 条提交记录的仓库，比一个完美但没有历史的仓库更有说服力。**

所以：**现在就推，别等"写好了再推"。** 你等不到那天的。

---

## 第 1 步：注册 GitHub（15 分钟）

### 地址

https://github.com/signup

### 用户名怎么起

**这个用户名会出现在你简历上，会出现在你所有提交记录里，改起来很麻烦。**

| 建议 | 例子 | 原因 |
|---|---|---|
| ✅ 真名拼音 | `zhangsan`、`zhang-san` | 面试官一眼对得上简历 |
| ✅ 拼音 + 领域 | `zhangsan-dev`、`zs-ml` | 重名时可用 |
| ❌ 中二昵称 | `darklord666`、`xiaoyao` | 简历上很减分 |
| ❌ 纯数字 | `a1234567` | 看起来像小号 |

### 注册流程

1. 填邮箱（**记住这个邮箱，等下要填进 `.gitconfig`**）
2. 设密码
3. 起用户名
4. 邮箱收验证码，填入
5. 选 Free 计划（够用，不用付费）

### 注册完必须做的一件事

打开 https://github.com/settings/emails

**确认你的邮箱旁边有 `Verified` 标记。** 没有的话点 `Resend verification email`，去邮箱点链接。

> 为什么必须验证：GitHub 只会把**已验证的邮箱**和你的提交关联起来。不验证的话，你推上去的提交显示的是一个灰色默认头像，不算你的贡献。

### 把邮箱填进 `.gitconfig`

用 VS Code 打开 `C:\Users\jack\.gitconfig`，确认 `email` 这一行和 GitHub 上验证的邮箱**一字不差**：

```ini
[user]
	name = Zhang San
	email = zhangsan@example.com
```

改完在新终端验证：

```powershell
git config --global user.email
```

---

## 第 2 步：把 doc-assistant 交给 Git 管（25 分钟）

### 2.1 先做一次安全检查（重要）

在 `doc-assistant` 目录下，先确认 `.env` 不存在或者已经被忽略：

```powershell
cd C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant
Test-Path .env
```

**如果输出 `True`**，说明这里有 `.env` 文件。先打开看一眼里面有没有真实 Key。有的话先确认 `.gitignore` 里有 `.env` 这一行（应该有），再继续。

**如果输出 `False`**，很好，这里没有密钥文件，可以直接继续。

> 你桌面的 `C:\Users\jack\Desktop\learn-fastapi\.env` 里有那个已经泄露的 Key。**那个目录不要推到 GitHub**，等第 14 天单独处理。

### 2.2 初始化

```powershell
git init
git status --short
```

### 2.3 仔细看 `git status --short` 的输出

**真实输出（我在你电脑上跑过）：**

```
?? .env.example
?? .gitignore
?? .vscode/
?? README.md
?? "VS Code 怎么用.md"
?? day03_split_functions.py
?? day04_files_json.py
?? day05_class_intro.py
?? day05_classes.py
?? day06_api.py
?? day06_api_intro.py
?? day07_fastapi.py
?? day10_sqlite.py
?? day11_sqlite_api.py
?? day12_parse.py
?? dev.cmd
?? dev.ps1
?? mock_api.py
?? practice01.py
?? requirements.txt
?? test_day12_parse.py
?? test_week01_advanced.py
?? week01_advanced.py
?? week01_start_here.py
?? 一周任务_2026-10-19至10-25.md
?? 今天的任务_day05.md
?? 今天的任务_day06.md
?? 代码解释_看不懂的地方.md
?? "打开VS Code.cmd"
?? 批改_day04.md
?? 批改_day06_api.md
```

**一共 31 个条目。** 现在验证三件事：

```powershell
# 1. 确认 .venv 不在里面（应该是空的）
git status --short | Select-String "\.venv"

# 2. 确认 .env 不在里面（应该是空的）
git status --short | Select-String "\.env$"

# 3. 确认 .tmp 不在里面（应该是空的）
git status --short | Select-String "\.tmp"
```

**三条命令都应该什么都不输出。**

如果第 1 条有输出，说明 `.gitignore` 里 `.venv/` 那行有问题——`.venv` 有几千个文件，提交上去要等很久，而且仓库会变成 100MB+。

### 2.4 提交

```powershell
git add .
git status --short
```

现在 `??` 应该全变成 `A `（Added，已暂存）。

**再确认一次：**

```powershell
git ls-files | Select-String "\.venv|\.env$|secret|\.key"
```

**必须什么都不输出。** 有输出就停下来，`git reset` 之后修 `.gitignore` 再重来。

```powershell
git commit -m "第一次提交：Python 学习项目，含 8 天练习和 FastAPI 服务"
git log --oneline
```

### 2.5 顺手改掉一个过期配置

打开 `.env.example`，第 9 行写着：

```
LLM_MODEL=deepseek-chat
```

**`deepseek-chat` 这个模型名已经失效了**（你在 `main.py` 里已经改成 `deepseek-flash` 了）。改成：

```
LLM_MODEL=deepseek-flash
```

然后：

```powershell
git add .env.example
git commit -m "修正过期的模型名：deepseek-chat -> deepseek-flash"
```

**这是你的第 2 条提交。** 一条提交只做一件事，这个习惯从今天开始。

---

## 第 3 步：建远程仓库并推上去（30 分钟）

### 3.1 建仓库

打开 https://github.com/new

填这些：

| 字段 | 填什么 | 为什么 |
|---|---|---|
| Repository name | `doc-assistant` | 和本地目录同名，好对应 |
| Description | `Python + FastAPI 学习项目` | 可留空 |
| Public / Private | **选 Public** | 私有仓库别人看不到，对求职没意义 |
| Add a README file | **不勾** | 你本地已经有 README.md，勾了会冲突 |
| Add .gitignore | **不勾** | 你本地已经有 |
| Choose a license | **不勾** | 学习项目不需要 |

点 `Create repository`。

> ⚠️ **三个"不勾"很重要。** 勾了任何一个，远程仓库就会有本地没有的文件，第一次推送会被拒绝，然后你要处理 `git pull --rebase` 的冲突。这是新手最常见的第一个坑。

### 3.2 关联远程

创建后会看到一个页面，顶部有 `Quick setup` 区域，里面有：

```powershell
git remote add origin https://github.com/你的用户名/doc-assistant.git
```

复制这一行，在你本地 `doc-assistant` 目录执行。然后：

```powershell
git branch -M main
git push -u origin main
```

### 3.3 认证：你不需要手动建 PAT

**GitHub 从 2021 年 8 月起不接受账号密码。** 你输密码会得到：

```
remote: Support for password authentication was removed on August 13, 2021.
fatal: Authentication failed for 'https://github.com/...'
```

但**你不用去手动生成 PAT**。你的电脑上装了 **Git Credential Manager（GCM）**，版本 2.9.1，`git push` 时会自动弹浏览器让你登录。

我验证过它工作正常：

```
$ git-credential-manager diagnose
  >>>>  Environment                    [ OK ]
  >>>>  Credential storage             [ OK ]
  >>>>  GitHub API                     [ OK ]
Diagnostic summary: 7 passed, 0 skipped, 0 failed.
```

### 3.4 推送

```powershell
git push -u origin main
```

**会发生什么：**

1. 终端出现 `Logon failed, use ctrl+c to cancel basic credential prompt.`
2. **弹出一个浏览器窗口**（或一个 GCM 登录窗口）
3. 里面显示 `Sign in with your browser`，点它
4. 浏览器跳到 GitHub，显示 **`Confirm access`** 页面（就是你截图那个）
5. 点 `Use your password` 或 `Use GitHub Mobile`，完成验证
6. 回到终端，推送自动继续

### 关于那个 `Confirm access` 页面

这是 GitHub 的 **sudo mode（提权模式）**。官方文档说明：

> 为了在敏感操作前确认身份，GitHub 要求你重新认证。这些操作包括：**创建 Personal Access Token**、添加 SSH Key、删除账号、授权第三方应用等。
> 认证后进入 sudo mode，有效期 **2 小时**，期间再做敏感操作不用重复认证。

**你看到它，说明你正在做的事被 GitHub 判定为"敏感操作"**——你当时很可能在生成 PAT，或者 GCM 的 OAuth 授权被视为敏感操作。

三个选项怎么选：

| 选项 | 什么时候用 |
|---|---|
| **`Use your password`** | 最直接。点它，输你的 GitHub 登录密码，点 `Confirm` |
| `Use GitHub Mobile` | 装了 GitHub 手机 App 才能用。打开 App 会显示数字，输进去 |
| 2FA code | 如果你开了两步验证，用验证器 App 的 6 位数字 |

**推荐点 `Use your password`。** 输一次密码就行，2 小时内不用再输。

> ⚠️ 注意：这里要的是 **GitHub 登录密码**，不是 PAT，也不是 token。输对了就能过。

### 如果你还是想手动建 PAT（备选方案）

GCM 弹窗失败、或者你不想用浏览器认证时，可以走这条路：

1. 打开 https://github.com/settings/tokens
2. 点 `Generate new token` → 选 `Generate new token (classic)`
3. 填：
   - **Note**：`doc-assistant 本地推送`
   - **Expiration**：`90 days`
   - **Select scopes**：只勾 **`repo`** 这一整个大项
4. 拉到最下面点 `Generate token`
5. **页面会显示一串 `ghp_` 开头的字符。立刻复制，关掉页面就再也看不到了。**
6. 回到终端推送，`Username` 填你的 GitHub 用户名，`Password` 粘贴那串 token

> 🔒 **Token 和密码同级。** 不要贴进任何聊天、不要写进代码、不要提交到仓库。
> 好消息：`credential.helper` 已配好，Windows 会把它存进凭据管理器，**只需要输一次**。以后 push 不用再输。

### 3.5 推送成功的输出

```
Enumerating objects: 45, done.
Counting objects: 100% (45/45), done.
Delta compression using up to 12 threads
Compressing objects: 100% (38/38), done.
Writing objects: 100% (45/45), 32.14 KiB | 3.21 MiB/s, done.
Total 45 (delta 3), reused 0 (delta 0), pack-reused 0
To https://github.com/你的用户名/doc-assistant.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

**注意 `32.14 KiB`。** 如果是几十 MB，说明 `.venv` 被提交了，赶紧停下来处理。

**最后一行的 `branch 'main' set up to track 'origin/main'.` 是关键。** 有这一行，说明 `-u` 生效了，以后直接 `git push` 就行，不用再写 `origin main`。

---

## 第 4 步：验证 + 安全检查（10 分钟）

### 4.1 网页上验证

打开 `https://github.com/你的用户名/doc-assistant`，应该能看到你的文件列表。

**点开一个 `.py` 文件**，确认能看到代码（说明推送完整）。

### 4.2 本地验证

```powershell
git remote -v
git log --oneline
git status
```

- `git remote -v` 应该显示两行（fetch 和 push），都是你的仓库地址
- `git log --oneline` 应该有 2 条以上
- `git status` 应该显示 `Your branch is up to date with 'origin/main'.` 和 `nothing to commit, working tree clean`

### 4.3 安全检查（最重要的一步）

```powershell
git ls-files | Select-String "\.env$|\.venv|secret|\.key|sk-"
```

**必须什么都不输出。**

如果有输出，立刻做：

```powershell
# 从 Git 里移除（不删本地文件）
git rm --cached 那个文件

# 提交这次移除
git commit -m "移除误提交的敏感文件"

# 推上去
git push
```

> ⚠️ **但注意：`git rm --cached` 只是让 Git 以后不管它，历史记录里还有。**
> 如果那是真的 API Key，**立刻去平台撤销重建**，因为历史记录任何人都能翻。
> 这就是为什么 `.gitignore` 要在第一次提交**之前**就写好。

### 4.4 看提交记录长什么样

打开 `https://github.com/你的用户名/doc-assistant/commits/main`

你应该看到 2 条记录，每条旁边是你的头像（如果邮箱验证过）和提交信息。

**这就是面试官会看的东西。** 一条好的提交信息长这样：

```
修正过期的模型名：deepseek-chat -> deepseek-flash
```

一条坏的：

```
update
```

**从今天开始，每条提交信息都写"做了什么"，不写"改了改"。**

---

## 做完自查

```powershell
cd C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant
.\.venv\Scripts\python.exe check_day09.py
```

检查项：
- 本地是不是 git 仓库
- 有没有配远程
- **远程名字是不是 `origin`**（不是 `orgin`）
- 远程地址是不是 GitHub
- 提交数 ≥ 2
- `git ls-files` 里没有 `.env` / `.venv` / `sk-`
- 本地和远程是否同步

---

## 卡住了对照表

| 你看到的 | 原因 | 怎么办 |
|---|---|---|
| **`Confirm access` 页面（要求重新验证）** | GitHub 的 sudo mode，敏感操作前要求重新认证 | 点 `Use your password`，输 GitHub 登录密码。2 小时内不用再输 |
| `Logon failed, use ctrl+c to cancel basic credential prompt` | GCM 在启动浏览器认证 | 等浏览器弹出，在里面完成登录 |
| `Support for password authentication was removed` | 用了账号密码 | 用 GCM 浏览器认证，或手动建 PAT，见 3.3 |
| **`'origin' does not appear to be a git repository`** | **远程名字拼错了**（比如写成 `orgin`） | `git remote rename orgin origin`，然后用 `git remote -v` 确认 |
| `remote origin already exists` | 之前加过 | `git remote remove origin` 再加 |
| `failed to push some refs` | 远程有本地没有的提交 | `git pull --rebase origin main` 再推 |
| `src refspec main does not match any` | 还没 commit | 先 `git commit` |
| `error: src refspec main does not match any` 但明明提交了 | 分支名是 `master` 不是 `main` | `git branch -M main` |
| `fatal: no upstream configured for branch 'main'` | 推送时漏了 `-u` | `git push -u origin main` 补一次 |
| 推送卡住不动超过 2 分钟 | 网络问题 | Ctrl+C 中断，重试；连续 3 次失败改用 Gitee |
| `Permission denied (publickey)` | 用了 SSH 地址但没配 SSH Key | 改用 HTTPS 地址 |
| 网页上看不到最新提交 | 浏览器缓存 | Ctrl+F5 强制刷新 |
| 网页显示空仓库 / `Git Repository is empty` | 推送还没成功 | 看终端有没有 `* [new branch] main -> main` |

---

## 今天不学的东西

| 东西 | 为什么 |
|---|---|
| SSH Key 配置 | HTTPS + GCM 已经够用，SSH 是优化项 |
| GitHub Actions（CI） | 第 14 天之后再说，现在没东西可自动化 |
| Pull Request 流程 | 一个人写项目用不上，等团队协作再学 |
| `.gitattributes` | 换行符高级配置，暂时用默认 |
| 私有仓库 + 协作者 | 不需要 |

---

## 一句话总结

> **今天之后，你的代码有了一个别人能打开的地址。**
> 这个地址会写进你的简历。它不需要完美，但它需要**存在**，而且需要**看起来像一直在写**。
> 所以：从今天起，每天学完就 `git add . && git commit -m "第 N 天：..."`，一周推一次。
