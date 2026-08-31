# -*- coding: utf-8 -*-
"""초광폭 사고를 정적으로 잡는다.

2026-08-29, 초광폭 화면에서 첫 화면 요금제 3열이 화면 전체(1985px)로
퍼져 있었다. 원인은 셋이었고, 셋 다 이 파일이 잡는 유형이다.

  1. .wrap 이 일찍 닫혀 그 뒤 블록이 절 직속 고아가 됨 (index planstrip)
  2. 페이지 로컬 CSS 가 wrap 동반 클래스에 max-width:none (ko 법률 .doc)
  3. 풀블리드 밴드에 상한이 없음 — 이건 정적으로 못 잡아 site.css 의
     .photosplit 캡으로 해결했고, 여기서는 1·2만 검사한다.

검사 1: class="wrap" div 를 가진 절(section/header/footer) 안에서,
그 wrap 이 닫힌 뒤에 형제 블록 태그가 나오면 오류. 장식 레이어와
두 번째 wrap 은 허용.
"""
import glob
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OK_AFTER = ("wrap", "scrim", "tint", "grainlayer", "stars", "bgimg",
            "navwrap", "heroscroll")
BLOCK = ("div", "ul", "ol", "table", "p", "h1", "h2", "h3", "figure",
         "article", "form")

TAG = re.compile(r"<(/?)(section|header|footer|div|ul|ol|table|p|h1|h2|h3"
                 r"|figure|article|form)\b([^>]*)>")


def first_class(attrs):
    m = re.search(r'class="([^"]*)"', attrs)
    return (m.group(1).split() or [""])[0] if m else ""


def check(path):
    s = io.open(path, encoding="utf-8").read()
    i = s.find("<main")
    j = s.rfind("</main>")
    frag = s[i:j] if i >= 0 else s
    bad = []

    # 절 단위로 돈다
    stack = []          # (tag, cls, depth-at-open)
    depth = 0
    # 절마다: wrap 을 depth+1 에서 봤는가, 그 wrap 이 닫혔는가
    secstate = []       # [sec_depth, wrap_seen, wrap_closed]

    for m in TAG.finditer(frag):
        close, tag, attrs = m.group(1), m.group(2), m.group(3)
        cls = first_class(attrs)
        if not close:
            if tag in ("section", "header", "footer"):
                secstate.append([depth, False, False])
            elif secstate:
                sd, wseen, wclosed = secstate[-1]
                if depth == sd + 1:                  # 절 직속
                    if cls == "wrap" or cls.startswith("wrap "):
                        secstate[-1][1] = True
                        secstate[-1][2] = False
                    elif wseen and wclosed and tag in BLOCK \
                            and cls not in OK_AFTER:
                        ln = frag.count("\n", 0, m.start()) + 1
                        bad.append((ln, tag, cls or "(no-class)"))
            if "/>" not in attrs:
                depth += 1
                stack.append((tag, cls, depth))
        else:
            if tag in ("section", "header", "footer"):
                if secstate:
                    secstate.pop()
            elif secstate and stack:
                # wrap 닫힘 감지
                for k in range(len(stack) - 1, -1, -1):
                    if stack[k][0] == tag:
                        if stack[k][1] == "wrap" or stack[k][1].startswith("wrap"):
                            if secstate and stack[k][2] == secstate[-1][0] + 2:
                                secstate[-1][2] = True
                        del stack[k]
                        break
            depth = max(0, depth - 1)

    # 검사 2 — wrap 동반 클래스에 max-width:none
    for wm in re.finditer(r'class="wrap ([a-z0-9-]+)', s):
        co = wm.group(1)
        if re.search(r"\.%s\s*\{[^}]*max-width\s*:\s*none" % re.escape(co), s):
            bad.append((0, "css", ".%s{max-width:none}" % co))

    return bad


total = 0
for f in sorted(glob.glob("en/*.html") + glob.glob("en/industries/*.html")
                + glob.glob("ko/*.html") + glob.glob("ko/industries/*.html")):
    bs = check(f)
    if bs:
        total += len(bs)
        print("◆ %s" % f)
        for ln, tag, cls in bs[:5]:
            print("   L%-5d <%s class=%s> — wrap 밖 고아 또는 캡 해제" % (ln, tag, cls))

n = len(glob.glob("en/**/*.html", recursive=True)
        + glob.glob("ko/**/*.html", recursive=True))
print("%d개 쪽, 초광폭 위반 %d곳" % (n, total))
sys.exit(1 if total else 0)
