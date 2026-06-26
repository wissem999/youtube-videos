@echo off
chcp 65001 >nul
title GENERATE AUDIO
echo ============================================
echo  STEP 1: Generate Audio from script.txt
echo ============================================
echo.

if not exist "script.txt" (
    for %%f in (*.txt) do set "SCRIPT=%%f" & goto :found
    echo ERROR: No script.txt found!
    pause & exit /b 1
)
:found

echo Using edge-tts... (script.txt ^> audio.mp3)

where edge-tts >nul 2>&1
if %errorlevel% equ 0 (
    edge-tts -f script.txt -v en-US-ChristopherNeural --write-media audio.mp3
    if exist audio.mp3 goto :done
)

if exist "C:\Users\bayou\AppData\Local\Programs\Python\Python311\Scripts\edge-tts.exe" (
    "C:\Users\bayou\AppData\Local\Programs\Python\Python311\Scripts\edge-tts.exe" -f script.txt -v en-US-ChristopherNeural --write-media audio.mp3
    if exist audio.mp3 goto :done
)

if exist "C:\Users\bayou\Desktop\voice_over\generate.bat" (
    copy script.txt "C:\Users\bayou\Desktop\voice_over\script.txt" /Y >nul
    pushd "C:\Users\bayou\Desktop\voice_over"
    call generate.bat
    popd
    copy "C:\Users\bayou\Desktop\voice_over\output.mp3" audio.mp3 /Y >nul
    if exist audio.mp3 goto :done
)

echo ERROR: edge-tts not found. Run setup.bat first.
pause & exit /b 1

:done
for %%f in (audio.mp3) do echo Audio: %%f (%%~zf bytes)
echo.
pause
