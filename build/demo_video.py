# -*- coding: utf-8 -*-
"""홈 데모(assets/js/demofull.js)와 같은 각본으로 영상을 만든다.

브라우저 없이 그린다: PIL 로 프레임을, imageio-ffmpeg 의 ffmpeg 로 음성(assets/audio/demo)과 합친다.
  python build/demo_video.py ko            → assets/video/demo-ko.mp4 (1280×720)
  python build/demo_video.py en --vertical → assets/video/demo-en-vertical.mp4 (720×1280)
프레임 수를 줄이려고 12fps 로 그린다. 말풍선 글자는 음성 길이에 맞춰 차오른다."""
import io
import json
import os
import random
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LANG = (sys.argv[1] if len(sys.argv) > 1 else "ko")
VERT = "--vertical" in sys.argv
FPS = 12
W, H = (720, 1280) if VERT else (1280, 720)

PAPER = (246, 244, 238); CARD = (255, 255, 255); INK = (20, 26, 31); INK2 = (59, 69, 77); MUTE = (97, 107, 117)
LINE = (226, 221, 211); TEAL = (11, 120, 120); TEAL_S = (231, 241, 241); AMBER = (183, 121, 31); AMBER_S = (247, 240, 228)
GREEN = (47, 133, 90); GREEN_S = (233, 243, 237)

FONT_KO = r"C:\Windows\Fonts\malgun.ttf"; FONT_KOB = r"C:\Windows\Fonts\malgunbd.ttf"
FONT_EN = r"C:\Windows\Fonts\segoeui.ttf"; FONT_ENB = r"C:\Windows\Fonts\segoeuib.ttf"
_fc = {}


FONT_SYM = r"C:\Windows\Fonts\seguisym.ttf"


def font(size, bold=False):
    k = (size, bold)
    if k not in _fc:
        p = (FONT_KOB if bold else FONT_KO) if LANG == "ko" else (FONT_ENB if bold else FONT_EN)
        _fc[k] = ImageFont.truetype(p, size)
    return _fc[k]


def sym(size):
    """✓ ↻ ⇄ ☎ 같은 기호는 Segoe UI Symbol 로 — 맑은 고딕에는 없다."""
    k = ("sym", size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONT_SYM, size)
    return _fc[k]


def t(ko, en):
    return ko if LANG == "ko" else en


# ── the script (same words as demofull.js) ───────────────────────────────
MAN = json.load(io.open("assets/audio/demo/manifest.json", encoding="utf-8"))[LANG]
AUDIO_DIR = "assets/audio/demo/%s/" % LANG
CLINIC = t("밝은미소치과", "Brightside Dental")
META = t("화요일 11:42 PM · 영업 종료 후 · 가상의 치과", "Tuesday 11:42 PM · after hours · a fictional practice")
F = {
    "request": (t("요청", "Request"), t("앞니 크라운 — 이번 주", "Front-tooth crown — this week"), t("통화에서", "from the call")),
    "quote": (t("견적", "Quote"), t("지르코니아 크라운 550,000원", "Crown $1,100–1,600 + exam $95"), t("사장님 요금표", "your fee schedule")),
    "name": (t("이름", "Name"), t("김지은", "Jane Kim"), t("본인 발화", "caller said it")),
    "phone": (t("전화", "Phone"), t("010-4482-51··", "555-01··"), t("발신번호와 일치", "matches caller ID")),
    "slot": (t("예약", "Slot"), t("목 10:30", "Thu 10:30"), t("캘린더의 빈 시간", "free in your calendar")),
    "pain": (t("증상", "Symptom"), t("시림 — 응급 아님", "sensitive — not urgent"), t("본인 발화 · 진단 아님", "caller said it · not a diagnosis")),
}
WORK = {
    "booked": ("✓", t("예약 확정", "Booked"), t("목 10:30 · 캘린더에 들어감 · 확인 문자 발송", "Thu 10:30 · in your calendar · confirmation text sent")),
    "estimate": ("#", "Estimate #2472", t("지르코니아 크라운 550,000원 — 사장님 요금표에서", "Crown $1,100–1,600 + exam $95 — from your fee schedule")),
    "owner": ("@", t("담당·기한", "Owner & due"), t("데스크 담당 배정 · 목 09:00까지 차트 준비", "assigned to the desk · chart ready by Thu 9:00")),
    "follow": ("↻", t("후속 문자", "Follow-up"), t("무응답 시 D+2 안내 문자 초안 — 발송 전 사장님 확인", "D+2 nudge drafted — you approve before it sends")),
}
SIDE = {1: ["request"], 2: ["quote"], 5: ["name", "phone"], 6: ["slot", "crm", "booked"], 7: ["pain"], 8: ["estimate", "owner", "follow"]}
CHAT = [
    ("user", "7:40 AM", t("어제 예약한 김지은인데, 주차가 되나요?", "Hi, Jane Kim from last night — is there parking?")),
    ("ai", "+2 sec", t("네 — 건물 뒤에 전용 4자리가 있습니다. 목요일 10:30 예약은 그대로 유효합니다.", "Yes — four spaces behind the building. Your Thursday 10:30 booking is unchanged.")),
    ("user", "7:41 AM", t("제 보험으로 크라운이 보장되나요?", "Will my insurance cover the crown?")),
    ("ai", "+2 sec", t("보험 보장 판단은 담당자가 확인해 드려야 합니다. 대화 내용을 그대로 전달해 두었고, 오전 중에 연락드리겠습니다.", "Coverage is a call for the desk, not for me. I’ve passed our conversation along — someone will reply this morning.")),
]
PERSON = ("person", "9:12 AM", t("담당자 이수진입니다. 김지은 님, 보장 범위는 보험사 약관마다 달라서 목요일에 보험증권을 가져오시면 접수 때 바로 확인해 드릴게요.",
                                "This is Sujin from the front desk. Hi Jane — coverage depends on your plan, so bring your insurance card on Thursday and we’ll confirm at check-in."))
MORNING = [
    ("✓", t("새 예약 1건", "New booking"), t("김지은 · 목 10:30 · 캘린더에 있음", "Jane Kim · Thu 10:30 · in the calendar")),
    ("#", t("견적서 #2472", "Estimate #2472"), t("550,000원 · 문자로 발송됨 · 열람 확인", "$1,100–1,600 · sent by text · opened")),
    ("@", t("데스크 할 일", "Desk task"), t("목 09:00까지 차트 준비 · 담당 이수진", "chart ready by Thu 9:00 · owner: Sujin")),
    ("!", t("답변 대기 1건", "Waiting for a person"), t("보험 보장 문의 · 대화 전체 첨부 · 담당 이수진", "insurance question · full thread attached · owner: Sujin")),
]
CHAN = t("카카오톡", "WhatsApp")
CHAPTERS = [t("1 · 밤 11:42, 전화", "1 · 11:42 PM, the call"), t("2 · 다음 날 아침, 카카오톡", "2 · Next morning, WhatsApp"), t("3 · 오전 9:00, 사장님 화면", "3 · 9:00 AM, the owner’s screen")]
END_H = t("통화 1:40 · 카카오톡 4건 · 사람이 한 일: 답장 한 줄.", "One call · four messages · one human reply.")
END_S = t("나머지는 사장님이 자는 동안 끝났습니다.", "Everything else happened while the owner slept.")
END_CTA = t("진짜 AI 음성: 070-5277-0820 · claude.saleringo.com", "Hear the real AI: +82 70-5277-0820 · claude.saleringo.com")
HONEST = t("각본이 있는 시연 · 예시 데이터 · 두 목소리는 합성 음성입니다", "Scripted simulation · sample data · both voices synthesised")

# ── timeline (seconds) ────────────────────────────────────────────────────
RING = 2.4; GAP = 0.6
events = []  # (start, end, kind, payload)
tt = RING
for i, ln in enumerate(MAN):
    events.append((tt, tt + ln["dur"], "line", i)); tt += ln["dur"] + GAP
CALL_END = tt + 0.8
tt = CALL_END + 1.2
for j, (who, when, text) in enumerate(CHAT):
    d = 3.2 if who == "user" else 3.8
    events.append((tt, tt + d, "chat", j)); tt += d
HAND_AT = tt; tt += 3.0
events.append((tt, tt + 4.2, "person", 0)); tt += 4.2
MORNING_AT = tt; tt += 7.0
END_AT = tt; TOTAL = tt + 7.0
CH_AT = [0, CALL_END + 1.2, MORNING_AT]


def wrap(draw, text, fnt, maxw):
    out = []; cur = ""
    units = list(text) if LANG == "ko" else text.split(" ")
    for u in units:
        cand = (cur + u) if LANG == "ko" else (cur + (" " if cur else "") + u)
        if draw.textlength(cand, font=fnt) <= maxw or not cur:
            cur = cand
        else:
            out.append(cur); cur = u
    if cur: out.append(cur)
    return out


def rrect(d, box, r, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def chip(d, x, y, s, bg, fg, fnt):
    w = d.textlength(s, font=fnt) + 16
    rrect(d, (x, y, x + w, y + 22), 11, bg); d.text((x + 8, y + 3), s, font=fnt, fill=fg)
    return w


def bubble(d, x, y, maxw, who, when, text, frac=1.0, right=False):
    """말풍선 하나. frac 만큼 글자를 보여 준다. 아래 y 를 돌려준다."""
    f = font(21 if not VERT else 22); fb = font(14, True); fm = font(13)
    n = max(1, int(len(text) * frac)) if frac < 1 else len(text)
    shown = text[:n]
    lines = wrap(d, shown, f, maxw - 34)
    h = 20 + len(lines) * 30 + 6
    label = {"ai": "AI", "user": t("손님", "Customer"), "person": t("담당자", "Front desk")}[who]
    lw = d.textlength(label, font=fb)
    lx = (x + maxw - lw - 60) if right else x
    d.text((lx, y), label, font=fb, fill=INK); d.text((lx + lw + 8, y + 1), when, font=fm, fill=MUTE)
    y += 22
    bw = min(maxw, max(d.textlength(l, font=f) for l in lines) + 34) if lines else 120
    bx = (x + maxw - bw) if right else x
    fill = TEAL_S if who == "user" else CARD
    rrect(d, (bx, y, bx + bw, y + h), 16, fill, outline=(TEAL if who == "person" else LINE), width=2 if who == "person" else 1)
    for k, l in enumerate(lines):
        d.text((bx + 17, y + 12 + k * 30), l, font=f, fill=INK)
    return y + h + 14


def card_fields(d, box, keys):
    x0, y0, x1, y1 = box; rrect(d, box, 14, CARD, LINE)
    d.text((x0 + 18, y0 + 14), t("받아 적은 것 — 항목마다 출처", "What it captured — with sources"), font=font(13, True), fill=MUTE)
    y = y0 + 44
    for k in keys:
        lab, val, src = F[k]
        d.line((x0 + 18, y, x1 - 18, y), fill=LINE)
        d.text((x0 + 18, y + 10), lab, font=font(13, True), fill=MUTE)
        d.text((x0 + 92, y + 8), val, font=font(17, True), fill=INK)
        d.text((x0 + 92, y + 33), "✓", font=sym(13), fill=TEAL); d.text((x0 + 108, y + 34), src, font=font(13, True), fill=TEAL)
        y += 56
    return y


def card_record(d, box, chans, works, matched=False):
    x0, y0, x1, y1 = box; rrect(d, box, 14, CARD, LINE)
    d.text((x0 + 18, y0 + 14), t("고객 카드 — 채널이 셋이어도 카드는 한 장", "The customer record — one, not three"), font=font(13, True), fill=MUTE)
    d.text((x0 + 18, y0 + 40), t("김지은", "Jane Kim"), font=font(19, True), fill=INK)
    cx = x0 + 110
    for c in chans:
        cx += chip(d, cx, y0 + 44, c, TEAL_S if c != CHAN else GREEN_S, TEAL if c != CHAN else GREEN, font(12, True)) + 6
    y = y0 + 76
    if matched:
        d.text((x0 + 18, y - 1), "⇄", font=sym(14), fill=TEAL); d.text((x0 + 38, y), t("같은 손님 — 전화번호로 이어 붙임, 대화 계속", "Same customer — matched by phone number"), font=font(13, True), fill=TEAL); y += 26
    for k in works:
        ic, lab, val = WORK[k]
        d.line((x0 + 18, y, x1 - 18, y), fill=LINE)
        d.text((x0 + 22, y + 10), ic, font=sym(16) if ic in "✓↻" else font(16, True), fill=TEAL)
        d.text((x0 + 48, y + 8), lab, font=font(15, True), fill=INK)
        for q, l in enumerate(wrap(d, val, font(13), x1 - x0 - 70)[:2]):
            d.text((x0 + 48, y + 30 + q * 17), l, font=font(13), fill=MUTE)
        y += 66
    return y


def card_hand(d, box):
    x0, y0, x1, y1 = box; rrect(d, box, 14, AMBER_S, AMBER, 2)
    d.text((x0 + 18, y0 + 14), t("사람에게 넘어감 — 담당자가 받는 것", "Handed to a person — what they receive"), font=font(13, True), fill=AMBER)
    for k, s in enumerate([t("두 채널의 대화 전체", "The whole conversation, both channels"), t("받아 적은 항목 전부, 출처와 함께", "Every captured field, with its source"),
                           t("멈춘 이유: 보험 보장은 판단입니다", "Why it stopped: coverage is a judgement")]):
        d.text((x0 + 18, y0 + 44 + k * 26), "→ " + s, font=font(15), fill=INK2)
    return y0 + 130


def card_morning(d, box, n):
    x0, y0, x1, y1 = box; rrect(d, box, 14, CARD, LINE)
    d.text((x0 + 18, y0 + 14), t("사장님 아침 화면 — 9:00에 놓여 있는 것", "The owner’s morning screen — 9:00 AM"), font=font(13, True), fill=MUTE)
    y = y0 + 44
    for ic, lab, val in MORNING[:n]:
        d.line((x0 + 18, y, x1 - 18, y), fill=LINE)
        d.text((x0 + 22, y + 10), ic, font=sym(16) if ic in "✓↻" else font(16, True), fill=AMBER if ic == "!" else TEAL)
        d.text((x0 + 48, y + 8), lab, font=font(15, True), fill=INK)
        d.text((x0 + 48, y + 30), val, font=font(13), fill=MUTE); y += 56
    return y


def frame(sec):
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    ch = 2 if sec >= CH_AT[2] else (1 if sec >= CH_AT[1] else 0)
    # chapter strip
    cw = (W - 80) / 3
    for k, name in enumerate(CHAPTERS):
        x = 40 + k * cw
        d.line((x, 26, x + cw - 14, 26), fill=TEAL if k == ch else LINE, width=3)
        d.text((x, 34), name, font=font(13 if VERT else 14, True), fill=INK if k == ch else MUTE)
    # regions
    if VERT:
        L = (40, 70, W - 40, 760); R = (40, 780, W - 40, H - 40)
    else:
        L = (40, 70, 760, H - 70); R = (790, 70, W - 40, H - 70)
    # left: call card
    rrect(d, L, 18, CARD, LINE)
    x0, y0, x1, y1 = L
    d.ellipse((x0 + 18, y0 + 14, x0 + 54, y0 + 50), fill=TEAL)
    d.text((x0 + 28, y0 + 21), "☎", font=sym(17), fill=CARD)
    state = t("수신 전화", "Incoming call") if sec < RING else (t("통화 중", "On the call") if sec < CALL_END else (t("카카오톡", "WhatsApp") if ch == 1 else t("사장님 화면", "Owner’s screen")))
    d.text((x0 + 66, y0 + 12), "%s · %s" % (CLINIC, state), font=font(17, True), fill=INK)
    meta = META if ch == 0 else (t("수요일 7:40 AM · 같은 손님, 다른 채널 · 가상의 치과", "Wednesday 7:40 AM · same customer, another channel · a fictional practice") if ch == 1 else t("수요일 9:00 AM · 데스크 출근 · 가상의 치과", "Wednesday 9:00 AM · the desk opens · a fictional practice"))
    d.text((x0 + 66, y0 + 36), meta, font=font(12), fill=MUTE)
    chip(d, x1 - 150, y0 + 18, t("시연 · 예시 데이터", "Simulation · sample data"), AMBER_S, AMBER, font(12, True))
    d.line((x0, y0 + 62, x1, y0 + 62), fill=LINE)
    # waveform
    active = [e for e in events if e[2] == "line" and e[0] <= sec < e[1]]
    rnd = random.Random(int(sec * FPS))
    wy = y0 + 84
    for k in range(0, x1 - x0 - 40, 6):
        a = 0
        if active:
            who = MAN[active[0][3]]["who"]; a = rnd.random() * (14 if who == "ai" else 9) + 2
        elif sec < RING:
            a = 3 + 3 * abs(((sec * 4) % 2) - 1)
        d.line((x0 + 20 + k, wy - a, x0 + 20 + k, wy + a), fill=TEAL if active else LINE, width=3)
    spk = ""
    if active:
        spk = t("AI 말하는 중", "AI speaking") if MAN[active[0][3]]["who"] == "ai" else t("손님 말하는 중 · 전화 음질", "Customer speaking · phone line")
    d.text((x1 - 20 - d.textlength(spk, font=font(12)), wy + 22), spk, font=font(12), fill=MUTE)
    # conversation: collect visible items (bottom-aligned)
    items = []
    for s, e, kind, idx in events:
        if s > sec: continue
        if kind == "line":
            ln = MAN[idx]; frac = min(1.0, (sec - s) / max(0.4, ln["dur"] * 0.85))
            items.append(("ai" if ln["who"] == "ai" else "user", "+%ds" % int(s - RING) if ln["who"] == "ai" else "11:%02d PM" % (42 + int((s - RING) / 40)), ln["text"], frac))
        elif kind == "chat":
            who, when, text = CHAT[idx]; items.append((who, when, text, 1.0))
        elif kind == "person":
            who, when, text = PERSON; items.append((who, when, text, 1.0))
    if sec >= CALL_END and ch >= 1 and len(items) > 11:
        items = items[11:]  # 2·3장에서는 카카오톡 대화만 보여 준다
    # measure from the bottom up
    scratch = Image.new("RGB", (W, H)); sd = ImageDraw.Draw(scratch)
    heights = [bubble(sd, x0 + 20, 0, x1 - x0 - 40, w, wh, tx, fr, right=(w == "user")) for (w, wh, tx, fr) in items]
    y = y1 - 20; keep = []
    for it, hgt in zip(reversed(items), reversed(heights)):
        if y - hgt < y0 + 118: break
        y -= hgt; keep.append((it, y))
    for (w, wh, tx, fr), yy in keep:
        bubble(d, x0 + 20, yy, x1 - x0 - 40, w, wh, tx, fr, right=(w == "user"))
    if sec < RING:
        d.text((x0 + 20, y0 + 130), t("전화벨이 울립니다 — 데스크는 비어 있습니다.", "The phone rings — the desk is empty."), font=font(18), fill=MUTE)
    if sec >= HAND_AT and ch == 1:
        d.text((x0 + 20, y0 + 100), t("오전 9:00 — 사장님 화면.", "9:00 AM — the owner’s screen."), font=font(14), fill=MUTE)
    # right column
    done_lines = [idx for s, e, kind, idx in events if kind == "line" and e <= sec + 0.3]
    keys = [k for i in done_lines for k in SIDE.get(i, []) if k in F]
    works = [k for i in done_lines for k in SIDE.get(i, []) if k in WORK]
    chans = [t("전화", "Phone")] + ([CHAN] if ch >= 1 else [])
    rx0, ry0, rx1, ry1 = R; y = ry0
    if ch == 0:
        y = card_fields(d, (rx0, y, rx1, y + 44 + max(1, len(keys)) * 56 + 8), keys) + 16
        if works or "crm" in keys:
            card_record(d, (rx0, y, rx1, min(ry1, y + 90 + len(works) * 66)), chans, works)
    elif ch == 1:
        y = card_record(d, (rx0, y, rx1, y + 90 + 26 + 4 * 66), chans, list(WORK.keys()), matched=True) + 16
        if sec >= HAND_AT: card_hand(d, (rx0, y, rx1, y + 130))
    else:
        n = min(4, 1 + int((sec - MORNING_AT) / 1.2))
        y = card_morning(d, (rx0, y, rx1, y + 44 + 4 * 56 + 8), n) + 16
        card_hand(d, (rx0, y, rx1, y + 130))
    # end card
    if sec >= END_AT:
        a = min(1.0, (sec - END_AT) / 0.6)
        ov = Image.new("RGB", (W, H), INK); im = Image.blend(im, ov, a * 0.92); d = ImageDraw.Draw(im)
        fh = font(34 if not VERT else 30, True); fs = font(22); fc = font(18, True)
        for k, (txt, fnt, col) in enumerate([(END_H, fh, CARD), (END_S, fs, (200, 206, 212)), (END_CTA, fc, (120, 200, 200))]):
            for q, l in enumerate(wrap(d, txt, fnt, W - 160)):
                d.text(((W - d.textlength(l, font=fnt)) / 2, H / 2 - 70 + k * 64 + q * 36), l, font=fnt, fill=col)
        d.text(((W - d.textlength(HONEST, font=font(13))) / 2, H - 60), HONEST, font=font(13), fill=(150, 156, 162))
    else:
        d.text((40, H - 34), HONEST, font=font(12), fill=MUTE)
        pb = (W - 80) * sec / TOTAL
        d.line((40, H - 44, W - 40, H - 44), fill=LINE, width=3); d.line((40, H - 44, 40 + pb, H - 44), fill=TEAL, width=3)
    return im


def main():
    out_dir = "assets/video"; os.makedirs(out_dir, exist_ok=True)
    name = "demo-%s%s" % (LANG, "-vertical" if VERT else "")
    tmp = os.path.join(os.environ.get("TEMP", "."), "srvideo-" + name)
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    n = int(TOTAL * FPS)
    for k in range(n):
        frame(k / FPS).save(os.path.join(tmp, "%05d.png" % k), compress_level=1)
        if k % 240 == 0: print("  frame %d/%d" % (k, n))
    frame(9.0).convert("RGB").save(os.path.join(out_dir, name + ".jpg"), quality=82)
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    # audio: ring + each line delayed to its slot
    ins = ["-f", "lavfi", "-t", "%.2f" % RING, "-i", "sine=f=440:b=2"]
    fc = ["[1]volume=0.18[r]"]; labels = ["[r]"]  # 입력 0 은 PNG 연속, 1 은 벨소리, 2부터 음성
    for i, (s, e, kind, idx) in enumerate([ev for ev in events if ev[2] == "line"]):
        ins += ["-i", AUDIO_DIR + MAN[idx]["file"]]
        ms = int(s * 1000); fc.append("[%d]adelay=%d|%d[a%d]" % (i + 2, ms, ms, i)); labels.append("[a%d]" % i)
    fc.append("".join(labels) + "amix=inputs=%d:normalize=0:dropout_transition=0,apad=whole_dur=%.2f[out]" % (len(labels), TOTAL))
    cmd = [ff, "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%05d.png")] + ins + [
        "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[out]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", "-t", "%.2f" % TOTAL, os.path.join(out_dir, name + ".mp4")]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
    shutil.rmtree(tmp, ignore_errors=True)
    print("wrote", os.path.join(out_dir, name + ".mp4"), "%.1fs" % TOTAL, os.path.getsize(os.path.join(out_dir, name + ".mp4")) // 1024, "KB")


if __name__ == "__main__":
    main()
