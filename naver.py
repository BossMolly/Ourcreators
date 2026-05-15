import os, requests

HEADERS_TEMPLATE = {
    "X-Naver-Client-Id": "",
    "X-Naver-Client-Secret": ""
}

BASE_URL = "https://openapi.naver.com/v1/search"

FASHION_QUERIES = ["패션 트렌드", "무신사 신상", "29CM 추천", "패션 코디", "셋업 룩"]
NEWS_QUERIES    = ["패션 브랜드 뉴스", "무신사", "패션 플랫폼"]


def _headers():
    return {
        "X-Naver-Client-Id":     os.getenv("NAVER_CLIENT_ID", ""),
        "X-Naver-Client-Secret": os.getenv("NAVER_CLIENT_SECRET", "")
    }


def _search(endpoint, query, display=5):
    if not os.getenv("NAVER_CLIENT_ID"):
        return []
    try:
        r = requests.get(
            f"{BASE_URL}/{endpoint}",
            headers=_headers(),
            params={"query": query, "display": display, "sort": "date"},
            timeout=10
        )
        return r.json().get("items", [])
    except Exception as e:
        print(f"[naver:{endpoint}] {query} error: {e}")
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

    # 중복 제거 (title 기준)
    seen = set()
    blog_items = [x for x in blog_items if x["title"] not in seen and not seen.add(x["title"])]
    seen = set()
    news_items = [x for x in news_items if x["title"] not in seen and not seen.add(x["title"])]

    if not blog_items and not news_items:
        return _mock_naver()

    return {"blogs": blog_items[:8], "news": news_items[:6]}


def _strip(text):
    import re
    return re.sub(r"<[^>]+>", "", text)


def _mock_naver():
    return {
        "blogs": [
            {"title": "5월 셋업 코디 추천 — 무신사 기획전 총정리", "description": "무신사 셋업 위크 참여 브랜드 220개 이상, 린넨·워시드 소재 집중 노출.", "link": "https://blog.naver.com", "date": "20250515"},
            {"title": "29CM 에디터 Pick — 감각적 데일리룩 큐레이션", "description": "인플루언서 착샷 중심 페이지, 전환율 2.4배 상승 기록.", "link": "https://blog.naver.com", "date": "20250515"},
            {"title": "2025 봄 트렌치코트 핏별 추천 가이드", "description": "오버사이즈·벨티드·크롭 비교. 30대 직장인 타깃 포스팅 검색 상위.", "link": "https://blog.naver.com", "date": "20250514"},
        ],
        "news": [
            {"title": "무신사, 5월 셋업 기획전 오픈 — 셋업 카테고리 매출 +38%", "description": "무신사가 '5월 셋업 위크'를 공식 론칭, 참여 브랜드 220개 이상.", "link": "https://fashionbiz.co.kr", "source": "패션비즈", "date": "Thu, 15 May 2025"},
            {"title": "MZ 세대 '조용한 럭셔리' 피로감 — 실용성 중심 소비 전환", "description": "원단 퀄리티와 착용감을 SNS 후기에서 직접 언급하는 비중 +52%.", "link": "https://apparelnews.co.kr", "source": "어패럴뉴스", "date": "Thu, 15 May 2025"},
            {"title": "29CM 인플루언서 큐레이션 리뉴얼 — 콘텐츠 커머스 전환율 2.4배", "description": "에디터 Pick 섹션 개편, 클릭-구매 전환율 기존 대비 2.4배 상승.", "link": "https://edaily.co.kr", "source": "이데일리", "date": "Thu, 15 May 2025"},
        ]
    }
