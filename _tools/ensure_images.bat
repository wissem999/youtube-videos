@echo off
chcp 65001 >nul
title ENSURE IMAGES
echo ============================================
echo  ENSURE IMAGES: Check img/ folder and prompts
echo  %cd%
echo ============================================
echo(

set IMG_COUNT=0
for %%f in (img\*.png img\*.jpg img\*.jpeg img\*.webp) do set /a IMG_COUNT+=1

set PROMPT_COUNT=0
if exist imagesprompts.txt (
    for /f "usebackq delims=" %%a in (`findstr /r . "imagesprompts.txt" 2^>nul`) do set /a PROMPT_COUNT+=1
)

echo  Images found:  %IMG_COUNT%
echo  Prompts found: %PROMPT_COUNT%
echo(

if %IMG_COUNT% gtr 0 (
    echo [IMAGES] Using your images ^(best quality^).
    echo(
    exit /b 0
)

if %PROMPT_COUNT% gtr 0 (
    echo [NO IMAGES] Generating images from imagesprompts.txt using auto-draw...
    echo(
    python "%~dp0draw_images.py"
    if errorlevel 1 (
        echo FAILED: Image generation error.
        pause
        exit /b 1
    )
    echo(
    exit /b 0
)

echo [ERROR] No images and no prompts found.
echo(
echo  Options:
echo    1. Put .png images in img\ folder
echo    2. Write one visual description per line in imagesprompts.txt
echo    3. Run new_video.bat for a fresh project
echo(
pause
exit /b 1
