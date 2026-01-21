# Windows 문제 해결 가이드

## 에러: ModuleNotFoundError: No module named 'pywintypes'

### 증상
```
Traceback (most recent call last):
  File "C:\Users\rekys\BlenderMCP_at_Home\blender_mcp_server.py", line 65, in <module>
    from mcp.server import Server
  ...
ModuleNotFoundError: No module named 'pywintypes'
```

### 원인
Windows에서 MCP 라이브러리가 `pywin32` 패키지를 필요로 하는데 설치되지 않았습니다.

### 해결 방법

#### 옵션 1: Blender Python에 pywin32 설치 (권장)

1. **관리자 권한으로 명령 프롬프트(CMD)를 실행합니다**
   - Windows 검색에서 "cmd" 입력
   - "명령 프롬프트"를 우클릭하고 "관리자 권한으로 실행"

2. **Blender Python에 pywin32 설치:**
   ```cmd
   "C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\bin\python.exe" -m pip install pywin32
   ```

3. **pywin32 post-install 스크립트 실행:**
   ```cmd
   "C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\bin\python.exe" "C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\lib\site-packages\pywin32_postinstall.py" -install
   ```

4. **Claude Desktop을 재시작합니다**

#### 옵션 2: 사용자 site-packages에 pywin32 설치

관리자 권한 없이 설치하려면:

1. **일반 명령 프롬프트 실행**

2. **사용자 Python에 pywin32 설치:**
   ```cmd
   python -m pip install --user pywin32
   ```

3. **post-install 스크립트 실행:**
   ```cmd
   python -m pip show pywin32
   ```
   출력에서 "Location" 경로를 확인한 후:
   ```cmd
   python "C:\Users\YourName\AppData\Roaming\Python\Python311\site-packages\pywin32_postinstall.py" -install
   ```

4. **Claude Desktop을 재시작합니다**

---

## 에러: Unexpected token 'B', "Blender 5."... is not valid JSON

### 증상
```
Unexpected token 'B', "Blender 5."... is not valid JSON
Server transport closed unexpectedly
```

### 원인
Blender가 stdout으로 시작 메시지를 출력하여 MCP의 JSON-RPC 통신을 방해합니다.

### 해결 방법

#### Wrapper 스크립트 사용

Wrapper 스크립트가 Blender의 불필요한 출력을 필터링합니다.

1. **Claude Desktop 설정 파일 수정:**

   `%APPDATA%\Claude\claude_desktop_config.json` 파일을 열어서:

   **변경 전:**
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

   **변경 후 (Python Launcher 사용):**
   ```json
   {
     "mcpServers": {
       "blender": {
         "command": "py",
         "args": [
           "C:\\Users\\YourName\\BlenderMCP_at_Home\\blender_mcp_wrapper.py"
         ]
       }
     }
   }
   ```

   또는 **변경 후 (Python 직접 경로):**
   ```json
   {
     "mcpServers": {
       "blender": {
         "command": "C:\\Users\\YourName\\AppData\\Local\\Programs\\Python\\Python311\\python.exe",
         "args": [
           "C:\\Users\\YourName\\BlenderMCP_at_Home\\blender_mcp_wrapper.py"
         ]
       }
     }
   }
   ```

2. **wrapper 스크립트의 Blender 경로 확인:**

   `blender_mcp_wrapper.py` 파일을 열어서 95번째 줄 근처의 경로가 맞는지 확인:
   ```python
   if sys.platform == "win32":
       blender_exe = r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"
   ```

3. **Claude Desktop을 재시작합니다**

---

## 설치 확인

모든 것이 올바르게 설치되었는지 확인:

### 1. pywin32 설치 확인

```cmd
"C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\bin\python.exe" -c "import pywintypes; print('pywin32 OK')"
```

성공하면 "pywin32 OK"가 출력됩니다.

### 2. MCP 설치 확인

```cmd
"C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\bin\python.exe" -c "import mcp; print('MCP OK')"
```

성공하면 "MCP OK"가 출력됩니다.

### 3. 전체 스택 테스트

```cmd
"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python "C:\Users\YourName\BlenderMCP_at_Home\blender_mcp_server.py"
```

에러 없이 실행되고 JSON-RPC 초기화 메시지가 나오면 성공입니다.

---

## 추가 문제 해결

### Claude Desktop이 MCP 서버를 인식하지 못함

1. **JSON 구문 확인**: JSON 파일에 문법 오류가 없는지 확인 (쉼표, 중괄호 등)
2. **경로에 역슬래시 이중 사용**: Windows 경로는 `\\`로 이스케이프 필요
3. **Claude Desktop 완전히 재시작**: 트레이에서도 종료해야 함

### Python을 찾을 수 없음

Claude Desktop 설정에서:
- `"command": "python"`가 작동하지 않으면
- `"command": "py"` 시도 (Windows Python Launcher)
- 또는 전체 경로 사용: `"command": "C:\\Python311\\python.exe"`

### 로그 확인 방법

Claude Desktop의 로그 확인:
1. Claude Desktop 설정 열기
2. "Developer" 섹션 찾기
3. "Show Logs" 클릭
4. MCP 연결 오류 확인

---

## 빠른 체크리스트

- [ ] Blender 5.0 설치됨
- [ ] Python 3.11 설치됨
- [ ] Blender Python에 `mcp` 패키지 설치됨
- [ ] Blender Python에 `pywin32` 패키지 설치됨
- [ ] `pywin32_postinstall.py` 실행됨
- [ ] Claude Desktop 설정 파일 수정됨
- [ ] 모든 경로가 올바름 (역슬래시 이중 사용)
- [ ] Claude Desktop 재시작됨

모든 항목을 확인했는데도 작동하지 않으면 이슈를 올려주세요!
