# -*- coding: utf-8 -*-
"""남은 여섯 장 - 검증, 회사, 해외 대상, 고르기 전에, 대화 보기, 업종별 사례.

영문 쪽의 같은 페이지를 옮긴 것이 아니다. 특히 두 장은 내용이 완전히 다르다.

  · cross-border.html 은 영문 쪽에서 "여러 나라에 파는 회사"를 상대로 쓴
    글이다. 한국에서 이 페이지를 읽는 사람은 반대 방향이다. 한국에서
    만들어 해외로 파는 회사, 또는 한국에 오는 외국인 손님을 받는 가게다.
    그래서 시차와 언어, 그리고 결제 통화를 그 방향으로 다시 썼다.

  · ai-answering-service.html 은 "무엇을 사는지 모르고 사는 것"을 막는
    페이지다. 한국에서 팔리는 것은 세 가지 - 단순 ARS, 전화대행, 그리고
    AI 응대 - 이고, 셋이 할 수 있는 일이 다르다. 업체에 물어봐야 할 질문
    일곱 개를 그대로 적었다. 우리에게 물어도 되는 질문이다.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.dirname(os.path.dirname(HERE)))
from shell import page, NAV, FOOT
from trades import TRADES
from trades2 import TRADES2

ALL = TRADES + TRADES2
NB = '&nbsp;'
PH = 'https://images.pexels.com/photos/%s/pexels-photo-%s.jpeg'

CSS = """
  .hero{display:block;padding:0 0 70px;}
  .hero.nophoto{padding:150px 0 60px;}
  .hero-inner{padding-top:130px;}
  .hero.nophoto .hero-inner{padding-top:0;}
  .heroband{max-width:820px;}
  .kolist{margin-top:26px;display:grid;gap:16px;}
  .kolist li{list-style:none;padding-left:26px;position:relative;
    font-size:var(--fs-body);line-height:1.8;color:var(--tx2);}
  .kolist li::before{content:"";position:absolute;left:2px;top:.72em;width:9px;height:9px;
    border-radius:50%;border:1.5px solid var(--teal);}
  .kolist li b{display:block;color:#fff;margin-bottom:4px;}
  .sec-light .kolist li,.bg-paper .kolist li,.sec-light2 .kolist li{color:var(--l-tx2);}
  .sec-light .kolist li b,.bg-paper .kolist li b,.sec-light2 .kolist li b{color:var(--l-ink);}
  .trio{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:34px;}
  @media (max-width:880px){.trio{grid-template-columns:1fr;}}
  .trio > div{padding:26px 24px;border:1px solid var(--hair-d);border-radius:12px;}
  .trio b{display:block;font-size:var(--fs-lead);color:#fff;}
  .trio p{margin-top:10px;font-size:var(--fs-sm);color:var(--tx2);line-height:1.75;}
  .sec-light .trio > div,.bg-paper .trio > div{border-color:#D5DBE4;}
  .sec-light .trio b,.bg-paper .trio b{color:var(--l-ink);}
  .sec-light .trio p,.bg-paper .trio p{color:var(--l-tx2);}
  .pipe{display:flex;flex-wrap:wrap;gap:10px;margin-top:28px;align-items:center;}
  .pipe b{padding:11px 18px;border:1px solid var(--hair-d);border-radius:8px;
    font-size:var(--fs-sm);font-weight:600;color:#fff;}
  .pipe i{font-style:normal;color:var(--teal);}
  .nightline{display:grid;gap:16px;padding:26px 24px;}
  .nl{display:grid;grid-template-columns:104px 1fr;gap:16px;align-items:start;}
  .nl .t{font-size:var(--fs-2xs);letter-spacing:.14em;color:rgba(255,255,255,.5);
    text-transform:uppercase;padding-top:9px;}
  .nl .t em{display:block;font-style:normal;color:rgba(255,255,255,.66);
    letter-spacing:.02em;text-transform:none;font-size:var(--fs-xs);}
  @media (max-width:640px){.nl{grid-template-columns:1fr;gap:6px;}.nl .t{padding-top:0;}}
  .cmp{width:100%;margin-top:34px;border-collapse:collapse;}
  .cmp th,.cmp td{padding:16px 14px;text-align:left;font-size:var(--fs-sm);
    border-bottom:1px solid var(--hair-d);vertical-align:top;line-height:1.7;}
  .cmp th{color:#fff;font-weight:600;}
  .cmp td{color:var(--tx2);}
  .cmp td b{color:#fff;}
  .cmpwrap{overflow-x:auto;}
  @media (max-width:700px){.cmp{min-width:640px;}}
  .qlist{margin-top:30px;display:grid;gap:0;}
  .qlist .q{padding:22px 0;border-top:1px solid #E3E7EE;}
  .qlist .q b{display:block;font-size:var(--fs-lead);color:var(--l-ink);}
  .qlist .q p{margin-top:9px;font-size:var(--fs-sm);color:var(--l-tx2);line-height:1.8;}
  .exwall{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:30px;}
  @media (max-width:820px){.exwall{grid-template-columns:1fr;}}
  .excard{display:block;padding:24px 22px;border:1px solid #D5DBE4;border-radius:12px;
    text-decoration:none;transition:all .35s var(--ease);}
  .excard:hover{border-color:var(--teal);background:rgba(23,189,189,.05);}
  .excard b{display:block;font-size:var(--fs-lead);color:var(--l-ink);}
  .excard span{display:block;margin-top:8px;font-size:var(--fs-sm);line-height:1.75;
    color:var(--l-tx2);}
  .excard em{display:block;margin-top:12px;font-style:normal;font-size:var(--fs-sm);
    color:var(--teal);font-weight:700;}
"""


def hero_photo(photo, kicker, h1, sub, cta1, cta2):
    p = PH % (photo, photo)
    return ('<header class="hero photohero">\n'
            '  <div class="bgimg" aria-hidden="true">\n'
            '    <img class="ph" src="%s?auto=compress&amp;cs=tinysrgb&amp;w=1600" alt=""\n'
            '         width="1900" height="1425" loading="eager" fetchpriority="high" decoding="async"\n'
            '         srcset="%s?auto=compress&amp;cs=tinysrgb&amp;w=640 640w, '
            '%s?auto=compress&amp;cs=tinysrgb&amp;w=1024 1024w, '
            '%s?auto=compress&amp;cs=tinysrgb&amp;w=1600 1600w"\n'
            '         sizes="(max-width:900px) 100vw, 60vw">\n'
            '  </div>\n'
            '  <div class="scrim" aria-hidden="true"></div>\n'
            '  <div class="tint" aria-hidden="true"></div>\n'
            '  <div class="grainlayer grain" aria-hidden="true"></div>\n'
            '  %s\n'
            '  <div class="wrap hero-inner">\n'
            '    <div class="heroband hero-panel">\n'
            '      <span class="eyebrow"><i></i>%s</span>\n'
            '      <h1>%s</h1>\n'
            '      <p class="sub">%s</p>\n'
            '      <div class="ctas">%s%s</div>\n'
            '    </div>\n  </div>\n</header>' % (p, p, p, p, NAV, kicker, h1, sub, cta1, cta2))


def hero_plain(kicker, h1, sub):
    return ('<header class="hero nophoto sec-dark bg-aurora">\n'
            '  <div class="scrim" aria-hidden="true"></div>\n  %s\n'
            '  <div class="wrap hero-inner">\n'
            '    <span class="eyebrow"><i></i>%s</span>\n'
            '    <h1 style="margin-top:24px;">%s</h1>\n'
            '    <p class="sub">%s</p>\n  </div>\n</header>' % (NAV, kicker, h1, sub))


def sec(cls, sid, eyebrow, h2, lead, inner='', dark=True):
    return ('<section class="%s" id="%s">\n  <div class="wrap">\n'
            '    <div class="secrule reveal"><span class="eyebrow"><i></i>%s</span>'
            '<span class="line"></span></div>\n'
            '    <h2 class="h2%s reveal">%s</h2>\n'
            '    <p class="sub reveal" style="max-width:none;">%s</p>\n'
            '%s  </div>\n</section>' % (cls, sid, eyebrow, ' onDark' if dark else '',
                                        h2, lead, inner))


def ul(items):
    return ('    <ul class="kolist reveal">' +
            ''.join('<li><b>%s</b>%s</li>' % (a, b) for a, b in items) + '</ul>\n')


def trio(items):
    return ('    <div class="trio reveal">' +
            ''.join('<div><b>%s</b><p>%s</p></div>' % (a, b) for a, b in items) + '</div>\n')


def pipe(items):
    return ('    <div class="pipe reveal">' +
            '<i>&rarr;</i>'.join('<b>%s</b>' % s for s in items) + '</div>\n')


def closer(h2, lead):
    return ('<section class="founding t-xl bg-aurora" id="start">\n'
            '  <div class="grainlayer grain" aria-hidden="true"></div>\n'
            '  <div class="wrap">\n'
            '    <h2 class="h2 onDark reveal">%s</h2>\n'
            '    <p class="sub reveal" style="max-width:none;">%s</p>\n'
            '    <div class="ctas reveal">\n'
            '      <a class="btn btn-teal" href="./get-started.html">우리 조건으로 견적 받기'
            '<span class="cir">&#8599;</span></a>\n'
            '      <a class="btn btn-ghostd" href="./pricing.html">요금부터 보기</a>\n'
            '    </div>\n  </div>\n</section>' % (h2, lead))


# ══ 1 · 답변 검증 ════════════════════════════════════════════════════════
verified = '\n\n'.join([
 hero_photo('6665032', '답변 검증 방식',
  '지어낸 답 하나면<br>나머지가 다 소용없습니다.',
  'AI가 없는 가격을 말하거나, 없는 시간에 예약을 잡거나, 하면 안 되는 말을 하면 '
  '그 손해는 전부 그 가게가 떠안습니다. 그래서 답할 수 있는 범위를 좁게 잠가 두었습니다.',
  '<a class="btn btn-teal" href="#life">답변 하나를 따라가 보기<span class="cir">&darr;</span></a>',
  '<a class="btn btn-ghostd" href="./security.html">보안 보기</a>'),
 '<main>',
 sec('t-md sec-dark bg-grid', 'life', '답변 하나가 만들어지기까지',
     '네 번 걸러진 뒤에<br>입 밖으로 나갑니다.',
     '아래 네 단계 중 어디에서든 막히면, 그 답은 나가지 않고 &ldquo;확인 후 연락드리겠습니다&rdquo;가 '
     '대신 나갑니다.',
     pipe(['질문 이해', '등록된 자료에서 찾기', '금지 규칙 검사', '답변 또는 사람에게'])),
 sec('t-md sec-dark bg-spot', 'refuse', '하지 않는 일',
     '기능을 끄는 것이 아니라<br>처음부터 막아 둡니다.', '',
     ul([('없는 것을 만들지 않습니다.', '등록된 요금표와 서비스 목록에 없으면 답하지 않습니다. 비슷한 것으로 대신하지도 않습니다.'),
         ('판단하지 않습니다.', '진단, 법률 판단, 사건 전망, 합격 가능성 같은 것은 사람만 합니다.'),
         ('사람인 척하지 않습니다.', '물어보시면 AI라고 답합니다.'),
         ('없는 시간에 예약을 잡지 않습니다.', '캘린더의 빈 시간에서만 잡습니다. 중복 예약은 손님을 돌려보내게 됩니다.'),
         ('안전이 걸리면 붙잡지 않습니다.', '응급 증상, 가스 냄새, 누수 같은 말이 나오면 즉시 사람에게 돌립니다.')])),
 sec('t-md sec-light bg-paper', 'audit', '감사 기록',
     '왜 그렇게 답했는지가<br>전부 남습니다.', '',
     ul([('답변마다 근거가 붙습니다.', '요금표의 어느 항목을 보고 그 금액을 말했는지 기록됩니다.'),
         ('막힌 것도 기록됩니다.', '무엇을 물었는데 왜 답하지 않았는지가 남습니다. 이것이 규칙을 고칠 자료가 됩니다.'),
         ('내려받을 수 있습니다.', '기록은 제품의 일부입니다. 요청해야 주는 것이 아닙니다.'),
         ('저희가 임의로 열어 보지 않습니다.', '장애 조사처럼 필요한 경우에만, 접근 기록을 남기고 봅니다.')]),
     dark=False),
 closer('우리 규칙을 넣고<br>막히는지 시험해 보십시오.',
        '하면 안 되는 말 몇 가지만 알려 주시면, 그것을 물었을 때 어떻게 막히는지 보여 드립니다.'),
 FOOT, '</main>'])

page('verified-ai.html', '답변 검증 방식 &mdash; 지어내지 않게 막는 네 단계 | Saleringo',
     '등록된 자료에만 답하고, 판단하지 않고, 없는 시간에 예약하지 않습니다. '
     '무엇을 왜 답했는지와 왜 막았는지가 전부 기록으로 남습니다.',
     verified, css=CSS, grade='trust',
     image=(PH % ('6665032', '6665032')) + '?auto=compress&amp;cs=tinysrgb&amp;fit=crop&amp;w=1200&amp;h=630',
     crumbs=[('홈', 'index.html'), ('답변 검증 방식', 'verified-ai.html')])


# ══ 2 · 회사 소개 ════════════════════════════════════════════════════════
about = '\n\n'.join([
 hero_plain('회사 소개',
  '작은 회사입니다.<br>전화하면 사람이 받습니다.',
  '정직한마케팅 주식회사가 만듭니다. 대한민국 법인이고, 서울에 있습니다. '
  '크게 보이려고 쓰는 문장을 이 페이지에 넣지 않았습니다.'),
 '<main>',
 sec('t-md sec-dark bg-grid', 'people', '누가 만드는가',
     '판매 조직이 따로 없습니다.',
     '견적 문의에 답장을 쓰는 사람과 제품을 만드는 사람이 같습니다. '
     '지금 규모에서는 그 편이 정확하고, 규모가 커져도 이 부분은 바꾸지 않을 생각입니다.',
     ul([('법인', '정직한마케팅 주식회사 &middot; 대한민국 법인'),
         ('이메일', 'hello@saleringo.com &mdash; 사람이 읽고 사람이 답합니다.'),
         ('전화', '+82 70-5277-0820 &mdash; 저희 AI가 먼저 받습니다. 그것으로 판단하셔도 됩니다.'),
         ('서비스 지역', '한국어와 영어로 서비스합니다. 응대 자체는 30개 이상의 언어로 합니다.')])),
 sec('t-md sec-dark bg-spot', 'promise', '약속하는 것',
     '지킬 수 있는 것만<br>적습니다.', '',
     ul([('데이터는 그 가게의 것입니다.', '언제든 전부 내려받을 수 있고, 해지할 때 막지 않습니다.'),
         ('학습에 쓰지 않습니다.', '고객의 대화 내용을 모델 학습에 사용하지 않습니다. 계약서에 넣습니다.'),
         ('약정을 걸지 않습니다.', '위약금이 없습니다. 다음 달부터 청구가 멈춥니다.'),
         ('먼저 보여 드리고 받습니다.', '결제 전에 실제 응대를 만들어 보내 드립니다.')])),
 sec('t-md sec-light bg-paper', 'not-yet', '아직 못 하는 것',
     '이것도 같이 적습니다.',
     '못 하는 것을 안 적으면 나중에 그것이 거짓말이 됩니다. '
     '지금 상태를 그대로 적고, 바뀌면 이 문단을 고치겠습니다.',
     ul([('보안 인증이 없습니다.', 'ISMS-P, ISO 27001, SOC 2 중 어느 것도 아직 없습니다. 운영 이력이 쌓여야 받을 수 있습니다.'),
         ('가동률 보장(SLA)이 없습니다.', '제공할 수 있게 되면 수치와 함께 공개하겠습니다.'),
         ('이용약관의 법률 검토가 끝나지 않았습니다.', '저희가 직접 쓴 상태이고, 그 사실을 <a href="./terms.html">약관</a>에 적어 두었습니다.'),
         ('고객 사례를 아직 못 보여 드립니다.', '신생 회사입니다. 사이트의 모든 대화는 예시라고 표시해 두었습니다.')]),
     dark=False),
 closer('궁금한 것이 있으면<br>그냥 물어보십시오.',
        '영업 전화를 드리지 않습니다. 답만 드리고, 아니다 싶으시면 거기서 끝입니다.'),
 FOOT, '</main>'])

page('about.html', '회사 소개 &mdash; 전화하면 사람이 받는 작은 회사 | Saleringo',
     '정직한마케팅 주식회사가 만듭니다. 약속하는 것과 아직 못 하는 것을 함께 적었습니다. '
     '보안 인증과 SLA는 아직 없습니다.',
     about, css=CSS, grade='trust',
     crumbs=[('홈', 'index.html'), ('회사 소개', 'about.html')])


# ══ 3 · 고르기 전에 ══════════════════════════════════════════════════════
guide = '\n\n'.join([
 hero_plain('고르기 전에',
  '세 가지가 전부 &ldquo;AI 응대&rdquo;라는<br>이름으로 팔립니다.',
  '단순 ARS, 전화대행, 그리고 진짜 AI 응대. 셋 다 &ldquo;전화를 대신 받아 준다&rdquo;고 하는데 '
  '할 수 있는 일이 완전히 다릅니다. 계약하기 전에 이 표를 한 번 보십시오. '
  '저희를 고르지 않으셔도 됩니다.'),
 '<main>',
 sec('t-md sec-dark bg-grid', 'three', '세 가지',
     '무엇을 사는지<br>먼저 아셔야 합니다.', '',
     '    <div class="cmpwrap reveal"><table class="cmp">\n'
     '      <thead><tr><th>종류</th><th>하는 일</th><th>못 하는 일</th><th>대략 비용</th></tr></thead>\n'
     '      <tbody>\n'
     '        <tr><td><b>단순 ARS</b></td>'
     '<td>안내 멘트를 읽고 번호를 누르게 합니다. 녹음된 문장만 나갑니다.</td>'
     '<td>질문에 답하지 못합니다. 예약을 잡지 못합니다. 누가 왜 걸었는지 남지 않습니다.</td>'
     '<td>월 3만~10만원</td></tr>\n'
     '        <tr><td><b>전화대행</b></td>'
     '<td>사람이 받아서 메모를 남깁니다. 다시 걸어 달라고 전달합니다.</td>'
     '<td>우리 요금표를 모르니 견적을 못 냅니다. 캘린더에 예약을 넣지 못합니다. '
     '시술이나 서비스 내용을 답하지 못합니다.</td>'
     '<td>월 30만~80만원</td></tr>\n'
     '        <tr><td><b>AI 응대</b></td>'
     '<td>등록된 요금표로 답하고, 캘린더의 빈 시간에 예약을 잡고, 고객 카드를 남깁니다.</td>'
     '<td>판단이 필요한 것은 하지 않습니다. 진단, 법률 판단, 없는 가격은 사람에게 넘깁니다.</td>'
     '<td>월 11만~82만원</td></tr>\n'
     '      </tbody></table></div>\n'),
 sec('t-md sec-light bg-paper', 'ask', '업체에 물어볼 것',
     '이 일곱 개면<br>대부분 갈립니다.',
     '어느 업체를 고르시든 이 질문들을 그대로 물어보십시오. 저희에게 물으셔도 됩니다.',
     '    <div class="qlist reveal">\n'
     '      <div class="q"><b>1. 우리 요금표를 넣으면 그 금액으로 답하나요?</b>'
     '<p>못 한다면 그것은 안내 멘트이지 응대가 아닙니다. 손님이 가장 많이 묻는 것이 가격입니다.</p></div>\n'
     '      <div class="q"><b>2. 캘린더에 예약을 직접 넣나요, 메모만 남기나요?</b>'
     '<p>메모만 남기면 다음 날 사람이 다시 전화를 걸어야 합니다. 그러면 아무 일도 줄지 않습니다.</p></div>\n'
     '      <div class="q"><b>3. 하면 안 되는 말을 어떻게 막나요?</b>'
     '<p>&ldquo;학습시켜서 막는다&rdquo;는 답은 막는 것이 아닙니다. 규칙으로 잠그는지 물어보십시오.</p></div>\n'
     '      <div class="q"><b>4. 통화 녹취와 상담 기록을 내려받을 수 있나요?</b>'
     '<p>못 준다면 나갈 때 아무것도 못 가지고 나갑니다.</p></div>\n'
     '      <div class="q"><b>5. 우리 대화를 다른 고객 AI 학습에 쓰나요?</b>'
     '<p>계약서에 &ldquo;쓰지 않는다&rdquo;고 적혀 있는지 확인하십시오. 구두 약속은 소용없습니다.</p></div>\n'
     '      <div class="q"><b>6. 통화료가 얼마이고, 한도를 걸 수 있나요?</b>'
     '<p>분당 요금이 안 적혀 있으면 청구서를 받아 보기 전까지 모릅니다.</p></div>\n'
     '      <div class="q"><b>7. 약정과 위약금이 있나요?</b>'
     '<p>1년 약정을 요구한다면, 한 달 써 보고 판단할 기회를 주지 않겠다는 뜻입니다.</p></div>\n'
     '    </div>\n', dark=False),
 closer('저희에게도<br>위 일곱 개를 그대로 물어보십시오.',
        '답은 이 사이트에 다 적혀 있지만, 직접 물어보시는 편이 확실합니다.'),
 FOOT, '</main>'])

page('ai-answering-service.html',
     '고르기 전에 &mdash; ARS · 전화대행 · AI 응대는 무엇이 다른가 | Saleringo',
     '세 가지가 모두 AI 응대라는 이름으로 팔립니다. 할 수 있는 일과 비용을 비교한 표와, '
     '어느 업체에든 물어야 할 질문 일곱 개.',
     guide, css=CSS, grade='trust',
     crumbs=[('홈', 'index.html'), ('고르기 전에', 'ai-answering-service.html')])


# ══ 4 · 해외 대상 ════════════════════════════════════════════════════════
cross = '\n\n'.join([
 hero_photo('29123790', '해외 대상 사업',
  '한국이 잘 때<br>주문이 들어옵니다.',
  '해외로 파는 회사와 외국인 손님을 받는 가게는 같은 문제를 겪습니다. '
  '문의가 오는 시간에 답할 사람이 없다는 것입니다.',
  '<a class="btn btn-teal" href="#time">시차 문제부터<span class="cir">&darr;</span></a>',
  '<a class="btn btn-ghostd" href="./pricing.html">요금 보기</a>'),
 '<main>',
 sec('t-md sec-dark bg-grid', 'time', '시차',
     '미국이 일할 때<br>한국은 자고 있습니다.',
     '한국 시간 밤 열 시는 미국 동부의 아침 아홉 시입니다. 그쪽이 출근해서 문의를 보내는 시간이 '
     '이쪽이 문을 닫은 시간입니다. 다음 날 아침에 답장을 보내면 그때는 그쪽이 퇴근한 뒤이고, '
     '이렇게 하루에 한 번씩 주고받으면 견적 하나에 일주일이 걸립니다.',
     ul([('밤에 온 문의에 그 밤에 답합니다.', '가격과 배송 기간, 최소 주문 수량 같은 것은 등록해 두면 바로 나갑니다.'),
         ('상대 시간대로 회신 시간을 잡습니다.', '&ldquo;내일 오전&rdquo;이 누구의 오전인지 헷갈리지 않게 적습니다.'),
         ('판단이 필요한 것만 아침으로 넘깁니다.', '단가 협의나 계약 조건은 사람이 봐야 합니다.')])),
 sec('t-md sec-dark bg-spot', 'lang', '언어',
     '손님의 언어로 답하고,<br>기록은 한국어로 남습니다.',
     '영어로 온 문의에는 영어로 답합니다. 일본어면 일본어로, 중국어면 중국어로 답합니다. '
     '그런데 그 내용이 CRM에 남을 때는 한국어 요약이 함께 붙습니다. '
     '읽어야 하는 사람이 한국 사무실에 있기 때문입니다.',
     trio([('30개 이상 언어', '응대는 손님의 언어로 합니다.'),
           ('기록은 원문 + 한국어', '원문 그대로와 한국어 요약이 같이 남습니다.'),
           ('말투는 한 번만 정합니다', '언어가 달라도 하지 말아야 할 말은 똑같이 막힙니다.')])),
 sec('t-md sec-light bg-paper', 'money', '통화와 청구',
     '원화로 청구하고<br>세금계산서를 발행합니다.',
     '해외 고객을 상대하는 사업이라도 청구는 한국 법인 기준입니다. '
     '원화, 부가세 별도, 전자세금계산서. 달러로 받으실 필요가 없습니다.',
     ul([('요금은 원화입니다.', '환율에 따라 달라지지 않습니다.'),
         ('세금계산서가 나갑니다.', '사업자등록번호만 등록해 두시면 매달 자동으로 발행됩니다.'),
         ('통화료는 발신 지역별로 다릅니다.', '해외로 거는 통화가 있으면 계약 전에 지역별 단가를 문서로 드립니다.')]),
     dark=False),
 closer('어느 나라에서<br>몇 시에 문의가 오는지 알려 주십시오.',
        '그 시간대에 어떻게 받을지 설계해서, 예상 통화량과 금액을 같이 보내 드립니다.'),
 FOOT, '</main>'])

page('cross-border.html', '해외 대상 사업 &mdash; 한국이 잘 때 오는 문의 받기 | Saleringo',
     '해외로 파는 회사와 외국인 손님을 받는 가게를 위한 시차·언어 대응. '
     '30개 이상 언어로 답하고 기록은 한국어 요약과 함께 남습니다. 원화 청구, 세금계산서 발행.',
     cross, css=CSS, grade='voice',
     image=(PH % ('29123790', '29123790')) + '?auto=compress&amp;cs=tinysrgb&amp;fit=crop&amp;w=1200&amp;h=630',
     crumbs=[('홈', 'index.html'), ('해외 대상 사업', 'cross-border.html')])


# ══ 5 · 대화 한 건 보기 ══════════════════════════════════════════════════
def turn(who, when, what, ai=False):
    return ('<div class="nl %s"><span class="t"><em>%s</em>%s</span>'
            '<div class="bub %s">%s</div></div>'
            % ('sr' if ai else 'us', who, when, 'ai' if ai else 'user', what))


def window(title, note, closed, turns):
    return ('    <div class="appwin reveal" style="margin-top:30px;">\n'
            '      <div class="bar"><i></i><i></i><i></i>'
            '<span class="tt">%s</span><span class="illus">%s</span>'
            '<span class="closed">%s</span></div>\n'
            '      <div class="body nightline">%s</div>\n    </div>\n'
            % (title, note, closed, ''.join(turns)))


demo = '\n\n'.join([
 hero_photo('18441167', '대화 한 건 보기',
  '설명을 읽는 것보다<br>통화를 읽는 편이 빠릅니다.',
  '아래 세 가지는 각각 다른 상황입니다. 잘 풀리는 통화, 막히는 통화, '
  '그리고 기계가 물러나야 하는 통화. 세 번째가 가장 중요합니다.',
  '<a class="btn btn-teal" href="#good">읽어 보기<span class="cir">&darr;</span></a>',
  '<a class="btn btn-ghostd" href="./examples.html">업종별로 더 보기</a>'),
 '<main>',
 sec('t-md sec-dark bg-dusk', 'good', '잘 풀리는 통화',
     '물어본 것에 답하고,<br>시간을 잡고, 끝냅니다.',
     '가장 흔한 형태입니다. 요금표에 있는 질문이고, 캘린더에 자리가 있고, 손님이 결정합니다.',
     window('미용실 &mdash; <b>화요일 오후 2시</b>', '예시 &middot; 가상의 통화', '시술 중', [
       turn('손님', '2:12 PM', '토요일에 뿌리염색이랑 클리닉 같이 되나요? 시간 얼마나 걸려요?'),
       turn('Saleringo', '+19초', '두 가지 같이 하시면 <b>약 2시간</b> 잡으시면 됩니다. '
            '뿌리염색 <b>7만원</b>, 클리닉은 모발 상태에 따라 <b>8만원부터</b>입니다. '
            '토요일은 <b>오후 1시</b>와 <b>4시 30분</b>이 비어 있습니다.', True),
       turn('손님', '2:13 PM', '1시로 할게요.'),
       turn('Saleringo', '+7초', '토요일 오후 1시로 잡았습니다. 전날 확인 문자 보내 드리겠습니다.', True)])),
 sec('t-md sec-dark bg-grid', 'blocked', '막히는 통화',
     '모르는 것을<br>모른다고 말합니다.',
     '요금표에 없는 항목을 물었습니다. 비슷한 금액으로 대신 답하는 것이 가장 나쁜 선택입니다.',
     window('치과 &mdash; <b>목요일 밤 11시</b>', '예시 &middot; 가상의 통화', '진료 종료', [
       turn('환자', '11:07 PM', '앞니 라미네이트 한 개에 얼마인가요?'),
       turn('Saleringo', '+14초', '라미네이트는 등록된 요금표에 없어서 제가 금액을 말씀드릴 수 없습니다. '
            '내일 아침에 데스크에서 확인하고 연락드리도록 남겨 두겠습니다. '
            '연락 가능한 번호를 남겨 주시겠어요?', True),
       turn('환자', '11:08 PM', '010-0000-0000이요.'),
       turn('Saleringo', '+6초', '남겨 두었습니다. 내일 오전 중에 연락드리겠습니다.', True)])),
 sec('t-md sec-dark bg-spot', 'handover', '물러나는 통화',
     '판단이 필요한 순간,<br>기계는 빠집니다.',
     '증상을 말하는 순간부터는 사람의 일입니다. 이 통화에서 AI가 한 일은 예약이 아니라 연결입니다.',
     window('동물병원 &mdash; <b>일요일 밤 10시 51분</b>', '예시 &middot; 가상의 통화', '휴진', [
       turn('보호자', '10:51 PM', '강아지가 초콜릿을 먹은 것 같아요. 어떻게 해야 하나요?'),
       turn('Saleringo', '+6초', '초콜릿 섭취는 응급 상황일 수 있습니다. 지금 바로 야간 진료 가능한 곳으로 '
            '연결해 드리겠습니다. <b>먹은 양과 시간, 체중</b>을 기억해 두시고, '
            '억지로 토하게 하지 마십시오.', True),
       turn('보호자', '10:52 PM', '네, 부탁드립니다.'),
       turn('Saleringo', '+3초', '야간 담당 번호로 연결합니다. 잠시만 기다려 주십시오.', True)])),
 sec('t-md sec-light bg-paper', 'note', '읽으실 때',
     '전부 예시입니다.',
     '위 대화는 실제 고객 사례가 아닙니다. 각 업종의 요금표와 안전 지침을 넣었을 때 '
     '제품이 어떻게 답하는지 보여 주는 예시이고, 금액은 국내에서 흔히 제시되는 범위입니다. '
     '실제로 안내되는 금액은 직접 넣으신 요금표에서 나옵니다.', '', dark=False),
 closer('우리 요금표로 만든 통화를<br>직접 읽어 보십시오.',
        '업종과 요금표만 보내 주시면, 위와 같은 대화를 만들어 영업일 하루 안에 보내 드립니다.'),
 FOOT, '</main>'])

page('demo.html', '대화 한 건 보기 &mdash; 잘 풀리는 통화, 막히는 통화, 물러나는 통화 | Saleringo',
     '미용실 예약, 치과의 없는 가격, 동물병원 응급. 세 가지 상황에서 AI가 어떻게 답하고 '
     '어디에서 물러나는지 통화 그대로 실었습니다.',
     demo, css=CSS, grade='voice',
     image=(PH % ('18441167', '18441167')) + '?auto=compress&amp;cs=tinysrgb&amp;fit=crop&amp;w=1200&amp;h=630',
     crumbs=[('홈', 'index.html'), ('대화 한 건 보기', 'demo.html')])


# ══ 6 · 업종별 사례 ══════════════════════════════════════════════════════
cards = ''.join(
    '<a class="excard" href="./industries/%s.html"><b>%s</b>'
    '<span>%s</span><em>그 통화 읽어 보기 &rarr;</em></a>'
    % (t['slug'], t['name'], t['sub'].replace('&ldquo;', '“').replace('&rdquo;', '”'))
    for t in ALL)

examples = '\n\n'.join([
 hero_plain('업종별 사례',
  '스물다섯 업종,<br>스물다섯 개의 다른 전화.',
  '치과에 밤에 걸려 오는 전화와 정비소에 오후에 걸려 오는 전화는 다른 전화입니다. '
  '묻는 것도, 말하면 안 되는 것도 다릅니다. '
  '우리 업종을 골라서 그 통화가 맞는지 읽어 보십시오.'),
 '<main>',
 sec('t-md sec-light bg-paper', 'all', '전체',
     '고르시면 그 업종의<br>통화 하나를 그대로 보여 드립니다.', '',
     '    <div class="exwall reveal">' + cards + '</div>\n', dark=False),
 sec('t-md sec-dark bg-grid', 'note', '읽으실 때',
     '전부 예시입니다.',
     '실제 고객 사례가 아닙니다. 각 업종의 요금표와 안전 지침을 넣었을 때 제품이 '
     '어떻게 답하는지 보여 주는 예시이고, 금액은 국내에서 흔히 제시되는 범위입니다. '
     '고객 이름이나 상호가 실제와 같더라도 우연이며, 저희 고객이 아닙니다.'),
 closer('우리 업종이 없어도<br>대부분 만들 수 있습니다.',
        '요금표와 영업시간, 그리고 하면 안 되는 말 몇 가지만 알려 주시면 됩니다.'),
 FOOT, '</main>'])

page('examples.html', '업종별 사례 &mdash; 스물다섯 업종의 실제 통화 | Saleringo',
     '치과, 의원, 학원, 미용실, 정비소, 부동산 등 스물다섯 업종에서 밤에 걸려 오는 전화를 '
     '업종별로 그대로 실었습니다.',
     examples, css=CSS, grade='trust',
     crumbs=[('홈', 'index.html'), ('업종별 사례', 'examples.html')])

print('남은 여섯 장 완료')
