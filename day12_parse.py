# -*- coding: utf-8 -*-
r"""
第 12 天：pytest
================

运行方式（在 doc-assistant 目录下）：
    .\dev.cmd test test_day12_parse.py

这个文件只有一个函数要你写：parse_score。
测试在 test_day12_parse.py 里，那个文件也有 TODO。

为什么要专门学 pytest？
    你这五天一直在用 check("标签", 你算的, 应该的)。
    它能用，但有两个毛病：
      1. 一个函数报错，后面所有测试都跑不到
         （第 4 天你就遇到过：load_scores 一崩，6 条全没跑）
      2. 输出是一堆自定义的中文，别人看不懂

    pytest 解决这两个问题：一条失败不影响其它条，
    输出是标准的 passed / failed，全世界的 Python 项目都用它。
"""


def parse_score(text):
    """把用户输入的字符串转成 0-100 的分数。

    参数：
        text  用户输入的字符串，比如 "85"、" 90.5 "、"abc"

    返回：
        float 类型的分数

    什么时候抛 ValueError：
        - 空字符串或全是空格        "   "
        - 不是数字                  "abc"、"8O"（字母 O 不是数字 0）
        - 超出 0-100 范围           "-1"、"101"
        - 传进来的不是字符串         None、85

    规则细节：
        - 前后的空格要去掉          " 85 " → 85.0
        - 整数和小数都要支持        "85" → 85.0，"85.5" → 85.5
        - 边界值算合法              0 和 100 都要通过

    要做的事：
        1. 如果不是字符串，抛 ValueError
        2. 去掉前后空格（.strip()）
        3. 如果去掉后是空的，抛 ValueError
        4. 转成 float（用 try/except 包住 float()，
           因为 "abc" 会让 float() 抛 ValueError）
        5. 检查范围 0 <= score <= 100，不满足就抛 ValueError
        6. 返回 score

    提示：
        isinstance(text, str)         判断是不是字符串
        text.strip()                  去掉前后空格
        float(text)                   转数字，失败会抛 ValueError
        raise ValueError("...")       主动抛错

    注意：
        抛错时写什么消息随你，测试只检查"有没有抛 ValueError"，
        不检查消息内容。但写清楚一点，将来你自己看得懂。
    """
    # TODO: 在这里写代码
    pass


# ============================================================
# 快速自检（不是 pytest，只是让你写完能马上看一眼）
# ============================================================
# 运行 .\dev.cmd run day12_parse.py 会执行这一段。

if __name__ == "__main__":
    print("=" * 60)
    print("快速自检（正式的测试在 test_day12_parse.py）")
    print("=" * 60)

    cases = [
        ("85", 85.0),
        ("85.5", 85.5),
        (" 90 ", 90.0),
        ("0", 0.0),
        ("100", 100.0),
    ]
    for text, want in cases:
        try:
            got = parse_score(text)
        except Exception as e:
            print(f"  [报错] parse_score({text!r})  {type(e).__name__}: {e}")
            continue
        if got == want:
            print(f"  [通过] parse_score({text!r}) == {want}")
        else:
            print(f"  [未通过] parse_score({text!r})")
            print(f"      你写的：{got!r}")
            print(f"      应该是：{want!r}")

    bad_cases = ["", "   ", "abc", "-1", "101", None]
    for text in bad_cases:
        try:
            got = parse_score(text)
            print(f"  [未通过] parse_score({text!r}) 应该抛 ValueError，但返回了 {got!r}")
        except ValueError:
            print(f"  [通过] parse_score({text!r}) 正确抛出 ValueError")
        except Exception as e:
            print(f"  [未通过] parse_score({text!r}) 抛了 {type(e).__name__}，应该抛 ValueError")

    print("=" * 60)
    print("全 [通过] 之后，去跑 .\\dev.cmd test test_day12_parse.py")
    print("=" * 60)
