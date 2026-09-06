# -*- coding: utf-8 -*-
"""업종 65개를 하나씩 구석구석 검사한다 — 파일·JSON·음성·목록·라우트·사이트맵·사진 정합.

실행:  python build/tradecheck.py            전체
       python build/tradecheck.py dental solar   일부만
       python build/tradecheck.py --live       라이브(claude.saleringo.com)까지 200 확인
       python build/tradecheck.py --json out.json   결과를 JSON 으로도 저장
종료코드 0 = 결함 없음."""
import io
import json
import os
import re
import sys
import glob
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "build", "ko"))
sys.path.insert(0, os.path.join(ROOT, "build", "demo"))

LIVE = "https://claude.saleringo.com/"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128 Safari/537.36"}


def load_trades():
    from trades import TRADES
    from trades2 import TRADES2
    allt = list(TRADES) + list(TRADES2)
    for mod, key in (("trades3", "TRADES3"), ("trades4", "TRADES4"), ("trades5", "TRADES5"),
                     ("trades6", "TRADES6"), ("trades7", "TRADES7")):
        try:
            allt += getattr(__import__(mod), key)
        except Exception as ex:
            print("  !! cannot import", mod, ex)
    return allt


def rd(p):
    return io.open(p, encoding="utf-8").read()


def http(url, method="HEAD"):
    try:
        req = urllib.request.Request(url, headers=UA, method=method)
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def mp3_dur(p):
    try:
        from mutagen.mp3 import MP3
        return MP3(p).info.length
    except Exception:
        return 0


def check_page(slug, lang, kind, t, issues):
    """kind: 'trade' | 'pack'"""
    fn = "%s/industries/%s%s.html" % (lang, slug, "-pack" if kind == "pack" else "")
    if not os.path.exists(fn):
        issues.append((slug, lang, kind, "missing page", fn)); return None
    s = rd(fn)
    if 'lang="%s"' % lang not in s[:400]:
        issues.append((slug, lang, kind, "html lang attr", fn))
    for bad, why in (("PENDING", "photo placeholder"), ("{", "brace placeholder?"), ("undefined", "js undefined leaked"),
                     ("&amp;amp;", "double escape"), (">None<", "python None leaked"), ("nan", None)):
        if why is None: continue
        if bad == "{":
            if re.search(r"\{[a-z_]{2,}\}", s): issues.append((slug, lang, kind, why, fn))
        elif bad in s:
            issues.append((slug, lang, kind, why, fn))
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    title = (m.group(1) if m else "").strip()
    if not title: issues.append((slug, lang, kind, "no title", fn))
    if "<br" in title: issues.append((slug, lang, kind, "br in title", fn))
    if not re.search(r'<meta name="description" content="[^"]{40,}"', s):
        issues.append((slug, lang, kind, "meta description short/missing", fn))
    if not re.search(r'<link rel="canonical" href="[^"]+"', s):
        issues.append((slug, lang, kind, "no canonical", fn))
    # 언어 교차 링크
    other = "en" if lang == "ko" else "ko"
    if ('hreflang="%s"' % other) not in s:
        issues.append((slug, lang, kind, "no hreflang alternate", fn))
    # 내부 링크가 실제 파일을 가리키는가
    base = os.path.dirname(fn)
    for href in re.findall(r'href="(\.\.?/[^"#?]+\.html)', s):
        p = os.path.normpath(os.path.join(base, href))
        if not os.path.exists(p):
            issues.append((slug, lang, kind, "broken internal link " + href, fn))
    # 사진
    for src in set(re.findall(r'src="(https://images\.pexels\.com/photos/\d+/[^"?]+)', s)):
        pass  # 아래에서 대표 사진만 HEAD 로 확인 (트래픽 절약)
    if kind == "trade":
        if 'data-d60-script="../../assets/demo/%s.json' % slug not in s:
            issues.append((slug, lang, kind, "demo block not wired to its json", fn))
        if "demofull.js" not in s:
            issues.append((slug, lang, kind, "demofull.js missing", fn))
        if 'data-d60-pick' in s:
            issues.append((slug, lang, kind, "home-only pick list on trade page", fn))
        if s.count("<h1") != 1:
            issues.append((slug, lang, kind, "h1 count %d" % s.count("<h1"), fn))
        # 팩 페이지 링크
        if ("./%s-pack.html" % slug) not in s:
            issues.append((slug, lang, kind, "no link to pack page", fn))
        # 이름이 제목에 들어가는가
        name = t["name"] if lang == "ko" else ((t.get("en") or {}).get("name") or "")
        plain = re.sub(r"&[a-z]+;", "", name).replace("·", "").replace(" ", "")
        tp = re.sub(r"&[a-z]+;", "", title).replace("·", "").replace(" ", "")
        if name and plain[:4] not in tp and lang == "ko":
            issues.append((slug, lang, kind, "title lacks trade name (%s)" % name, fn))
    else:
        if ("./%s.html" % slug) not in s:
            issues.append((slug, lang, kind, "pack has no link back to trade page", fn))
        if 'class="fieldgrid"' not in s and not re.search(r"[Ff]ield|필드|항목", s):
            issues.append((slug, lang, kind, "no fields section", fn))
    return s


def check_demo(slug, t, issues):
    jp = "assets/demo/%s.json" % slug
    if not os.path.exists(jp):
        issues.append((slug, "-", "demo", "json missing", jp)); return
    try:
        d = json.load(io.open(jp, encoding="utf-8"))
    except Exception as ex:
        issues.append((slug, "-", "demo", "json invalid: %s" % ex, jp)); return
    for lang in ("ko", "en"):
        a = d.get(lang)
        if not a: issues.append((slug, lang, "demo", "lang missing in json", jp)); continue
        lines = a.get("lines") or []
        if not (8 <= len(lines) <= 14): issues.append((slug, lang, "demo", "line count %d" % len(lines), jp))
        total = 0.0
        for i, ln in enumerate(lines):
            mp = "assets/audio/demo/%s/%s/%02d-%s.mp3" % (slug, lang, i + 1, ln.get("who"))
            if not os.path.exists(mp) or os.path.getsize(mp) < 1000:
                issues.append((slug, lang, "audio", "missing/short mp3 line %d" % (i + 1), mp)); continue
            dur = ln.get("dur") or 0
            real = mp3_dur(mp)
            if real < 0.4: issues.append((slug, lang, "audio", "unreadable mp3 line %d" % (i + 1), mp))
            if dur and abs(real - dur) > 0.6: issues.append((slug, lang, "audio", "json dur %.1f != file %.1f line %d" % (dur, real, i + 1), mp))
            if not dur: issues.append((slug, lang, "demo", "no dur on line %d" % (i + 1), jp))
            total += real
            txt = ln.get("text") or ""
            n = len(re.sub(r"\s+", "", txt)) if lang == "ko" else len(txt)
            if real > 0 and n / real > (11 if lang == "ko" else 26):
                issues.append((slug, lang, "audio", "audio too short for its text (truncated?) line %d" % (i + 1), mp))
            if re.search(r"[<>{}\[\]]|&[a-z]+;", txt): issues.append((slug, lang, "demo", "markup in spoken line %d" % (i + 1), jp))
            if lang == "ko" and re.search(r"[A-Za-z]{4,}", txt) and not re.search(r"Saleringo|AI|SUV|MRI|CT|LED|CCTV|kW", txt):
                issues.append((slug, lang, "demo", "latin word in korean line %d: %s" % (i + 1, txt[:40]), jp))
        if total < 45: issues.append((slug, lang, "audio", "call audio only %.0fs" % total, jp))
        # 더 이상의 mp3 (남은 옛 파일)
        extra = sorted(glob.glob("assets/audio/demo/%s/%s/*.mp3" % (slug, lang)))
        if len(extra) != len(lines): issues.append((slug, lang, "audio", "mp3 files %d != lines %d" % (len(extra), len(lines)), jp))
        if any(p.endswith(".raw.mp3") for p in extra): issues.append((slug, lang, "audio", "raw temp mp3 left", jp))
        for k in ("biz", "meta", "summary", "honest", "person"):
            if not a.get(k): issues.append((slug, lang, "demo", "empty %s" % k, jp))
        if len(a.get("handoff") or []) != 3: issues.append((slug, lang, "demo", "handoff != 3", jp))
        if len(a.get("morning") or []) != 4: issues.append((slug, lang, "demo", "morning != 4", jp))
        chat = a.get("chat") or []
        if not chat or chat[0].get("who") != "user": issues.append((slug, lang, "demo", "chat must start with customer", jp))
        # 업종 이름과 가상 상호가 다른 업종 것이 아닌지: 상호에 '치과' 가 다른 slug 에 있으면 의심
        if slug != "dental" and lang == "ko" and "치과" in (a.get("biz") or ""): issues.append((slug, lang, "demo", "biz says 치과", jp))
        if slug != "dental" and lang == "en" and "Dental" in (a.get("biz") or ""): issues.append((slug, lang, "demo", "biz says Dental", jp))


def check_lists(slug, t, issues, ko_index, en_index, ko_ind, en_ind, sitemap, vercel):
    for nm, s in (("ko/index.html", ko_index), ("en/index.html", en_index)):
        if ('<option value="%s"' % slug) not in s: issues.append((slug, "-", "list", "not in home pick", nm))
    for nm, s in (("ko/industries.html", ko_ind), ("en/industries.html", en_ind)):
        if ('industries/%s.html' % slug) not in s: issues.append((slug, "-", "list", "not in industries listing", nm))
    for u in ("en/industries/%s.html", "ko/industries/%s.html", "en/industries/%s-pack.html", "ko/industries/%s-pack.html"):
        if (LIVE + (u % slug)) not in sitemap: issues.append((slug, "-", "sitemap", "url missing " + (u % slug), "sitemap.xml"))
    if ('"/industries/%s"' % slug) not in vercel and ('/industries/%s"' % slug) not in vercel:
        issues.append((slug, "-", "routes", "no clean-url route", "vercel.json"))


def check_photo(slug, t, issues):
    ph = t.get("photo") or ""
    if "PENDING" in ph:
        try:
            pj = json.load(io.open("build/demo/photos.json", encoding="utf-8"))
            if pj.get(slug): ph = "https://images.pexels.com/photos/%s/pexels-photo-%s.jpeg" % (pj[slug], pj[slug])
        except Exception:
            pass
    if not ph or "PENDING" in ph:
        issues.append((slug, "-", "photo", "no representative photo", "trades")); return
    code = http(ph + "?auto=compress&cs=tinysrgb&w=200")
    if code != 200: issues.append((slug, "-", "photo", "photo HTTP %s" % code, ph))


def check_live(slug, issues):
    for u in ("en/industries/%s.html", "ko/industries/%s.html", "en/industries/%s-pack.html", "ko/industries/%s-pack.html",
              "assets/demo/%s.json"):
        code = http(LIVE + (u % slug) + "?fresh=chk")
        if code != 200: issues.append((slug, "-", "live", "HTTP %s" % code, u % slug))
    for lang in ("ko", "en"):
        code = http(LIVE + "assets/audio/demo/%s/%s/01-ai.mp3?fresh=chk" % (slug, lang))
        if code != 200: issues.append((slug, lang, "live", "audio HTTP %s" % code, "01-ai.mp3"))


def main():
    live = "--live" in sys.argv
    out = None
    if "--json" in sys.argv: out = sys.argv[sys.argv.index("--json") + 1]
    only = [a for a in sys.argv[1:] if not a.startswith("-") and a != out]
    trades = load_trades()
    slugs = [t["slug"] for t in trades]
    if len(set(slugs)) != len(slugs):
        print("!! duplicate slugs:", [s for s in slugs if slugs.count(s) > 1])
    if only: trades = [t for t in trades if t["slug"] in only]
    ko_index, en_index = rd("ko/index.html"), rd("en/index.html")
    ko_ind, en_ind = rd("ko/industries.html"), rd("en/industries.html")
    sitemap, vercel = rd("sitemap.xml"), rd("vercel.json")
    issues = []
    for t in trades:
        slug = t["slug"]
        n0 = len(issues)
        if "en" not in t and not os.path.exists("en/industries/%s.html" % slug):
            issues.append((slug, "en", "trade", "no english data and no page", "trades"))
        for lang in ("ko", "en"):
            check_page(slug, lang, "trade", t, issues)
            check_page(slug, lang, "pack", t, issues)
        check_demo(slug, t, issues)
        check_lists(slug, t, issues, ko_index, en_index, ko_ind, en_ind, sitemap, vercel)
        check_photo(slug, t, issues)
        if live: check_live(slug, issues)
        n = len(issues) - n0
        print("%-22s %s" % (slug, "ok" if n == 0 else "%d issue(s)" % n))
    print()
    for i in issues: print("  ", " | ".join(str(x) for x in i))
    print("\ntrades: %d | issues: %d" % (len(trades), len(issues)))
    if out:
        io.open(out, "w", encoding="utf-8").write(json.dumps(
            [dict(slug=a, lang=b, area=c, issue=d, where=e) for a, b, c, d, e in issues], ensure_ascii=False, indent=1))
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
