# Blender MCP 서버 설정 가이드 (Windows 11)

이 가이드는 Windows 11에서 Blender 5.01용 MCP 서버를 설정하는 방법을 안내합니다.

## 사전 요구사항

- Windows 11
- Blender 5.01 설치됨
- Claude Desktop 또는 다른 MCP 클라이언트

## 설치 단계

### 1. Blender Python에 MCP 패키지 설치

Blender는 자체 Python 인터프리터를 포함하고 있습니다. MCP 패키지를 Blender의 Python에 설치해야 합니다.

**방법 A: 명령 프롬프트 사용 (권장)**

1. 명령 프롬프트(cmd)를 **관리자 권한**으로 실행합니다.

2. Blender Python 경로로 이동:
   ```cmd
   cd "C:\Program Files\Blender Foundation\Blender 5.0"
   ```

3. pip가 없다면 먼저 설치:
   ```cmd
   .\5.0\python\bin\python.exe -m ensurepip
   ```

4. MCP 패키지 설치:
   ```cmd
   .\5.0\python\bin\python.exe -m pip install mcp
   ```

**방법 B: Blender 내부에서 설치**

1. Blender를 열고 Scripting 탭으로 이동합니다.

2. 새 스크립트를 만들고 다음 코드를 실행:
   ```python
   import subprocess
   import sys

   # Blender의 Python 경로
   python_exe = sys.executable

   # pip 확인 및 설치
   subprocess.check_call([python_exe, "-m", "ensurepip"])

   # MCP 설치
   subprocess.check_call([python_exe, "-m", "pip", "install", "mcp"])

   print("MCP 설치 완료!")
   ```

### 2. MCP 서버 스크립트 위치 확인

`blender_mcp_server.py` 파일의 전체 경로를 확인하세요. 예:
```
C:\Users\YourName\BlenderMCP_at_Home\blender_mcp_server.py
```

### 3. Blender MCP 서버 시작 스크립트 생성

프로젝트 디렉토리에 `start_blender_mcp.bat` 파일을 생성합니다:

```batch
@echo off
echo Starting Blender MCP Server...

REM Blender 실행 파일 경로 (본인의 경로로 수정하세요)
set BLENDER_PATH=C:\Program Files\Blender Foundation\Blender 5.0\blender.exe

REM MCP 서버 스크립트 경로 (본인의 경로로 수정하세요)
set SCRIPT_PATH=%~dp0blender_mcp_server.py

REM Blender를 백그라운드 모드로 실행하고 MCP 서버 시작
"%BLENDER_PATH%" --background --python "%SCRIPT_PATH%"
```

### 4. Claude Desktop 설정

Claude Desktop에서 MCP 서버를 사용하려면 설정 파일을 수정해야 합니다.

1. Claude Desktop 설정 파일 위치:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. 파일을 열고 다음과 같이 추가:
   ```json
   {
     "mcpServers": {
       "blender": {
         "command": "C:\\Program Files\\Blender Foundation\\Blender 5.0\\blender.exe",
         "args": [
           "--background",
           "--python",
           "C:\\Users\\YourName\\BlenderMCP_at_Home\\blender_mcp_server.py"
         ]
       }
     }
   }
   ```

   **주의:** 경로에서 백슬래시(`\`)를 이중 백슬래시(`\\`)로 변경해야 합니다.

3. Claude Desktop을 재시작합니다.

## 사용 방법

### Claude Desktop에서 사용

Claude Desktop이 설정되면 다음과 같이 Blender를 제어할 수 있습니다:

```
Claude, Blender에서 큐브를 만들어줘.
```

```
위치 (5, 0, 0)에 빨간색 구를 만들어줘.
```

### 사용 가능한 명령

- **create_cube**: 큐브 생성
- **create_sphere**: 구 생성
- **delete_object**: 객체 삭제
- **list_objects**: 씬의 모든 객체 나열
- **move_object**: 객체 이동
- **set_material**: 객체에 재질 설정
- **render_scene**: 씬 렌더링
- **save_blend_file**: Blender 파일 저장
- **execute_python**: 임의의 Python 코드 실행

## 문제 해결

### Blender가 시작되지 않음
- Blender 경로가 올바른지 확인하세요
- 관리자 권한으로 실행해보세요

### MCP 패키지를 찾을 수 없음
- Blender의 Python에 MCP가 설치되었는지 확인:
  ```cmd
  "C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\bin\python.exe" -m pip list
  ```

### Claude Desktop에서 연결 안 됨
- `claude_desktop_config.json` 파일의 경로가 올바른지 확인
- JSON 문법이 올바른지 확인 (쉼표, 중괄호 등)
- Claude Desktop 로그 확인:
  ```
  %APPDATA%\Claude\logs
  ```

## 테스트

MCP 서버가 올바르게 작동하는지 테스트하려면:

1. 명령 프롬프트에서 직접 실행:
   ```cmd
   "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python blender_mcp_server.py
   ```

2. 오류 메시지가 없으면 성공입니다!

## 추가 정보

- Blender Python API 문서: https://docs.blender.org/api/current/
- MCP 프로토콜: https://modelcontextprotocol.io
