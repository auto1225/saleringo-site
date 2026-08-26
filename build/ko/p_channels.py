# -*- coding: utf-8 -*-
"""제품 페이지 다섯 장 - 플랫폼, AI 전화, 홈페이지 채팅, 카카오톡, 연동.

파일 이름은 영문 쪽과 같게 둔다. whatsapp.html 이 카카오톡 페이지가 되는 것이
어색해 보이지만, 두 언어의 같은 페이지가 짝을 이뤄야 언어 전환 버튼과
hreflang 이 서로를 찾는다. 주소는 짝을 맞추는 열쇠일 뿐이고, 화면에 보이는
것은 카카오톡이다.

내용은 옮기지 않았다. 영문 쪽은 WhatsApp 을 쓰는 나라를 상대로 쓴 글이고,
한국에서 메신저 문의는 카카오톡 채널과 네이버 톡톡으로 들어온다. 전화도
마찬가지다. 영문 쪽은 지역번호와 국제 발신을 설명하지만, 여기서 설명해야
할 것은 대표번호를 그대로 두고 못 받은 전화만 넘기는 방법이다.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.dirname(os.path.dirname(HERE)))
from shell import page, NAV, FOOT

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
  .nightline{display:grid;gap:16px;padding:26px 24px;}
  .nl{display:grid;grid-template-columns:104px 1fr;gap:16px;align-items:start;}
  .nl .t{font-size:var(--fs-2xs);letter-spacing:.14em;color:rgba(255,255,255,.42);
    text-transform:uppercase;padding-top:9px;}
  .nl .t em{display:block;font-style:normal;color:rgba(255,255,255,.66);
    letter-spacing:.02em;text-transform:none;font-size:var(--fs-xs);}
  @media (max-width:640px){.nl{grid-template-columns:1fr;gap:6px;}.nl .t{padding-top:0;}}
  .pipe{display:flex;flex-wrap:wrap;gap:10px;margin-top:28px;align-items:center;}
  .pipe b{padding:11px 18px;border:1px solid var(--hair-d);border-radius:8px;
    font-size:var(--fs-sm);font-weight:600;color:#fff;}
  .pipe i{font-style:normal;color:var(--teal);}
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
            '    </div>\n'
            '  </div>\n'
            '</header>' % (p, p, p, p, NAV, kicker, h1, sub, cta1, cta2))


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


def closer(h2, lead, root='./'):
    return ('<section class="founding t-xl bg-aurora" id="start">\n'
            '  <div class="grainlayer grain" aria-hidden="true"></div>\n'
            '  <div class="wrap">\n'
            '    <h2 class="h2 onDark reveal">%s</h2>\n'
            '    <p class="sub reveal" style="max-width:none;">%s</p>\n'
            '    <div class="ctas reveal">\n'
            '      <a class="btn btn-teal" href="%sget-started.html">우리 조건으로 견적 받기'
            '<span class="cir">&#8599;</span></a>\n'
            '      <a class="btn btn-ghostd" href="%spricing.html">요금부터 보기</a>\n'
            '    </div>\n  </div>\n</section>' % (h2, lead, root, root))


# ══ 1 · 플랫폼 ═══════════════════════════════════════════════════════════
platform = '\n\n'.join([
 hero_photo('8475194', '플랫폼 &amp; CRM',
  '받는 것까지가 절반입니다.<br>나머지 절반은 받아 적는 것입니다.',
  '전화를 받아 주는 서비스는 이미 있습니다. 그런데 받고 나서 남는 것이 메모 한 줄이면, '
  '다음 날 그 메모를 보고 다시 전화를 걸어야 합니다. 그러면 아무것도 줄지 않습니다.',
  '<a class="btn btn-teal" href="#inside">응대 한 건을 따라가 보기<span class="cir">&darr;</span></a>',
  '<a class="btn btn-ghostd" href="./pricing.html">요금 보기</a>'),
 '<main>',
 sec('t-md sec-dark bg-grid', 'inside', '응대 한 건이 만들어지는 과정',
     '전화가 울리고 나서<br>예약이 잡히기까지, 여섯 단계.',
     '아래 여섯 가지는 순서대로 일어납니다. 어느 하나가 빠지면 그 통화는 '
     '메모 한 줄로 끝납니다.',
     pipe(['전화 · 채팅 도착', '누구인지 확인', '요금표에서 답', '빈 시간 확인',
           '예약 잡기', '고객 카드 저장'])),
 sec('t-md sec-dark bg-spot', 'crm', 'CRM',
     '업종의 말로 적힙니다.<br>빈칸을 고쳐 쓰지 않습니다.',
     '치과의 예약 단계와 정비소의 입고 단계는 다릅니다. 부동산의 매물 문의와 학원의 상담 문의도 '
     '다릅니다. 그래서 항목과 단계를 업종별로 미리 만들어 두었습니다.',
     ul([('고객 카드', '이름, 연락처, 무엇을 물었는지, 언제 다시 연락하기로 했는지가 한 화면에 있습니다.'),
         ('예약', '캘린더에 바로 들어갑니다. 메모가 아니라 시간입니다.'),
         ('견적', '직접 넣으신 요금표에서 계산합니다. AI가 금액을 지어내지 않습니다.'),
         ('통화 기록', '녹취와 요약, 그리고 그렇게 답한 근거가 함께 남습니다.'),
         ('내보내기', '전부 내려받을 수 있습니다. 나가는 길을 막지 않는 것도 제품의 일부입니다.')])),
 sec('t-md sec-light bg-paper', 'who-next', '누구에게 넘기는가',
     '기계가 멈추는 자리를<br>미리 정해 둡니다.', '',
     ul([('요금표에 없는 질문', '&ldquo;확인 후 연락드리겠습니다&rdquo;로 멈추고, 담당자에게 넘깁니다.'),
         ('판단이 필요한 질문', '진단, 법률 판단, 사건 전망 같은 것은 사람만 합니다.'),
         ('화가 난 사람', '말투에서 불만이 감지되면 붙잡지 않고 바로 사람에게 돌립니다.'),
         ('안전이 걸린 상황', '가스, 누수, 응급 증상 같은 말이 나오면 예약을 잡지 않고 연결합니다.')]),
     dark=False),
 closer('우리 요금표를 넣으면<br>어떻게 답하는지 보여 드립니다.',
        '결제 정보는 받지 않습니다. 영업일 하루 안에 실제 대화를 만들어 보내 드립니다.'),
 FOOT, '</main>'])

page('platform.html', '플랫폼과 CRM &mdash; 받는 것으로 끝나지 않습니다 | Saleringo',
     '전화가 울리고 예약이 잡히기까지 여섯 단계, 그리고 통화 뒤에 남는 업종별 CRM. '
     'AI가 멈추고 사람에게 넘기는 자리까지 적었습니다.',
     platform, css=CSS, grade='voice',
     image=(PH % ('8475194', '8475194')) + '?auto=compress&amp;cs=tinysrgb&amp;fit=crop&amp;w=1200&amp;h=630',
     crumbs=[('홈', 'index.html'), ('플랫폼과 CRM', 'platform.html')])


# ══ 2 · AI 전화 ══════════════════════════════════════════════════════════
voice = '\n\n'.join([
 hero_photo('19061187', 'AI 전화',
  '쓰던 번호를 그대로 두고<br>못 받은 전화만 넘길 수 있습니다.',
  '번호를 바꾸지 않습니다. 명함과 간판, 네이버 플레이스에 적힌 그 번호 그대로 두고, '
  '벨이 몇 번 울린 뒤에도 아무도 받지 않을 때만 AI가 받습니다.',
  '<a class="btn btn-teal" href="#how">연결 방식 보기<span class="cir">&darr;</span></a>',
  '<a class="btn btn-ghostd" href="tel:+827052770820" data-tel>지금 걸어서 들어 보기</a>'),
 '<main>',
 sec('t-md sec-dark bg-grid', 'how', '연결 방식',
     '세 가지 중에 고르시면 됩니다.',
     '어떤 방식이든 번호는 그대로입니다. 통신사를 바꾸지 않고, 회선을 새로 놓지 않습니다.',
     trio([('못 받을 때만',
            '벨이 다섯 번 울려도 안 받으면 그때 넘어갑니다. 가장 많이 고르시는 방식입니다.'),
           ('영업시간 밖에만',
            '문을 닫은 시간과 점심시간에만 AI가 받습니다. 시간표는 직접 정하십니다.'),
           ('처음부터 AI가',
            'AI가 먼저 받고, 사람이 필요한 통화만 돌립니다. 문의량이 많은 곳에 맞습니다.')])),
 sec('t-md sec-dark bg-dusk', 'listen', '실제 통화',
     '사람처럼 들리되,<br>사람인 척하지는 않습니다.',
     '물어보시면 AI라고 답합니다. 그것을 숨기면 그때부터는 신뢰의 문제가 됩니다.',
     '    <div class="appwin reveal" style="margin-top:30px;">\n'
     '      <div class="bar"><i></i><i></i><i></i>'
     '<span class="tt">일반 문의 &mdash; <b>오후 12시 40분</b></span>'
     '<span class="illus">예시 &middot; 가상의 통화</span>'
     '<span class="closed">점심시간</span></div>\n'
     '      <div class="body nightline">'
     '<div class="nl us"><span class="t"><em>고객</em>12:41</span>'
     '<div class="bub user">혹시 지금 사람이랑 통화하는 건가요?</div></div>'
     '<div class="nl sr"><span class="t"><em>Saleringo</em>+2초</span>'
     '<div class="bub ai">아닙니다. 저는 이 매장의 AI 응대입니다. '
     '예약을 잡아 드리거나 가격을 안내해 드릴 수 있고, '
     '사람과 통화가 필요하시면 바로 연결해 드리겠습니다.</div></div>'
     '<div class="nl us"><span class="t"><em>고객</em>12:42</span>'
     '<div class="bub user">아 괜찮아요. 예약만 하면 돼요.</div></div>'
     '</div>\n    </div>\n'),
 sec('t-md sec-light bg-paper', 'rules', '통화에서 지키는 것',
     '녹음하고, 알리고,<br>지웁니다.', '',
     ul([('녹음한다고 먼저 말합니다.', '통화 시작에 안내가 나갑니다. 원치 않으시면 녹음을 끄고 요약만 남길 수 있습니다.'),
         ('녹취는 그 가게의 것입니다.', '언제든 내려받고, 삭제 요청하면 지웁니다.'),
         ('사람에게 돌리는 조건을 정해 둡니다.', '어떤 말이 나오면 붙잡지 말고 넘길지를 미리 적어 둡니다.'),
         ('통화료는 쓴 만큼 청구합니다.', '1분당 190원부터이고, 월 한도를 걸어 두실 수 있습니다.')]),
     dark=False),
 closer('우리 매장 전화를<br>AI가 받으면 어떻게 되는지.',
        '업종과 영업시간만 알려 주시면, 실제 통화를 만들어 들려 드립니다.'),
 FOOT, '</main>'])

page('voice.html', 'AI 전화 &mdash; 쓰던 번호 그대로, 못 받은 전화만 | Saleringo',
     '번호를 바꾸지 않고 못 받은 전화만 AI가 받습니다. 연결 방식 세 가지, 통화 녹음 처리, '
     '분당 190원부터의 통화료를 적었습니다.',
     voice, css=CSS, grade='voice',
     image=(PH % ('19061187', '19061187')) + '?auto=compress&amp;cs=tinysrgb&amp;fit=crop&amp;w=1200&amp;h=630',
     crumbs=[('홈', 'index.html'), ('AI 전화', 'voice.html')])


# ══ 3 · 홈페이지 채팅 ════════════════════════════════════════════════════
webchat = '\n\n'.join([
 hero_photo('8353764', '홈페이지 채팅',
  '가격을 못 찾은 사람은<br>창을 닫습니다.',
  '홈페이지에 들어와서 3분을 뒤지다가 가격을 못 찾으면, 전화를 거는 대신 뒤로 가기를 누릅니다. '
  '그 사람이 무엇을 찾고 있었는지는 영영 모릅니다.',
  '<a class="btn btn-teal" href="#what">무엇을 답하는지 보기<span class="cir">&darr;</span></a>',
  '<a class="btn btn-ghostd" href="./pricing.html">요금 보기</a>'),
 '<main>',
 sec('t-md sec-dark bg-grid', 'what', '무엇을 답하는가',
     '홈페이지에 이미 있는 것과,<br>어디에도 없는 것.',
     '채팅으로 들어오는 질문의 대부분은 두 가지입니다. 찾기 어려워서 묻는 것과, '
     '아예 적혀 있지 않아서 묻는 것. 앞쪽은 그 자리에서 답하고, 뒤쪽은 예약으로 넘깁니다.',
     ul([('가격', '요금표에 있는 항목은 금액을 그대로 말합니다. 없으면 확인 후 연락드린다고 답합니다.'),
         ('예약 가능 시간', '캘린더의 빈 시간을 보고 답하고, 그 자리에서 잡습니다.'),
         ('오시는 길과 주차', '적어 두신 안내를 그대로 읽습니다.'),
         ('&ldquo;이런 것도 하나요&rdquo;', '서비스 목록에 있으면 답하고, 없으면 넘깁니다. 만들어 내지 않습니다.')])),
 sec('t-md sec-dark bg-spot', 'install', '설치',
     '스크립트 한 줄입니다.',
     '홈페이지를 새로 만들 필요가 없습니다. 워드프레스, 카페24, 아임웹, 직접 만든 사이트 모두 '
     '</body> 앞에 한 줄을 넣으면 됩니다. 넣는 작업은 저희가 해 드립니다.',
     pipe(['한 줄 넣기', '요금표 등록', '말투 확인', '켜기'])),
 sec('t-md sec-light bg-paper', 'left', '창을 닫아도',
     '대화는 남습니다.', '',
     ul([('연락처를 남기면 고객 카드가 생깁니다.', '이름과 번호를 받은 시점부터 그 사람은 문의가 됩니다.'),
         ('안 남겨도 무엇을 물었는지는 남습니다.', '어떤 질문이 반복되는지 보이면 홈페이지를 고칠 수 있습니다.'),
         ('밤에 온 문의는 아침에 목록으로 옵니다.', '누가 무엇을 물었고 어디까지 답이 나갔는지 정리되어 있습니다.')]),
     dark=False),
 closer('우리 홈페이지에 붙이면<br>어떤 질문이 들어올지.',
        '주소만 알려 주시면 지금 홈페이지를 보고, 무엇이 안 적혀 있는지부터 알려 드립니다.'),
 FOOT, '</main>'])

page('webchat.html', '홈페이지 채팅 &mdash; 가격을 못 찾아 나가는 사람 잡기 | Saleringo',
     '홈페이지에 스크립트 한 줄을 넣으면 가격과 예약 가능 시간을 그 자리에서 답하고 예약까지 잡습니다. '
     '요금표에 없는 것은 지어내지 않습니다.',
     webchat, css=CSS, grade='chat',
     image=(PH % ('8353764', '8353764')) + '?auto=compress&amp;cs=tinysrgb&amp;fit=crop&amp;w=1200&amp;h=630',
     crumbs=[('홈', 'index.html'), ('홈페이지 채팅', 'webchat.html')])


# ══ 4 · 카카오톡 ═════════════════════════════════════════════════════════
kakao = '\n\n'.join([
 hero_photo('31080810', '카카오톡 &amp; 메신저',
  '채널에 쌓인 안 읽은 문의는<br>대부분 예약이었습니다.',
  '카카오톡 채널로 오는 문의는 전화보다 가볍게 옵니다. 그래서 더 많이 오고, 더 많이 밀립니다. '
  '사흘 뒤에 답장하면 그 손님은 이미 다른 곳에 다녀왔습니다.',
  '<a class="btn btn-teal" href="#why">왜 밀리는지<span class="cir">&darr;</span></a>',
  '<a class="btn btn-ghostd" href="./pricing.html">요금 보기</a>'),
 '<main>',
 sec('t-md sec-dark bg-grid', 'why', '왜 밀리는가',
     '전화는 울리지만<br>메시지는 조용합니다.',
     '전화는 안 받으면 눈에 보입니다. 부재중 목록에 남고, 소리가 납니다. '
     '채널 메시지는 그렇지 않습니다. 알림을 한 번 넘기면 그것으로 끝이고, '
     '다음에 열었을 때는 이미 열두 개가 쌓여 있습니다.',
     ul([('가볍게 오는 만큼 많이 옵니다.', '전화를 걸 만큼은 아닌 질문이 전부 여기로 옵니다.'),
         ('답이 늦으면 다르게 읽힙니다.', '전화를 못 받은 것은 바빠서지만, 메시지에 답이 없는 것은 무시로 읽힙니다.'),
         ('밤에 옵니다.', '퇴근하고 누워서 보내는 문의입니다. 그 시간에 답할 사람은 없습니다.')])),
 sec('t-md sec-dark bg-spot', 'what', '받는 방식',
     '사람이 답하던 그 말투로<br>같은 내용을 답합니다.',
     '홈페이지 채팅과 전화에서 쓰는 요금표와 규칙이 그대로 적용됩니다. '
     '채널마다 다른 답이 나가면 그것이 더 큰 문제이기 때문입니다.',
     trio([('카카오톡 채널', '채널로 온 문의를 받고, 예약을 잡고, 알림톡으로 확인을 보냅니다.'),
           ('네이버 톡톡', '플레이스에서 넘어온 문의를 같은 내용으로 받습니다.'),
           ('인스타그램 DM', '프로필을 보고 바로 묻는 문의를 받습니다.')])),
 sec('t-md sec-light bg-paper', 'rules', '지키는 것',
     '광고로 쓰지 않습니다.', '',
     ul([('먼저 보내지 않습니다.', '문의에 답할 뿐입니다. 수신 동의 없는 광고 발송에 쓰지 않습니다.'),
         ('알림톡은 예약 확인에만.', '「정보통신망법」이 정하는 정보성 메시지 범위 안에서만 보냅니다.'),
         ('사람인 척하지 않습니다.', '물어보시면 AI라고 답합니다.'),
         ('발송 건당 요금입니다.', '알림톡은 건당 15원부터이고, 청구서에 건수가 그대로 나옵니다.')]),
     dark=False),
 closer('채널에 밀려 있는 문의를<br>지금 세어 보십시오.',
        '몇 건인지 알려 주시면, 그중 몇 건이 예약이 되었을지 같이 계산해 드립니다.'),
 FOOT, '</main>'])

page('whatsapp.html', '카카오톡 &amp; 메신저 응대 &mdash; 밀린 문의를 그 밤에 | Saleringo',
     '카카오톡 채널, 네이버 톡톡, 인스타그램 DM으로 온 문의를 전화·홈페이지 채팅과 같은 내용으로 '
     '답하고 예약까지 잡습니다. 광고 발송에는 쓰지 않습니다.',
     kakao, css=CSS, grade='chat',
     image=(PH % ('31080810', '31080810')) + '?auto=compress&amp;cs=tinysrgb&amp;fit=crop&amp;w=1200&amp;h=630',
     crumbs=[('홈', 'index.html'), ('카카오톡과 메신저', 'whatsapp.html')])


# ══ 5 · 연동 ═════════════════════════════════════════════════════════════
integ = '\n\n'.join([
 '<header class="hero nophoto sec-dark bg-aurora">\n'
 '  <div class="scrim" aria-hidden="true"></div>\n  ' + NAV + '\n'
 '  <div class="wrap hero-inner">\n'
 '    <span class="eyebrow"><i></i>연동</span>\n'
 '    <h1 style="margin-top:24px;">된다고 먼저 적어 두지<br>않습니다.</h1>\n'
 '    <p class="sub">연동된다고 써 놓고 안 되는 것이 이 업계에서 가장 흔한 거짓말입니다. '
 '그래서 어느 업종에서나 같은 방식으로 붙는 것만 아래에 적고, '
 '지금 쓰고 계신 제품이 되는지는 확인해서 알려 드립니다.</p>\n'
 '  </div>\n</header>',
 '<main>',
 sec('t-md sec-dark bg-grid', 'standard', '표준으로 붙는 것',
     '이 여섯 가지는<br>업종을 가리지 않습니다.', '',
     ul([('전화 회선', '쓰던 대표번호를 그대로 두고 못 받은 전화만 넘기거나, 처음부터 받게 합니다.'),
         ('카카오톡 채널', '채널 문의를 받고 알림톡을 보냅니다.'),
         ('홈페이지 채팅', '스크립트 한 줄이면 됩니다. 홈페이지 종류를 가리지 않습니다.'),
         ('구글 · 네이버 캘린더', '예약을 캘린더에 직접 넣습니다. 메모가 아니라 일정입니다.'),
         ('문자', '예약 확인과 전날 알림을 보내고, 발송 기록을 남깁니다.'),
         ('CSV 내보내기와 웹훅', '고객과 상담 내역을 파일로 내보내거나, 쓰시는 시스템으로 바로 보냅니다.')])),
 sec('t-md sec-dark bg-spot', 'yours', '쓰고 계신 제품',
     '되는지 확인해서<br>답해 드립니다.',
     '병원 차트 프로그램, 학원 관리 프로그램, 부동산 매물 시스템은 제품마다 다릅니다. '
     '문서로 열려 있는 제품은 대부분 붙고, 닫혀 있으면 CSV와 웹훅으로 우회합니다. '
     '어느 쪽인지는 제품 이름을 알려 주시면 확인해서 말씀드립니다.',
     pipe(['제품 이름 알려 주기', '연결 방식 확인', '가능 여부 회신', '설정'])),
 sec('t-md sec-light bg-paper', 'no', '안 하는 것',
     '데이터를 가두지 않습니다.', '',
     ul([('연동 비용을 받지 않습니다.', '위 여섯 가지에 따로 청구하지 않습니다.'),
         ('내보내기를 막지 않습니다.', '언제든 전부 내려받을 수 있습니다. 해지할 때도 마찬가지입니다.'),
         ('안 되는 것을 된다고 하지 않습니다.', '확인 전에는 &ldquo;확인해 보겠습니다&rdquo;라고만 답합니다.')]),
     dark=False),
 closer('쓰고 계신 프로그램 이름만<br>알려 주십시오.',
        '되는지 안 되는지, 안 되면 어떻게 우회하는지 영업일 하루 안에 답해 드립니다.'),
 FOOT, '</main>'])

page('integrations.html', '연동 &mdash; 표준으로 붙는 여섯 가지, 나머지는 확인 후 | Saleringo',
     '전화 회선, 카카오톡 채널, 홈페이지 채팅, 캘린더, 문자, CSV·웹훅은 업종을 가리지 않고 붙습니다. '
     '쓰고 계신 차트·관리 프로그램은 확인해서 답해 드립니다.',
     integ, css=CSS, grade='trust',
     crumbs=[('홈', 'index.html'), ('연동', 'integrations.html')])

print('제품 페이지 5장')
