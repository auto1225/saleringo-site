# -*- coding: utf-8 -*-
"""Turn build/ko/trades.py into ten trade pages and the wall that lists them.

The page is the same shape every time - night call, what it costs to miss,
what it will not do, what it writes down - because that shape is the argument
and repeating it is the point. What is never repeated is the content: no two
of these pages share a sentence, because no two of these trades lose a call
the same way.
"""
import io
import json
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

TRADES = TRADES + TRADES2

# 요금은 assets/data/pricing.json 하나에서만 읽는다. 페이지에 숫자를 직접
# 적어 두면 요금표가 바뀔 때 한쪽만 고쳐지고, 그 순간 이 페이지가 거짓말이 된다.
PR = json.load(io.open('assets/data/pricing.json', encoding='utf-8'))

NB = '&nbsp;'

CSS = """
  .hero{display:block;padding:0 0 74px;}
  .hero-inner{padding-top:130px;}
  .heroband{max-width:820px;}
  .nightline{display:grid;gap:16px;padding:26px 24px;}
  .nl{display:grid;grid-template-columns:104px 1fr;gap:16px;align-items:start;}
  .nl .t{font-size:var(--fs-2xs);letter-spacing:.14em;color:rgba(20,26,31,.5);
    text-transform:uppercase;padding-top:9px;}
  .nl .t em{display:block;font-style:normal;color:rgba(20,26,31,.66);
    letter-spacing:.02em;text-transform:none;font-size:var(--fs-xs);}
  @media (max-width:640px){.nl{grid-template-columns:1fr;gap:6px;}.nl .t{padding-top:0;}}
  .kolist{margin-top:26px;display:grid;gap:16px;}
  .kolist li{list-style:none;padding-left:26px;position:relative;
    font-size:var(--fs-body);line-height:1.8;color:var(--tx2);}
  .kolist li::before{content:"";position:absolute;left:2px;top:.72em;width:9px;height:9px;
    border-radius:50%;border:1.5px solid var(--teal);}
  .kolist li b{display:block;color:#141A1F;margin-bottom:4px;}
  .sec-light .kolist li,.bg-paper .kolist li,.sec-light2 .kolist li{color:var(--l-tx2);}
  .sec-light .kolist li b,.bg-paper .kolist li b,.sec-light2 .kolist li b{color:var(--l-ink);}
  .fieldgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:30px;}
  @media (max-width:760px){.fieldgrid{grid-template-columns:1fr;}}
  .fieldgrid span{padding:16px 18px;border:1px solid #D5DBE4;border-radius:8px;
    font-size:var(--fs-sm);line-height:1.65;color:var(--l-tx2);}
  .pipe{display:flex;flex-wrap:wrap;gap:10px;margin-top:28px;align-items:center;}
  .pipe b{padding:11px 18px;border:1px solid var(--hair-d);border-radius:8px;
    font-size:var(--fs-sm);font-weight:600;color:#141A1F;}
  .pipe i{font-style:normal;color:var(--teal);}
  .otherwall{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px;}
  .otherwall a{padding:11px 18px;border:1px solid #D5DBE4;border-radius:8px;
    text-decoration:none;color:var(--l-ink);font-size:var(--fs-sm);font-weight:500;
    transition:all .3s var(--ease);}
  .otherwall a:hover{border-color:var(--teal);background:rgba(11,120,120,.08);}
  /* ══ 사고가 나면 · 약관과 보안 페이지의 문장을 옮겨 적은 것 ══ */
  .ifwrong{margin-top:30px;padding:22px 24px;border:1px solid var(--hair-d);border-radius:8px;}
  .ifwrong > b{display:block;font-size:var(--fs-body);color:#141A1F;margin-bottom:10px;}
  .ifwrong ul{display:grid;gap:10px;}
  .ifwrong li{list-style:none;font-size:var(--fs-sm);line-height:1.75;color:var(--tx2);}
  .ifwrong li b{color:#141A1F;}
  .ifwrong a{color:var(--teal);font-weight:700;text-decoration:none;white-space:nowrap;}
  /* ══ the playbook · what each door captures ══ */
  #playbook .trio p a{color:var(--teal);font-weight:700;text-decoration:none;}
  #playbook .trio{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;}
  @media(max-width:880px){#playbook .trio{grid-template-columns:1fr;}}
  #playbook .trio>div{background:#fff;border:1px solid var(--l-hair);border-radius:14px;padding:24px 24px 26px;}
  #playbook .trio b{display:block;font-size:var(--fs-body);letter-spacing:-.01em;color:var(--l-ink);}
  #playbook .trio p{margin-top:8px;font-size:var(--fs-xs);line-height:1.7;color:var(--l-mut);font-weight:500;}
  #playbook .h3{font-family:'Bricolage Grotesque',sans-serif;font-size:var(--fs-h2s);font-weight:600;letter-spacing:-.03em;color:var(--l-ink);}
  #playbook .dtwrap{overflow-x:auto;}
  #playbook .dtable{width:100%;margin-top:16px;border-collapse:collapse;}
  #playbook .dtable th,#playbook .dtable td{padding:13px 12px;text-align:left;font-size:var(--fs-xs);line-height:1.65;
    border-bottom:1px solid #E3E7EE;vertical-align:top;color:var(--l-mut);font-weight:500;}
  #playbook .dtable th{color:var(--l-ink);font-weight:700;}
  #playbook .dtable td b{color:var(--l-ink);}
  @media(max-width:700px){#playbook .dtable{min-width:640px;}}
"""

TPL = """
<header class="hero photohero">
  <div class="bgimg" aria-hidden="true">
    <img class="ph" src="{photo}?auto=compress&amp;cs=tinysrgb&amp;w=1600" alt=""
         width="1900" height="1425" loading="eager" fetchpriority="high" decoding="async"
         srcset="{photo}?auto=compress&amp;cs=tinysrgb&amp;w=640 640w, {photo}?auto=compress&amp;cs=tinysrgb&amp;w=1024 1024w, {photo}?auto=compress&amp;cs=tinysrgb&amp;w=1600 1600w"
         sizes="(max-width:900px) 100vw, 60vw">
  </div>
  <div class="scrim" aria-hidden="true"></div>
  <div class="tint" aria-hidden="true"></div>
  <div class="grainlayer grain" aria-hidden="true"></div>
  {NAV}
  <div class="wrap hero-inner">
    <div class="heroband hero-panel">
      <span class="eyebrow"><i></i>{kicker}</span>
      <h1>{h1}</h1>
      <p class="sub">{sub}</p>
      <div class="ctas">
        <a class="btn btn-teal" href="#call">그 통화 읽어 보기<span class="cir">&darr;</span></a>
        <a class="btn btn-ghostd" href="../get-started.html">{name} 견적 받기</a>
      </div>
    </div>
  </div>
</header>

<main>

<section class="t-md sec-dark bg-dusk" id="call">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>{when_eyebrow}</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">{when_h2}</h2>
    <div class="appwin reveal" style="margin-top:34px;">
      <div class="bar"><i></i><i></i><i></i>
        <span class="tt">{name} &mdash; <b>{when_tt}</b></span>
        <span class="illus">예시 &middot; 가상의 상담</span>
        <span class="closed">{when_badge}</span></div>
      <div class="body nightline">{turns}</div>
    </div>
    <p class="seccap reveal" style="margin-top:16px;">실제 고객 사례가 아니라, {name} 요금표와 안전 지침을
      넣었을 때 제품이 어떻게 답하는지 보여 주는 예시입니다. 금액은 국내에서 흔히 제시되는 범위이고,
      실제로 안내되는 금액은 {owner}이 넣으신 요금표에서 나옵니다.</p>
  </div>
</section>

<section class="t-md sec-dark bg-grid" id="cost">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>놓쳤을 때</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">{name}에서 못 받은 전화는<br>어디에도 기록되지 않습니다.</h2>
    <div class="illrow reveal"><p class="sub" style="max-width:none;margin-top:0;">{cost}</p>{ill_night}</div>
  </div>
</section>

<section class="t-md sec-dark bg-spot" id="refuses">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>하지 않는 일</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">{name}에서 기계가<br>말하면 안 되는 것들.</h2>
    <p class="sub reveal" style="max-width:none;">아래 네 가지는 설정으로 끄고 켜는 기능이 아니라,
      {name} 응대를 만들 때 처음부터 막아 두는 것입니다. 여기에 걸리면 AI는 답하지 않고
      사람에게 넘깁니다.</p>
    <div class="illrow reveal"><ul class="kolist" style="margin-top:0;">{refuse}</ul>{ill_handoff}</div>
    <div class="ifwrong reveal">
      <b>사고가 나면</b>
      <ul>
        <li>AI 응답의 오류로 손해가 생기면, 저희 배상 책임은 <b>그 사고가 난 달로부터 직전 3개월간
          지급하신 요금의 합계</b>가 한도입니다. 저희의 고의 또는 중대한 과실로 인한 손해는 이 한도와
          관계없이 법이 정하는 바에 따라 배상합니다. <a href="../terms.html#sec-8">약관 제7조 &rarr;</a></li>
        <li>통화마다 녹음(끄실 수 있습니다)과 요약, 그리고 무엇을 근거로 답했는지가 기록으로 남습니다.
          그 기록의 권리는 {owner}께 있고, 언제든 전부 내려받으실 수 있습니다.
          <a href="../terms.html#sec-9">약관 제8조 &rarr;</a></li>
        <li>응대 문장은 미국에 있는 언어모델이 만듭니다. 고객 기록, 예약, 통화 녹취는 서울의 운영 서버에
          저장됩니다. <a href="../security.html#where">데이터가 어디에 있는가 &rarr;</a></li>
      </ul>
    </div>
  </div>
</section>

<section class="t-md sec-light bg-paper" id="crm">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>남는 것</span><span class="line"></span></div>
    <h2 class="h2 reveal">통화가 끝나면<br>이 항목들이 채워져 있습니다.</h2>
    <p class="sub reveal" style="max-width:none;">{name}용 CRM에는 {name}의 항목이 들어 있습니다.
      범용 CRM의 빈칸을 우리 업종에 맞게 고쳐 가며 쓰는 것이 아니라, 첫날부터 우리 업종의 말로 적힙니다.</p>
    <div class="illrow reveal">{ill_card}<div class="fieldgrid" style="margin-top:0;">{fields}</div></div>
  </div>
</section>
{playbook}
<section class="t-md sec-dark bg-grid" id="pipeline">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>진행 단계</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">문의가 어디까지 왔는지<br>한 줄로 보입니다.</h2>
    <div class="pipe reveal">{stages}</div>
    <div class="illwide reveal">{ill_pipe}</div>
  </div>
</section>

<section class="packcard t-md sec-dark bg-grid" id="the-pack">
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
</section>

<section class="t-md sec-light2" id="others">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>다른 업종</span><span class="line"></span></div>
    <h2 class="h2 reveal">우리 업종이 여기 없어도<br>대부분 만들 수 있습니다.</h2>
    <div class="photowall reveal">{others_photos}</div>
    <div class="otherwall reveal">{others}</div>
  </div>
</section>

<section class="founding t-xl bg-aurora" id="start">
  <div class="grainlayer grain" aria-hidden="true"></div>
  <div class="wrap">
    <div class="illrow reveal"><div>
    <h2 class="h2 onDark">{name} 요금표를 보내 주시면,<br>그 요금표로 답하는 것을 보여 드립니다.</h2>
    <p class="sub" style="max-width:none;">결제 정보는 받지 않습니다. 손님이 가장 자주 묻는 질문 열 개에
      그 요금표로 답하는 녹음을 영업일 하루 안에 만들어 보내 드리고, 아니다 싶으면 거기서 끝내시면 됩니다.</p>
    <div class="ctas">
      <a class="btn btn-teal" href="../get-started.html">{name} 견적 받기<span class="cir">&#8599;</span></a>
      <a class="btn btn-ghostd" href="../pricing.html">먼저 요금부터 보기</a>
    </div></div>{ill_morning}</div>
  </div>
</section>

{FOOT}
</main>

<div class="stickycta"><div class="wrap"><span class="msg">{name} 요금표로 만든 응대를
  <b>먼저 들어 보고 결정하세요.</b></span><a class="btn btn-teal" href="../get-started.html">견적 받기<span class="cir">&#8599;</span></a></div></div>
"""


PB = """
<section class="t-md sec-light bg-paper" id="playbook">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow light"><i></i>플레이북</span><span class="line"></span></div>
    <h2 class="h2 reveal">문마다 무엇을 받아 적고,<br>어떤 업무가 되는가.</h2>
    <p class="lead reveal">{lead}</p>

    <div class="trio reveal" style="margin-top:30px;">
      <div><b>✆ AI 전화</b><p>{phone}</p></div>
      <div><b>💬 홈페이지 채팅</b><p>{chat}</p></div>
      <div><b>✓ 메신저</b><p>{msg}</p></div>
    </div>

    <h3 class="h3 reveal" style="margin-top:34px;">남는 기록</h3>
    <div class="dtwrap reveal"><table class="dtable">
      <thead><tr><th>항목</th><th>출처</th><th>확인 방법</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>

    <h3 class="h3 reveal" style="margin-top:30px;">준비되는 업무</h3>
    <ul class="kolist reveal">{tasks}</ul>

    <h3 class="h3 reveal" style="margin-top:30px;">사람이 판단하는 것</h3>
    <ul class="kolist reveal">{human}</ul>

    <h3 class="h3 reveal" style="margin-top:30px;">전·후</h3>
    <div class="trio reveal">
      <div><b>전</b><p>{before}</p></div>
      <div><b>후</b><p>{after}</p></div>
      <div><b>첫 14일</b><p>{days}</p></div>
    </div>
  </div>
</section>
"""


def build_playbook(t):
    """playbook 데이터가 있는 업종에만 절을 렌더한다.

    내용은 전부 그 업종 dict 에 이미 있는 것 - 통화 대사, 거부 목록,
    CRM 항목과 단계 - 의 재배치다. 마지막 칸의 파일럿 14일·전액 환불·
    첫 달 일할 계산은 사이트 공통의 사실이라 여기서 한 번만 조립한다.
    """
    pb = t.get('playbook')
    if not pb:
        return ''
    rows = ''.join('<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>' % r
                   for r in pb['record'])
    tasks = ''.join('<li><b>%s</b>%s &rarr; %s</li>' % k for k in pb['tasks'])
    human = ''.join('<li><b>%s</b>%s</li>' % h for h in pb['human'])
    days = ('파일럿은 첫 14일입니다. 판단 근거는 실제 응대 기록 &mdash; %s &mdash; 이고, '
            '아니다 싶으시면 전액 환불입니다. 비용은 요금제 그대로이고, '
            '첫 달만 일할로 계산합니다.' % pb['proof'])
    # 아래 한 줄의 숫자는 pricing.json 에서 온다. 여기에 손으로 적지 않는다.
    scale = [p for p in PR['plans'] if p['id'] == 'scale'][0]
    voice = [u for u in PR['usage'] if u['id'] == 'voiceMinutes'][0]
    disc = PR.get('discount') or {}
    price = ('AI 전화 포함 Scale {0:,}원/월 + 통화 분당 {1:,}원, 부가세 별도'
             .format(scale['price']['KRW'], voice['unitPrice']['KRW']))
    if disc.get('active'):
        price += ' &middot; 처음 %d개월 %d%%' % (disc['months'], disc['percent'])
    days += ('<br><br>%s. <a href="../checkout.html?plan=scale">Scale 주문서 열기 &rarr;</a>'
             % price)
    return PB.format(lead=pb['lead'], phone=pb['phone'], chat=pb['chat'],
                     msg=pb['msg'], rows=rows, tasks=tasks, human=human,
                     before=pb['before'], after=pb['after'], days=days)


def other_photos(t):
    """같은 묶음의 업종을 먼저, 그다음 나머지로 여덟 곳. 사진은 각 업종 페이지의 대표 사진."""
    mine = [g for _, g in GROUPS if t['slug'] in g]
    order = [s for s in (mine[0] if mine else []) if s != t['slug']]
    order += [o['slug'] for o in TRADES if o['slug'] not in order and o['slug'] != t['slug']]
    by = {o['slug']: o for o in TRADES}
    out = []
    for s in order[:8]:
        o = by[s]
        out.append('<a href="./%s.html"><img src="%s?auto=compress&amp;cs=tinysrgb&amp;w=560&amp;h=420&amp;fit=crop" alt="" loading="lazy" decoding="async" width="560" height="420"><b>%s</b></a>'
                   % (o['slug'], o['photo'], o['name']))
    return ''.join(out)


def build_trade(t):
    turns = []
    for who, when, what in t['call']:
        side = 'sr' if who == 'Saleringo' else 'us'
        bub = 'ai' if side == 'sr' else 'user'
        turns.append('<div class="nl %s"><span class="t"><em>%s</em>%s</span>'
                     '<div class="bub %s">%s</div></div>' % (side, who, when, bub, what))
    refuse = ''.join('<li><b>%s</b>%s</li>' % (a, b) for a, b in t['refuse'])
    fields = ''.join('<span>%s</span>' % f for f in t['fields'])
    stages = '<i>&rarr;</i>'.join('<b>%s</b>' % s for s in t['stages'])
    others = ''.join('<a href="./%s.html">%s</a>' % (o['slug'], o['name'])
                     for o in TRADES if o['slug'] != t['slug'])

    ctx = dict(t)
    w = t.get('when') or {}
    ctx.update(when_eyebrow=w.get('eyebrow', '그날 밤의 통화'),
               when_h2=w.get('h2', '%s이 자는 동안<br>이렇게 흘러갑니다.' % t['owner']),
               when_tt=w.get('tt', '영업 종료 후'), when_badge=w.get('badge', '문 닫은 시간'))
    ctx.update(NAV=NAV, FOOT=FOOT, turns=''.join(turns), refuse=refuse,
               fields=fields, stages=stages, others=others,
               playbook=build_playbook(t))
    ctx.update(ill_night=illus.figure(illus.night('ko'), '하루 24시간 중 문을 연 시간은 9시간 안팎입니다. 나머지 15시간에도 전화는 옵니다.'),
               ill_handoff=illus.figure(illus.handoff('ko', question=t['call'][0][2][:40]), '요금표에 있으면 답하고, 판단이나 안전이 걸리면 사람에게 넘깁니다. 넘길 때는 대화 전체와 받아 적은 항목이 함께 갑니다.'),
               ill_card=illus.figure(illus.card('ko', rows=[(f, None, '통화에서') for f in t['fields'][:4]]), '통화가 끝나면 이 카드가 채워져 있습니다. 항목마다 어디서 나온 값인지가 붙습니다.'),
               ill_pipe=illus.figure(illus.pipeline('ko', stages=t['stages'][:5]), '{name}의 단계 그대로입니다. 지금 몇 건이 어느 단계에 있는지 한눈에 보입니다.'.format(name=t['name'])),
               ill_morning=illus.figure(illus.morning('ko'), '밤사이 받은 것이 아침 화면에 이렇게 놓여 있습니다.'),
               others_photos=other_photos(t))
    body = TPL.format(**ctx)
    page('industries/%s.html' % t['slug'],
         '%s AI 응대 &mdash; 밤에 걸려 온 전화가 예약이 되는 방법' % t['name'],
         '%s에 걸려 오는 문의를 AI가 대신 받아 예약을 잡고 고객 카드로 남깁니다. '
         '통화 예시, 하지 않는 일, CRM에 남는 항목을 그대로 실었습니다.' % t['name'],
         body, css=CSS, grade='voice',
         image=t['photo'] + '?auto=compress&amp;cs=tinysrgb&amp;fit=crop&amp;w=1200&amp;h=630',
         crumbs=[('홈', 'index.html'), ('업종', 'industries.html'),
                 (t['name'], 'industries/%s.html' % t['slug'])])


GROUPS = [
    ('의료 &middot; 요양', ['dental', 'clinics', 'veterinary', 'senior-care']),
    ('배우고 가꾸는 곳', ['academies', 'universities', 'salons', 'fitness']),
    ('집과 건물', ['home-services', 'pest-control', 'property-management', 'real-estate']),
    ('차 · 짐 · 장비', ['auto-repair', 'movers', 'self-storage', 'equipment-rental']),
    ('모이는 곳', ['restaurants', 'venues', 'stays', 'golf']),
    ('전문직 &middot; 공공', ['legal', 'public-sector', 'funeral-homes']),
    ('온라인 &middot; 여러 점포', ['ecommerce', 'franchise']),
]

WALL_CSS = """
  .hero{display:block;padding:150px 0 60px;}
  .wallgrp{margin-top:44px;}
  .wallgrp h2{font-size:var(--fs-lead);color:var(--l-ink);
    padding-bottom:14px;border-bottom:1px solid #E3E7EE;}
  .wallrow{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:20px;}
  @media (max-width:820px){.wallrow{grid-template-columns:1fr;}}
  .wallcard{display:block;padding:26px 24px;border:1px solid #D5DBE4;border-radius:8px;
    text-decoration:none;transition:all .35s var(--ease);}
  .wallcard:hover{border-color:var(--teal);background:rgba(11,120,120,.05);}
  .wallcard img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:8px;margin-bottom:14px;background:#E2DDD3;}
  .wallcard b{display:block;font-size:var(--fs-lead);color:var(--l-ink);}
  .wallcard span{display:block;margin-top:9px;font-size:var(--fs-sm);line-height:1.75;
    color:var(--l-tx2);}
  .wallcard em{display:block;margin-top:14px;font-style:normal;font-size:var(--fs-sm);
    color:var(--teal);font-weight:700;}
"""

WALL = """
<header class="hero nophoto sec-dark bg-aurora">
  <div class="scrim" aria-hidden="true"></div>
  {NAV}
  <div class="wrap hero-inner">
    <span class="eyebrow"><i></i>업종</span>
    <h1 style="margin-top:24px;">업종마다 걸려 오는 전화가 다릅니다.<br>그래서 답도 달라야 합니다.</h1>
    <p class="sub">치과에 밤에 걸려 오는 전화와 정비소에 오후에 걸려 오는 전화는 다른 전화입니다.
      묻는 것도, 말하면 안 되는 것도 다릅니다. 업종을 고르고, 그 통화를 그대로 읽어 보십시오.</p>
  </div>
</header>

<main>

<section class="t-md sec-dark bg-grid" id="whytrade">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>왜 업종별인가</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">같은 AI에 요금표만<br>바꿔 넣는 것이 아닙니다.</h2>
    <p class="sub reveal" style="max-width:none;">「업종 맞춤」이라고 적어 두고 실제로는 인사말만
      바꾸는 제품이 많습니다. 그러면 치과에서도 &ldquo;문의 주셔서 감사합니다&rdquo;로 시작해
      &ldquo;담당자가 연락드리겠습니다&rdquo;로 끝납니다. 업종이 달라지면 바뀌어야 하는 것은
      인사말이 아니라 아래 셋입니다.</p>

    <div class="trio reveal" style="margin-top:34px;">
      <div><b>무엇을 묻는가</b><p>치과에는 &ldquo;씌운 게 빠졌는데 내일 되나요&rdquo;가 오고,
        정비소에는 &ldquo;시동이 안 걸리는데 얼마쯤 나올까요&rdquo;가 옵니다. 학원에는
        아이가 잠든 뒤 학부모가 겁니다. 묻는 것이 다르면 되물어야 할 것도 다릅니다.</p></div>
      <div><b>말하면 안 되는 것이 무엇인가</b><p>이것이 가장 중요합니다. 치과에서 병명을 말하면
        의료법 위반이고, 학원에서 합격 가능성을 말하면 나중에 책임을 집니다. 정비소는 차를
        보지 않고 원인을 단정하면 안 되고, 웨딩홀은 날짜를 확정하면 중복 예약이 납니다.
        업종마다 이 목록이 다르고, 저희는 그것을 먼저 만들어 드립니다.</p></div>
      <div><b>무엇을 기록해야 하는가</b><p>치과는 신환·구환 구분과 문의한 시술 부위가 남아야 하고,
        부동산은 희망 조건과 예산대가 남아야 합니다. 일반 CRM의 빈칸에 이것을 직접 채워 넣는
        작업이 도입의 절반이고, 도입은 대개 거기서 멈춥니다.</p></div>
    </div>

    <p class="seccap reveal" style="margin-top:22px;">지금 운영 중인 팩은 <b>예식장·행사장과 의원 두 가지</b>입니다. 아래 나머지 업종은
      항목·단계·하지 않는 말의 초안까지 준비해 두었고, 요청하시면 그 업종으로 만들어 드립니다. 골라 들어가시면 그 업종의 통화 예시 하나와, 그 업종에서 AI가
      하지 않는 것, 그리고 통화 뒤에 남는 CRM 항목을 보실 수 있습니다.
      <a class="lnk" href="./examples.html">여섯 업종의 통화는 한 페이지에 모아</a> 두었습니다.</p>
  </div>
</section>

<section class="t-md sec-light bg-paper" id="all">
  <div class="wrap">
    {groups}
  </div>
</section>

<section class="t-md sec-dark bg-grid" id="notlisted">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>여기 없는 업종</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">목록에 없다고<br>안 되는 것은 아닙니다.</h2>
    <p class="sub reveal" style="max-width:none;">업종별 CRM이란 결국 항목과 단계, 그리고 하면 안 되는 말의
      목록입니다. 요금표와 영업시간, 그리고 &ldquo;이 말은 절대 하면 안 된다&rdquo;는 것 몇 가지만
      알려 주시면 만들 수 있습니다. 한의원, 세무사무소, 사진 스튜디오, 산후조리원, 카센터 프랜차이즈처럼 위 목록에 없는 곳도 같은 방식입니다.</p>
    <div class="ctas reveal">
      <a class="btn btn-teal" href="./get-started.html">우리 업종으로 만들어 보기<span class="cir">&#8599;</span></a>
    </div>
  </div>
</section>

{FOOT}
</main>
"""

LEAD = {
    'dental': '밤에 걸려 오는 신환 전화. 증상은 듣되 진단은 하지 않고, 요금표의 금액으로 예약까지 잡습니다.',
    'clinics': '가격부터 묻는 전화. 효과를 약속하지 않고, 심의받지 않은 말을 만들지 않습니다.',
    'veterinary': '급한 전화와 급하지 않은 전화를 나눕니다. 응급 신호가 나오면 즉시 사람에게 넘깁니다.',
    'senior-care': '가장 어려운 전화입니다. 본인부담금을 계산하지 않고, 사람에게 잘 넘기는 것에 집중합니다.',
    'salons': '시술 중에 오는 예약 전화. 소요 시간을 넉넉히 잡아 캘린더에 그대로 넣습니다.',
    'fitness': '밤에 결심하고 거는 전화. 그날 안에 체험 예약까지 끝냅니다.',
    'academies': '아이가 잠든 뒤 걸려 오는 학부모 전화. 레벨테스트 예약까지 잡습니다.',
    'auto-repair': '리프트 아래에서는 못 받는 견적 전화. 범위까지만 말하고 입고를 잡습니다.',
    'real-estate': '임장 나가 있을 때 오는 매물 전화. 조건을 협의하지 않고 임장만 잡습니다.',
    'venues': '&ldquo;그 날짜 되나요&rdquo; 한 문장. 가능 여부와 상담 예약을 그 자리에서 답합니다.',
    'home-services': '보일러가 멈춘 집은 기다리지 않습니다. 원인은 단정하지 않고, 출장 시간과 기본 비용만 말하고 방문을 잡습니다.',
    'pest-control': '벌레를 본 사람은 그 밤에 겁니다. 박멸을 약속하지 않고, 시공 일정과 금액 범위만 말합니다.',
    'property-management': '누수와 정전은 근무 시간에 맞춰 일어나지 않습니다. 급한 신고만 골라 당직에게 바로 넘깁니다.',
    'movers': '짐을 보지 않고 금액을 확정하지 않습니다. 범위만 말하고 방문 견적을 잡습니다.',
    'restaurants': '스무 명 회식 전화가 점심 피크에 옵니다. 좌석 현황에서만 잡고, 알레르기는 주방으로 넘깁니다.',
    'stays': '직접 예약이면 수수료가 없습니다. 밤에 온 문의를 그 밤에 받아 객실을 잡습니다.',
    'golf': '주말 티타임은 먼저 답하는 곳이 가져갑니다. 남은 시간에서만 잡습니다.',
    'funeral-homes': '가장 급하고 가장 조심스러운 전화입니다. 상품을 권하지 않고 사람에게 바로 넘깁니다.',
    'legal': '사건 전망을 말하지 않습니다. 사실만 받아 적고 상담 일정을 잡습니다.',
    'universities': '원서 기간에 같은 질문이 수백 통 옵니다. 공고된 것만 답하고, 판단이 필요하면 담당자에게 넘깁니다.',
    'public-sector': '민원인은 이미 두 번 돌려진 뒤에 겁니다. 판단하지 않고 담당 부서를 정확히 찾아 줍니다.',
    'self-storage': '무인으로 돌릴수록 받을 사람이 없습니다. 평수와 공실, 금액을 그 자리에서 답합니다.',
    'equipment-rental': '내일 쓸 장비는 오늘 밤에 정해집니다. 재고에 있는 것만 잡습니다.',
    'ecommerce': '결제 직전의 질문 세 가지에 밤에도 답합니다. 재고와 출고일은 지어내지 않습니다.',
    'franchise': '가맹 문의와 클레임이 같은 번호로 옵니다. 예상 수익은 말하지 않고, 갈라서 담당자에게 보냅니다.',
}


def build_wall():
    by = {t['slug']: t for t in TRADES}
    out = []
    for title, slugs in GROUPS:
        cards = ''.join(
            '<a class="wallcard" href="./industries/%s.html"><img src="%s?auto=compress&amp;cs=tinysrgb&amp;w=560&amp;h=315&amp;fit=crop" alt="" loading="lazy" decoding="async" width="560" height="315"><b>%s</b><span>%s</span>'
            '<em>통화 읽어 보기 &rarr;</em></a>' % (s, by[s]['photo'], by[s]['name'], LEAD[s]) for s in slugs)
        out.append('<div class="wallgrp reveal"><h2>%s</h2><div class="wallrow">%s</div></div>'
                   % (title, cards))
    page('industries.html',
         '업종별 AI 응대 &mdash; 우리 업종의 전화는 어떻게 받아야 하는가',
         '치과, 의원, 학원, 미용실, 동물병원, 정비소, 부동산, 웨딩홀, 요양, 헬스장. '
         '업종마다 다른 문의와 다른 금지 사항에 맞춘 AI 응대와 CRM.',
         WALL.format(NAV=NAV, FOOT=FOOT, groups=''.join(out)), css=WALL_CSS, grade='trust',
         crumbs=[('홈', 'index.html'), ('업종', 'industries.html')])


for t in TRADES:
    build_trade(t)
build_wall()
print('wrote %d trade pages and the wall' % len(TRADES))
