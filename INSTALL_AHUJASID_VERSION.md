# ahujasid/blender-mcp 설치 가이드

이 가이드는 GUI를 지원하는 ahujasid의 blender-mcp 프로젝트를 설치하는 방법입니다.

## 왜 이 버전을 사용하나요?

- ✅ **Blender GUI를 열고 실시간으로 작업 확인 가능**
- ✅ Blender 애드온 패널에서 "Connect to Claude" 버튼으로 간편하게 연결
- ✅ 소켓 기반 통신으로 GUI와 MCP 서버가 독립적으로 작동
- ✅ Poly Haven, Sketchfab, Hyper3D 등 외부 자산 통합

## 설치 단계

### 1단계: uv 패키지 매니저 설치

**Windows PowerShell (관리자 권한)에서:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

설치 후 PowerShell을 재시작하세요.

**확인:**
```cmd
uv --version
```

---

### 2단계: Blender 애드온 다운로드

1. **애드온 파일 다운로드:**
   - https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py
   - 우클릭 → "다른 이름으로 저장" → `blender_mcp_addon.py`로 저장

2. **또는 git clone:**
   ```bash
   git clone https://github.com/ahujasid/blender-mcp.git
   cd blender-mcp
   ```

---

### 3단계: Blender에 애드온 설치

1. **Blender 실행**

2. **Edit → Preferences → Add-ons**

3. **Install 버튼 클릭**

4. **다운로드한 `addon.py` 파일 선택**

5. **"BlenderMCP" 애드온 활성화** (체크박스 체크)

6. **애드온 설정 확인:**
   - Host: `127.0.0.1` (기본값)
   - Port: `9876` (기본값)

7. **Preferences 저장** (Save Preferences 버튼)

---

### 4단계: Claude Desktop 설정

`%APPDATA%\Claude\claude_desktop_config.json` 파일을 수정:

**기존 설정 제거하고 다음으로 교체:**

```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp"]
    }
  }
}
```

---

### 5단계: 연결 및 사용

1. **Blender 실행** (GUI 모드로)

2. **3D Viewport 오른쪽 사이드바에서 "BlenderMCP" 탭 찾기**
   - 사이드바가 안 보이면 `N` 키 누르기

3. **"Connect to Claude" 버튼 클릭**
   - 상태가 "Connected" 또는 "Server Running"으로 변경됨

4. **Claude Desktop 실행**

5. **Claude에게 요청:**
   ```
   큐브를 (0, 0, 0)에 만들어줘
   ```

6. **Blender에서 실시간으로 큐브가 생성되는 것을 확인!**

---

## 사용 예시

### 기본 3D 모델링

```
큐브를 (0, 0, 0)에 만들고, 빨간색으로 칠해줘.
구를 (5, 0, 0)에 만들고, 파란색으로 칠해줘.
```

### Poly Haven 자산 사용

```
Poly Haven에서 "wood floor" 텍스처를 검색하고 적용해줘.
```

### AI 3D 모델 생성 (Hyper3D)

```
Hyper3D로 "medieval castle"을 생성해줘.
```

### 장면 정보 조회

```
현재 씬에 있는 모든 객체를 보여줘.
```

---

## 문제 해결

### 애드온이 보이지 않음

1. Blender를 완전히 재시작
2. Preferences → Add-ons에서 "BlenderMCP" 검색
3. 체크박스가 체크되어 있는지 확인

### "Connect to Claude" 버튼을 눌러도 연결 안 됨

1. 포트 9876이 다른 프로그램에서 사용 중인지 확인:
   ```cmd
   netstat -ano | findstr :9876
   ```

2. 포트가 사용 중이면 애드온 설정에서 다른 포트로 변경

### Claude Desktop에서 MCP 서버를 인식하지 못함

1. `uvx blender-mcp` 명령이 수동으로 작동하는지 테스트:
   ```cmd
   uvx blender-mcp
   ```

2. 에러가 나면 uv 재설치

3. Claude Desktop 완전히 재시작 (트레이에서도 종료)

### Blender가 느리거나 멈춤

- 대용량 자산 다운로드 중일 수 있으므로 잠시 대기
- Blender 콘솔 창 확인 (Window → Toggle System Console)

---

## 기존 BlenderMCP_at_Home과 비교

| 특징 | ahujasid/blender-mcp | BlenderMCP_at_Home |
|------|---------------------|-------------------|
| GUI 지원 | ✅ 실시간 | ❌ 백그라운드만 |
| 설치 복잡도 | 중간 (uv + 애드온) | 쉬움 (스크립트만) |
| 외부 자산 | ✅ 다양함 | ❌ 없음 |
| 자동 시작 | ❌ 수동 연결 | ✅ 자동 |
| 메모리 사용 | 높음 (GUI) | 낮음 (백그라운드) |

---

## 추가 정보

- **공식 GitHub**: https://github.com/ahujasid/blender-mcp
- **Discord 커뮤니티**: [링크는 GitHub README 참조]
- **PyPI 패키지**: https://pypi.org/project/blender-mcp/

---

## 원래 프로젝트로 돌아가기

ahujasid 버전이 맞지 않으면 언제든 원래 BlenderMCP_at_Home으로 돌아갈 수 있습니다:

1. Claude Desktop 설정을 원래대로 변경
2. Blender 애드온 비활성화
3. README.md의 설치 가이드 따라하기

---

**설치 후 즐거운 3D 모델링 되세요!** 🎨✨
