"""
Phase 1-B: FM코리아 패션 갤러리 크롤러
- 패션 갤러리 인기 게시물 수집
- 브랜드 언급 추출
- 긍정/부정 맥락 샘플 수집
"""
import re, time
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Referer": "https://www.fmkorea.com/",
}

# 모니터링 대상 브랜드 키워드
BRAND_KEYWORDS = {
    "24/7": ["24/7", "247series", "이사칠"],
    "포터리": ["포터리", "pottery", "ptry"],
    "어나더오피스": ["어나더오피스", "another office", "anotheroffice"],
    "쿠어": ["쿠어", "coor"],
    "아트이프액츠": ["아트이프액츠", "artifacts", "아티팩츠"],
    "유스랩": ["유스랩", "youth lab", "youthlab"],
    "벨리에": ["벨리에", "belier"],
    "인사일런스": ["인사일런스", "insilence"],
    "홀리선": ["홀리선", "horlisun"],
    "러프사이드": ["러프사이드", "roughside"],
    "아모멘토": ["아모멘토", "amomento"],
    "솔리드옴므": ["솔리드옴므", "solid homme"],
    "마뗑킴": ["마뗑킴", "matin kim"],
    "무신사": ["무신사"],
}

# 감성 키워드
POSITIVE_KW = ["좋다","최고","추천","예쁘","갓","레전드","완벽","마음에","사고싶","사야","퀄리티","소재","핏","좋음"]
NEGATIVE_KW = ["별로","비싸","가격","아쉽","실망","구리","불편","안좋","노","별로","이상","짭","짝퉁","값어치"]

FM_FASHION_URL = "https://www.fmkorea.com/index.php?mid=fashion&sort_index=pop&order_type=desc"


def fetch_fmkorea() -> dict:
    """FM코리아 패션 갤러리 크롤링"""
    if not REQUESTS_OK:
        return _mock_fm()
    try:
        resp = requests.get(FM_FASHION_URL, headers=HEADERS, timeout=12)
        if resp.status_code != 200:
            print(f"[fmkorea] HTTP {resp.status_code}")
            return _mock_fm()

        soup = BeautifulSoup(resp.text, "html.parser")
        posts = soup.select(".li.li_best2_pop0, .hotdeal_var8 li, article.ek-article")

        if not posts:
            # 대안 셀렉터 시도
            posts = soup.select("li.li_best2_pop0") or soup.select(".bd_lst_wrp li")

        raw_posts = []
        for post in posts[:30]:
            title_el = post.select_one(".title, .hotdeal_info strong, h3, h4")
            title = title_el.get_text(strip=True) if title_el else ""
            if not title or len(title) < 5:
                continue
            raw_posts.append(title)

        if not raw_posts:
            print("[fmkorea] 파싱 실패 — mock 반환")
            return _mock_fm()

        return _analyze(raw_posts)

    except Exception as e:
        print(f"[fmkorea] 크롤링 실패: {e}")
        return _mock_fm()


def _analyze(posts: list) -> dict:
    """브랜드 언급 분석"""
    brand_data = {b: {"count": 0, "positive": [], "negative": [], "context": []}
                  for b in BRAND_KEYWORDS}

    for text in posts:
        text_l = text.lower()
        for brand, keywords in BRAND_KEYWORDS.items():
            if any(kw.lower() in text_l for kw in keywords):
                brand_data[brand]["count"] += 1
                brand_data[brand]["context"].append(text[:60])
                # 감성 분류
                pos = sum(kw in text_l for kw in POSITIVE_KW)
                neg = sum(kw in text_l for kw in NEGATIVE_KW)
                if pos > neg:
                    brand_data[brand]["positive"].append(text[:40])
                elif neg > pos:
                    brand_data[brand]["negative"].append(text[:40])

    # 언급량 기준 정렬
    sorted_brands = sorted(
        [(b, d) for b, d in brand_data.items() if d["count"] > 0],
        key=lambda x: x[1]["count"], reverse=True
    )

    mentions = []
    for rank, (brand, d) in enumerate(sorted_brands[:10], 1):
        total = max(d["count"], 1)
        pos_n = len(d["positive"])
        neg_n = len(d["negative"])
        neu_n = total - pos_n - neg_n
        mentions.append({
            "rank": str(rank),
            "name": brand,
            "count": d["count"],
            "pos": max(20, int(pos_n / total * 60)),
            "neu": max(10, int(neu_n / total * 60 * 0.5)),
            "neg": max(8,  int(neg_n / total * 60)),
            "why": _summarize_why(d),
            "positive_samples": d["positive"][:2],
            "negative_samples": d["negative"][:2],
            "context": d["context"][:3],
        })

    # 키워드 추출
    all_text = " ".join(posts)
    keywords = _extract_keywords(all_text)

    return {
        "mentions": mentions,
        "keywords": keywords,
        "post_count": len(posts),
        "crawled_at": datetime.now().isoformat()
    }


def _summarize_why(d: dict) -> str:
    if d["positive"] and not d["negative"]:
        return "긍정 반응 우세"
    if d["negative"] and not d["positive"]:
        return "부정 반응 감지"
    if d["positive"]:
        sample = d["positive"][0][:15]
        return f'"{sample}..." 언급'
    return "언급 감지"


def _extract_keywords(text: str) -> list:
    """패션 관련 키워드 빈도 추출"""
    fashion_terms = [
        "빈티지","워시드","셋업","린넨","나일론","오버사이즈","아카이브",
        "워크웨어","고프코어","미니멀","레이어드","크롭","와이드","피그먼트",
        "에포트리스","Y2K","그래픽","캐주얼","스트리트","오피스룩"
    ]
    counts = {}
    text_l = text.lower()
    for term in fashion_terms:
        cnt = text_l.count(term.lower())
        if cnt > 0:
            counts[term] = cnt

    sorted_kw = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    result = []
    for i, (kw, cnt) in enumerate(sorted_kw[:12]):
        sz = "sz-l" if i < 3 else ("sz-m" if i < 7 else "sz-s")
        result.append({"w": f"#{kw}", "sz": sz})
    return result


def _mock_fm() -> dict:
    return {
        "mentions": [
            {"rank":"1","name":"포터리",       "count":8,"pos":38,"neu":14,"neg":8, "why":"원단·실루엣 칭찬","positive_samples":["원단이 진짜 좋다","핏이 완벽함"],"negative_samples":[],"context":["포터리 신상 어때요?","포터리 워크셔츠 추천"]},
            {"rank":"2","name":"24/7",          "count":6,"pos":32,"neu":16,"neg":12,"why":"소재↑ 가격 이슈↓","positive_samples":["소재 퀄리티 좋음"],"negative_samples":["가격이 좀 세다"],"context":["24/7 시리즈 어때요","247 원단 퀄리티"]},
            {"rank":"3","name":"쿠어",          "count":5,"pos":30,"neu":20,"neg":10,"why":"가성비 데일리","positive_samples":["가성비 최고"],"negative_samples":[],"context":["쿠어 데일리 추천"]},
            {"rank":"4","name":"아트이프액츠",  "count":4,"pos":28,"neu":18,"neg":14,"why":"그래픽·워크웨어","positive_samples":["그래픽 감각 있음"],"negative_samples":[],"context":["아트이프액츠 그래픽티"]},
            {"rank":"5","name":"어나더오피스",  "count":4,"pos":26,"neu":22,"neg":12,"why":"오피스웨어 감도","positive_samples":["오피스룩에 딱"],"negative_samples":[],"context":["어나더오피스 치노"]},
            {"rank":"6","name":"벨리에",        "count":3,"pos":24,"neu":20,"neg":16,"why":"시티캐주얼","positive_samples":[],"negative_samples":["가격 대비"],"context":["벨리에 여름 컬렉션"]},
            {"rank":"7","name":"홀리선",        "count":3,"pos":22,"neu":18,"neg":20,"why":"가격 이슈","positive_samples":[],"negative_samples":["너무 비쌈"],"context":["홀리선 드롭"]},
            {"rank":"8","name":"인사일런스",    "count":2,"pos":20,"neu":24,"neg":16,"why":"신제품 반응","positive_samples":["퀄리티 좋네"],"negative_samples":[],"context":["인사일런스 신상"]},
        ],
        "keywords": [
            {"w":"#빈티지실루엣","sz":"sz-l"},{"w":"#워시드소재","sz":"sz-l"},
            {"w":"#셋업코디","sz":"sz-m"},{"w":"#에포트리스","sz":"sz-m"},
            {"w":"#아카이브무드","sz":"sz-m"},{"w":"#오피스룩","sz":"sz-s"},
            {"w":"#캡슐워드로브","sz":"sz-s"},{"w":"#워크웨어","sz":"sz-m"},
            {"w":"#고프코어피로","sz":"sz-l"},{"w":"#원단퀄리티","sz":"sz-s"},
        ],
        "post_count": 30,
        "crawled_at": datetime.now().isoformat()
    }
