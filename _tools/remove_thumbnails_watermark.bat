@echo off
chcp 65001 >nul
title REMOVE THUMBNAIL WATERMARK
echo ============================================
echo  REMOVE WATERMARK from thumbnails
echo  %cd%
echo ============================================
echo.

:: Count images in current folder
set IMG_COUNT=0
for %%f in (*.png *.jpg *.jpeg *.webp) do set /a IMG_COUNT+=1
if %IMG_COUNT% equ 0 (
    echo No images found in %cd%
    pause & exit /b 1
)
echo  Found %IMG_COUNT% image(s)

:: Mask is next to this bat
set "MASK=%~dp0watermark_mask.png"
if not exist "%MASK%" (
    echo ERROR: watermark_mask.png not found
    pause & exit /b 1
)

echo  Removing watermarks...
echo.

:: Temp input folder for IOPaint
mkdir "_input_temp" 2>nul
xcopy "*.png" "_input_temp\" /y >nul 2>nul
xcopy "*.jpg" "_input_temp\" /y >nul 2>nul
xcopy "*.jpeg" "_input_temp\" /y >nul 2>nul
xcopy "*.webp" "_input_temp\" /y >nul 2>nul

:: IOPaint outputs to current folder, overwriting originals
"C:\opencode\watermark-remover\venv\Scripts\python.exe" -m iopaint run --model=lama --device=cpu --image="%cd%\_input_temp" --mask="%MASK%" --output="%cd%"

if errorlevel 1 (
    rmdir /s /q "_input_temp" 2>nul
    echo ERROR: Watermark removal failed.
    pause & exit /b 1
)

rmdir /s /q "_input_temp" 2>nul

echo.
echo  Done! %IMG_COUNT% thumbnails cleaned.
echo.
