@echo off
chcp 65001 >nul
title FULL PIPELINE
echo ============================================
echo  FULL PIPELINE: Audio ^> Transcribe ^> Images ^> Match ^> Render
echo  %cd%
echo ============================================
echo.

if not exist "script.txt" (
    echo ERROR: script.txt not found!
    pause & exit /b 1
)

set "TBAT=%~dp0"

echo.
echo ===== STEP 1/4: Generate Audio =====
call "%TBAT%generate_audio.bat"
if not exist audio.mp3 (
    if exist output.mp3 (rename output.mp3 audio.mp3) else (
        echo FAILED at Step 1 & pause & exit /b 1
    )
)

echo.
echo ===== STEP 2/4: Transcribe =====
call "%TBAT%transcribe.bat"
if not exist transcript_words.txt (
    echo FAILED at Step 2 & pause & exit /b 1
)

echo.
echo ===== STEP 2b/4: Ensure Images =====
call "%TBAT%ensure_images.bat"
if errorlevel 1 (
    echo FAILED at Step 2b: No images available.
    pause & exit /b 1
)

echo.
echo ===== STEP 3/4: Match Images =====
call "%TBAT%match_images.bat"
if not exist timeline.txt (
    echo FAILED at Step 3 & pause & exit /b 1
)

echo.
echo ===== STEP 4/4: Render Video =====
call "%TBAT%render.bat"

if exist output.mp4 (
    echo.
    echo ============================================
    echo  PIPELINE COMPLETE!
    echo  Output: %cd%\output.mp4
    echo ============================================
)
pause
