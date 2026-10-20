# 第 6 天：用程序跟服务器说话（API 请求）

**日期**：2026-10-17（周六）
**昨天**：day05 全 12 条通过 ✅

---

## 今天的顺序（按这个顺序做，别跳）

### 第 0 步：先花 3 分钟修一个昨天留下的坑

你 day05 的 `best()` 里有一行：

```python
best_score = 0
```

自测 12 条全过，因为测试数据里最高分是 100。但我用别的数据试了一下：

```
全是 0 分时   best() = None     ← 应该是 "数学"
全是负分时    best() = None     ← 应该是 "扣分"
```

**原因**：初始值设成 `0`，意味着「比 0 大的才算候选」。
如果所有分数都是 0 或负数，一个都不会被选中，`best_name` 一直是 `None`。

**改法**（把初始值设成"比任何分数都小"）：

```python
best_score = -1
```

或者更稳的写法，先拿第一门课当初始值。但 `-1` 够用了——分数不会是负数。

改完再跑一次 `day05_classes.py`，还是 12 条通过就对了。

> 这不是吹毛求疵。**"测试通过"和"代码正确"是两件事**，
> 测试只覆盖你想到的情况。这个坑现在就补，比将来上线了才发现便宜得多。

### 第 1 步：先读，别写（约 25 分钟）

打开 `day06_api_intro.py`，9 节，**每节都运行看输出**：

```powershell
cd C:\Users\jack\Documents\deepseek-harness\default-workspace\doc-assistant
.\dev.cmd run day06_api_intro.py
```

这个文件**不用改，读懂就行**。它用的是我写的假服务器 `mock_api.py`——
跑在你自己的电脑上，**不要钱、不用 API key、断网也能用**。

重点看这四节：

| 节 | 讲什么 | 你要带走的 |
|---|---|---|
| 第 4 节 | 状态码 | **404 和 500 时 `requests` 不报错**，要自己查 |
| 第 5 节 | `raise_for_status()` | 让失败变成异常，配合 try/except |
| 第 6 节 | `timeout` | 不写会**挂死**，这是你抄的 `main.py` 的 bug |
| 第 8 节 | 把地址存进对象 | 昨天学的类，今天用上了 |

第 6 节的输出长这样，注意同一个接口两种结果：

```
等 3 秒，timeout=10 → 200 {'message': '我慢吞吞地来了'}
timeout=1 → 超时了，抛 Timeout 异常 ✅
```

### 第 2 步：做题（约 45 分钟）

打开 `day06_api.py`，写 **4 个函数 + 1 个类**：

| 要写的 | 干什么 | 关键点 |
|---|---|---|
| `get_json` | GET，返回字典或 None | 先查状态码，再 `r.json()` |
| `get_scores` | 拿成绩，失败给 `{}` | **调用 `get_json`，别重写一遍** |
| `post_json` | POST，拿回服务器收到的内容 | `json=data` 自动转换 |
| `get_with_timeout` | 亲手撞一次超时 | `timeout=1` 打慢接口 |
| `ApiClient` 类 | 把地址存进 `self` | 和昨天 `ScoreBook` 一个套路 |

### 第 3 步：运行检查

```powershell
.\dev.cmd run day06_api.py
```

目标：**16 条全 `[通过]`**

---

## 三个必须记住的点

### ① `timeout` 必须写

你抄的 `main.py` 第 30 行是错的：

```python
resp = requests.post(url, headers=headers, json=data)
#                                      ↑ 没有 timeout
```

不写 `timeout`，服务器不回话时程序会**永远卡住**——不报错、不退出。
线上服务里这叫"挂死"，一个卡住的请求占一个线程，卡多了整个服务就废了。

```python
resp = requests.post(url, headers=headers, json=data, timeout=60)
```

调大模型接口时 timeout 要设大（模型生成一段话可能几十秒），常见 30~120 秒。
**但必须设。**

### ② 404 和 500 时 `requests` 不报错

```python
r = requests.get(url)              # 服务器返回 404
data = r.json()["message"]         # ← KeyError 崩掉
```

因为 404 时服务器给的是 `{"error": "没有这个路径"}`，根本没有 `message` 这个键。

所以拿到响应后**第一件事是看状态码**：

```python
r = requests.get(url, timeout=5)
if r.status_code != 200:
    return None
return r.json()
```

### ③ `except` 要接对名字

```python
# ✅ 接网络异常
except requests.exceptions.RequestException:
    return None

# ❌ 什么都接（你抄的 main.py 里就是这么写的）
except Exception:
    return None
```

`except Exception` 会把你**自己代码写错**（比如 `r.josn()` 拼错）也一起吞掉，
只留一句看不出原因的报错。我写了个测试验证这个区别：

```
参考答案：16 通过，0 失败
题目与自测一致，且正确区分了「捕获网络异常」和「吞掉自己的 bug」。
```

---

## 如果卡住了

| 卡在哪 | 去看 |
|---|---|
| 不知道 GET/POST 区别 | `day06_api_intro.py` 第 1 节 |
| 不知道 `r.json()` 为什么要括号 | 第 2 节（属性 vs 方法） |
| 404 时崩了 `KeyError` | 第 4 节 |
| 不知道 `raise_for_status` | 第 5 节 |
| 不知道 timeout 怎么用 | 第 6 节 |
| `ApiClient` 不知道写什么 | 第 8 节 + 昨天的 `ScoreBook` |
| 报 `ModuleNotFoundError: mock_api` | 你没在 `doc-assistant` 目录下运行 |

**卡住 15 分钟以上再看入门文件。**

---

## 今天不学的（别提前碰）

- **`async` / `await` / `httpx.AsyncClient`** —— 以后讲，现在用同步的 `requests` 就够
- **`headers` 里放 API key** —— 明天的内容（真正调 DeepSeek）
- **重试 / 退避** —— 知道有这回事就行

---

## 做完之后

改完告诉我，我看一遍。然后明天的安排大概是：

**第 7 天：把假服务器换成真的 DeepSeek 接口**——
也就是回去收拾 `C:\Users\jack\Desktop\learn-fastapi\main.py` 那 5 个 bug。
那时候你就知道为什么每一行要那么写了。

另外那个泄露的 DeepSeek API Key 记得去 https://platform.deepseek.com/api_keys
删掉重建（如果还没做的话），明天要用新的。
