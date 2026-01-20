@echo off
echo Starting Skill Watcher...
echo Target Directory: %CD%

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

:: Run the watcher script
python "%~dp0skill_watcher.py" --target . --watch
