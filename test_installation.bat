@echo off
REM Blender MCP 설치 테스트 스크립트 실행

echo ========================================
echo Blender MCP Installation Test
echo ========================================
echo.

REM Blender 실행 파일 경로 (본인의 경로로 수정하세요)
set BLENDER_PATH=C:\Program Files\Blender Foundation\Blender 5.0\blender.exe

REM 테스트 스크립트 경로
set TEST_SCRIPT=%~dp0test_installation.py

REM 경로 확인
if not exist "%BLENDER_PATH%" (
    echo ERROR: Blender를 찾을 수 없습니다!
    echo 경로: %BLENDER_PATH%
    echo.
    echo 이 배치 파일을 메모장으로 열어서 BLENDER_PATH를 수정하세요.
    echo.
    pause
    exit /b 1
)

if not exist "%TEST_SCRIPT%" (
    echo ERROR: 테스트 스크립트를 찾을 수 없습니다!
    echo 경로: %TEST_SCRIPT%
    echo.
    pause
    exit /b 1
)

echo Blender로 설치 테스트를 실행합니다...
echo.

REM Blender를 백그라운드 모드로 실행하고 테스트 스크립트 실행
"%BLENDER_PATH%" --background --python "%TEST_SCRIPT%"

echo.
echo.
pause
