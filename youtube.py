import os, requests

BASE_URL = "https://www.googleapis.com/youtube/v3"

FASHION_QUERIES = [
    "패션 하울 2025", "무신사 코디 추천", "패션 트렌드 봄여름",
    "Y2K 코디 2025", "셋업 룩 코디"
]


def fetch_youtube():
    key = os.getenv("YOUTUBE", "")
    if not key:
        print("[youtube] API 키 없음 — mock 반환")
        return _mock_youtube()

    results = []
    seen_ids = set()

    for query in FASHION_QUERIES:
        try:
            r = requests.get(
                f"{BASE_URL}/search",
                params={
                    "key":               key,
                    "q":                 query,
                    "part":              "snippet",
                    "type":              "video",
                    "maxResults":        3,
                    "order":             "viewCount",
                    "relevanceLanguage": "ko",
                    "regionCode":        "KR",
                    "publishedAfter":    _two_weeks_ago(),
                },
                timeout=10
            )
            if r.status_code != 200:
                print(f"[youtube] HTTP {r.status_code}")
                continue

            for item in r.json().get("items", []):
                vid = item["id"].get("videoId")
                if not vid or vid in seen_ids:
                    continue
                seen_ids.add(vid)
                sn = item["snippet"]
                results.append({
                    "title":       sn.get("title", ""),
                    "channel":     sn.get("channelTitle", ""),
                    "description": sn.get("description", "")[:120],
                    "link":        f"https://youtube.com/watch?v={vid}",
                    "published":   sn.get("publishedAt", "")[:10]
                })
        except Exception as e:
            print(f"[youtube] {query} 오류: {e}")

    if results:
        print(f"[youtube] {len(results)}개 수집")
        return results[:8]

    print("[youtube] 결과 없음 — mock 반환")
    return _mock_youtube()


def _two_weeks_ago():
    from datetime import datetime, timedelta
    return (datetime.utcnow() - timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _mock_youtube():
    return [
        {"title": "5월 패션 하울 BEST — 무신사 3만원대 셋업 리뷰", "channel": "스타일로그", "description": "린넨 셋업·나일론 재킷 착용감 실검증.", "link": "https://youtube.com", "published": ""},
        {"title": "2025 봄 Y2K 코디 완성하는 법", "channel": "패션피플", "description": "크롭톱·와이드데님 조합 가이드.", "link": "https://youtube.com", "published": ""},
        {"title": "나일론 재킷 방수 능력 비교 — 5개 브랜드", "channel": "리뷰맨", "description": "실제 방수 성능 실험 영상.", "link": "https://youtube.com", "published": ""},
        {"title": "미니멀 패션 옷장 30벌로 줄이기", "channel": "미니멀라이프", "description": "실용주의 패션 소비 트렌드.", "link": "https://youtube.com", "published": ""},
        {"title": "크림 빈티지 스니커즈 리셀 시황", "channel": "스니커헤드TV", "description": "나이키 AF1 리셀가 분석.", "link": "https://youtube.com", "published": ""},
    ]
