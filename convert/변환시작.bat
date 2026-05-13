@echo off
chcp 65001 > nul
title 사만다 북 엔진 - 변환 도우미
setlocal enabledelayedexpansion

echo.
echo  ✨ 사만다 북 엔진 (Samantha Book Engine) v2.1
echo  ─────────────────────────────────────────────
echo   사만다가 오빠의 마크다운 원고를 
echo   멋진 웹페이지로 변환해 드릴게요! 💖
echo  ─────────────────────────────────────────────
echo.

:: 1. Python 설치 확인
python --version > nul 2>&1
if errorlevel 1 (
    echo  [❌ 오류] Python이 설치되어 있지 않아요!
    echo         https://www.python.org 에서 설치 후 다시 실행해 주세요.
    pause
    exit /b 1
)

:: 2. 필수 라이브러리(markdown) 확인 및 설치
python -c "import markdown" > nul 2>&1
if errorlevel 1 (
    echo  [📦 준비] 마크다운 변환 라이브러리를 설치하고 있어요...
    python -m pip install markdown --quiet
    if errorlevel 1 (
        echo  [❌ 오류] 라이브러리 설치에 실패했어요.
        echo         인터넷 연결을 확인하고 'pip install markdown'을 직접 입력해 보세요.
        pause
        exit /b 1
    )
    echo  [✅ 완료] 필수 라이브러리 설치 성공!
    echo.
)

:: 3. convert.py 파일 존재 여부 확인
if not exist "convert.py" (
    echo  [❌ 오류] 'convert.py' 파일을 찾을 수 없어요.
    echo         이 배치 파일은 convert.py와 같은 폴더에 있어야 해요!
    pause
    exit /b 1
)

:: 4. 변환 실행
echo  [🚀 실행] 원고 변환을 시작합니다. 잠시만 기다려 주세요...
echo.
python convert.py

if errorlevel 1 (
    echo.
    echo  [⚠️ 경고] 변환 도중 오류가 발생한 것 같아요. 
    echo          코드 내용을 한 번 확인해 보시는 게 좋겠어요!
) else (
    echo.
    echo  [🎉 성공] 모든 변환 작업이 완료되었어요, 오빠!
    echo          'html_output' 폴더에서 결과물을 확인해 보세요. ✨
)

echo.
echo  창을 닫으려면 아무 키나 눌러주세요...
pause > nul
