# ============================================================
# 第 7 天任务 —— 把你的函数变成一个"服务"
# ============================================================
#
# 前 6 天你写的都是"自己运行、打印结果"的程序。
# 今天开始，你要写的是"别人通过网络来调用"的程序。
#
# 这就是 FastAPI 干的事，也是你桌面那份 main.py 用的东西。
#
# 目标：学会 路由 / 路径参数 / 请求体模型 / 404 / 自动校验
# 验收：下面 4 个 TODO 写完，自测全部显示 [通过]
#
# 怎么用：
#   1. 文件最上面已经给了你一个完整示例（GET /），照着它的形状写别的
#   2. 你要写的是 4 个带 TODO 的函数
#   3. 运行：.\dev.cmd run day07_fastapi.py
#
# ⚠️ 今天**不需要**联网，**不需要** API key，**不需要**真的启动服务器。
#    自测用的是 TestClient，它在你自己的进程里假装发请求。
# ============================================================


from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

# 复用你第 3 天、第 4 天写的函数。这就是"函数可以互相调用"的好处：
# 写一次，后面每个项目都能拿去用。
from day04_files_json import average_score, best_course, load_scores, save_scores


# ============================================================
# 服务本体和数据
# ============================================================

app = FastAPI()

DATA = Path(__file__).parent / ".tmp" / "day07_scores.json"

# 启动时从文件读一次。文件不存在时 load_scores 返回 {}，不会崩。
# 注意：这是"进程启动时"读的，之后改了内存里的 SCORES，
# 文件不会自动跟着变——要你自己调 save_scores。
SCORES = load_scores(DATA)


# ============================================================
# 已经给你的完整示例：读懂这个，下面 4 个都是同一个形状
# ============================================================

@app.get("/")
def read_root():
    """访问 http://127.0.0.1:8000/ 时，返回这句话。

    @app.get("/") 这一行叫"装饰器"，作用是：
        告诉 FastAPI —— 有人用 GET 方法访问路径 "/" 时，
        就调用下面这个函数，把它的返回值当响应发回去。

    几个要点：
        - 返回值是字典，FastAPI 会自动帮你转成 JSON。
          你不用写 json.dumps，也不用设 Content-Type。
        - 函数名随便叫，不影响 URL。URL 由 @app.get("...") 里的字符串决定。
        - 这个函数**没有参数**，因为它不需要从请求里拿任何东西。
    """
    return {"message": "成绩服务已启动"}


# ============================================================
# 今天要你写的 4 个
# ============================================================

@app.get("/scores")
def list_scores():
    """返回全部成绩，比如 {"数学": 80.0, "英语": 100.0}。

    提示：
        - 直接 return SCORES 就行，FastAPI 会帮你转 JSON
        - 但要想一下：直接返回 SCORES 本身，调用方拿到的是一份拷贝，
          还是"同一个字典"？这个问题今天先不用管，明天讲。
    """
    # TODO
    return SCORES


@app.get("/scores/{course}")
def get_one_score(course: str):
    """返回某一门课的成绩，比如访问 /scores/数学 时返回
    {"course": "数学", "score": 80.0}。

    这门课不存在时，要返回 404，不能返回 200 加一个空字典。

    提示：
        - 函数参数 course 会自动从 URL 里取。你访问 /scores/数学，
          FastAPI 就自动把 course 设成 "数学"。这叫"路径参数"。
        - 判断存在：if course not in SCORES
        - 抛 404 用：
              raise HTTPException(status_code=404, detail="没有这门课")
          注意是 raise 不是 return —— 你要"中断"这个函数。
        - 存在的话，返回 {"course": course, "score": SCORES[course]}
    """
    # TODO
    if course not in SCORES:
        raise HTTPException(status_code=404,detail="没有这门课")
    else:
        return {"course":course,"score":SCORES[course]}



# 请求体模型。POST 过来的 JSON 会先被这个类"接住"再交给你。
#
# Field(ge=0, le=100) 的意思是"大于等于 0，小于等于 100"。
# 如果前端传了 150，FastAPI 会在进你的函数**之前**就返回 422，
# 你的代码根本不会执行 —— 这叫"自动校验"，一分钱不花、一行 if 不用写。
#
# 这正是你 main.py 里缺的东西：那边 message 是裸的 str，传空字符串也能进去。
class ScoreIn(BaseModel):
    course: str = Field(min_length=1, max_length=20)
    score: float = Field(ge=0, le=100)


@app.post("/scores")
def set_score(item: ScoreIn):
    """新增或修改一门课的成绩，并写进文件。

    成功时返回 {"course": ..., "score": ...}。

    提示：
        - 参数 item 的类型是 ScoreIn，FastAPI 会自动把请求体的 JSON
          变成一个 ScoreIn 对象。取值用 item.course 和 item.score。
        - 存进内存：SCORES[item.course] = item.score
        - 存进文件：save_scores(DATA, SCORES)
        - 返回 {"course": item.course, "score": item.score}
    """
    # TODO
    SCORES[item.course] = item.score
    save_scores(DATA,SCORES)
    return {"course":item.course,"score":item.score}


@app.get("/report")
def report():
    """返回一份汇总报告，比如
    {"count": 2, "average": 90.0, "best": "英语"}。

    提示：
        - 别重新写一遍求平均和找最高分！
        - 直接调用文件顶部 import 进来的 average_score(SCORES)
          和 best_course(SCORES)
        - 这就是你第 4 天写 make_report 时做过的事，一模一样
    """
    # TODO
    return {"count":len(SCORES),"average":average_score(SCORES),"best":best_course(SCORES)}


# ============================================================
# 下面是自测代码，不用改。
# 运行：.\dev.cmd run day07_fastapi.py
#
# TestClient 会直接调用你的函数，不经过网络、不占端口。
# 所以你可以一边跑自测一边开着别的服务，不会打架。
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("第 7 天自测：把函数变成服务")
    print("=" * 50)

    client = TestClient(app)

    def reset():
        """每组测试前把状态清干净，不然上一组的数据会影响下一组。"""
        SCORES.clear()
        if DATA.exists():
            DATA.unlink()

    def check(label, resp, want_status, want_json=None):
        got_status = resp.status_code
        try:
            got_json = resp.json()
        except Exception:
            got_json = resp.text

        ok = got_status == want_status
        if want_json is not None and got_json != want_json:
            ok = False

        if ok:
            print(f"  [通过] {label}")
        else:
            print(f"  [未通过] {label}")
            print(f"          状态码：{got_status}   应该是：{want_status}")
            if want_json is not None:
                print(f"          返回的：{got_json!r}")
                print(f"          应该是：{want_json!r}")

    print("\n1. GET / （这个已经给你写好了，先确认环境没问题）")
    reset()
    check("根路径返回问候语", client.get("/"), 200, {"message": "成绩服务已启动"})

    print("\n2. GET /scores：没有任何数据时")
    reset()
    check("空的时候返回 {}", client.get("/scores"), 200, {})

    print("\n3. POST /scores：加一门课")
    reset()
    check("数学 80 加进去", client.post("/scores", json={"course": "数学", "score": 80}),
          200, {"course": "数学", "score": 80.0})

    print("\n4. 加完之后，GET /scores 能查到")
    check("现在有数学了", client.get("/scores"), 200, {"数学": 80.0})

    print("\n5. 再加一门，POST 是'新增或修改'")
    check("英语 100 加进去", client.post("/scores", json={"course": "英语", "score": 100}),
          200, {"course": "英语", "score": 100.0})
    check("现在有两门", client.get("/scores"), 200, {"数学": 80.0, "英语": 100.0})
    check("数学改成 90", client.post("/scores", json={"course": "数学", "score": 90}),
          200, {"course": "数学", "score": 90.0})
    check("数学确实变了", client.get("/scores"), 200, {"数学": 90.0, "英语": 100.0})

    print("\n6. GET /scores/{course}：查单门")
    check("查数学", client.get("/scores/数学"), 200, {"course": "数学", "score": 90.0})
    check("查化学 → 404", client.get("/scores/化学"), 404)

    print("\n7. 自动校验：分数超范围要被拦住")
    check("150 分 → 422", client.post("/scores", json={"course": "体育", "score": 150}), 422)
    check("负分 → 422", client.post("/scores", json={"course": "体育", "score": -5}), 422)
    check("空课程名 → 422", client.post("/scores", json={"course": "", "score": 60}), 422)
    check("超范围的不该进到数据里", client.get("/scores"), 200, {"数学": 90.0, "英语": 100.0})

    print("\n8. GET /report：复用第 4 天的函数")
    check("汇总", client.get("/report"), 200, {"count": 2, "average": 95.0, "best": "英语"})

    print("\n9. 数据真的写进文件了吗")
    if DATA.exists():
        print(f"  [通过] 文件已生成：{DATA.name}")
        reloaded = load_scores(DATA)
        if reloaded == {"数学": 90.0, "英语": 100.0}:
            print("  [通过] 从文件读回来，内容一致")
        else:
            print("  [未通过] 从文件读回来，内容一致")
            print(f"          文件里是：{reloaded!r}")
            print(f"          应该是：  {{'数学': 90.0, '英语': 100.0}}")
    else:
        print("  [未通过] 文件已生成")
        print("          说明 set_score 里没有调用 save_scores")

    print("\n" + "=" * 50)
    print("全 [通过] 就算完成第 7 天。")
    print("=" * 50)
