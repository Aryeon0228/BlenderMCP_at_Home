# BlenderMCP_at_Home

Blender 3D를 제어하기 위한 Model Context Protocol (MCP) 서버입니다.

## 개요

이 프로젝트는 Claude Desktop 또는 다른 MCP 클라이언트를 통해 Blender를 제어할 수 있게 해주는 MCP 서버를 제공합니다. Python을 사용하여 Blender의 강력한 3D 모델링, 애니메이션, 렌더링 기능에 접근할 수 있습니다.

## 지원 플랫폼

- ✅ Windows 11
- ✅ Blender 5.01 (다른 버전도 호환 가능)

## 주요 기능

MCP 서버를 통해 다음 작업을 수행할 수 있습니다:

- 🎲 **3D 객체 생성**: 큐브, 구, 실린더 등 기본 도형 생성
- 🎨 **재질 설정**: 객체에 색상 및 재질 적용
- 🔄 **객체 변환**: 위치, 회전, 크기 조절
- 🗑️ **객체 관리**: 객체 삭제 및 씬 정리
- 📋 **씬 조회**: 현재 씬의 모든 객체 목록 확인
- 🖼️ **렌더링**: 씬을 이미지로 렌더링
- 💾 **파일 저장**: .blend 파일로 작업 저장
- 🐍 **Python 실행**: Blender 컨텍스트에서 임의의 Python 코드 실행

## 빠른 시작

### Windows 11 사용자

자세한 설치 가이드는 [setup_windows.md](setup_windows.md)를 참조하세요.

**간단 설치:**

1. 이 리포지토리를 클론하거나 다운로드합니다.

2. **관리자 권한으로 명령 프롬프트를 실행**하고, Blender의 Python에 필요한 패키지를 설치합니다:
   ```cmd
   "C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\bin\python.exe" -m pip install mcp pywin32
   ```

3. **pywin32 설치 후 post-install 스크립트를 실행합니다** (중요!):
   ```cmd
   "C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\bin\python.exe" "C:\Program Files\Blender Foundation\Blender 5.0\5.0\python\lib\site-packages\pywin32_postinstall.py" -install
   ```

4. Claude Desktop 설정 파일(`%APPDATA%\Claude\claude_desktop_config.json`)을 수정합니다:
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

5. Claude Desktop을 재시작합니다.

**참고:** 설치 중 문제가 발생하면 [TROUBLESHOOTING_WINDOWS.md](TROUBLESHOOTING_WINDOWS.md)를 참조하세요.

## 사용 예시

Claude Desktop에서 다음과 같이 요청할 수 있습니다:

```
큐브를 (0, 0, 0) 위치에 만들어줘.
```

```
빨간색 구를 (5, 0, 0) 위치에 만들고, 반지름은 2로 설정해줘.
```

```
현재 씬에 있는 모든 객체를 보여줘.
```

```
"Cube"라는 이름의 객체를 (10, 10, 5)로 이동해줘.
```

```
씬을 C:\temp\render.png로 렌더링해줘.
```

## 파일 구조

```
BlenderMCP_at_Home/
├── blender_mcp_server.py          # MCP 서버 메인 스크립트
├── requirements.txt                # Python 의존성
├── start_blender_mcp.bat          # Windows 실행 스크립트
├── claude_desktop_config_example.json  # Claude Desktop 설정 예제
├── setup_windows.md               # Windows 설치 가이드
└── README.md                      # 이 파일
```

## MCP 도구 목록

| 도구 이름 | 설명 |
|---------|------|
| `create_cube` | 큐브 생성 |
| `create_sphere` | UV 구 생성 |
| `delete_object` | 객체 삭제 |
| `list_objects` | 씬의 모든 객체 나열 |
| `move_object` | 객체 위치 이동 |
| `set_material` | 객체에 재질 및 색상 설정 |
| `render_scene` | 씬 렌더링 |
| `save_blend_file` | Blender 파일 저장 |
| `execute_python` | Python 코드 실행 |

## 문제 해결

자세한 문제 해결 방법은 [setup_windows.md](setup_windows.md#문제-해결)를 참조하세요.

일반적인 문제:
- **MCP를 찾을 수 없음**: Blender의 Python에 MCP가 설치되었는지 확인
- **Blender를 찾을 수 없음**: `start_blender_mcp.bat`의 경로 확인
- **Claude Desktop 연결 안 됨**: JSON 설정 파일 문법 및 경로 확인

## 기여

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다!

## 라이선스

MIT License

## 참고 자료

- [Blender Python API 문서](https://docs.blender.org/api/current/)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Claude Desktop](https://claude.ai/download)