@echo off
REM ============================================================
REM 双击这个文件，就会用 VS Code 打开当前项目
REM ============================================================

set "PROJECT_DIR=%~dp0"

REM 去掉路径末尾的反斜杠
if "%PROJECT_DIR:~-1%"=="\" set "PROJECT_DIR=%PROJECT_DIR:~0,-1%"

echo Opening project in VS Code...
echo %PROJECT_DIR%
echo.

REM 优先用 PATH 里的 code 命令
where code >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    start "" code "%PROJECT_DIR%"
    goto :done
)

REM 找不到就试常见安装位置
if exist "D:\Microsoft VS Code\Code.exe" (
    start "" "D:\Microsoft VS Code\Code.exe" "%PROJECT_DIR%"
    goto :done
)
if exist "%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe" (
    start "" "%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe" "%PROJECT_DIR%"
    goto :done
)

echo Could not find VS Code.
echo Please open VS Code manually and use File - Open Folder.
pause
exit /b 1

:done
echo Done. VS Code should open in a moment.
timeout /t 2 >nul
