#!/usr/bin/env python3
"""
24/7 Market Dashboard — 메인 실행 스크립트
모든 파일이 루트에 있는 평탄한 구조
"""
import sys, json, os
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from weather         import fetch_weather
from naver           import fetch_naver
from youtube         import fetch_youtube
from platforms       import fetch_platforms
from instagram       import fetch_brand_accounts
from claude_analyzer import generate_insights
from render          import render


def main():
    print("=" * 50)
    print(f"  24/7 Dashboard Build — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    print("\n[1/3] 데이터 수집 중...")
    data = {
        "weather":   _run("날씨",       fetch_weather),
        "naver":     _run("네이버",     fetch_naver),
        "youtube":   _run("유튜브",     fetch_youtube),
        "platforms": _run("플랫폼",     fetch_platforms),
        "instagram": _run("인스타그램", fetch_brand_accounts),
    }

    print("\n[2/3] Claude 인사이트 생성 중...")
    data["insights"] = _run("Claude AI", lambda: generate_insights(data))

    today_str = datetime.now().strftime("%Y-%m-%d")
    data_dir = ROOT / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / f"{today_str}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"       저장: data/{today_str}.json")

    print("\n[3/3] HTML 빌드 중...")
    render(data, str(ROOT / "index.html"))

    print(f"\n✅ 완료!")
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
