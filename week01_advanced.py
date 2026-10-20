r"""第1周自测：把成绩数据做统计（进阶版）。

如果你看不太懂这个文件，请先读 week01_start_here.py，
并参考 代码解释_看不懂的地方.md。

不依赖任何第三方库。

要求：
    1. 输入一组 (课程名, 成绩) 数据
    2. 算出平均分、最高分课程
    3. 按课程名查询成绩
    4. 把结果写入 JSON 文件并能读回来
    5. 空数据、成绩非法、课程不存在时给出清楚提示，不要崩溃

运行：
    .\dev.cmd run week01_advanced.py
"""

from __future__ import annotations

import json
from pathlib import Path

# 一个模块级的常量：数据存哪里
DATA_FILE = Path(__file__).parent / "scores.json"


def average(scores: dict[str, float]) -> float:
    """算平均分。空字典返回 0.0，避免 ZeroDivisionError。"""
    if not scores:
        return 0.0
    return sum(scores.values()) / len(scores)


def top_course(scores: dict[str, float]) -> tuple[str, float] | None:
    """返回分数最高的课程和分数；空字典返回 None。

    max() 的 key 参数是"按什么排序"：这里按 value（分数）。
    """
    if not scores:
        return None
    name = max(scores, key=scores.__getitem__)
    return name, scores[name]


def query(scores: dict[str, float], course: str) -> float | None:
    """按课程名查询。查不到返回 None，而不是抛异常。

    用 .get() 而不是 scores[course]，后者会抛 KeyError。
    """
    return scores.get(course)


def save(scores: dict[str, float], path: Path = DATA_FILE) -> None:
    """写入 JSON。ensure_ascii=False 让中文正常显示，indent=2 便于阅读。"""
    path.write_text(
        json.dumps(scores, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load(path: Path = DATA_FILE) -> dict[str, float]:
    """读回 JSON。文件不存在或内容损坏时返回空字典并提示。"""
    if not path.exists():
        print(f"[提示] {path.name} 不存在，从空数据开始。")
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        # 捕获具体异常，而不是裸 except
        print(f"[警告] {path.name} 格式损坏，已忽略：{exc}")
        return {}

    if not isinstance(raw, dict):
        print(f"[警告] {path.name} 内容不是字典，已忽略。")
        return {}
    return {str(k): float(v) for k, v in raw.items()}


def validate(score: float) -> bool:
    """成绩必须在 0-100。这个检查很朴素，但这是"校验输入"的起点。"""
    return 0 <= score <= 100


def main() -> None:
    # 用 dict 存"课程名 -> 分数"
    scores: dict[str, float] = {
        "高等数学": 88.5,
        "大学物理": 92.0,
        "线性代数": 79.0,
    }

    print("=== 成绩统计 ===")
    print(f"课程数：{len(scores)}")
    print(f"平均分：{average(scores):.2f}")

    top = top_course(scores)
    if top is not None:
        print(f"最高分：{top[0]} {top[1]}")

    print("\n=== 查询测试 ===")
    for course in ("大学物理", "量子力学"):
        result = query(scores, course)
        if result is None:
            print(f"{course}：未找到该课程")
        else:
            print(f"{course}：{result}")

    print("\n=== 校验测试 ===")
    for value in (85.0, -5.0, 120.0):
        status = "合法" if validate(value) else "非法"
        print(f"{value} -> {status}")

    print("\n=== 空数据测试（不应崩溃）===")
    print(f"空字典平均分：{average({})}")
    print(f"空字典最高分：{top_course({})}")

    print("\n=== 保存与读回 ===")
    save(scores)
    reloaded = load()
    print(f"读回内容：{reloaded}")
    print(f"读回后平均分：{average(reloaded):.2f}")


if __name__ == "__main__":
    main()
