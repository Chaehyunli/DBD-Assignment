@echo off
echo ====================================
echo 가상환경 설정 및 패키지 설치
echo ====================================
echo.

REM py 런처로 Python 버전 확인
echo [1/4] Python 버전 확인...
py --version
if errorlevel 1 (
    echo Python이 설치되어 있지 않거나 py 런처를 사용할 수 없습니다.
    echo Python 3.10 이상을 설치하세요: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.

REM 가상환경 생성
echo [2/4] 가상환경 생성...
py -m venv venv
if errorlevel 1 (
    echo 가상환경 생성 실패!
    pause
    exit /b 1
)
echo 가상환경 생성 완료!
echo.

REM 가상환경 활성화 및 pip 업그레이드
echo [3/4] pip 업그레이드...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
echo.

REM 패키지 설치
echo [4/4] 패키지 설치 중...
pip install -r requirements.txt
if errorlevel 1 (
    echo 패키지 설치 실패!
    pause
    exit /b 1
)
echo.

echo ====================================
echo 설치 완료!
echo ====================================
echo.
echo 다음 명령어로 가상환경을 활성화하세요:
echo   venv\Scripts\activate
echo.
echo 또는 다음 명령어로 DB 연결 테스트를 실행하세요:
echo   venv\Scripts\python.exe test_db_connection.py
echo.
pause
