@echo off
chcp 65001 >nul
title MATCH IMAGES
echo ============================================
echo  STEP 3: Match Images to Transcript
echo ============================================
echo.

if not exist "transcript_words.txt" (
    echo ERROR: transcript_words.txt not found. Run transcribe.bat first.
    pause & exit /b 1
)
if not exist "img\" (
    echo ERROR: img folder not found.
    pause & exit /b 1
)

python "%~dp0match_images.py"
if %errorlevel% neq 0 (
    echo ERROR: Matching failed.
    pause & exit /b 1
)

echo.
echo ============================================
echo  CHECKING SYNC...
echo ============================================
python "%~dp0check_sync.py"
if %errorlevel% neq 0 (
    echo WARNING: Sync check encountered errors.
)
echo.
pause
