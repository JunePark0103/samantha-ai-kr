@echo off
setlocal enabledelayedexpansion
title Samantha Book Engine - Ultra Starter

echo.
echo ===================================================
echo   Samantha Book Engine - Ultra Starter v2.3
echo ---------------------------------------------------
echo   Searching for Python environment...
echo ===================================================

set PYTHON_CMD=none

python --version >nul 2>&1
if !errorlevel! equ 0 (
    set PYTHON_CMD=python
) else (
    py --version >nul 2>&1
    if !errorlevel! equ 0 (
        set PYTHON_CMD=py
    ) else (
        python3 --version >nul 2>&1
        if !errorlevel! equ 0 (
            set PYTHON_CMD=python3
        )
    )
)

if "%PYTHON_CMD%"=="none" (
    echo [ERROR] Python was not found on your system.
    echo Please install Python from https://www.python.org/
    echo or make sure it is added to your PATH.
    echo.
    pause
    exit /b 1
)

echo [INFO] Using command: %PYTHON_CMD%
%PYTHON_CMD% --version

%PYTHON_CMD% -c "import markdown" >nul 2>&1
if !errorlevel! neq 0 (
    echo [INFO] Installing 'markdown' library...
    %PYTHON_CMD% -m pip install markdown
)

if not exist "convert.py" (
    echo [ERROR] 'convert.py' not found!
    pause
    exit /b 1
)

echo.
echo [RUN] Starting conversion...
%PYTHON_CMD% convert.py

if !errorlevel! neq 0 (
    echo.
    echo [FAIL] Conversion failed.
) else (
    echo.
    echo [SUCCESS] Done! ?
)

echo.
pause