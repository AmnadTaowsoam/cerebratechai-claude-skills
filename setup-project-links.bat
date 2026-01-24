@echo off
REM ========================================
REM Setup Project Junction Links
REM ========================================
REM สร้าง junction links ให้ project เข้าถึง skills ได้
REM ต้องรันใน project directory ที่ต้องการใช้ skills
REM ========================================

echo.
echo ========================================
echo Setup Project Junction Links
echo ========================================
echo.

REM ตรวจสอบว่ารันด้วย admin หรือไม่
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: ต้องรันด้วย Administrator privileges
    echo.
    echo วิธีแก้:
    echo 1. คลิกขวาที่ Command Prompt
    echo 2. เลือก "Run as administrator"
    echo 3. รัน script นี้อีกครั้ง
    echo.
    pause
    exit /b 1
)

set SKILLS_PATH=D:\AgentSkill\cerebraSkills

REM ตรวจสอบว่า skills directory มีอยู่จริง
if not exist "%SKILLS_PATH%" (
    echo ERROR: ไม่พบ skills directory: %SKILLS_PATH%
    echo.
    echo กรุณา clone repository ก่อน:
    echo cd D:\AgentSkill
    echo git clone https://github.com/AmnadTaowsoam/cerebraSkills.git
    echo.
    pause
    exit /b 1
)

echo Current directory: %CD%
echo Skills path: %SKILLS_PATH%
echo.

REM สร้างโฟลเดอร์ .agentskills
echo [1/3] Creating .agentskills directory...
if not exist ".agentskills" (
    mkdir .agentskills
    echo ✓ Created .agentskills
) else (
    echo ✓ .agentskills already exists
)

echo.

REM สร้าง junction link ไปที่ skills
echo [2/3] Creating junction link: .agentskills\skills
if exist ".agentskills\skills" (
    echo ! .agentskills\skills already exists
    echo   Removing old link...
    rmdir .agentskills\skills
)

mklink /J .agentskills\skills "%SKILLS_PATH%"
if errorlevel 1 (
    echo ERROR: Failed to create junction link
    pause
    exit /b 1
)
echo ✓ Created .agentskills\skills → %SKILLS_PATH%

echo.

REM สร้าง junction link สำหรับ Codex
echo [3/3] Creating junction link: .codex
if exist ".codex" (
    echo ! .codex already exists
    echo   Removing old link...
    rmdir .codex
)

mklink /J .codex .agentskills
if errorlevel 1 (
    echo ERROR: Failed to create .codex junction link
    pause
    exit /b 1
)
echo ✓ Created .codex → .agentskills

echo.
echo ========================================
echo Junction Links Created Successfully!
echo ========================================
echo.
echo โครงสร้าง:
echo %CD%
echo ├── .agentskills\
echo │   └── skills\ → %SKILLS_PATH%
echo └── .codex\ → .agentskills\
echo.
echo ตอนนี้ Agent สามารถเข้าถึง skills ได้แล้ว!
echo.
pause
