# ============================================================
# 第 6 天 先读这个 —— 用程序跟服务器说话
# ============================================================
#
# 怎么用：
#   1. 从头往下读，一次读一小节
#   2. 每一节都运行看结果
#   3. 运行：.\dev.cmd run day06_api_intro.py
#
# 读完之后，再去写 day06_api.py 里的作业。
#
# 为什么今天学这个？
#   你抄的 main.py 里，最核心的一行是：
#       resp = requests.post(url, headers=headers, json=data)
#   这一行就是"跟服务器说话"。
#   今天把这个动作彻底搞懂，之后调 DeepSeek、Qwen 的接口都是同一件事。
#
#   Agent 开发 90% 的工作就是：调接口、拿结果、处理出错。
#   所以这一天不是"顺带学一下"，是主线的核心。
# ============================================================

import requests
import mock_api


# 先启动假服务器。它会返回一个地址，像 http://127.0.0.1:54321
BASE = mock_api.start()
print("假服务器地址：", BASE)
print()


# ------------------------------------------------------------
# 第 1 节：一次"说话"由四部分组成
# ------------------------------------------------------------
#
# 你在浏览器里输入网址、按回车，背后发生的事叫「HTTP 请求」。
# 一个请求有四个部分：
#
#   1. 方法（method）  —— 想干什么
#        GET  = 我要拿东西（读）
#        POST = 我要送东西给你（写）
#
#   2. 地址（url）     —— 找谁
#        http://127.0.0.1:54321/hello
#        └─协议─┘ └──主机──┘└端口┘└路径┘
#
#   3. 请求头（headers）—— 附带的说明，比如"我是谁""我接受什么格式"
#
#   4. 请求体（body）  —— POST 时送过去的内容（GET 一般没有）
#
# 服务器处理完，会回一个「响应」，也有三部分：
#
#   1. 状态码（status code）—— 结果怎么样
#        200 = 成功
#        404 = 你要的东西不存在
#        500 = 服务器自己出错了
#
#   2. 响应头（headers）
#   3. 响应体（body）—— 真正的内容，通常是 JSON

print("第1节：一次请求的四个部分")


# ------------------------------------------------------------
# 第 2 节：最简单的 GET
# ------------------------------------------------------------

r = requests.get(BASE + "/hello", timeout=5)

print("第2节：")
print("  状态码：", r.status_code)      # 200
print("  原始文本：", r.text)           # {"message": "..."}
print("  变成字典：", r.json())         # {'message': '...'}

# r 是"响应对象"，它身上挂着好几样东西：
#
#   r.status_code   200 这样的数字
#   r.text          服务器发回来的原始字符串
#   r.json()        把 r.text 当成 JSON 解析成 Python 字典
#
# ⚠️ r.json() 后面有括号，因为它是个方法（要"执行"一下）；
#    r.text 后面没括号，因为它是个属性（已经在那了）。
#
# 这个区别和你昨天学的 self.name（属性）vs self.bark()（方法）是同一个道理。


# ------------------------------------------------------------
# 第 3 节：拿到数据之后，就是普通的字典操作
# ------------------------------------------------------------

r = requests.get(BASE + "/scores", timeout=5)
scores = r.json()

print("第3节：")
print("  拿到的字典：", scores)
print("  数学的分数：", scores["数学"])
print("  一共几门：", len(scores))

# 看，到这里它就是个普通字典了。
# 你第 3 天写的 average_score(scores) 可以直接用：
#
#     from day03_split_functions import average_score
#     print(average_score(scores))
#
# 网络请求只是"把数据弄进来"，弄进来之后还是你熟悉的那套东西。
# 这是今天最该有的心态：不用怕，只是多了一步"取数据"。


# ------------------------------------------------------------
# 第 4 节：状态码 —— 服务器在告诉你结果
# ------------------------------------------------------------

print("第4节：不同状态码")

for path in ["/hello", "/没有这个", "/boom"]:
    r = requests.get(BASE + path, timeout=5)
    print(f"  {path:10s} → {r.status_code}  {r.json()}")

# 输出：
#   /hello     → 200  {'message': '你好，我是假服务器'}
#   /没有这个   → 404  {'error': '没有这个路径'}
#   /boom      → 500  {'error': '服务器炸了'}
#
# 关键点：**404 和 500 的时候，requests 不会报错！**
# 它照样把响应交给你，只是 status_code 不是 200。
#
# 这是新手最常踩的坑：
#
#     r = requests.get(url)
#     data = r.json()["message"]     # ← 404 时这里会 KeyError 崩掉
#
# 你以为代码是对的，其实服务器根本没给你 message，
# 它给的是 {"error": "没有这个路径"}。
#
# 所以拿到响应后，第一件事是看状态码。


# ------------------------------------------------------------
# 第 5 节：raise_for_status() —— 让出错变成异常
# ------------------------------------------------------------
#
# 与其每次手动 if r.status_code != 200，requests 提供了更省事的写法：

r = requests.get(BASE + "/boom", timeout=5)
try:
    r.raise_for_status()          # 不是 2xx 就抛异常
    print("第5节：成功")
except requests.exceptions.HTTPError as e:
    print("第5节：抓到异常 →", e)

# raise_for_status() 的意思是：
#   "如果状态码表示失败，就抛个异常出来，别让我继续往下走"
#
# 配合 try/except（你第 4 天学的），就变成：
#
#     try:
#         r = requests.get(url, timeout=5)
#         r.raise_for_status()
#         return r.json()
#     except requests.exceptions.HTTPError:
#         return None            # 服务器说不行，那就当没拿到
#
# ⚠️ 注意 except 后面写的是 requests.exceptions.HTTPError，
#    不是你第 4 天用的 FileNotFoundError。
#    异常名字必须精确匹配 —— 这条规则没变。


# ------------------------------------------------------------
# 第 6 节：timeout —— 为什么这个参数不能省
# ------------------------------------------------------------
#
# 你抄的 main.py 里这一行是错的：
#
#     resp = requests.post(url, headers=headers, json=data)
#                                        ↑ 没有 timeout
#
# 没有 timeout 会怎样？
#   如果服务器一直不回话（网络卡住、对方挂了、防火墙吞了包），
#   requests 会**一直等下去**，你的程序就永远卡在那里，不报错、不退出。
#
#   这叫"挂死"。线上服务里这是最严重的问题之一 ——
#   一个卡住的请求会占着一个线程，卡多了整个服务就废了。
#
# 加上 timeout 之后：超过这个秒数还没回，就抛 Timeout 异常。

print("第6节：timeout")

r = requests.get(BASE + "/slow", timeout=10)
print("  等 3 秒，timeout=10 →", r.status_code, r.json())

try:
    requests.get(BASE + "/slow", timeout=1)
    print("  timeout=1 → 居然成功了？不应该")
except requests.exceptions.Timeout:
    print("  timeout=1 → 超时了，抛 Timeout 异常 ✅")

# 同一个接口：
#   timeout=10 → 等到了，200
#   timeout=1  → 1 秒还没回，抛异常
#
# ⚠️ timeout 的单位是**秒**。
# ⚠️ 调大模型接口时，timeout 要设得比一般接口大
#    （模型生成一段话可能要几十秒），常见是 30~120 秒。
# ⚠️ 但**必须**设。哪怕设 300 也比不设强。


# ------------------------------------------------------------
# 第 7 节：POST —— 把数据送过去
# ------------------------------------------------------------
#
# GET 是把参数拼在地址里（?a=1&b=2），POST 是把数据放在"请求体"里。
#
# requests 最方便的用法是 json= 参数：
#   它会自动做两件事：
#     1. 把字典变成 JSON 字符串
#     2. 自动加上请求头 Content-Type: application/json

payload = {"name": "张三", "age": 20}
r = requests.post(BASE + "/echo", json=payload, timeout=5)

print("第7节：")
print("  发出去：", payload)
print("  状态码：", r.status_code)
print("  收回来：", r.json())

# 输出里 received 就是服务器收到的原样。
# 你抄的 main.py 里这一行做的就是这件事：
#
#     resp = requests.post(url, headers=headers, json=data)
#
# data 里装的是 {"model": "deepseek-flash", "messages": [...]}
# 服务器（DeepSeek）收到后，把回答放在响应体里发回来。
#
# 注：老教程里写的是 "deepseek-chat"，这个模型名已经下线了，
#     现在只能用 "deepseek-flash" 或 "deepseek-v4-pro"。


# ------------------------------------------------------------
# 第 8 节：把地址存进对象里（接上昨天的类）
# ------------------------------------------------------------
#
# 上面每次调用都要写 BASE + "/hello"、BASE + "/scores"……
# 地址是重复的，这正好是昨天学的类能解决的：把地址存到对象身上。

class ScoreClient:
    def __init__(self, base_url):
        self.base_url = base_url        # 地址存在自己身上

    def hello(self):
        r = requests.get(self.base_url + "/hello", timeout=5)
        return r.json()["message"]

    def scores(self):
        r = requests.get(self.base_url + "/scores", timeout=5)
        return r.json()


client = ScoreClient(BASE)
print("第8节：")
print("  client.hello()  →", client.hello())
print("  client.scores() →", client.scores())

# 对比一下：
#   没有类：requests.get(BASE + "/hello")     每次都要带 BASE
#   有了类：client.hello()                    地址在对象身上，不用管
#
# 这跟你昨天写 ScoreBook 是同一个思路：
#   昨天把 scores 存到 self 上，今天把 base_url 存到 self 上。


# ------------------------------------------------------------
# 第 9 节：小结
# ------------------------------------------------------------
#
# 今天你只要记住这 6 句：
#
# 1. GET 拿东西，POST 送东西
# 2. r.status_code 看结果，200 才是成功
# 3. r.json() 把响应变成字典（记得加括号）
# 4. 404 / 500 时 requests 不报错，要自己查状态码
# 5. timeout 必须写，不写会挂死
# 6. 地址存进 self，就是昨天学的类

print()
print("第9节：小结")
print("接下来：写 day06_api.py 里的作业")

mock_api.stop()
