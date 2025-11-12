@echo off
echo ====================================
echo 데이터베이스 연결 테스트
echo ====================================
echo.

REM 가상환경이 있는지 확인
if not exist "venv\Scripts\python.exe" (
    echo 가상환경이 없습니다!
    echo setup_env.bat 을 먼저 실행하세요.
    echo.
    pause
    exit /b 1
)

REM 테스트 실행
venv\Scripts\python.exe test_db_connection.py

echo.
pause
