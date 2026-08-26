# -*- coding: utf-8 -*-
"""키보드와 스크린리더가 서로 다른 화면을 보게 되는 곳을 찾는다.

감사에서 나온 지적:
  · Critical ARIA 오류 2건
  · 숨겨진 영역의 포커스 버튼

가장 잘 숨는 종류입니다. 눈으로 보면 멀쩡하고, 콘솔에도 아무것도 안 뜨고,
빌드도 통과합니다. 스크린리더를 켜 봐야만 드러납니다.

    python build/a11ycheck.py
"""
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PAGES = sorted(
    glob.glob("en/**/*.html", recursive=True) + glob.glob("ko/**/*.html", recursive=True)
)

problems = []

# 짝이 분명한 블록 태그만 봅니다. span·i 같은 인라인 태그는 문서 안에
# 수없이 많아서 짝을 세는 방식이 어긋납니다. 어긋난 검사는 오탐만 냅니다.
BLOCK = ("nav", "aside", "section", "form", "ul", "ol", "table", "main", "footer", "header")
FOCUSABLE = re.compile(
    r"<(?:a\s[^>]*href=|button\b|select\b|textarea\b"
    r"|input(?!\s[^>]*type=\"hidden\")\b"
    r"|[a-z]+\s[^>]*tabindex=\"(?!-)[0-9])",
    re.I,
)


def inner_of(s, tag, start):
    """여는 태그 뒤부터 짝이 맞는 닫는 태그까지."""
    depth = 1
    i = start
    pat = re.compile(r"</?%s\b" % tag, re.I)
    while depth and i < len(s):
        m = pat.search(s, i)
        if not m:
            return s[start:]
        depth += -1 if s[m.start() : m.start() + 2] == "</" else 1
        i = m.end()
    return s[start : max(start, i - len(tag) - 3)]


for p in PAGES:
    s = io.open(p, encoding="utf-8").read()
    page = p.replace(os.sep, "/")

    # ── 1. aria-hidden 안에 포커스 갈 수 있는 것 ────────────────────────
    #      키보드는 갈 수 있는데 스크린리더는 아무것도 읽지 않습니다.
    #      그 순간 사용자는 자기가 어디에 있는지 알 수 없습니다.
    for tag in BLOCK:
        for m in re.finditer(r'<%s\b[^>]*aria-hidden="true"[^>]*>' % tag, s):
            inner = inner_of(s, tag, m.end())
            f = FOCUSABLE.search(inner)
            if f:
                problems.append(
                    (
                        "aria-hidden 안의 포커스",
                        page,
                        "<%s aria-hidden> 안에 %s… — 키보드는 가는데 스크린리더는 못 읽습니다"
                        % (tag, re.sub(r"\s+", " ", inner[f.start() : f.start() + 40])),
                    )
                )

    ids = set(re.findall(r'\bid="([^"]+)"', s))

    # ── 2. 없는 id 를 가리키는 aria 참조 ────────────────────────────────
    for attr in ("aria-labelledby", "aria-describedby", "aria-controls", "aria-owns"):
        for m in re.finditer(r'%s="([^"]+)"' % attr, s):
            for ref in m.group(1).split():
                if ref not in ids:
                    problems.append(
                        ("닿지 않는 참조", page, '%s="%s" — 그런 id 가 없습니다' % (attr, ref))
                    )

    # ── 3. 붙지 않는 라벨 ───────────────────────────────────────────────
    for m in re.finditer(r'<label[^>]*\bfor="([^"]+)"', s):
        if m.group(1) not in ids:
            problems.append(
                ("붙지 않는 라벨", page, 'label for="%s" — 그런 id 가 없습니다' % m.group(1))
            )

    # ── 4. 한 페이지에 같은 id 가 둘 ───────────────────────────────────
    all_ids = re.findall(r'\bid="([^"]+)"', s)
    for i in set(all_ids):
        if all_ids.count(i) > 1:
            problems.append(("겹친 id", page, 'id="%s" 가 %d번' % (i, all_ids.count(i))))

    # ── 5. 이름 없는 칸 ────────────────────────────────────────────────
    #      라벨도 aria-label 도 없으면 스크린리더는 "편집 상자" 라고만 읽습니다.
    labelled = set(re.findall(r'<label[^>]*\bfor="([^"]+)"', s))

    # <label>…<input>…</label> 처럼 감싸는 형태도 이름이 붙은 것입니다.
    # for= 만 보면 이 흔한 형태를 전부 오탐으로 잡고, 오탐이 많은 검사는
    # 곧 아무도 안 봅니다.
    wrapped = []
    for lm in re.finditer(r"<label\b[^>]*>", s):
        end = s.find("</label>", lm.end())
        if end > 0:
            wrapped.append((lm.end(), end))

    def inside_label(pos):
        return any(a <= pos < b for a, b in wrapped)

    for m in re.finditer(r"<(input|select|textarea)\b([^>]*)>", s):
        attrs = m.group(2)
        if 'type="hidden"' in attrs:
            continue
        idm = re.search(r'\bid="([^"]+)"', attrs)
        has_name = (
            (idm and idm.group(1) in labelled)
            or inside_label(m.start())
            or "aria-label=" in attrs
            or "aria-labelledby=" in attrs
            or 'aria-hidden="true"' in attrs
        )
        if not has_name:
            problems.append(
                ("이름 없는 칸", page, "<%s %s> — 무엇을 넣는 칸인지 읽어 줄 것이 없습니다"
                 % (m.group(1), re.sub(r"\s+", " ", attrs.strip())[:60]))
            )


if not problems:
    print("키보드와 스크린리더가 같은 화면을 봅니다.")
    sys.exit(0)

kinds = {}
for k, page, msg in problems:
    kinds.setdefault(k, []).append((page, msg))

for k in sorted(kinds, key=lambda x: -len(kinds[x])):
    rows = kinds[k]
    print("\n%s (%d)" % (k, len(rows)))
    seen = set()
    shown = 0
    for page, msg in rows:
        if msg in seen:
            continue
        seen.add(msg)
        shown += 1
        if shown > 6:
            break
        print("   %-30s %s" % (page, msg))
    if len(rows) > shown:
        print("   … 외 %d건" % (len(rows) - shown))

print("\n합계 %d건" % len(problems))
sys.exit(1)
