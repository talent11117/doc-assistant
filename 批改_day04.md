# 批改：day04_files_json.py

批改时间：2026-10-15
运行结果：**代码在第 162 行崩溃，自测一条都没跑出来。**

```
FileNotFoundError: [Errno 2] No such file or directory:
'...\.tmp\没有这个文件.json'
```

---

## 一、总评

| 函数 | 结果 | 说明 |
|---|---|---|
| `save_scores` | ✅ **完全正确** | 三个要求全中，一次写对 |
| `make_report` | ✅ **结果正确** | 两条自测都过，但写法绕了远路（见 §4） |
| `load_scores` | ❌ **4 个问题** | 其中 1 个是致命的：它让整个程序崩了 |

**好消息**：`save_scores` 你一次就写对了。`ensure_ascii=False` 和 `indent=2` 都放对了位置，
`Path(path)` 也转了。这说明**写文件这条路你已经通了**。

**坏消息**：`load_scores` 把「读文件」和「错误处理」两个东西混在一起了。
这不是你笨，是异常（exception）这个概念本身有个反直觉的地方。看完下面你就懂了。

---

## 二、`load_scores` 的 4 个问题

你写的原文（第 67—73 行）：

```python
    try:
        floder = Path(path)
        with open(floder,"r",encoding = "utf-8") as f:
            json.load(f)
    except FileExistsError:
        print('文件不存在')
```

### 问题 1（致命）：`FileExistsError` 写错了，应该是 `FileNotFoundError`

这是它崩溃的直接原因。

你大概是这样想的：「文件不存在 → 那异常名字里应该有 File 和 Not 和 Found……诶，
`FileExistsError` 里有 File 也有 Error，差不多就是这个吧。」

但这两个是**完全不同**的两个异常：

| 异常名 | 什么时候抛 | 直译 |
|---|---|---|
| `FileNotFoundError` | 文件**找不到** | 文件没找到错误 |
| `FileExistsError` | 文件**已经存在**，你不该再建 | 文件已存在错误 |

`FileExistsError` 是「你想创建一个新文件夹，但同名的已经有了」时抛的。
你现在是**读**文件，永远不会遇到它。

所以真实情况是：

1. `open()` 抛出了 `FileNotFoundError`
2. 你的 `except` 只接 `FileExistsError`
3. **对不上 → 异常没人接 → 直接崩掉，程序退出**

这就是你看到的那一大串红字。

> **记住这句话**：`except` 后面写的名字，必须和真实抛出来的名字**一字不差**。
> 名字对不上，就等于没写 `except`。

**怎么知道真实名字是什么？** 看报错最后一行，它已经告诉你了：

```
FileNotFoundError: [Errno 2] No such file or directory: '...没有这个文件.json'
^^^^^^^^^^^^^^^^^
```

Python 把答案印在屏幕上了。**报错的最后一行，就是你要写进 `except` 的名字。**

### 问题 2：`json.load(f)` 读出来的东西被你扔了

```python
json.load(f)          # ← 读出来了，然后呢？没了
```

`json.load(f)` 会**返回**一个字典，但你没有用变量接住它，也没 `return`。

类比一下，这就像：

```python
def get_name():
    "张三"        # ← 写了个字符串，然后呢？函数返回的是 None
```

`"张三"` 这个值被算出来了，然后就丢掉了。函数最后悄悄返回 `None`。

`json.load(f)` 同理：字典被读出来了，然后丢了，函数返回 `None`。

正确的样子应该是二选一：

```python
# 写法 A：直接 return
with open(floder, "r", encoding="utf-8") as f:
    return json.load(f)

# 写法 B：先接住再返回（更清楚，推荐你先用这个）
with open(floder, "r", encoding="utf-8") as f:
    data = json.load(f)
return data
```

### 问题 3：`print('文件不存在')` 不等于 `return {}`

题目要求是：

> 文件不存在时，返回 `{}`（空字典），不要崩溃。

`print` 只是**在屏幕上打一行字**，它和「返回值」是两回事。
你打印完之后，函数依然悄悄返回 `None`。

自测里是这样检查的：

```python
check("load_scores(不存在的文件)", load_scores(...), {})
```

它会拿你的返回值去和 `{}` 比。你返回 `None`，`None == {}` 是 `False`，所以即使不崩，
这一条也会显示 `[未通过]`。

**该写的是：**

```python
except FileNotFoundError:
    return {}
```

### 问题 4：变量名 `floder` 是 `folder` 的拼写错误

这个不影响运行，但要提。而且更准确地说，**你拿到的是一个文件路径，不是文件夹**。

```python
floder = Path(path)      # 拼错了，而且语义也不太对
path_obj = Path(path)    # 更好
```

`path` 是参数名，`path_obj` 表示「path 转成的 Path 对象」。
变量名拼错在初学阶段无所谓，但**如果以后在几百行代码里把 `folder` 拼错**，
你搜的时候就会搜不到，会很痛苦。现在养成习惯。

---

## 三、改好的 `load_scores`

```python
def load_scores(path):
    """读一个 JSON 文件，返回里面的字典；文件不存在时返回 {}。"""
    try:
        path_obj = Path(path)
        with open(path_obj, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}
```

**注意 `return data` 的位置**：它在 `with` 块**外面**，但在 `try` 里面。

为什么可以放外面？因为 `with` 块结束时文件会自动关闭，而 `data` 这个变量还在。
放里面（缩进到 `with` 底下）也能跑，但放外面更能体现「先读完，再返回」的顺序。

**为什么 `return data` 不能放到 `try` 外面？**

```python
    try:
        ...
        data = json.load(f)
    except FileNotFoundError:
        return {}
    return data          # ← 如果这样写，也能跑
```

这样写其实也对。但如果 `except` 分支里只 `print` 不 `return`，走到最后这行时
`data` 根本没被定义过，会报 `UnboundLocalError: local variable 'data' referenced
before assignment`——又是一个新的崩溃。**先按上面那个版本写，别自找麻烦。**

---

## 四、`make_report` 能跑，但绕了远路

你的写法（第 117—125 行）：

```python
    if not scores:
        return {"count": 0, "average": 0, "best": None}

    lists = {}
    list1 = ['count','average','best']
    list2 = [len(scores),average_score(scores),best_course(scores)]
    for i in range(3):
        lists[list1[i]] = list2[i]
    return lists
```

**结果是对的**，两条自测都过。但有意思的是：

- 空字典那个分支，你直接写了字典字面量 `{"count": 0, ...}`
- 正常那个分支，你绕成了「两个列表 + 循环下标」

**同一个函数里，你用了两种完全不同的思路。** 而且第二种（两个列表靠下标对齐）
是个很危险的习惯——将来 `list1` 加了第 4 个元素但 `list2` 忘了加，
两个列表就错位了，而且**不会报错**，只会悄悄返回错的数据。

既然你会写字典字面量，直接写就行：

```python
def make_report(scores):
    """把成绩字典变成一份报告字典。"""
    if not scores:
        return {"count": 0, "average": 0, "best": None}

    return {
        "count": len(scores),
        "average": average_score(scores),
        "best": best_course(scores),
    }
```

**为什么空字典还要单独判断？** 其实不用——`average_score({})` 你已经写成返回 `0` 了，
`best_course({})` 返回 `None`，`len({})` 是 `0`。所以理论上不写那个 `if` 也对：

```python
    return {
        "count": len(scores),                      # {} → 0
        "average": average_score(scores),          # {} → 0
        "best": best_course(scores),               # {} → None
    }
```

**但保留 `if not scores:` 更好**，理由是你昨天自己定的边界规则在今天就生效了。
写代码时明确写出「空的情况怎么办」，比依赖三个函数碰巧都对要踏实。

> 这正是第 3 天那个 `if not scores: return 0` 的价值所在——
> 你今天什么都不用想，直接复用就行。

---

## 五、关于 `try/except`，你需要建立的直觉

这是今天最值得带走的东西。

**没有 `try` 的时候，程序遇到异常会怎样？**

一路往上炸，直到把整个程序炸停，屏幕上打印一大串红字。
你刚才看到的就是这个。

**`try/except` 的作用是「在这个点上把异常拦下来，换个方式继续」。**

```python
try:
    可能出错的事
except 具体的错误名:
    出错之后怎么办
```

三个关键点：

1. **`except` 后面的名字必须精确匹配**（问题 1）
2. **`except` 分支里要有 `return`**，否则函数返回 `None`（问题 3）
3. **`try` 里正常路径也要有 `return`**，否则读到了也白读（问题 2）

**最后一条经验**：不要写 `except Exception:` 这种什么都接的。
`main.py` 里那个教程代码就是这么写的，它会把「key 过期」「网络断了」
「返回的 JSON 格式变了」全部吞掉，只留一句看不出原因的报错。
**只接你预期会发生的那一种。** 你今天就预期「文件可能不在」，那就只接 `FileNotFoundError`。

---

## 六、现在做什么

1. 按 §3 改 `load_scores`
2. 按 §4 简化 `make_report`（可选，现在的结果已经对了）
3. 运行：

```powershell
cd C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant
.\dev.cmd run day04_files_json.py
```

4. 目标：**6 条全 `[通过]`**

改完告诉我，我再看一遍。

---

## 附：本次批改怎么验证的

因为 `load_scores` 一崩，自测后面的内容全跑不到，所以我单独写了个脚本
（`.tmp/verify_day04_parts.py`）只测 `save_scores` 和 `make_report`，确认它们是好的：

```
save_scores 写出文件: True
  中文未转义: True
  有缩进: True
  内容: '{\n  "数学": 80,\n  "物理": 90,\n  "英语": 100\n}'
make_report(三门): {'count': 3, 'average': 90.0, 'best': '英语'}
make_report({}): {'count': 0, 'average': 0, 'best': None}
```

所以这两个不用动，专心改 `load_scores` 就行。
