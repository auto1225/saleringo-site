# -*- coding: utf-8 -*-
"""이해를 돕는 그림 — 인라인 SVG. 영·한 문구를 같은 틀에서 만든다.

쓰는 곳: build/ko/p_*.py (한국어 생성기)와 build/illus_en.py (영어 HTML 삽입).
그림은 장식이 아니라 본문이 말하는 구조를 그대로 그린 것이다: 세 단계, 세 채널→한 수신함,
고객 카드, 사람에게 넘기는 문, 진행 단계, 문 닫은 시간, 아침 화면.
색은 assets/css/ledger.css 의 토큰과 같다."""
import html

INK = '#141A1F'; INK2 = '#3B454D'; MUTE = '#616B75'; LINE = '#E2DDD3'; PAPER = '#F6F4EE'
CARD = '#FFFFFF'; TEAL = '#0B7878'; TEAL_S = 'rgba(11,120,120,.10)'; AMBER = '#B7791F'
AMBER_S = 'rgba(183,121,31,.12)'; GREEN = '#2F855A'; GREEN_S = 'rgba(47,133,90,.12)'
FONT = 'font-family="inherit"'

L = {
 'ko': dict(
  flow_t='세 단계로 움직입니다', f1='우리 가게의 말', f1a='요금표', f1b='영업시간', f1c='하면 안 되는 말',
  f2='AI가 대신 받습니다', f2a='전화', f2b='홈페이지 채팅', f2c='카카오톡', f2n='같은 내용으로 답합니다',
  f3='남는 것', f3a='예약 — 캘린더에', f3b='고객 카드 — 업종 항목', f3c='견적 — 요금표 그대로', f3d='할 일 — 담당·기한',
  a1='넣습니다', a2='적힙니다',
  ch_t='세 채널, 한 수신함', c1='전화', c2='홈페이지 채팅', c3='카카오톡 · 메신저', inbox='한 수신함', inv='세금계산서 한 장',
  in1='김지은 · 전화 · 예약 확정', in2='박민수 · 채팅 · 견적 발송', in3='이서연 · 카카오톡 · 답변 대기',
  card_t='고객 카드', cname='김지은', cphone='010-4482-51··', cch1='전화', cch2='카카오톡',
  r1=('요청', '앞니 크라운 — 이번 주', '통화에서'), r2=('견적', '지르코니아 크라운 550,000원', '사장님 요금표'),
  r3=('예약', '목 10:30', '캘린더의 빈 시간'), r4=('담당 · 기한', '데스크 · 목 09:00까지', '규칙대로'),
  ho_t='답하지 않고 사람에게 넘기는 문', hq='손님의 말', hq1='“보험으로 크라운이 보장되나요?”',
  g1='요금표에 있는가', g2='판단이 필요한가', g3='안전이 걸렸는가', yes='답합니다', yes2='요금표 그대로, 근거와 함께',
  no='사람에게 넘깁니다', n1='대화 전체', n2='받아 적은 항목', n3='멈춘 이유',
  pipe_t='진행 단계', pn='건', ni_t='문 닫은 시간', ni_open='영업 중', ni_closed='닫힘', ni_c='24시간 중', ni_h='15시간',
  ni_note='전화는 이 시간에도 옵니다', ni_call='11:42 PM 전화',
  mo_t='오전 9:00 — 사장님 화면', m1=('새 예약 1건', '김지은 · 목 10:30 · 캘린더에 있음'), m2=('견적서 1건', '550,000원 · 문자로 발송 · 열람 확인'),
  m3=('데스크 할 일', '목 09:00까지 차트 준비'), m4=('답변 대기 1건', '보험 문의 · 대화 전체 첨부'),
 ),
 'en': dict(
  flow_t='Three steps, no more', f1='Your own words', f1a='Price list', f1b='Opening hours', f1c='What never to say',
  f2='The AI answers', f2a='Phone', f2b='Website chat', f2c='WhatsApp', f2n='Same answers on every channel',
  f3='What is left behind', f3a='Booking — in the calendar', f3b='Customer record — your fields', f3c='Quote — from your prices', f3d='Task — owner and deadline',
  a1='you add', a2='it writes',
  ch_t='Three channels, one inbox', c1='Phone', c2='Website chat', c3='WhatsApp · messengers', inbox='One inbox', inv='One invoice',
  in1='J. Kim · phone · booked', in2='M. Park · chat · quote sent', in3='S. Lee · WhatsApp · reply waiting',
  card_t='Customer record', cname='Jane Kim', cphone='555-01··', cch1='Phone', cch2='WhatsApp',
  r1=('Request', 'Front-tooth crown — this week', 'from the call'), r2=('Quote', 'Zirconia crown $550', 'your price list'),
  r3=('Booking', 'Thu 10:30', 'free slot in calendar'), r4=('Owner · deadline', 'Front desk · Thu 09:00', 'by your rule'),
  ho_t='The gate before a person', hq='The customer asks', hq1='“Does my insurance cover the crown?”',
  g1='On the price list?', g2='Needs a judgement?', g3='Safety involved?', yes='It answers', yes2='word for word, with the source',
  no='Handed to a person', n1='the whole conversation', n2='every captured field', n3='why it stopped',
  pipe_t='Pipeline', pn='', ni_t='Closed hours', ni_open='open', ni_closed='closed', ni_c='of 24 hours', ni_h='15 hours',
  ni_note='calls still arrive in these hours', ni_call='11:42 PM call',
  mo_t='9:00 AM — the owner’s screen', m1=('1 new booking', 'Jane Kim · Thu 10:30 · in the calendar'), m2=('1 estimate sent', '$550 · by text · opened'),
  m3=('Front-desk task', 'Chart ready by Thu 09:00'), m4=('1 reply waiting', 'insurance question · thread attached'),
 ),
}


def esc(s):
    return html.escape(s, quote=True)


def _svg(w, h, body, label):
    return ('<svg class="illus" viewBox="0 0 %d %d" role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg">'
            '<title>%s</title>%s</svg>' % (w, h, esc(label), esc(label), body))


def rect(x, y, w, h, r=10, fill=CARD, stroke=LINE, sw=1, extra=''):
    return '<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" stroke-width="%g" %s/>' % (x, y, w, h, r, fill, stroke, sw, extra)


def text(x, y, s, size=13, fill=INK, weight=600, anchor='start', extra=''):
    return '<text x="%g" y="%g" font-size="%g" fill="%s" font-weight="%d" text-anchor="%s" %s>%s</text>' % (x, y, size, fill, weight, anchor, extra, esc(s))


def chip(x, y, s, fill=TEAL_S, color=TEAL, size=11):
    w = 10 + len(s) * (size * 0.62 if all(ord(c) < 128 for c in s) else size * 1.0)
    return rect(x, y, w, 20, 10, fill, 'none') + text(x + w / 2, y + 14, s, size, color, 700, 'middle'), w


def arrow(x1, y1, x2, y2, color=TEAL):
    return ('<path d="M%g %g L%g %g" stroke="%s" stroke-width="1.6" fill="none"/>'
            '<path d="M%g %g l-7 -4 v8 z" fill="%s"/>' % (x1, y1, x2 - 6, y2, color, x2, y2, color))


def check(x, y, color=TEAL):
    return '<path d="M%g %g l3.5 3.5 l7 -7" stroke="%s" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' % (x, y, color)


def flow3(lang='ko'):
    t = L[lang]; o = []
    cw, ch, gap, y0 = 184, 230, 44, 62
    xs = [12, 12 + cw + gap, 12 + 2 * (cw + gap)]
    o.append(text(12, 30, t['flow_t'], 12, MUTE, 700, extra='letter-spacing=".08em"'))
    # card 1: the shop's own words
    x = xs[0]; o.append(rect(x, y0, cw, ch, 14))
    o.append(text(x + 18, y0 + 30, '1', 22, TEAL, 800)); o.append(text(x + 40, y0 + 30, t['f1'], 14, INK, 700))
    for i, s in enumerate((t['f1a'], t['f1b'], t['f1c'])):
        yy = y0 + 66 + i * 44
        o.append(rect(x + 18, yy, cw - 36, 32, 8, PAPER, 'none'))
        o.append('<rect x="%g" y="%g" width="4" height="16" rx="2" fill="%s"/>' % (x + 28, yy + 8, TEAL if i < 2 else AMBER))
        o.append(text(x + 42, yy + 21, s, 13, INK2, 600))
    # arrow 1
    ax = xs[0] + cw; o.append(arrow(ax + 6, y0 + ch / 2, ax + gap - 6, y0 + ch / 2)); o.append(text(ax + gap / 2, y0 + ch / 2 - 10, t['a1'], 11, MUTE, 600, 'middle'))
    # card 2: the AI answers on three channels
    x = xs[1]; o.append(rect(x, y0, cw, ch, 14))
    o.append(text(x + 18, y0 + 30, '2', 22, TEAL, 800)); o.append(text(x + 40, y0 + 30, t['f2'], 14, INK, 700))
    icons = [
        '<path d="M%g %g h3l1.5 3.5-2 1.2a9 9 0 0 0 5.3 5.3l1.2-2 3.5 1.5v3a1.5 1.5 0 0 1-1.6 1.5A13.5 13.5 0 0 1 %g %g a1.5 1.5 0 0 1 1.5-1.5z"/>',
        '<path d="M%g %g h14a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3h-8l-5 4v-4a3 3 0 0 1-3-3v-8a3 3 0 0 1 3-3z"/>',
        '<path d="M%g %g c-5 0-9 3.4-9 7.6 0 2.7 1.7 5 4.3 6.4l-1 3.6 4.2-2.6c.5.1 1 .1 1.5.1 5 0 9-3.4 9-7.6s-4-7.5-9-7.5z"/>',
    ]
    for i, s in enumerate((t['f2a'], t['f2b'], t['f2c'])):
        yy = y0 + 66 + i * 44
        o.append(rect(x + 18, yy, cw - 36, 32, 8, PAPER, 'none'))
        ic = icons[i]
        if i == 0: ic = ic % (x + 26, yy + 8, x + 26, yy + 9.5)
        else: ic = ic % (x + 26, yy + 8)
        o.append('<g fill="none" stroke="%s" stroke-width="1.6" stroke-linejoin="round">%s</g>' % (TEAL, ic))
        o.append(text(x + 50, yy + 21, s, 13, INK2, 600))
    o.append(text(x + cw / 2, y0 + ch - 14, t['f2n'], 11, MUTE, 600, 'middle'))
    ax = xs[1] + cw; o.append(arrow(ax + 6, y0 + ch / 2, ax + gap - 6, y0 + ch / 2)); o.append(text(ax + gap / 2, y0 + ch / 2 - 10, t['a2'], 11, MUTE, 600, 'middle'))
    # card 3: what is left behind
    x = xs[2]; o.append(rect(x, y0, cw, ch, 14, CARD, TEAL, 1.5))
    o.append(text(x + 18, y0 + 30, '3', 22, TEAL, 800)); o.append(text(x + 40, y0 + 30, t['f3'], 14, INK, 700))
    for i, s in enumerate((t['f3a'], t['f3b'], t['f3c'], t['f3d'])):
        yy = y0 + 58 + i * 38
        o.append(check(x + 20, yy + 10)); o.append(text(x + 40, yy + 15, s, 12.5, INK2, 600))
    return _svg(640, 310, ''.join(o), t['flow_t'])


def channels(lang='ko'):
    t = L[lang]; o = []
    o.append(text(12, 30, t['ch_t'], 12, MUTE, 700, extra='letter-spacing=".08em"'))
    ys = [86, 156, 226]
    for i, s in enumerate((t['c1'], t['c2'], t['c3'])):
        y = ys[i]; o.append(rect(12, y - 20, 176, 44, 10, PAPER, 'none'))
        o.append('<circle cx="%g" cy="%g" r="5" fill="%s"/>' % (32, y + 2, (TEAL, TEAL, GREEN)[i]))
        o.append(text(48, y + 7, s, 13.5, INK, 700))
        o.append('<path d="M%g %g C %g %g, %g %g, %g %g" stroke="%s" stroke-width="1.6" fill="none"/>' % (188, y + 2, 236, y + 2, 236, 156, 262, 156, LINE))
    o.append('<path d="M262 156 l-7 -4 v8 z" fill="%s"/>' % TEAL)
    # inbox
    o.append(rect(270, 80, 236, 152, 14, CARD, TEAL, 1.5))
    o.append(text(288, 106, t['inbox'], 14, INK, 700))
    for i, s in enumerate((t['in1'], t['in2'], t['in3'])):
        yy = 122 + i * 34
        o.append(rect(288, yy, 200, 26, 6, PAPER, 'none'))
        o.append('<circle cx="%g" cy="%g" r="3.5" fill="%s"/>' % (300, yy + 13, (TEAL, TEAL, GREEN)[i]))
        o.append(text(310, yy + 17, s, 11.5, INK2, 600))
    o.append(arrow(512, 156, 546, 156))
    o.append(rect(552, 118, 76, 76, 10, PAPER, LINE))
    o.append('<path d="M570 136 h40 v40 h-40z M576 148 h28 M576 158 h28 M576 168 h18" stroke="%s" stroke-width="1.5" fill="none"/>' % INK2)
    o.append(text(590, 214, t['inv'], 11, MUTE, 700, 'middle'))
    return _svg(640, 250, ''.join(o), t['ch_t'])


def card(lang='ko', rows=None, name=None, phone=None, chans=None):
    t = L[lang]; o = []
    rows = rows or (t['r1'], t['r2'], t['r3'], t['r4'])
    name = name or t['cname']; phone = phone or t['cphone']; chans = chans or (t['cch1'], t['cch2'])
    h = 96 + len(rows) * 50 + 8
    o.append(rect(12, 12, 616, h, 14))
    o.append(text(32, 40, t['card_t'], 12, MUTE, 700, extra='letter-spacing=".08em"'))
    o.append(text(32, 70, name, 17, INK, 800))
    o.append(text(32 + 10 + len(name) * 15 + 6, 70, phone, 12.5, MUTE, 600, extra='font-family="ui-monospace,monospace"'))
    x = 400
    for i, c in enumerate(chans):
        s, w = chip(x, 54, c, TEAL_S if i == 0 else GREEN_S, TEAL if i == 0 else GREEN); o.append(s); x += w + 8
    for i, (k, v, src) in enumerate(rows):
        yy = 96 + i * 50
        o.append('<path d="M32 %g H608" stroke="%s"/>' % (yy, LINE))
        kx = 32; vx = 150 if len(k) <= 8 else 270
        o.append(text(kx, yy + 22, k[:22], 11.5, MUTE, 700))
        if v is None:
            # 값을 지어내지 않는다 — 채워진 칸을 막대로 그린다
            o.append('<rect x="%g" y="%g" width="%g" height="9" rx="4.5" fill="%s"/>' % (vx, yy + 13, 240 - (i % 3) * 40, INK2))
        else:
            o.append(text(vx, yy + 22, v, 13.5, INK, 700))
        o.append(check(vx, yy + 36)); o.append(text(vx + 16, yy + 42, src, 11, TEAL, 700))
    return _svg(640, h + 24, ''.join(o), t['card_t'])


def handoff(lang='ko', question=None):
    t = L[lang]; o = []
    o.append(text(12, 30, t['ho_t'], 12, MUTE, 700, extra='letter-spacing=".08em"'))
    # the question
    o.append(rect(12, 52, 214, 92, 14, TEAL_S, 'none'))
    o.append(text(30, 78, t['hq'], 11.5, MUTE, 700))
    import re as _re
    q = _re.sub(r'<[^>]+>|&[a-z]+;', '', question or t['hq1']).strip()
    if question and not q.startswith(('“', '"')): q = '“' + q[:38] + ('…”' if len(q) > 38 else '”')
    o.append(text(30, 106, q[:22], 13.5, INK, 700))
    if len(q) > 22: o.append(text(30, 126, q[22:44], 13.5, INK, 700))
    o.append(arrow(232, 98, 262, 98))
    # gate: three checks
    o.append(rect(266, 44, 190, 110, 14, CARD, INK, 1.5))
    for i, s in enumerate((t['g1'], t['g2'], t['g3'])):
        yy = 72 + i * 30
        o.append('<circle cx="%g" cy="%g" r="6" fill="none" stroke="%s" stroke-width="1.6"/>' % (286, yy - 4, (TEAL, AMBER, AMBER)[i]))
        o.append(text(300, yy, s, 12.5, INK, 700))
    # yes path (down)
    o.append(arrow(361, 160, 361, 200))
    o.append(rect(266, 204, 190, 62, 12, TEAL_S, 'none'))
    o.append(text(286, 230, t['yes'], 13.5, TEAL, 800)); o.append(text(286, 250, t['yes2'], 11, INK2, 600))
    # no path (right)
    o.append(arrow(462, 98, 492, 98))
    o.append(rect(496, 44, 132, 222, 14, AMBER_S, AMBER, 1.2))
    o.append(text(512, 72, t['no'], 13, AMBER, 800))
    for i, s in enumerate((t['n1'], t['n2'], t['n3'])):
        yy = 104 + i * 40
        o.append(rect(512, yy - 14, 100, 28, 6, CARD, 'none'))
        o.append(text(522, yy + 5, s, 11.5, INK2, 700))
    return _svg(640, 280, ''.join(o), t['ho_t'])


def pipeline(lang='ko', stages=None, counts=None):
    t = L[lang]; o = []
    stages = stages or (['문의 접수', '예약 확정', '방문', '진행'] if lang == 'ko' else ['Inquiry', 'Booked', 'Visited', 'In progress'])
    n = len(stages); counts = counts or [4, 3, 2, 1, 1, 1][:n]
    o.append(text(12, 30, t['pipe_t'], 12, MUTE, 700, extra='letter-spacing=".08em"'))
    gap = 12; cw = (616 - gap * (n - 1)) / n; y0 = 48
    for i, s in enumerate(stages):
        x = 12 + i * (cw + gap)
        o.append(rect(x, y0, cw, 212, 12, PAPER, 'none'))
        o.append('<rect x="%g" y="%g" width="%g" height="3" rx="1.5" fill="%s"/>' % (x + 12, y0 + 12, cw - 24, TEAL if i < 2 else LINE))
        o.append(text(x + 12, y0 + 38, s[:9], 12, INK, 700))
        o.append(text(x + cw - 12, y0 + 38, '%d%s' % (counts[i], t['pn']), 12, MUTE, 700, 'end'))
        for j in range(min(counts[i], 3)):
            yy = y0 + 54 + j * 46
            o.append(rect(x + 12, yy, cw - 24, 36, 8, CARD, LINE))
            o.append('<rect x="%g" y="%g" width="%g" height="5" rx="2.5" fill="%s"/>' % (x + 22, yy + 11, (cw - 44) * (0.8 - j * 0.15), INK2 if j == 0 and i < 2 else LINE))
            o.append('<rect x="%g" y="%g" width="%g" height="5" rx="2.5" fill="%s"/>' % (x + 22, yy + 22, (cw - 44) * 0.45, LINE))
        if i < n - 1: o.append('<path d="M%g %g l6 -4 v8 z" fill="%s"/>' % (x + cw + 2, y0 + 106, LINE))
    return _svg(640, 275, ''.join(o), t['pipe_t'])


def night(lang='ko', open_from=9, open_to=18, call='11:42 PM'):
    import math
    t = L[lang]; o = []
    cx, cy, r = 150, 150, 104
    o.append(text(12, 30, t['ni_t'], 12, MUTE, 700, extra='letter-spacing=".08em"'))
    o.append('<circle cx="%g" cy="%g" r="%g" fill="none" stroke="%s" stroke-width="22"/>' % (cx, cy, r, INK))
    def pt(h, rr=r):
        a = (h / 24.0) * 2 * math.pi - math.pi / 2
        return cx + rr * math.cos(a), cy + rr * math.sin(a)
    x1, y1 = pt(open_from); x2, y2 = pt(open_to)
    large = 1 if (open_to - open_from) > 12 else 0
    o.append('<path d="M%g %g A%g %g 0 %d 1 %g %g" fill="none" stroke="%s" stroke-width="22" stroke-linecap="butt"/>' % (x1, y1, r, r, large, x2, y2, TEAL))
    for h in (0, 6, 12, 18):
        x, y = pt(h, r + 22); o.append(text(x, y + 4, {0: '0', 6: '6', 12: '12', 18: '18'}[h], 10.5, MUTE, 700, 'middle'))
    closed = 24 - (open_to - open_from)
    o.append(text(cx, cy - 6, t['ni_h'] if closed == 15 else ('%d시간' % closed if lang == 'ko' else '%d hours' % closed), 24, INK, 800, 'middle'))
    o.append(text(cx, cy + 16, t['ni_c'], 11.5, MUTE, 700, 'middle'))
    o.append(text(cx, cy + 34, t['ni_closed'], 11.5, INK2, 700, 'middle'))
    # the call marker at 23:42
    x, y = pt(23.7); o.append('<circle cx="%g" cy="%g" r="7" fill="%s" stroke="%s" stroke-width="2"/>' % (x, y, AMBER, CARD))
    # legend
    o.append('<rect x="300" y="82" width="14" height="14" rx="4" fill="%s"/>' % TEAL); o.append(text(322, 94, t['ni_open'] + ' %d–%d' % (open_from, open_to), 13, INK, 700))
    o.append('<rect x="300" y="116" width="14" height="14" rx="4" fill="%s"/>' % INK); o.append(text(322, 128, t['ni_closed'], 13, INK, 700))
    o.append('<circle cx="307" cy="157" r="6" fill="%s"/>' % AMBER); o.append(text(322, 162, call + ' — ' + t['ni_call'].split(' ', 2)[-1] if lang == 'en' else t['ni_call'], 13, INK, 700))
    o.append(text(300, 204, t['ni_note'], 12, MUTE, 600))
    return _svg(640, 300, ''.join(o), t['ni_t'])


def morning(lang='ko', items=None):
    t = L[lang]; o = []
    items = items or (t['m1'], t['m2'], t['m3'], t['m4'])
    o.append(rect(150, 10, 340, 260, 22, INK, 'none'))
    o.append(rect(160, 20, 320, 240, 16, PAPER, 'none'))
    o.append(text(178, 46, t['mo_t'], 12, MUTE, 700))
    marks = ['✓', '#', '@', '!']
    for i, (a, b) in enumerate(items):
        yy = 60 + i * 48
        o.append(rect(178, yy, 284, 40, 10, CARD, LINE))
        o.append(text(192, yy + 25, marks[i], 14, TEAL if i < 3 else AMBER, 800))
        o.append(text(212, yy + 18, a, 12.5, INK, 700)); o.append(text(212, yy + 33, b, 10.5, MUTE, 600))
    return _svg(640, 280, ''.join(o), t['mo_t'])


def figure(svg, caption='', cls=''):
    return '<figure class="illfig %s">%s%s</figure>' % (cls, svg, ('<figcaption class="illcap">%s</figcaption>' % caption) if caption else '')


if __name__ == '__main__':
    import io, sys
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    parts = []
    for lang in ('ko', 'en'):
        for name, fn in (('flow3', flow3), ('channels', channels), ('card', card), ('handoff', handoff), ('pipeline', pipeline), ('night', night), ('morning', morning)):
            parts.append('<h3>%s · %s</h3><div style="max-width:640px;border:1px dashed #ccc">%s</div>' % (lang, name, fn(lang)))
    io.open(sys.argv[1] if len(sys.argv) > 1 else 'illus_preview.html', 'w', encoding='utf-8').write(
        '<!doctype html><meta charset="utf-8"><body style="font-family:IBM Plex Sans KR,IBM Plex Sans,sans-serif;padding:20px;background:#F6F4EE">' + ''.join(parts))
    print('ok', len(parts))
