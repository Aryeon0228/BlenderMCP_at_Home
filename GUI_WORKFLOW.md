# Blender MCP GUI 워크플로우 가이드

## 문제: GUI 모드에서 MCP가 작동하지 않는 이유

MCP(Model Context Protocol)는 **stdin/stdout** 기반으로 통신합니다. Blender를 GUI 모드로 실행하면:

- ❌ stdin/stdout이 GUI 이벤트 루프와 충돌
- ❌ JSON-RPC 메시지가 GUI 출력에 섞임
- ❌ MCP 서버가 응답 없음 상태가 됨

**결론**: MCP 서버는 백그라운드 모드(`--background`)에서만 안정적으로 작동합니다.

---

## 해결책 1: 자동 저장 + 수동 리로드 (권장)

### Claude Desktop 설정 (백그라운드 유지)

`%APPDATA%\Claude\claude_desktop_config.json`:
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

### 워크플로우

1. **작업 파일 경로 설정**
   - 예: `C:\temp\blender_work.blend`

2. **Claude에게 작업 요청 + 저장**
   ```
   (0, 0, 0)에 큐브를 만들고, (5, 0, 0)에 빨간 구를 만들어줘.
   그리고 C:\temp\blender_work.blend 파일로 저장해줘.
   ```

3. **별도의 Blender GUI에서 파일 열기**
   - Blender를 직접 실행
   - File > Open > `C:\temp\blender_work.blend` 선택

4. **변경사항 확인**
   - F12로 렌더링하거나
   - Viewport에서 직접 확인

5. **추가 작업 요청**
   ```
   구를 (10, 0, 0)으로 이동하고 다시 저장해줘.
   ```

6. **Blender GUI에서 리로드**
   - File > Revert (또는 Ctrl+Shift+W)

---

## 해결책 2: 렌더링 이미지로 결과 확인

작업 후 이미지로 렌더링하여 결과를 바로 확인할 수 있습니다.

### 워크플로우

```
큐브와 구를 만들어줘.
그리고 C:\temp\render.png로 렌더링해줘.
```

렌더링된 이미지를 열어서 결과를 확인합니다.

**장점**:
- ✅ Blender를 직접 열 필요 없음
- ✅ 빠르게 결과 확인 가능
- ✅ Claude에게 이미지 분석 요청 가능

**단점**:
- ❌ 3D 뷰어에서 회전/확대 불가
- ❌ 렌더링 시간 소요

---

## 해결책 3: 실시간 모니터링 스크립트 (고급)

Blender GUI를 별도로 띄우고, 파일이 변경되면 자동으로 리로드하는 스크립트를 작성할 수 있습니다.

### Blender GUI에서 실행할 스크립트

Blender의 Scripting 탭에서:

```python
import bpy
import time
from pathlib import Path

WATCH_FILE = r"C:\temp\blender_work.blend"
last_modified = 0

def check_and_reload():
    global last_modified

    if not Path(WATCH_FILE).exists():
        return 1.0  # Check every second

    current_modified = Path(WATCH_FILE).stat().st_mtime

    if current_modified > last_modified:
        last_modified = current_modified
        print(f"File changed, reloading...")
        bpy.ops.wm.open_mainfile(filepath=WATCH_FILE)

    return 1.0  # Check every second

# Register timer
bpy.app.timers.register(check_and_reload)
```

**사용 방법**:
1. Blender GUI 실행
2. Scripting 탭으로 이동
3. 위 코드 붙여넣기
4. Run Script 실행
5. 이제 Claude가 파일을 저장하면 자동으로 리로드됨

---

## 권장 워크플로우 요약

### 빠른 프로토타이핑 (추천)
```
1. Claude에게 작업 요청 + 렌더링
   "큐브를 만들고 C:\temp\render.png로 렌더링해줘"
2. 이미지 확인
3. 수정 요청
4. 반복
```

### 정밀 작업
```
1. Claude에게 작업 요청 + 저장
   "복잡한 모델을 만들고 C:\temp\work.blend로 저장해줘"
2. Blender GUI에서 파일 열기
3. 세부 조정 및 확인
4. 추가 작업을 Claude에게 요청
5. Blender에서 File > Revert로 리로드
```

---

## FAQ

### Q: GUI 모드에서 MCP를 사용할 수 있는 방법은 없나요?

A: MCP는 stdio 기반이라 GUI와 호환되지 않습니다. 대안으로 소켓 기반 통신을 구현할 수 있지만, 이는 MCP 표준을 벗어나며 Claude Desktop과 호환되지 않습니다.

### Q: 매번 파일을 저장하고 리로드하는 게 번거롭습니다.

A: "해결책 3"의 자동 리로드 스크립트를 사용하면 파일이 변경될 때마다 자동으로 리로드됩니다.

### Q: 렌더링이 너무 느립니다.

A: Viewport 렌더링을 사용하거나, 해상도를 낮춰서 빠르게 확인할 수 있습니다:
```
낮은 해상도(800x600)로 렌더링해줘.
```

---

## 결론

백그라운드 MCP 서버 + 자동 저장 + 별도 GUI의 조합이 가장 안정적이고 실용적인 워크플로우입니다.

실시간으로 보고 싶다면 "해결책 3"의 자동 리로드 스크립트를 활용하세요!
