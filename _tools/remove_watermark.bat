@echo off
chcp 65001 >nul
title REMOVE WATERMARK
echo ============================================
echo  REMOVE WATERMARK from images
echo  %cd%
echo ============================================
echo.

if not exist "img-with-watermark\" (
    echo ERROR: img-with-watermark folder not found!
    echo Create it and put your watermarked images inside.
    pause & exit /b 1
)

:: Count images in source
set IMG_COUNT=0
for %%f in (img-with-watermark\*.png img-with-watermark\*.jpg img-with-watermark\*.jpeg img-with-watermark\*.webp) do set /a IMG_COUNT+=1
if %IMG_COUNT% equ 0 (
    echo ERROR: No images found in img-with-watermark\
    pause & exit /b 1
)
echo  Found %IMG_COUNT% watermarked images

:: Check if already processed
if exist "img\" (
    dir /b /a-d "img\*.png" "img\*.jpg" "img\*.jpeg" "img\*.webp" 2>nul >nul && (
        echo [SKIP] img folder already has cleaned images.
        echo.
        exit /b 0
    )
)

echo.
echo  Removing watermarks using AI...
echo.

:: Get mask from tools folder
set "MASK=%~dp0watermark_mask.png"
if not exist "%MASK%" (
    echo ERROR: watermark_mask.png not found in _tools folder
    pause & exit /b 1
)

:: Run IOPaint batch
"C:\opencode\watermark-remover\venv\Scripts\python.exe" -m iopaint run --model=lama --device=cpu --image="%cd%\img-with-watermark" --mask="%MASK%" --output="%cd%\img"

if errorlevel 1 (
    echo ERROR: Watermark removal failed.
    pause & exit /b 1
)

echo.
echo  Done! Cleaned images saved to img\
echo.
exit /b 0
