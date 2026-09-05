# -*- coding: utf-8 -*-
"""주문 조회 페이지를 만든다 (한국어·영문).

왜 필요한가.

주문을 넣으면 성공 화면이 뜨고 주문번호가 나오는데, 새로고침하면
사라졌습니다. 그리고 그 번호를 다시 조회할 곳이 사이트에 없었습니다.
접수 화면을 닫고 나면 (확인 메일은 아직 없습니다) 자기가 무엇을 얼마에
주문했는지 확인할 방법이 아무 데도 없었습니다.

번호만으로는 열리지 않습니다. 접수할 때 쓴 이메일이 함께 맞아야
합니다. 번호를 찍어 보는 것만으로 남의 주문 내용이 열리면 안 됩니다.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import NAV, FOOT, page  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)


CSS = """
  .oswrap{max-width:640px;margin:0 auto;}
  .osform{margin-top:30px;display:grid;gap:18px;}
  .osform .btn{justify-self:start;}
  .osresult{margin-top:34px;}
  .osrow{display:flex;justify-content:space-between;gap:20px;padding:13px 0;
    border-bottom:1px solid var(--line);font-size:var(--fs-sm);}
  .osrow > span{color:var(--tx2);}
  .osrow > b{color:#141A1F;font-weight:600;text-align:right;}
  .osno{font-family:var(--mono,ui-monospace,monospace);letter-spacing:.04em;}
  .ostrack{margin-top:30px;padding:0;}
  .ostrack li{list-style:none;position:relative;padding:0 0 22px 30px;
    border-left:2px solid var(--line);margin-left:6px;}
  .ostrack li:last-child{border-left-color:transparent;padding-bottom:0;}
  .ostrack li::before{content:'';position:absolute;left:-7px;top:3px;width:12px;height:12px;
    border-radius:50%;background:var(--bg);border:2px solid var(--line);}
  .ostrack li.done::before{background:var(--teal);border-color:var(--teal);}
  /* 밟지 않고 지나간 단계 — 체크도 빈 동그라미도 아닌, 흐릿한 선 */
  .ostrack li.skipped{opacity:.45;}
  .ostrack li.skipped::before{background:transparent;border-style:dashed;}
  .ostrack li.now::before{background:var(--teal);border-color:var(--teal);
    box-shadow:0 0 0 5px rgba(11,120,120,.18);}
  .ostrack b{display:block;font-size:var(--fs-sm);font-weight:600;color:var(--tx3);}
  .ostrack li.done b,.ostrack li.now b{color:#141A1F;}
  .ostrack span{display:block;margin-top:4px;font-size:var(--fs-xs);color:var(--tx3);line-height:1.7;}
  .osnote{margin-top:26px;font-size:var(--fs-xs);color:var(--tx3);line-height:1.8;}
  .oshead{margin-bottom:8px;font-size:var(--fs-lead);color:#141A1F;font-weight:600;}
  .ostag{display:inline-block;margin-left:8px;font-style:normal;font-size:11px;font-weight:600;
    padding:2px 8px;border-radius:999px;vertical-align:middle;background:#EEEAE2;color:#616B75;}
  .ostag.done{background:rgba(47,133,90,.12);color:#2F855A;}
  .ostag.running{background:rgba(11,120,120,.12);color:#0B7878;}
  .ostag.needs_customer{background:rgba(183,121,31,.14);color:#B7791F;}
  .ostag.needs_human{background:rgba(180,69,58,.10);color:#B4453A;}
  .osprov.preview li{opacity:.7;}
  .osprov li span a{font-weight:600;}
"""


def build(lang):
    ko = lang == "ko"

    def t(k, e):
        return k if ko else e

    body = (
        NAV
        + """
<section class="sec t-xl">
  <div class="wrap oswrap">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>

    <form class="osform gsform" data-order-lookup novalidate>
      <div class="fld">
        <label for="osNo">{fNo}</label>
        <input id="osNo" name="orderNo" type="text" required autocomplete="off"
               placeholder="SO-20260827-1001" spellcheck="false" maxlength="40">
        <span class="hint">{noHint}</span>
      </div>
      <div class="fld">
        <label for="osEmail">{fEmail}</label>
        <input id="osEmail" name="email" type="email" required autocomplete="email"
               inputmode="email" placeholder="you@company.com" maxlength="200">
        <span class="hint">{emailHint}</span>
      </div>
      <button class="btn btn-teal" type="submit" data-lookup-submit>{cta}</button>
      <p class="sm-note sm-warn" data-lookup-error role="alert" hidden></p>
    </form>

    <div class="osresult" data-lookup-result hidden></div>

    <p class="osnote">{note}</p>
  </div>
</section>
""".format(
            eyebrow=t("주문 조회", "Order status"),
            h1=t("접수한 주문을 다시 열어 보기", "Look up an order you placed"),
            lead=t(
                "주문번호와 접수할 때 쓰신 이메일을 넣으시면, 무엇을 얼마에 접수하셨는지와 "
                "지금 어느 단계인지 보여 드립니다. 접수 화면을 닫으셨어도 여기서 다시 보실 수 있습니다.",
                "Enter the order number and the email you used. You will see what was recorded, "
                "at what price, and where it stands — even after you have closed the "
                "confirmation screen.",
            ),
            fNo=t("주문번호", "Order number"),
            noHint=t(
                "접수 화면에 적힌 SO- 로 시작하는 번호입니다.",
                "The SO- number shown on the confirmation screen.",
            ),
            fEmail=t("접수할 때 쓰신 이메일", "The email you used"),
            emailHint=t(
                "번호만으로는 열리지 않습니다. 번호를 찍어 보는 것만으로 남의 주문이 열리면 안 되기 때문입니다.",
                "The number alone will not open it — otherwise anyone could read someone "
                "else's order by guessing.",
            ),
            cta=t("주문 찾기", "Find my order"),
            note=t(
                "찾지 못하셨으면 hello@saleringo.com 으로 주문번호와 함께 보내 주십시오. 사람이 확인해 드립니다. "
                "이 화면은 접수 내용을 보여 줄 뿐이고, 여기서 결제되는 금액은 없습니다.",
                "If it does not come up, email hello@saleringo.com with the number and a person "
                "will check. This screen only shows what was recorded; nothing is charged here.",
            ),
        )
        + FOOT
    )

    return page(
        "order-status.html",
        t("주문 조회 &mdash; Saleringo", "Order status &mdash; Saleringo"),
        t(
            "접수한 주문번호와 이메일로 주문 내용과 진행 단계를 확인합니다.",
            "Check what was recorded on your order and where it stands, using your order "
            "number and the email you used.",
        ),
        body,
        image='https://images.pexels.com/photos/8422729/pexels-photo-8422729.jpeg?auto=compress&amp;cs=tinysrgb&amp;fit=crop&amp;w=1200&amp;h=630',
        css=CSS,
        grade="trust",
        scripts=("site", "balance", "wrap", "order-status"),
        lang=lang,
        crumbs=[
            (t("홈", "Home"), "index.html"),
            (t("주문 조회", "Order status"), "order-status.html"),
        ],
    )


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(", ".join(build(l) for l in ("ko", "en")))
