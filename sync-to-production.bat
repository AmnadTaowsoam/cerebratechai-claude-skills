@echo off
REM ========================================
REM Sync Skills to Production (GitHub)
REM ========================================
REM This script pushes changes from local development
REM (D:\Cerebra\cerebraSkills)
REM to GitHub repository
REM ========================================

set DEV_DIR=D:\Cerebra\cerebraSkills

echo.
echo ========================================
echo Syncing Skills to Production (GitHub)
echo ========================================
echo.

cd /d %DEV_DIR% || (
    echo ERROR: Cannot access development directory: %DEV_DIR%
    exit /b 1
)

echo.
echo [0/5] Running Gap Analysis...
python "%~dp0scripts\skill_watcher.py" --target .
if errorlevel 1 (
    echo WARNING: Gap detection failed, but proceeding with sync...
) else (
    echo Gap analysis complete. Check GAP_REPORT.md for details.
)

echo [1/5] Checking git status...
git status

echo.
echo [2/5] Adding all changes...
git add .

echo.
echo [3/5] Committing changes...
set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Update skills from local development

git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo.
    echo No changes to commit or commit failed.
    echo.
    pause
    exit /b 1
)

echo.
echo [4/5] Pushing to GitHub...
git push origin main
if errorlevel 1 (
    echo.
    echo ERROR: Failed to push to GitHub
    echo.
    pause
    exit /b 1
)

echo.
echo [5/5] Success!
echo ========================================
echo Changes pushed to GitHub successfully!
echo ========================================
echo.
echo Next step: Run update-skills.bat to sync to D:\AgentSkill
echo.
pause
