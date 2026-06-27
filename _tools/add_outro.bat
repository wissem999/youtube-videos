@echo off
chcp 65001 >nul
title ADD OUTRO
cd /d "%~dp0"

set "FFMPEG=C:\Users\LITE\AppData\Local\Programs\Python\Python313\ffmpeg.exe"
set "MAIN_OUTRO=%~dp0..\outro\outro.mp4"

if not exist "%MAIN_OUTRO%" (
    echo ERROR: Outro not found at %MAIN_OUTRO%
    echo Run build_outro.bat from the main project folder first.
    pause & exit /b 1
)

if not exist "output.mp4" (
    echo ERROR: output.mp4 not found in %cd%
    pause & exit /b 1
)

echo.
echo ============================================
echo  APPENDING OUTRO
echo ============================================
echo  Video:  output.mp4
echo  Outro:  %MAIN_OUTRO%
echo ============================================
echo.

"%FFMPEG%" -y -i "output.mp4" -i "%MAIN_OUTRO%" -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -c:a aac -pix_fmt yuv420p -preset medium -crf 23 -b:a 192k "final_output.mp4"

if %errorlevel% neq 0 (
    echo ERROR: Failed to append outro.
    pause & exit /b 1
)

move "output.mp4" "output_main.mp4" >nul
move "final_output.mp4" "output.mp4" >nul

echo.
echo SUCCESS! output.mp4 now includes the outro.
echo Backup: output_main.mp4
echo.
pause
