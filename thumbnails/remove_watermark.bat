@echo off
chcp 65001 >nul
title REMOVE WATERMARK - THUMBNAILS
echo ============================================
echo  REMOVE WATERMARK from thumbnails
echo ============================================
echo.

cd /d "%~dp0"

:: Count images
set IMG_COUNT=0
for %%f in (*.png *.jpg *.jpeg *.webp) do set /a IMG_COUNT+=1
if %IMG_COUNT% equ 0 (
    echo No images found. Put watermarked thumbnails here.
    pause & exit /b 1
)
echo  Found %IMG_COUNT% image(s)

:: Check if already cleaned
if exist "_cleaned\" (
    echo [SKIP] Already processed. Delete _cleaned folder to redo.
    pause & exit /b 0
)

:: Get mask
set "MASK=%~dp0..\_tools\watermark_mask.png"
if not exist "%MASK%" (
    echo ERROR: watermark_mask.png not found
    pause & exit /b 1
)

echo  Removing watermarks...
echo.

:: Create temp input and output folders
mkdir "_input_temp" 2>nul
mkdir "_cleaned" 2>nul

:: Copy originals to temp input
xcopy "*.png" "_input_temp\" /y >nul 2>nul
xcopy "*.jpg" "_input_temp\" /y >nul 2>nul
xcopy "*.jpeg" "_input_temp\" /y >nul 2>nul
xcopy "*.webp" "_input_temp\" /y >nul 2>nul

:: Run IOPaint
"C:\opencode\watermark-remover\venv\Scripts\python.exe" -m iopaint run --model=lama --device=cpu --image="_input_temp" --mask="%MASK%" --output="_cleaned"

if errorlevel 1 (
    echo ERROR: Watermark removal failed.
    pause & exit /b 1
)

:: Replace originals with cleaned versions
echo  Replacing originals with cleaned versions...
xcopy "_cleaned\*.*" . /y >nul 2>nul

:: Clean up temp
rmdir /s /q "_input_temp" 2>nul
rmdir /s /q "_cleaned" 2>nul

echo.
echo  Done! %IMG_COUNT% thumbnails cleaned.
echo.
pause
