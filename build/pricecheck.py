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
