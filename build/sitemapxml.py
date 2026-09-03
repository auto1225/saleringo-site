# -*- coding: utf-8 -*-
"""sitemap.xml 을 실제 쪽 목록에서 다시 쓴다.

손으로 유지되던 파일이라 status.html 같은 새 쪽이 빠졌다. 이제
en/·ko/ 의 HTML 전부를 훑어, 언어 짝(hreflang)까지 붙여 낸다.
빌드마다 돌려도 결과가 같다.
"""
import glob
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

SITE = "https://claude.saleringo.com"
SKIP = {"404.html"}


def pages(lang):
    out = []
    for f in sorted(glob.glob(lang + "/*.html") + glob.glob(lang + "/industries/*.html")):
        rel = f.replace("\\", "/")
        if os.path.basename(rel) in SKIP:
            continue
        out.append(rel[len(lang) + 1:])
    return out


def prio(rel):
    if rel == "index.html":
        return "1.0"
    if rel in ("pricing.html", "checkout.html", "get-started.html", "demo.html"):
        return "0.9"
    if rel.startswith("industries/") and not rel.endswith("-pack.html"):
        return "0.8"
    if rel in ("privacy.html", "terms.html", "sitemap.html", "order-status.html"):
        return "0.3"
    return "0.7"


en = set(pages("en"))
ko = set(pages("ko"))
rows = []
for rel in sorted(en | ko):
    for lang in ("en", "ko"):
        if rel not in (en if lang == "en" else ko):
            continue
        loc = "%s/%s/%s" % (SITE, lang, rel)
        alts = []
        if rel in en:
            alts.append(("en", "%s/en/%s" % (SITE, rel)))
        if rel in ko:
            alts.append(("ko-KR", "%s/ko/%s" % (SITE, rel)))
        if rel in en:
            alts.append(("x-default", "%s/en/%s" % (SITE, rel)))
        rows.append(
            "  <url><loc>%s</loc><changefreq>weekly</changefreq><priority>%s</priority>\n" % (loc, prio(rel))
            + "".join('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>\n' % a for a in alts)
            + "  </url>\n")

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
       '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "".join(rows) + "</urlset>\n")
io.open("sitemap.xml", "w", encoding="utf-8").write(xml)
print("sitemap.xml: %d urls (en %d · ko %d)" % (len(rows), len(en), len(ko)))
