# 第 5 天：把函数和数据装进一个盒子里（类）

**日期**：2026-10-16
**昨天**：day04 全 6 条通过 ✅

---

## 今天的顺序（按这个顺序做，别跳）

### 第 1 步：先读，别写（约 20 分钟）

打开 `day05_class_intro.py`，从头读到尾，**每一节都自己敲一遍**，运行看输出：

```powershell
cd C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant
.\dev.cmd run day05_class_intro.py
```

这个文件**不用改，读懂就行**。重点看两节：

- **第 3 节**：`self` 是什么 → 输出里 `c1` 改名字后 `c2` 不受影响
- **第 4 节**：`tricks` 写在 `class` 下面 → 阿黄学会"坐下"，**阿黑也跟着会了**

第 4 节那个 `['坐下']` 重复出现两遍，就是今天要避免的 bug。

### 第 2 步：做题（约 40 分钟）

打开 `day05_classes.py`，写 `ScoreBook` 类的 **5 个方法**：

| 方法 | 要做什么 | 你其实已经会了 |
|---|---|---|
| `__init__` | 存 `self.name`，建空 `self.scores` | 就是 `day05_class_intro.py` 第 2 节 |
| `add` | 往 `self.scores` 加一项 | 给字典加一项：`d[键] = 值` |
| `average` | 平均分，空的时候返回 0 | **第 3 天你写的 `average_score`** |
| `best` | 最高分的课，空的时候返回 None | **第 3 天你写的 `best_course`** |
| `save` | 存成 JSON 文件 | **第 4 天你写的 `save_scores`** |

**今天真正新的只有前两个。** 后三个是把你已经写对过的东西，
把 `scores` 换成 `self.scores` 而已。

### 第 3 步：运行检查

```powershell
.\dev.cmd run day05_classes.py
```

目标：**12 条全 `[通过]`**

---

## 两个必须记住的点

### 1. `self.scores = {}` 必须写在 `__init__` 里面

```python
# ✅ 对
class ScoreBook:
    def __init__(self, name):
        self.name = name
        self.scores = {}       # ← 在里面

# ❌ 错（这就是第 4 节那只 BadDog）
class ScoreBook:
    scores = {}                # ← 在外面，所有成绩本共用同一个字典
    def __init__(self, name):
        self.name = name
```

写错的话，**自测第 5 条会挂**：给张三加成绩，李四的本里也会出现。

### 2. `add` 不要 `return` 东西

```python
def add(self, course, score):
    self.scores[course] = score     # 直接改自己身上的字典，不用 return
```

因为字典是"可变"的，改了就改了。这一点和 `average`（要 `return` 一个数字）不一样。

---

## 如果卡住了

| 卡在哪 | 去看 |
|---|---|
| 不知道 `self` 是什么 | `day05_class_intro.py` 第 3 节 |
| `__init__` 不知道写几行 | `day05_class_intro.py` 第 2 节（Dog 类） |
| 忘了怎么写平均分 | 翻回 `day03_split_functions.py` 看你写的 `average_score` |
| 忘了怎么写文件 | 翻回 `day04_files_json.py` 看你写的 `save_scores` |
| 报 `AttributeError` | 检查 `__init__` 里是不是漏了 `self.xxx = ...` |

**卡住 15 分钟以上再看答案**，抄来的不算学会。

---

## 今天不学的（别提前碰）

- **继承**（`class A(B)`）—— 知道有这么个东西就行，`main.py` 里的 `BaseModel` 用了
- **`@property`、`@staticmethod`、`__str__`** —— 以后再说
- **`lambda`** —— 自测代码里用了一点，先照抄，以后专门讲

---

## 做完之后

改完告诉我，我看一遍。然后有两个待办还悬着：

1. `C:\Users\jack\Desktop\learn-fastapi\main.py` 的 5 个 bug（从 BUG 2 加 `timeout` 开始）
2. 那个已经泄露的 DeepSeek API Key 记得去 https://platform.deepseek.com/api_keys 删掉重建
