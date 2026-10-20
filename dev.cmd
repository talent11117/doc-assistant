@echo off
REM Convenience entry point (bypasses PowerShell execution policy).
REM
REM Usage, from the doc-assistant directory:
REM   dev run week01_start_here.py   - run a script
REM   dev test                   - run pytest
REM   dev install <package>      - install a dependency
REM   dev list                   - list installed packages
REM   dev freeze                 - freeze deps to requirements.txt
REM   dev shell                  - open Python REPL
REM   dev check                  - verify the environment

setlocal
set "SCRIPT_DIR=%~dp0"

where pwsh >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    pwsh -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%dev.ps1" %*
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%dev.ps1" %*
)

endlocal
