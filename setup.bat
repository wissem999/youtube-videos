@echo off
chcp 65001 >nul
title SETUP - YouTube Video Pipeline
echo ============================================
echo  INSTALLING DEPENDENCIES
echo ============================================
echo.
cd /d "%~dp0"
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Install Python 3.10+ first.
    pause
    exit /b 1
)
echo [OK] Python: 
python --version
echo.
echo Installing packages (this may take a while)...
pip install -r "_tools\requirements.txt"
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Some packages failed. Try manual install:
    echo   pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
    echo   pip install whisperx edge-tts
) else (
    echo [OK] All packages installed!
)
echo.
echo Setup complete! Run new_video.bat to start.
pause
