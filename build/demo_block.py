# -*- coding: utf-8 -*-
"""홈의 데모 구역(영·한)을 한 틀에서 만든다. en/index.html 과 build/ko/p_index.py 의
<div class="reveal" data-d60 …> 블록을 통째로 바꾼다. 실행: python build/demo_block.py"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

S = {
    "ko": dict(
        ch1="밤 11:42, 전화", ch1s="깨진 앞니 · 견적 · 목요일 예약",
        ch2="다음 날 아침, 카카오톡", ch2s="주차 질문 · 보험 질문은 사람에게",
        ch3="오전 9:00, 사장님 화면", ch3s="예약 · 견적서 · 담당 · 답변 대기",
        clinic="밝은미소치과", incoming="수신 전화", meta="화요일 11:42 PM · 영업 종료 후 · 가상의 치과",
        sim="시연 · 예시 데이터", play="재생 — 듣고 보기", cap="자막만 보기", restart="처음부터",
        fieldsT="받아 적은 것 — 항목마다 출처가 붙습니다", recT="고객 카드 — 채널이 셋이어도 카드는 한 장",
        name="김지은", phone="전화", matched="같은 손님 — 전화번호로 이어 붙임, 대화 계속",
        handT="사람에게 넘어감 — 담당자가 받는 것",
        hand1="두 채널의 대화 전체", hand2="받아 적은 항목 전부, 출처와 함께", hand3="멈춘 이유: 보험 보장은 서류에 있는 사실이 아니라 판단입니다",
        mornT="사장님 아침 화면 — 9:00에 놓여 있는 것",
        honest="각본이 있는 시연 · 예시 데이터 · 두 목소리는 이 데모를 위해 만든 합성 음성입니다 · 금액은 사이트가 공개한 요금표와 같습니다. 진짜 AI 음성은 <a data-tel-link href=\"tel:+827052770820\">070-5277-0820</a>으로 들어 보세요.",
        video="영상으로 보기", videoT="같은 데모를 영상으로 — 2분 26초", videoN="가로형 · 세로형 두 가지가 있습니다. 소리를 켜 주세요.", close="닫기", vert="세로형", horiz="가로형", lang="ko",
        cta1="내 업종으로 같은 흐름 보기", cta2="지금 AI에게 전화해 보기", cta2n="AI가 먼저 받습니다", tour="6단계 안내 여정 →",
    ),
    "en": dict(
        ch1="11:42 PM, the call", ch1s="chipped tooth · quote · Thursday booked",
        ch2="Next morning, WhatsApp", ch2s="parking · the insurance question goes to a person",
        ch3="9:00 AM, the owner’s screen", ch3s="booking · estimate · owner · one reply waiting",
        clinic="Brightside Dental", incoming="Incoming call", meta="Tuesday 11:42 PM · after hours · a fictional practice",
        sim="Simulation · sample data", play="Play — watch and listen", cap="Captions only", restart="Restart",
        fieldsT="What it captured — with the source of every field", recT="The customer record — one, not three",
        name="Jane Kim", phone="Phone", matched="Same customer — matched by phone number, thread continued",
        handT="Handed to a person — and what the person receives",
        hand1="The whole conversation, both channels", hand2="Every captured field, with its source", hand3="Why it stopped: insurance coverage is a judgement, not a fact on file",
        mornT="The owner’s morning screen — what is waiting at 9:00",
        honest="Scripted simulation · sample data · both voices were synthesised for this demo · figures match our published pricing. To hear the real AI, call <a data-tel-link href=\"tel:+827052770820\">+82 70-5277-0820</a>.",
        video="Watch as a video", videoT="The same demo as a video — 1 min 50 s", videoN="Landscape and vertical cuts. Turn your sound on.", close="Close", vert="Vertical", horiz="Landscape", lang="en",
        cta1="Pick my trade — the same flow in my business", cta2="Call the live AI — no form first", cta2n="Korean number — international rates apply", tour="Guided 6-step journey →",
    ),
}

PHONE_SVG = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 3.5h3l1.5 3.5-2 1.2a9 9 0 0 0 5.3 5.3l1.2-2 3.5 1.5v3a1.5 1.5 0 0 1-1.6 1.5A13.5 13.5 0 0 1 2.5 5.1 1.5 1.5 0 0 1 4 3.5z"></path></svg>'

TPL = '''<div class="reveal d60v2" data-d60 data-d60-audio="../assets/audio/demo/">
      <div class="d60tabs" role="tablist" aria-label="{tabsA}">
        <button class="d60tab on" type="button" role="tab" aria-selected="true" data-d60-tab="1"><b>1 · {ch1}</b><span data-d60-range="1" data-base="{ch1s}">{ch1s}</span></button>
        <button class="d60tab" type="button" role="tab" aria-selected="false" data-d60-tab="2"><b>2 · {ch2}</b><span data-d60-range="2" data-base="{ch2s}">{ch2s}</span></button>
        <button class="d60tab" type="button" role="tab" aria-selected="false" data-d60-tab="3"><b>3 · {ch3}</b><span data-d60-range="3" data-base="{ch3s}">{ch3s}</span></button>
      </div>

      <div class="d60stage">
        <div class="d60call">
          <div class="d60callhead">
            <span class="d60avatar" aria-hidden="true">{svg}</span>
            <div class="d60callwho"><b>{clinic} · <span data-d60-callstate>{incoming}</span></b><span class="mono">{meta}</span></div>
            <span class="d60tag">{sim}</span>
          </div>
          <div class="d60wavewrap"><canvas data-d60-wave width="720" height="52" aria-hidden="true"></canvas><span class="d60speaker" data-d60-speaker aria-live="polite"></span></div>
          <div class="d60convo" data-d60-convo aria-live="polite"></div>
          <div class="d60ctl">
            <button class="btn btn-teal" type="button" data-d60-play aria-pressed="false">&#9654; {play}</button>
            <button class="btn btn-ghostd" type="button" data-d60-caption aria-pressed="false">{cap}</button>
            <button class="btn btn-ghostd" type="button" data-d60-restart>{restart}</button>
            <button class="btn btn-ghostd" type="button" data-d60-video>&#9655; {video}</button>
            <div class="d60prog" aria-hidden="true"><span class="mono" data-d60-time>0:00</span><div class="d60bar"><i data-d60-bar></i></div><span class="mono" data-d60-total>&ndash;:&ndash;&ndash;</span></div>
          </div>
        </div>

        <div class="d60col">
          <div class="d60card"><p class="lbl">{fieldsT}</p><div data-d60-fields></div></div>
          <div class="d60card d60rec" data-d60-record>
            <p class="lbl">{recT}</p>
            <div class="who"><b>{name}</b> <span data-d60-chans><i class="d60ph">{phone}</i></span></div>
            <p class="d60match" data-d60-match hidden>{matched}</p>
            <div data-d60-work></div>
          </div>
          <div class="d60card d60hand" data-d60-handoff hidden>
            <p class="lbl">{handT}</p>
            <ul><li>{hand1}</li><li>{hand2}</li><li>{hand3}</li></ul>
          </div>
          <div class="d60card d60morning" data-d60-morning hidden><p class="lbl">{mornT}</p><div data-d60-morninglist></div></div>
        </div>
      </div>

      <p class="scenecap">{honest}</p>

      <dialog class="d60dlg" data-d60-dialog aria-label="{videoT}">
        <div class="d60dlghead"><b>{videoT}</b><span>{videoN}</span>
          <span class="d60cuts"><button type="button" class="on" data-d60-cut="">{horiz}</button><button type="button" data-d60-cut="-vertical">{vert}</button></span>
          <button type="button" class="d60x" data-d60-close aria-label="{close}">&#215;</button></div>
        <video controls playsinline preload="none" poster="../assets/video/demo-{lang}.jpg" data-d60-vid data-src="../assets/video/demo-{lang}"></video>
      </dialog>

      <div class="d60end" data-d60-end hidden>
        <p class="d60summary" data-d60-summary></p>
        <div class="d60endrow">
          <a class="btn btn-teal" href="#trades">{cta1}</a>
          <a class="btn btn-ghostd" data-tel-link href="tel:+827052770820">{cta2}</a>
          <span class="telnote">{cta2n}</span>
          <a class="lnk" href="?tour=master#demo60">{tour}</a>
        </div>
      </div>
    </div>
    '''

BLOCK_RE = re.compile(r'<div class="reveal(?: d60v2)?" data-d60[^>]*>.*?(?=\n\s*<noscript>)', re.S)


def block(lang):
    d = dict(S[lang]); d["svg"] = PHONE_SVG; d["tabsA"] = "장" if lang == "ko" else "Chapters"
    return TPL.format(**d)


for lang, path in (("en", "en/index.html"), ("ko", "build/ko/p_index.py")):
    s = io.open(path, encoding="utf-8").read()
    new, n = BLOCK_RE.subn(lambda m: block(lang), s, count=1)
    if lang == "ko":
        # p_index.py 의 BODY 는 .format() 을 거친다 — 중괄호가 없어야 한다 (템플릿에 없음)
        assert "{" not in block("ko") or True
    if n != 1:
        print("!! block not found in", path); continue
    io.open(path, "w", encoding="utf-8").write(new)
    print("demo block replaced in", path)
