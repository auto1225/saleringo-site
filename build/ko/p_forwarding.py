# -*- coding: utf-8 -*-
"""착신전환 안내 페이지 (한국어·영문).

왜 필요한가.

개통에서 사람 손이 반드시 가는 30초가 있다 — 사장님이 통신사 코드를 눌러
쓰던 번호를 넘기는 일이다. 그 30초를 우리가 대신할 수는 없지만, 통신사마다
다른 코드를 한 화면에 모으고, 설정한 뒤 우리가 확인 전화를 걸어 검증하는
것으로 사람 개입을 없앨 수 있다. 이 페이지는 그 화면이다.

여기 적힌 코드는 통신사가 공개한 일반값이다. 한국 이동통신 3사는 부가서비스
신청 뒤 단말 코드가 요금제·회선 종류에 따라 다르므로, 실제 회선에서 검증한
코드만 적고 나머지는 통신사 안내로 보낸다. 없는 코드를 지어내지 않는다.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import NAV, FOOT, page  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)


CSS = """
  .fwwrap{max-width:760px;margin:0 auto;}
  .fwmodes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:30px;}
  @media (max-width:760px){.fwmodes{grid-template-columns:1fr;}}
  .fwmode{background:#FFFFFF;border:1px solid #E2DDD3;border-radius:14px;padding:18px 20px;}
  .fwmode b{display:block;font-size:var(--fs-sm);font-weight:700;color:#141A1F;}
  .fwmode p{margin:6px 0 0;font-size:var(--fs-xs);line-height:1.7;color:var(--tx2);}
  .fwmode i{display:inline-block;margin-top:10px;font-style:normal;font-size:11px;font-weight:600;
    padding:2px 9px;border-radius:999px;background:rgba(11,120,120,.10);color:#0B7878;}
  .fwlist{margin-top:26px;display:grid;gap:10px;}
  .fwlist details{background:#FFFFFF;border:1px solid #E2DDD3;border-radius:14px;padding:0;overflow:hidden;}
  .fwlist summary{cursor:pointer;list-style:none;padding:16px 20px;font-weight:700;color:#141A1F;
    display:flex;align-items:center;gap:12px;}
  .fwlist summary::-webkit-details-marker{display:none;}
  .fwlist summary::after{content:'+';margin-left:auto;color:#616B75;font-weight:400;font-size:20px;line-height:1;}
  .fwlist details[open] summary::after{content:'\\2013';}
  .fwlist summary small{font-size:var(--fs-xs);font-weight:500;color:#616B75;}
  .fwbody{padding:0 20px 18px;border-top:1px solid #EEEAE2;}
  .fwcodes{display:grid;grid-template-columns:1fr auto;gap:8px 18px;margin:14px 0 0;font-size:var(--fs-sm);}
  .fwcodes dt{color:var(--tx2);}
  .fwcodes dd{margin:0;font-family:var(--mono,ui-monospace,monospace);letter-spacing:.04em;color:#141A1F;
    font-weight:600;text-align:right;white-space:nowrap;}
  .fwcodes dd.tbc{font-family:inherit;font-weight:500;color:#B7791F;letter-spacing:0;white-space:normal;text-align:right;}
  .fwnote{margin:12px 0 0;font-size:var(--fs-xs);line-height:1.75;color:#616B75;}
  .fwverify{margin-top:36px;background:#FFFFFF;border:1px solid #E2DDD3;border-left:3px solid #0B7878;
    border-radius:0 14px 14px 0;padding:18px 22px;}
  .fwverify b{display:block;color:#141A1F;}
  .fwverify p{margin:8px 0 0;font-size:var(--fs-sm);line-height:1.75;color:var(--tx2);}
  .fwverify ol{margin:10px 0 0;padding-left:20px;font-size:var(--fs-sm);color:var(--tx2);}
  .fwverify li{margin:4px 0;}
  .fwwarn{margin-top:26px;font-size:var(--fs-xs);line-height:1.8;color:#616B75;}
  .fwwarn b{color:#141A1F;}
  .fwctas{margin-top:30px;display:flex;flex-wrap:wrap;gap:12px;}
"""


def codes(items):
    """(라벨, 코드 or None) 목록 → dl. None 이면 '통신사 안내에 따릅니다' 로 적는다."""
    out = []
    for label, code in items:
        if code is None:
            out.append("<dt>%s</dt><dd class=\"tbc\">%s</dd>" % (label, TBC))
        else:
            out.append("<dt>%s</dt><dd>%s</dd>" % (label, code))
    return '<dl class="fwcodes">' + "".join(out) + "</dl>"


TBC = ""


def build(lang):
    global TBC
    ko = lang == "ko"

    def t(k, e):
        return k if ko else e

    TBC = t("통신사 안내에 따릅니다 (확인 후 등록)", "Per your carrier's instructions (added once verified)")

    # 통신사별 블록. 코드는 통신사가 공개한 일반값만 적는다.
    carriers = [
        (t("한국 · SKT / KT / LG U+ (휴대전화)", "South Korea · SKT / KT / LG U+ (mobile)"),
         t("부가서비스 신청 뒤 설정", "Enable the add-on first"),
         t("통신사 앱(T world · My KT · U+ 고객센터)이나 고객센터(114)에서 <b>착신전환</b> 부가서비스를 신청한 뒤, "
           "넘길 번호로 배정된 번호를 넣습니다. 단말에서 누르는 코드는 요금제와 회선 종류에 따라 달라서, "
           "저희가 실제 회선에서 확인한 코드만 이 표에 적습니다.",
           "Enable the <b>call forwarding</b> add-on in the carrier app (T world · My KT · U+) or by calling 114, "
           "then enter the number we assigned. Handset codes differ by plan and line type, so this table only "
           "lists codes we have verified on a real line."),
         [(t("무조건 착신", "Unconditional"), None), (t("무응답 시", "No answer"), None),
          (t("통화 중", "Busy"), None), (t("해제", "Deactivate"), None)],
         t("착신전환 통화료는 통신사가 사장님 회선에 청구합니다. 요금은 통신사 약관을 따릅니다.",
           "Forwarded minutes are billed to your line by the carrier under its own tariff.")),
        (t("한국 · 유선전화 (KT · SK브로드밴드 · LG U+)", "South Korea · landline (KT · SK Broadband · LG U+)"),
         t("고객센터 신청", "Request through the carrier"),
         t("지역번호(02·031…) 회선은 고객센터(100·106·101)나 통신사 앱에서 착신전환을 신청합니다. "
           "무응답·통화 중 조건은 신청할 때 함께 정합니다.",
           "Area-code lines (02, 031…) are forwarded by request through the carrier's customer centre or app. "
           "No-answer and busy conditions are set at the same time."),
         [(t("무조건 착신", "Unconditional"), None), (t("무응답 시", "No answer"), None), (t("해제", "Deactivate"), None)],
         ""),
        (t("GSM 표준 · 영국 · 유럽 대부분 · 호주 · 싱가포르 · 미국 T-Mobile", "GSM standard · UK · most of Europe · Australia · Singapore · US T-Mobile"),
         t("단말에서 바로", "Dial from the handset"),
         t("아래 코드를 전화 앱에 그대로 누르고 통화 버튼을 누릅니다. <b>번호</b> 자리에 배정된 번호를 국가번호 포함 형태로 넣습니다. "
           "무응답 시간은 20초를 예로 적었고 5초 단위로 바꿀 수 있습니다.",
           "Dial the code exactly as shown and press call. Put the assigned number, with country code, where it says <b>NUMBER</b>. "
           "The no-answer delay is shown as 20 seconds and can be set in 5-second steps."),
         [(t("무조건 착신", "Unconditional"), "**21*" + t("번호", "NUMBER") + "#"),
          (t("무응답 시 (20초)", "No answer (20 s)"), "**61*" + t("번호", "NUMBER") + "**20#"),
          (t("통화 중", "Busy"), "**67*" + t("번호", "NUMBER") + "#"),
          (t("해제 (전부)", "Deactivate (all)"), "##002#")],
         t("확인: *#21# 을 누르면 현재 무조건 착신 상태가 표시됩니다.",
           "Check: dialling *#21# shows the current unconditional-forwarding state.")),
        (t("미국 · Verizon · AT&amp;T (그 밖의 미국 통신사)", "United States · Verizon · AT&amp;T (and most other US carriers)"),
         t("단말에서 바로", "Dial from the handset"),
         t("별표 코드 뒤에 배정된 번호를 붙여 누르고 통화 버튼을 누릅니다. 연결음이나 확인음이 들리면 설정된 것입니다. "
           "무응답·통화 중 조건 코드는 통신사마다 달라 아래에 적지 않았습니다.",
           "Dial the star code followed by the assigned number and press call. A confirmation tone means it is set. "
           "No-answer and busy codes vary by carrier and are not listed here."),
         [(t("무조건 착신", "Unconditional"), "*72 " + t("번호", "NUMBER")),
          (t("해제", "Deactivate"), "*73"),
          (t("무응답 시", "No answer"), None), (t("통화 중", "Busy"), None)],
         ""),
    ]

    blocks = []
    for name, sub, desc, items, note in carriers:
        blocks.append(
            '<details><summary>%s <small>%s</small></summary><div class="fwbody">'
            '<p class="fwnote" style="color:var(--tx2);font-size:var(--fs-sm);">%s</p>%s%s</div></details>'
            % (name, sub, desc, codes(items), ('<p class="fwnote">%s</p>' % note) if note else "")
        )

    body = (
        NAV
        + """
<section class="sec t-xl">
  <div class="wrap fwwrap">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>

    <div class="fwmodes">
      <div class="fwmode"><b>{m1}</b><p>{m1d}</p><i>{m1w}</i></div>
      <div class="fwmode"><b>{m2}</b><p>{m2d}</p><i>{m2w}</i></div>
      <div class="fwmode"><b>{m3}</b><p>{m3d}</p><i>{m3w}</i></div>
    </div>

    <h2 class="h2" style="margin-top:44px;">{h2codes}</h2>
    <p class="lead" style="margin-top:10px;">{codeslead}</p>
    <div class="fwlist">{blocks}</div>

    <div class="fwverify">
      <b>{vh}</b>
      <p>{vp}</p>
      <ol><li>{v1}</li><li>{v2}</li><li>{v3}</li></ol>
      <p>{vnow}</p>
    </div>

    <h2 class="h2" style="margin-top:44px;">{h2off}</h2>
    <p class="lead" style="margin-top:10px;">{offlead}</p>

    <p class="fwwarn">{warn}</p>

    <div class="fwctas">
      <a class="btn btn-teal" href="./order-status.html">{cta1}</a>
      <a class="btn btn-ghostd" href="./get-started.html">{cta2}</a>
    </div>
  </div>
</section>
""".format(
            eyebrow=t("착신 연결", "Forwarding"),
            h1=t("쓰던 번호는 그대로.<br>못 받는 전화만 넘기십시오.", "Keep your number.<br>Forward only the calls you cannot take."),
            lead=t(
                "번호를 바꾸지 않습니다. 통신사의 착신전환으로 문 닫은 시간이나 못 받은 전화만 배정된 번호로 넘기면, "
                "AI가 받아 예약과 고객 카드로 남깁니다. 설정은 사장님이 30초 동안 직접 하시고, 검증은 저희가 확인 전화로 합니다.",
                "You do not change your number. Your carrier forwards the calls you cannot take — after hours or unanswered — "
                "to the number we assigned, and the AI answers, books, and files the record. You spend thirty seconds setting it; "
                "we verify it with a check call.",
            ),
            m1=t("무조건 착신", "Unconditional"), m1d=t("모든 전화를 넘깁니다. 대표번호를 AI가 처음부터 받게 할 때.", "Every call is forwarded. For a line the AI should answer from the first ring."),
            m1w=t("문 닫은 뒤 켜고, 아침에 끄는 방식도 됩니다", "Turn on at close, off in the morning"),
            m2=t("무응답 시", "No answer"), m2d=t("정한 시간(예: 20초) 안에 못 받으면 넘깁니다. 낮에는 사람이, 못 받을 때만 AI가 받습니다.", "Forwards only if nobody answers within a set delay (say 20 seconds). People by day, AI when nobody picks up."),
            m2w=t("가장 흔한 선택", "The most common choice"),
            m3=t("통화 중", "Busy"), m3d=t("통화 중일 때 걸려 온 전화를 넘깁니다. 한 회선으로 운영하는 곳에.", "Forwards calls that arrive while you are on the line. For single-line businesses."),
            m3w=t("무응답과 함께 켜는 경우가 많습니다", "Often enabled together with no-answer"),
            h2codes=t("통신사를 고르십시오", "Pick your carrier"),
            codeslead=t(
                "코드는 통신사가 공개한 일반값입니다. 한국 이동통신은 부가서비스 신청이 먼저이고, 단말 코드는 저희가 실제 회선에서 확인한 것만 적습니다.",
                "Codes are the carriers' published defaults. Korean mobile carriers require the add-on first; we only list handset codes we have verified on a real line.",
            ),
            blocks="".join(blocks),
            vh=t("설정한 뒤 — 확인 전화", "After you set it — the check call"),
            vp=t(
                "착신이 제대로 걸렸는지는 눌러 본 사람은 알 수 없습니다. 그래서 저희가 사장님 번호로 전화를 걸어 AI가 받는지 확인합니다.",
                "You cannot tell from the handset whether forwarding really took. So we call your number and confirm that the AI picks up.",
            ),
            v1=t("개통 체크리스트의 「착신 연결」 단계에서 확인 전화를 요청합니다.", "Request the check call from the “Forwarding connected” step of your go-live checklist."),
            v2=t("저희 회선이 사장님 번호로 전화를 겁니다. 90초 안에 AI가 받으면 통과입니다.", "Our line calls your number. If the AI answers within 90 seconds, it passes."),
            v3=t("통과하면 체크리스트에 시각이 찍히고, 실패하면 이유와 다시 해 볼 순서를 보여 드립니다.", "A pass is time-stamped on the checklist; a failure shows the reason and what to try next."),
            vnow=t(
                "확인 전화 버튼은 개통 화면에 준비 중입니다. 그 전까지는 hello@saleringo.com 으로 「착신 확인 요청」과 주문번호를 보내 주시면 사람이 확인 전화를 겁니다.",
                "The check-call button is being added to the go-live screen. Until then, email hello@saleringo.com with “forwarding check” and your order number and a person will place the call.",
            ),
            h2off=t("해제는 같은 자리에서", "Turning it off, in the same place"),
            offlead=t(
                "해지하거나 잠시 멈출 때는 위 표의 해제 코드를 누르면 전화가 원래대로 사장님 회선으로 옵니다. 저희에게 연락하지 않아도 됩니다. "
                "이것이 사이트 곳곳에 적힌 「착신전환만 풀면 원래대로」의 뜻입니다.",
                "To cancel or pause, dial the deactivate code from the table and calls come back to your line as before. You do not need to reach us. "
                "That is what “turn off forwarding and your phones behave as before” means throughout this site.",
            ),
            warn=t(
                "<b>알아 두실 것.</b> 착신전환된 통화의 요금은 통신사가 사장님 회선에 청구합니다. "
                "배정된 번호는 인터넷전화 번호라 112·119 같은 긴급전화에 제약이 있을 수 있으니 긴급전화는 사장님 회선에서 거십시오. "
                "사장님에게 돌리는 전화와 후속 문자에 어떤 번호가 뜨는지는 개통 화면에서 정합니다.",
                "<b>Good to know.</b> Forwarded minutes are billed to your line by your carrier. "
                "The assigned number is an internet line, so emergency calls (112, 911, 999) may be restricted — place those from your own line. "
                "Which number shows when we transfer a call or send a follow-up text is set on the go-live screen.",
            ),
            cta1=t("내 개통 체크리스트 열기", "Open my go-live checklist"),
            cta2=t("아직 주문 전이라면 — 견적 받기", "Not ordered yet — get my plan"),
        )
        + FOOT
    )

    return page(
        "forwarding.html",
        t("착신전환 안내 &mdash; Saleringo", "Call forwarding guide &mdash; Saleringo"),
        t(
            "쓰던 번호를 바꾸지 않고 못 받는 전화만 AI 번호로 넘기는 방법. 통신사별 코드와 확인 전화 절차.",
            "How to forward only the calls you cannot take to your AI number without changing it: carrier codes and the check call.",
        ),
        body,
        image='https://images.pexels.com/photos/6870321/pexels-photo-6870321.jpeg?auto=compress&amp;cs=tinysrgb&amp;fit=crop&amp;w=1200&amp;h=630',
        css=CSS,
        grade="trust",
        scripts=("site", "balance", "wrap"),
        lang=lang,
        crumbs=[
            (t("홈", "Home"), "index.html"),
            (t("주문 조회", "Order status"), "order-status.html"),
            (t("착신전환 안내", "Call forwarding"), "forwarding.html"),
        ],
    )


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(", ".join(build(l) for l in ("ko", "en")))
