# 第 8 天笔记批改

> 你的笔记文件：`doc-assistant\.tmp\git练习_day08.md`
> 批改日期：2026-10-20

---

## 总评

| 题号 | 题目 | 你的答案 | 判定 |
|---|---|---|---|
| 1 | 工作区/暂存区/版本库对应哪一步 | 改文件未 add / add 未 commit / commit 完 | ✅ **完全正确** |
| 2 | `git add` 之后反悔用什么命令 | `git restore +文件名` | ❌ **不对**，这是撤销工作区改动 |
| 3 | `git commit` 之后反悔用什么命令 | `git reset --hard HEAD^` | ⚠️ **命令对，但理解错了 `^` 的含义** |

第 1 题答得干净利落，说明你真的把三个区的概念想清楚了。第 2、3 题踩的是**同一类坑**：把两个作用范围不同的命令当成了一个。

---

## 第 2 题：`git add` 之后反悔

### 你写的

```
git restore +文件名
```

### 为什么不对

**`git restore <文件>` 撤的是"工作区的改动"，不是"暂存区的登记"。**

`git add` 之后，文件有三个"版本"同时存在：

| 位置 | 内容 |
|---|---|
| 最后一次提交（HEAD） | 旧内容 |
| 暂存区（index） | **你 add 进去的新内容** |
| 工作区（硬盘上的文件） | 新内容 |

`git restore <文件>` 做的事是：**用"暂存区的内容"覆盖"工作区的内容"**。

但此时暂存区里已经是新内容了，工作区也是新内容——**两边一样，覆盖等于什么都没做。**

### 我实测给你看

```powershell
# 1. 改文件，然后 add
$ git status --short
M  a.txt          ← 注意 M 在左边，表示"已暂存"

# 2. 跑你笔记里的命令
$ git restore a.txt
$ git status --short
M  a.txt          ← 完全没变！还在暂存区里

$ 文件内容: 改过的内容   ← 也没变
```

**你的命令跑完，状态一点没变。** 这就是"不报错但做错事"。

### 正确的命令

```powershell
git restore --staged a.txt
```

多了一个 `--staged`。意思是"**只把暂存区退回上一次提交的样子，工作区的文件别动**"。

实测：

```powershell
$ git restore --staged a.txt
$ git status --short
 M a.txt          ← 注意 M 跑到右边了，表示"未暂存"

$ 文件内容: 改过的内容   ← 你的改动还在！没丢
```

### 三个 `restore` 的区别，一次记清

| 命令 | 撤什么 | 你的改动 | 用在哪 |
|---|---|---|---|
| `git restore 文件` | 工作区 ← 暂存区 | **丢了** | 改错了，想全部作废 |
| `git restore --staged 文件` | 暂存区 ← HEAD | **还在**（变回未暂存） | add 了但不想提交 |
| `git restore --source=HEAD 文件` | 工作区 ← HEAD | **丢了** | 想回到上次提交的样子，连暂存区一起跳过 |

**一句话记法：`--staged` 只管"篮子"，不管"菜"。**

- 不带 `--staged`：把菜倒掉，换成篮子里那份
- 带 `--staged`：把篮子里的菜倒回桌上，菜还在

---

## 第 3 题：`git commit` 之后反悔

### 你写的

```
git reset --hard HEAD^    回退一个版本
^的数量  -->表示回退几个版本
HEAD~100  回退100个版本
```

### 命令是对的

`git reset --hard HEAD^` 确实能回退一个版本。实测：

```powershell
$ git log --oneline
7f156b9 c3
8562aae c2
b751246 c1

$ git reset --hard HEAD^
HEAD is now at 8562aae c2

$ git log --oneline
8562aae c2
b751246 c1

$ 文件内容: v2      ← 文件也真的回到了 v2
```

### 但 `^` 的含义你理解错了

你写"`^` 的数量表示回退几个版本"。**这个说法只在一种情况下成立，而且会误导你。**

`^` 真正的含义是：**"第几个爸爸"**。

Git 的提交可以有两个爸爸——**合并提交（merge commit）** 就有两个。所以：

| 写法 | 真正的含义 | 结果 |
|---|---|---|
| `HEAD^` | 第 1 个爸爸 | 往回 1 个 |
| `HEAD^2` | **第 2 个爸爸**（只在合并提交上有） | **不是"往回 2 个"！** |
| `HEAD^^` | 爸爸的爸爸 | 往回 2 个 |
| `HEAD~2` | 顺着第一爸爸往回 2 个 | 往回 2 个 |

**`HEAD^2` 和 `HEAD^^` 是两个完全不同的东西。** 这是新手最容易搞混的一对。

### 实测：`HEAD^2` 在普通提交上直接报错

我建了 3 个普通提交（不是合并），然后：

```powershell
$ git log --oneline -1 HEAD^
d91fbd0 c2          ← 往回 1 个，正确

$ git log --oneline -1 HEAD^^
0a4f05a c1          ← 往回 2 个，正确

$ git log --oneline -1 HEAD^2
fatal: ambiguous argument 'HEAD^2': unknown revision or path not in the working tree.
                    ↑ 报错！因为普通提交没有第二个爸爸
```

**如果 `^2` 真是"往回 2 个"，这里就该输出 c1，而不是报错。** 报错本身就证明了它的含义不是"数量"。

### 那 `HEAD~100` 呢

`~` 才是"数量"符号。`HEAD~100` = 顺着第一爸爸往回 100 个。**你的理解在这里是对的。**

但有个前提：**仓库里得有 100 个提交。** 我实测在只有 2 个提交的仓库里跑：

```powershell
$ git reset --hard HEAD~100
fatal: ambiguous argument 'HEAD~100': unknown revision or path not in the working tree.
```

**没有第 100 个祖先，直接报错，什么都不会发生。**（这算好事——报错比悄悄算错安全。）

### 修正后的记法

| 符号 | 含义 | 记忆方法 |
|---|---|---|
| `^` | 第 1 个爸爸 = 往回 1 个 | `^` 像"往上戳一下" |
| `^2` | 第 2 个爸爸（合并提交才有） | **不是数量！** |
| `^^` | 往回 2 个 | 戳两下 |
| `~N` | 往回 N 个 | `~` 才是数量 |

**日常只用两个：`HEAD^`（回退 1 个）和 `HEAD~3`（回退 3 个）。`^2` 你这辈子可能都用不上。**

---

## 关于 `--hard` 的一个警告

你笔记里写的是 `git reset --hard HEAD^`。**这个命令是对的，但它是今天文档里唯一标红的危险命令。**

`--hard` 的意思是"**工作区、暂存区、提交历史，三样一起改**"。它会：

1. 删掉最新那次提交
2. **永久丢掉你所有未提交的改动，不给第二次机会**

实测一下就明白有多狠：

```powershell
# 有未提交的改动
$ echo "重要内容" > a.txt
$ git status --short
 M a.txt

# 跑 reset --hard
$ git reset --hard HEAD^
HEAD is now at 8562aae c2

$ cat a.txt
v2                  ← "重要内容"永久消失了
```

### 更安全的替代

**想撤销提交但保留改动**，用 `--soft` 或 `--mixed`（默认）：

| 命令 | 提交历史 | 暂存区 | 工作区 | 你的改动 |
|---|---|---|---|---|
| `git reset --soft HEAD^` | 回退 | 保留 | 保留 | ✅ 都在，还暂存着 |
| `git reset HEAD^`（默认 `--mixed`） | 回退 | 清空 | 保留 | ✅ 都在，变未暂存 |
| `git reset --hard HEAD^` | 回退 | 清空 | **覆盖** | ❌ **全丢** |

**规则：想不清的时候，先不加 `--hard`。** 少了 `--hard` 最多是多跑一条 `git restore`，加了 `--hard` 可能丢掉一天的工作。

### 还有一个更安全的：`git revert`

`reset` 是"**假装那次提交没发生过**"——它改写历史。如果已经推到 GitHub 了，别人拉代码会出问题。

`revert` 是"**新增一次提交，把上次的改动反向抵消**"——历史不变，只往后加。

```powershell
git revert HEAD        # 撤销最后一次提交，但历史里多一条"撤销记录"
```

**已经 push 过的提交，用 `revert` 不用 `reset`。** 这个区别面试会问。

---

## 你今天真正学到的东西

不是三条命令，是**一个思维习惯**：

> **每敲一条命令，先问自己："它动的是哪一层？"**

Git 有四层：工作区 → 暂存区 → 本地仓库 → 远程仓库。

`git add` 动第 1→2 层，`git commit` 动第 2→3 层，`git push` 动第 3→4 层。

**反悔的命令，就是往回推一层**：

| 想撤销 | 命令 | 动的是 |
|---|---|---|
| 工作区的改动 | `git restore 文件` | 2 → 1 |
| 暂存区的登记 | `git restore --staged 文件` | 3 → 2 |
| 本地提交 | `git reset HEAD^` | 4 → 3（本地） |
| 远程提交 | `git revert HEAD` | 加一条反向提交 |

你今天第 2 题答错，本质是**把"2→1"当成了"3→2"**。想清楚层次就不会错了。

---

## 自查

```powershell
cd C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant\.tmp\git-practice

# 1. 改 note.txt，add，然后用 --staged 撤销
git add note.txt
git status --short        # 应该看到 M 在左边
git restore --staged note.txt
git status --short        # 应该看到 M 跑到右边，文件内容没变

# 2. 确认 ^ 的含义
git log --oneline
git log --oneline -1 HEAD^      # 应该是"第一次提交"
git log --oneline -1 HEAD^2     # 应该报错
```

跑完把这两条结果补进你的笔记。
