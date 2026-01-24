@echo off
REM ========================================
REM Update Skills from Production (GitHub)
REM ========================================
REM This script pulls latest changes from GitHub
REM to production directory
REM (D:\AgentSkill\cerebraSkills)
REM for multi-agent consumption
REM ========================================

set PROD_DIR=D:\AgentSkill\cerebraSkills

echo.
echo ========================================
echo Updating Skills from Production (GitHub)
echo ========================================
echo.

cd /d %PROD_DIR% || (
    echo ERROR: Cannot access production directory: %PROD_DIR%
    echo.
    echo Please ensure the directory exists and you have access.
    pause
    exit /b 1
)

echo [1/4] Fetching latest changes from GitHub...
git fetch origin
if errorlevel 1 (
    echo ERROR: Failed to fetch from GitHub
    pause
    exit /b 1
)

echo.
echo [2/4] Switching to main branch...
git checkout main
if errorlevel 1 (
    echo ERROR: Failed to checkout main branch
    pause
    exit /b 1
)

echo.
echo [3/4] Pulling latest changes...
git pull --ff-only origin main
if errorlevel 1 (
    echo ERROR: Failed to pull changes (possible conflicts or diverged branches)
    pause
    exit /b 1
)

echo.
echo [4/4] Success!
echo ========================================
echo Skills updated successfully!
echo ========================================
echo.
echo Production directory is now up to date.
echo Multi-agent systems can now access the latest skills.
echo.
echo [Final Check] Running Gap Analysis on Production...
REM We run this against the current directory (Production)
python "%~dp0scripts\skill_watcher.py" --target .
echo.
pause
