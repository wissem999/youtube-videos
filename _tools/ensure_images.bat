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
    echo [IMAGES] Using your cleaned images ^(img\^).
    echo(
    exit /b 0
)

:: Check img-with-watermark as fallback
set WMI_COUNT=0
for %%f in (img-with-watermark\*.png img-with-watermark\*.jpg img-with-watermark\*.jpeg img-with-watermark\*.webp) do set /a WMI_COUNT+=1
if %WMI_COUNT% gtr 0 (
    echo [WATERMARKED] Images found in img-with-watermark\, removing watermarks...
    echo(
    call "%~dp0remove_watermark.bat"
    if errorlevel 1 (
        echo FAILED: Watermark removal failed.
        pause & exit /b 1
    )
    echo  Verifying cleaned images...
    dir /b /a-d "img\*.png" "img\*.jpg" "img\*.jpeg" "img\*.webp" 2>nul >nul
    if not errorlevel 1 (
        echo [IMAGES] Cleaned images ready in img\.
        echo(
        exit /b 0
    ) else (
        echo FAILED: No images found in img\ after watermark removal.
        pause & exit /b 1
    )
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
echo    1. Put .png images in img-with-watermark\ folder
echo    2. Write one visual description per line in imagesprompts.txt
echo    3. Run new_video.bat for a fresh project
echo(
pause
exit /b 1
