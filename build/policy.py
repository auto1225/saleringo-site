# -*- coding: utf-8 -*-
"""계약·환불·갱신·보관·관할을 한 파일에서 두 언어로 내보낸다.

왜 이것이 필요한가.

한국어 약관 제10조는 "회사는 이용자에게 불리한 전속관할 조항을 두지
않습니다" 라고 했고, 같은 회사의 영문 약관 §5 는 "Disputes ... are heard
in the courts of Seoul" 이라고 했습니다. 어느 쪽이 계약인지는 구매자가
어느 언어 페이지를 봤는가라는 우연으로 갈렸습니다.

환불도 마찬가지였습니다. 영문 요금 페이지는 "일부 기간은 환불하지
않는다", 영문 약관과 주문서는 "남은 기간을 일할 환불한다" 였습니다.
그리고 "매월 자동결제" 와 "Nothing renews" 가 같은 구매 흐름 안에
나란히 있었습니다.

한쪽을 손으로 고치면 다른 쪽은 그대로 남습니다. 실제로 그렇게 되어
있었습니다. 그래서 문장은 assets/data/policy.json 한 곳에만 두고,
두 언어의 페이지가 여기서 받아 갑니다.

    python build/policy.py            페이지에 심는다
    python build/policy.py --check    심은 것과 원본이 같은지만 본다

페이지에는 표시자를 둡니다. 이 저장소가 이미 nav·footer 에 쓰는 방식과
같습니다.

    <!--#policy:refund--> … <!--/#policy:refund-->
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CHECK = "--check" in sys.argv
P = json.load(io.open("assets/data/policy.json", encoding="utf-8"))


def block(name, lang):
    """policy.json 에서 한 덩어리를 그 언어의 HTML 로."""
    ko = lang == "ko"
    k = "ko" if ko else "en"

    if name == "formation":
        steps = "".join(
            '<li><b>%s</b><span>%s</span></li>' % (s[k]["title"], s[k]["body"])
            for s in P["contractFormation"]["steps"]
        )
        return (
            '<p class="polsum">%s</p><ol class="polsteps">%s</ol>'
            % (P["contractFormation"]["summary"][k], steps)
        )

    if name == "refund":
        r = P["refund"]
        return "<p>%s</p><p>%s</p>" % (r["summary"][k], r["companyFault"][k])

    if name == "cancellation":
        c = P["cancellation"]
        return "<p>%s</p><p>%s</p>" % (c["beforeStart"][k], c["afterStart"][k])

    if name == "renewal":
        return "<p>%s</p>" % P["renewal"]["summary"][k]

    if name == "law":
        g = P["governingLaw"]
        return "".join(
            "<p>%s</p>" % g[x][k] for x in ("law", "forum", "localRights", "beforeSuing")
        )

    if name == "retention":
        rows = "".join(
            "<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
            % (i[k]["label"], i[k]["period"], i[k]["basis"])
            for i in P["retention"]["items"]
        )
        head = (
            "<tr><th>구분</th><th>보관기간</th><th>근거</th></tr>"
            if ko
            else "<tr><th>What</th><th>How long</th><th>Why</th></tr>"
        )
        return (
            '<div class="dtwrap"><table class="dtable"><thead>%s</thead>'
            "<tbody>%s</tbody></table></div>" % (head, rows)
        )

    raise KeyError(name)


NAMES = ("formation", "refund", "cancellation", "renewal", "law", "retention")


def apply_to(path, lang):
    """표시자 사이를 policy.json 의 내용으로 채운다."""
    s = io.open(path, encoding="utf-8").read()
    original = s
    found = []
    for name in NAMES:
        pat = re.compile(
            r"(<!--#policy:%s-->)(.*?)(<!--/#policy:%s-->)" % (name, name), re.S
        )
        if not pat.search(s):
            continue
        found.append(name)
        s = pat.sub(lambda m: m.group(1) + block(name, lang) + m.group(3), s)
    if not found:
        return None, []
    changed = s != original
    if changed and not CHECK:
        io.open(path, "w", encoding="utf-8").write(s)
    return changed, found


TARGETS = [
    ("en/terms.html", "en"),
    ("ko/terms.html", "ko"),
    ("en/privacy.html", "en"),
    ("ko/privacy.html", "ko"),
    ("en/checkout.html", "en"),
    ("ko/checkout.html", "ko"),
]

stale = []
placed = 0
missing = []

for path, lang in TARGETS:
    if not os.path.exists(path):
        continue
    changed, found = apply_to(path, lang)
    if changed is None:
        missing.append(path)
        continue
    placed += len(found)
    if changed:
        stale.append((path, found))

print("정책 판 %s (%s 시행)" % (P["version"], P["effective"]))
print("표시자 %d곳에 심었습니다." % placed)

if missing:
    print()
    print("표시자가 아직 없는 페이지 — 정책 문장을 손으로 적고 있다는 뜻입니다:")
    for m in missing:
        print("   %s" % m)

if CHECK:
    if stale:
        print()
        print("!! 페이지에 적힌 정책이 assets/data/policy.json 과 다릅니다:")
        for path, names in stale:
            print("   %-22s %s" % (path, ", ".join(names)))
        print()
        print("   python build/policy.py 로 맞추십시오.")
        print("   페이지를 직접 고치지 마십시오 — 다른 언어가 따라오지 않습니다.")
        sys.exit(1)
    print("페이지와 policy.json 이 같은 말을 합니다.")
elif stale:
    print()
    for path, names in stale:
        print("   고침 %-22s %s" % (path, ", ".join(names)))
