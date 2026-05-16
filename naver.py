import os, re, requests

BASE_URL = "https://openapi.naver.com/v1/search"

FASHION_QUERIES = ["패션 트렌드", "무신사 신상", "29CM 추천", "패션 코디", "셋업 룩"]
NEWS_QUERIES    = ["패션 브랜드 뉴스", "무신사", "패션 플랫폼"]


def _headers():
    # GitHub Secret 이름: NAPI (ID), NAPISECRET (Secret)
    return {
        "X-Naver-Client-Id":     os.getenv("NAPI", ""),
        "X-Naver-Client-Secret": os.getenv("NAPISECRET", "")
    }


def _search(endpoint, query, display=5):
    cid = os.getenv("NAPI", "")
    if not cid:
        print(f"[naver] API 키 없음")
        return []
    try:
        r = requests.get(
            f"{BASE_URL}/{endpoint}",
            headers=_headers(),
            params={"query": query, "display": display, "sort": "date"},
            timeout=10
        )
        if r.status_code != 200:
            print(f"[naver] HTTP {r.status_code}")
            return []
        return r.json().get("items", [])
    except Exception as e:
        print(f"[naver:{endpoint}] {query} 오류: {e}")
        return []


def fetch_naver():
    blog_items, news_items = [], []

    for q in FASHION_QUERIES:
        for item in _search("blog", q, display=3):
            blog_items.append({
                "title":       _strip(item.get("title", "")),
                "description": _strip(item.get("description", "")),
                "link":        item.get("link", ""),
                "date":        item.get("postdate", "")
            })

    for q in NEWS_QUERIES:
        for item in _search("news", q, display=3):
            news_items.append({
                "title":       _strip(item.get("title", "")),
                "description": _strip(item.get("description", "")),
                "link":        item.get("link", ""),
                "source":      item.get("originallink", ""),
                "date":        item.get("pubDate", "")
            })

    # 중복 제거
    seen = set()
    blog_items = [x for x in blog_items if x["title"] not in seen and not seen.add(x["title"])]
    seen = set()
    news_items = [x for x in news_items if x["title"] not in seen and not seen.add(x["title"])]

    if not blog_items and not news_items:
        print("[naver] 결과 없음 — mock 반환")
        return _mock_naver()

    print(f"[naver] 블로그 {len(blog_items)}개, 뉴스 {len(news_items)}개")
    return {"blogs": blog_items[:8], "news": news_items[:6]}


def _strip(text):
    return re.sub(r"<[^>]+>", "", text)


def _mock_naver():
    return {
        "blogs": [
            {"title": "5월 셋업 코디 추천 — 무신사 기획전 총정리", "description": "무신사 셋업 위크 참여 브랜드 220개 이상.", "link": "https://blog.naver.com", "date": ""},
            {"title": "29CM 에디터 Pick 큐레이션 리뷰", "description": "인플루언서 착샷 중심 페이지, 전환율 2.4배.", "link": "https://blog.naver.com", "date": ""},
            {"title": "2025 봄 트렌치코트 핏별 추천", "description": "오버사이즈·벨티드·크롭 비교.", "link": "https://blog.naver.com", "date": ""},
        ],
        "news": [
            {"title": "무신사, 5월 셋업 기획전 — 매출 +38%", "description": "셋업 카테고리 전월 대비 급등.", "link": "", "source": "패션비즈", "date": ""},
            {"title": "MZ 세대 실용성 소비 전환", "description": "원단 퀄리티 언급 비중 +52%.", "link": "", "source": "어패럴뉴스", "date": ""},
        ]
    }
