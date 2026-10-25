# ============================================================
# 练习 01 —— 填空版
# ============================================================
#
# 怎么用：
#   1. 每个函数里都有  # TODO  标记，把 TODO 换成真正的代码
#   2. 填完一个就运行测试看对不对：
#          .\dev.cmd test
#   3. 全部通过（绿色）就说明你写对了
#
# 遇到不会的，查这两个文件：
#   - week01_start_here.py        （从零开始的基础）
#   - 代码解释_看不懂的地方.md      （那些天书写法）
#
# 重要：不要一次填完 6 个。填一个、测一个、过了再下一个。
# ============================================================


def add(a, b):
    """返回 a 加 b 的结果。

    例子：add(3, 5) 应该返回 8
    """
    # TODO: 把下面这行删掉，改成 return a + b
    return a + b


def count_items(items):
    """返回列表里有几个元素。

    例子：count_items([1, 2, 3]) 应该返回 3
    提示：用 len()
    """
    # TODO
    if not items:
        return 0
    lens = len(items)
    return lens


def find_max(numbers):
    """找出列表里最大的数，不许用 max()。

    例子：find_max([3, 9, 2]) 应该返回 9

    思路（照着写）：
        best = numbers[0]        # 先假设第一个最大
        for n in numbers:        # 挨个看
            if n > best:         # 如果发现更大的
                best = n         # 就换成它
        return best
    """
    # TODO
    best = numbers[0]
    for n in numbers:
        if n > best:
            best = n
    return best


def count_above(numbers, threshold):
    """数一数有多少个数大于 threshold。

    例子：count_above([60, 85, 90, 45], 80) 应该返回 2
          （85 和 90 大于 80）

    思路：
        count = 0
        for n in numbers:
            if n > threshold:
                count = count + 1
        return count
    """
    # TODO
    count = 0
    for n in numbers:
        if n > threshold:
            count += 1
    return count


def make_dict(names, scores):
    """把两个列表合成一个字典。

    例子：make_dict(["数学", "物理"], [88, 92])
          应该返回 {"数学": 88, "物理": 92}

    思路：
        result = {}
        for i in range(len(names)):     # i 是 0, 1, 2...
            result[names[i]] = scores[i]
        return result

    提示：range(3) 会给出 0, 1, 2
    """
    # TODO
    result = {}
    for i in range(len(names)):
        result[names[i]] = scores[i]
    return result


def safe_divide(a, b):
    """返回 a 除以 b。如果 b 是 0，返回 None（不要让它崩溃）。

    例子：safe_divide(10, 2) 应该返回 5.0
          safe_divide(10, 0) 应该返回 None

    提示：用 try / except ZeroDivisionError
          参考 week01_start_here.py 第 7 节
    """
    # TODO
    try:
        return a / b
    except ZeroDivisionError:
        return None


# ============================================================
# 下面是自测代码，不用改
# 直接运行就能看到你写对没有：
#     .\dev.cmd run practice01.py
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("填空练习 01 自测")
    print("=" * 50)

    def check(label, got, want):
        if got == want:
            print(f"  [通过] {label}")
        else:
            print(f"  [未通过] {label}")
            print(f"          你写的：{got!r}")
            print(f"          应该是：{want!r}")

    print("\n1. add")
    check("add(3, 5)", add(3, 5), 8)

    print("\n2. count_items")
    check("count_items([1,2,3])", count_items([1, 2, 3]), 3)
    check("count_items([])", count_items([]), 0)

    print("\n3. find_max")
    check("find_max([3,9,2])", find_max([3, 9, 2]), 9)
    check("find_max([100])", find_max([100]), 100)

    print("\n4. count_above")
    check("count_above([60,85,90,45], 80)", count_above([60, 85, 90, 45], 80), 2)
    check("count_above([1,2], 99)", count_above([1, 2], 99), 0)

    print("\n5. make_dict")
    check(
        'make_dict(["数学","物理"], [88,92])',
        make_dict(["数学", "物理"], [88, 92]),
        {"数学": 88, "物理": 92},
    )

    print("\n6. safe_divide")
    check("safe_divide(10, 2)", safe_divide(10, 2), 5.0)
    check("safe_divide(10, 0)", safe_divide(10, 0), None)

    print("\n" + "=" * 50)
    print("全部显示 [通过] 就说明你写完了。")
    print("如果有 [未通过]，回到上面看 TODO。")
    print("=" * 50)
