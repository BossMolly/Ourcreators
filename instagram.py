"""
브랜드 계정 모니터링 모듈
현재: mock 데이터 (계정 목록 전달 시 실제 데이터로 교체)
추후: Instagram Graph API 연동
"""
import os

# 모니터링할 계정 목록 — 전달받은 계정으로 교체 예정
WATCH_ACCOUNTS = [
    "@247series",
    "@musinsa_official",
    "@29cm_official",
    "@stylenanda",
    "@matinkim_official",
    "@low_classic",
    "@feelslike.seoul",
]


def fetch_brand_accounts():
    token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    if token:
        return _fetch_from_api(token)
    return _mock_accounts()


def _fetch_from_api(token):
    """Instagram Graph API — 비즈니스 계정 전용"""
    import requests
    results = []
    # Graph API는 연결된 비즈니스 계정만 조회 가능
    # 추후 구현 예정
    return _mock_accounts()


def _mock_accounts():
    return [
        {"handle": "@247series",        "summary": "루나라이트 재킷 착샷 릴스 업로드, 좋아요 2,841 · 댓글 134 — 저장율 높음",              "updated": "3h ago",  "likes": 2841, "comments": 134},
        {"handle": "@musinsa_official", "summary": "5월 셋업 기획전 스토리 공지, 스토리 노출 8만 · 링크 클릭율 4.2%",                      "updated": "5h ago",  "likes": 0,    "comments": 0},
        {"handle": "@29cm_official",    "summary": "에디터 Pick 큐레이션 피드 게시, 저장수 4,102 · 클릭 전환 +41%",                          "updated": "7h ago",  "likes": 3200, "comments": 89},
        {"handle": "@stylenanda",       "summary": "Y2K 룩북 피드 6장 업데이트, 좋아요 7,903 · 타 계정 리그램 다수",                        "updated": "10h ago", "likes": 7903, "comments": 228},
        {"handle": "@matinkim_official","summary": "크롭 집업 착샷 캐러셀, 1시간 내 저장 2,200건 · 댓글 내 구매 문의 폭주",               "updated": "1h ago",  "likes": 4100, "comments": 312},
        {"handle": "@low_classic",      "summary": "SS 룩북 피날레 영상 게재, 조회 18만 · 미디 스커트 품절 유발 콘텐츠",                   "updated": "12h ago", "likes": 5600, "comments": 140},
        {"handle": "@feelslike.seoul",  "summary": "레이어드 데일리룩 릴스 바이럴, 48h 저장 9,200건 · 팔로워 유입 +820명",                 "updated": "어제",    "likes": 6800, "comments": 195},
    ]
