import os, json
import anthropic


def generate_insights(data: dict) -> dict:
    """수집된 데이터를 Claude API에 전달해 인사이트를 생성합니다."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("[analyzer] ANTHROPIC_API_KEY 없음 — mock 인사이트 반환")
        return _mock_insights()

    client = anthropic.Anthropic(api_key=api_key)

    prompt = _build_prompt(data)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.content[0].text
        return _parse_response(raw)
    except Exception as e:
        print(f"[analyzer] Claude API 오류: {e}")
        return _mock_insights()


def _build_prompt(data: dict) -> str:
    weather = data.get("weather", {}).get("today", {})
    news    = data.get("naver", {}).get("news", [])
    blogs   = data.get("naver", {}).get("blogs", [])
    yt      = data.get("youtube", [])

    news_text  = "\n".join([f"- {n['title']}: {n['description']}" for n in news[:5]])
    blog_text  = "\n".join([f"- {b['title']}: {b['description']}" for b in blogs[:5]])
    yt_text    = "\n".join([f"- {v['title']}: {v['description']}" for v in yt[:5]])
    wx_text    = f"기온 {weather.get('temp','?')}°C, {weather.get('desc','?')}, 체감 {weather.get('feels_like','?')}°C"

    return f"""당신은 한국 패션 브랜드 '24/7 series'의 마케팅 인텔리전스 AI입니다.
오늘의 데이터를 분석하여 브랜드에게 가장 중요한 인사이트 3개와 액션 아이템 4개를 추출해주세요.

## 오늘 날씨 (서울)
{wx_text}

## 패션 뉴스
{news_text}

## 블로그 트렌드
{blog_text}

## 유튜브 인기 콘텐츠
{yt_text}

## 출력 형식 (JSON만 반환, 다른 텍스트 없이)
{{
  "insights": [
    {{
      "index": "01",
      "source": "출처1 · 출처2",
      "title": "뉴스/트렌드 제목 (30자 이내)",
      "body": "24/7 브랜드 관점에서의 인사이트 (80자 이내)",
      "tags": ["태그1", "태그2"],
      "tag_types": ["trend", "convert"]
    }},
    ...3개
  ],
  "actions": [
    {{
      "type": "content|price|sns|alert",
      "title": "액션 제목 (20자 이내)",
      "desc": "구체적인 실행 방법 (50자 이내)"
    }},
    ...4개
  ],
  "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5", "키워드6", "키워드7", "키워드8"],
  "sentiment": {{"positive": 62, "neutral": 24, "negative": 14}},
  "weather_items": ["추천아이템1", "추천아이템2", "추천아이템3", "추천아이템4"]
}}

tag_types 가능한 값: weather, trend, curate, convert, viral, price, brand"""


def _parse_response(raw: str) -> dict:
    try:
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception as e:
        print(f"[analyzer] JSON 파싱 오류: {e}\n원문: {raw[:200]}")
        return _mock_insights()


def _mock_insights():
    return {
        "insights": [
            {
                "index": "01",
                "source": "WWD Korea · 패션비즈",
                "title": "무신사 5월 셋업 기획전 오픈 — 매출 +38%",
                "body": "셋업 카테고리 전월 대비 매출 38% 급등. 린넨·워시드 소재 집중 노출. 24/7 셋업 라인 진입 적기.",
                "tags": ["트렌드", "전환상승", "매출급등"],
                "tag_types": ["trend", "convert", "price"]
            },
            {
                "index": "02",
                "source": "패션포스트 · 어패럴뉴스",
                "title": "MZ '조용한 럭셔리' 피로 — 실용성 소비 전환",
                "body": "원단 퀄리티·착용감 SNS 후기 언급 비중 +52%. 24/7 루나라이트 소재 스토리텔링 강화 기회.",
                "tags": ["트렌드", "브랜드", "바이럴"],
                "tag_types": ["trend", "brand", "viral"]
            },
            {
                "index": "03",
                "source": "이데일리 · 29CM 블로그",
                "title": "29CM 큐레이션 리뉴얼 — 전환율 2.4배 상승",
                "body": "에디터 Pick 개편 후 클릭-구매 전환율 2.4배. 입점 브랜드 콘텐츠 제공 요청 증가.",
                "tags": ["큐레이션", "전환상승", "플랫폼변화"],
                "tag_types": ["curate", "convert", "weather"]
            }
        ],
        "actions": [
            {"type": "content", "title": "나일론 재킷 레이어드 릴스 발행",   "desc": "비 예보 + 레이어드 급상승. 오후 6~8시 발행 최적."},
            {"type": "price",   "title": "29CM 셋업 가격 대응 검토",          "desc": "경쟁사 -15% 프로모션 감지. 번들 혜택 대안 검토."},
            {"type": "sns",     "title": "@feelslike.seoul 협업 제안",         "desc": "저장 9.2만 · 스타일 싱크 높음. 콜라보 적합 시점."},
            {"type": "alert",   "title": "FM코리아 가격 반응 모니터링",        "desc": "가격 저항 스레드 증가. CS 선제 대응 준비 필요."}
        ],
        "keywords": ["#셋업", "#나일론재킷", "#Y2K", "#레이어드룩", "#가성비아우터", "#린넨팬츠", "#워시드데님", "#캡슐워드로브"],
        "sentiment": {"positive": 62, "neutral": 24, "negative": 14},
        "weather_items": ["린넨 셋업", "코튼 반소매", "크롭 트렌치", "라이트 스니커즈"]
    }
