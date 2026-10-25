# -*- coding: utf-8 -*-
"""app 包：把一个大文件拆成职责单一的几块。

Python 靠这个文件判断一个目录是不是"包"。
文件可以是空的，但必须存在，否则 `from app.database import ...` 会报错。
"""
