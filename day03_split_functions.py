# ============================================================
# 第 3 天任务 —— 把一坨代码拆成 3 个函数
# ============================================================
#
# 目标：学会 函数 / 参数 / 返回值
# 验收：下面 3 个函数写对，自测全部显示 [通过]
#
# 怎么用：
#   1. 先读懂第一步那坨"全部挤在一起"的代码
#   2. 把它的三段逻辑，分别搬进第二步的 3 个函数里
#   3. 运行：.\dev.cmd run day03_split_functions.py
#
# ⚠️ 不要翻 week01_start_here.py 抄。
#    先自己写，卡住 15 分钟以上再看。抄来的不算学会。
# ============================================================


# ------------------------------------------------------------
# 第一步：读懂这坨代码
# ------------------------------------------------------------
# 下面这个函数里，所有逻辑都挤在一起，而且只能算固定的那几门课。
# 想看它的输出：把文件最下面 _messy_demo() 前面的 # 去掉，再运行。

def _messy_demo():
    scores = {
        "数学": 80,
        "物理": 90,
        "英语": 100,
    }

    # 第一段：算平均分
    total = 0
    for value in scores.values():
        total = total + value
    average = total / len(scores)
    print("平均分：", average)

    # 第二段：找最高分的课
    best_name = None
    best_score = -1
    for name in scores:
        if scores[name] > best_score:
            best_score = scores[name]
            best_name = name
    print("最高分：", best_name, best_score)

    # 第三段：查某门课的分数
    target = "物理"
    found = None
    for name in scores:
        if name == target:
            found = scores[name]
    print(target, "的分数：", found)


# _messy_demo()        # ← 想看原始版本，就取消这一行的注释


# ------------------------------------------------------------
# 第二步：把上面三段逻辑，分别写成 3 个函数
# ------------------------------------------------------------
#
# 为什么要拆？
#   现在这坨代码只认写死的 scores。想算另一批成绩，得整个复制一遍。
#   拆成函数后，把 scores 当"参数"传进去，同一段代码能算任意数据。
#
# 每个函数只干一件事，用 return 把结果交出去。

def average_score(scores):
    """返回平均分。

    例子：average_score({"数学": 80, "物理": 90, "英语": 100})
          应该返回 90.0

    空字典应该返回 0（不要让它除以 0 崩溃）

    提示：
      - 用循环把每个分数加起来（或用 sum()）
      - 除以 len(scores)
    """
    # TODO
    if not scores:
        return 0
    total = 0
    for n in scores.values():
        total += n
    lens = len(scores)
    return total / lens



def best_course(scores):
    """返回分数最高的课程名。

    例子：best_course({"数学": 80, "物理": 90, "英语": 100})
          应该返回 "英语"

    空字典应该返回 None

    提示：
      - 先假设第一个是最高分
      - 或者像 _messy_demo 里那样，用一个很小的数开头
    """
    # TODO
    if not scores:
        return None
    best_name = list(scores)[0]
    best_score = -1
    for name in scores:
        if scores[name] > scores[best_name]:
            best_score = scores[name]
            best_name = name
    return best_course


def find_score(scores, name):
    """返回 name 这门课的分数。

    例子：find_score({"数学": 80, "物理": 90}, "物理") 应该返回 90
          find_score({"数学": 80, "物理": 90}, "化学") 应该返回 None

    找不到时返回 None（不是 0，也不是空字符串）

    提示：
      - 用 in 判断在不在：if name in scores
      - 或者循环找
    """
    # TODO
    if name not in scores:
        return None
    else:
        return scores[name]


# ============================================================
# 下面是自测代码，不用改。
# 运行：.\dev.cmd run day03_split_functions.py
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("第 3 天自测：函数、参数、返回值")
    print("=" * 50)

    def check(label, got, want):
        if got == want:
            print(f"  [通过] {label}")
        else:
            print(f"  [未通过] {label}")
            print(f"          你写的：{got!r}")
            print(f"          应该是：{want!r}")

    demo = {"数学": 80, "物理": 90, "英语": 100}

    print("\n1. average_score")
    check("average_score(三门)", average_score(demo), 90.0)
    check("average_score({})", average_score({}), 0)

    print("\n2. best_course")
    check("best_course(三门)", best_course(demo), "英语")
    check("best_course({})", best_course({}), None)

    print("\n3. find_score")
    check('find_score(三门, "物理")', find_score(demo, "物理"), 90)
    check('find_score(三门, "化学")', find_score(demo, "化学"), None)

    print("\n" + "=" * 50)
    print("6 个全 [通过] 就算完成今天的任务。")
    print("有 [未通过]，回到上面看 TODO 和提示。")
    print("=" * 50)
    print()
    print("⚠️ 注意：刚打开这个文件时，第 2 组和第 3 组的最后一个")
    print("   可能就显示 [通过] —— 那是假通过。因为 pass 什么都没做，")
    print("   正好返回 None，撞上了'找不到就返回 None'的期望值。")
    print("   判断有没有真写完，看 average_score 那两条：")
    print("   它们必须都 [通过]，才算 3 个函数真的都写了。")
