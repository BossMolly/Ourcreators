import os, json
import anthropic


def generate_insights(data: dict) -> dict:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("[analyzer] API 키 없음 — mock 반환")
        return _mock()

    client = anthropic.Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": _prompt(data)}]
        )
        return _parse(response.content[0].text)
    except Exception as e:
        print(f"[analyzer] 오류: {e}")
        return _mock()


def _prompt(data: dict) -> str:
    weather = data.get("weather", {}).get("today", {})
    news    = data.get("naver", {}).get("news", [])
    blogs   = data.get("naver", {}).get("blogs", [])
    yt      = data.get("youtube", [])

    news_text  = "\n".join(f"- {n['title']}: {n['description']}" for n in news[:5])
    blog_text  = "\n".join(f"- {b['title']}: {b['description']}" for b in blogs[:5])
    yt_text    = "\n".join(f"- {v['title']}: {v['description']}" for v in yt[:5])
    wx_text    = f"기온 {weather.get('temp','?')}°C, {weather.get('desc','?')}"

    return f"""당신은 한국 패션 브랜드 '24/7 series'의 Brand Intelligence AI입니다.
아래 데이터를 분석해 Brand Intelligence Dashboard용 인사이트를 생성하세요.

## 오늘 날씨
{wx_text}

## 패션 뉴스
{news_text}

## 블로그 트렌드
{blog_text}

## 유튜브 인기 콘텐츠
{yt_text}

## 출력 형식 (JSON만 반환, 마크다운 없이)
{{
  "weekly_insight": {{
    "headline_en": "영문 헤드라인 (20단어 이내, 이번 주 소비 무드 핵심)",
    "headline_ko": "한국어 해석 (30자 이내)",
    "highlight_word": "headline_en에서 강조할 단어 1개",
    "consumer_shift": "소비 무드 변화 요약 (40자 이내)",
    "consumer_body": "소비 변화 해석 (80자 이내)",
    "consumer_sub": "영문 + 한국어 서브 문장",
    "mood_tags": ["태그1","태그2","태그3","태그4"],
    "active_tags": ["강조태그1","강조태그2"],
    "declining": "하락 트렌드 키워드",
    "declining_sub": "하락 이유 설명 (60자 이내)",
    "key_mood": "영문 무드 키워드 3개 (· 구분)",
    "key_mood_sub": "무드 설명 (60자 이내)",
    "key_item": "핵심 아이템 3개 (· 구분)",
    "key_item_sub": "아이템 선정 이유 (50자 이내)",
    "rising_brand": "주목 브랜드 3개 (· 구분)",
    "rising_sub": "브랜드 상승 이유 (60자 이내)",
    "styling_mood": "스타일링 무드 변화",
    "styling_sub": "변화 해석 (60자 이내)"
  }},
  "surge_items": [{{"text":"상품/키워드","meta":"플랫폼·수치"}}],
  "surge_pct": "+XX%",
  "soldout_items": [{{"text":"상품명","meta":"플랫폼·상황"}}],
  "soldout_count": "N",
  "new_items": [{{"text":"상품명","meta":"브랜드·플랫폼"}}],
  "new_count": "N",
  "brand_mentions": [
    {{"rank":"1","name":"브랜드","pos":60,"neu":25,"neg":15,"why":"반응 이유"}}
  ],
  "community_keywords": [{{"w":"#키워드","sz":"sz-l|sz-m|sz-s"}}],
  "community_why": "커뮤니티 반응의 본질적 이유 (한 문장, 이탤릭 강조 문장)",
  "actions": [
    {{
      "type": "Content|Platform|Collaboration|Alert",
      "title": "액션 제목 (25자 이내)",
      "desc": "구체적 실행 방법 (60자 이내)",
      "timing": "오늘|이번 주 내|즉시",
      "primary": true
    }}
  ]
}}"""


def _parse(raw: str) -> dict:
    try:
        raw = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(raw)
    except Exception as e:
        print(f"[analyzer] 파싱 오류: {e}")
        return _mock()


def _mock() -> dict:
    return {
        "weekly_insight": {
            "headline_en": "Vintage softness is quietly replacing aggressive gorpcore.",
            "headline_ko": "이번 주 소비 무드는 절제와 자연스러움으로 이동하고 있다.",
            "highlight_word": "replacing",
            "consumer_shift": "잘 꾸민 느낌보다 자연스럽게 멋있는 스타일 선호 증가.",
            "consumer_body": "고프코어 피로감이 가시화되며 빈티지 실루엣과 워시드 소재로의 회귀 조짐이 포착된다. MZ 소비자는 이제 기능보다 무드를 구매한다.",
            "consumer_sub": "Effortless over polished — 이번 주 소비 무드의 핵심 방향.",
            "mood_tags": ["빈티지 실루엣","워시드 소재","고프코어↓","에포트리스"],
            "active_tags": ["빈티지 실루엣","워시드 소재"],
            "declining": "고프코어 · 테크웨어 피로감",
            "declining_sub": "기능성 중심 아이템 체류 시간 감소. 로고·패치 중심 스타일 저장률 하락.",
            "key_mood": "Quiet · Worn-in · Considered",
            "key_mood_sub": "과하지 않은 절제미. 오래 입은 듯한 자연스러움이 감도의 기준으로 이동.",
            "key_item": "워시드 린넨 셋업 · 오버사이즈 셔츠 · 크롭 트러커",
            "key_item_sub": "소재 퀄리티와 실루엣이 구매 결정의 핵심 변수.",
            "rising_brand": "포터리 · 어나더오피스 · 러프사이드",
            "rising_sub": "워크웨어·아카이브 감도 브랜드 커뮤니티 언급 동반 상승.",
            "styling_mood": "레이어드 → 심플 싱글룩으로 전환",
            "styling_sub": "과한 레이어링보다 한 피스가 완성하는 룩. 저장 콘텐츠 패턴 변화 감지."
        },
        "surge_items": [
            {"text":"워시드 린넨 셋업","meta":"무신사 TOP100 신규 진입"},
            {"text":"오버사이즈 체크 셔츠","meta":"29CM 저장 +38% 급증"},
            {"text":"\"빈티지 반팔\" 검색량","meta":"네이버 전주 대비 +61%"},
            {"text":"크롭 트러커 자켓","meta":"KREAM 관심 등록 급증"},
        ],
        "surge_pct": "+42%",
        "soldout_items": [
            {"text":"피그먼트 후드 S·M","meta":"재입고 문의 200건↑"},
            {"text":"실크 블렌드 미디 스커트","meta":"전 사이즈 품절 · 29CM"},
            {"text":"크루넥 피그먼트 스웻","meta":"블랙·그레이 품절 · 4910"},
            {"text":"고프코어 아우터","meta":"클릭률 -18% 하락 감지"},
        ],
        "soldout_count": "3",
        "new_items": [
            {"text":"워크웨어 와이드 팬츠","meta":"커버낫 · 무신사"},
            {"text":"반집업 테크 스웨트","meta":"인사일런스 · 4910"},
            {"text":"세미글로시 메리제인","meta":"페디 · 29CM"},
            {"text":"조던1 로우 OG","meta":"KREAM 신규"},
        ],
        "new_count": "48",
        "brand_mentions": [
            {"rank":"1","name":"포터리","pos":38,"neu":14,"neg":8,"why":"원단·실루엣 칭찬"},
            {"rank":"2","name":"24/7 series","pos":32,"neu":16,"neg":12,"why":"소재↑ 가격 이슈↓"},
            {"rank":"3","name":"쿠어","pos":30,"neu":20,"neg":10,"why":"가성비 데일리"},
            {"rank":"4","name":"아트이프액츠","pos":28,"neu":18,"neg":14,"why":"그래픽·워크웨어"},
            {"rank":"5","name":"어나더오피스","pos":26,"neu":22,"neg":12,"why":"오피스웨어 상승"},
            {"rank":"6","name":"벨리에","pos":24,"neu":20,"neg":16,"why":"시티캐주얼"},
            {"rank":"7","name":"홀리선","pos":22,"neu":18,"neg":20,"why":"가격 이슈 일부"},
            {"rank":"8","name":"인사일런스","pos":20,"neu":24,"neg":16,"why":"신제품 초기 반응"},
        ],
        "community_keywords": [
            {"w":"#빈티지실루엣","sz":"sz-l"},{"w":"#워시드소재","sz":"sz-l"},
            {"w":"#셋업코디","sz":"sz-m"},{"w":"#에포트리스","sz":"sz-m"},
            {"w":"#아카이브무드","sz":"sz-m"},{"w":"#오피스룩","sz":"sz-s"},
            {"w":"#캡슐워드로브","sz":"sz-s"},{"w":"#워크웨어","sz":"sz-m"},
            {"w":"#린넨셋업","sz":"sz-s"},{"w":"#고프코어피로","sz":"sz-l"},
            {"w":"#미니멀데일리","sz":"sz-s"},{"w":"#원단퀄리티","sz":"sz-m"},
        ],
        "community_why": '"소재를 먼저 이야기하고, 브랜드를 나중에 언급한다. 구매 이유가 브랜드에서 소재·실루엣으로 이동 중."',
        "actions": [
            {"type":"Content · Urgent","title":"워시드 소재 중심 릴스 오늘 발행 권장","desc":"빈티지 실루엣 키워드 급상승. 오후 6~8시 발행 시 저장율 최적.","timing":"오늘 오후 6시 전","primary":True},
            {"type":"Platform · Price","title":"29CM 셋업 가격 포지셔닝 재검토","desc":"쿠어 번들 프로모션 감지. 번들 구성으로 차별화 권장.","timing":"이번 주 내","primary":False},
            {"type":"Collaboration","title":"@feelslike.seoul 협업 제안","desc":"48h 저장 9.2만. 스타일 싱크 높음. 콜라보 적기.","timing":"이번 주 DM","primary":False},
            {"type":"Community · Alert","title":"FM코리아 가격 반응 선제 대응","desc":"가격 저항 스레드 3건 감지. 소재 가치 재설명 필요.","timing":"오늘 중","primary":False},
        ]
    }
