@echo off
chcp 65001 >nul
title ADD OUTRO
setlocal enabledelayedexpansion

cd /d "%~dp0"

set "FFMPEG=C:\Users\LITE\AppData\Local\Programs\Python\Python313\ffmpeg.exe"
set "OUTRO=%~dp0outro\outro.mp4"
set "INPUT_VIDEO=%~1"

if "%INPUT_VIDEO%"=="" (
    if exist "output.mp4" (
        set "INPUT_VIDEO=output.mp4"
    ) else (
        echo ERROR: No video specified and output.mp4 not found.
        echo Usage: %~nx0 [path_to_main_video.mp4]
        pause
        exit /b 1
    )
)

if not exist "!INPUT_VIDEO!" (
    echo ERROR: Input video not found: !INPUT_VIDEO!
    pause
    exit /b 1
)

if not exist "!OUTRO!" (
    echo ERROR: Outro not found. Run build_outro.bat first.
    pause
    exit /b 1
)

echo ============================================
echo  APPENDING OUTRO TO VIDEO
echo ============================================
echo  Input:  !INPUT_VIDEO!
echo  Outro:  !OUTRO!
echo  Output: final_output.mp4
echo ============================================
echo.

"!FFMPEG!" -y -i "!INPUT_VIDEO!" -i "!OUTRO!" -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -c:a aac -pix_fmt yuv420p -preset medium -crf 23 -b:a 192k "final_output.mp4"

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS! final_output.mp4 created.
    if "!INPUT_VIDEO!"=="output.mp4" (
        echo.
        echo Renaming output.mp4 -^> output_main.mp4
        move "output.mp4" "output_main.mp4" >nul
        echo Renaming final_output.mp4 -^> output.mp4
        move "final_output.mp4" "output.mp4" >nul
        echo Ready: output.mp4 ^(with outro^)
    )
) else (
    echo ERROR: Failed to append outro.
    pause
    exit /b 1
)

pause
