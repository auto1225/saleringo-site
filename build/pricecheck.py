# -*- coding: utf-8 -*-
"""요금표와 페이지가 말하는 숫자가 어긋나는 곳을 찾는다.

해외 구매자 검수에서 나온 지적의 절반이 같은 종류였다. 요금 페이지가
광고한 숫자와 주문서가 계산하는 숫자가 달랐다. Scale 대화량이 6,000 대
2,000, 초과 요금이 건당 $0.08 대 $0.07, 창립 할인은 한쪽에만 있었다.

사람이 눈으로 맞추는 것으로는 계속 어긋난다. 요금표가 유일한 출처이고,
페이지가 그와 다른 숫자를 적고 있으면 여기서 걸린다.

    python build/pricecheck.py
"""
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

P = json.load(io.open('assets/data/pricing.json', encoding='utf-8'))
problems = []


def text_of(path):
    s = io.open(path, encoding='utf-8').read()
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    for a, b in (('&nbsp;', ' '), ('&mdash;', '—'), ('&amp;', '&'), ('&middot;', '·')):
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s)


def fmt(n, cur):
    c = P['currencies'][cur]
    if abs(n - round(n)) < 1e-9:
        t = '{:,.0f}'.format(n)
    else:
        t = ('{:,.%df}' % c['decimals']).format(n)
    return (c['symbol'] + t) if c['position'] == 'before' else (t + c['symbol'])


PAGES = {'ko': sorted(glob.glob('ko/*.html')), 'en': sorted(glob.glob('en/*.html'))}
CUR = {'ko': 'KRW', 'en': 'USD'}

# ── 1. 요금 페이지와 주문서에 그 요금제의 값이 실제로 적혀 있어야 한다 ──
#      "이름 근처의 숫자"를 보는 방식은 바로 다음 카드의 금액을 집습니다.
#      있어야 할 문자열이 있는지만 봅니다. 그쪽은 오탐이 없습니다.
for lang, files in PAGES.items():
    cur = CUR[lang]
    for fp in ['%s/pricing.html' % lang, '%s/checkout.html' % lang]:
        if not os.path.exists(fp):
            continue
        t = text_of(fp)
        for pl in P['plans']:
            want = fmt(pl['price'][cur], cur)
            if want.replace(' ', '') not in t.replace(' ', ''):
                problems.append(('요금제 금액', fp,
                                 '%s 의 %s 가 이 페이지에 없습니다' % (pl['name'][lang], want)))

# ── 2. 요금제 가격을 소수점까지 늘여 쓰면 금액으로 안 읽힌다 ────────────
#      다만 송장 견본 안은 예외입니다. 인보이스에 $599.00 은 오히려 맞는
#      표기이고, 그 그림은 "청구서가 이렇게 생겼다"를 보여 주는 것입니다.
def text_no_svg(path):
    raw = io.open(path, encoding='utf-8').read()
    raw = re.sub(r'<svg.*?</svg>', ' ', raw, flags=re.S)
    raw = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', raw, flags=re.S)
    raw = re.sub(r'<[^>]+>', ' ', raw)
    for a, b in (('&nbsp;', ' '), ('&mdash;', '—'), ('&amp;', '&'), ('&middot;', '·')):
        raw = raw.replace(a, b)
    return re.sub(r'\s+', ' ', raw)


for lang, files in PAGES.items():
    if CUR[lang] != 'USD':
        continue
    for fp in files:
        t = text_no_svg(fp)
        for pl in P['plans']:
            bad = '$%s.00' % '{:,.0f}'.format(pl['price']['USD'])
            if bad in t:
                problems.append(('금액 표기', fp,
                                 '%s 로 적혀 있습니다 — $%s 로 써야 합니다'
                                 % (bad, '{:,.0f}'.format(pl['price']['USD']))))

# ── 3. 초과 요금 ─────────────────────────────────────────────────────────
for lang, files in PAGES.items():
    cur = CUR[lang]
    per = P['overage']['perConversation'][cur]
    for fp in files:
        t = text_of(fp)
        for m in re.finditer(r'([\d,]+)\s*건당\s*([\d,]+)\s*원', t):
            block, price = int(m.group(1).replace(',', '')), int(m.group(2).replace(',', ''))
            if abs(price / block - per) > 1e-6:
                problems.append(('초과 요금', fp,
                                 '%s건당 %s원 (=건당 %.2f) — 요금표는 건당 %s'
                                 % (m.group(1), m.group(2), price / block, per)))
        if cur == 'USD':
            for m in re.finditer(r'\$(\d+\.\d+)\s*per conversation', t):
                if abs(float(m.group(1)) - per) > 1e-6:
                    problems.append(('초과 요금', fp,
                                     '$%s each — 요금표는 $%s' % (m.group(1), per)))

# ── 4. 통화 요금 ─────────────────────────────────────────────────────────
voice = next((u for u in P['usage'] if u['id'] == 'voiceMinutes'), None)
if voice:
    for lang, files in PAGES.items():
        cur = CUR[lang]
        want = voice['unitPrice'][cur]
        for fp in files:
            t = text_of(fp)
            pats = [r'분당\s*([\d,]+)\s*원', r'1분당\s*([\d,]+)\s*원'] if cur == 'KRW' \
                else [r'\$(\d+\.\d+)\s*(?:/|a |per )\s*(?:min|talk minute)']
            for pat in pats:
                for m in re.finditer(pat, t):
                    got = float(m.group(1).replace(',', ''))
                    if abs(got - want) > 1e-6:
                        problems.append(('통화 요금', fp, '%s — 요금표는 %s' % (m.group(0), want)))

# ── 5. 할인이 켜져 있으면 두 언어의 요금 페이지가 그것을 말해야 한다 ────
d = P.get('discount')
if d and d.get('active'):
    for lang in ('ko', 'en'):
        fp = '%s/pricing.html' % lang
        if not os.path.exists(fp):
            continue
        t = text_of(fp)
        pct = str(d['percent'])
        if pct + '%' not in t:
            problems.append(('할인 고지', fp,
                             '요금표에 %d%% %d개월 할인이 켜져 있는데 이 페이지에 없습니다. '
                             '주문서는 할인가로 계산하므로 정가만 보이면 어긋납니다.'
                             % (d['percent'], d['months'])))

# ── 6. 주문서로 가는 길 ──────────────────────────────────────────────────
for lang in ('ko', 'en'):
    fp = '%s/pricing.html' % lang
    if os.path.exists(fp):
        s = io.open(fp, encoding='utf-8').read()
        body = s[s.find('<!--/#nav-->'):] if '<!--/#nav-->' in s else s
        n = len(re.findall(r'checkout\.html\?plan=', body))
        if n < len(P['plans']):
            problems.append(('구매 경로', fp,
                             '본문에서 주문서로 가는 링크 %d개 — 요금제는 %d개'
                             % (n, len(P['plans']))))

# ── 7. 페이지가 요금표에 없는 통화를 약속하면 안 된다 ────────────────────
#      "USD·EUR·GBP·AUD·SGD·KRW·JPY 중 고르실 수 있습니다" 가 세 페이지에
#      적혀 있었습니다. 그중 둘은 [필수] 동의를 받는 약관이었고, 실제로
#      존재하는 통화는 KRW 와 USD 둘뿐이며 주문서에는 고를 칸도 없었습니다.
#      약속을 늘리는 것은 쉽고, 그것이 거짓이 되었는지는 아무도 안 봅니다.
HAVE = set(P['currencies'])
MAYBE = {'EUR': '유로', 'GBP': '파운드', 'JPY': '엔', 'AUD': '호주달러',
         'SGD': '싱가포르달러', 'CAD': '캐나다달러', 'CHF': '스위스프랑',
         'CNY': '위안', 'INR': '루피', 'BRL': '헤알', 'AED': '디르함'}
for lang, files in PAGES.items():
    for fp in files:
        t = text_of(fp)
        for code, name in MAYBE.items():
            if code in HAVE:
                continue
            # 상인이 자기 손님에게 유로로 견적을 내는 것은 이 제품이 하는
            # 일이고, 그 문장은 옳습니다. 문제는 "우리가 당신에게 그 통화로
            # 청구한다" 는 약속입니다. 청구를 말하는 문장 안에서만 봅니다.
            for m in re.finditer(r'\b%s\b' % code, t):
                near = t[max(0, m.start() - 170):m.end() + 170]
                if not re.search(r'billed in|bill you|pay in|invoice you|charged in'
                                 r'|청구|결제하실|인보이스', near, re.I):
                    continue
                problems.append(('없는 통화', fp,
                                 '%s(%s) 로 청구한다고 적혀 있으나 요금표에 없습니다 '
                                 '(있는 것: %s)' % (code, name, ', '.join(sorted(HAVE)))))
                break

# ── 8. 한국 밖에 세금을 걷는다고 적으면 안 된다 ──────────────────────────
#      요금표의 tax 는 KR 10% 와 default 0% 둘뿐입니다. "세금은 청구 국가
#      기준으로 계산됩니다" 는 자기 나라 세금이 붙는다는 뜻으로 읽히는데,
#      한국 밖 19개국은 전부 0 입니다.
collected = [k for k, v in P['tax'].items()
             if k != 'default' and v.get('collected')]
if collected == ['KR']:
    LIES = [r'[Tt]ax is (?:added|calculated)[^.]{0,60}based on[^.]{0,40}billing country',
            r'[Tt]axes are added[^.]{0,60}based on[^.]{0,30}country',
            r'세금은[^.]{0,30}국가[^.]{0,20}기준으로[^.]{0,20}계산']
    for lang, files in PAGES.items():
        for fp in files:
            t = text_of(fp)
            for pat in LIES:
                m = re.search(pat, t)
                if m:
                    problems.append(('세금 안내', fp,
                                     '"%s" — 실제로 세금을 걷는 나라는 한국뿐입니다'
                                     % m.group(0)[:70]))

# ── 9. 통화 가용 국가는 요금표와 요금 페이지가 같아야 한다 ──────────────
#      요금 페이지의 표는 여섯 나라를 못박아 두었는데, 요금표에는 세 나라에만
#      "안 됨" 이 붙어 있었습니다. 그래서 독일·프랑스·일본 … 열 곳의 구매자가
#      AI 전화가 든 Scale 을 골라도 아무 경고가 뜨지 않았습니다.
#      전화가 핵심인 요금제를 전화 없이 파는 셈입니다.
VOICE_OK = {'live', 'soon', 'no'}
missing_voice = [c['code'] for c in P['countries'] if c.get('voice') not in VOICE_OK]
if missing_voice:
    problems.append(('통화 가용성', 'assets/data/pricing.json',
                     '%s 에 voice 가 없거나 값이 이상합니다 (live/soon/no 중 하나여야 합니다)'
                     % ', '.join(missing_voice)))
else:
    live = sorted(c['name']['en'] for c in P['countries'] if c['voice'] == 'live')
    fp = 'en/pricing.html'
    if os.path.exists(fp):
        t = text_of(fp)
        for nm in live:
            if nm not in t:
                problems.append(('통화 가용성', fp,
                                 '요금표는 %s 에서 AI 전화가 된다고 하는데 이 페이지에 없습니다' % nm))
        # 반대 방향: 페이지가 되는 것처럼 적어 둔 나라가 요금표에서는 안 되는 경우
        for c in P['countries']:
            if c['voice'] == 'live':
                continue
            nm = c['name']['en']
            if re.search(r'%s\s*[✓✔]' % re.escape(nm), t):
                problems.append(('통화 가용성', fp,
                                 '%s 이 되는 것처럼 표에 있는데 요금표는 %s 입니다'
                                 % (nm, c['voice'])))

# ── 10. 요금표를 판 번호 없이 부르면 안 된다 ────────────────────────────
#      사이트의 모든 자산에는 ?v= 가 붙는데, 정작 돈의 유일한 출처인
#      요금표만 그냥 부르고 있었습니다. 캐시가 한 시간이라, 새 코드가 옛
#      요금표를 읽는 시간이 배포마다 한 시간씩 생겼습니다. 실제로 그 사이
#      한국 구매자에게 "이 나라는 AI 전화가 안 됩니다"가 떴습니다.
#      값이 아니라 금액이 어긋났다면 알아채지도 못했을 것입니다.
for fp in sorted(glob.glob('assets/js/*.js')):
    src = io.open(fp, encoding='utf-8').read()
    for m in re.finditer(r"""fetch\(\s*['"]([^'"]*pricing\.json)['"]""", src):
        problems.append(('캐시', fp,
                         '%s 를 판 번호 없이 부릅니다. 배포 뒤 한 시간 동안 '
                         '새 코드가 옛 요금표를 읽습니다.' % m.group(1)))

# ── 결과 ─────────────────────────────────────────────────────────────────
if not problems:
    print('요금표와 페이지가 말하는 숫자가 모두 일치합니다.')
else:
    kinds = {}
    for k, fp, msg in problems:
        kinds.setdefault(k, []).append((fp, msg))
    for k in sorted(kinds):
        print('\n%s (%d)' % (k, len(kinds[k])))
        for fp, msg in kinds[k][:8]:
            print('   %-22s %s' % (fp.replace(os.sep, '/'), msg))
        if len(kinds[k]) > 8:
            print('   … 외 %d건' % (len(kinds[k]) - 8))
    print('\n합계 %d건' % len(problems))
    sys.exit(1)
