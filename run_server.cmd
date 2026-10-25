@echo off
REM ============================================================
REM 启动成绩服务
REM
REM 双击这个文件，或者在终端里跑 run_server.cmd
REM 然后在浏览器打开 http://127.0.0.1:8000/docs
REM
REM --reload 的意思是"改了代码自动重启"，开发时很有用。
REM 按 Ctrl+C 停止服务。
REM ============================================================

cd /d "%~dp0"

".venv\Scripts\python.exe" -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
