# -*- coding: utf-8 -*-
"""업종별 데모 대본의 형식(schema)과 검사기.

대본 한 편 = 한 업종 × 한 언어. 홈과 모든 업종 페이지의 데모 플레이어(assets/js/demofull.js)가
assets/demo/<slug>.json 을 읽어 그대로 재생한다. 음성은 build/demo_audio.py 가 이 대본에서 만든다.

파일 배치
  build/demo/scripts_<batch>.py  →  SCRIPTS = { '<slug>': { 'ko': {...}, 'en': {...} }, ... }

대본 한 언어의 형식 (전부 필수, 없으면 검사기가 막는다)
  biz        가상의 상호. 실제 업체 이름 금지. 예) '밝은미소치과' / 'Brightside Dental'
  owner      화면에서 사장님을 부르는 말. 예) '원장님' / 'the owner'
  meta       통화 카드 부제. 예) '화요일 11:42 PM · 영업 종료 후 · 가상의 치과'
  callTime   '11:42 PM' 같은 12시간 표기 — 말풍선 시각의 기준
  chan       2장 채널 이름. ko는 '카카오톡', en은 'WhatsApp' (다른 값 금지)
  chapters   [3] 탭 제목.  예) ['밤 11:42, 전화', '다음 날 아침, 카카오톡', '오전 9:00, 사장님 화면']
  chapterSubs[3] 탭 부제.  예) ['깨진 앞니 · 견적 · 목요일 예약', ...]
  sys        {'ring': '벨 울릴 때 한 줄', 'chat': '2장 시작 한 줄', 'morning': '3장 시작 한 줄'}
  customer   {'name': '김지은', 'phone': '010-4482-51··'}  — 전화번호는 반드시 뒷자리를 가린다
  lines      [8~14] 통화 한 줄씩. {'who': 'ai'|'user', 'text': '말 그대로', 'side': [...]}
             · 첫 줄은 ai 인사, 마지막 줄은 ai 끝인사. ai/user 가 번갈아 나온다(같은 쪽 연속 금지).
             · text 는 그대로 음성으로 읽힌다: 기호·괄호·영문 약어 금지, 숫자는 읽는 대로.
             · side 는 이 줄이 말해지는 동안 오른쪽 패널에 나타나는 것들, 순서대로:
               {'field': {'k': '요청', 'v': '앞니 크라운 — 이번 주', 'src': '통화에서'}}
               {'crm': True}                         ← 고객 카드가 켜진다 (이름·전화 받은 뒤 한 번)
               {'work': {'icon': '✓', 'k': '예약 확정', 'v': '목 10:30 · 캘린더에 들어감 · 확인 문자 발송'}}
             · field.src 는 출처: '통화에서' | '사장님 요금표' | '본인 발화' | '발신번호와 일치' | '캘린더의 빈 시간'
               | '본인 발화 · 진단 아님' 같은 짧은 근거. 지어낸 출처 금지.
             · work.icon 은 '✓' '#' '@' '↻' 중 하나.
  chat       [3~5] 다음 날 메시지. {'who': 'user'|'ai', 'when': '7:40 AM'|'+2 sec', 'text': '...',
             'merge': True(첫 ai 답 — 같은 손님으로 이어 붙음), 'handoff': True(마지막 ai 답 — 사람에게 넘김)}
             · 마지막 손님 질문은 반드시 AI가 답하면 안 되는 종류(판단·보장·진단·법적 확정)여야 하고,
               그 답은 handoff=True 로 "담당자가 확인" 으로 넘긴다.
  handoff    [3] 사람에게 넘어갈 때 담당자가 받는 것. 세 번째는 '멈춘 이유: ...' 로 시작.
  morning    [4] 아침 화면. {'icon': '✓'|'#'|'@'|'!', 'k': '새 예약 1건', 'v': '...'}
             · 네 번째는 icon '!' 로 '답변 대기' (handoff 와 같은 건).
  person     {'when': '9:12 AM', 'text': '담당자의 실제 답장 한 줄'}
  summary    끝 문장. '{call}' 자리에 통화 길이가 들어간다.
             예) '통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 사장님이 자는 동안 끝났습니다.'
  honest     정직 문구. 시연·예시 데이터·합성 음성임을 밝힌다. 가격이 '예시 요금표'임을 적는다.
  video      (선택) True 면 '영상으로 보기' 버튼이 보인다. 영상 파일이 있는 업종만.

지켜야 할 것 (이 사이트의 약속)
  · AI 는 요금표에 있는 금액만 말하고, 없는 금액을 지어내지 않는다. 진단·법적 판단·보장·수익 전망을 하지 않는다.
  · 안전이 걸리면(통증 악화·가스 냄새·누수·아이 다침) 예약 대신 즉시 사람에게 돌린다.
  · 사람인 척하지 않는다. 물으면 AI 라고 답한다.
  · 손님이 이름과 전화번호를 말하는 줄이 있어야 카드가 켜진다(crm).
  · ko 와 en 은 같은 이야기여야 한다(같은 손님, 같은 문제, 같은 결과). 번역이 아니라 그 나라 말투로 다시 쓴다.
  · 금액은 ko 는 원화(예: 55만원), en 은 달러. 둘 다 그 업종에서 흔한 범위.
  · 통화 줄 수는 8~14, 총 글자 수(ko 기준)는 500자 안팎. 길수록 음성 파일이 커진다.

검사: python build/demo/validate.py   (모든 scripts_*.py 를 읽어 형식과 규칙을 확인)
"""
import glob
import importlib.util
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))

REQ = ["biz", "owner", "meta", "callTime", "chan", "chapters", "chapterSubs", "sys", "customer",
       "lines", "chat", "handoff", "morning", "person", "summary", "honest"]
SRC_OK_KO = {"통화에서", "사장님 요금표", "본인 발화", "발신번호와 일치", "캘린더의 빈 시간", "본인 발화 · 진단 아님",
             "요금표에 없음 · 확인 후 안내", "재고 현황", "사장님 규칙", "원장님 요금표", "대표님 요금표", "약사님 요금표", "관장님 요금표"}


def load_all():
    out = {}
    for p in sorted(glob.glob(os.path.join(HERE, "scripts_*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(p)[:-3], p)
        m = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(m)
        except Exception as ex:  # 다른 사람이 쓰는 중인 파일은 건너뛴다 — 검사기가 나중에 다시 본다
            print("  !! skip %s: %s" % (os.path.basename(p), str(ex)[:80]))
            continue
        for slug, v in getattr(m, "SCRIPTS", {}).items():
            if slug in out: raise SystemExit("duplicate slug %s in %s" % (slug, p))
            out[slug] = v
    return out


def check_lang(slug, lang, d, errs):
    def e(msg): errs.append("%s/%s: %s" % (slug, lang, msg))
    for k in REQ:
        if k not in d: e("missing " + k)
    if errs and any(x.startswith(slug + "/" + lang + ": missing") for x in errs): return
    if d["chan"] != ("카카오톡" if lang == "ko" else "WhatsApp"): e("chan must be 카카오톡/WhatsApp")
    if len(d["chapters"]) != 3 or len(d["chapterSubs"]) != 3: e("chapters/chapterSubs must have 3")
    for k in ("ring", "chat", "morning"):
        if not d["sys"].get(k): e("sys." + k + " empty")
    c = d["customer"]
    if not c.get("name") or not c.get("phone"): e("customer name/phone")
    if not re.search(r"[·•\*]", c.get("phone", "")): e("customer.phone must mask the tail (use ··)")
    L = d["lines"]
    if not (8 <= len(L) <= 14): e("lines count %d (8~14)" % len(L))
    if L and L[0]["who"] != "ai": e("first line must be ai")
    if L and L[-1]["who"] != "ai": e("last line must be ai")
    for i, ln in enumerate(L):
        if ln.get("who") not in ("ai", "user"): e("line %d who" % i)
        if i and L[i - 1]["who"] == ln["who"]: e("line %d same speaker twice" % i)
        tx = ln.get("text", "")
        if not tx or len(tx) < 4: e("line %d text" % i)
        if re.search(r"[\[\]{}<>|]", tx): e("line %d has markup chars" % i)
        for s in ln.get("side", []):
            if "field" in s:
                f = s["field"]
                if not all(f.get(x) for x in ("k", "v", "src")): e("line %d field incomplete" % i)
            elif "work" in s:
                w = s["work"]
                if w.get("icon") not in ("✓", "#", "@", "↻"): e("line %d work.icon" % i)
                if not (w.get("k") and w.get("v")): e("line %d work k/v" % i)
            elif "crm" not in s: e("line %d side item unknown" % i)
    if sum(1 for ln in L for s in ln.get("side", []) if "crm" in s) != 1: e("exactly one crm side item")
    if sum(1 for ln in L for s in ln.get("side", []) if "field" in s) < 3: e("at least 3 fields")
    if sum(1 for ln in L for s in ln.get("side", []) if "work" in s) < 2: e("at least 2 work items")
    total = sum(len(ln["text"]) for ln in L)
    if lang == "ko" and total > 760: e("ko call text too long (%d chars)" % total)
    if lang == "en" and total > 1500: e("en call text too long (%d chars)" % total)
    C = d["chat"]
    if not (3 <= len(C) <= 5): e("chat count")
    if C and C[0]["who"] != "user": e("chat must start with the customer")
    if not any(m.get("merge") for m in C if m["who"] == "ai"): e("one ai chat needs merge=True")
    if not (C and C[-1]["who"] == "ai" and C[-1].get("handoff")): e("last chat must be ai with handoff=True")
    if len(d["handoff"]) != 3: e("handoff must have 3")
    M = d["morning"]
    if len(M) != 4: e("morning must have 4")
    if M and M[-1].get("icon") != "!": e("4th morning icon must be '!'")
    for m in M:
        if m.get("icon") not in ("✓", "#", "@", "!"): e("morning icon")
    if "{call}" not in d["summary"]: e("summary must contain {call}")
    if not d["person"].get("text"): e("person.text")
    if "video" in d and not isinstance(d["video"], bool): e("video must be bool")


def main():
    S = load_all(); errs = []
    for slug, v in S.items():
        if not re.match(r"^[a-z0-9-]+$", slug): errs.append(slug + ": bad slug")
        for lang in ("ko", "en"):
            if lang not in v: errs.append("%s: missing %s" % (slug, lang)); continue
            check_lang(slug, lang, v[lang], errs)
        if "ko" in v and "en" in v and len(v["ko"]["lines"]) != len(v["en"]["lines"]):
            errs.append("%s: ko/en line count differ (%d vs %d)" % (slug, len(v["ko"]["lines"]), len(v["en"]["lines"])))
    print("scripts:", len(S), "| errors:", len(errs))
    for x in errs[:80]: print("  -", x)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
