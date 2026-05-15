import os, requests

BASE_URL = "https://www.googleapis.com/youtube/v3"

FASHION_QUERIES = ["패션 하울 2025", "무신사 코디", "패션 트렌드 봄", "Y2K 코디", "셋업 룩"]


def fetch_youtube():
    key = os.getenv("YOUTUBE_API_KEY")
    if not key:
        return _mock_youtube()

    results = []
    seen_ids = set()

    for query in FASHION_QUERIES:
        try:
            r = requests.get(
                f"{BASE_URL}/search",
                params={
                    "key":        key,
                    "q":          query,
                    "part":       "snippet",
                    "type":       "video",
                    "maxResults": 3,
                    "order":      "viewCount",
                    "relevanceLanguage": "ko",
                    "regionCode": "KR"
                },
                timeout=10
            )
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
                    "thumbnail":   sn["thumbnails"]["medium"]["url"] if "thumbnails" in sn else "",
                    "link":        f"https://youtube.com/watch?v={vid}",
                    "published":   sn.get("publishedAt", "")[:10]
                })
        except Exception as e:
            print(f"[youtube] {query} error: {e}")

    return results[:10] if results else _mock_youtube()


def _mock_youtube():
    return [
        {"title": "5월 패션 하울 BEST — 무신사 3만원대 셋업 리뷰", "channel": "스타일로그", "description": "린넨 셋업·나일론 재킷 착용감 실검증. 세탁 후 변형 여부까지 비교.", "link": "https://youtube.com", "published": "2025-05-14"},
        {"title": "2025 봄 Y2K 코디 완성하는 법 — 빈티지 믹스매치", "channel": "패션피플", "description": "크롭톱·와이드데님·플랫폼슈즈 조합 가이드.", "link": "https://youtube.com", "published": "2025-05-13"},
        {"title": "나일론 재킷 방수 능력 비교 테스트 — 5개 브랜드", "channel": "리뷰맨", "description": "실제 방수 성능 실험 영상. 실용성 중심 소비자 반응.", "link": "https://youtube.com", "published": "2025-05-12"},
        {"title": "미니멀 패션으로 옷장 30벌로 줄이기", "channel": "미니멀라이프", "description": "실용주의 패션 소비 트렌드 반영. 기본템 큐레이션.", "link": "https://youtube.com", "published": "2025-05-11"},
        {"title": "크림 빈티지 스니커즈 리셀 시황 — 5월 2주차", "channel": "스니커헤드TV", "description": "나이키 AF1·뉴발란스 1906R 리셀가 분석.", "link": "https://youtube.com", "published": "2025-05-10"},
    ]
