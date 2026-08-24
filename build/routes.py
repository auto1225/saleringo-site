# -*- coding: utf-8 -*-
"""vercel.json 을 파일 목록에서 다시 만든다.

무엇이 잘못돼 있었나.

  이 파일에는 손으로 적은 리디렉션이 207개 있었고, 그중 206개가 /en/ 으로
  보내고 있었다. /ko/ 로 보내는 것은 하나도 없었다. 영어 사이트만 있던
  시절에 만든 규칙이 그대로 남아 있었기 때문이다.

  결과는 두 가지였다.

    · /ko/pricing 처럼 .html 을 뺀 한국어 주소가 전부 404 였다.
      영어 쪽은 /en/pricing 이 멀쩡히 열리는데 한국어만 안 열렸다.

    · /pricing 이나 /about 처럼 언어가 안 붙은 주소가 무조건 영어로 갔다.
      그것도 301, 즉 "영구 이동"이라서 브라우저가 그 답을 캐시에 넣는다.
      한국어 사용자가 한 번 /pricing 을 누르면 그 뒤로는 규칙을 고쳐도
      브라우저가 캐시된 301 을 그대로 써서 계속 영어로 간다.

무엇을 바꿨나.

  1) 두 언어 모두 .html 없는 주소가 열린다. /ko/pricing, /en/pricing.
     이건 언어가 정해진 주소라 301(영구)로 둬도 안전하다.

  2) 언어가 안 붙은 주소는 읽는 사람의 브라우저 언어를 보고 보낸다.
     Accept-Language 가 ko 로 시작하면 한국어로, 아니면 영어로.
     그리고 이건 302(임시)다. 목적지가 읽는 사람에 따라 달라지는 주소를
     301 로 돌리는 것은 처음부터 틀린 일이었다.

  3) 한국어에 없는 페이지는 조건 규칙을 만들지 않는다.
     지금은 69장이 다 짝이 맞지만, 한쪽에만 있는 페이지가 생기면
     그 페이지는 조용히 영어로 간다. 없는 곳으로 보내지 않는다.

    python build/routes.py            vercel.json 을 다시 쓴다
    python build/routes.py --check    바뀔 내용을 보여주고 쓰지는 않는다
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

LANGS = ('en', 'ko')
# Accept-Language 가 ko 로 시작할 때만 한국어로 보낸다. ko-KR, ko;q=0.9 둘 다 잡는다.
KO_HEADER = [{'type': 'header', 'key': 'accept-language', 'value': '^ko(-[A-Za-z]+)?\\b.*'}]


def pages(lang):
    out = []
    for p in sorted(glob.glob('%s/*.html' % lang)) + sorted(glob.glob('%s/industries/*.html' % lang)):
        out.append(p.replace(os.sep, '/')[len(lang) + 1:-5])   # 'pricing', 'industries/dental'
    return out


def build():
    en, ko = pages('en'), pages('ko')
    have_ko = set(ko)
    redirects = [
        {'source': '/favicon.ico', 'destination': '/favicon.svg', 'permanent': False},
    ]

    # ── 1. 언어가 붙은 주소에서 .html 빼기 ────────────────────────────────
    # /en/pricing → /en/pricing.html, /ko/pricing → /ko/pricing.html
    # 목적지가 읽는 사람과 무관하므로 301 로 둔다.
    for lang in LANGS:
        for slug in pages(lang):
            redirects.append({'source': '/%s/%s' % (lang, slug),
                              'destination': '/%s/%s.html' % (lang, slug),
                              'permanent': True})
        redirects.append({'source': '/%s/index' % lang,
                          'destination': '/%s/index.html' % lang, 'permanent': True})

    # ── 2. 언어가 안 붙은 주소 ────────────────────────────────────────────
    # 예전부터 검색엔진에 올라가 있는 주소들이다. 죽이면 안 되고,
    # 그렇다고 한국어 사용자를 영어로 보내서도 안 된다. 그래서 헤더를 본다.
    for slug in en:
        for src in ('/%s' % slug, '/%s.html' % slug):
            if slug in have_ko:
                redirects.append({'source': src, 'has': KO_HEADER,
                                  'destination': '/ko/%s.html' % slug,
                                  'permanent': False})
            redirects.append({'source': src,
                              'destination': '/en/%s.html' % slug,
                              'permanent': False})
    # /industries 처럼 예전에 쓰던 짧은 주소 하나
    redirects.append({'source': '/industries', 'has': KO_HEADER,
                      'destination': '/ko/industries.html', 'permanent': False})
    redirects.append({'source': '/industries',
                      'destination': '/en/industries.html', 'permanent': False})

    # 같은 source 가 두 번 들어가면 앞의 것만 쓰이므로, 순서를 지키며 중복만 뺀다
    seen, clean = set(), []
    for r in redirects:
        key = (r['source'], json.dumps(r.get('has', '')))
        if key in seen:
            continue
        seen.add(key)
        clean.append(r)

    cfg = {
        '$schema': 'https://openapi.vercel.sh/vercel.json',
        'cleanUrls': False,
        'trailingSlash': False,
        'redirects': clean,
        'headers': [
            {'source': '/assets/(.*)',
             'headers': [{'key': 'Cache-Control',
                          'value': 'public, max-age=3600, must-revalidate'}]},
            # 언어를 보고 갈라지는 것은 언어가 안 붙은 주소뿐이다.
            # /en/... 과 /ko/... 은 이미 언어가 정해진 주소라서 Vary 를 붙이면
            # 캐시만 쪼개고 얻는 것이 없다. 그래서 루트 한 단계에만 붙인다.
            {'source': '/:slug.html',
             'headers': [{'key': 'Vary', 'value': 'Accept-Language'}]},
            {'source': '/industries/:slug.html',
             'headers': [{'key': 'Vary', 'value': 'Accept-Language'}]},
            {'source': '/.well-known/security.txt',
             'headers': [{'key': 'Content-Type', 'value': 'text/plain; charset=utf-8'},
                         {'key': 'Cache-Control', 'value': 'public, max-age=86400'}]},
        ],
    }
    return cfg, en, ko


cfg, en, ko = build()
text = json.dumps(cfg, ensure_ascii=False, indent=2) + '\n'
old = io.open('vercel.json', encoding='utf-8').read() if os.path.exists('vercel.json') else ''

n_ko = sum(1 for r in cfg['redirects'] if r['destination'].startswith('/ko/'))
n_en = sum(1 for r in cfg['redirects'] if r['destination'].startswith('/en/'))
n_301 = sum(1 for r in cfg['redirects'] if r.get('permanent'))
print('영어 %d장, 한국어 %d장' % (len(en), len(ko)))
print('규칙 %d개 — 한국어로 %d개, 영어로 %d개, 301 %d개, 302 %d개'
      % (len(cfg['redirects']), n_ko, n_en, n_301, len(cfg['redirects']) - n_301))

if '--check' in sys.argv:
    print('바뀜' if text != old else '바뀐 것 없음')
else:
    io.open('vercel.json', 'w', encoding='utf-8').write(text)
    print('vercel.json 다시 씀' if text != old else 'vercel.json 그대로')
