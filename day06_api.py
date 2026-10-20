# ============================================================
# 第 6 天任务 —— 用程序跟服务器说话
# ============================================================
#
# 目标：学会 GET / POST / 状态码 / timeout / 出错处理
# 验收：下面 4 个函数 + 1 个类写对，自测全部显示 [通过]
#
# 怎么用：
#   1. 先读 day06_api_intro.py（9 节，运行看输出）
#   2. 再写这个文件里 5 处 TODO
#   3. 运行：.\dev.cmd run day06_api.py
#
# ⚠️ 先自己写，卡住 15 分钟以上再看 day06_api_intro.py。
#
# 为什么今天重要？
#   你抄的 main.py 里最核心的一行是：
#       resp = requests.post(url, headers=headers, json=data)
#   这一行就是"跟服务器说话"。
#   之后调 DeepSeek、Qwen、任何 Agent 框架，都是同一件事换个地址。
#
#   而且你抄的那行**漏了 timeout**，今天你就会知道为什么这是 bug。
# ============================================================

import requests
import mock_api


# ============================================================
# 今天要你写的 4 个函数
# ============================================================

def get_json(base_url, path, seconds=5):
    """GET 请求，把结果变成字典返回。

    参数：
        base_url  服务器地址，比如 "http://127.0.0.1:54321"
        path      路径，比如 "/hello"
        seconds   timeout 秒数，默认 5

    返回：
        - 状态码是 200  → 返回 r.json()（一个字典）
        - 状态码不是 200 → 返回 None
        - 超时 / 连不上  → 返回 None

    例子：
        get_json(BASE, "/hello")        → {"message": "你好，我是假服务器"}
        get_json(BASE, "/没有这个")      → None
        get_json(BASE, "/slow", 1)      → None（1 秒等不到就放弃）

    提示：
      1. r = requests.get(base_url + path, timeout=seconds)
      2. 先看状态码：if r.status_code != 200: return None
      3. 再看成功：return r.json()
      4. 整个包在 try/except 里，接住这几种异常：
             requests.exceptions.Timeout          超时
             requests.exceptions.ConnectionError  连不上
         或者一次接住它们的共同父类（推荐，短一些）：
             requests.exceptions.RequestException
         ⚠️ 不要写 except Exception —— 那会把所有错误都吞掉，
            包括你自己代码写错（比如变量名拼错）导致的错误。
    """
    # TODO
    try:
        r =requests.get(base_url + path,timeout=seconds)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.exceptions.RequestException:
        return None





def get_scores(base_url):
    """从服务器拿成绩字典。

    返回：
        - 成功 → 那个字典，比如 {"数学": 80, "物理": 90, "英语": 100}
        - 失败 → 空字典 {}

    提示：
        - 别重新写一遍 requests.get！
        - 直接调用上面的 get_json(base_url, "/scores")
        - 如果它返回 None，你就返回 {}
    """
    # TODO
    data = get_json(base_url,"/scores",seconds=5)
    if data is None:
        return {}
    return data


def post_json(base_url, data):
    """POST 一个字典过去，把服务器收到的内容拿回来。

    参数：
        data  要送过去的字典，比如 {"course": "数学", "score": 80}

    返回：
        - 成功 → r.json()["received"]（服务器说它收到了什么）
        - 失败 → None

    提示：
        - requests.post(base_url + "/echo", json=data, timeout=5)
        - json=data 会自动把字典变成 JSON 字符串，
          还会自动加上请求头 Content-Type: application/json
        - 和 get_json 一样要检查状态码、要 try/except
    """
    # TODO
    try:
        r = requests.post(base_url + "/echo",json=data,timeout=5)
        if r.status_code != 200:
            return None
        return r.json()["received"]
    except requests.exceptions.RequestException:
        return None



def get_with_timeout(base_url, path, seconds):
    """带 timeout 的 GET。这个函数是为了让你亲手撞一次超时。

    返回：
        - 等到了 → r.json()
        - 超时了 → None
        - 其他错误 → None

    提示：
        - 和 get_json 几乎一样，只是 timeout 由参数传进来
        - 其实你可以直接 return get_json(base_url, path, seconds)
          但更建议你自己写一遍 try/except，练手感
    """
    # TODO
    try:
        r = requests.get(base_url + path,timeout=seconds)
        if r.status_code != 200:
            return None
        else:
            return r.json()
    except requests.exceptions.RequestException:
        return None



# ============================================================
# 今天要你写的 1 个类
# ============================================================

class ApiClient:
    """把服务器地址存在自己身上，之后调用就不用每次传了。

    这就是昨天 ScoreBook 的同一个套路：
        昨天：self.scores  → 不用每次传 scores
        今天：self.base_url → 不用每次传 base_url
    """

    def __init__(self, base_url):
        """把 base_url 存到 self.base_url。"""
        # TODO
        self.base_url = base_url

    def hello(self):
        """返回服务器那句问候语（字符串）；失败返回 None。

        提示：
            - 调用 get_json(self.base_url, "/hello")
            - 它返回的是 {"message": "..."} 这样的字典
            - 你要返回的是里面 message 那个字符串
            - 如果 get_json 返回 None，直接返回 None
        """
        # TODO

        data = get_json(self.base_url,"/hello")
        if data is None:
            return None
        return data["message"]



    def scores(self):
        """返回成绩字典；失败返回 {}。

        提示：直接调用 get_scores(self.base_url)
        """
        # TODO

        return get_scores(self.base_url)



# ============================================================
# 下面是自测代码，不用改。
# 运行：.\dev.cmd run day06_api.py
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("第 6 天自测：跟服务器说话")
    print("=" * 50)

    # 启动假服务器（就在你自己电脑上，不要钱、不用 key、断网也能用）
    BASE = mock_api.start()
    print(f"\n假服务器已启动：{BASE}")

    def safe(label, want, fn):
        """执行 fn()，把结果和 want 比。出错只记一条，不中断整个自测。"""
        try:
            got = fn()
        except Exception as e:
            print(f"  [报错] {label}")
            print(f"          {type(e).__name__}: {e}")
            return
        if got == want:
            print(f"  [通过] {label}")
        else:
            print(f"  [未通过] {label}")
            print(f"          你写的：{got!r}")
            print(f"          应该是：{want!r}")

    print("\n1. get_json：成功的情况")
    safe("GET /hello 拿到字典", {"message": "你好，我是假服务器"},
         lambda: get_json(BASE, "/hello"))

    print("\n2. get_json：服务器说'没有这个路径'（404）")
    safe("404 要返回 None，不能崩", None,
         lambda: get_json(BASE, "/没有这个"))

    print("\n3. get_json：服务器自己出错（500）")
    safe("500 要返回 None", None,
         lambda: get_json(BASE, "/boom"))

    print("\n4. timeout：等不到就放弃")
    safe("timeout=1 撞上慢接口 → None", None,
         lambda: get_json(BASE, "/slow", 1))
    safe("get_with_timeout 也一样", None,
         lambda: get_with_timeout(BASE, "/slow", 1))
    safe("get_with_timeout 等得够久 → 拿到", {"message": "我慢吞吞地来了"},
         lambda: get_with_timeout(BASE, "/slow", 10))

    print("\n5. get_scores：拿数据，失败时给空字典")
    safe("成功时拿到三门成绩", {"数学": 80, "物理": 90, "英语": 100},
         lambda: get_scores(BASE))
    # 127.0.0.1:1 上没有服务器，连接会被拒绝
    safe("连不上时返回 {}（不能崩）", {},
         lambda: get_scores("http://127.0.0.1:1"))

    print("\n6. post_json：把数据送过去")
    payload = {"course": "数学", "score": 80}
    safe("服务器收到的东西和发出的一样", payload,
         lambda: post_json(BASE, payload))
    safe("换一组数据也对", {"course": "英语", "score": 100},
         lambda: post_json(BASE, {"course": "英语", "score": 100}))

    print("\n7. ApiClient：地址存在对象身上")
    client = ApiClient(BASE)
    safe("client.base_url 存对了", BASE,
         lambda: getattr(client, "base_url", "<还没定义>"))
    safe("client.hello()", "你好，我是假服务器", lambda: client.hello())
    safe("client.scores()", {"数学": 80, "物理": 90, "英语": 100},
         lambda: client.scores())

    print("\n8. 两个 client 互不干扰")
    other = ApiClient("http://127.0.0.1:1")     # 一个连不上的地址
    safe("other.scores() 返回 {}", {}, lambda: other.scores())
    safe("client.base_url 没被改", BASE,
         lambda: getattr(client, "base_url", "<还没定义>"))

    mock_api.stop()

    print("\n" + "=" * 50)
    print("全 [通过] 就算完成第 6 天。")
    print("=" * 50)
