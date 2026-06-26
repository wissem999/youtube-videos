@echo off
chcp 65001 >nul
title TRANSCRIBE
echo ============================================
echo  STEP 2: Transcribe Audio to Word Timings
echo ============================================
echo.

if not exist "audio.mp3" (
    if exist "output.mp3" (rename output.mp3 audio.mp3) else (
        echo ERROR: audio.mp3 not found. Run generate_audio.bat first.
        pause & exit /b 1
    )
)

echo Running WhisperX (word-level timestamps)...
echo This may take a few minutes.
echo.

python "%~dp0transcribe.py"
if %errorlevel% neq 0 (
    echo ERROR: Transcription failed. Install: pip install whisperx
    pause & exit /b 1
)
echo.
pause
