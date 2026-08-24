# -*- coding: utf-8 -*-
"""One chrome, two languages, sixty-nine pages.

The navigation is a 9.9KB block that appears on every page of the site. Before
this, changing one link in it meant editing sixty-nine files, and adding a
Korean site would have meant editing a hundred and thirty-eight. The parts that
actually differed between those sixty-nine copies were three: how deep the page
sits in the tree, which item is the current page, and whether the bar is over a
light section.

So the block lives once, in build/chrome/, with those three as parameters and
every human-readable word replaced by a key. The words live in
build/strings/<lang>.json. Structure is edited once; translation is the only
thing kept per language.

    python build/build.py            rebuild every page in place
    python build/build.py --check    rebuild into memory and report any page
                                     that would change, without writing

The check mode is the safety rail: run it after editing the chrome and it tells
you exactly which pages move, and run it after editing nothing and it must
report zero.

Pages opt in by carrying markers:

    <!--#nav-->  ...anything...  <!--/#nav-->
    <!--#footer--> ... <!--/#footer-->

A page without them is left completely alone, which is how a page with a
deliberately different header keeps it.
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

VERSION = None          # read from the pages themselves, so one bump still works
LANGS = ('en', 'ko')


# Which top-level panel owns which page. This cannot be derived from the links:
# get-started.html is not listed in the pricing panel and cross-border.html is
# not listed in the trade panel, yet both belong there - the panel that lights
# up is an editorial claim about where the page sits, not a link lookup. So it
# is written down once, here, and the Korean site inherits it by filename.
OWNER = {
    'about.html': 'nt-trust', 'privacy.html': 'nt-trust', 'security.html': 'nt-trust',
    'sitemap.html': 'nt-trust', 'terms.html': 'nt-trust', 'verified-ai.html': 'nt-trust',
    'ai-answering-service.html': 'nt-how', 'integrations.html': 'nt-how',
    'platform.html': 'nt-how', 'voice.html': 'nt-how', 'webchat.html': 'nt-how',
    'whatsapp.html': 'nt-how',
    'demo.html': 'nt-see', 'examples.html': 'nt-see', 'index.html': 'nt-see',
    'get-started.html': 'nt-price', 'pricing.html': 'nt-price',
    'cross-border.html': 'nt-trade', 'industries.html': 'nt-trade',
}


def load(name):
    return io.open(os.path.join('build', 'chrome', name), encoding='utf-8').read()


def strings(lang):
    p = os.path.join('build', 'strings', '%s.json' % lang)
    if not os.path.exists(p):
        return {}
    return json.load(io.open(p, encoding='utf-8'))


def render(tpl, lang, root, assets, ver, onlight, here, fallback):
    """fill the three parameters and every string key"""
    out = tpl
    out = out.replace('{{root}}', root)
    out = out.replace('{{assets}}', assets)
    out = out.replace('{{ver}}', ver)
    out = out.replace('{{onlight}}', ' onlight' if onlight else '')

    tbl = strings(lang)
    def word(m):
        k = m.group(1)
        if k in tbl:
            return tbl[k]
        if k in fallback:
            return fallback[k]        # not translated yet: show the English
        return ''
    out = re.sub(r'\{\{t:([\w.\-]+)\}\}', word, out)

    # The current page marks itself, and the two marks mean different things.
    #   np-here  goes on a link whose href IS this page, so a reader opening
    #            the panel sees the entry they are already standing on.
    #   navtop on goes on the button of the panel that holds any link to this
    #            page, fragment or not - that panel owns the page. Where two
    #            panels hold one, the later one wins, which is the convention
    #            the hand-written pages already followed.
    if here:
        target = root + here
        # the logo points home on every page; it is a button, not a nav entry,
        # and marking it would tell a reader they are "here" on all 69 pages
        exact = re.compile(r'(<a(?:\s+class="(?!logo)[^"]*")?\s+href="' + re.escape(target) + r'")(>)')
        out, n = exact.subn(lambda m: m.group(1) +
                            (' aria-current="page" class="np-here"' if 'class=' not in m.group(1)
                             else ' aria-current="page"') + m.group(2), out)
        own = OWNER.get(here) or ('nt-trade' if here.startswith('industries/') else None)
        if own:
            j = out.find('id="%s"' % own)
            j = out.rfind('<button class="navtop"', 0, j) if j > 0 else -1
            if j >= 0:
                k = out.index('>', j) + 1
                seg = (out[j:k].replace('class="navtop"', 'class="navtop on"')
                                .replace('>', ' aria-current="true">', 1))
                out = out[:j] + seg + out[k:]
    return out


def page_params(path):
    p = path.replace('\\', '/')
    lang = p.split('/')[0]
    deep = p.count('/') > 1
    return {
        'lang': lang if lang in LANGS else 'en',
        'root': '../' if deep else './',
        'assets': '../../assets' if deep else '../assets',
        'here': os.path.basename(p) if not deep else 'industries/' + os.path.basename(p),
    }


def swap(html, tag, new):
    a = '<!--#%s-->' % tag
    b = '<!--/#%s-->' % tag
    i = html.find(a)
    j = html.find(b)
    if i < 0 or j < 0:
        return html, False
    return html[:i + len(a)] + '\n' + new + '\n' + html[j:], True


def build(check=False):
    nav_tpl = load('nav.html')
    foot_tpl = load('footer.html')
    en_fallback = strings('en')

    pages = []
    for lang in LANGS:
        pages += sorted(glob.glob('%s/*.html' % lang))
        pages += sorted(glob.glob('%s/industries/*.html' % lang))

    changed, skipped, done = [], 0, 0
    for fp in pages:
        s = io.open(fp, encoding='utf-8').read()
        if '<!--#nav-->' not in s and '<!--#footer-->' not in s:
            skipped += 1
            continue
        prm = page_params(fp)
        m = re.search(r'\?v=([0-9.]+)', s)
        ver = m.group(1) if m else '1.0'
        onlight = 'navwrap onlight' in s or '<!--#nav:onlight-->' in s

        out = s
        nav = render(nav_tpl, prm['lang'], prm['root'], prm['assets'], ver,
                     onlight, prm['here'], en_fallback)
        # the footer marks the current page too, in its own link columns
        foot = render(foot_tpl, prm['lang'], prm['root'], prm['assets'], ver,
                      False, prm['here'], en_fallback)
        out, okn = swap(out, 'nav', nav)
        out, okf = swap(out, 'footer', foot)

        if out != s:
            changed.append(fp.replace('\\', '/'))
            if not check:
                io.open(fp, 'w', encoding='utf-8').write(out)
        done += 1

    print('%s: %d pages built, %d without markers left alone'
          % ('CHECK' if check else 'BUILD', done, skipped))
    if changed:
        print('%d page(s) %s:' % (len(changed), 'would change' if check else 'rewritten'))
        for c in changed[:12]:
            print('   ' + c)
        if len(changed) > 12:
            print('   ... and %d more' % (len(changed) - 12))
    else:
        print('no page changed')
    return changed


if __name__ == '__main__':
    build(check='--check' in sys.argv)
