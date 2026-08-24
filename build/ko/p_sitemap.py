# -*- coding: utf-8 -*-
"""사이트맵 - every Korean page in one place.

The Korean site is smaller than the English one, and a site map is the honest
way to say so: a reader who came looking for a page that only exists in
English can see the whole set at a glance and switch languages once, rather
than clicking around finding pruned links.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.dirname(os.path.dirname(HERE)))
from shell import page, NAV, FOOT
from trades import TRADES
from trades2 import TRADES2

TRADES = TRADES + TRADES2

CSS = """
  .hero{display:block;padding:150px 0 56px;}
  /* space on both sides of the rule, so two groups never share an edge */
  .mapgrp{padding-bottom:32px;margin-bottom:32px;border-bottom:1px solid #E3E7EE;}
  .mapgrp:last-child{padding-bottom:0;margin-bottom:0;border-bottom:0;}
  .mapgrp h2{font-size:var(--fs-lead);color:var(--l-ink);}
  .mapgrp p{margin-top:10px;font-size:var(--fs-sm);line-height:1.8;color:var(--l-tx2);}
  .maplinks{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px;}
  .maplinks a{padding:11px 18px;border:1px solid #D5DBE4;border-radius:8px;
    text-decoration:none;color:var(--l-ink);font-size:var(--fs-sm);font-weight:500;
    transition:all .3s var(--ease);}
  .maplinks a:hover{border-color:var(--teal);background:rgba(23,189,189,.08);}
"""

GROUPS = [
    ('먼저 읽을 것',
     '이 셋이면 무엇인지, 얼마인지, 어떻게 시작하는지가 다 나옵니다.',
     [('홈 &mdash; 무엇을 하는가', './index.html'),
      ('요금 &mdash; 얼마인가', './pricing.html'),
      ('시작하기 &mdash; 어떻게 시작하는가', './get-started.html')]),
    ('제품',
     '전화, 홈페이지 채팅, 카카오톡. 그리고 그 뒤에 붙는 CRM과 연동.',
     [('플랫폼과 CRM', './platform.html'),
      ('AI 전화', './voice.html'),
      ('홈페이지 채팅', './webchat.html'),
      ('카카오톡과 메신저', './whatsapp.html'),
      ('연동', './integrations.html')]),
    ('직접 판단하기',
     '설명 대신 통화를 읽어 보시는 편이 빠릅니다.',
     [('대화 한 건 보기', './demo.html'),
      ('업종별 사례', './examples.html'),
      ('고르기 전에 &mdash; ARS · 전화대행 · AI 응대', './ai-answering-service.html'),
      ('답변 검증 방식', './verified-ai.html')]),
    ('업종별 페이지',
     '업종마다 걸려 오는 전화가 다르므로, 그 통화를 업종별로 그대로 적어 두었습니다. '
     '각 업종에는 팩 상세 페이지가 따로 있습니다.',
     [('업종 전체', './industries.html')] +
     [(t['name'], './industries/%s.html' % t['slug']) for t in TRADES]),
    ('회사와 법적 고지',
     '대한민국 법을 기준으로 작성했습니다. 아직 하지 않은 것도 함께 적어 두었습니다.',
     [('회사 소개', './about.html'),
      ('보안', './security.html'),
      ('개인정보처리방침', './privacy.html'),
      ('이용약관', './terms.html'),
      ('해외 대상 사업', './cross-border.html')]),
]

body = ['<header class="hero nophoto sec-dark bg-aurora">',
        '  <div class="scrim" aria-hidden="true"></div>',
        '  ' + NAV,
        '  <div class="wrap hero-inner">',
        '    <span class="eyebrow"><i></i>사이트맵</span>',
        '    <h1 style="margin-top:24px;">이 사이트의 모든 페이지.</h1>',
        '    <p class="sub">영어 사이트에 있는 예순아홉 장이 한국어로도 모두 있습니다. '
        '오른쪽 위 English 버튼을 누르면 지금 보고 계신 페이지의 영어판으로 바로 넘어갑니다.</p>',
        '  </div>', '</header>', '', '<main>', '',
        '<section class="t-lg sec-light bg-paper"><div class="wrap">']
for h, d, links in GROUPS:
    body.append('<div class="mapgrp reveal"><h2>%s</h2><p>%s</p><div class="maplinks">%s</div></div>'
                % (h, d, ''.join('<a href="%s">%s</a>' % (u, n) for n, u in links)))
body += ['</div></section>', '', FOOT, '</main>']

page('sitemap.html', '사이트맵 &mdash; Saleringo 한국어',
     'Saleringo 한국어 사이트의 모든 페이지. 요금, 업종별 페이지, 개인정보처리방침과 이용약관, '
     '그리고 아직 영어로만 제공되는 페이지 목록.',
     '\n'.join(body), css=CSS, grade='trust',
     crumbs=[('홈', 'index.html'), ('사이트맵', 'sitemap.html')])
print('wrote ko/sitemap.html')
