import json
from datetime import datetime
from pathlib import Path


SIGNAL_TAG = {
    "급등":    ("ptag-up",    "급등↑"),
    "품절":    ("ptag-sold",  "품절"),
    "신상품":  ("ptag-new",   "신상품"),
    "가격↓":   ("ptag-drop",  "가격↓"),
    "트렌딩":  ("ptag-trend", "트렌딩"),
    "모니터":  ("ptag-watch", "모니터링"),
    "HOT":     ("ptag-hot",   "HOT"),
    "리셀↑":   ("ptag-up",    "리셀↑"),
    "품절임박":("ptag-sold",  "품절임박"),
    "신규상장":("ptag-new",   "신규상장"),
    "검색급등":("ptag-up",    "검색급등"),
    "브랜드언급":("ptag-trend","브랜드언급"),
    "신규유입":("ptag-new",   "신규유입"),
}

IT_CLASS = {
    "weather": "it-weather",
    "trend":   "it-trend",
    "curate":  "it-curate",
    "convert": "it-convert",
    "viral":   "it-viral",
    "price":   "it-price",
    "brand":   "it-brand",
}

TAG_LABEL = {
    "weather": "날씨", "trend": "트렌드", "curate": "큐레이션",
    "convert": "전환상승", "viral": "바이럴", "price": "매출급등", "brand": "브랜드"
}

WX_ICON = {
    "Clear": "ti-sun", "Clouds": "ti-cloud",
    "Rain": "ti-cloud-rain", "Snow": "ti-snowflake",
    "Thunderstorm": "ti-cloud-storm", "Drizzle": "ti-cloud-rain",
}

ACTION_ICON = {
    "content": ("ai-content", "ti-camera"),
    "price":   ("ai-price",   "ti-adjustments"),
    "sns":     ("ai-sns",     "ti-brand-instagram"),
    "alert":   ("ai-alert",   "ti-alert-triangle"),
}


def render(data: dict, output_path: str = "index.html"):
    today      = datetime.now().strftime("%Y년 %m월 %d일 (%a)")
    updated_at = datetime.now().strftime("%H:%M")
    weather    = data.get("weather", {})
    insights   = data.get("insights", {})
    platforms  = data.get("platforms", {})
    youtube    = data.get("youtube", [])
    naver      = data.get("naver", {})
    instagram  = data.get("instagram", [])

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>24/7 × Daily Market Intelligence</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap" rel="stylesheet">
{_css()}
</head>
<body>

{_header(today, updated_at, weather)}

<div class="body">
  {_insight_section(insights)}
  {_weather_strip(weather, insights)}
  {_platform_section(platforms)}
  <div class="bottom-grid">
    {_brand_accounts(instagram)}
    {_content_section(youtube, naver)}
  </div>
  <div class="bottom-grid">
    {_keyword_section(insights)}
    {_action_section(insights)}
  </div>
</div>

{_footer()}

{_scripts()}
</body>
</html>"""

    Path(output_path).write_text(html, encoding="utf-8")
    print(f"[builder] {output_path} 생성 완료")


# ─── SECTIONS ──────────────────────────────────────────────

def _header(today, updated_at, weather):
    today_wx = weather.get("today", {})
    temp = today_wx.get("temp", "--")
    desc = today_wx.get("desc", "")
    icon = WX_ICON.get(today_wx.get("icon", ""), "ti-cloud")
    return f"""<div class="hd">
  <div class="hd-brand">24/7 <em>× Daily Market Intelligence</em></div>
  <div class="hd-right">
    <span>{today}</span>
    <div class="wpill"><i class="ti {icon}"></i>&nbsp;서울 · {temp}°C · {desc}</div>
    <span style="color:#e0ddd6">|</span>
    <span>{updated_at} 업데이트</span>
  </div>
</div>"""


def _insight_section(insights):
    items = insights.get("insights", [])
    cards = ""
    for item in items[:3]:
        tags_html = ""
        for tag, ttype in zip(item.get("tags", []), item.get("tag_types", [])):
            cls = IT_CLASS.get(ttype, "it-brand")
            tags_html += f'<span class="it {cls}"># {tag}</span>'
        cards += f"""<div class="ins-item">
      <div class="ins-num">NEWS {item.get("index","")}</div>
      <div class="ins-source">{item.get("source","")}</div>
      <div class="ins-title">{item.get("title","")}</div>
      <div class="ins-body">{item.get("body","")}</div>
      <div class="ins-tags">{tags_html}</div>
    </div>"""
    return f"""<div class="card">
  <div class="clabel"><i class="ti ti-news"></i> 데일리 AI 인사이트 — 오늘 24/7이 주목할 뉴스</div>
  <div class="ins-row">{cards}</div>
</div>"""


def _weather_strip(weather, insights):
    today_wx = weather.get("today", {})
    weekly   = weather.get("weekly", [])
    items    = insights.get("weather_items", ["린넨 셋업", "코튼 반소매", "크롭 트렌치", "라이트 스니커즈"])
    temp = today_wx.get("temp", "--")
    desc = today_wx.get("desc", "")
    feels = today_wx.get("feels_like", "--")

    wx_rows = ""
    colors = ["#8bbfe8", "#f0c070", "#f0c070", "#b0d0a0", "#b0c0e8"]
    reasons = ["나일론·방수 수요↑", "린넨·코튼 전환", "반소매·셋업 수요", "레이어드룩 유지", "기온 변동 대비"]
    for i, day in enumerate(weekly[:5]):
        c = colors[i % len(colors)]
        r = reasons[i % len(reasons)]
        wx_rows += f'<div class="wx-item-row"><span class="wx-dot" style="background:{c}"></span><span class="wx-item-name">{day.get("date","")} {day.get("temp","")}° {day.get("desc","")}</span><span class="wx-item-why">{r}</span></div>'

    item_rows = ""
    dot_colors = ["#b0d890","#b0d890","#b0d890","#b0d890"]
    item_reasons = ["기온 대응", "반팔 시즌", "기온차 레이어", "야외활동 증가"]
    for i, item in enumerate(items[:4]):
        c = dot_colors[i % len(dot_colors)]
        r = item_reasons[i % len(item_reasons)]
        item_rows += f'<div class="wx-item-row"><span class="wx-dot" style="background:{c}"></span><span class="wx-item-name">{item}</span><span class="wx-item-why">{r}</span></div>'

    return f"""<div class="wx-strip">
  <div class="wx-today">
    <div class="wx-temp">{temp}°</div>
    <div class="wx-desc">서울 · {desc}<br>체감 {feels}°C</div>
  </div>
  <div><div class="wx-col-label">이번 주 날씨</div>{wx_rows}</div>
  <div><div class="wx-col-label">내일 추천 아이템</div>{item_rows}</div>
  <div>
    <div class="wx-col-label">주간 핵심 시그널</div>
    <div class="wx-item-row"><span class="wx-dot" style="background:#c0a0e0"></span><span class="wx-item-name">셋업 수요</span><span class="wx-item-why">무신사 기획전 연계</span></div>
    <div class="wx-item-row"><span class="wx-dot" style="background:#c0a0e0"></span><span class="wx-item-name">Y2K 무드</span><span class="wx-item-why">SNS 급상승 지속</span></div>
    <div class="wx-item-row"><span class="wx-dot" style="background:#c0a0e0"></span><span class="wx-item-name">레이어드룩</span><span class="wx-item-why">기온 변동 주간</span></div>
    <div class="wx-item-row"><span class="wx-dot" style="background:#c0a0e0"></span><span class="wx-item-name">워시드 소재</span><span class="wx-item-why">커뮤니티 언급 급증</span></div>
  </div>
</div>"""


def _ptable_rows(items):
    rows = ""
    for item in items:
        sig = item.get("signal", "")
        cls, label = SIGNAL_TAG.get(sig, ("ptag-watch", sig))
        rows += f"""<tr>
      <td><div>{item.get("name","")}</div><div class="brand-sm">{item.get("brand","")}</div></td>
      <td><span class="ptag {cls}">{label}</span></td>
      <td class="issue-txt">{item.get("issue","")}</td>
    </tr>"""
    return rows


def _platform_section(platforms):
    tabs = [
        ("p-ms",  "무신사",  platforms.get("musinsa", [])),
        ("p-29",  "29CM",    platforms.get("cm29", [])),
        ("p-49",  "4910",    platforms.get("store49", [])),
        ("p-kr",  "KREAM",   platforms.get("kream", [])),
        ("p-nv",  "네이버",  platforms.get("naver", [])),
    ]
    tab_btns = "".join(
        f'<button class="tab-btn{"  active" if i==0 else ""}" data-tab="{tid}">{label}</button>'
        for i, (tid, label, _) in enumerate(tabs)
    )
    panels = ""
    for i, (tid, _, items) in enumerate(tabs):
        active = " active" if i == 0 else ""
        rows = _ptable_rows(items)
        panels += f"""<div class="tab-panel{active}" id="{tid}">
      <table class="ptable">
        <thead><tr><th style="width:28%">상품명 / 키워드</th><th style="width:13%">시그널</th><th>이슈 내용</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>"""
    return f"""<div class="card">
  <div class="clabel"><i class="ti ti-building-store"></i> 플랫폼별 주요 상품 · 이슈</div>
  <div class="tab-wrap" id="ptabs">{tab_btns}</div>
  {panels}
</div>"""


def _brand_accounts(instagram):
    rows = ""
    for acc in instagram:
        rows += f"""<div class="ba-row">
      <div class="ba-handle">{acc.get("handle","")}</div>
      <div class="ba-summary">{acc.get("summary","")}</div>
      <div class="ba-time">{acc.get("updated","")}</div>
    </div>"""
    return f"""<div class="card">
  <div class="clabel"><i class="ti ti-brand-instagram"></i> 브랜드 계정 활동 요약</div>
  {rows}
</div>"""


def _content_section(youtube, naver):
    yt_items = ""
    for v in youtube[:5]:
        yt_items += f"""<div class="ct-item">
      <span class="ct-badge b-yt">YT</span>
      <div style="flex:1">
        <div class="ct-title">{v.get("title","")}</div>
        <div class="ct-sum">{v.get("description","")}</div>
        <a class="ct-link" href="{v.get("link","#")}" target="_blank"><i class="ti ti-external-link"></i> 영상 바로가기</a>
      </div>
      <div class="ct-stat">{v.get("channel","")}</div>
    </div>"""

    nv_items = ""
    for b in naver.get("blogs", [])[:5]:
        nv_items += f"""<div class="ct-item">
      <span class="ct-badge b-nv">NV</span>
      <div style="flex:1">
        <div class="ct-title">{b.get("title","")}</div>
        <div class="ct-sum">{b.get("description","")}</div>
        <a class="ct-link" href="{b.get("link","#")}" target="_blank"><i class="ti ti-external-link"></i> 포스팅 바로가기</a>
      </div>
    </div>"""

    return f"""<div class="card">
  <div class="clabel"><i class="ti ti-trending-up"></i> 상위 패션 콘텐츠</div>
  <div class="tab-wrap" id="ctabs">
    <button class="tab-btn active" data-tab="c-yt">유튜브</button>
    <button class="tab-btn" data-tab="c-nv">네이버</button>
  </div>
  <div class="tab-panel active" id="c-yt">{yt_items}</div>
  <div class="tab-panel" id="c-nv">{nv_items}</div>
</div>"""


def _keyword_section(insights):
    kw_sizes = ["kw-1","kw-2","kw-1","kw-3","kw-2","kw-4","kw-3","kw-4","kw-3","kw-4"]
    kws = insights.get("keywords", [])
    kw_html = "".join(
        f'<span class="kw-b {kw_sizes[i % len(kw_sizes)]}">{kw}</span>'
        for i, kw in enumerate(kws)
    )
    sent = insights.get("sentiment", {"positive": 62, "neutral": 24, "negative": 14})
    p, n, neg = sent.get("positive",62), sent.get("neutral",24), sent.get("negative",14)
    return f"""<div class="card">
  <div class="clabel"><i class="ti ti-tag"></i> 급상승 키워드 · 커뮤니티 감성</div>
  <div class="kw-cloud">{kw_html}</div>
  <div style="margin-top:16px">
    <div style="font-size:10px;color:#bbb;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px;">커뮤니티 감성 분석</div>
    <div class="sent-bar"><div class="s-pos" style="width:{p}%"></div><div class="s-neu" style="width:{n}%"></div><div class="s-neg" style="width:{neg}%"></div></div>
    <div class="sent-leg">
      <span><span class="sdot" style="background:#7dc4a0"></span>긍정 {p}%</span>
      <span><span class="sdot" style="background:#d4d0c8"></span>중립 {n}%</span>
      <span><span class="sdot" style="background:#e89898"></span>부정 {neg}%</span>
    </div>
  </div>
</div>"""


def _action_section(insights):
    actions = insights.get("actions", [])
    items_html = ""
    for act in actions[:4]:
        atype = act.get("type", "content")
        cls, icon = ACTION_ICON.get(atype, ("ai-content", "ti-camera"))
        items_html += f"""<div class="act-item">
      <div class="act-icon {cls}"><i class="ti {icon}"></i></div>
      <div><div class="act-t">{act.get("title","")}</div><div class="act-d">{act.get("desc","")}</div></div>
    </div>"""
    return f"""<div class="card">
  <div class="clabel"><i class="ti ti-bolt"></i> 오늘의 AI 추천 액션 아이템</div>
  <div class="act-grid">{items_html}</div>
</div>"""


def _footer():
    updated = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""<div class="footer">
  <span>수집 범위: 무신사 · 29CM · 4910 · KREAM · Instagram · YouTube · 네이버 카페 · FM코리아</span>
  <span style="color:#ddd">|</span>
  <span>마지막 업데이트: {updated}</span>
</div>"""


def _scripts():
    return """<script>
function initTabs(id) {
  var wrap = document.getElementById(id);
  if (!wrap) return;
  wrap.addEventListener('click', function(e) {
    var btn = e.target.closest('.tab-btn');
    if (!btn) return;
    var tid = btn.dataset.tab;
    wrap.querySelectorAll('.tab-btn').forEach(function(b){b.classList.remove('active');});
    btn.classList.add('active');
    var card = wrap.closest('.card') || wrap.parentElement;
    card.querySelectorAll('.tab-panel').forEach(function(p){
      p.classList.toggle('active', p.id === tid);
    });
  });
}
initTabs('ptabs');
initTabs('ctabs');
</script>"""


# ─── CSS ───────────────────────────────────────────────────

def _css():
    return """<style>
/* ── RESET ── */
*{box-sizing:border-box;margin:0;padding:0;}
html{-webkit-text-size-adjust:100%;}

/* ── BASE ── */
body{font-family:'DM Sans',sans-serif;font-weight:400;color:#1a1a1a;background:#f7f6f3;min-height:100vh;}

/* ── HEADER ── */
.hd{background:#fff;border-bottom:.5px solid #e4e1da;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;gap:10px;position:sticky;top:0;z-index:100;}
.hd-brand{font-family:'DM Serif Display',serif;font-size:16px;letter-spacing:.06em;color:#111;white-space:nowrap;}
.hd-brand em{font-style:italic;color:#999;font-size:11px;font-family:'DM Sans',sans-serif;font-weight:300;letter-spacing:.04em;margin-left:8px;}
.hd-right{display:flex;align-items:center;gap:10px;font-size:11px;color:#aaa;font-weight:300;letter-spacing:.03em;flex-wrap:wrap;justify-content:flex-end;}
.hd-date{display:none;}.hd-sep{display:none;}.hd-upd{display:none;}
.wpill{display:flex;align-items:center;gap:4px;background:#f5f3ee;border:.5px solid #e0ddd6;border-radius:20px;padding:4px 10px;font-size:11px;color:#666;white-space:nowrap;}

/* ── BODY ── */
.body{padding:14px 16px;display:flex;flex-direction:column;gap:12px;}

/* ── CARD ── */
.card{background:#fff;border:.5px solid #e4e1da;border-radius:12px;padding:16px;}
.clabel{font-size:10px;font-weight:500;letter-spacing:.1em;color:#bbb;text-transform:uppercase;margin-bottom:12px;display:flex;align-items:center;gap:5px;}
.clabel i{font-size:12px;}

/* ── INSIGHT ── */
.ins-row{display:flex;flex-direction:column;gap:10px;}
.ins-item{background:#fafaf8;border:.5px solid #eceae4;border-radius:10px;padding:14px;}
.ins-num{font-size:10px;font-weight:500;letter-spacing:.1em;color:#ccc;margin-bottom:5px;}
.ins-source{font-size:10px;color:#bbb;font-weight:300;margin-bottom:4px;}
.ins-title{font-size:13px;font-weight:500;color:#222;line-height:1.45;margin-bottom:6px;}
.ins-body{font-size:12px;color:#666;line-height:1.65;font-weight:300;}
.ins-tags{margin-top:9px;display:flex;flex-wrap:wrap;gap:5px;}
.it{font-size:10px;font-weight:500;letter-spacing:.04em;padding:3px 8px;border-radius:4px;}
.it-weather{background:#e6f2fb;color:#1a6fa8;}
.it-trend{background:#f0edf8;color:#6b30b8;}
.it-curate{background:#fdf0e6;color:#b85c10;}
.it-convert{background:#e8f4ed;color:#1f7a40;}
.it-viral{background:#fce8f0;color:#b8205a;}
.it-price{background:#fff3e0;color:#b06000;}
.it-brand{background:#f5f3ee;color:#7a6a50;}

/* ── WEATHER ── */
.wx-strip{background:#fff;border:.5px solid #e4e1da;border-radius:12px;padding:16px;}
.wx-top{display:flex;align-items:flex-start;gap:16px;padding-bottom:14px;margin-bottom:14px;border-bottom:.5px solid #f2f0eb;}
.wx-today{flex-shrink:0;}
.wx-temp{font-family:'DM Serif Display',serif;font-size:38px;color:#333;line-height:1;}
.wx-desc{font-size:11px;color:#aaa;font-weight:300;margin-top:3px;}
.wx-weekly{flex:1;}
.wx-cols{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
.wx-col-label{font-size:10px;font-weight:500;letter-spacing:.1em;color:#bbb;text-transform:uppercase;margin-bottom:8px;}
.wx-item-row{display:flex;align-items:center;gap:7px;padding:5px 0;border-bottom:.5px solid #f5f3ee;}
.wx-item-row:last-child{border-bottom:none;}
.wx-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;}
.wx-item-name{font-size:12px;color:#333;flex:1;}
.wx-item-why{font-size:11px;color:#aaa;font-weight:300;}

/* ── TABS ── */
.tab-wrap{display:flex;border-bottom:.5px solid #eceae4;margin-bottom:12px;overflow-x:auto;-webkit-overflow-scrolling:touch;}
.tab-wrap::-webkit-scrollbar{display:none;}
.tab-btn{font-size:11px;font-weight:500;letter-spacing:.03em;padding:7px 13px;color:#bbb;background:none;border:none;cursor:pointer;font-family:'DM Sans',sans-serif;border-bottom:2px solid transparent;white-space:nowrap;-webkit-tap-highlight-color:transparent;}
.tab-btn.active{color:#222;border-bottom-color:#222;}
.tab-panel{display:none;}
.tab-panel.active{display:block;}

/* ── PLATFORM TABLE (hidden mobile, shown tablet+) ── */
.ptable{display:none;width:100%;border-collapse:collapse;}
.ptable th{font-size:10px;font-weight:500;letter-spacing:.07em;color:#bbb;text-transform:uppercase;padding:6px 8px;border-bottom:.5px solid #eceae4;text-align:left;}
.ptable td{font-size:12px;padding:8px;border-bottom:.5px solid #f5f3ee;vertical-align:middle;color:#333;}
.ptable tr:last-child td{border-bottom:none;}
.ptable tr:hover td{background:#fafaf8;}

/* ── PLATFORM CARDS (mobile only) ── */
.pcard-list{display:flex;flex-direction:column;gap:8px;}
.pcard{background:#fafaf8;border:.5px solid #eceae4;border-radius:8px;padding:11px 13px;}
.pcard-top{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:6px;}
.pcard-name{font-size:12.5px;font-weight:500;color:#222;line-height:1.35;}
.pcard-brand{font-size:11px;color:#aaa;font-weight:300;margin-top:1px;}
.pcard-issue{font-size:11.5px;color:#666;line-height:1.5;font-weight:300;}

/* ── SIGNAL TAGS ── */
.ptag{font-size:10px;font-weight:500;letter-spacing:.03em;padding:2px 7px;border-radius:4px;display:inline-block;}
.ptag-new{background:#e8f4ed;color:#2d7a4a;}
.ptag-up{background:#fdf0e6;color:#c46a1a;}
.ptag-sold{background:#fce8e8;color:#b53030;}
.ptag-drop{background:#e9f0fb;color:#2c5fc4;}
.ptag-trend{background:#f3eefa;color:#7438c2;}
.ptag-watch{background:#f5f3ee;color:#888;border:.5px solid #e0ddd6;}
.ptag-hot{background:#fff0e6;color:#d44800;}
.brand-sm{font-size:11px;color:#aaa;font-weight:300;margin-top:1px;}
.issue-txt{font-size:11.5px;color:#555;line-height:1.45;}

/* ── BOTTOM GRID ── */
.bottom-grid{display:flex;flex-direction:column;gap:12px;}

/* ── BRAND ACCOUNTS ── */
.ba-row{display:flex;align-items:flex-start;gap:8px;padding:9px 0;border-bottom:.5px solid #f5f3ee;}
.ba-row:last-child{border-bottom:none;}
.ba-handle{font-size:11px;font-weight:500;color:#7438c2;width:130px;flex-shrink:0;letter-spacing:.02em;padding-top:1px;}
.ba-summary{font-size:12px;color:#444;font-weight:300;flex:1;line-height:1.55;}
.ba-time{font-size:10px;color:#ccc;flex-shrink:0;padding-top:1px;}

/* ── CONTENT ── */
.ct-item{display:flex;gap:10px;padding:10px 0;border-bottom:.5px solid #f5f3ee;align-items:flex-start;}
.ct-item:last-child{border-bottom:none;}
.ct-badge{font-size:9px;font-weight:500;letter-spacing:.06em;padding:3px 6px;border-radius:4px;flex-shrink:0;margin-top:2px;}
.b-yt{background:#ffe8e8;color:#c0341d;}
.b-nv{background:#e6f5e6;color:#2a7a2a;}
.b-ig{background:#f3eefa;color:#7438c2;}
.ct-title{font-size:12.5px;font-weight:500;color:#222;line-height:1.4;margin-bottom:3px;}
.ct-sum{font-size:11.5px;color:#888;line-height:1.5;font-weight:300;}
.ct-link{font-size:10.5px;color:#7438c2;font-weight:500;text-decoration:none;margin-top:5px;display:inline-flex;align-items:center;gap:3px;}
.ct-stat{font-size:11px;color:#ccc;flex-shrink:0;text-align:right;font-weight:300;min-width:52px;}

/* ── KEYWORDS ── */
.kw-cloud{display:flex;flex-wrap:wrap;gap:6px;}
.kw-b{font-weight:500;padding:5px 11px;border-radius:20px;border:.5px solid;cursor:default;}
.kw-1{font-size:14px;background:#f0ede6;border-color:#d4cfc4;color:#4a4030;}
.kw-2{font-size:13px;background:#edf3f9;border-color:#c0d3e8;color:#2a4f70;}
.kw-3{font-size:12px;background:#f0edf8;border-color:#cdc0e8;color:#4a3070;}
.kw-4{font-size:11px;background:#f5f3ee;border-color:#e0ddd6;color:#777;}
.sent-bar{display:flex;height:5px;border-radius:3px;overflow:hidden;margin:12px 0 7px;}
.s-pos{background:#7dc4a0;}.s-neu{background:#d4d0c8;}.s-neg{background:#e89898;}
.sent-leg{display:flex;gap:12px;font-size:11px;color:#888;font-weight:300;}
.sdot{width:7px;height:7px;border-radius:50%;display:inline-block;margin-right:3px;vertical-align:middle;}

/* ── ACTIONS ── */
.act-grid{display:grid;grid-template-columns:1fr 1fr;gap:9px;}
.act-item{background:#fafaf8;border:.5px solid #eceae4;border-radius:8px;padding:11px 12px;display:flex;gap:9px;align-items:flex-start;}
.act-icon{width:26px;height:26px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;}
.ai-content{background:#f0edf8;color:#7438c2;}
.ai-price{background:#fdf0e6;color:#c46a1a;}
.ai-sns{background:#e8f4ed;color:#2d7a4a;}
.ai-alert{background:#fce8e8;color:#b53030;}
.act-t{font-size:12px;font-weight:500;color:#222;margin-bottom:2px;line-height:1.3;}
.act-d{font-size:11px;color:#999;font-weight:300;line-height:1.45;}

/* ── FOOTER ── */
.footer{padding:12px 16px;border-top:.5px solid #e4e1da;font-size:10px;color:#ccc;font-weight:300;background:#fff;text-align:center;line-height:1.7;}

/* ══ TABLET ≥640px ══ */
@media(min-width:640px){
  .body{padding:18px 22px;gap:14px;}
  .card{padding:18px 20px;}
  .hd{padding:13px 22px;}
  .hd-date{display:inline;}
  .hd-sep{display:inline;}
  .ins-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
  .wx-cols{grid-template-columns:1fr 1fr 1fr;}
  .ptable{display:table;}
  .pcard-list{display:none;}
  .bottom-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
  .footer{display:flex;justify-content:space-between;align-items:center;padding:12px 22px;text-align:left;}
}

/* ══ DESKTOP ≥1024px ══ */
@media(min-width:1024px){
  .body{padding:22px 28px;gap:16px;}
  .card{padding:20px 22px;}
  .hd{padding:14px 28px;}
  .hd-brand{font-size:18px;}
  .hd-upd{display:inline;}
  .ins-row{grid-template-columns:1fr 1fr 1fr;}
  .wx-strip{display:grid;grid-template-columns:auto 1fr 1fr 1fr;gap:24px;align-items:start;padding:18px 22px;}
  .wx-top{display:contents;}
  .wx-today{flex-shrink:0;}
  .wx-weekly{display:contents;}
  .wx-cols{display:contents;}
  .footer{padding:13px 28px;}
}
</style>"""
