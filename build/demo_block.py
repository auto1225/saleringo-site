# -*- coding: utf-8 -*-
"""데모 구역(영·한)을 한 틀에서 만든다 — 홈과 모든 업종 페이지가 같은 플레이어를 쓴다.

block(lang, slug, home=False, pick=None) → HTML 문자열.
  · lang  'ko' | 'en'
  · slug  assets/demo/<slug>.json 을 재생한다
  · home  True 면 업종 전환(select)·영상 버튼이 붙는다
  · pick  [(slug, name), ...] 업종 전환 목록 (home 일 때)

정적 문구(탭 제목·상호)는 빌드 시 JSON 에서 채워 JS 가 없어도 뼈대가 읽힌다. 나머지 UI 문구는 플레이어가 언어별로 채운다.
실행: python build/demo_block.py  → en/index.html 과 build/ko/p_index.py 의 홈 데모 블록을 갈아 끼운다.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

S = {
    "ko": dict(
        tabsA="장", incoming="수신 전화", sim="시연 · 예시 데이터", play="재생 — 듣고 보기", cap="자막만 보기", restart="처음부터",
        speedA="재생 속도", video="영상으로 보기", videoT="같은 데모를 영상으로 — 2분 26초",
        videoN="가로형 · 세로형 두 가지가 있습니다. 소리를 켜 주세요.", close="닫기", vert="세로형", horiz="가로형",
        fieldsT="받아 적은 것 — 항목마다 출처가 붙습니다", recT="고객 카드 — 채널이 셋이어도 카드는 한 장", phone="전화",
        matched="같은 손님 — 전화번호로 이어 붙임, 대화 계속", handT="사람에게 넘어감 — 담당자가 받는 것",
        mornT="사장님 아침 화면 — 9:00에 놓여 있는 것", pickL="내 업종으로 듣기", pickHint="55개 업종 · 같은 플레이어, 다른 통화",
        cta1="내 업종으로 같은 흐름 보기", cta2="지금 AI에게 전화해 보기", cta2n="AI가 먼저 받습니다", tour="6단계 안내 여정 →",
        caller="발신",
    ),
    "en": dict(
        tabsA="Chapters", incoming="Incoming call", sim="Simulation · sample data", play="Play — watch and listen", cap="Captions only", restart="Restart",
        speedA="Playback speed", video="Watch as a video", videoT="The same demo as a video — 1 min 50 s",
        videoN="Landscape and vertical cuts. Turn your sound on.", close="Close", vert="Vertical", horiz="Landscape",
        fieldsT="What it captured — with the source of every field", recT="The customer record — one, not three", phone="Phone",
        matched="Same customer — matched by phone number, thread continued", handT="Handed to a person — and what the person receives",
        mornT="The owner’s morning screen — what is waiting at 9:00", pickL="Hear it for my trade", pickHint="55 trades · same player, a different call",
        cta1="Pick my trade — the same flow in my business", cta2="Call the live AI — no form first", cta2n="Korean number — international rates apply", tour="Guided 6-step journey →",
        caller="From",
    ),
}

PHONE_SVG = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 3.5h3l1.5 3.5-2 1.2a9 9 0 0 0 5.3 5.3l1.2-2 3.5 1.5v3a1.5 1.5 0 0 1-1.6 1.5A13.5 13.5 0 0 1 2.5 5.1 1.5 1.5 0 0 1 4 3.5z"></path></svg>'


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def script_of(slug, lang):
    p = os.path.join(ROOT, "assets", "demo", slug + ".json")
    if not os.path.exists(p): return None
    try:
        return json.load(io.open(p, encoding="utf-8")).get(lang)
    except Exception:
        return None


def block(lang, slug, home=False, pick=None, rel="../"):
    d = dict(S[lang]); d["svg"] = PHONE_SVG; d["slug"] = slug; d["rel"] = rel; d["lang"] = lang
    sc = script_of(slug, lang) or {}
    ch = sc.get("chapters") or (["밤 11:42, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 사장님 화면"] if lang == "ko"
                                else ["11:42 PM, the call", "Next morning, WhatsApp", "9:00 AM, the owner’s screen"])
    subs = sc.get("chapterSubs") or ["", "", ""]
    d.update(ch1=esc(ch[0]), ch2=esc(ch[1]), ch3=esc(ch[2]), s1=esc(subs[0]), s2=esc(subs[1]), s3=esc(subs[2]),
             biz=esc(sc.get("biz", "")), meta=esc(sc.get("meta", "")), cust=esc((sc.get("customer") or {}).get("name", "")),
             honest=esc(sc.get("honest", "")), hand="".join("<li>%s</li>" % esc(x) for x in sc.get("handoff", [])))
    d["tel"] = ('<a data-tel-link href="tel:+827052770820">070-5277-0820</a>' if lang == "ko"
                else '<a data-tel-link href="tel:+827052770820">+82 70-5277-0820</a>')
    d["honestTel"] = ("진짜 AI 음성은 %s으로 들어 보세요." % d["tel"]) if lang == "ko" else ("To hear the real AI, call %s." % d["tel"])

    pick_html = ""
    if home and pick:
        opts = "".join('<option value="%s"%s>%s</option>' % (esc(s), ' selected' if s == slug else '', esc(n)) for s, n in pick)
        pick_html = ('<label class="d60pick"><span>%s</span><select data-d60-pick aria-label="%s">%s</select>'
                     '<small>%s</small></label>' % (d["pickL"], d["pickL"], opts, d["pickHint"]))
    d["pick"] = pick_html
    d["videoBtn"] = ('<button class="btn btn-ghostd" type="button" data-d60-video hidden>&#9655; %s</button>' % d["video"]) if home else ""
    d["videoDlg"] = ("""
      <dialog class="d60dlg" data-d60-dialog aria-label="{videoT}">
        <div class="d60dlghead"><b>{videoT}</b><span>{videoN}</span>
          <span class="d60cuts"><button type="button" class="on" data-d60-cut="">{horiz}</button><button type="button" data-d60-cut="-vertical">{vert}</button></span>
          <button type="button" class="d60x" data-d60-close aria-label="{close}">&#215;</button></div>
        <video controls playsinline preload="none" poster="{rel}assets/video/demo-{lang}.jpg" data-d60-vid data-src="{rel}assets/video/demo-{lang}"></video>
      </dialog>""".format(**d)) if home else ""
    d["endrow"] = ("""
      <div class="d60end" data-d60-end hidden>
        <p class="d60summary" data-d60-summary></p>
        <div class="d60endrow">
          <a class="btn btn-teal" href="#trades">{cta1}</a>
          <a class="btn btn-ghostd" data-tel-link href="tel:+827052770820">{cta2}</a>
          <span class="telnote">{cta2n}</span>
          <a class="lnk" href="?tour=master#demo60">{tour}</a>
        </div>
      </div>""".format(**d)) if home else ("""
      <div class="d60end" data-d60-end hidden>
        <p class="d60summary" data-d60-summary></p>
        <div class="d60endrow">
          <a class="btn btn-teal" href="{rel}get-started.html">{ctaT}</a>
          <a class="btn btn-ghostd" data-tel-link href="tel:+827052770820">{cta2}</a>
          <span class="telnote">{cta2n}</span>
        </div>
      </div>""".format(ctaT=("이 업종으로 견적 받기" if lang == "ko" else "Get my plan for this trade"), **d))

    return """<div class="reveal d60v2" data-d60 data-d60-script="{rel}assets/demo/{slug}.json" data-d60-audio="{rel}assets/audio/demo/">
      {pick}
      <div class="d60tabs" role="tablist" aria-label="{tabsA}">
        <button class="d60tab on" type="button" role="tab" aria-selected="true" data-d60-tab="1"><b>1 · {ch1}</b><span data-d60-range="1" data-base="{s1}">{s1}</span></button>
        <button class="d60tab" type="button" role="tab" aria-selected="false" data-d60-tab="2"><b>2 · {ch2}</b><span data-d60-range="2" data-base="{s2}">{s2}</span></button>
        <button class="d60tab" type="button" role="tab" aria-selected="false" data-d60-tab="3"><b>3 · {ch3}</b><span data-d60-range="3" data-base="{s3}">{s3}</span></button>
      </div>

      <div class="d60stage">
        <div class="d60call">
          <div class="d60callhead">
            <span class="d60avatar" aria-hidden="true">{svg}</span>
            <div class="d60callwho"><b><span data-d60-biz>{biz}</span> · <span data-d60-callstate>{incoming}</span></b><span class="mono" data-d60-meta>{meta}</span><span class="mono d60caller">{caller} <span data-d60-caller></span></span></div>
            <span class="d60tag">{sim}</span>
          </div>
          <div class="d60wavewrap"><canvas data-d60-wave width="720" height="52" aria-hidden="true"></canvas><span class="d60speaker" data-d60-speaker aria-live="polite"></span></div>
          <div class="d60convo" data-d60-convo aria-live="polite"></div>
          <div class="d60ctl">
            <button class="btn btn-teal" type="button" data-d60-play aria-pressed="false">&#9654; {play}</button>
            <button class="btn btn-ghostd" type="button" data-d60-caption aria-pressed="false">{cap}</button>
            <button class="btn btn-ghostd" type="button" data-d60-restart>{restart}</button>
            <button class="btn btn-ghostd d60speed" type="button" data-d60-speed aria-label="{speedA}">1×</button>
            {videoBtn}
            <div class="d60prog" aria-hidden="true"><span class="mono" data-d60-time>0:00</span><div class="d60bar"><i data-d60-bar></i></div><span class="mono" data-d60-total>&ndash;:&ndash;&ndash;</span></div>
          </div>
        </div>

        <div class="d60col">
          <div class="d60card"><p class="lbl">{fieldsT}</p><div data-d60-fields></div></div>
          <div class="d60card d60rec" data-d60-record>
            <p class="lbl">{recT}</p>
            <div class="who"><b data-d60-custname>{cust}</b> <span data-d60-chans><i class="d60ph">{phone}</i></span></div>
            <p class="d60match" data-d60-match hidden>{matched}</p>
            <div data-d60-work></div>
          </div>
          <div class="d60card d60hand" data-d60-handoff hidden>
            <p class="lbl">{handT}</p>
            <ul data-d60-handlist>{hand}</ul>
          </div>
          <div class="d60card d60morning" data-d60-morning hidden><p class="lbl">{mornT}</p><div data-d60-morninglist></div></div>
        </div>
      </div>

      <p class="scenecap" data-d60-honest>{honest} {honestTel}</p>
      {videoDlg}
      {endrow}
    </div>
    """.format(**d)


BLOCK_RE = re.compile(r'<div class="reveal(?: d60v2)?" data-d60[^>]*>.*?(?=\n\s*<noscript>)', re.S)


def trade_names():
    """홈의 업종 전환 목록 — 모든 업종을 이름순으로."""
    sys.path.insert(0, os.path.join(ROOT, "build", "ko"))
    out = {"ko": [], "en": []}
    try:
        from trades import TRADES
        from trades2 import TRADES2
        all_t = TRADES + TRADES2
        for mod, key in (("trades3", "TRADES3"), ("trades4", "TRADES4"), ("trades5", "TRADES5")):
            try:
                m = __import__(mod); all_t = all_t + getattr(m, key)
            except Exception:
                pass
    except Exception:
        return out
    en_names = json.load(io.open(os.path.join(ROOT, "build", "demo", "en_names.json"), encoding="utf-8")) if os.path.exists(os.path.join(ROOT, "build", "demo", "en_names.json")) else {}
    for t in all_t:
        slug = t["slug"]
        if not os.path.exists(os.path.join(ROOT, "assets", "demo", slug + ".json")): continue
        out["ko"].append((slug, re.sub(r"&[a-z]+;", "·", t["name"]).replace("·", " · ").replace("  ", " ")))
        out["en"].append((slug, (t.get("en") or {}).get("name") or en_names.get(slug) or slug.replace("-", " ").title()))
    out["ko"].sort(key=lambda x: x[1]); out["en"].sort(key=lambda x: x[1])
    return out


if __name__ == "__main__":
    os.chdir(ROOT)
    names = trade_names()
    for lang, path in (("en", "en/index.html"), ("ko", "build/ko/p_index.py")):
        s = io.open(path, encoding="utf-8").read()
        html = block(lang, "dental", home=True, pick=names[lang], rel="../")
        if lang == "ko":
            assert "{" not in html.replace("{", "", 0) or True
        new, n = BLOCK_RE.subn(lambda m: html, s, count=1)
        if n != 1:
            print("!! block not found in", path); continue
        io.open(path, "w", encoding="utf-8").write(new)
        print("demo block replaced in", path, "| pick:", len(names[lang]))
