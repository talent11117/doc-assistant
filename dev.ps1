# Convenience helper for this project.
#
# Usage, from the doc-assistant directory:
#   .\dev.ps1 run week01_start_here.py   - run a script
#   .\dev.ps1 test                   - run pytest
#   .\dev.ps1 install <package>      - install a dependency
#   .\dev.ps1 list                   - list installed packages
#   .\dev.ps1 freeze                 - freeze deps to requirements.txt
#   .\dev.ps1 shell                  - open a Python REPL
#   .\dev.ps1 check                  - verify the environment
#
# Note: this file is intentionally ASCII-only. Windows PowerShell 5.1 reads
# .ps1 files as the system ANSI codepage unless they carry a UTF-8 BOM, so
# non-ASCII text here would be mis-decoded.

param(
    [Parameter(Position = 0)]
    [string]$Command = "check",

    [Parameter(Position = 1, ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$TempDir = Join-Path $ProjectRoot ".tmp"

if (-not (Test-Path $Python)) {
    Write-Host "ERROR: interpreter not found: $Python" -ForegroundColor Red
    Write-Host "Create it first with: py -3.12 -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Keep temp files inside the project to avoid system-temp permission issues.
$env:TEMP = $TempDir
$env:TMP = $TempDir
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

switch ($Command.ToLower()) {
    "run" {
        if (-not $Args) { Write-Host "Usage: .\dev.ps1 run <script.py>" -ForegroundColor Yellow; exit 1 }
        & $Python @Args
    }
    "test" {
        & $Python -m pytest @Args
    }
    "install" {
        if (-not $Args) { Write-Host "Usage: .\dev.ps1 install <package>" -ForegroundColor Yellow; exit 1 }
        & $Python -m pip install @Args
    }
    "list" {
        & $Python -m pip list
    }
    "freeze" {
        & $Python -m pip freeze | Out-File -FilePath (Join-Path $ProjectRoot "requirements.txt") -Encoding utf8
        Write-Host "Wrote requirements.txt" -ForegroundColor Green
    }
    "shell" {
        Write-Host "Python REPL (type exit() to leave)" -ForegroundColor Cyan
        & $Python
    }
    "check" {
        Write-Host "=== interpreter ===" -ForegroundColor Cyan
        & $Python -c "import sys; print(sys.version.split()[0], '|', sys.executable); print('isolated:', sys.prefix != sys.base_prefix)"
        Write-Host ""
        Write-Host "=== key dependencies ===" -ForegroundColor Cyan
        & $Python -c "import importlib
for name in ['requests', 'httpx', 'pytest', 'dotenv']:
    try:
        mod = importlib.import_module(name)
        print('  %-10s %s' % (name, getattr(mod, '__version__', 'OK')))
    except ImportError:
        print('  %-10s NOT INSTALLED' % name)
"
        Write-Host ""
        Write-Host "=== temp dir ===" -ForegroundColor Cyan
        & $Python -c "import tempfile, pathlib
d = tempfile.mkdtemp()
pathlib.Path(d, 't.txt').write_text('x', encoding='utf-8')
print('  writable: OK')
"
        Write-Host ""
        Write-Host "Environment OK." -ForegroundColor Green
    }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host "Available: run / test / install / list / freeze / shell / check" -ForegroundColor Yellow
        exit 1
    }
}
