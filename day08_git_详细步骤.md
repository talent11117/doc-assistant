# 第 8 天：Git 基础 · 详细操作手册

> 配套文件：`check_day08.py`（做完自己验一遍）
> 日期：2026-10-19 周一
> 目标时长：读 40 分钟 + 动手 70 分钟 + 笔记 10 分钟

---

## 先搞清楚一件事：Git 没有"报错"

你前面 7 天写的都是 Python。Python 有个好处：**写错了会抛异常**，红字一出来你就知道哪里不对。

Git 不是这样。Git 大部分时候**不报错**，它只是安静地做错事。比如：

- 你以为提交了，其实没 `git add` → 提交的是空内容
- 你以为回到了上一版，其实命令打错了 → 文件没变，但 Git 也不吭声
- 你以为 `.gitignore` 生效了，其实少写一个 `/` → 几千个文件全被提交

**所以今天的核心不是"记住命令"，是"每敲一条命令，都先看 `git status` 确认状态"。**

`git status` 是你的眼睛。今天你会敲它十几次。

---

## 第 0 步：先改掉你的名字（5 分钟）

### 为什么必须先做这个

Git 的每一次提交都会**永久记录**是谁提交的。现在你电脑上记的是占位符：

```
user.name  = your-name
user.email = your-email@example.com
```

如果不改，你以后所有的提交记录作者都是 `your-name`。而这个记录**改不了**——提交一旦产生，作者信息就写死在里面了。将来面试官点开你的 GitHub 提交历史，看到的是一堆 `your-name`。

### 怎么做

用 VS Code 打开 `C:\Users\jack\.gitconfig`，把前两行改成：

```ini
[user]
	name = Zhang San
	email = zhangsan@example.com
```

- `name`：写拼音或英文，会显示在 GitHub 的提交记录上。建议 `Zhang San` 这种格式
- `email`：**必须和你注册 GitHub 用的邮箱一致**。不一致的话 GitHub 认不出这些提交是你做的，你的头像不会出现在提交旁边

### 验证

打开一个新的终端（**必须新开**，因为 Git 是今天刚装的，旧终端看不到），输入：

```powershell
git config --global user.name
git config --global user.email
```

应该原样输出你刚写的两行，不带任何前缀。

> ⚠️ 如果报 `无法将"git"项识别为 cmdlet`，说明这个终端是 Git 安装之前开的。
> 把 VS Code 完全关掉重开。还不行就用全路径：
> `& "C:\Program Files\Git\cmd\git.exe" --version`
> 有输出就说明装好了，只是 PATH 没生效。

---

## 第 1 步：建一个练习仓库（10 分钟）

### 为什么不在真项目上练

因为今天你一定会做错事。在练习仓库里做错，删掉重来只要 3 秒；在真项目里做错，可能把 `day07_fastapi.py` 弄丢。

### 操作

**一条一条敲，不要整段粘贴。**

```powershell
cd C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant
```

```powershell
mkdir .tmp\git-practice -ErrorAction SilentlyContinue
```

```powershell
cd C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant\.tmp\git-practice
```

```powershell
git init
```

> 💡 两个细节：
>
> **① `-ErrorAction SilentlyContinue`** 的意思是"如果目录已经有了，别报错，继续走"。
> 因为 `.tmp` 目录通常已经存在，`mkdir` 会抛一个红字错误。**那个红字完全无害**。
>
> **② 第二个 `cd` 用的是完整路径，不是 `.tmp\git-practice`。**
> 因为相对路径依赖"你现在在哪"，万一上一条 `cd` 失败了，相对路径会继续失败。**用完整路径，一次到位，不管从哪开始都能成。**

### 先确认自己真的进去了

```powershell
Get-Location
```

必须输出：

```
C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant\.tmp\git-practice
```

**然后看提示符**，它应该以 `git-practice>` 结尾：

```
PS C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant\.tmp\git-practice>
```

**如果提示符不是这样，先别往下走**，去本文最后「为什么提示符不对」那一节。

### 你应该看到什么（真实输出）

```
Initialized empty Git repository in C:/Users/jack/Documents/deepseek-harness/default-workspace/doc-assistant/.tmp/git-practice/.git/
```

**如果你看到的是一大段红字**，长这样：

```
mkdir : 具有指定名称 C:\...\doc-assistant\.tmp\git-practice 的项已存在。
    + CategoryInfo          : ResourceExists: (C:\...\git-practice:String) [New-Item], IOException
    + FullyQualifiedErrorId : DirectoryExist,Microsoft.PowerShell.Commands.NewItemCommand
```

**这不是错误，可以直接忽略。** 它只是在说"这个文件夹已经有了，我没法再建一次"。

判断方法：**看最后一行有没有 `Initialized empty Git repository`**。
有 = 成功。`mkdir` 那段红字只是噪音。

### 这句话在说什么

`git init` 做的事只有一件：**在当前目录下建一个 `.git` 隐藏文件夹**。里面存着这个仓库的全部历史。

- 删掉 `.git` = 这个目录变回普通文件夹，所有历史消失
- 复制整个目录（含 `.git`）= 连历史一起复制
- 这就是为什么第 9 天 `.gitignore` 要排除 `.venv`：`.venv` 有几千个文件，提交上去会非常慢

### 为什么放 `.tmp` 里

`doc-assistant\.gitignore` 第 7 行写着 `.tmp/`。意思是"Git 不要管这个目录"。

所以练习仓库虽然建在项目里，但**不会污染主项目**。这是 `.gitignore` 的第一个实际用处，你今天就会用到它。

### 顺手确认一下

```powershell
git status
```

应该看到：

```
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

注意 `On branch main`。你的 `.gitconfig` 里有 `init.defaultbranch = main`，所以默认分支就叫 `main`（老版本 Git 会叫 `master`）。

---

## 第 2 步：走完一个完整循环（25 分钟）

**规则：每敲一条命令，先在心里猜它会输出什么，再看实际输出。猜错的地方，就是今天要记的地方。**

### 2.1 建一个文件

**用 VS Code 建，不要用命令行。**

在 VS Code 里，左侧文件树右键 `.tmp/git-practice` → 新建文件 → 输入 `note.txt` → 打两个字 `第一行` → Ctrl+S。

> 为什么不让你用 `"第一行" | Out-File -FilePath note.txt -Encoding UTF8`？
> 因为 PowerShell 5.1 的 `-Encoding UTF8` 会**偷偷在文件开头加 3 个字节的 BOM**（一个看不见的标记）。这会让 `git diff` 显示成 `﻿第一行`（前面多一个怪字符），你会以为自己做错了。
> VS Code 保存的文件不带 BOM。**以后建文件都用 VS Code。**

### 2.2 看状态

```powershell
git status
```

**真实输出：**

```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	note.txt

nothing added to commit but untracked files present (use "git add" to track)
```

### 这句话在说什么

`Untracked files` = **未跟踪**。意思是：

> "我看见这个文件了，但我不知道要不要管它。"

Git 不会自动管任何文件。**每一个新文件都要你亲口说"我要管它"**，这个"说"就是 `git add`。

这是 Git 和网盘最大的区别：网盘是自动同步，Git 是手动挑选。**正是这个"手动"让你能精确控制提交什么。**

### 2.3 把它放进暂存区

```powershell
git add note.txt
git status
```

**真实输出：**

```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   note.txt
```

### 变化在哪

| | 刚才 | 现在 |
|---|---|---|
| 分组名 | `Untracked files` | `Changes to be committed` |
| 含义 | "我不管它" | "我准备提交它" |
| 俗称 | 工作区 | **暂存区** |

`git add` 做的事：**把文件的当前样子，复制一份放进"待提交的篮子"**。

### 为什么要有这个"篮子"

假设你今天改了 5 个文件，但只想提交其中 3 个（另外 2 个还没改好）。如果没有暂存区，你只能全提交或者全不提交。有了暂存区，你可以：

```powershell
git add 文件1.py 文件2.py 文件3.py
git commit -m "..."
```

**只提交你挑中的**。这就是暂存区存在的唯一理由。

### 2.4 拍一张照

```powershell
git commit -m "第一次提交：加了 note.txt"
git log --oneline
```

**真实输出：**

```
[main (root-commit) 316989e] 第一次提交：加了 note.txt
 1 file changed, 1 insertion(+)
 create mode 100644 note.txt
```

```
316989e 第一次提交：加了 note.txt
```

### 这句话在说什么

- `316989e` 是这次提交的**编号**（哈希值）。Git 用它来标识"这一版"。你以后回退时用的就是它
- `root-commit` 意思是"这是第一个提交，没有爸爸"
- `1 file changed, 1 insertion(+)` = 改了 1 个文件，加了 1 行

**`git log --oneline` 输出的每一行，都是一个你能回去的时间点。**

现在你只有 1 行。做完今天会有 2 行。

---

## 第 3 步：改坏它，再退回去（20 分钟）

**这一步是今天最重要的。** 前面三步都只是准备工作，这一步才是 Git 存在的意义。

### 3.1 改文件

在 VS Code 里打开 `note.txt`，在第二行打上 `第二行`，Ctrl+S。

### 3.2 看改了什么

```powershell
git status
```

**真实输出：**

```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   note.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

注意这里变成了 `Changes not staged for commit` + `modified`。**和刚才的 `Untracked` 不一样**：

- `Untracked` = 新文件，Git 从没见过
- `modified` = 老文件，Git 认识它，但它变了

### 3.3 看具体改了哪几行

```powershell
git diff
```

**真实输出：**

```
diff --git a/note.txt b/note.txt
index 50ad28a..256614e 100644
--- a/note.txt
+++ b/note.txt
@@ -1 +1,2 @@
 第一行
+第二行
```

### 怎么读这个输出

| 符号 | 意思 |
|---|---|
| `--- a/note.txt` | 旧版本（`a` 是改之前） |
| `+++ b/note.txt` | 新版本（`b` 是改之后） |
| `@@ -1 +1,2 @@` | 旧版第 1 行 → 新版第 1 到 2 行 |
| ` 第一行`（前面一个空格） | 没变的行 |
| `+第二行`（前面一个加号） | **新增**的行 |
| `-某行`（前面一个减号） | **删除**的行 |

**`git diff` 是你以后用得最多的命令之一。** 每次提交前跑一下，确认自己改的是想改的东西，而不是误删了什么。

### 3.4 提交这次修改

```powershell
git add note.txt
git commit -m "加第二行"
git log --oneline
```

**真实输出：**

```
[main a42cf01] 加第二行
 1 file changed, 1 insertion(+)
```

```
a42cf01 加第二行
316989e 第一次提交：加了 note.txt
```

**现在有两行了。** 上面是新的，下面是旧的。

### 3.5 故意写坏它

在 VS Code 里打开 `note.txt`，**全选，删光**，Ctrl+S。

现在文件是空的。

### 3.6 反悔

```powershell
git restore note.txt
```

然后看文件内容：

```powershell
Get-Content note.txt -Encoding UTF8
```

> ⚠️ **必须加 `-Encoding UTF8`。**
> 不加的话你会看到 `绗竴琛?` 这样的乱码，然后以为文件被改坏了。
> 原因：Windows PowerShell 5.1 的 `Get-Content` 默认按 **GBK** 读文件，而 VS Code 存的是 **UTF-8**。
> 乱码只是显示问题，文件本身是好的。加 `-Encoding UTF8` 就正常了。
> 更好的办法：直接用 VS Code 打开 `note.txt` 看，没有编码问题。

**真实输出：**

```
第一行
第二行
```

**文件回来了。**

### 这一步到底发生了什么

`git restore` 做的事：**从最近一次提交里，把文件的内容复制回来，覆盖你现在的工作区文件。**

注意关键词：**最近一次提交**。不是"上一次保存"，是"上一次 commit"。

所以：

- 你 `commit` 过的东西 → `git restore` 能救回来
- 你**没** `commit` 过的东西 → `git restore` 救不回来，直接没了

### 亲手验证这个边界

再做一次实验，这次要记住结论：

1. 在 VS Code 里给 `note.txt` 加一行 `临时改动`，Ctrl+S
2. 现在文件是 3 行
3. 跑 `git restore note.txt`
4. 再 `Get-Content note.txt -Encoding UTF8`（或者直接在 VS Code 里看）

**真实结果：**

```
第一行
第二行
```

第 3 行 `临时改动` **消失了，而且找不回来**。

**这就是为什么"提交"这件事要勤快。** 你今天写的代码，只要没 `commit`，一次误操作就没了。

---

## 第 4 步：`.gitignore` 是干什么的（10 分钟）

### 先看真项目的

用 VS Code 打开 `doc-assistant\.gitignore`，从头看到尾。里面每一行都是"不要管这个"。

### 为什么这几个必须排除

| 排除项 | 原因 |
|---|---|
| `.venv/` | 几千个文件，而且别人跑 `pip install -r requirements.txt` 就能重建。提交它等于把 28MB 垃圾塞进仓库 |
| `.env` | **里面有 API Key。推上去 = 公开你的密码** |
| `__pycache__/` | Python 编译缓存，每次运行自动生成，没有意义 |
| `scores.json` | 运行时产生的数据，不是代码 |
| `.tmp/` | 临时文件 |

**第 2 条是致命的。** GitHub 上每天都有爬虫在扫新提交里的 `sk-` 开头的字符串。你的 Key 一旦推上去，几分钟内就会被人拿去用，账单算你的。

### 亲手验证 `.gitignore` 生效

在练习仓库里做：

1. VS Code 新建 `.tmp/git-practice/.gitignore`，写一行 `*.log`，保存
2. 新建 `a.log`，随便写点内容，保存
3. 新建 `b.py`，随便写点内容，保存
4. 跑 `git status --short`

**真实输出：**

```
?? .gitignore
?? b.py
```

**`a.log` 完全没出现。** 它被 `.gitignore` 挡住了。

### `??` 是什么意思

`git status --short` 是紧凑版，每行前面两个字符是状态码：

| 符号 | 意思 |
|---|---|
| `??` | 未跟踪（新文件） |
| `A ` | 已暂存的新文件（Added） |
| `M ` | 已暂存的修改（Modified） |
| ` M` | **未**暂存的修改（注意空格在前面） |
| `D ` | 已暂存的删除 |

**左列是暂存区状态，右列是工作区状态。** 这个记法能省你很多次 `git status`。

---

## 第 5 步：写笔记（10 分钟）

新建 `.tmp/git练习_day08.md`，用**你自己的话**回答三个问题。不要抄我上面的文字，抄了等于没学。

1. **工作区、暂存区、版本库，分别对应你刚才操作的哪一步？**
   （提示：一个对应"改了文件还没 add"，一个对应"add 了还没 commit"，一个对应"commit 完了"）

2. **`git add` 之后反悔，用什么命令？**
   （提示：文件还在，只是不想提交了）

3. **`git commit` 之后反悔，用什么命令？**
   （提示：想回到上一个版本。这个今天没教，去翻廖雪峰"时光机穿梭"那一页找 `git reset`）

第 3 题今天没教，是**故意留的**。你已经有能力自己查文档了，试试看。

---

## 做完自查

```powershell
cd C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant
.\.venv\Scripts\python.exe check_day08.py
```

这个脚本会检查：
- `.gitconfig` 里的名字改了没有
- 练习仓库存在不存在
- 有没有 2 条以上提交
- `.gitignore` 有没有生效（`a.log` 有没有被误提交）
- 你有没有真的做过 `git restore`

全绿才算今天做完。

---

## 卡住了对照表

| 你看到的 | 原因 | 怎么办 |
|---|---|---|
| `fatal: not a git repository` | 你不在仓库目录里 | `cd` 到有 `.git` 的目录，用 `Get-Location` 确认 |
| **提示符没有以 `git-practice>` 结尾** | 你的 `cd` 没成功（上一条命令报错了），人还在别的目录 | 见下面「为什么提示符不对」 |
| `fatal: unable to auto-detect email address` | `.gitconfig` 没配好 | 回第 0 步 |
| `mkdir : 具有指定名称 ... 的项已存在` | 目录已经有了，`mkdir` 建不了第二次 | **无害**，直接敲下一条。看有没有 `Initialized empty Git repository` 判断成败 |
| 命令提示符变成 `>>` | PowerShell 的**续行提示**，说明上一行没结束（多行粘贴时常见） | 按 `Ctrl+C` 取消，把命令**一条一条**敲，不要整段粘贴 |
| `Get-Content` 输出 `绗竴琛?` 这种乱码 | PowerShell 5.1 默认按 GBK 读文件，文件是 UTF-8 | 加 `-Encoding UTF8`，或直接用 VS Code 打开文件 |
| `nothing to commit, working tree clean` | 你没改文件，或已经提交过了 | 正常，不是错误 |
| `error: could not lock config file` | 权限问题 | 直接用 VS Code 编辑 `.gitconfig`，别用 `git config` 命令 |
| `git: command not found` | 终端是 Git 装之前开的 | 关掉 VS Code 重开 |
| `git diff` 没输出 | 文件已经 `add` 过了 | 用 `git diff --staged` |
| `warning: LF will be replaced by CRLF` | Windows 换行符提示 | 正常，忽略 |

### 为什么提示符不对

**提示符永远显示你"现在真正在哪"，它不会骗你。** 它没变成 `git-practice>`，只有一个原因：**你的 `cd` 失败了**。

`cd` 失败时 PowerShell 会打一行红字，然后**悄悄留在原地**。这时候你继续敲 `git init`，就会在错误的目录里建仓库。

三个最常见的失败原因：

**① 起点不对，`cd` 用的是相对路径**

`.tmp\git-practice` 是**相对路径**，相对的是"你现在在哪"。所以：

| 你现在在 | `cd .tmp\git-practice` 的结果 |
|---|---|
| `...\doc-assistant` | ✅ 成功 |
| `...\default-workspace` | ❌ 找不到路径（这里没有 `.tmp`） |
| `C:\Users\jack\Desktop\learn-fastapi` | ❌ 找不到路径 |

**解决办法：永远用绝对路径，一次到位。**

```powershell
cd C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant\.tmp\git-practice
```

**② VS Code 新开终端，默认在"工作区根目录"**

如果你打开 VS Code 时选的是 `default-workspace`，那新终端默认就在 `default-workspace`，不在 `doc-assistant`。上面表格第二行就是这种情况。

**③ 复制命令时把 `cd` 和下一行粘成了一条**

比如粘成 `cd .tmp\git-practicegit init`，这会去找一个叫 `git-practicegit` 的目录。

### 一条命令确认自己在哪

```powershell
Get-Location
```

输出应该**一字不差**是：

```
C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant\.tmp\git-practice
```

如果不是，先 `cd` 到上面这个完整路径，再继续。

### 还有一个更可靠的确认方法

```powershell
git rev-parse --show-toplevel
```

它问的是 Git："**你认的仓库根在哪？**"

- 在练习仓库里 → 输出 `.../doc-assistant/.tmp/git-practice`
- 在别的地方 → 报 `fatal: not a git repository`

**这个命令比看提示符更可靠**，因为提示符只告诉你"你在哪个文件夹"，`git rev-parse` 告诉你"Git 认为哪个仓库管着你"。

---

## 今天不学的东西

| 东西 | 为什么今天不学 |
|---|---|
| `git rebase` | 会改写历史，新手用错会丢代码。等你独立提交过 50 次再说 |
| `git stash` | 有用，但今天的场景用不上 |
| 分支合并 | 第 9 天之后再说，一个人写项目暂时不需要 |
| `git reset --hard` | **危险命令**，会永久丢掉未提交的修改。今天先用 `git restore` |
| GUI 工具（GitHub Desktop 等） | 先把命令行走顺。面试时问你 Git，说的是命令不是按钮 |

---

## 一句话总结

> **Git 不是备份工具，是时间机器。它只能带你回到你曾经 `commit` 过的时刻。**
> 所以：改完就 `git add`，想清楚了就 `git commit`。没提交的东西，Git 救不了你。
