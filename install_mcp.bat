@echo off
REM Blender MCP 패키지 설치 스크립트
REM 이 스크립트는 Blender의 Python에 MCP 패키지를 설치합니다.

echo ========================================
echo Blender MCP Package Installer
echo ========================================
echo.

REM Blender Python 경로 (본인의 경로로 수정하세요)
set BLENDER_PYTHON=C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\bin\python.exe

REM 경로 확인
if not exist "%BLENDER_PYTHON%" (
    echo ERROR: Blender Python을 찾을 수 없습니다!
    echo 경로: %BLENDER_PYTHON%
    echo.
    echo 이 배치 파일을 메모장으로 열어서 BLENDER_PYTHON 경로를 수정하세요.
    echo.
    echo 일반적인 Blender 5.0 경로:
    echo C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\bin\python.exe
    echo.
    pause
    exit /b 1
)

echo Blender Python 경로: %BLENDER_PYTHON%
echo.

REM pip 확인 및 설치
echo [1/3] pip 확인 중...
"%BLENDER_PYTHON%" -m ensurepip
if errorlevel 1 (
    echo WARNING: ensurepip 실행 중 경고가 있었지만 계속 진행합니다.
)
echo.

REM pip 업그레이드
echo [2/3] pip 업그레이드 중...
"%BLENDER_PYTHON%" -m pip install --upgrade pip
if errorlevel 1 (
    echo WARNING: pip 업그레이드 중 오류가 발생했지만 계속 진행합니다.
)
echo.

REM MCP 패키지 설치
echo [3/3] MCP 패키지 설치 중...
"%BLENDER_PYTHON%" -m pip install mcp
if errorlevel 1 (
    echo.
    echo ERROR: MCP 패키지 설치에 실패했습니다.
    echo.
    echo 가능한 해결 방법:
    echo 1. 이 스크립트를 관리자 권한으로 실행하세요.
    echo 2. Blender Python 경로가 올바른지 확인하세요.
    echo 3. 인터넷 연결을 확인하세요.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo 설치 완료!
echo ========================================
echo.
echo MCP 패키지가 성공적으로 설치되었습니다.
echo 이제 start_blender_mcp.bat을 실행하여 MCP 서버를 시작할 수 있습니다.
echo.
echo 설치된 패키지 확인:
"%BLENDER_PYTHON%" -m pip list | findstr mcp
echo.
pause
