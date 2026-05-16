"""
Phase 1-D: 아카이브 비교 모듈
- 전주 data/YYYY-MM-DD.json에서 랭킹 데이터 로드
- 현재 랭킹과 비교해 순위 변화 계산
- Weekly Insight용 변화량 요약 생성
"""
import json
from datetime import datetime, timedelta
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


def load_prev_week_data(days_ago: int = 7) -> dict:
    """N일 전 아카이브 데이터 로드"""
    for offset in range(days_ago, days_ago + 4):  # 최대 4일 앞뒤 탐색
        target_date = (datetime.now() - timedelta(days=offset)).strftime("%Y-%m-%d")
        path = DATA_DIR / f"{target_date}.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                print(f"[archive] 이전 데이터 로드: {target_date}")
                return data
            except Exception as e:
                print(f"[archive] 로드 실패 {target_date}: {e}")
    print("[archive] 이전 데이터 없음 — 첫 실행")
    return {}


def compare_rankings(current: list, prev_data: dict) -> list:
    """
    현재 랭킹과 이전 랭킹 비교
    각 아이템에 rank_prev, rank_delta 추가
    """
    if not prev_data:
        return current

    # 이전 랭킹 맵 구성 (상품명 기준)
    prev_platforms = prev_data.get("platforms", {})
    prev_musinsa   = prev_platforms.get("musinsa", [])
    prev_rank_map  = {
        item.get("name", ""): item.get("rank", 999)
        for item in prev_musinsa
    }

    enriched = []
    for item in current:
        name      = item.get("name", "")
        rank_now  = item.get("rank", 999)
        rank_prev = prev_rank_map.get(name)

        if rank_prev is None:
            delta = None  # 신규 진입
            delta_label = "NEW"
        else:
            delta = rank_prev - rank_now  # 양수 = 상승
            if delta > 10:   delta_label = f"↑{delta} 급등"
            elif delta > 0:  delta_label = f"↑{delta}"
            elif delta == 0: delta_label = "→ 유지"
            elif delta > -5: delta_label = f"↓{abs(delta)}"
            else:            delta_label = f"↓{abs(delta)} 하락"

        enriched.append({
            **item,
            "rank_prev":  rank_prev,
            "rank_delta": delta,
            "delta_label": delta_label,
        })

    return enriched


def build_weekly_summary(current_data: dict, prev_data: dict) -> dict:
    """
    전주 대비 주요 변화 요약
    Claude 프롬프트에 추가 컨텍스트로 전달
    """
    if not prev_data:
        return {"available": False, "summary": "첫 실행 — 이전 데이터 없음"}

    curr_platforms = current_data.get("platforms", {})
    prev_platforms = prev_data.get("platforms", {})

    # 무신사 랭킹 변화 분석
    curr_ms = curr_platforms.get("musinsa", [])
    prev_ms = prev_platforms.get("musinsa", [])
    prev_map = {i.get("name",""): i.get("rank",999) for i in prev_ms}

    big_risers  = []  # 큰 폭 상승
    big_fallers = []  # 큰 폭 하락
    new_entries = []  # 신규 진입

    for item in curr_ms:
        name = item.get("name","")
        rank_now = item.get("rank", 999)
        rank_prev = prev_map.get(name)

        if rank_prev is None:
            new_entries.append(f"{name}(신규)")
        elif rank_prev - rank_now > 10:
            big_risers.append(f"{name}(+{rank_prev - rank_now})")
        elif rank_now - rank_prev > 10:
            big_fallers.append(f"{name}(-{rank_now - rank_prev})")

    # 커뮤니티 감성 변화
    curr_comm = current_data.get("community", {}).get("mentions", [])
    prev_comm = prev_data.get("community", {}).get("mentions", [])
    prev_comm_map = {m.get("name",""): m.get("count",0) for m in prev_comm}

    comm_changes = []
    for m in curr_comm[:5]:
        name = m.get("name","")
        curr_cnt = m.get("count",0)
        prev_cnt = prev_comm_map.get(name, 0)
        if prev_cnt > 0 and curr_cnt > prev_cnt * 1.3:
            comm_changes.append(f"{name} 언급 +{round((curr_cnt/prev_cnt-1)*100)}%")

    return {
        "available": True,
        "big_risers":  big_risers[:3],
        "big_fallers": big_fallers[:3],
        "new_entries": new_entries[:3],
        "comm_changes": comm_changes[:3],
        "summary": _build_summary_text(big_risers, big_fallers, new_entries, comm_changes)
    }


def _build_summary_text(risers, fallers, new_entries, comm) -> str:
    parts = []
    if risers:
        parts.append(f"급등: {', '.join(risers[:2])}")
    if new_entries:
        parts.append(f"신규진입: {', '.join(new_entries[:2])}")
    if fallers:
        parts.append(f"하락: {', '.join(fallers[:2])}")
    if comm:
        parts.append(f"커뮤니티 상승: {', '.join(comm[:2])}")
    return " / ".join(parts) if parts else "변화 미미"
