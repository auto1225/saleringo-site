# -*- coding: utf-8 -*-
"""사이트가 안내하는 이메일 주소가 실제로 메일을 받는지 확인한다.

왜 이것이 검사가 되어야 하는가.

이 사이트는 142개 페이지에서 hello@saleringo.com 을 188번 안내합니다.
주문 접수가 실패했을 때 "다시 시도하시거나 여기로 보내세요", 해지할 때
"주문번호와 함께 취소라고 보내세요", 약관의 "소송 이전에 먼저 연락
주세요", DPA·보안 개요 문서 요청 — 전부 그 주소입니다.

그런데 saleringo.com 에는 MX 레코드가 없습니다. SPF 도 없습니다.
A 레코드는 Vercel 엣지(76.76.21.21)라 SMTP 를 받지 않으므로, 암묵적 MX
대체 경로로도 배달되지 않습니다. **보내는 메일이 전부 반송됩니다.**

이런 종류는 아무도 모르게 오래 갑니다. 페이지는 멀쩡해 보이고, 빌드도
통과하고, 링크 검사도 통과합니다. 메일을 보낸 사람만 알고, 그 사람은
이미 떠난 뒤입니다.

    python build/mailcheck.py

네트워크를 씁니다(DNS-over-HTTPS). 못 물어보면 실패로 세지 않고
그렇다고 알려 줍니다 — 확인하지 못한 것을 확인한 척하지 않습니다.
"""
import glob
import io
import json
import os
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PAGES = sorted(
    glob.glob("en/**/*.html", recursive=True)
    + glob.glob("ko/**/*.html", recursive=True)
)

# 예시로 적어 둔 주소는 세지 않습니다. 받을 생각이 없는 주소입니다.
EXAMPLE = re.compile(r"@(example|test|yourcompany|yourbusiness|company|domain)\.", re.I)

found = {}
for p in PAGES:
    s = io.open(p, encoding="utf-8").read()
    for m in re.finditer(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", s):
        addr = m.group(0)
        if EXAMPLE.search(addr):
            continue
        found.setdefault(addr.lower(), []).append(p.replace(os.sep, "/"))

domains = sorted({a.split("@")[1] for a in found})


def dns(name, rtype):
    url = "https://dns.google/resolve?name=%s&type=%s" % (name, rtype)
    req = urllib.request.Request(url, headers={"accept": "application/dns-json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


status = {}
unreachable = False
for d in domains:
    try:
        mx = dns(d, "MX").get("Answer")
        txt = dns(d, "TXT").get("Answer") or []
        spf = any("v=spf1" in (x.get("data") or "") for x in txt)
        status[d] = {"mx": bool(mx), "spf": spf,
                     "hosts": [x.get("data") for x in (mx or [])][:3]}
    except Exception as e:
        unreachable = True
        status[d] = {"error": str(e)[:60]}

print("사이트가 안내하는 주소 %d개, 도메인 %d개" % (len(found), len(domains)))
print()

broken = []
for d in domains:
    st = status[d]
    addrs = sorted(a for a in found if a.endswith("@" + d))
    uses = sum(len(found[a]) for a in addrs)
    if "error" in st:
        print("  ?  %-24s 확인하지 못했습니다 (%s)" % (d, st["error"]))
        continue
    if st["mx"]:
        print("  O  %-24s MX 있음%s · 주소 %d개 · %d곳"
              % (d, "" if st["spf"] else " (SPF 없음)", len(addrs), uses))
    else:
        broken.append((d, addrs, uses))
        print("  X  %-24s MX 없음 — 이 도메인으로 오는 메일은 반송됩니다" % d)

if not broken:
    print()
    if unreachable:
        print("확인하지 못한 도메인이 있습니다. 위를 보십시오.")
        sys.exit(0)
    print("안내하는 주소가 모두 메일을 받을 수 있습니다.")
    sys.exit(0)

print()
print("=" * 66)
for d, addrs, uses in broken:
    print()
    print("%s — 반송되는 주소 %d개, 사이트에 %d번" % (d, len(addrs), uses))
    for a in addrs:
        pages = found[a]
        print("   %-28s %4d곳   예: %s" % (a, len(pages), pages[0]))

print()
print("이 주소들은 구매자가 막혔을 때 가라고 안내하는 곳입니다 —")
print("주문 접수 실패, 해지 요청, 문서 요청, 소송 이전 연락.")
print("보내면 반송되고, 보낸 사람은 답이 없다고 생각합니다.")
print()
print("고치는 법은 둘 중 하나입니다.")
print("  1. 도메인에 MX·SPF·DMARC 를 걸어 실제 사서함으로 넘긴다 (권장)")
print("  2. 그때까지 페이지의 주소를 수신이 확인된 주소로 바꾼다")
sys.exit(1)
