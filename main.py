#!/usr/bin/env python3
"""
24/7 Brand Intelligence Dashboard — 메인 실행 스크립트
Phase 1: 무신사 크롤러 + FM코리아 커뮤니티 + 전주 비교 + Claude 고도화 프롬프트
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

from collectors.weather   import fetch_weather
from collectors.naver     import fetch_naver
from collectors.youtube   import fetch_youtube
from collectors.platforms import fetch_platforms
from collectors.musinsa   import fetch_musinsa_ranking
from collectors.fmkorea   import fetch_fmkorea
from collectors.instagram import fetch_brand_accounts
from collectors.archive   import load_prev_week_data, compare_rankings, build_weekly_summary
from analysis.claude_analyzer import generate_insights
from builder.render       import render


def main():
    print("=" * 55)
    print(f"  24/7 Brand Intelligence — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 55)

    # ── 1. 데이터 수집
    print("\n[1/4] 데이터 수집 중...")

    weather   = _run("날씨",            fetch_weather)
    naver     = _run("네이버",          fetch_naver)
    youtube   = _run("유튜브",          fetch_youtube)
    instagram = _run("인스타그램",      fetch_brand_accounts)

    # 무신사 실제 크롤링
    ms_raw    = _run("무신사 랭킹",     lambda: fetch_musinsa_ranking("전체", 20))

    # FM코리아 커뮤니티
    community = _run("FM코리아",        fetch_fmkorea)

    # 기존 platform mock (29CM, KREAM 등)
    platforms_all = _run("플랫폼 데이터", fetch_platforms)

    # ── 2. 전주 비교
    print("\n[2/4] 전주 데이터 비교 중...")
    prev_data      = load_prev_week_data(days_ago=7)
    ms_enriched    = compare_rankings(ms_raw, prev_data)
    weekly_summary = build_weekly_summary(
        {"platforms": {"musinsa": ms_raw}, "community": community},
        prev_data
    )
    platforms_all["musinsa"] = ms_enriched
    print(f"   ✓ 전주 비교 — {weekly_summary.get('summary', '첫 실행')}")

    # ── 3. 데이터 통합
    data = {
        "weather":        weather,
        "naver":          naver,
        "youtube":        youtube,
        "instagram":      instagram,
        "platforms":      platforms_all,
        "community":      community,
        "weekly_summary": weekly_summary,
    }

    # ── 4. Claude 인사이트 생성
    print("\n[3/4] Claude Brand Intelligence 분석 중...")
    data["insights"] = _run("Claude AI", lambda: generate_insights(data))

    # ── 5. 아카이브 저장
    today_str    = datetime.now().strftime("%Y-%m-%d")
    archive_path = ROOT / "data" / f"{today_str}.json"
    archive_path.parent.mkdir(exist_ok=True)
    archive_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"   ✓ 저장: data/{today_str}.json")

    # ── 6. HTML 빌드
    print("\n[4/4] 대시보드 HTML 빌드 중...")
    render(data, str(ROOT / "index.html"))

    print(f"\n✅ 완료!")
    print("=" * 55)


def _run(name: str, fn):
    try:
        result = fn()
        print(f"   ✓ {name}")
        return result
    except Exception as e:
        print(f"   ✗ {name}: {e}")
        return {} if name != "무신사 랭킹" else []


if __name__ == "__main__":
    main()
