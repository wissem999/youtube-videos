@echo off
chcp 65001 >nul
title BUILD OUTRO
cd /d "%~dp0"
set "FFMPEG=C:\Users\LITE\AppData\Local\Programs\Python\Python313\ffmpeg.exe"

echo ============================================
echo  BUILDING OUTRO VIDEO
echo ============================================
echo.

if not exist "outro\script.txt" (
    echo ERROR: outro\script.txt not found!
    pause & exit /b 1
)

echo Generating audio...
python -m edge_tts -f "outro\script.txt" -v en-US-ChristopherNeural --rate=+10% --write-media "outro\audio.mp3"
if not exist "outro\audio.mp3" (
    echo ERROR: Audio generation failed.
    pause & exit /b 1
)

echo.
echo Rendering outro MP4...
"%FFMPEG%" -y -loop 1 -i "outro\1. if you enjoyed this exploration.png" -i "outro\audio.mp3" ^
  -c:v libx264 -c:a aac -b:a 192k -pix_fmt yuv420p ^
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1" ^
  -r 24 -preset medium -crf 23 -shortest "outro\outro.mp4"

if exist "outro\outro.mp4" (
    echo.
    echo SUCCESS! outro\outro.mp4 created.
    echo.
    echo Use add_outro.bat to append this to any video:
    echo   add_outro.bat path\to\video.mp4
    echo   add_outro.bat                (uses output.mp4 in current folder)
) else (
    echo ERROR: Render failed.
    pause & exit /b 1
)
pause
