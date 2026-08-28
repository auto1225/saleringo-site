# -*- coding: utf-8 -*-
"""상태 & 장애 이력 — 양 언어를 한 원문에서.

정직 규칙이 이 페이지에서 제일 어렵다. 상태 페이지는 보통
「All systems operational」 초록 벽인데, 우리가 실제로 실시간으로
확인할 수 있는 것은 하나뿐이다 — 주문 접수 API 가 지금 응답하는가.
그래서 그 하나만 브라우저가 직접 확인하고(status.js), 나머지는
손으로 갱신하는 이력이라고 페이지가 스스로 말한다.

없는 것(공식 SLA, 자동 가동률 그래프)은 없다고 적는다. 약관
얼리액세스 조항과 같은 말이어야 하고, 실제로 그 조항을 링크한다.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from shell import page, NAV, FOOT  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def build(lang):
    ko = lang == "ko"

    def t(k, e):
        return k if ko else e

    CSS = """
  .stwrap{max-width:760px;margin:0 auto;}
  .stcard{background:rgba(255,255,255,.035);border:1px solid var(--hair-d);border-radius:16px;
    padding:24px 26px;margin-top:22px;}
  .stcard .lbl{font-size:var(--fs-2xs);font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--tx3);}
  .stbadge{display:inline-block;margin-top:14px;font-size:var(--fs-h3);font-weight:700;}
  .stbadge.ok{color:var(--green);}
  .stbadge.warn{color:var(--amber);}
  .stwhen{margin-top:8px;font-size:var(--fs-2xs);color:var(--tx3);font-weight:600;}
  .strow{display:grid;grid-template-columns:150px 1fr;gap:6px 16px;padding:11px 0;
    border-bottom:1px dashed var(--hair-d);font-size:var(--fs-sm);}
  .strow:last-child{border-bottom:0;}
  .strow b{color:var(--tx);}
  .strow span{color:var(--tx2);}
  .stnone{margin-top:14px;font-size:var(--fs-sm);color:var(--tx2);}
  @media (max-width:640px){.strow{grid-template-columns:1fr;}}
"""

    body = "".join([
        '<header class="hero heroatmo photohero bg-grid nophoto">\n',
        '  <div class="scrim" aria-hidden="true"></div>\n',
        '  <div class="tint" aria-hidden="true"></div>\n',
        "  {NAV}\n",
        '  <div class="wrap hero-inner" style="max-width:760px;text-align:center;">\n',
        "    <h1>", t("상태 &amp; 장애 이력", "Status &amp; incidents"), "</h1>\n",
        '    <p class="sub">',
        t("이 페이지가 실시간으로 확인하는 것은 하나 &mdash; 주문 접수가 지금 되는가 &mdash; 이고, "
          "사장님 브라우저가 직접 확인합니다. 나머지는 손으로 갱신하는 기록이며, 그렇게 적혀 있습니다.",
          "This page makes one live check &mdash; whether order intake works right now &mdash; "
          "and your own browser makes it. Everything else here is hand-updated history, and says so."),
        "</p>\n  </div>\n</header>\n\n",

        '<section class="t-md sec-dark bg-grid">\n  <div class="wrap stwrap">\n',

        '    <div class="stcard reveal">\n',
        '      <p class="lbl">', t("지금, 실시간", "Right now, live"), "</p>\n",
        '      <p class="stbadge" data-status-live>', t("확인 중&hellip;", "Checking&hellip;"), "</p>\n",
        '      <p class="stwhen" data-status-when></p>\n',
        "      <p class=\"stnone\">",
        t("확인 방법: 이 브라우저가 <code>/api/order</code> 에 물어, 주문이 지금 저장될 수 있는지를 "
          "서버가 답한 그대로 보여 줍니다. 저희가 대신 말해 주는 값이 아닙니다.",
          "How: this browser asks <code>/api/order</code> and shows the server's own answer on whether "
          "an order can be stored right now. It is not a value we assert for you."),
        "</p>\n    </div>\n\n",

        '    <div class="stcard reveal">\n',
        '      <p class="lbl">', t("장애 이력", "Incident history"), "</p>\n",
        '      <p class="stnone">',
        t("게시된 장애가 아직 없습니다. 장애가 나면 이 자리에 <b>무엇이 &middot; 언제부터 언제까지 &middot; "
          "누구에게 영향 &middot; 무엇을 고쳤는지</b> 형식으로 남고, 진행 중 주문이 있는 분께는 이메일로도 갑니다.",
          "No incidents published yet. When one happens it is recorded here as <b>what &middot; from&ndash;to "
          "&middot; who was affected &middot; what we fixed</b>, and anyone with an order in flight is emailed."),
        "</p>\n    </div>\n\n",

        '    <div class="stcard reveal">\n',
        '      <p class="lbl">', t("아직 없는 것 &mdash; 있는 척하지 않습니다", "What we do not have yet &mdash; said plainly"), "</p>\n",
        '      <div class="strow"><b>', t("공식 가동률 SLA", "A formal uptime SLA"), "</b><span>",
        t("얼리액세스 기간에는 없습니다. <a class=\"lnk\" href=\"./terms.html\">약관</a>에 같은 말이 적혀 있습니다.",
          "Not during early access. The <a class=\"lnk\" href=\"./terms.html\">Terms</a> say the same thing."),
        "</span></div>\n",
        '      <div class="strow"><b>', t("자동 가동률 그래프", "An automated uptime graph"), "</b><span>",
        t("아직 없습니다. 초록 막대 90일치를 그려 두는 것보다, 없는 것을 없다고 적는 쪽을 골랐습니다.",
          "Not yet. We chose saying so over drawing ninety days of green bars."),
        "</span></div>\n",
        "    </div>\n\n",

        '    <div class="stcard reveal">\n',
        '      <p class="lbl">', t("어디서 돌아가는가", "Where things run"), "</p>\n",
        '      <div class="strow"><b>', t("운영 데이터베이스", "Operational database"), "</b><span>",
        t("대한민국(서울). 다른 리전은 계약으로.", "South Korea (Seoul). Other regions by contract."),
        "</span></div>\n",
        '      <div class="strow"><b>', t("답변을 만드는 모델", "The model that composes answers"), "</b><span>",
        t("미국 서버에서 실행됩니다. 주문서에서 이 국외 이전에 별도로 동의를 받습니다.",
          "Runs on US servers. The order form asks for separate consent to this transfer."),
        "</span></div>\n",
        '      <div class="strow"><b>', t("나라별 전화 회선", "Phone lines by country"), "</b><span>",
        t("<a class=\"lnk\" href=\"./pricing.html#rates\">요금 페이지</a>에 통화 단가가, 나라별 회선 상태는 주문서에서 나라를 고르시면 그 자리에서 확인됩니다.",
          "The <a class=\"lnk\" href=\"./pricing.html#countries\">country table on the pricing page</a> lists line status per country."),
        "</span></div>\n",
        '      <div class="strow"><b>', t("실제 상담 음성", "Hearing the real voice"), "</b><span>",
        t("언어별 녹음 샘플은 준비 중입니다. 지금은 <a class=\"lnk\" href=\"./index.html#demo60\">60초 데모</a>나 "
          "실제 데모 번호로 직접 들어 보시는 것이 정확합니다.",
          "Per-language recorded samples are in preparation. Today the accurate way is the "
          "<a class=\"lnk\" href=\"./index.html#demo60\">60-second demo</a> or dialling a live demo number."),
        "</span></div>\n",
        "    </div>\n",

        "  </div>\n</section>\n\n{FOOT}",
    ])

    body = body.replace("{NAV}", "<!--#nav-->\n<!--/#nav-->").replace("{FOOT}", "<!--#footer-->\n<!--/#footer-->")

    page("status.html",
         t("상태 &amp; 장애 이력 &mdash; Saleringo", "Status &amp; incidents &mdash; Saleringo"),
         t("Saleringo 의 지금 상태. 주문 접수는 브라우저가 실시간으로 확인하고, 장애 이력은 여기 게시되며, "
           "없는 것은 없다고 적습니다.",
           "Saleringo right now: order intake checked live from your browser, incidents published here, "
           "and what we lack said plainly."),
         body, css=CSS, grade="trust",
         scripts=("site", "balance", "panels", "wrap", "rail", "guide", "status"),
         lang=lang,
         crumbs=[(t("홈", "Home"), "index.html"), (t("상태", "Status"), "status.html")])


build("ko")
build("en")
print("ko/status.html, en/status.html")
