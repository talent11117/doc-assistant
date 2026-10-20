# day06_api.py 批改

**检查时间**：2026-10-17
**结果**：16 条自测里 **4 条通过、6 条报错、6 条没跑到**（程序在第 7 组崩了，后面的测试根本没执行）

先说结论：**今天的错误全部集中在一个地方——你没有分清「r 是什么」和「r 身上有什么」。**
5 个函数/方法里有 4 个栽在同一个坑上。把这一件事想通，今天的内容就通了。

---

## 一、先看现在跑出来是什么样

```
1. get_json：成功的情况
  [报错] AttributeError: 'Response' object has no attribute 'ststus_code'

2. get_json：404
  [报错] AttributeError: 'Response' object has no attribute 'ststus_code'

3. get_json：500
  [报错] AttributeError: 'Response' object has no attribute 'ststus_code'

4. timeout
超时 HTTPConnectionPool(...): Read timed out. (read timeout=1)   ← 这行是你 print 出来的
  [通过] timeout=1 撞上慢接口 → None
  [通过] get_with_timeout 也一样
  [未通过] get_with_timeout 等得够久 → 拿到
          你写的：None
          应该是：{'message': '我慢吞吞地来了'}

5. get_scores
  [报错] TypeError: get_json() got an unexpected keyword argument 'timeout'
  [报错] TypeError: get_json() got an unexpected keyword argument 'timeout'

6. post_json
  [通过] 服务器收到的东西和发出的一样
  [通过] 换一组数据也对

7. ApiClient：地址存在对象身上
  AttributeError: 'ApiClient' object has no attribute 'base_url'
  ↑ 这里程序直接崩了，第 7、8 组的 6 条测试一条都没跑
```

---

## 二、五类错误，逐个讲

### 根因 A：把「方法」当成「属性」用（忘了加括号）

**出问题的地方**：`get_json` 第 68 行、`get_with_timeout` 第 138 行、`hello` 第 173 行、`scores` 第 185 行

你写的是：

```python
return r.json        # get_json 第 68 行
return r.josn        # get_with_timeout 第 138 行
return r.josn()["message"]    # hello 第 173 行
return r.josn()               # scores 第 185 行
```

我实际跑了一下 `r.json` 不加括号返回什么：

```
r.json   → <bound method Response.json of <Response [200]>>
r.json() → {'message': '你好，我是假服务器'}
```

**`r.json` 不加括号，你拿到的是「这个方法本身」，不是它算出来的结果。**
就像一个函数名 `get_average` 和调用 `get_average(...)` 的区别——名字只是名字，加括号才执行。

**这和你昨天学的 `self.name` vs `self.bark()` 是同一件事**：

| 写法 | 名字 | 是什么 |
|---|---|---|
| `self.name` | 属性 | 已经在那的数据 |
| `self.bark()` | 方法 | 要加括号才执行 |
| `r.text` | 属性 | 已经在那的字符串 |
| `r.json()` | 方法 | **要加括号** |

**改法**：

```python
return r.json()      # 注意括号
```

另外 `josn` 是 `json` 拼错了（第 138、173、185 行）。拼错成 `josn` 时 Python 报的是
`AttributeError: 'Response' object has no attribute 'josn'`——**它其实在提醒你拼错了**，
但你现在这行没跑到（被前面的错误挡住了），所以还没见过这个报错。

---

### 根因 B：属性名记混了（`status_code` 拼错、`encoding` 用错）

**出问题的地方**：`get_json` 第 65 行、`get_with_timeout` 第 135 行

```python
if r.ststus_code != 200:      # 第 65 行：status 拼成了 ststus
```

报错很明确：

```
AttributeError: 'Response' object has no attribute 'ststus_code'
```

**这个报错其实是好消息**——它在告诉你「Response 对象上没有叫 ststus_code 的东西」。
正确名字是 `status_code`（status + code，中间有下划线）。

第二个更隐蔽：

```python
if r.encoding != 200:         # 第 135 行
```

`encoding` 不是状态码，是**字符编码**。我实际打印了一下：

```
r2.encoding        = 'utf-8'
r2.encoding != 200 = True        ← 永远为 True！
r2.status_code     = 200
```

`'utf-8' != 200` 永远成立，所以这个 `if` **永远进去**，函数**永远 `return None`**。
这就是为什么第 6 条「等得够久 → 拿到」显示 `你写的：None`。

**这个错误比拼写错误危险得多**，因为它不报错，只是悄悄返回错的结果。
（跟昨天 `best_score = 0` 那个坑是同一类。）

**改法**：

```python
if r.status_code != 200:      # 用 status_code，不是 encoding
```

---

### 根因 C：没想清楚 `r` 到底是什么

**出问题的地方**：`get_scores` 第 90-94 行

```python
r = get_json(base_url,"/scores",timeout=5)
if not r.json():
    return {}
else:
    return r.json()
```

这里有**两个**问题。

**问题 1：参数名不对（第 90 行）**

```
TypeError: get_json() got an unexpected keyword argument 'timeout'
```

看 `get_json` 的定义：

```python
def get_json(base_url, path, seconds=5):
#                          ^^^^^^^ 这个参数叫 seconds，不叫 timeout
```

`timeout` 是 `requests.get()` 的参数名，`seconds` 是**你自己**定的参数名。
传的时候必须用你自己定的那个名字。

**改法**（三种都对）：

```python
r = get_json(base_url, "/scores")            # 用默认值 5 秒，最省事
r = get_json(base_url, "/scores", 5)         # 按位置传，第 3 个就是 seconds
r = get_json(base_url, "/scores", seconds=5) # 按名字传，必须写 seconds
```

**问题 2：`r` 已经是字典了，不能再 `.json()`**

`get_json` 的返回值是什么？看它的文档：

```
返回：
    - 状态码是 200  → 返回 r.json()（一个字典）
```

**`get_json` 已经把 JSON 解析好了，返回的就是字典。**
所以 `r` 是 `{"数学": 80, ...}` 这样一个 dict，dict 身上**没有** `.json()` 这个方法。

我实际跑了一下：

```
[get_scores(BASE)] TypeError: get_json() got an unexpected keyword argument 'timeout'
```

先卡在参数名上，还没走到 `.json()`。你把参数名改对之后，会立刻撞上第二个错：

```
AttributeError: 'dict' object has no attribute 'json'
```

**记住这条链**：

```
requests.get(...)  →  返回 Response 对象
Response.json()    →  返回 dict
```

**每跨一层，对象类型就变了。** 你现在在第二层（已经是 dict），却又调了一次第一层的方法。

**改法**：

```python
def get_scores(base_url):
    data = get_json(base_url, "/scores")
    if data is None:
        return {}
    return data
```

注意我把变量名从 `r` 改成了 `data`——**因为它是数据，不是响应**。
名字起对了，脑子就不容易乱。这是个很实用的习惯。

顺便说 `if not r.json()` 这个写法：即使 `r` 是 dict，`if not {}` 也确实为 `True`
（空字典在 Python 里算「假」），逻辑上碰巧能对。但**`if data is None` 更准确**，
因为你要判的是「失败了」，不是「空的」——这两件事不一样。

---

### 根因 D：赋值方向反了

**出问题的地方**：`ApiClient.__init__` 第 159 行

```python
def __init__(self, base_url):
    base_url = self.base_url      # ← 反了
```

报错：

```
AttributeError: 'ApiClient' object has no attribute 'base_url'
```

**为什么报这个错？** 因为 `=` 右边的先算。`self.base_url` 这时候还不存在
（对象刚造出来，`__init__` 还没存过任何东西），所以读它就炸了。

**这一行的实际含义是**：「把 `self.base_url` 的值，存进局部变量 `base_url`」——
方向完全反了。你要的是「把参数 `base_url` 的值，存到对象身上」。

**改法**：

```python
def __init__(self, base_url):
    self.base_url = base_url      # 左边是"存到哪"，右边是"存什么"
```

**记法**：`self.xxx = yyy` 永远读作「**把 yyy 存进我自己的 xxx**」。
左边是抽屉，右边是东西。昨天 `ScoreBook` 你写对了（`self.name = name`），今天不知怎么反了。

**这个错很典型**：昨天刚学完，今天换个名字就写反。说明当时是「照着形状抄」，
不是「想清楚在干什么」。这类错误只能靠多写几遍磨掉，不用自责，但要留意。

---

### 根因 E：只写了「顺利的情况」

**出问题的地方**：`post_json` 第 114-115 行

```python
r = requests.post(base_url + "/echo",json=data,timeout=5)
return r.json()["received"]
```

**这两行在自测里是 `[通过]` 的**——因为假服务器一切正常。
但它和你抄的 `main.py` 有**完全一样的毛病**：

- 没查 `status_code`（服务器返回 500 时，`r.json()["received"]` 会 KeyError）
- 没有 try/except（网络断了直接崩）

**这就是「测试通过 ≠ 代码正确」的活例子。** 自测只喂了正常数据。

**改法**：

```python
def post_json(base_url, data):
    try:
        r = requests.post(base_url + "/echo", json=data, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()["received"]
    except requests.exceptions.RequestException:
        return None
```

我知道你可能会想「自测过了就行」。但明天就要拿这套东西去调真的 DeepSeek 接口了，
那时候网络会断、key 会失效、服务器会返回 401/429——**这些都不会是 200**。

---

## 三、还有一个「没报错但不对」的地方

`get_json` 的 except 块（第 69-72 行）：

```python
except requests.exceptions.Timeout as e:
    print('超时',e)
except requests.exceptions.ConnectionError as e:
    print('连不上',e)
```

**为什么第 4 条「timeout=1 → None」显示通过了？**
因为函数走到 except 里 print 完，没有 `return`，Python 就**隐式返回 `None`**。
结果碰巧对了。

但有两个问题：

1. **`print` 污染了输出。** 你看到的那行 `超时 HTTPConnectionPool(...)` 就是它打的。
   一个「取数据的函数」不应该往屏幕上说话——将来这函数被调用一千次，屏幕就刷一千行。
   要输出应该在**调用方**输出。

2. **依赖隐式 `None` 很脆弱。** 万一你以后在 except 后面又加了几行代码，
   返回值就不是 `None` 了。**显式写 `return None`**，让读代码的人一眼看到。

**改法**：

```python
except requests.exceptions.RequestException:
    return None
```

用 `RequestException` 一个就够，它是 `Timeout` 和 `ConnectionError` 的**共同父类**——
接住父类就等于接住所有子类。这是昨天「继承」概念的第一次实战。

---

## 四、一个值得表扬的地方

你 `get_json` 里写的是：

```python
except requests.exceptions.Timeout as e:
except requests.exceptions.ConnectionError as e:
```

**没有写 `except Exception`。** 正因为这样，`ststus_code` 这个拼写错误才能
以 `AttributeError` 的形式**暴露出来**，让你看到真实原因。

对比一下：如果你写了 `except Exception`，那 `ststus_code` 的报错会被吞掉，
你只会看到「所有测试都返回 None」，然后完全不知道为什么。

**这就是我昨天说「不要写 except Exception」的实际价值。** 你已经做对了。

---

## 五、修改清单（按顺序改，改一条跑一次）

| 序号 | 文件位置 | 现在 | 改成 |
|---|---|---|---|
| 1 | `day06_api.py:65` | `r.ststus_code` | `r.status_code` |
| 2 | `day06_api.py:68` | `return r.json` | `return r.json()` |
| 3 | `day06_api.py:69-72` | `print(...)` | `return None` |
| 4 | `day06_api.py:90` | `timeout=5` | 删掉，或改成 `seconds=5` |
| 5 | `day06_api.py:91-94` | `r.json()` | `data is None` 判断 |
| 6 | `day06_api.py:114-115` | 无检查 | 补 `status_code` + `try/except` |
| 7 | `day06_api.py:135` | `r.encoding != 200` | `r.status_code != 200` |
| 8 | `day06_api.py:138` | `r.josn` | `r.json()` |
| 9 | `day06_api.py:159` | `base_url = self.base_url` | `self.base_url = base_url` |
| 10 | `day06_api.py:173` | `r.josn()["message"]` | `data["message"]` |
| 11 | `day06_api.py:174` | `except:` | `except requests.exceptions.RequestException:` |
| 12 | `day06_api.py:185` | `r.josn()` | `return r` |

---

## 六、改完应该长这样（对照用，先自己改再看）

```python
def get_json(base_url, path, seconds=5):
    try:
        r = requests.get(base_url + path, timeout=seconds)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.exceptions.RequestException:
        return None


def get_scores(base_url):
    data = get_json(base_url, "/scores")
    if data is None:
        return {}
    return data


def post_json(base_url, data):
    try:
        r = requests.post(base_url + "/echo", json=data, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()["received"]
    except requests.exceptions.RequestException:
        return None


def get_with_timeout(base_url, path, seconds):
    try:
        r = requests.get(base_url + path, timeout=seconds)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.exceptions.RequestException:
        return None


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def hello(self):
        data = get_json(self.base_url, "/hello")
        if data is None:
            return None
        return data["message"]

    def scores(self):
        return get_scores(self.base_url)
```

我用这套代码跑了一遍自测：**16 通过，0 失败**。

---

## 七、今天真正要带走的一句话

> **每调用一次函数，先问自己：它返回的是什么类型？**

今天的错误全是这一件事：

| 你的假设 | 实际情况 |
|---|---|
| `r.json` 是数据 | 它是方法对象，要 `r.json()` |
| `r.encoding` 是状态码 | 它是 `'utf-8'` |
| `get_scores` 里 `r` 还是 Response | 它已经是 dict 了 |
| `self.base_url` 已经存在 | 它要你先赋值 |

**下次写之前，先在心里过一遍**：
「我现在手里拿的是 Response 还是 dict？这个属性是数字还是字符串？」

---

改完运行：

```powershell
.\dev.cmd run day06_api.py
```

16 条全绿了告诉我。然后我们就去收拾 `C:\Users\jack\Desktop\learn-fastapi\main.py`——
你会发现它的 bug 和今天的 `post_json` 是同一个毛病。
