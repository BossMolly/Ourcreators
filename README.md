# 📊 Market Dashboard for 247

24/7 series 브랜드를 위한 데일리 패션 마켓 인텔리전스 대시보드

---

## 구조

```
market-dashboard-247/
├── index.html                      # 최종 대시보드 (자동 생성)
├── main.py                         # 전체 파이프라인 실행
├── requirements.txt
├── vercel.json                     # Vercel 배포 설정
├── .env.example                    # 환경변수 템플릿
├── collectors/
│   ├── weather.py                  # OpenWeatherMap API
│   ├── naver.py                    # 네이버 검색 API
│   ├── youtube.py                  # YouTube Data API v3
│   ├── platforms.py                # 무신사·29CM·KREAM·4910 (mock→크롤러 예정)
│   └── instagram.py                # 브랜드 계정 모니터링 (mock→Graph API 예정)
├── analysis/
│   └── claude_analyzer.py          # Claude API 인사이트 생성
├── builder/
│   └── render.py                   # 데이터 → index.html 렌더링
├── data/
│   └── YYYY-MM-DD.json             # 날짜별 수집 데이터 아카이브
└── .github/
    └── workflows/
        └── update-dashboard.yml    # 매일 오전 8시 KST 자동 실행
```

---

## 로컬 실행

### 1. 환경 설정
```bash
cp .env.example .env
# .env 파일에 API 키 입력
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 대시보드 빌드
```bash
python main.py
```
→ `index.html` 생성 완료

---

## Vercel 배포

### 최초 배포
```bash
npm install -g vercel
vercel deploy --prod
```

### 이후 업데이트
```bash
python main.py        # index.html 재생성
vercel deploy --prod  # 배포
```

---

## GitHub Actions 자동화 설정

레포 Settings → Secrets and variables → Actions 에서 아래 키 등록:

| Secret 이름 | 내용 |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API 키 |
| `OPENWEATHER_API_KEY` | OpenWeatherMap 키 |
| `NAVER_CLIENT_ID` | 네이버 Client ID |
| `NAVER_CLIENT_SECRET` | 네이버 Client Secret |
| `YOUTUBE_API_KEY` | YouTube Data API 키 |
| `VERCEL_TOKEN` | Vercel 토큰 |
| `VERCEL_ORG_ID` | Vercel Org ID |
| `VERCEL_PROJECT_ID` | Vercel Project ID |

등록 후 매일 오전 8시 KST 자동 빌드 및 배포.

---

## API 키 발급

| API | 발급처 | 무료 한도 |
|---|---|---|
| Anthropic | console.anthropic.com | $5 크레딧 |
| OpenWeatherMap | openweathermap.org/api | 1,000 calls/day |
| 네이버 검색 | developers.naver.com | 25,000 calls/day |
| YouTube Data v3 | console.cloud.google.com | 10,000 units/day |
| Instagram Graph | developers.facebook.com | 200 calls/hour |

---

## 데이터 수집 범위

- **플랫폼**: 무신사, 29CM, 4910, KREAM, 네이버
- **SNS**: Instagram 브랜드 계정 모니터링
- **콘텐츠**: YouTube, 네이버 블로그·카페
- **날씨**: 서울 실시간 날씨 + 주간 예보
- **커뮤니티**: FM코리아 패션 갤러리

---

## 반응형 지원

| 화면 | 레이아웃 |
|---|---|
| 모바일 (~ 639px) | 1열, 카드형 플랫폼 목록 |
| 태블릿 (640px ~) | 2열 그리드, 테이블 복원 |
| 데스크탑 (1024px ~) | 3열, 풀 레이아웃 |
