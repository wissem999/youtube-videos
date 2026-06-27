@echo off
chcp 65001 >nul
title FULL PIPELINE
echo ============================================
echo  FULL PIPELINE: Audio ^> Transcribe ^> Remove WM ^> Images ^> Match ^> Render
echo  %cd%
echo ============================================
echo.

if not exist "script.txt" (
    echo ERROR: script.txt not found!
    pause & exit /b 1
)

set "TBAT=%~dp0"

echo.
echo ===== STEP 1/6: Generate Audio =====
call "%TBAT%generate_audio.bat"
if not exist audio.mp3 (
    if exist output.mp3 (rename output.mp3 audio.mp3) else (
        echo FAILED at Step 1 & pause & exit /b 1
    )
)

echo.
echo ===== STEP 2/6: Transcribe =====
call "%TBAT%transcribe.bat"
if not exist transcript_words.txt (
    echo FAILED at Step 2 & pause & exit /b 1
)

echo.
echo ===== STEP 3/6: Remove Watermarks =====
call "%TBAT%remove_watermark.bat"

echo.
echo ===== STEP 4/6: Ensure Images =====
call "%TBAT%ensure_images.bat"
if errorlevel 1 (
    echo FAILED at Step 4: No images available.
    pause & exit /b 1
)

echo.
echo ===== STEP 5/6: Match Images =====
call "%TBAT%match_images.bat"
if not exist timeline.txt (
    echo FAILED at Step 3 & pause & exit /b 1
)

echo.
echo ===== STEP 6/7: Render Video =====
call "%TBAT%render.bat"
if not exist output.mp4 (
    echo FAILED at Step 6 & pause & exit /b 1
)

echo.
echo ===== STEP 7/7: Add Outro =====
call "%TBAT%add_outro.bat"

echo.
echo ============================================
echo  PIPELINE COMPLETE!
echo  Output: %cd%\output.mp4
echo ============================================
pause
