# -*- coding: utf-8 -*-
"""en/industries.html 의 방(room) 목록에 새 업종을 넣는다. 멱등 (<!--gen:room--> 표식).

새 업종 데이터(trades3~5)의 en.room / en.room_d / en.room_no 로 <li> 를 만들어 해당 방 <ul> 끝에 붙인다.
실행: python build/industries_rooms.py"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "build", "ko"))

NEW = []
for mod, key in (("trades3", "TRADES3"), ("trades4", "TRADES4"), ("trades5", "TRADES5")):
    try:
        NEW += getattr(__import__(mod), key)
    except Exception as ex:
        print("  skip", mod, str(ex)[:60])

NB = "&nbsp;"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def li(t):
    e = t["en"]; no = e.get("room_no") or ("0", "answers the AI invents")
    return ('            <li>\n'
            '              <a class="room-t" href="./industries/%s.html"><b>%s</b><span class="room-go" aria-hidden="true">&rarr;</span></a>\n'
            '              <span class="room-d">%s</span>\n'
            '              <span class="room-no"><b>%s</b>%s</span>\n'
            '            </li>' % (t["slug"], esc(e["name"]).replace("&amp;", "&amp;"), e.get("room_d", ""), esc(no[0]), esc(no[1])))


def main():
    p = "en/industries.html"; s = io.open(p, encoding="utf-8").read()
    s = re.sub(r"\n?<!--gen:room:[a-z-]+-->.*?<!--/gen:room-->", "", s, flags=re.S)
    by_room = {}
    for t in NEW:
        by_room.setdefault(t["en"]["room"], []).append(t)
    n = 0
    for room, ts in by_room.items():
        # 방의 <h3 id="rm-<room>"> 뒤 첫 </ul> 앞에 넣는다
        h = s.find('id="rm-%s"' % room)
        if h < 0: print("  !! room not found:", room); continue
        u = s.find("</ul>", h)
        gen = "\n<!--gen:room:%s-->\n%s\n<!--/gen:room-->" % (room, "\n".join(li(t) for t in ts))
        s = s[:u] + gen + "\n          " + s[u:]
        n += len(ts)
    io.open(p, "w", encoding="utf-8").write(s)
    print("industries.html: %d new trades placed in %d rooms" % (n, len(by_room)))


if __name__ == "__main__":
    main()
