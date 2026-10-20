# -*- coding: utf-8 -*-
r"""第 8 天自查：Git 基础。

用法（在 doc-assistant 目录下）：
    .\.venv\Scripts\python.exe check_day08.py

它只读不写，不会改你的任何文件。
"""
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
GIT_CANDIDATES = [
    r"C:\Program Files\Git\cmd\git.exe",
    r"C:\Program Files (x86)\Git\cmd\git.exe",
    str(Path.home() / "AppData/Local/PortableGit/cmd/git.exe"),
]

ok_count = 0
fail_count = 0
warn_count = 0


def ok(label, detail=""):
    global ok_count
    ok_count += 1
    print(f"[通过] {label}" + (f"  ({detail})" if detail else ""))


def warn(label, detail=""):
    global warn_count
    warn_count += 1
    print(f"[注意] {label}" + (f"  ({detail})" if detail else ""))


def bad(label, hint):
    global fail_count
    fail_count += 1
    print(f"[未通过] {label}")
    print(f"         怎么办：{hint}")


def find_git():
    for p in GIT_CANDIDATES:
        if Path(p).exists():
            return p
    # 退而求其次：PATH 里找
    try:
        r = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            return "git"
    except Exception:
        pass
    return None


def run(git, *args, cwd=None):
    """跑一条 git 命令，返回 (退出码, stdout+stderr)。"""
    try:
        r = subprocess.run(
            [git, *args],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=30, cwd=str(cwd) if cwd else None,
        )
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}"


print("=" * 60)
print("第 8 天自查：Git 基础")
print("=" * 60)
print()

# ---------- 1. Git 装好了吗 ----------
git = find_git()
if git is None:
    bad("找不到 git", '重开终端；或用全路径 & "C:\\Program Files\\Git\\cmd\\git.exe" --version 测一下')
    print()
    print("后面的检查都需要 git，先解决这个。")
    sys.exit(1)

code, out = run(git, "--version")
ver = out.strip().replace("git version ", "")
ok("git 可用", f"版本 {ver}")

# ---------- 2. .gitconfig 名字改了吗 ----------
code, name = run(git, "config", "--global", "user.name")
code2, email = run(git, "config", "--global", "user.email")
name, email = name.strip(), email.strip()

if not name:
    bad("user.name 没设置", "用 VS Code 打开 C:\\Users\\jack\\.gitconfig，在 [user] 下面加 name = 你的名字")
elif name == "your-name":
    bad("user.name 还是占位符 your-name", "打开 C:\\Users\\jack\\.gitconfig，把 your-name 改成你真实的拼音名")
elif name.strip() in {"Zhang San", "zhangsan", "Li Si", "Wang Wu", "your name"}:
    warn("user.name 还是我文档里的示例名", "打开 C:\\Users\\jack\\.gitconfig，改成你自己名字的拼音")
    print("         （会永久写进每条提交记录，改晚了历史里就都是别人的名字）")
else:
    ok("user.name 已改", name)

if not email:
    bad("user.email 没设置", "在 .gitconfig 的 [user] 下面加 email = 你的邮箱")
elif email == "your-email@example.com" or email.startswith("your-email") or email.startswith("your.name"):
    bad("user.email 还是占位符", "改成你注册 GitHub 用的真实邮箱，否则提交不算你的贡献")
elif "@" not in email:
    bad("user.email 不像一个邮箱", "要有 xxx@yyy 的格式")
else:
    ok("user.email 已改", email)

# ---------- 3. 练习仓库存在吗 ----------
practice = HERE / ".tmp" / "git-practice"
if not practice.exists():
    bad("练习仓库不存在",
        "cd 到 doc-assistant，然后 mkdir .tmp\\git-practice; cd .tmp\\git-practice; git init")
else:
    ok("练习仓库存在", str(practice.relative_to(HERE)))
    code, out = run(git, "rev-parse", "--git-dir", cwd=practice)
    if code != 0:
        bad("练习仓库里没有 .git", "在 .tmp\\git-practice 目录里跑一次 git init")
    else:
        ok("练习仓库是合法的 git 仓库")

        # ---------- 4. 提交数量 ----------
        code, out = run(git, "log", "--oneline", cwd=practice)
        if code != 0:
            bad("练习仓库还没有任何提交", '在 .tmp\\git-practice 里 git add note.txt 然后 git commit -m "第一次提交"')
        else:
            lines = [l for l in out.splitlines() if l.strip()]
            if len(lines) >= 2:
                ok(f"提交数量达标", f"{len(lines)} 条")
                print()
                print("   你的提交记录：")
                for l in lines:
                    print(f"     {l}")
                print()
            else:
                bad(f"提交数量不够（现在 {len(lines)} 条，需要 2 条）",
                    "再改一次 note.txt，git add 然后 git commit -m \"加第二行\"")

        # ---------- 5. note.txt 内容恢复了吗 ----------
        note = practice / "note.txt"
        if not note.exists():
            bad("note.txt 不见了", "在 .tmp\\git-practice 里新建 note.txt，写两行，然后提交")
        else:
            content = note.read_text(encoding="utf-8", errors="replace").strip()
            if not content:
                bad("note.txt 是空的", "跑 git restore note.txt 把它恢复回来")
            elif "第一行" in content:
                ok("note.txt 内容正常", repr(content[:30]))
            else:
                ok("note.txt 有内容", repr(content[:30]))

        # ---------- 6. .gitignore 生效了吗 ----------
        ignore = practice / ".gitignore"
        if not ignore.exists():
            bad("练习仓库里没有 .gitignore",
                "新建 .tmp\\git-practice\\.gitignore，写一行 *.log")
        else:
            ok(".gitignore 存在")
            alog = practice / "a.log"
            if alog.exists():
                code, out = run(git, "status", "--short", "--ignored", cwd=practice)
                if "a.log" in out and "!!" in out:
                    ok(".gitignore 生效了", "a.log 被正确忽略")
                else:
                    code2, tracked = run(git, "ls-files", cwd=practice)
                    if "a.log" in tracked:
                        bad("a.log 被提交进去了", "git rm --cached a.log，然后确认 .gitignore 里有 *.log")
                    else:
                        ok(".gitignore 生效了", "a.log 没有被跟踪")
            else:
                bad("没有 a.log 可以验证 .gitignore",
                    "新建 .tmp\\git-practice\\a.log（随便写点），然后 git status 看它出不出现")

print()
print("=" * 60)
if fail_count == 0:
    print(f"全部通过（{ok_count} 项）。第 8 天完成，可以进第 9 天。")
    if warn_count:
        print(f"另有 {warn_count} 条提醒，建议看一下（不影响继续）。")
    print()
    print("别忘了写笔记：.tmp/git练习_day08.md（三个问题）")
elif ok_count == 0:
    print(f"一项都没通过（{fail_count} 项待做）。从第 0 步开始吧。")
else:
    print(f"通过 {ok_count} 项，还有 {fail_count} 项待做。")
    if warn_count:
        print(f"另有 {warn_count} 条提醒。")
    print("按上面的『怎么办』一条条改，改完再跑一次这个脚本。")
print("=" * 60)
sys.exit(0 if fail_count == 0 else 1)
