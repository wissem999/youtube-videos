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
echo ===== STEP 1/5: Generate Audio + Transcript =====
call "%TBAT%generate_audio.bat"
if not exist transcript_words.txt (
    echo FAILED at Step 1 & pause & exit /b 1
)

echo.
echo ===== STEP 2/5: Remove Watermarks =====
call "%TBAT%remove_watermark.bat"

echo.
echo ===== STEP 3/5: Ensure Images =====
call "%TBAT%ensure_images.bat"
if errorlevel 1 (
    echo FAILED at Step 3: No images available.
    pause & exit /b 1
)

echo.
echo ===== STEP 4/5: Match Images =====
call "%TBAT%match_images.bat"
if not exist timeline.txt (
    echo FAILED at Step 4 & pause & exit /b 1
)

echo.
echo ===== STEP 5/5: Render Video =====
call "%TBAT%render.bat"
if not exist output.mp4 (
    echo FAILED at Step 5 & pause & exit /b 1
)

echo.
echo ===== EXTRA: Add Outro =====
call "%TBAT%add_outro.bat"

echo.
echo ============================================
echo  PIPELINE COMPLETE!
echo  Output: %cd%\output.mp4
echo ============================================
pause
