r"""第1周练习的测试（对应 week01_advanced.py）。

运行：
    .\dev.cmd test
或：
    .venv\Scripts\python.exe -m pytest -v

写测试的思路：每个函数问自己"什么情况下会出错"。
平均分怕空数据，查询怕查不到，读文件怕文件不存在或内容坏掉。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from week01_advanced import (
    DATA_FILE,
    average,
    load,
    query,
    save,
    top_course,
    validate,
)


# ---------- average ----------

def test_average_normal():
    assert average({"a": 80.0, "b": 90.0}) == 85.0


def test_average_empty_returns_zero():
    # 空数据不能抛 ZeroDivisionError
    assert average({}) == 0.0


def test_average_single():
    assert average({"a": 77.0}) == 77.0


# ---------- top_course ----------

def test_top_course_picks_highest():
    assert top_course({"a": 80.0, "b": 95.0, "c": 60.0}) == ("b", 95.0)


def test_top_course_empty_returns_none():
    assert top_course({}) is None


# ---------- query ----------

def test_query_found():
    assert query({"数学": 88.0}, "数学") == 88.0


def test_query_missing_returns_none():
    # 查不到应返回 None，而不是抛 KeyError
    assert query({"数学": 88.0}, "物理") is None


# ---------- validate ----------

@pytest.mark.parametrize(
    "value, expected",
    [
        (0.0, True),      # 边界
        (100.0, True),    # 边界
        (60.5, True),
        (-0.1, False),    # 越界
        (100.1, False),
    ],
)
def test_validate(value, expected):
    assert validate(value) is expected


# ---------- save / load ----------

def test_save_then_load_roundtrip(tmp_path: Path):
    """保存后读回应完全一致。tmp_path 是 pytest 提供的临时目录。"""
    target = tmp_path / "scores.json"
    original = {"高等数学": 88.5, "大学物理": 92.0}

    save(original, target)
    assert load(target) == original


def test_save_writes_valid_json(tmp_path: Path):
    target = tmp_path / "scores.json"
    save({"a": 1.0}, target)

    # 文件内容应是合法 JSON，且中文不被转义
    text = target.read_text(encoding="utf-8")
    assert json.loads(text) == {"a": 1.0}
    assert "\\u" not in text or "a" in text


def test_load_missing_file_returns_empty(tmp_path: Path):
    assert load(tmp_path / "nope.json") == {}


def test_load_corrupt_file_returns_empty(tmp_path: Path):
    """内容损坏时应返回空字典并提示，而不是让程序崩溃。"""
    bad = tmp_path / "bad.json"
    bad.write_text("{ this is not json", encoding="utf-8")
    assert load(bad) == {}


def test_load_non_dict_returns_empty(tmp_path: Path):
    """JSON 合法但不是字典（比如是列表）也要能处理。"""
    weird = tmp_path / "list.json"
    weird.write_text("[1, 2, 3]", encoding="utf-8")
    assert load(weird) == {}
