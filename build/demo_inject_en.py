# -*- coding: utf-8 -*-
"""손으로 쓴 영문 업종 페이지 25쪽에 업종 데모를 넣는다. 멱등 (<!--demo:v2--> 표식).

넣는 자리: 히어로(</header>) 바로 뒤. 모든 페이지가 같은 자리에 같은 플레이어를 갖는다.
실행: python build/demo_inject_en.py"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "build"))
import demo_block  # noqa: E402

SECTION = """<!--demo:v2-->
<section class="sec-light t-md" id="demo">
  <div class="wrap">
    <div class="reveal" style="max-width:720px;">
      <span class="eyebrow light"><i></i>Hear it &middot; {name}</span>
      <h2 class="h2" style="margin-top:20px;">The call, the next morning&rsquo;s message, <br>and what was waiting at nine.</h2>
      <p class="lead" style="margin-top:16px;">A scripted call for a {lname}: two synthetic voices, an example price list, and every field it captured with its source. Press play &mdash; about two and a half minutes.</p>
    </div>
    {block}
    <noscript><p class="lead">The demo needs JavaScript. The same story is written out in the worked examples below.</p></noscript>
  </div>
</section>
<!--/demo:v2-->"""

MARK = re.compile(r"<!--demo:v2-->.*?<!--/demo:v2-->\n?", re.S)


def inject(path, slug, name):
    s = io.open(path, encoding="utf-8").read()
    if not os.path.exists(os.path.join(ROOT, "assets", "demo", slug + ".json")):
        print("  skip (no script):", slug); return
    block = demo_block.block("en", slug, rel="../../")
    sec = SECTION.format(name=name, lname=name[0].lower() + name[1:], block=block)
    s2 = MARK.sub("", s)
    i = s2.find("</header>")
    if i < 0: print("  !! no header:", path); return
    i += len("</header>")
    s2 = s2[:i] + "\n\n" + sec + "\n" + s2[i:]
    if 'demofull.js' not in s2:
        m = re.search(r'<script src="(\.\./\.\./assets/js/)site\.js\?v=([0-9.]+)"[^>]*></script>', s2)
        if m:
            tag = '<script src="%sdemofull.js?v=%s" defer></script>' % (m.group(1), m.group(2))
            s2 = s2[:m.end()] + "\n" + tag + s2[m.end():]
        else:
            print("  !! site.js tag not found:", slug)
    if s2 != s:
        io.open(path, "w", encoding="utf-8").write(s2); print("  ok", slug)


if __name__ == "__main__":
    import json
    names = json.load(io.open(os.path.join(ROOT, "build", "demo", "en_names.json"), encoding="utf-8"))
    for slug, name in names.items():
        p = os.path.join(ROOT, "en", "industries", slug + ".html")
        if os.path.exists(p): inject(p, slug, name)
