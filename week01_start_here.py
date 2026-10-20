# ============================================================
# 第 1 周 · 从这里开始
# ============================================================
#
# 这个文件是给"看得懂语法但写不出来"的人准备的。
#
# 怎么用：
#   1. 从头往下读，一次只读一小节
#   2. 每一节都自己敲一遍（不要复制粘贴）
#   3. 运行看结果：.\dev.cmd run week01_start_here.py
#   4. 改几个数字或文字，再运行，看结果怎么变
#
# 重要：看不懂某一节，就跳过，先往下。回头再看常常就懂了。
# ============================================================


# ------------------------------------------------------------
# 第 1 节：变量 —— 就是给一个值起个名字
# ------------------------------------------------------------

name = "小明"          # 等号左边是名字，右边是值
age = 20
score = 88.5

# print() 是把东西显示到屏幕上
print("第1节：变量")
print(name)
print(age)
print(score)

# 变量可以重新赋值
age = 21               # 现在 age 变成了 21
print(age)

# 把几个东西拼在一起显示。
# 方法一：用逗号分隔（print 会自动加空格）
print("我叫", name, "今年", age, "岁")

# 方法二：f-string。
# 在引号前面加个 f，然后在花括号里写变量名，
# Python 会自动把它替换成变量的值。
# 这个写法最常用，建议记住。
print(f"我叫{name}，今年{age}岁")


# ------------------------------------------------------------
# 第 2 节：列表 —— 一排东西装在一起
# ------------------------------------------------------------

print()
print("第2节：列表")

# 方括号，逗号分隔
scores = [88, 92, 79]

print(scores)          # 整个列表
print(scores[0])       # 第 1 个：88（编号从 0 开始！）
print(scores[1])       # 第 2 个：92
print(scores[2])       # 第 3 个：79
print(scores[-1])      # -1 表示最后一个：79

print(len(scores))     # len() 数一数有几个：3

# 往列表里加东西
scores.append(95)      # 加到末尾
print(scores)          # [88, 92, 79, 95]

# 算总数和平均分
total = sum(scores)         # sum() 求和
count = len(scores)         # 有几个
average = total / count     # 除号是 /
print("总分：", total)
print("平均分：", average)

# 取最大和最小
print("最高分：", max(scores))
print("最低分：", min(scores))


# ------------------------------------------------------------
# 第 3 节：循环 —— 把一件事重复做
# ------------------------------------------------------------

print()
print("第3节：循环")

scores = [88, 92, 79]

# for 循环：把列表里每个元素轮流拿出来，叫它 s
for s in scores:
    print(s)           # 这一行会执行 3 次

print("---")

# 加个判断：只有 90 分以上的才显示
for s in scores:
    if s >= 90:
        print(s, "是优秀")

# 注意缩进！
# 冒号后面缩进的部分，才是"循环里面"要重复做的。
# Python 用缩进（一般是 4 个空格）来表示层级，不用大括号。


# ------------------------------------------------------------
# 第 4 节：字典 —— 名字对应值，像查字典
# ------------------------------------------------------------

print()
print("第4节：字典")

# 花括号，每项是 "键: 值"
student = {
    "姓名": "小明",
    "年龄": 20,
    "专业": "自动化",
}

print(student)
print(student["姓名"])      # 用键取值：小明
print(student["专业"])      # 自动化

# 增加或修改
student["年龄"] = 21        # 改
student["年级"] = "大三"    # 加
print(student)

# 遍历字典
for key in student:
    print(key, "->", student[key])


# ------------------------------------------------------------
# 第 5 节：函数 —— 把一段代码打包起来重复用
# ------------------------------------------------------------

print()
print("第5节：函数")


# def 是 define（定义）的缩写
# 括号里是"参数"，就是外部传进来的东西
# return 是"返回"，把结果交出去
def add(a, b):
    result = a + b
    return result


# 定义好之后，就可以调用它
x = add(3, 5)
print(x)                    # 8
print(add(10, 20))          # 30


def average_of(numbers):
    """算平均分。空列表要特殊处理，不然会除以 0 报错。"""
    if len(numbers) == 0:
        return 0            # 空的时候直接返回 0
    total = sum(numbers)
    return total / len(numbers)


print(average_of([88, 92, 79]))     # 86.33...
print(average_of([]))               # 0（没有报错）


# ------------------------------------------------------------
# 第 6 节：把字典和函数合起来 —— 一个小统计程序
# ------------------------------------------------------------

print()
print("第6节：小统计程序")

# 这次用字典存：课程名 -> 分数
scores = {
    "高等数学": 88,
    "大学物理": 92,
    "线性代数": 79,
}

print("所有课程：", scores)


def get_average(score_dict):
    """算平均分。"""
    if len(score_dict) == 0:
        return 0
    total = 0
    for value in score_dict.values():   # .values() 取出所有分数
        total = total + value
    return total / len(score_dict)


def get_best(score_dict):
    """找出分数最高的课程名。"""
    if len(score_dict) == 0:
        return None

    best_name = None
    best_score = -1              # 先设一个很小的数

    for name in score_dict:
        this_score = score_dict[name]
        if this_score > best_score:
            best_score = this_score
            best_name = name

    return best_name


print("平均分：", get_average(scores))
print("最高分课程：", get_best(scores))

# 查某一门课
course = "大学物理"
if course in scores:            # in 用来判断"在不在里面"
    print(course, "的分数是", scores[course])
else:
    print("没有这门课：", course)

course = "量子力学"
if course in scores:
    print(course, "的分数是", scores[course])
else:
    print("没有这门课：", course)


# ------------------------------------------------------------
# 第 7 节：错误处理 —— 别让程序崩掉
# ------------------------------------------------------------

print()
print("第7节：错误处理")

# 如果把文字当数字用，程序会报错停下。
# try / except 就是"试着做，出错就换个方式处理"

text = "abc"

try:
    number = int(text)          # 想把 "abc" 变成数字，会失败
    print("转换成功：", number)
except ValueError:
    print("转换失败：", text, "不是数字")

# 对比：这次是能成功的
text = "123"
try:
    number = int(text)
    print("转换成功：", number)
except ValueError:
    print("转换失败：", text, "不是数字")


# ------------------------------------------------------------
# 第 8 节：读写文件
# ------------------------------------------------------------

print()
print("第8节：读写文件")

import json                     # json 是标准库，用来存结构化数据
from pathlib import Path        # Path 用来处理文件路径

# __file__ 是"当前这个文件"，.parent 是它所在的文件夹
# 这样写的好处：不管你在哪个目录运行，都能找到正确位置
folder = Path(__file__).parent
file_path = folder / "my_scores.json"

print("要写入的文件：", file_path)

# 写文件
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(scores, f, ensure_ascii=False, indent=2)

print("写入完成")

# 读回来
with open(file_path, "r", encoding="utf-8") as f:
    loaded = json.load(f)

print("读回内容：", loaded)

# with 的作用：用完自动关文件，不用自己写 close()

# 读一个不存在的文件，用 try 保护起来
missing = folder / "根本没有这个文件.json"
try:
    with open(missing, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("读到了：", data)
except FileNotFoundError:
    print("文件不存在，已跳过（没有崩溃）")


# ------------------------------------------------------------
# 第 9 节：小结 —— 你现在会什么了
# ------------------------------------------------------------

print()
print("第9节：小结")
print("你已经用到：")
print("  1. 变量      —— 给值起名字")
print("  2. 列表      —— 一排东西")
print("  3. 循环      —— 重复做")
print("  4. 字典      —— 名字对应值")
print("  5. 函数      —— 打包代码")
print("  6. try/except —— 出错不崩溃")
print("  7. 文件读写  —— 把数据存下来")
print()
print("这些就是写程序最常用的东西。剩下的都是它们的组合。")
