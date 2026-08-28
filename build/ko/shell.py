# -*- coding: utf-8 -*-
"""The shell every Korean page is poured into.

The English pages were written one at a time and grew their own heads; the
Korean ones are written together, so the head is a function instead of a
paragraph repeated eighteen times. Everything that varies is an argument, and
the two things that must not vary - the asset version and the chrome markers -
come from here so a Korean page cannot drift out of the build.

The file name is deliberately the English one: ko/pricing.html sits opposite
en/pricing.html, which is what lets the language switch and the hreflang pair
find each other without a translation table.
"""
import io
import os

SITE = 'https://claude.saleringo.com'
VER = '60.0'
FONTS = ('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700'
         '&family=Plus+Jakarta+Sans:wght@400;500;600;700;800'
         '&family=Noto+Sans+KR:wght@400;500;700;800&display=swap')
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'"
        "%3E%3Ccircle cx='50' cy='50' r='46' fill='%230FA3A3'/%3E%3Ctext x='50' y='66' "
        "font-size='52' font-family='Arial' font-weight='bold' fill='white' "
        "text-anchor='middle'%3ES%3C/text%3E%3C/svg%3E")


def og_image_of(slug):
    """같은 이름의 영문 쪽에서 og:image 를 가져온다.

    한국어 38쪽에 og:image 가 없었습니다. 카카오톡 공유 미리보기가
    이 태그를 읽으므로 한국 사업에는 빈칸이 실제 손실입니다. 영문
    쪽은 전부 갖고 있고 사진도 같은 사진이 맞으므로, 따로 안 주면
    영문 것을 씁니다.
    """
    import re
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), 'en', slug)
    try:
        m = re.search(r'property="og:image" content="([^"]*)"',
                      io.open(p, encoding='utf-8').read())
        return m.group(1) if m else ''
    except OSError:
        return ''


def page(slug, title, desc, body, css='', grade='', scripts=('site', 'balance', 'panels', 'wrap', 'rail', 'guide'),
         image='', crumbs=None, lang='ko'):
    if not image:
        image = og_image_of(slug)
    deep = '/' in slug
    root = '../' if deep else './'
    a = '../../assets' if deep else '../assets'
    url = '%s/%s/%s' % (SITE, lang, slug)
    ld = [('{"@context":"https://schema.org","@type":"WebPage","name":"%s",'
           '"description":"%s","url":"%s","isPartOf":{"@type":"WebSite","name":"Saleringo",'
           '"url":"https://saleringo.com/"},"inLanguage":"%s"}')
          % (title, desc, url, 'ko-KR' if lang == 'ko' else 'en')]
    if crumbs:
        items = ','.join('{"@type":"ListItem","position":%d,"name":"%s","item":"%s/%s/%s"}'
                         % (i + 1, n, SITE, lang, h) for i, (n, h) in enumerate(crumbs))
        ld.append('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[%s]}' % items)

    head = ['<!DOCTYPE html>', '<html lang="%s">' % lang, '<head>',
            '<meta charset="UTF-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            '<title>%s</title>' % title,
            '<meta name="description" content="%s">' % desc,
            '<link rel="canonical" href="%s">' % url,
            '<meta property="og:type" content="website">',
            '<meta property="og:site_name" content="Saleringo">',
            '<meta property="og:locale" content="%s">' % ('ko_KR' if lang == 'ko' else 'en_US'),
            '<meta property="og:locale:alternate" content="%s">' % ('en_US' if lang == 'ko' else 'ko_KR'),
            '<meta property="og:url" content="%s">' % url,
            '<meta property="og:title" content="%s">' % title,
            '<meta property="og:description" content="%s">' % desc]
    if image:
        head += ['<meta property="og:image" content="%s">' % image,
                 '<meta property="og:image:width" content="1200">',
                 '<meta property="og:image:height" content="630">',
                 '<meta name="twitter:card" content="summary_large_image">',
                 '<meta name="twitter:image" content="%s">' % image]
    head += ['<meta name="twitter:title" content="%s">' % title,
             '<meta name="twitter:description" content="%s">' % desc,
             '<link rel="icon" href="%s">' % ICON,
             '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
             '<link rel="preconnect" href="https://images.pexels.com">',
             '<link rel="preconnect" href="https://fonts.googleapis.com">',
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
             '<link href="%s" rel="stylesheet">' % FONTS]
    for j in ld:
        head += ['<script type="application/ld+json">', j, '</script>']
    head += ['<link rel="stylesheet" href="%s/css/site.css?v=%s">' % (a, VER),
             '<link rel="stylesheet" href="%s/css/scenes.css?v=%s">' % (a, VER),
             '<link rel="stylesheet" href="%s/css/crm.css?v=%s">' % (a, VER),
             '<link rel="stylesheet" href="%s/css/examples.css?v=%s">' % (a, VER)]
    if lang == 'ko':
        # ko.css 는 전부 html[lang="ko"] 아래라 영어 쪽에서는 빈 요청이었습니다
        head += ['<link rel="stylesheet" href="%s/css/ko.css?v=%s">' % (a, VER)]
    if css:
        head += ['<style>', css.rstrip(), '</style>']
    head += ['<!--#alt--><!--/#alt-->', '</head>']

    tail = ['', ''] + ['<script src="%s/js/%s.js?v=%s"%s></script>'
                       % (a, s, VER, '' if s == 'site' or s == 'guide' else ' defer')
                       for s in scripts] + ['</body>', '</html>', '']

    out = '\n'.join(head) + '\n<body%s>\n' % (' data-grade="%s"' % grade if grade else '') \
        + body.strip() + '\n' + '\n'.join(tail)
    path = os.path.join(lang, slug)
    io.open(path, 'w', encoding='utf-8').write(out)
    return path


NAV = '<!--#nav--><!--/#nav-->'
FOOT = '<!--#footer--><!--/#footer-->'
