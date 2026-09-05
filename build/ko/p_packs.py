# -*- coding: utf-8 -*-
"""업종별 팩 상세 - 스물다섯 장.

업종 페이지는 주장이다. 밤에 어떤 전화가 오고, 못 받으면 무엇을 잃고,
기계가 무엇을 말하면 안 되는가. 팩 페이지는 그 주장의 목록이다.
무엇이 들어 있는지, 어떤 칸이 채워지는지, 어디에 연결되는지.

두 개를 한 페이지에 놓으면 읽는 사람이 지친다. 그래서 나눴고,
서로 오가는 링크를 달았다. 영문 사이트에서 같은 판단을 이미 한 구조다.

연동을 적을 때 특정 제품 이름을 함부로 쓰지 않는다. 국내 예약 시스템과
차트 프로그램은 병원마다 다르고, 연동된다고 적어 놓고 안 되면 그것이
가장 나쁜 거짓말이 된다. 그래서 "표준 방식으로 연결되고, 쓰시는 제품이
되는지는 확인해서 알려 드린다"고 쓴다.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.dirname(os.path.dirname(HERE)))
from shell import page, NAV, FOOT
from trades import TRADES
from trades2 import TRADES2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import illus

try:
    from trades3 import TRADES3
except Exception:
    TRADES3 = []
try:
    from trades4 import TRADES4
except Exception:
    TRADES4 = []
try:
    from trades5 import TRADES5
except Exception:
    TRADES5 = []
NEW_TRADES = TRADES3 + TRADES4 + TRADES5
ALL = TRADES + TRADES2 + NEW_TRADES
import json as _json
_PHOTOS = _json.load(io.open('build/demo/photos.json', encoding='utf-8')) if os.path.exists('build/demo/photos.json') else {}
for _t in NEW_TRADES:
    if 'PENDING' in str(_t.get('photo', '')) and _PHOTOS.get(_t['slug']):
        _t['photo'] = 'https://images.pexels.com/photos/%s/pexels-photo-%s.jpeg' % (_PHOTOS[_t['slug']], _PHOTOS[_t['slug']])
NB = '&nbsp;'

CSS = """
  .hero{display:block;padding:150px 0 54px;}
  .packgrid{display:grid;gap:26px;margin-top:36px;}
  .packblock{padding:30px 28px;border:1px solid var(--hair-d);border-radius:14px;}
  .packblock h2{font-size:var(--fs-lead);color:#141A1F;}
  .packblock .why{margin-top:10px;font-size:var(--fs-sm);line-height:1.8;color:var(--tx2);}
  .fieldgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:22px;}
  @media (max-width:760px){.fieldgrid{grid-template-columns:1fr;}}
  .fieldgrid span{padding:14px 16px;border:1px solid var(--hair-d);border-radius:9px;
    font-size:var(--fs-sm);line-height:1.6;color:var(--tx2);}
  .pipe{display:flex;flex-wrap:wrap;gap:9px;margin-top:22px;align-items:center;}
  .pipe b{padding:10px 16px;border:1px solid var(--hair-d);border-radius:8px;
    font-size:var(--fs-sm);font-weight:600;color:#141A1F;}
  .pipe i{font-style:normal;color:var(--teal);}
  .kolist{margin-top:20px;display:grid;gap:14px;}
  .kolist li{list-style:none;padding-left:26px;position:relative;
    font-size:var(--fs-sm);line-height:1.8;color:var(--tx2);}
  .kolist li::before{content:"";position:absolute;left:2px;top:.72em;width:8px;height:8px;
    border-radius:50%;border:1.5px solid var(--teal);}
  .kolist li b{display:block;color:#141A1F;margin-bottom:3px;}
  .packback{border-top:1px solid var(--hair-d);}
  .pb-line{font-size:var(--fs-body);line-height:1.85;color:var(--tx2);max-width:none;}
  .pb-line b{color:#141A1F;}
  .pb-links{margin-top:22px;display:flex;flex-wrap:wrap;gap:22px;}
"""

# 연동은 업종을 가리지 않고 같은 방식으로 붙는다. 그래서 한 번만 쓴다.
LINKS = [
    ('전화 회선', '쓰시던 대표번호는 그대로 두고, 못 받은 전화만 AI에게 넘기거나 '
                 '처음부터 AI가 받게 할 수 있습니다. 필요할 때는 사람에게 돌립니다.'),
    ('카카오톡 채널', '채널로 온 문의를 같은 내용으로 받습니다. 알림톡 발송도 붙습니다.'),
    ('홈페이지 채팅', '스크립트 한 줄을 넣으면 됩니다. 홈페이지를 새로 만들 필요가 없습니다.'),
    ('캘린더', '구글 캘린더와 네이버 캘린더에 예약을 그대로 넣습니다. '
              '메모를 남기는 것이 아니라 시간을 잡습니다.'),
    ('문자', '예약 확인과 전날 알림을 보냅니다. 발송 기록이 함께 남습니다.'),
    ('내보내기', '고객, 상담 내역, 녹취를 언제든 전부 내려받을 수 있습니다. '
                'CSV와 웹훅으로 나갑니다.'),
]

TPL = """
<header class="hero nophoto sec-dark bg-aurora">
  <div class="scrim" aria-hidden="true"></div>
  {NAV}
  <div class="wrap hero-inner">
    <span class="eyebrow"><i></i>{name} 팩</span>
    <h1 style="margin-top:24px;">팩에 들어 있는 것 전부,<br>그리고 하지 않는 것 전부.</h1>
    <p class="sub">통화 뒤에 붙는 CRM의 항목과 단계, 어디에 연결되는지,
      그리고 무엇을 말하지 않는지. 왜 이것이 필요한지는
      <a href="./{slug}.html">{name} 페이지</a>에 적어 두었습니다.</p>
  </div>
</header>

<main>

<section class="t-md sec-dark bg-grid" id="pack">
  <div class="wrap">
    <div class="packphoto reveal"><img src="{photo}?auto=compress&amp;cs=tinysrgb&amp;w=1600&amp;h=640&amp;fit=crop" alt="" width="1600" height="640" loading="lazy" decoding="async"><span>{name} &mdash; 이 팩은 이 현장의 전화를 위해 만든 것입니다. 사진은 예시입니다.</span></div>
    <div class="packgrid">

      <div class="packblock reveal" id="fields">
        <h2>통화가 끝나면 채워져 있는 칸</h2>
        <p class="why">{packstatus}</p>
        <div class="fieldgrid">{fields}</div>
      </div>

      <div class="packblock reveal" id="stages">
        <h2>문의가 지나가는 단계</h2>
        <p class="why">지금 몇 건이 어느 단계에 있는지 한 줄로 보입니다.
          {name}에서 실제로 일이 흘러가는 순서 그대로입니다.</p>
        <div class="pipe">{stages}</div>
        <div class="illwide">{ill_pipe}</div>
      </div>

      <div class="packblock reveal" id="links">
        <h2>어디에 연결되는가</h2>
        <p class="why">아래는 어느 업종에서나 같은 방식으로 붙습니다.
          지금 쓰고 계신 예약 시스템이나 차트 프로그램이 되는지는
          제품마다 달라서, 확인해서 알려 드립니다. 된다고 먼저 적어 두지 않습니다.</p>
        <ul class="kolist">{links}</ul>
      </div>

      <div class="packblock reveal" id="refuse">
        <h2>하지 않는 일</h2>
        <p class="why">설정으로 끄고 켜는 기능이 아니라, {name} 응대를 만들 때
          처음부터 막아 두는 것입니다. 여기에 걸리면 답하지 않고 사람에게 넘깁니다.</p>
        <ul class="kolist">{refuse}</ul>
      </div>

    </div>
  </div>
</section>

<section class="packback t-sm sec-dark" id="back">
  <div class="wrap">
    <p class="pb-line"><b>이 페이지는 목록이고, 주장은 저쪽에 있습니다.</b>
      밤에 걸려 오는 전화가 어떤 전화인지, 못 받으면 무엇을 잃는지,
      기계가 왜 그 말을 하면 안 되는지는 이 팩이 나온 페이지에 적혀 있습니다.</p>
    <p class="pb-links"><a class="linkcta" href="./{slug}.html">{name} 페이지로 돌아가기{NB}{NB}&rarr;</a><a class="linkcta" href="../get-started.html">{name} 견적 받기{NB}{NB}&rarr;</a></p>
  </div>
</section>

{FOOT}
</main>
"""

CARD = """<section class="packcard t-md sec-dark bg-grid" id="the-pack">
  <div class="wrap">
    <a class="pc-link" href="./{slug}-pack.html">
      <span class="pc-k">{name} 팩</span>
      <b class="pc-h">팩에 들어 있는 것 전부, 따로 한 장에</b>
      <span class="pc-d">통화 뒤에 붙는 CRM의 항목과 단계, 어디에 연결되는지,
        그리고 무엇을 말하지 않는지를 한 장에 적어 두었습니다.
        주장이 아니라 목록이라서, 이 페이지와 섞지 않고 따로 떼어 두었습니다.</span>
      <span class="pc-go" aria-hidden="true">&rarr;</span>
    </a>
  </div>
</section>"""


LIVE = ('venues', 'clinics')


def pack_status(t):
    if t['slug'] in LIVE:
        return ('빈 CRM을 받아 %s에 맞게 고쳐 쓰는 것이 아닙니다. 이 항목들이 처음부터 들어 있고, '
                '첫 통화부터 여기에 적힙니다. 이 팩은 지금 운영 중입니다.' % t['name'])
    return ('이 업종 팩은 <b>아직 운영 중이 아닙니다</b>. 아래는 요청하시면 그대로 만들어 드리는 설계안입니다. '
            '항목·단계·하지 않는 말의 초안까지 준비되어 있어, 요금표와 영업시간을 주시면 며칠 안에 켤 수 있습니다.')


LINKS_EN = [
    ('Phone line', 'Keep the main number you already publish; forward only the calls you cannot take, or let the AI '
                   'answer from the first ring. When it needs to, it hands the call to a person.'),
    ('WhatsApp & messengers', 'Messages to your business number are answered from the same facts. Templates and follow-ups included.'),
    ('Website chat', 'One line of script on the site you already have. No rebuild.'),
    ('Calendar', 'Bookings are written into Google Calendar or Outlook as real slots, not notes.'),
    ('Text messages', 'Confirmations and day-before reminders, with a delivery record.'),
    ('Export', 'Customers, conversations and recordings can be downloaded in full at any time — CSV and webhooks.'),
]

TPL_EN = """
<header class="hero nophoto sec-dark bg-aurora">
  <div class="scrim" aria-hidden="true"></div>
  {NAV}
  <div class="wrap hero-inner">
    <span class="eyebrow"><i></i>The {name} pack</span>
    <h1 style="margin-top:24px;">Everything in the pack,<br>and everything it will not do.</h1>
    <p class="sub">The CRM fields and stages that follow every call, what it connects to, and what it never says.
      Why any of it matters is on the <a href="./{slug}.html">{name} page</a>.</p>
  </div>
</header>

<main>

<section class="t-md sec-dark bg-grid" id="pack">
  <div class="wrap">
    <div class="packphoto reveal"><img src="{photo}?auto=compress&amp;cs=tinysrgb&amp;w=1600&amp;h=640&amp;fit=crop" alt="" width="1600" height="640" loading="lazy" decoding="async"><span>{name} &mdash; this pack was built for the calls that reach this kind of business. Illustrative photograph.</span></div>
    <div class="packgrid">

      <div class="packblock reveal" id="fields">
        <h2>Fields that are filled when the call ends</h2>
        <p class="why">{packstatus}</p>
        <div class="fieldgrid">{fields}</div>
      </div>

      <div class="packblock reveal" id="stages">
        <h2>The stages an inquiry moves through</h2>
        <p class="why">How many inquiries sit at each stage, on one line &mdash; in the order work actually flows in a {name}.</p>
        <div class="pipe">{stages}</div>
        <div class="illwide">{ill_pipe}</div>
      </div>

      <div class="packblock reveal" id="links">
        <h2>What it connects to</h2>
        <p class="why">These connect the same way in every trade. Whether your booking system or practice software connects
          depends on the product, so we check and tell you &mdash; we do not write &ldquo;yes&rdquo; first.</p>
        <ul class="kolist">{links}</ul>
      </div>

      <div class="packblock reveal" id="refuse">
        <h2>What it will not do</h2>
        <p class="why">Not a setting you switch on and off. These are blocked when the {name} answering is built; anything that touches them
          goes to a person instead of being answered.</p>
        <ul class="kolist">{refuse}</ul>
      </div>

    </div>
  </div>
</section>

<section class="packback t-sm sec-dark" id="back">
  <div class="wrap">
    <p class="pb-line"><b>This page is the list; the argument is on the other one.</b>
      What kind of call comes in at night, what a missed one costs, and why a machine must not say certain things
      are written on the page this pack came from.</p>
    <p class="pb-links"><a class="linkcta" href="./{slug}.html">Back to the {name} page{NB}{NB}&rarr;</a><a class="linkcta" href="../get-started.html">Get my plan &mdash; {name}{NB}{NB}&rarr;</a></p>
  </div>
</section>

{FOOT}
</main>
"""


def pack_status_en(t, name):
    if t['slug'] in LIVE:
        return ('Not an empty CRM bent to a %s over months. These fields are in it from the start and the first call '
                'writes into them. This pack is running today.' % name)
    return ('This trade pack is <b>not running yet</b>. Below is the design we build for you on request: the fields, '
            'stages and never-say list are drafted, so with your price list and hours it can be switched on within days.')


def build_pack_en(t):
    e = t['en']; name = e['name']
    fields = ''.join('<span>%s</span>' % f for f in e['fields'])
    stages = '<i>&rarr;</i>'.join('<b>%s</b>' % s for s in e['stages'])
    links = ''.join('<li><b>%s</b>%s</li>' % (a, b) for a, b in LINKS_EN)
    refuse = ''.join('<li><b>%s</b>%s</li>' % (a, b) for a, b in e['refuse'])
    body = TPL_EN.format(NAV=NAV, FOOT=FOOT, NB=NB, fields=fields, stages=stages,
                         links=links, refuse=refuse, slug=t['slug'], name=name, packstatus=pack_status_en(t, name),
                         photo=t['photo'], ill_pipe=illus.figure(illus.pipeline('en', stages=e['stages'][:5])))
    page('industries/%s-pack.html' % t['slug'],
         'What is in the %s pack &mdash; Saleringo' % name,
         'Every CRM field and pipeline stage for a %s, what it connects to, and what the AI never does.' % name,
         body, css=CSS, grade='trust', lang='en',
         crumbs=[('Home', 'index.html'), ('Trades', 'industries.html'),
                 (name, 'industries/%s.html' % t['slug']),
                 ('The %s pack' % name, 'industries/%s-pack.html' % t['slug'])])


def build_pack(t):
    fields = ''.join('<span>%s</span>' % f for f in t['fields'])
    stages = '<i>&rarr;</i>'.join('<b>%s</b>' % s for s in t['stages'])
    links = ''.join('<li><b>%s</b>%s</li>' % (a, b) for a, b in LINKS)
    refuse = ''.join('<li><b>%s</b>%s</li>' % (a, b) for a, b in t['refuse'])
    body = TPL.format(NAV=NAV, FOOT=FOOT, NB=NB, fields=fields, stages=stages,
                      links=links, refuse=refuse, slug=t['slug'], name=t['name'], packstatus=pack_status(t),
                      photo=t['photo'], ill_pipe=illus.figure(illus.pipeline('ko', stages=t['stages'][:5])))
    page('industries/%s-pack.html' % t['slug'],
         '%s 팩에 들어 있는 것 &mdash; Saleringo' % t['name'],
         '%s용 CRM의 항목과 진행 단계, 연동되는 곳, 그리고 AI가 하지 않는 일을 '
         '전부 적었습니다.' % t['name'],
         body, css=CSS, grade='trust',
         crumbs=[('홈', 'index.html'), ('업종', 'industries.html'),
                 (t['name'], 'industries/%s.html' % t['slug']),
                 ('%s 팩' % t['name'], 'industries/%s-pack.html' % t['slug'])])


n_en = 0
for t in ALL:
    build_pack(t)
    if 'en' in t:
        build_pack_en(t); n_en += 1
print('팩 페이지 %d장' % len(ALL))
