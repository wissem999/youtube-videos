@echo off
chcp 65001 >nul
title RENDER VIDEO
echo ============================================
echo  STEP 4: Render Final MP4 Video
echo ============================================
echo.

if not exist "timeline.txt" (
    echo ERROR: timeline.txt not found. Run match_images.bat first.
    pause & exit /b 1
)
if not exist "audio.mp3" (
    if exist "output.mp3" (rename output.mp3 audio.mp3) else (
        echo ERROR: No audio file found.
        pause & exit /b 1
    )
)

:: Ensure ffmpeg is findable
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    if exist "C:\Program Files\Shutter Encoder\Library\ffmpeg.exe" (
        set "PATH=C:\Program Files\Shutter Encoder\Library;%PATH%"
    )
)

python "%~dp0render.py"
if %errorlevel% neq 0 (
    echo ERROR: Render failed.
    pause & exit /b 1
)

for %%f in (output.mp4) do echo Output: %%f (%%~zf bytes)
echo.
pause
