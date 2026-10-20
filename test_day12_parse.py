# -*- coding: utf-8 -*-
r"""
第 12 天：pytest 测试文件
=========================

运行方式（在 doc-assistant 目录下）：
    .\dev.cmd test test_day12_parse.py

这个文件有 5 个测试要你写。每个都有 # TODO 和提示。

pytest 靠三条规则找测试：
    1. 文件名必须是 test_*.py 或 *_test.py     ← 本文件满足
    2. 函数名必须是 test_ 开头                  ← 你要写的 5 个满足
    3. 用 assert 判断，不用 check()

跑出来 5 passed 就算完成。
"""

import pytest

from day12_parse import parse_score


# ============================================================
# 测试 1：正常输入
# ============================================================

def test_normal_input():
    """普通数字能正确转换。

    要做的事：
        写 3 条 assert，分别测 "85"、"0"、"100"

    提示：
        assert parse_score("85") == 85.0

    为什么 "85" 要写成 85.0 而不是 85？
        parse_score 返回的是 float，85.0 == 85 在 Python 里是 True，
        但写 85.0 更能说明"我知道它返回浮点数"。
    """
    # TODO: 写 3 条 assert
    raise NotImplementedError('这个测试还没写，写完把这行删掉')


# ============================================================
# 测试 2：空格和小数
# ============================================================

def test_whitespace_and_decimal():
    """前后有空格、带小数点的也要能转。

    要做的事：
        写 3 条 assert：
            " 90 "  → 90.0
            "85.5"  → 85.5
            "  0  " → 0.0

    提示：
        和测试 1 一样，只是输入多了空格和小数点。
    """
    # TODO: 写 3 条 assert
    raise NotImplementedError('这个测试还没写，写完把这行删掉')


# ============================================================
# 测试 3：非数字要抛 ValueError
# ============================================================

def test_not_a_number():
    """不是数字的输入应该抛 ValueError。

    要做的事：
        用 pytest.raises 测三种情况：
            "abc"
            ""
            "   "（全是空格）

    提示：
        with pytest.raises(ValueError):
            parse_score("abc")

    为什么不用 try/except 写？
        pytest.raises 更短，而且如果函数没抛异常，
        它会自动让这个测试失败——这正是你要的。
        用 try/except 的话，你得自己写"没抛异常就 fail"，很啰嗦。
    """
    # TODO: 用 pytest.raises 写 3 段
    raise NotImplementedError('这个测试还没写，写完把这行删掉')


# ============================================================
# 测试 4：超出范围要抛 ValueError
# ============================================================

def test_out_of_range():
    """分数超过 0-100 应该抛 ValueError。

    要做的事：
        用 pytest.raises 测三种情况：
            "-1"
            "101"
            "-0.1"

    注意：
        0 和 100 是合法的（在测试 1 里已经测了）。
        这里测的是严格超出边界的值。
    """
    # TODO: 用 pytest.raises 写 3 段
    raise NotImplementedError('这个测试还没写，写完把这行删掉')


# ============================================================
# 测试 5：用 parametrize 把多组数据压成一个测试
# ============================================================

@pytest.mark.parametrize("text, expected", [
    ("85", 85.0),
    ("0", 0.0),
    ("100", 100.0),
    ("  60  ", 60.0),
    ("99.9", 99.9),
])
def test_parametrized(text, expected):
    """这 5 组数据一次跑完。

    要做的事：
        函数体只有一行：
            assert parse_score(text) == expected

    这就是 parametrize 的作用：
        写一个测试函数，pytest 会用它跑 5 次，每次填不同的参数。
        失败了 pytest 会告诉你是哪一组（比如 "text='99.9'"）。

    注意：
        这个函数的参数 text 和 expected 由装饰器提供，
        pytest 会自动填，你不用管。
    """
    # TODO: 写 1 条 assert
    raise NotImplementedError('这个测试还没写，写完把这行删掉')
