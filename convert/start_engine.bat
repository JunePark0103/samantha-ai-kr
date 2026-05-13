@echo off
title Samantha Book Engine - Safe Starter
echo.
echo =============================================
echo  Samantha Book Engine v2.1
echo ---------------------------------------------
echo  Starting conversion process...
echo =============================================
echo.

:: 1. Check Python
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install it from python.org
    pause
    exit /b 1
)

:: 2. Check & Install Markdown
python -c "import markdown" > nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing required library (markdown)...
    python -m pip install markdown --quiet
)

:: 3. Run Conversion
echo [RUN] Running convert.py...
echo.
python convert.py

if errorlevel 1 (
    echo.
    echo [FAIL] Something went wrong during conversion.
) else (
    echo.
    echo [SUCCESS] Conversion completed! ✨
    echo Check the 'html_output' folder.
)

echo.
echo Press any key to close...
pause > nul
