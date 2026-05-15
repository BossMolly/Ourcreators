#!/usr/bin/env python3
"""
24/7 Market Dashboard — 메인 실행 스크립트
사용법: python main.py
"""
import sys, json, os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# 경로 설정
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from collectors.weather   import fetch_weather
from collectors.naver     import fetch_naver
from collectors.youtube   import fetch_youtube
from collectors.platforms import fetch_platforms
from collectors.instagram import fetch_brand_accounts
from analysis.claude_analyzer import generate_insights
from builder.render       import render


def main():
    print("=" * 50)
    print(f"  24/7 Dashboard Build — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    # 1. 데이터 수집
    print("\n[1/3] 데이터 수집 중...")
    data = {
        "weather":   _run("날씨",       fetch_weather),
        "naver":     _run("네이버",     fetch_naver),
        "youtube":   _run("유튜브",     fetch_youtube),
        "platforms": _run("플랫폼",     fetch_platforms),
        "instagram": _run("인스타그램", fetch_brand_accounts),
    }

    # 2. Claude 인사이트 생성
    print("\n[2/3] Claude 인사이트 생성 중...")
    data["insights"] = _run("Claude AI", lambda: generate_insights(data))

    # 3. 아카이브 저장
    today_str = datetime.now().strftime("%Y-%m-%d")
    archive_path = ROOT / "data" / f"{today_str}.json"
    archive_path.parent.mkdir(exist_ok=True)
    archive_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"       데이터 저장: data/{today_str}.json")

    # 4. HTML 빌드
    print("\n[3/3] 대시보드 HTML 빌드 중...")
    output = ROOT / "index.html"
    render(data, str(output))

    print(f"\n✅ 완료! → {output}")
    print("=" * 50)


def _run(name, fn):
    try:
        result = fn()
        print(f"   ✓ {name}")
        return result
    except Exception as e:
        print(f"   ✗ {name}: {e}")
        return {}


if __name__ == "__main__":
    main()
