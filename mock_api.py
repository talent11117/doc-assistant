# ============================================================
# mock_api.py —— 一个假的服务器，专门给第 6 天练习用
# ============================================================
#
# 为什么要有这个文件？
#
#   学"用程序跟服务器说话"需要有个服务器可以说话。
#   但真的服务器（比如 DeepSeek 的）要花钱、要 key、还可能连不上，
#   而且它返回什么你控制不了，出错时你不知道是自己写错了还是网络问题。
#
#   所以这里造一个"假的"服务器，跑在你自己电脑上：
#     - 不要钱
#     - 不用 key
#     - 断网也能用
#     - 它返回什么，我全写好了，你能对照着看
#
# ⚠️ 这个文件里的代码你现在**不用看懂**，尤其是 threading 那几行。
#    你只要知道怎么用这两个函数：
#
#       base_url = start()      # 启动服务器，拿到它的地址
#       ...
#       stop()                  # 用完关掉
#
#    然后就可以 requests.get(base_url + "/hello") 了。
#
# ============================================================

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer


# 这个类规定了"假服务器"收到不同请求时怎么回答。
# 每个 do_XXX 对应一种请求方法：do_GET 处理 GET，do_POST 处理 POST。
class _Handler(BaseHTTPRequestHandler):

    def _send(self, status, obj):
        """把 obj 变成 JSON，连同状态码一起发回去。"""
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        # self.path 是请求的路径，比如 "/hello" 或 "/slow?seconds=3"
        path = self.path.split("?")[0]

        if path == "/hello":
            self._send(200, {"message": "你好，我是假服务器"})

        elif path == "/scores":
            self._send(200, {"数学": 80, "物理": 90, "英语": 100})

        elif path.startswith("/slow"):
            # 故意慢 3 秒，用来演示 timeout
            time.sleep(3)
            self._send(200, {"message": "我慢吞吞地来了"})

        elif path == "/boom":
            # 故意返回 500（服务器内部错误）
            self._send(500, {"error": "服务器炸了"})

        else:
            # 其它路径一律 404（找不到）
            self._send(404, {"error": "没有这个路径"})

    def do_POST(self):
        # 读请求体：先看有多长，再按长度读出来
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8")

        try:
            data = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            self._send(400, {"error": "你发的不是合法 JSON"})
            return

        if self.path == "/echo":
            # 原样送回去，外加一个字段，证明服务器确实收到了
            self._send(200, {"received": data, "ok": True})
        else:
            self._send(404, {"error": "没有这个路径"})

    # 默认每来一个请求就往屏幕上打一行日志，太吵，关掉
    def log_message(self, fmt, *args):
        pass


class _QuietServer(HTTPServer):
    """普通的 HTTPServer，只是不把"客户端提前断开"当成错误打出来。

    练 timeout 的时候，客户端 1 秒就放弃了，服务器还在慢慢回话，
    这时会冒出 ConnectionAbortedError 的红色报错 —— 那不是你的 bug，
    只是客户端走了。这里把它静音，免得你误以为是自己写错了。
    """

    def handle_error(self, request, client_address):
        import sys
        exc = sys.exc_info()[1]
        if isinstance(exc, (ConnectionAbortedError, ConnectionResetError, BrokenPipeError)):
            return
        super().handle_error(request, client_address)


_server = None
_thread = None


def start(port=0):
    """启动假服务器，返回它的地址（像 "http://127.0.0.1:54321"）。

    port=0 的意思是"随便找个空闲端口"，这样不会跟别的程序抢。
    """
    global _server, _thread

    if _server is not None:
        return _base_url()

    _server = _QuietServer(("127.0.0.1", port), _Handler)
    _thread = threading.Thread(target=_server.serve_forever, daemon=True)
    _thread.start()
    return _base_url()


def _base_url():
    host, actual_port = _server.server_address
    return f"http://{host}:{actual_port}"


def stop():
    """关掉假服务器。"""
    global _server, _thread
    if _server is not None:
        _server.shutdown()
        _server.server_close()
        _server = None
        _thread = None


if __name__ == "__main__":
    # 直接运行这个文件时，把服务器开着，方便你手动试
    import requests

    base = start()
    print("假服务器已启动：", base)
    print("试试这些：")
    for p in ["/hello", "/scores", "/boom", "/没有这个"]:
        r = requests.get(base + p, timeout=5)
        print(f"  GET {p:12s} → {r.status_code}  {r.json()}")
    print()
    print("按 Ctrl+C 关掉。")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop()
        print("已关闭。")
