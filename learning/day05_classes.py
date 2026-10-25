# ============================================================
# 第 5 天任务 —— 把函数和数据装进一个盒子里
# ============================================================
#
# 目标：学会 类（class）/ 对象 / self / 方法
# 验收：下面 ScoreBook 类的 4 个方法写对，自测全部显示 [通过]
#
# 怎么用：
#   1. 先读懂第一步那个 Dog 类（每一行都写了注释）
#   2. 再自己写第二步的 ScoreBook 类
#   3. 运行：.\dev.cmd run day05_classes.py
#
# ⚠️ 先自己写，卡住 15 分钟以上再看 week01_start_here.py 第 9 节。
#
# 为什么今天学类？
#   前 4 天你写的都是"函数"：average_score(scores)、save_scores(path, scores)。
#   每写一个函数，都得把 scores 当参数传进去一遍。
#
#   类就是解决这个的：把数据（scores）和操作数据的函数（add/average/best）
#   打包在一起。之后你写 book.add("数学", 80) 就行，不用再传 scores。
#
#   这不是为了炫技。你抄的 main.py 里已经有：
#       app = FastAPI()              ← app 是一个对象
#       class ChatRequest(BaseModel) ← 你在定义一个类
#   看不懂 self，就看不懂 FastAPI。今天补上这一课。
# ============================================================

from pathlib import Path
import json


# ============================================================
# 第一步：读懂这个类（不用改，读懂就行）
# ============================================================
#
# 一个"类"是模板，"对象"是按模板造出来的东西。
#   class Dog:          ← 模板：狗
#   d = Dog("旺财", 3)  ← 对象：一只具体的狗
#
# 你可以造很多只狗，每只名字年龄都不一样，但都按同一个模板。

class Dog:
    # __init__ 是"造对象时自动执行的函数"，用来初始化。
    # 注意是 init 前后各两个下划线，一共 4 个。
    def __init__(self, name, age):
        # self 就是"正在被造的那只狗本身"。
        # self.name = name 的意思是：把这只狗的名字，记在它自己身上。
        self.name = name
        self.age = age

    # 类里面的函数叫"方法"，第一个参数永远是 self。
    # 调用时不用手动传 self，Python 会自动把对象塞进去。
    def bark(self):
        # 用 self.name 就能取到"这只狗自己"的名字
        return self.name + "：汪汪！"

    def birthday(self):
        # 改自己身上的属性
        self.age = self.age + 1


# 你可以把下面几行的 # 去掉，运行看看效果
# d1 = Dog("旺财", 3)
# d2 = Dog("小黑", 5)
# print(d1.bark())       # 旺财：汪汪！
# print(d2.bark())       # 小黑：汪汪！
# print(d1.age)          # 3
# d1.birthday()
# print(d1.age)          # 4
# print(d2.age)          # 5   ← d1 过生日，d2 不受影响！


# 上面最后两行是今天的核心：
#   d1.age 变成 4，d2.age 还是 5。
#   因为 self.name / self.age 是"这只狗自己的"，不是"所有狗共用的"。
#
# 反面例子（❌ 别这样写）：
#     class Dog:
#         age = 0              # ← 写在方法外面，这是"所有狗共用的"
#         def __init__(self, name):
#             self.name = name
#
# 这样 d1.age 和 d2.age 会互相影响，一只狗过生日所有狗都老一岁。


# ============================================================
# 第二步：你来写这个类
# ============================================================

class ScoreBook:
    """一本成绩本：存一个人的各科成绩。

    用法：
        book = ScoreBook("张三")
        book.add("数学", 80)
        book.add("物理", 90)
        print(book.average())    # 85.0
        print(book.best())       # 物理
    """

    def __init__(self, name):
        """创建成绩本时要做的准备。

        要做两件事：
          1. 把传进来的 name 存到 self.name（这本成绩本是谁的）
          2. 把 self.scores 设成一个空字典 {}

        提示：
          - 照抄上面 Dog 的 __init__ 的写法
          - 第 2 条直接写 self.scores = {}
          - ⚠️ 千万**不要**把 scores 写在 __init__ 外面！
            那样所有成绩本会共用同一个字典（见第一步最后的反面例子）
        """
        # TODO
        self.name = name
        self.scores = {}

    def add(self, course, score):
        """加一门课的成绩。

        例子：book.add("数学", 80)
              之后 book.scores 里就有 "数学": 80

        注意：
          - 不用 return 任何东西
          - 是"往字典里加一项"，不是"换一个新字典"
          - 想清楚：self.scores[course] = score 对，还是 self.scores = {...} 对？

        提示：
          - 给字典加一项：d[键] = 值
        """
        # TODO
        self.scores[course] = score



    def average(self):
        """返回平均分；一本成绩都没有时返回 0。

        这就是你第 3 天写的 average_score，只是 scores 换成 self.scores。

        提示：
          - 先把 self.scores 当成第 3 天的 scores 来写
          - 空的时候要 return 0，别除以 0
        """
        # TODO
        if not self.scores:
            return 0
        length = len(self.scores)
        total = 0
        for n in self.scores:
            total += self.scores[n]
        return total / length


    def best(self):
        """返回分数最高的课程名；一本成绩都没有时返回 None。

        这就是你第 3 天写的 best_course，scores 换成 self.scores。
        """
        # TODO
        if not self.scores:
            return None
        best_name = None
        best_score = -1
        for name in self.scores:
            if self.scores[name] > best_score:
                best_score = self.scores[name]
                best_name = name
        return best_name

    def save(self, path):
        """把 self.scores 存进 path 这个文件（JSON）。

        这就是你第 4 天写的 save_scores，只是不用再传 scores 了 ——
        它从 self.scores 拿。

        两个要求（自测会检查）：
          1. 中文不要转义成 \u6570\u5b66
          2. 缩进 2 个空格

        提示：
          - json.dump(self.scores, f, ensure_ascii=False, indent=2)
        """
        # TODO
        folder = Path(path)

        with open(folder,"w",encoding="utf-8") as f:
            json.dump(self.scores,f,ensure_ascii=False,indent=2)


# ============================================================
# 下面是自测代码，不用改。
# 运行：.\dev.cmd run day05_classes.py
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("第 5 天自测：类与对象")
    print("=" * 50)

    # safe 的作用：你写的代码报错时，只把错误显示在这一条旁边，
    # 不再让整个程序崩掉，这样你能一次看到所有没通过的地方。
    # 里面的 lambda 先照抄，以后会学。
    def safe(label, want, fn):
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

    # getattr(obj, "name", 默认值)：取 obj.name，没有就返回默认值。
    # 这样即使你还没写 self.name，也只是显示 [未通过]，不会崩溃。
    def attr(obj, name):
        return getattr(obj, name, "<还没定义>")

    print("\n1. 创建对象：__init__ 有没有把东西存好")
    book = ScoreBook("张三")
    safe("book.name", "张三", lambda: attr(book, "name"))
    safe("book.scores 一开始是空的", {}, lambda: attr(book, "scores"))

    print("\n2. add：往里加成绩")
    book.add("数学", 80)
    book.add("物理", 90)
    book.add("英语", 100)
    safe("加了三门课", {"数学": 80, "物理": 90, "英语": 100},
         lambda: attr(book, "scores"))

    print("\n3. average / best")
    safe("平均分", 90.0, lambda: book.average())
    safe("最高分的课", "英语", lambda: book.best())

    print("\n4. 空成绩本不能崩")
    empty = ScoreBook("李四")
    safe("空本的平均分", 0, lambda: empty.average())
    safe("空本的最高分", None, lambda: empty.best())

    print("\n5. 两个对象互不干扰（今天最重要的一条）")
    safe("张三的本里还是那 3 门", {"数学": 80, "物理": 90, "英语": 100},
         lambda: attr(book, "scores"))
    safe("李四的本里还是空的", {}, lambda: attr(empty, "scores"))

    print("\n6. save：存成 JSON 文件")
    tmp = Path(__file__).parent / ".tmp"
    tmp.mkdir(exist_ok=True)
    out = tmp / "day05_test.json"
    if out.exists():
        out.unlink()

    try:
        book.save(out)
    except Exception as e:
        print(f"  [报错] book.save(out)")
        print(f"          {type(e).__name__}: {e}")

    safe("文件确实写出来了", True, lambda: out.exists())

    if out.exists():
        raw = out.read_text(encoding="utf-8")
        safe("中文没被转义成乱码", True, lambda: "数学" in raw)
        safe("有缩进（不是挤成一行）", True, lambda: "\n" in raw.strip())
    else:
        print("  [跳过] 文件没写出来，下面两条无法检查")

    print("\n" + "=" * 50)
    print("全 [通过] 就算完成第 5 天。")
    print("=" * 50)
