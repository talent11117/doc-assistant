# ============================================================
# 第 4 天任务 —— 把数据存下来，再读回来
# ============================================================
#
# 目标：学会 文件读写 / JSON / 文件路径 / 文件不存在的处理
# 验收：下面 3 个函数写对，自测全部显示 [通过]
#
# 怎么用：
#   1. 上面两个函数（average_score / best_course）是第 3 天你写好的，
#      直接拿来用，不用改。
#   2. 你要写的是下面 3 个带 TODO 的函数。
#   3. 运行：.\dev.cmd run day04_files_json.py
#
# ⚠️ 先自己写，卡住 15 分钟以上再看 week01_start_here.py 第 8 节。
# ============================================================

from pathlib import Path
import json


# ============================================================
# 这两个是第 3 天的成果，已经填好了，直接调用
# ============================================================

def average_score(scores):
    """返回平均分；空字典返回 0。"""
    if not scores:
        return 0
    total = 0
    for n in scores.values():
        total += n
    return total / len(scores)


def best_course(scores):
    """返回分数最高的课程名；空字典返回 None。"""
    if not scores:
        return None
    best_name = None
    best_score = -1
    for name in scores:
        if scores[name] > best_score:
            best_score = scores[name]
            best_name = name
    return best_name


# ============================================================
# 今天要你写的 3 个函数
# ============================================================

def load_scores(path):
    """读一个 JSON 文件，返回里面的字典。

    例子：文件里是 {"数学": 80}
          load_scores(那个文件的路径) 应该返回 {"数学": 80}

    文件不存在时，返回 {}（空字典），不要崩溃。

    提示：
      - 用 open(路径, "r", encoding="utf-8") 打开文件
      - 用 json.load(f) 把文件内容变成字典
      - 文件不存在会抛 FileNotFoundError，用 try/except 接住
      - 传进来的 path 可能是字符串，用 Path(path) 转一下更保险
      - 参考 week01_start_here.py 第 8 节
    """
    # TODO
    try:
        Path_obj = Path(path)
        with open(Path_obj,"r",encoding = "utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}




def save_scores(path, scores):
    """把字典 scores 写进 path 这个文件，存成 JSON。

    例子：save_scores("a.json", {"数学": 80})
          之后 a.json 里就有 {"数学": 80}

    两个要求（自测会检查）：
      1. 中文不要被转义成 \u6570\u5b66 这种乱码，要能直接看懂
      2. 缩进 2 个空格，方便人看

    提示：
      - open(路径, "w", encoding="utf-8") 是写模式，"w" 会把原内容覆盖掉
      - json.dump(数据, f, ensure_ascii=False, indent=2)
      - ensure_ascii=False 就是"别转义中文"的意思
      - 这个函数不需要 return 什么
    """
    # TODO
    floder = Path(path)
    with open(floder,"w",encoding = "utf-8") as f:
        json.dump(scores,f,ensure_ascii=False,indent = 2)



def make_report(scores):
    """把成绩字典变成一份"报告"字典。

    例子：make_report({"数学": 80, "物理": 90, "英语": 100})
          应该返回 {"count": 3, "average": 90.0, "best": "英语"}

    空字典应该返回 {"count": 0, "average": 0, "best": None}

    提示：
      - 别重新写一遍求平均和找最高分！
      - 直接调用上面已经给你的 average_score() 和 best_course()
      - 这个函数体现的正是"函数可以互相调用"：
        你昨天写的两个函数，今天换个场景直接复用
      - count 用 len(scores)
    """
    # TODO
    if not scores:
        return {"count": 0, "average": 0, "best": None}

    # lists = {}
    # list1 = ['count','average','best']
    # list2 = [len(scores),average_score(scores),best_course(scores)]
    # for i in range(3):
    #     lists[list1[i]] = list2[i]
    return {"count":len(scores),"average":average_score(scores),"best":best_course(scores)}






# ============================================================
# 下面是自测代码，不用改。
# 运行：.\dev.cmd run day04_files_json.py
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("第 4 天自测：文件、JSON、路径")
    print("=" * 50)

    def check(label, got, want):
        if got == want:
            print(f"  [通过] {label}")
        else:
            print(f"  [未通过] {label}")
            print(f"          你写的：{got!r}")
            print(f"          应该是：{want!r}")

    # 在项目里建一个 .tmp 文件夹放测试文件（这个文件夹已被 git 忽略）
    tmp = Path(__file__).parent / ".tmp"
    tmp.mkdir(exist_ok=True)
    test_file = tmp / "day04_test.json"

    # 先删掉上次可能留下的测试文件，保证每次从干净状态开始
    if test_file.exists():
        test_file.unlink()

    demo = {"数学": 80, "物理": 90, "英语": 100}

    print("\n1. load_scores：文件不存在时要返回 {}")
    check("load_scores(不存在的文件)", load_scores(tmp / "没有这个文件.json"), {})

    print("\n2. save_scores：能不能真的写出来")
    save_scores(test_file, demo)
    check("写完文件确实存在了", test_file.exists(), True)

    if test_file.exists():
        raw = test_file.read_text(encoding="utf-8")
        check("中文没被转义成乱码", "数学" in raw, True)
        check("有缩进（不是挤成一行）", "\n" in raw.strip(), True)
    else:
        print("  [跳过] 文件没写出来，下面两条无法检查")

    print("\n3. load_scores：能不能读回来")
    check("读回来的内容和存进去的一样", load_scores(test_file), demo)

    print("\n4. make_report：复用昨天的函数")
    check("make_report(三门)", make_report(demo),
          {"count": 3, "average": 90.0, "best": "英语"})
    check("make_report({})", make_report({}),
          {"count": 0, "average": 0, "best": None})

    print("\n" + "=" * 50)
    print("全 [通过] 就算完成第 4 天。")
    print("=" * 50)
