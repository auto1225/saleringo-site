# -*- coding: utf-8 -*-
"""페이지 안 링크가 가리키는 자리가 실제로 있는지 본다.

routes.py 는 파일이 있는지만 봅니다. href="./index.html#today" 처럼
파일은 있는데 그 안의 자리가 없어진 링크는 잡히지 않고, 누르면 그냥
맨 위로 갑니다 — 고장 난 티가 안 나는 종류의 고장입니다.

절 하나를 지울 때마다 이 검사를 돌리십시오.

    python build/anchorcheck.py     끊어진 자리를 모두 보고하고 1 로 끝냅니다
"""
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PAGES = sorted(glob.glob("en/**/*.html", recursive=True)) + \
        sorted(glob.glob("ko/**/*.html", recursive=True))

ids = {}
for p in PAGES:
    s = io.open(p, encoding="utf-8").read()
    ids[os.path.normpath(p)] = set(re.findall(r'\sid="([^"]+)"', s)) | \
                               set(re.findall(r'\sname="([^"]+)"', s))

bad = []

# guide.js 의 안내 투어 정거장도 페이지 속 자리를 가리킵니다. href 가
# 아니라서 아래 본검사에는 안 걸리는데, 실제로 두 번 끊어진 적이
# 있습니다 — 절을 옮기고 투어를 잊는 것이 정확히 그 사고입니다.
GUIDE = "assets/js/guide.js"
if os.path.exists(GUIDE):
    g = io.open(GUIDE, encoding="utf-8").read()
    for m in re.finditer(r"u:\s*'([a-z0-9/.-]+\.html)'\s*,\s*h:\s*'#([a-z0-9-]+)'", g):
        page, frag = m.group(1), m.group(2)
        for lang in ("en", "ko"):
            target = os.path.normpath(os.path.join(lang, page))
            if target not in ids:
                continue
            if frag not in ids[target]:
                # 한국어에 절이 없어서 그 언어의 투어가 건너뛰는 것은
                # build.py 의 규칙과 같아 en 만 오류로 봅니다
                if lang == "en":
                    bad.append((GUIDE, "%s#%s" % (page, frag), target))

for p in PAGES:
    s = io.open(p, encoding="utf-8").read()
    for href in re.findall(r'href="([^"]*#[^"]+)"', s):
        page, frag = href.split("#", 1)
        if not frag or frag.startswith("~"):
            continue
        if page.startswith(("http", "mailto", "tel")):
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(p), page)) if page \
            else os.path.normpath(p)
        if target not in ids:
            continue                       # 파일 자체는 routes.py 의 일입니다
        if frag not in ids[target]:
            bad.append((p, href, target))

for p, href, t in bad:
    print("  %-24s %s   → %s 에 그 자리가 없습니다" % (p, href, t))
print("\n%d개 쪽, 끊어진 자리 %d곳" % (len(PAGES), len(bad)))
sys.exit(1 if bad else 0)
