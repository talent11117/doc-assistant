# -*- coding: utf-8 -*-
r"""第 9 天自查：GitHub 远程仓库。

用法（在 doc-assistant 目录下）：
    .\.venv\Scripts\python.exe check_day09.py

它只读不写，不会改你的任何文件，也不会联网（只看本地配置和远程地址）。
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


def bad(label, hint):
    global fail_count
    fail_count += 1
    print(f"[未通过] {label}")
    print(f"         怎么办：{hint}")


def warn(label, detail=""):
    global warn_count
    warn_count += 1
    print(f"[注意] {label}" + (f"  ({detail})" if detail else ""))


def find_git():
    for p in GIT_CANDIDATES:
        if Path(p).exists():
            return p
    try:
        r = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            return "git"
    except Exception:
        pass
    return None


def run(git, *args, cwd=None):
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
print("第 9 天自查：GitHub 远程仓库")
print("=" * 60)
print()

git = find_git()
if git is None:
    bad("找不到 git", "重开终端；或用全路径测 & \"C:\\Program Files\\Git\\cmd\\git.exe\" --version")
    sys.exit(1)

# ---------- 1. doc-assistant 是不是 git 仓库 ----------
if not (HERE / ".git").exists():
    bad("doc-assistant 还不是 git 仓库",
        "在 doc-assistant 目录里跑 git init，然后 git add . 和 git commit")
    print()
    print("后面的检查都要先有这个，做完再跑一次。")
    sys.exit(1)

ok("doc-assistant 是 git 仓库")

# ---------- 2. 有没有提交 ----------
code, out = run(git, "log", "--oneline", cwd=HERE)
if code != 0:
    bad("还没有任何提交", 'git add . 然后 git commit -m "第一次提交：..."')
    commits = []
else:
    commits = [l for l in out.splitlines() if l.strip()]
    if len(commits) >= 2:
        ok("提交数量达标", f"{len(commits)} 条")
    elif len(commits) == 1:
        warn("只有 1 条提交", "第 9 天应该有 2 条（主提交 + 修 .env.example 的模型名）")
    else:
        bad("没有提交", "git add . 然后 git commit")

if commits:
    print()
    print("   提交记录（最近 5 条）：")
    for l in commits[:5]:
        print(f"     {l}")
    print()

# ---------- 3. 分支名是不是 main ----------
code, branch = run(git, "branch", "--show-current", cwd=HERE)
branch = branch.strip()
if branch == "main":
    ok("当前分支是 main")
elif branch == "master":
    bad("当前分支叫 master，不是 main",
        "跑 git branch -M main 改名（GitHub 默认分支叫 main）")
elif branch:
    warn(f"当前分支是 {branch}", "不是 main，确认一下这是你想要的")
else:
    bad("没有当前分支（仓库可能是空的）", "先做一次 git commit")

# ---------- 4. 有没有配远程 ----------
code, remotes = run(git, "remote", "-v", cwd=HERE)
if not remotes.strip():
    bad("没有配置远程仓库",
        "去 https://github.com/new 建仓库，然后 git remote add origin https://github.com/你的用户名/doc-assistant.git")
else:
    ok("已配置远程仓库")
    print()
    for line in remotes.strip().splitlines():
        print(f"     {line}")
    print()

    # 检查地址是不是 GitHub
    if "github.com" in remotes:
        ok("远程地址是 GitHub")
    elif "gitee.com" in remotes:
        warn("远程地址是 Gitee", "能用，但校招认可度不如 GitHub。有余力再迁到 GitHub")
    else:
        warn("远程地址不是 GitHub 也不是 Gitee", "确认一下这是什么")

    # 检查有没有把 token 写进 URL（严重安全问题）
    if "@github.com" in remotes or "ghp_" in remotes:
        bad("远程地址里含用户名/token！",
            "立刻跑 git remote set-url origin https://github.com/你的用户名/doc-assistant.git 去掉它，"
            "并去 https://github.com/settings/tokens 撤销那个 token")

# ---------- 5. 安全检查：有没有把敏感文件提交进去 ----------
code, tracked = run(git, "ls-files", cwd=HERE)
files = [f for f in tracked.splitlines() if f.strip()]

if not files:
    bad("仓库里没有任何文件被跟踪", "git add . 然后 git commit")
else:
    ok("仓库里有文件被跟踪", f"{len(files)} 个")

    # 5.1 敏感文件
    dangerous = []
    for f in files:
        low = f.lower().replace("\\", "/")
        base = low.rsplit("/", 1)[-1]
        if base == ".env" or base.startswith(".env.") and base != ".env.example":
            dangerous.append(f)
        elif "/.venv/" in low or low.startswith(".venv/"):
            dangerous.append(f)
        elif base.endswith(".key") or base == "secrets.json":
            dangerous.append(f)

    if dangerous:
        bad(f"有 {len(dangerous)} 个敏感文件被提交了！",
            "git rm --cached <文件>，然后确认 .gitignore 有对应规则，再 git commit。"
            "如果里面有真 Key，立刻去平台撤销重建")
        for d in dangerous[:10]:
            print(f"         -> {d}")
        if len(dangerous) > 10:
            print(f"         ... 还有 {len(dangerous) - 10} 个")
    else:
        ok("没有 .env / .venv / .key 被提交", "安全")

    # 5.2 .venv 文件数量（间接判断）
    venv_files = [f for f in files if ".venv/" in f.replace("\\", "/")]
    if venv_files:
        bad(f"有 {len(venv_files)} 个 .venv 里的文件被提交",
            "git rm -r --cached .venv，确认 .gitignore 第一行是 .venv/，然后 git commit")
    else:
        ok(".venv 没有被提交", "很好，仓库不会变成 100MB")

    # 5.3 文件里有没有 sk- 开头的 key
    # 只匹配真实 key 的形状：sk- 后面跟 20 个以上的字母数字。
    # 不匹配说明文字（如 "# sk- 开头的 key"）和代码里的字符串（如 'sk-' not in s）
    KEY_RE = re.compile(r"sk-[A-Za-z0-9]{20,}")
    suspects = []
    for f in files:
        p = HERE / f
        if not p.is_file():
            continue
        # 跳过自查脚本自身：它里面写了 "sk-" 这个字符串做检测，不是真 key
        if p.name in {"check_day08.py", "check_day09.py"}:
            continue
        if p.suffix.lower() in {".py", ".md", ".txt", ".json", ".ini", ".cfg", ".yaml", ".yml", ".example"}:
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for line in text.splitlines():
                for m in KEY_RE.finditer(line):
                    token = m.group(0)
                    # 明显是示例的跳过
                    if token.lower() in {"sk-xxxxxxxxxxxxxxxxxxxx", "sk-testtesttesttesttest"}:
                        continue
                    suspects.append((f, token[:12] + "..." + token[-4:]))

    if suspects:
        bad(f"有 {len(suspects)} 处疑似真实 API Key 在仓库文件里",
            "这些文件推上去就等于公开密码。删掉 key，改成读 .env，然后 git commit")
        for f, s in suspects[:5]:
            print(f"         -> {f}: {s}")
    else:
        ok("仓库文件里没有疑似真实 API Key", "安全")

# ---------- 6. 本地和远程同步了吗 ----------
code, out = run(git, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", cwd=HERE)
if code != 0:
    bad("本地分支没有关联远程分支",
        "git push -u origin main（-u 就是建立关联）")
else:
    upstream = out.strip()
    ok("本地分支已关联远程", upstream)

    code, out = run(git, "rev-list", "--left-right", "--count", f"{upstream}...HEAD", cwd=HERE)
    if code == 0 and out.strip():
        parts = out.split()
        if len(parts) == 2:
            behind, ahead = int(parts[0]), int(parts[1])
            if ahead == 0 and behind == 0:
                ok("本地和远程完全同步")
            else:
                if ahead > 0:
                    bad(f"有 {ahead} 条提交还没推上去", "git push")
                if behind > 0:
                    warn(f"远程有 {behind} 条你本地没有的提交", "git pull --rebase")

# ---------- 7. .env.example 的模型名改了吗 ----------
example = HERE / ".env.example"
if example.exists():
    text = example.read_text(encoding="utf-8", errors="replace")
    if "deepseek-chat" in text:
        bad(".env.example 里还是失效的 deepseek-chat",
            "改成 LLM_MODEL=deepseek-flash，然后 git add .env.example && git commit")
    elif "deepseek-flash" in text:
        ok(".env.example 的模型名已更新", "deepseek-flash")
    else:
        warn(".env.example 里没有找到模型名", "确认一下是不是被改成了别的")

# ---------- 8. 工作区干净吗 ----------
code, out = run(git, "status", "--porcelain", cwd=HERE)
dirty = [l for l in out.splitlines() if l.strip()]
if dirty:
    warn(f"工作区有 {len(dirty)} 个未提交的改动",
         "如果是有意留的，忽略；如果是忘了提交，git add . && git commit")
else:
    ok("工作区干净（所有改动都提交了）")

print()
print("=" * 60)
if fail_count == 0:
    print(f"全部通过（{ok_count} 项）。第 9 天完成。")
    if warn_count:
        print(f"另有 {warn_count} 条提醒，不影响完成。")
    print()
    print("去网页上看一眼：https://github.com/你的用户名/doc-assistant")
    print("确认文件都在，提交记录旁边是你的头像。")
elif ok_count == 0:
    print(f"一项都没通过（{fail_count} 项待做）。从第 2 步开始吧。")
else:
    print(f"通过 {ok_count} 项，还有 {fail_count} 项待做。")
    print("按上面的『怎么办』一条条改，改完再跑一次。")
print("=" * 60)
sys.exit(0 if fail_count == 0 else 1)
