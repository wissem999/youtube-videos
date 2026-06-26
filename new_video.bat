@echo off
chcp 65001 >nul
title NEW VIDEO PROJECT

cd /d "%~dp0"

for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set dt=%%I
set today=%dt:~0,4%-%dt:~4,2%-%dt:~6,2%_%dt:~8,2%-%dt:~10,2%-%dt:~12,2%-%dt:~15,3%
set "PROJECT=%CD%\%today%"

mkdir "%PROJECT%" 2>nul
copy nul "%PROJECT%\script.txt" >nul
copy nul "%PROJECT%\imagesprompts.txt" >nul
mkdir "%PROJECT%\img" 2>nul

set "TOOLS=%~dp0_tools"

:: Create local batch files in project folder
set "LOCAL_BATS=generate_audio.bat transcribe.bat ensure_images.bat match_images.bat render.bat run_all.bat"
for %%b in (%LOCAL_BATS%) do (
    copy nul "%PROJECT%\%%b" >nul
    (
        echo @echo off
        echo chcp 65001 ^>nul
        echo cd /d "%%~dp0"
        echo call "%TOOLS%\%%b"
    ) > "%PROJECT%\%%b"
)

cls
echo ============================================
echo  NEW PROJECT: %today%
echo ============================================
echo.
echo  %PROJECT%
echo.
echo  Files:
echo    script.txt         - Write your script here
echo    imagesprompts.txt  - Write image prompts here (one per line, for auto-draw)
echo    img\               - Put images here (1. title.png, 2. title.png, ...)
echo    generate_audio.bat - Step 1: Generate MP3 from script
echo    transcribe.bat     - Step 2: Transcribe words + timings
echo    ensure_images.bat  - Step 2b: Auto-gen images if prompts exist
echo    match_images.bat   - Step 3: Match images to transcript
echo    render.bat         - Step 4: Render final MP4
echo    run_all.bat        - Do everything at once
echo.
echo  Image naming: 1. your sentence.png
echo.
echo  For prompt template, see _tools\img_prompt_template.txt
echo.
echo ============================================
pause
start "" "%PROJECT%"
