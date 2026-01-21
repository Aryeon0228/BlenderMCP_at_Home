@echo off
REM Blender MCP Server Launcher for Windows
REM 이 스크립트를 실행하기 전에 아래 경로들을 본인의 환경에 맞게 수정하세요.

echo ========================================
echo Blender MCP Server Launcher
echo ========================================
echo.

REM Blender 실행 파일 경로 (본인의 경로로 수정하세요)
set BLENDER_PATH=C:\Program Files\Blender Foundation\Blender 5.0\blender.exe

REM MCP 서버 스크립트 경로 (이 bat 파일과 같은 폴더에 있다고 가정)
set SCRIPT_PATH=%~dp0blender_mcp_server.py

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

if not exist "%SCRIPT_PATH%" (
    echo ERROR: MCP 서버 스크립트를 찾을 수 없습니다!
    echo 경로: %SCRIPT_PATH%
    echo.
    pause
    exit /b 1
)

echo Blender 경로: %BLENDER_PATH%
echo 스크립트 경로: %SCRIPT_PATH%
echo.
echo Blender MCP 서버를 시작합니다...
echo 종료하려면 Ctrl+C를 누르세요.
echo.

REM Blender를 백그라운드 모드로 실행하고 MCP 서버 시작
"%BLENDER_PATH%" --background --python "%SCRIPT_PATH%"

REM 오류 확인
if errorlevel 1 (
    echo.
    echo ERROR: Blender MCP 서버 실행 중 오류가 발생했습니다.
    echo.
    echo 가능한 원인:
    echo 1. MCP 패키지가 설치되지 않음
    echo 2. Python 스크립트에 오류가 있음
    echo 3. Blender 버전 호환성 문제
    echo.
    echo setup_windows.md 파일을 참고하여 MCP 패키지를 설치하세요.
    echo.
    pause
)
