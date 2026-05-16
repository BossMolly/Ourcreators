import json
from datetime import datetime
from pathlib import Path


# ── 데이터 매핑 ──────────────────────────────────────────
WX_ICON = {
    "Clear":"ti-sun","Clouds":"ti-cloud","Rain":"ti-cloud-rain",
    "Snow":"ti-snowflake","Thunderstorm":"ti-cloud-storm","Drizzle":"ti-cloud-rain",
}

SIGNAL_CSS = {
    "급등":("up","↑ Surge"),"품절":("down","⊘ Sold Out"),
    "신상품":("new","✦ New"),"가격↓":("down","가격↓"),
    "트렌딩":("hot","◎ Hot"),"HOT":("hot","◎ Hot"),
    "리셀↑":("up","↑ 리셀"),"품절임박":("down","⊘ 품절임박"),
    "신규상장":("new","✦ New"),"검색급등":("up","↑ 검색"),
    "브랜드언급":("hot","◎ 언급"),"모니터":("down","모니터"),
}

COMP_BRANDS = [
    {"brand":"포터리",      "sub":"ptry.co.kr",           "ig":"@pottery_seoul",     "move":"아카이브 릴스 빈도 +40%",          "tag":"콘텐츠↑","tagcls":"cst-up",  "meaning":"장인정신·소재 스토리텔링 강화 — 고감도 소비자 락인 전략"},
    {"brand":"어나더오피스","sub":"anotheroffice.co.kr",   "ig":"@another_office",    "move":"오피스웨어 라인 확장, 여성 노출 확대","tag":"라인확장","tagcls":"cst-new","meaning":"젠더 뉴트럴 오피스웨어 시장 선점 — 직장인 타깃 강화"},
    {"brand":"쿠어",        "sub":"coor.kr",               "ig":"@coor_kr",           "move":"기본템 번들 프로모션 강화",           "tag":"가격전략","tagcls":"cst-shift","meaning":"가성비 포지셔닝 공고화 — 번들로 객단가 방어"},
    {"brand":"COS",         "sub":"cos.com/ko-kr",         "ig":"@cosstores",         "move":"한국 전용 컬러 라인 출시",            "tag":"로컬라이징","tagcls":"cst-new","meaning":"글로벌 미니멀 감도로 도메스틱 시장 직접 공략"},
    {"brand":"ARKET",       "sub":"arket.com/ko-kr",       "ig":"@arketofficial",     "move":"지속가능 소재 캠페인 강화",           "tag":"무드전환","tagcls":"cst-shift","meaning":"가치소비 트렌드 공략 — 친환경 스토리텔링"},
    {"brand":"아트이프액츠","sub":"artifacts.co.kr",       "ig":"@artifacts_kr",      "move":"그래픽 티 라인 확장",                 "tag":"콘텐츠↑","tagcls":"cst-up",  "meaning":"워크웨어→스트리트 피벗 — 20대 남성 외연 확장"},
    {"brand":"유스랩",      "sub":"youth-lab.kr",          "ig":"@youth_lab_kr",      "move":"Y2K 빈티지 협업 · 아이돌 착용 연계", "tag":"바이럴↑","tagcls":"cst-up",  "meaning":"10~20대 팬덤 소비 공략 — 바이럴 의존도 높아짐"},
    {"brand":"벨리에",      "sub":"belier.co.kr",          "ig":"@belier_official",   "move":"시티트립 콘셉트 강화",                "tag":"방향전환","tagcls":"cst-shift","meaning":"여행·레저 시즌 선점 — 무드 중심 포지셔닝"},
    {"brand":"아모멘토",    "sub":"amomento.co",           "ig":"@amomento.co",       "move":"여성 전용 드롭 시스템 도입",          "tag":"구조변화","tagcls":"cst-new","meaning":"희소성 기반 고감도 여성복 포지셔닝 — EQL 채널 강화"},
    {"brand":"솔리드옴므",  "sub":"solidhomme",            "ig":"@solidhomme",        "move":"기본 라인 가격 조정",                 "tag":"가격↓","tagcls":"cst-dn",   "meaning":"볼륨존 진입 시도 — 프리미엄 포지션 약화 모니터링 필요"},
    {"brand":"홀리선",      "sub":"horlisun",              "ig":"@horlisun",          "move":"아카이브 드롭 빈도 감소",             "tag":"전략조정","tagcls":"cst-shift","meaning":"드롭 피로감 인식 — 정규 컬렉션 중심으로 전환"},
    {"brand":"인사일런스",  "sub":"insilence",             "ig":"@insilence_official","move":"4910 익스클루시브 한정 수량 전략",    "tag":"채널전략","tagcls":"cst-new","meaning":"특정 플랫폼 독점 — 희소성·충성도 동시 확보"},
    {"brand":"러프사이드",  "sub":"roughside",             "ig":"@roughside_official","move":"워크웨어 무드 릴스 집중 게시",        "tag":"콘텐츠↑","tagcls":"cst-up",  "meaning":"포터리와 동일 감도 공략 — 워크웨어 시장 경쟁 심화"},
]


# ── 메인 렌더 함수 ────────────────────────────────────────
def render(data: dict, output_path: str = "index.html"):
    now        = datetime.now()
    today      = now.strftime("%Y. %m. %d (%a)")
    updated_at = now.strftime("%H:%M")
    week_num   = now.isocalendar()[1]

    weather   = data.get("weather", {})
    insights  = data.get("insights", {})
    platforms = data.get("platforms", {})
    youtube   = data.get("youtube", [])
    naver     = data.get("naver", {})
    instagram = data.get("instagram", [])

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>24/7 — Brand Intelligence</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&family=Bebas+Neue&family=Libre+Baskerville:ital@1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
{_css()}
</head>
<body>
{_header(today, updated_at, weather)}
<main class="page">
  {_weekly(insights, week_num, now)}
  {_daily_signal(insights, platforms, instagram)}
  {_platform_pulse(platforms)}
  {_community_heat(insights, naver)}
  {_competitor()}
  {_action(insights)}
</main>
{_footer()}
{_scripts()}
</body>
</html>"""

    Path(output_path).write_text(html, encoding="utf-8")
    print(f"[builder] {output_path} 생성 완료")


# ── SECTIONS ─────────────────────────────────────────────

def _header(today, updated_at, weather):
    wx = weather.get("today", {})
    temp = wx.get("temp", "--")
    desc = wx.get("desc", "")
    icon = WX_ICON.get(wx.get("icon",""), "ti-cloud")
    return f"""<header class="hd">
  <div class="hd-brand">24/7 <span>Brand Intelligence</span></div>
  <div class="hd-right">
    <span>{today}</span>
    <div class="hd-wx"><i class="ti {icon}"></i>&nbsp;서울 {temp}° {desc}</div>
  </div>
</header>"""


def _weekly(insights, week_num, now):
    wi = insights.get("weekly_insight", {})
    headline_en = wi.get("headline_en", "Market mood is shifting — quietly but clearly.")
    headline_ko = wi.get("headline_ko", "이번 주 소비 무드는 절제와 자연스러움으로 이동하고 있다.")
    highlight   = wi.get("highlight_word", "shifting")
    headline_en_html = headline_en.replace(highlight, f'<em>{highlight}</em>', 1)

    consumer_shift = wi.get("consumer_shift", "잘 꾸민 느낌보다 자연스럽게 멋있는 스타일 선호 증가.")
    consumer_body  = wi.get("consumer_body",  "고프코어 피로감이 가시화되며 빈티지 실루엣과 워시드 소재로의 회귀 조짐이 포착된다.")
    consumer_sub   = wi.get("consumer_sub",   "Effortless over polished — 이번 주 소비 무드의 핵심 방향.")
    mood_tags      = wi.get("mood_tags",      ["빈티지 실루엣","워시드 소재","고프코어↓","에포트리스"])
    active_tags    = wi.get("active_tags",    ["빈티지 실루엣","워시드 소재"])

    declining      = wi.get("declining",      "고프코어 · 테크웨어 피로감")
    declining_sub  = wi.get("declining_sub",  "기능성 중심 아이템 체류 시간 감소. 로고·패치 중심 스타일 저장률 하락.")
    key_mood       = wi.get("key_mood",       "Quiet · Worn-in · Considered")
    key_mood_sub   = wi.get("key_mood_sub",   "과하지 않은 절제미. 오래 입은 듯한 자연스러움이 감도의 기준으로 이동.")
    key_item       = wi.get("key_item",       "워시드 린넨 셋업 · 오버사이즈 셔츠 · 크롭 트러커")
    key_item_sub   = wi.get("key_item_sub",   "소재 퀄리티와 실루엣이 구매 결정의 핵심 변수.")
    rising_brand   = wi.get("rising_brand",   "포터리 · 어나더오피스 · 러프사이드")
    rising_sub     = wi.get("rising_sub",     "워크웨어·아카이브 감도 브랜드 커뮤니티 언급 동반 상승.")
    styling_mood   = wi.get("styling_mood",   "레이어드 → 심플 싱글룩으로 전환")
    styling_sub    = wi.get("styling_sub",    "과한 레이어링보다 한 피스가 완성하는 룩. 저장 콘텐츠 패턴 변화 감지.")

    month_str = now.strftime("%b %Y").upper()
    tags_html = "".join(
        f'<span class="mood-tag{"  active" if t in active_tags else ""}">{t}</span>'
        for t in mood_tags
    )

    return f"""<section class="weekly-wrap">
  <div class="sec-label">01 — Weekly Insight</div>
  <div class="weekly-header">
    <h1 class="weekly-headline">
      {headline_en_html} —<br>{headline_ko}
    </h1>
    <div class="weekly-date-block">
      <div class="week-num">W {week_num}</div>
      <div class="week-label">{month_str}</div>
    </div>
  </div>
  <div class="weekly-grid">
    <div class="weekly-cell featured">
      <div class="weekly-cell-label">Consumer Shift</div>
      <div class="weekly-cell-text">"{consumer_shift}"<br><br>{consumer_body}</div>
      <div class="weekly-cell-sub">{consumer_sub}</div>
      <div class="mood-tags" style="margin-top:20px;">{tags_html}</div>
    </div>
    <div class="weekly-cell">
      <div class="weekly-cell-label">Declining Trend</div>
      <div class="weekly-cell-text">{declining}</div>
      <div class="weekly-cell-sub">{declining_sub}</div>
    </div>
    <div class="weekly-cell">
      <div class="weekly-cell-label">Key Mood</div>
      <div class="weekly-cell-text">{key_mood}</div>
      <div class="weekly-cell-sub">{key_mood_sub}</div>
    </div>
    <div class="weekly-cell">
      <div class="weekly-cell-label">Key Item</div>
      <div class="weekly-cell-text">{key_item}</div>
      <div class="weekly-cell-sub">{key_item_sub}</div>
    </div>
    <div class="weekly-cell">
      <div class="weekly-cell-label">Rising Brand</div>
      <div class="weekly-cell-text">{rising_brand}</div>
      <div class="weekly-cell-sub">{rising_sub}</div>
    </div>
    <div class="weekly-cell">
      <div class="weekly-cell-label">Styling Mood</div>
      <div class="weekly-cell-text">{styling_mood}</div>
      <div class="weekly-cell-sub">{styling_sub}</div>
    </div>
  </div>
</section>"""


def _daily_signal(insights, platforms, instagram):
    # Surge items
    surge = insights.get("surge_items", [
        {"text":"워시드 린넨 셋업","meta":"무신사 TOP100 신규 진입"},
        {"text":"오버사이즈 체크 셔츠","meta":"29CM 저장 +38% 급증"},
        {"text":"\"빈티지 반팔\" 검색량","meta":"네이버 전주 대비 +61%"},
        {"text":"크롭 트러커 자켓","meta":"KREAM 관심 등록 급증"},
    ])
    surge_num = insights.get("surge_pct", "+42%")

    # Soldout
    soldout = insights.get("soldout_items", [
        {"text":"피그먼트 후드 S·M","meta":"재입고 문의 200건↑"},
        {"text":"실크 블렌드 미디 스커트","meta":"전 사이즈 품절 · 29CM"},
        {"text":"크루넥 피그먼트 스웻","meta":"블랙·그레이 품절 · 4910"},
        {"text":"고프코어 아우터","meta":"클릭률 -18% 하락 감지"},
    ])
    soldout_num = insights.get("soldout_count", "3")

    # New
    new_items = insights.get("new_items", [
        {"text":"워크웨어 와이드 팬츠","meta":"커버낫 · 무신사"},
        {"text":"반집업 테크 스웨트","meta":"인사일런스 · 4910 익스클루시브"},
        {"text":"세미글로시 메리제인","meta":"페디 · 29CM"},
        {"text":"조던1 로우 OG","meta":"KREAM 신규 상장"},
    ])
    new_num = insights.get("new_count", "48")

    # SNS heat
    sns_items = [a for a in instagram[:4]] if instagram else [
        {"handle":"@feelslike.seoul","summary":"레이어드 데일리룩 릴스 · 저장 9.2만"},
        {"handle":"@daily.ootd.kr","summary":"셋업 코디 릴스 · 저장 6.8만"},
        {"handle":"@seoul.minimalist","summary":"캡슐 워드로브 · 저장 5.1만"},
        {"handle":"@musinsa_official","summary":"셋업 기획전 스토리 · 노출 8만"},
    ]
    sns_top = "9.2만"

    def items_html(items, key_text="text", key_meta="meta"):
        out = ""
        for it in items[:4]:
            t = it.get(key_text) or it.get("handle","")
            m = it.get(key_meta) or it.get("summary","")
            out += f"""<div class="signal-item">
          <span class="signal-dot"></span>
          <div><div class="signal-text">{t}</div><div class="signal-meta">{m}</div></div>
        </div>"""
        return out

    return f"""<section class="signal-wrap">
  <div class="sec-label">02 — Daily Signal</div>
  <div class="signal-grid">
    <div class="signal-cell up">
      <div class="signal-type">↑ Surge</div>
      <div class="signal-num">{surge_num}</div>
      <div class="signal-caption">셔츠 카테고리 · 전일 대비</div>
      {items_html(surge)}
    </div>
    <div class="signal-cell down">
      <div class="signal-type">⊘ Sold Out</div>
      <div class="signal-num">{soldout_num}</div>
      <div class="signal-caption">품절 발생 · 오늘 기준</div>
      {items_html(soldout)}
    </div>
    <div class="signal-cell new">
      <div class="signal-type">✦ New Entry</div>
      <div class="signal-num">{new_num}</div>
      <div class="signal-caption">오늘 신규 등록 상품</div>
      {items_html(new_items)}
    </div>
    <div class="signal-cell hot">
      <div class="signal-type">◎ SNS Heat</div>
      <div class="signal-num">{sns_top}</div>
      <div class="signal-caption">최고 저장 릴스 · 48h</div>
      {items_html(sns_items, key_text="handle", key_meta="summary")}
    </div>
  </div>
</section>"""


def _platform_pulse(platforms):
    cells = [
        {"name":"Musinsa","rows":[("메인 기획전","5월 셋업 위크"),("강조 카테고리","셋업 · 워크웨어"),("컬러 톤","워시드 · 뉴트럴"),("노출 실루엣","오버사이즈 · 와이드")],"mood":'"빈티지·워크웨어 감도 강화"'},
        {"name":"29CM",   "rows":[("에디터 픽","감각적 데일리룩"),("강조 카테고리","라이프스타일 협업"),("컬러 톤","크림 · 오프화이트"),("노출 실루엣","미디 · 크롭")],"mood":'"라이프스타일 감도 확대 — 콘텐츠 커머스 강화"'},
        {"name":"KREAM",  "rows":[("리셀 강세","삼바 OG · 1906R"),("신규 관심","콜라보 아이템"),("가격 방향","빈티지 스니커↑"),("분위기","빈티지 · 아이돌 콜라보")],"mood":'"콜라보·아이돌 연동 수요 급증"'},
        {"name":"W Concept","rows":[("메인 무드","페미닌 미니멀"),("강조 카테고리","드레스 · 스커트"),("컬러 톤","소프트 뉴트럴"),("노출 실루엣","미디 · 플리츠")],"mood":'"여성 디자이너 브랜드 큐레이션 강화"'},
        {"name":"EQL",    "rows":[("메인 무드","하이엔드 도메스틱"),("강조 카테고리","리미티드 드롭"),("컬러 톤","모노크롬 · 어스톤"),("분위기","희소성 · 아카이브")],"mood":'"드롭 방식 강화 — 희소성 기반 소비 자극"'},
    ]
    cells_html = ""
    for c in cells:
        rows = "".join(f'<div class="platform-row"><div class="platform-row-label">{l}</div><div class="platform-row-val">{v}</div></div>' for l,v in c["rows"])
        cells_html += f"""<div class="platform-cell">
      <div class="platform-name">{c["name"]}</div>
      {rows}
      <div class="platform-mood">{c["mood"]}</div>
    </div>"""

    return f"""<section class="platform-wrap">
  <div class="sec-label">03 — Platform Pulse</div>
  <div class="platform-grid">{cells_html}</div>
</section>"""


def _community_heat(insights, naver):
    mentions = insights.get("brand_mentions", [
        {"rank":"1","name":"포터리",      "pos":38,"neu":14,"neg":8, "why":"원단·실루엣 칭찬"},
        {"rank":"2","name":"24/7 series", "pos":32,"neu":16,"neg":12,"why":"소재↑ 가격 이슈↓"},
        {"rank":"3","name":"쿠어",        "pos":30,"neu":20,"neg":10,"why":"가성비 데일리 언급"},
        {"rank":"4","name":"아트이프액츠","pos":28,"neu":18,"neg":14,"why":"그래픽·워크웨어 관심"},
        {"rank":"5","name":"어나더오피스","pos":26,"neu":22,"neg":12,"why":"오피스웨어 감도 상승"},
        {"rank":"6","name":"벨리에",      "pos":24,"neu":20,"neg":16,"why":"시티캐주얼 언급"},
        {"rank":"7","name":"홀리선",      "pos":22,"neu":18,"neg":20,"why":"가격 이슈 일부"},
        {"rank":"8","name":"인사일런스",  "pos":20,"neu":24,"neg":16,"why":"신제품 초기 반응"},
    ])
    keywords = insights.get("community_keywords", [
        {"w":"#빈티지실루엣","sz":"sz-l"},{"w":"#워시드소재","sz":"sz-l"},
        {"w":"#셋업코디","sz":"sz-m"},   {"w":"#에포트리스","sz":"sz-m"},
        {"w":"#아카이브무드","sz":"sz-m"},{"w":"#오피스룩","sz":"sz-s"},
        {"w":"#캡슐워드로브","sz":"sz-s"},{"w":"#워크웨어","sz":"sz-m"},
        {"w":"#린넨셋업","sz":"sz-s"},   {"w":"#고프코어피로","sz":"sz-l"},
        {"w":"#미니멀데일리","sz":"sz-s"},{"w":"#원단퀄리티","sz":"sz-m"},
    ])
    why_quote = insights.get("community_why", '"소재를 먼저 이야기하고, 브랜드를 나중에 언급한다. 구매 이유가 브랜드에서 소재·실루엣으로 이동 중."')

    mentions_html = ""
    for m in mentions:
        total = m["pos"] + m["neu"] + m["neg"]
        pp = round(m["pos"]/total*60); np = round(m["neu"]/total*60*0.5); ngp = 60-pp-np
        mentions_html += f"""<div class="comm-brand-row">
        <span class="comm-rank">{m["rank"]}</span>
        <span class="comm-brand-name">{m["name"]}</span>
        <div class="comm-sentiment">
          <div class="sent-pip sent-pos" style="width:{pp}px"></div>
          <div class="sent-pip sent-neu" style="width:{np}px"></div>
          <div class="sent-pip sent-neg" style="width:{ngp}px"></div>
        </div>
        <span class="comm-why">{m["why"]}</span>
      </div>"""

    kw_html = "".join(f'<span class="kw {k["sz"]}">{k["w"]}</span>' for k in keywords)

    return f"""<section class="community-wrap">
  <div class="sec-label">04 — Community Heat</div>
  <div class="community-grid">
    <div class="community-cell">
      <div class="sec-label" style="margin-bottom:14px;">Brand Mention Top 8</div>
      <div class="comm-brand-list">{mentions_html}</div>
    </div>
    <div class="community-cell">
      <div class="sec-label" style="margin-bottom:14px;">반복 키워드 · 언급 맥락</div>
      <div class="keyword-cloud">{kw_html}</div>
      <div style="margin-top:20px;padding-top:16px;border-top:.5px solid var(--divider);">
        <div class="sec-label" style="margin-bottom:10px;">왜 반응하는가</div>
        <div class="why-quote">{why_quote}</div>
      </div>
    </div>
  </div>
</section>"""


def _competitor():
    rows_html = ""
    for c in COMP_BRANDS:
        rows_html += f"""<tr>
      <td><div class="comp-brand">{c["brand"]}</div><div class="comp-brand-sub">{c["ig"]}</div></td>
      <td>{c["move"]}</td>
      <td><span class="comp-signal-tag {c["tagcls"]}">{c["tag"]}</span></td>
      <td class="comp-meaning">{c["meaning"]}</td>
    </tr>"""

    return f"""<section class="competitor-wrap">
  <div class="sec-label">05 — Competitor Movement</div>
  <table class="comp-table">
    <thead><tr>
      <th style="width:14%">Brand</th>
      <th style="width:26%">Movement</th>
      <th style="width:10%">Signal</th>
      <th>전략적 의미</th>
    </tr></thead>
    <tbody>{rows_html}</tbody>
  </table>
</section>"""


def _action(insights):
    actions = insights.get("actions", [
        {"type":"Content · Urgent","title":"워시드 소재 중심 릴스 오늘 발행 권장","desc":"빈티지 실루엣 키워드 급상승 + 비 예보로 레이어드룩 수요 동시 상승. 오후 6~8시 발행 시 저장율 최적.","timing":"오늘 오후 6시 전","primary":True},
        {"type":"Platform · Price","title":"29CM 셋업 가격 포지셔닝 재검토","desc":"쿠어 번들 프로모션 감지. 동일 가격대 경쟁 심화 전 번들 구성으로 차별화 권장.","timing":"이번 주 내","primary":False},
        {"type":"Collaboration","title":"@feelslike.seoul 협업 제안","desc":"48h 저장 9.2만. 24/7 소재 무드와 스타일 싱크 높음. 콜라보 제안 적기.","timing":"이번 주 DM 발송","primary":False},
        {"type":"Community · Alert","title":"FM코리아 가격 반응 선제 대응","desc":"가격 저항 스레드 3건 감지. 소재 퀄리티 스토리텔링으로 가치 재설명 필요.","timing":"오늘 중 모니터링","primary":False},
    ])

    cells_html = ""
    for i, act in enumerate(actions[:4]):
        pri = act.get("primary", i == 0)
        cls = "action-cell primary" if pri else "action-cell"
        num = str(i + 1).zfill(2)
        cells_html += f"""<div class="{cls}">
      <div class="action-priority">{num}</div>
      <div class="action-type">{act["type"]}</div>
      <div class="action-title">{act["title"]}</div>
      <div class="action-desc">{act["desc"]}</div>
      <div class="action-timing"><i class="ti ti-clock"></i> {act["timing"]}</div>
    </div>"""

    return f"""<section class="action-wrap">
  <div class="sec-label">06 — Action Suggestion</div>
  <div class="action-header">
    <h2 class="action-headline">Today, what should we do?</h2>
    <span class="action-subline">오늘 실행 가능한 액션 · 우선순위 순</span>
  </div>
  <div class="action-grid">{cells_html}</div>
</section>"""


def _footer():
    updated = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""<footer class="footer">
  <div class="footer-brand">24/7 Brand Intelligence</div>
  <div>수집: 무신사 · 29CM · KREAM · W Concept · EQL · Instagram · YouTube · 네이버 · FM코리아</div>
  <div>업데이트: {updated}</div>
</footer>"""


def _scripts():
    return """<script>
const now = new Date();
const days = ['일','월','화','수','목','금','토'];
const d = document.getElementById('hd-date');
if(d) d.textContent = `${now.getFullYear()}. ${String(now.getMonth()+1).padStart(2,'0')}. ${String(now.getDate()).padStart(2,'0')} (${days[now.getDay()]})`;

// 섹션 페이드인
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if(e.isIntersecting){
      e.target.style.opacity='1';
      e.target.style.transform='translateY(0)';
    }
  });
},{threshold:0.04});
document.querySelectorAll('section').forEach(s=>{
  s.style.opacity='0';
  s.style.transform='translateY(14px)';
  s.style.transition='opacity .5s ease, transform .5s ease';
  obs.observe(s);
});
</script>"""


# ── CSS ──────────────────────────────────────────────────
def _css():
    return """<style>
:root{
  --cream:#f2ede6;--cream-d:#e8e1d6;--warm-gray:#8c8278;
  --ink:#1c1a17;--ink-light:#3d3830;--burgundy:#6b2737;
  --olive:#4a5240;--dusty-navy:#2d3a4a;--sand:#c4b89a;
  --muted:#a09588;--divider:#d6cfc4;--card-bg:#faf7f3;
  --signal-hot:#8c5a1a;
}
*{box-sizing:border-box;margin:0;padding:0;}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;}
body{font-family:'DM Sans',sans-serif;font-weight:400;color:var(--ink);background:var(--cream);min-height:100vh;line-height:1.5;}
.hd{background:var(--ink);color:var(--cream);padding:14px 32px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:200;}
.hd-brand{font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:.15em;color:var(--cream);}
.hd-brand span{font-family:'DM Sans',sans-serif;font-weight:300;font-size:11px;letter-spacing:.12em;color:var(--muted);margin-left:14px;text-transform:uppercase;}
.hd-right{display:flex;align-items:center;gap:16px;font-size:11px;color:var(--muted);font-weight:300;letter-spacing:.05em;}
.hd-wx{display:flex;align-items:center;gap:5px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:4px 12px;color:var(--cream);font-size:11px;}
.page{padding:0 32px 60px;}
.sec-label{font-size:9px;font-weight:500;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);display:flex;align-items:center;gap:8px;margin-bottom:20px;}
.sec-label::after{content:'';flex:1;height:.5px;background:var(--divider);}

/* WEEKLY */
.weekly-wrap{padding:40px 0 36px;border-bottom:1px solid var(--divider);}
.weekly-header{display:flex;align-items:flex-end;justify-content:space-between;gap:32px;margin-bottom:32px;}
.weekly-headline{font-family:'DM Sans',sans-serif;font-size:clamp(20px,2.2vw,28px);font-weight:300;line-height:1.5;color:var(--ink-light);letter-spacing:-.01em;max-width:640px;}
.weekly-headline em{font-style:normal;font-weight:500;color:var(--burgundy);}
.weekly-date-block{text-align:right;flex-shrink:0;padding-bottom:2px;}
.week-num{font-family:'DM Sans',sans-serif;font-weight:300;font-size:24px;line-height:1;color:var(--muted);letter-spacing:.08em;}
.week-label{font-size:9px;letter-spacing:.14em;color:var(--muted);text-transform:uppercase;margin-top:5px;opacity:.7;}
.weekly-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:1px;background:var(--divider);border:1px solid var(--divider);}
.weekly-cell{background:var(--cream);padding:24px 28px;}
.weekly-cell.featured{background:var(--ink);color:var(--cream);grid-row:span 2;}
.weekly-cell-label{font-size:9px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:12px;}
.weekly-cell.featured .weekly-cell-label{color:var(--sand);}
.weekly-cell-text{font-family:'DM Sans',sans-serif;font-size:14px;line-height:1.6;color:var(--ink-light);font-weight:400;}
.weekly-cell.featured .weekly-cell-text{font-size:15px;color:var(--cream);line-height:1.65;}
.weekly-cell-sub{font-size:11.5px;color:var(--muted);margin-top:8px;font-weight:300;line-height:1.55;}
.weekly-cell.featured .weekly-cell-sub{color:var(--sand);}
.mood-tags{display:flex;flex-wrap:wrap;gap:6px;}
.mood-tag{font-size:10px;font-weight:500;letter-spacing:.05em;padding:4px 10px;border:1px solid rgba(255,255,255,.15);border-radius:2px;color:var(--sand);background:rgba(255,255,255,.06);}
.mood-tag.active{background:var(--burgundy);color:var(--cream);border-color:var(--burgundy);}

/* SIGNAL */
.signal-wrap{padding:48px 0;border-bottom:1px solid var(--divider);}
.signal-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--divider);border:1px solid var(--divider);}
.signal-cell{background:var(--card-bg);padding:20px 22px;position:relative;overflow:hidden;}
.signal-cell::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.signal-cell.up::before{background:var(--olive);}
.signal-cell.down::before{background:var(--burgundy);}
.signal-cell.new::before{background:var(--dusty-navy);}
.signal-cell.hot::before{background:var(--signal-hot);}
.signal-type{font-size:9px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;margin-bottom:8px;}
.signal-cell.up .signal-type{color:var(--olive);}
.signal-cell.down .signal-type{color:var(--burgundy);}
.signal-cell.new .signal-type{color:var(--dusty-navy);}
.signal-cell.hot .signal-type{color:var(--signal-hot);}
.signal-num{font-family:'Bebas Neue',sans-serif;font-size:28px;line-height:1;margin-bottom:2px;}
.signal-cell.up .signal-num{color:var(--olive);}
.signal-cell.down .signal-num{color:var(--burgundy);}
.signal-cell.new .signal-num{color:var(--dusty-navy);}
.signal-cell.hot .signal-num{color:var(--signal-hot);}
.signal-caption{font-size:10px;color:var(--muted);font-weight:300;margin-bottom:12px;}
.signal-item{display:flex;align-items:flex-start;gap:8px;padding:7px 0;border-bottom:.5px solid var(--divider);}
.signal-item:last-child{border-bottom:none;}
.signal-dot{width:5px;height:5px;border-radius:50%;flex-shrink:0;margin-top:5px;}
.signal-cell.up .signal-dot{background:var(--olive);}
.signal-cell.down .signal-dot{background:var(--burgundy);}
.signal-cell.new .signal-dot{background:var(--dusty-navy);}
.signal-cell.hot .signal-dot{background:var(--signal-hot);}
.signal-text{font-size:12px;color:var(--ink-light);line-height:1.4;}
.signal-meta{font-size:10px;color:var(--muted);font-weight:300;margin-top:2px;}

/* PLATFORM */
.platform-wrap{padding:48px 0;border-bottom:1px solid var(--divider);}
.platform-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--divider);border:1px solid var(--divider);}
.platform-cell{background:var(--card-bg);padding:22px 20px;}
.platform-name{font-family:'Bebas Neue',sans-serif;font-size:20px;letter-spacing:.08em;color:var(--ink);margin-bottom:14px;padding-bottom:12px;border-bottom:.5px solid var(--divider);}
.platform-row{padding:6px 0;border-bottom:.5px solid var(--divider);}
.platform-row:last-of-type{border-bottom:none;}
.platform-row-label{font-size:9px;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:3px;}
.platform-row-val{font-size:12px;color:var(--ink-light);line-height:1.4;}
.platform-mood{margin-top:12px;font-size:11.5px;font-style:italic;color:var(--warm-gray);line-height:1.5;padding-top:10px;border-top:.5px solid var(--divider);}

/* COMMUNITY */
.community-wrap{padding:48px 0;border-bottom:1px solid var(--divider);}
.community-grid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--divider);border:1px solid var(--divider);}
.community-cell{background:var(--card-bg);padding:24px 26px;}
.comm-brand-list{display:flex;flex-direction:column;}
.comm-brand-row{display:flex;align-items:center;gap:10px;padding:9px 0;border-bottom:.5px solid var(--divider);}
.comm-brand-row:last-child{border-bottom:none;}
.comm-rank{font-family:'Bebas Neue',sans-serif;font-size:18px;color:var(--sand);width:22px;flex-shrink:0;line-height:1;}
.comm-brand-name{font-size:13px;font-weight:500;color:var(--ink);flex:1;}
.comm-sentiment{display:flex;gap:3px;align-items:center;}
.sent-pip{height:4px;border-radius:2px;}
.sent-pos{background:var(--olive);}
.sent-neg{background:var(--burgundy);}
.sent-neu{background:var(--divider);}
.comm-why{font-size:10px;color:var(--muted);font-weight:300;margin-left:auto;text-align:right;max-width:110px;line-height:1.35;flex-shrink:0;}
.keyword-cloud{display:flex;flex-wrap:wrap;gap:7px;}
.kw{font-size:11px;font-weight:500;padding:5px 12px;border:1px solid var(--divider);border-radius:2px;color:var(--ink-light);background:var(--cream);cursor:default;}
.kw.sz-l{font-size:14px;border-color:var(--sand);color:var(--ink);}
.kw.sz-m{font-size:12px;}
.kw.sz-s{font-size:10px;color:var(--muted);}
.why-quote{font-style:italic;font-size:13px;color:var(--warm-gray);line-height:1.7;}

/* COMPETITOR */
.competitor-wrap{padding:48px 0;border-bottom:1px solid var(--divider);}
.comp-table{width:100%;border-collapse:collapse;}
.comp-table thead tr{border-bottom:1px solid var(--ink);}
.comp-table th{font-size:9px;font-weight:500;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);padding:0 0 10px;text-align:left;}
.comp-table tbody tr{border-bottom:.5px solid var(--divider);}
.comp-table tbody tr:hover{background:var(--cream-d);}
.comp-table td{padding:13px 0;font-size:12px;color:var(--ink-light);vertical-align:top;padding-right:16px;}
.comp-brand{font-weight:500;color:var(--ink);font-size:13px;}
.comp-brand-sub{font-size:10px;color:var(--muted);font-weight:300;margin-top:2px;}
.comp-signal-tag{font-size:10px;font-weight:500;letter-spacing:.04em;padding:3px 8px;border-radius:2px;display:inline-block;}
.cst-up{background:#e8f0e4;color:var(--olive);}
.cst-dn{background:#f5e8ea;color:var(--burgundy);}
.cst-new{background:#e4eaf0;color:var(--dusty-navy);}
.cst-shift{background:#f0ece4;color:var(--warm-gray);}
.comp-meaning{font-size:11.5px;color:var(--warm-gray);font-style:italic;line-height:1.5;}

/* ACTION */
.action-wrap{padding:48px 0;}
.action-header{display:flex;align-items:baseline;gap:20px;margin-bottom:28px;}
.action-headline{font-family:'DM Sans',sans-serif;font-size:22px;font-weight:300;color:var(--ink);letter-spacing:-.01em;}
.action-subline{font-size:10px;color:var(--muted);letter-spacing:.08em;}
.action-grid{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:1px;background:var(--divider);border:1px solid var(--divider);}
.action-cell{background:var(--card-bg);padding:24px 22px;position:relative;}
.action-cell.primary{background:var(--ink);grid-column:span 2;}
.action-priority{font-family:'Bebas Neue',sans-serif;font-size:44px;line-height:1;color:var(--divider);position:absolute;top:14px;right:16px;opacity:.35;}
.action-cell.primary .action-priority{color:var(--warm-gray);opacity:.25;}
.action-type{font-size:9px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:10px;}
.action-cell.primary .action-type{color:var(--sand);}
.action-title{font-size:14px;font-weight:500;color:var(--ink);line-height:1.4;margin-bottom:8px;}
.action-cell.primary .action-title{font-size:16px;color:var(--cream);line-height:1.45;font-weight:400;}
.action-desc{font-size:11.5px;color:var(--muted);line-height:1.55;font-weight:300;}
.action-cell.primary .action-desc{color:var(--sand);}
.action-timing{margin-top:12px;font-size:10px;font-weight:500;letter-spacing:.06em;color:var(--olive);display:flex;align-items:center;gap:4px;}
.action-cell.primary .action-timing{color:#7dc4a0;}

/* FOOTER */
.footer{background:var(--ink);color:var(--muted);padding:20px 32px;display:flex;justify-content:space-between;align-items:center;font-size:10px;letter-spacing:.06em;font-weight:300;}
.footer-brand{font-family:'Bebas Neue',sans-serif;font-size:14px;color:var(--sand);letter-spacing:.12em;}

/* RESPONSIVE */
@media(max-width:1024px){
  .page{padding:0 22px 48px;}
  .hd{padding:12px 22px;}
  .weekly-grid{grid-template-columns:1fr 1fr;}
  .weekly-cell.featured{grid-row:span 1;grid-column:span 2;}
  .signal-grid{grid-template-columns:1fr 1fr;}
  .platform-grid{grid-template-columns:1fr 1fr 1fr;}
  .action-grid{grid-template-columns:1fr 1fr;}
  .action-cell.primary{grid-column:span 2;}
}
@media(max-width:640px){
  .page{padding:0 16px 40px;}
  .hd{padding:11px 16px;}
  .hd-brand span{display:none;}
  .weekly-grid{grid-template-columns:1fr;}
  .weekly-cell.featured{grid-column:span 1;}
  .signal-grid,.platform-grid,.action-grid{grid-template-columns:1fr;}
  .action-cell.primary{grid-column:span 1;}
  .community-grid{grid-template-columns:1fr;}
  .comp-table td:nth-child(3){display:none;}
  .footer{flex-direction:column;gap:6px;text-align:center;padding:16px;}
}
</style>"""
