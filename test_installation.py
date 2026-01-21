#!/usr/bin/env python3
"""
Blender MCP 설치 테스트 스크립트
이 스크립트는 Blender의 Python 환경에서 실행하여 MCP 패키지 설치를 확인합니다.
"""

import sys

print("=" * 50)
print("Blender MCP 설치 테스트")
print("=" * 50)
print()

# Python 버전 확인
print(f"Python 버전: {sys.version}")
print(f"Python 경로: {sys.executable}")
print()

# bpy 모듈 확인
print("[1/3] Blender Python API (bpy) 확인...")
try:
    import bpy
    print(f"✓ bpy 모듈 로드 성공")
    print(f"  Blender 버전: {bpy.app.version_string}")
except ImportError as e:
    print(f"✗ bpy 모듈을 찾을 수 없습니다: {e}")
    print("  이 스크립트는 Blender 내부에서 실행해야 합니다.")
print()

# MCP 패키지 확인
print("[2/3] MCP 패키지 확인...")
try:
    import mcp
    print(f"✓ mcp 모듈 로드 성공")
    try:
        print(f"  MCP 버전: {mcp.__version__}")
    except AttributeError:
        print("  (버전 정보 없음)")
except ImportError as e:
    print(f"✗ mcp 모듈을 찾을 수 없습니다: {e}")
    print("  install_mcp.bat을 실행하여 MCP 패키지를 설치하세요.")
    sys.exit(1)
print()

# MCP 서버 모듈 확인
print("[3/3] MCP 서버 모듈 확인...")
try:
    from mcp.server import Server
    import mcp.server.stdio
    print("✓ MCP 서버 모듈 로드 성공")
except ImportError as e:
    print(f"✗ MCP 서버 모듈 로드 실패: {e}")
    sys.exit(1)
print()

# 최종 결과
print("=" * 50)
print("✓ 모든 테스트 통과!")
print("=" * 50)
print()
print("Blender MCP 서버를 시작할 준비가 되었습니다.")
print("start_blender_mcp.bat을 실행하여 서버를 시작하세요.")
