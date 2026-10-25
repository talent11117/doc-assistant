# -*- coding: utf-8 -*-
"""models.py —— 只管"数据长什么样"。

判断标准：**这里只有类的定义，没有任何逻辑。**
    有 Field(...) 校验规则的          -> 放这个文件
    有 @router.get / conn.execute     -> 不该放这个文件

为什么单独一个文件？
    因为"数据长什么样"会被很多地方用到：
        路由要它（接收请求体）
        测试要它（构造测试数据）
        将来前端生成 TypeScript 类型也要它
    放一处，改一处，所有地方跟着变。
"""

from pydantic import BaseModel, Field


class ScoreIn(BaseModel):
    """POST /scores 的请求体。

    Field(...) 就是校验规则，和 day07 学的完全一样：
        min_length=1 / max_length=20  ->  课程名长度
        ge=0 / le=100                 ->  分数范围

    传 150 分，FastAPI 会在进你的函数**之前**返回 422，
    你的路由代码根本不会执行。
    """

    course: str = Field(min_length=1, max_length=20, description="课程名")
    score: float = Field(ge=0, le=100, description="分数，0-100")


class ScoreOut(BaseModel):
    """GET /scores/{course} 的响应体。

    ⚠️ 今天**没有用它**，路由里还是直接 return 字典。
    那为什么写出来？因为它是"接口契约"的文档：
    别人看这个文件就知道这个接口返回什么形状。

    想真的用上它，可以在路由上加 response_model：
        @router.get("/scores/{course}", response_model=ScoreOut)
    这样 FastAPI 会：
        1. 按 ScoreOut 校验你的返回值（返回多了/少了字段会报错）
        2. 在 /docs 里显示完整的响应结构
    这是第 14 天写 README 时可以顺手加的东西，今天先放着。
    """

    course: str
    score: float


class ScoreUpdateOut(BaseModel):
    """POST /scores 的响应体。

    updated=True  表示"改的"
    updated=False 表示"新加的"
    """

    course: str
    score: float
    updated: bool
