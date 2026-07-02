@echo off
chcp 65001 >nul
title GENERATE AUDIO
echo ============================================
echo  STEP 1: Generate Audio from script.txt
echo ============================================
echo.

python "%~dp0generate_audio.py"
if %errorlevel% neq 0 (
    echo ERROR: Audio generation failed
    pause & exit /b 1
)

echo.
pause
