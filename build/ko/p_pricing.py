# -*- coding: utf-8 -*-
"""요금 - the Korean pricing page.

Korean small-business buyers read a price sheet differently from the way the
English page assumes. Three things had to change beyond the currency:

  · 부가세 별도 is stated on every number, because a Korean B2B price that
    does not say so is read as including VAT and the invoice then looks like
    a bait.
  · The comparison is not "a receptionist vs an answering service". In Korea
    the honest comparison is 직원 한 명 더 쓰기, 전화대행 서비스, and 그냥
    놓치기, so those are the three columns.
  · 세금계산서 is the first billing question a Korean business asks, so it is
    the first line of the FAQ rather than a footnote.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shell import page, NAV, FOOT

NB = '&nbsp;'

CSS = """
  .hero{display:block;padding:150px 0 70px;}
  .planwall{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:38px;}
  @media (max-width:900px){.planwall{grid-template-columns:1fr;}}
  .kplan{padding:30px 26px;border:1px solid var(--hair-d);border-radius:14px;
    background:rgba(20,26,31,.039);display:flex;flex-direction:column;position:relative;}
  .kplan.best{border-color:var(--teal);background:rgba(11,120,120,.06);}
  .kplan .rec{position:absolute;top:-13px;left:24px;padding:5px 12px;border-radius:999px;
    background:var(--teal);color:#141A1F;font-size:var(--fs-2xs);font-weight:800;letter-spacing:.08em;}
  .kplan .nm{font-size:var(--fs-sm);letter-spacing:.12em;text-transform:uppercase;
    color:var(--tx2);}
  .kplan .pr{margin-top:12px;font-family:'Bricolage Grotesque','IBM Plex Sans KR',sans-serif;
    font-size:var(--fs-h2s);font-weight:600;color:#141A1F;letter-spacing:-.03em;}
  .kplan .pr i{font-style:normal;font-size:var(--fs-sm);font-weight:500;color:var(--tx2);
    margin-left:4px;letter-spacing:0;}
  .kplan .vat{margin-top:6px;font-size:var(--fs-xs);color:var(--tx2);}
  .kplan ul{margin-top:20px;display:grid;gap:11px;flex:1;}
  .kplan li{list-style:none;padding-left:22px;position:relative;font-size:var(--fs-sm);
    line-height:1.7;color:var(--tx2);}
  .kplan li::before{content:"";position:absolute;left:2px;top:.62em;width:7px;height:7px;
    border-radius:50%;background:var(--teal);}
  .kplan .go{margin-top:24px;}
  .cmp{width:100%;margin-top:34px;border-collapse:collapse;}
  .cmp th,.cmp td{padding:16px 14px;text-align:left;font-size:var(--fs-sm);
    border-bottom:1px solid var(--hair-d);vertical-align:top;line-height:1.7;}
  .cmp th{color:#141A1F;font-weight:600;}
  .cmp td{color:var(--tx2);}
  .cmp td b{color:#141A1F;}
  .cmpwrap{overflow-x:auto;}
  @media (max-width:700px){.cmp{min-width:620px;}}
  .qa{margin-top:34px;display:grid;gap:0;}
  .qa .q{padding:22px 0;border-top:1px solid #E3E7EE;}
  .qa .q b{display:block;font-size:var(--fs-lead);color:var(--l-ink);}
  .qa .q p{margin-top:9px;font-size:var(--fs-sm);color:var(--l-tx2);line-height:1.8;}
  .foundbox{margin-top:32px;padding:26px 24px;border:1px solid var(--teal);
    border-radius:8px;background:rgba(11,120,120,.07);}
  .foundbox > b{display:block;font-size:var(--fs-lead);color:#141A1F;}
  .foundbox p{margin-top:12px;font-size:var(--fs-sm);line-height:1.8;color:var(--tx2);}
  .fb-rows{display:flex;flex-wrap:wrap;gap:22px;margin-top:16px;}
  .fb-rows span{font-size:var(--fs-sm);color:var(--tx2);}
  .fb-rows b{color:var(--teal);font-weight:700;font-size:var(--fs-body);}
  .fb-rows s{color:var(--tx3);}
  .fb-fine{font-size:var(--fs-xs);color:var(--tx3);}
  .ratebox{margin-top:32px;padding:26px 24px;border:1px solid var(--hair-d);
    border-radius:8px;display:grid;gap:14px;}
  .ratebox div{display:flex;justify-content:space-between;gap:20px;
    font-size:var(--fs-sm);color:var(--tx2);flex-wrap:wrap;}
  .ratebox div b{color:#141A1F;}
  .ratebox div span{color:var(--teal);font-weight:700;white-space:nowrap;}

  /* ── 이 값에 무엇이 들어 있는가 ───────────────────────────────────
     한국어 페이지는 요금제 카드만 보여 주고 끝났습니다. 값에 CRM 이
     들어 있다는 것, 채널마다 얼마인지, 한도를 넘기면 어떻게 되는지를
     묻지 않고는 아무도 결재를 올리지 않습니다. */
  .kbuy{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:36px;}
  .kbuy > div{padding:26px 24px;border:1px solid var(--hair-d);border-radius:14px;
    background:rgba(20,26,31,.039);}
  .kbuy b{display:block;color:#141A1F;font-size:var(--fs-lead);margin-bottom:10px;}
  .kbuy p{font-size:var(--fs-sm);line-height:1.85;color:var(--tx2);}
  @media (max-width:900px){.kbuy{grid-template-columns:1fr;}}

  .krate{width:100%;border-collapse:collapse;margin-top:30px;font-size:var(--fs-sm);}
  .krate th,.krate td{padding:14px 12px;text-align:left;border-bottom:1px solid var(--hair-d);
    vertical-align:top;}
  .krate th{font-size:var(--fs-xs);letter-spacing:.1em;text-transform:uppercase;
    color:var(--tx3);font-weight:600;}
  .krate td:last-child,.krate th:last-child{text-align:right;white-space:nowrap;}
  .krate b{color:#141A1F;font-weight:600;font-variant-numeric:tabular-nums;}
  .krate span{display:block;margin-top:4px;font-size:var(--fs-xs);color:var(--tx3);
    line-height:1.7;}
  .kratewrap{overflow-x:auto;}

  .kover{margin-top:34px;display:grid;grid-template-columns:repeat(3,1fr);gap:1px;
    background:var(--hair-d);border:1px solid var(--hair-d);border-radius:14px;overflow:hidden;}
  .kover > div{background:rgba(20,26,31,.039);padding:24px 22px;}
  .kover i{display:block;font-style:normal;font-size:var(--fs-2xs);letter-spacing:.16em;
    text-transform:uppercase;color:var(--teal);font-weight:700;margin-bottom:10px;}
  .kover b{display:block;color:#141A1F;font-size:var(--fs-body);margin-bottom:8px;}
  .kover p{font-size:var(--fs-sm);line-height:1.8;color:var(--tx2);}
  @media (max-width:900px){.kover{grid-template-columns:1fr;}}

  .kbill{margin-top:34px;max-width:560px;border:1px solid var(--hair-d);border-radius:14px;
    background:rgba(20,26,31,.039);overflow:hidden;}
  .kbill .bh{padding:18px 22px;border-bottom:1px solid var(--hair-d);
    display:flex;justify-content:space-between;align-items:baseline;gap:14px;}
  .kbill .bh b{color:#141A1F;font-size:var(--fs-body);}
  .kbill .bh span{font-size:var(--fs-xs);color:var(--tx3);}
  .kbill .br{display:flex;justify-content:space-between;gap:16px;padding:12px 22px;
    font-size:var(--fs-sm);color:var(--tx2);}
  .kbill .br em{font-style:normal;font-variant-numeric:tabular-nums;color:#141A1F;}
  .kbill .br.sub{border-top:1px solid var(--hair-d);margin-top:6px;padding-top:14px;}
  .kbill .br.tot{border-top:2px solid var(--hair-d);padding-top:16px;padding-bottom:20px;}
  .kbill .br.tot span{color:#141A1F;font-weight:600;}
  .kbill .br.tot em{color:var(--teal);font-size:var(--fs-lead);font-weight:600;}
  .kbillcap{margin-top:14px;font-size:var(--fs-xs);color:var(--tx3);line-height:1.8;}
"""

BODY = """
<header class="hero nophoto sec-dark bg-aurora">
  <div class="scrim" aria-hidden="true"></div>
  {NAV}
  <div class="wrap hero-inner">
    <span class="eyebrow"><i></i>요금 &middot; 숨긴 것 없이</span>
    <h1 style="margin-top:24px;">월 110,000원부터.<br>청구서를 먼저 읽고 결정하십시오.</h1>
    <p class="sub">챗봇 하나를 사는 것이 아닙니다. 세 채널의 응대와, 그 뒤에 붙는 업종별 CRM을
      함께 쓰는 값입니다. 통화와 메시지는 쓴 만큼 청구됩니다. 저희도 쓴 만큼 원가가 들기 때문입니다.
      모든 금액은 <b>부가세 별도</b>이며, 세금계산서를 발행합니다.</p>
  </div>
</header>

<main>

<section class="t-md sec-dark bg-grid" id="plans">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>요금제</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">세 개뿐입니다.</h2>
    <div class="planwall reveal">
      <div class="kplan">
        <span class="nm">Start</span>
        <span class="pr">110,000원<i>/월</i></span>
        <span class="vat">부가세 별도 &middot; 약정 없음</span>
        <ul>
          <li>홈페이지 채팅 응대</li>
          <li>문의 수신함과 고객 카드</li>
          <li>캘린더 예약 잡기</li>
          <li>월 500건 대화</li>
          <li>지점 1곳</li>
          <li>상담 기록 내려받기</li>
        </ul>
        <a class="btn btn-ghostd go" href="./checkout.html?plan=start">이 요금제로 주문</a>
      </div>
      <div class="kplan best">
        <span class="rec">추천</span>
        <span class="nm">Grow</span>
        <span class="pr">340,000원<i>/월</i></span>
        <span class="vat">부가세 별도 &middot; 약정 없음</span>
        <ul>
          <li>Start의 모든 기능</li>
          <li>카카오톡 채널 응대</li>
          <li>요금표 기반 견적 발송</li>
          <li>예약 확인과 노쇼 방지 안내</li>
          <li>월 2,000건 대화</li>
          <li>지점 3곳까지</li>
        </ul>
        <a class="btn btn-teal go" href="./checkout.html?plan=grow">이 요금제로 주문<span class="cir">&#8599;</span></a>
      </div>
      <div class="kplan">
        <span class="nm">Scale</span>
        <span class="pr">820,000원<i>/월</i></span>
        <span class="vat">부가세 별도 &middot; 통화료 별도</span>
        <ul>
          <li>Grow의 모든 기능</li>
          <li>AI 전화 응대</li>
          <li>통화 1분당 190원부터</li>
          <li>사람에게 돌리기와 야간 전환</li>
          <li>녹취와 요약 보관</li>
          <li>지점 10곳까지</li>
        </ul>
        <a class="btn btn-ghostd go" href="./checkout.html?plan=scale">이 요금제로 주문</a>
      </div>
    </div>
    <div class="foundbox reveal" id="founding">
      <b>창립 고객 할인 &mdash; 이번 회차 5팀, 처음 3개월 50%</b>
      <p>지금 시작하시면 처음 세 달은 위 금액의 절반입니다. 가입 시점에 확정되고,
        그 사이에 요금이 올라도 그 세 달은 그대로입니다. 넉 달째부터 정가입니다.
        주문서에 자동으로 반영되므로 따로 코드를 넣지 않으셔도 됩니다.
        이번 회차는 <b>5팀 한정</b>입니다 &mdash; 저희가 손으로 온보딩할 수 있는 수가
        그만큼이기 때문이고, 마감 시계가 아니라 정원입니다.</p>
      <p class="fb-rows"><span>Start <b>55,000원</b> <s>110,000원</s></span><span>Grow
        <b>170,000원</b> <s>340,000원</s></span><span>Scale <b>410,000원</b>
        <s>820,000원</s></span></p>
      <p class="fb-fine">부가세 별도. 넉 달째부터 각각 110,000 / 340,000 / 820,000원입니다.</p>
    </div>

    <div class="ratebox reveal" id="rates">
      <div><b>AI 전화 &mdash; 통화 요금</b><span>1분당 190원부터</span></div>
      <div><b>카카오톡 알림톡 &mdash; 발송 건당</b><span>건당 15원부터</span></div>
      <div><b>추가 대화 &mdash; 한도 초과분</b><span>100건당 9,000원</span></div>
      <div><b>설치비 &mdash; 셀프서브 설정 기본</b><span>0원</span></div>
    </div>
    <p class="seccap reveal" style="margin-top:18px;">통화 요금은 발신 지역과 회선에 따라 달라집니다.
      그래서 계약 전에 사장님 쪽 회선과 지역으로 계산한 금액을 문서로 먼저 드립니다. 추정치로
      시작해서 나중에 바뀌는 방식으로는 청구하지 않습니다.</p>
  </div>
</section>

<section class="t-md sec-light bg-paper" id="crm">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>이 값에 무엇이 들어 있는가</span><span class="line"></span></div>
    <h2 class="h2 reveal">응대는 현관입니다.<br>값을 치르시는 것은 그 뒤의 건물입니다.</h2>
    <p class="sub reveal">전화를 받아 주는 서비스는 이미 있습니다. 통화가 끝나면 녹취와 메모가
      남고, 그것을 누군가 다시 읽고 옮겨 적어야 합니다. 그 옮겨 적는 일이 실제 업무의 대부분입니다.
      Saleringo 는 그 일을 하지 않아도 되게 만듭니다.</p>

    <div class="kbuy reveal">
      <div>
        <b>대화가 고객 기록이 됩니다</b>
        <p>통화든 채팅이든 카카오톡이든, 끝나면 고객 카드 한 장이 남습니다. 이름, 연락처,
          무엇을 물었는지, 무엇을 약속했는지가 한 곳에 모입니다. 같은 사람이 다음 달에 다시
          연락하면 그 카드에 이어 붙습니다.</p>
      </div>
      <div>
        <b>예약과 견적이 그 자리에서</b>
        <p>비어 있는 시간을 확인하고 잡습니다. 등록해 두신 요금표로 견적을 만들어 보냅니다.
          사람이 나중에 확인해 다시 연락하는 것이 아니라, 통화 중에 끝납니다.</p>
      </div>
      <div>
        <b>다음에 할 일이 누구 것인지</b>
        <p>확인이 필요한 건은 담당자에게 넘어갑니다. 누구에게 언제 넘어갔는지, 처리됐는지가
          남습니다. 「그 건 어떻게 됐지」를 다시 묻지 않아도 됩니다.</p>
      </div>
    </div>

    <p class="seccap reveal" style="margin-top:22px;">이것은 상위 요금제의 기능이 아닙니다.
      <b>Start 110,000원부터</b> 세 요금제 모두에 같은 CRM 이 들어 있습니다. 요금제가
      나뉘는 기준은 CRM 이 아니라 <b>어느 채널로 받는가</b>와 <b>한 달에 몇 건인가</b>입니다.</p>
  </div>
</section>


<section class="t-md sec-dark bg-spot" id="quote-builder">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>내 한 달 만들기</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">우리 가게 숫자를 넣으면,<br>묻기 전에 한 달이 보입니다.</h2>
    <p class="lead onDark reveal" style="margin-top:14px;">위 요금표와 같은 숫자를 <b>사장님 통화량</b> 기준으로 다시 늘어놓은 것입니다.
      추정치는 추정치라고 적혀 있고, 세금과 접수 가능 여부는 이 화면이 아니라 서버가 판정합니다.</p>

    <div class="qbgrid reveal" data-qb>
      <div class="qbcard">
        <p class="lbl">우리 가게 구성</p>
        <div class="qbrow">
          <b>사업장이 있는 나라</b>
          <select data-qb-country aria-label="나라"></select>
        </div>
        <div class="qbrow">
          <b>어느 문을 받게 할까요?</b>
          <div class="qbchan">
            <label><input type="checkbox" checked disabled> 홈페이지 채팅 &mdash; 기본</label>
            <label><input type="checkbox" data-qb-msg> 메신저·알림톡</label>
            <label><input type="checkbox" data-qb-voice> AI 전화</label>
          </div>
          <p class="qbplan" data-qb-plan></p>
        </div>
        <div class="qbrow" data-qb-row-calls hidden>
          <b>한 달 통화 수 &middot; 평균 통화 시간</b>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <input type="number" data-qb-calls value="150" min="0" max="10000" step="10" aria-label="월 통화 수" style="max-width:150px;">
            <select data-qb-mins aria-label="평균 분" style="max-width:150px;">
              <option value="2">약 2분</option><option value="3" selected>약 3분</option><option value="4">약 4분</option>
            </select>
          </div>
        </div>
        <div class="qbrow" data-qb-row-talks hidden>
          <b>한 달 알림톡 발송 수</b>
          <input type="number" data-qb-talks value="300" min="0" max="100000" step="50" aria-label="월 알림톡 수" style="max-width:150px;">
        </div>
      </div>

      <div class="qbcard" data-qb-live>
        <p class="lbl">예상되는 한 달</p>
        <p style="margin-top:12px;" data-qb-sum></p>
        <p class="qbtax" data-qb-tax>세금과 접수 가능 여부는 주문서에서 확인됩니다.</p>
        <ul class="qbinc" data-qb-inc></ul>
        <div class="qbnote" data-qb-note></div>
        <div class="ctas" style="margin-top:18px;">
          <a class="btn btn-teal" href="./checkout.html" data-qb-go>이 구성 그대로 주문서로<span class="cir">&#8599;</span></a>
        </div>
        <p class="qb-split" style="margin-top:10px;">접수하시면 접수번호와 다음 절차를 바로 안내드리고, 결제는 담당자 확인 뒤에 진행됩니다.</p>
      </div>
    </div>
    <noscript><p class="lead onDark">이 계산기는 자바스크립트로 움직입니다 &mdash; 위 요금표의 숫자가 그대로 유효합니다.</p></noscript>
  </div>
</section>

<section class="t-md sec-dark bg-grid" id="channels">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>채널 요금</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">채널은 셋,<br>수신함과 청구서는 하나.</h2>
    <p class="sub reveal">채널마다 다른 도구를 쓰고 채널마다 따로 청구되는 구조가 흔합니다.
      그러면 어디서 얼마가 나가는지 아무도 모릅니다. 여기서는 세 채널이 한 수신함으로 들어오고,
      한 장의 세금계산서로 나갑니다.</p>

    <div class="kratewrap reveal">
      <table class="krate">
        <thead>
          <tr><th>채널</th><th>어느 요금제부터</th><th>월정액 밖에서 더 나가는 것</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><b>홈페이지 채팅</b><span>방문자가 창을 열고 묻습니다. 야간과 주말에 가장 많이 옵니다.</span></td>
            <td>Start 110,000원<span>월 500건 포함</span></td>
            <td><b>없음</b><span>월정액 안에서 끝납니다</span></td>
          </tr>
          <tr>
            <td><b>카카오톡 채널</b><span>이미 채널을 쓰고 계시면 그대로 연결합니다.
              예약 확인과 안내를 알림톡으로 보냅니다.</span></td>
            <td>Grow 340,000원<span>월 2,000건 포함</span></td>
            <td><b>알림톡 건당 15원</b><span>보내신 만큼만. 받는 것은 대화 건수에 들어갑니다</span></td>
          </tr>
          <tr>
            <td><b>AI 전화</b><span>실제로 벨이 울리고 사람 목소리로 받습니다.
              번호는 쓰시던 것을 그대로 두셔도 됩니다.</span></td>
            <td>Scale 820,000원<span>월 6,000건 포함</span></td>
            <td><b>통화 1분당 190원부터</b><span>통신사 회선 요금이라 나라마다 다릅니다</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <p class="seccap reveal" style="margin-top:18px;">모든 금액은 부가세 별도입니다.
      통화료와 알림톡은 <b>쓰신 만큼 다음 달에</b> 정산합니다 &mdash; 미리 사 두는 방식이 아닙니다.
      쓰지 않으신 달에는 월정액만 나갑니다.</p>
  </div>
</section>

<section class="t-md sec-light2" id="bill">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>한 달 청구서</span><span class="line"></span></div>
    <h2 class="h2 reveal">청구서가<br>이렇게 생겼습니다.</h2>
    <p class="sub reveal">요금제 카드만 보면 월정액밖에 모릅니다. 실제로 오는 종이는 이렇습니다
      &mdash; 치과 한 곳이 AI 전화까지 켜고 한 달을 쓴 경우입니다.</p>

    <div class="kbill reveal">
      <div class="bh"><b>전자세금계산서 &middot; 3월분</b><span>공급가액 기준</span></div>
      <div class="br"><span>Scale 월정액</span><em>820,000원</em></div>
      <div class="br"><span>AI 전화 통화료 &middot; 420분 &times; 190원</span><em>79,800원</em></div>
      <div class="br"><span>알림톡 발송 &middot; 310건 &times; 15원</span><em>4,650원</em></div>
      <div class="br"><span>대화 초과 &middot; 0건</span><em>0원</em></div>
      <div class="br sub"><span>공급가액</span><em>904,450원</em></div>
      <div class="br"><span>부가세 10%</span><em>90,445원</em></div>
      <div class="br tot"><span>합계</span><em>994,895원</em></div>
    </div>

    <p class="kbillcap reveal">이 예시에서 월정액 밖으로 나간 것은 84,450원입니다.
      통화를 한 통도 안 받은 달이면 그 줄이 0원이 되고, 청구서는 월정액과 부가세뿐입니다.
      <b>청구서에 처음 등장하는 항목은 없습니다</b> &mdash; 위 세 가지 단가가 이 페이지에 적힌 전부입니다.</p>

    <p class="calccta reveal" style="margin-top:26px;">
      <a class="btn btn-teal" href="#quote-builder">우리 숫자로 계산해 보기<span class="cir">&uarr;</span></a>
      <a class="lnk" href="./checkout.html?plan=scale">이 구성으로 주문서 열기</a>
    </p>
  </div>
</section>

<section class="t-md sec-dark bg-spot" id="over">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>한도를 넘기면</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">넘기기 전에 알려 드리고,<br>넘기지 않게 막아 드릴 수도 있습니다.</h2>
    <p class="sub reveal">포함된 대화 건수를 넘기는 달이 옵니다. 그때 어떻게 되는지를
      청구서를 받고 나서가 아니라 지금 적어 둡니다.</p>

    <div class="kover reveal">
      <div>
        <i>80%</i>
        <b>미리 알려 드립니다</b>
        <p>포함 건수의 80%에 닿으면 담당자 이메일로 알립니다. 이 달에 넘길 것 같은지
          그때 판단하실 수 있습니다.</p>
      </div>
      <div>
        <i>100%</i>
        <b>넘긴 만큼만 붙습니다</b>
        <p>초과분은 <b>건당 90원</b>입니다. 100건이면 9,000원입니다.
          요금제가 저절로 올라가지 않고, 다음 달에 다시 원래대로 돌아옵니다.</p>
      </div>
      <div>
        <i>상한</i>
        <b>아예 막아 두실 수 있습니다</b>
        <p>월 상한을 걸어 두시면 그 지점에서 AI 응대를 멈춥니다. 청구가 늘어나는 대신
          멈추는 쪽입니다. 그래도 <b>들어온 문의는 직원분들께 그대로 보입니다</b> &mdash;
          응대만 멈추고 기록은 계속 남습니다.</p>
      </div>
    </div>

    <p class="seccap reveal" style="margin-top:18px;">「대화 한 건」은 <b>같은 손님이 같은 채널에서
      24시간 안에</b> 주고받은 것 전부입니다. 그 사이에 세 번 되물어도 한 건입니다. 24시간이 지나
      다시 연락하시거나 다른 채널로 옮겨 오시면 그때 새 한 건입니다. 메시지 수로 세지 않습니다.</p>
  </div>
</section>

<section class="t-md sec-dark bg-spot" id="alternatives">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>무엇과 비교하는가</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">지금도 이미 비용을 내고 계십니다.<br>다만 청구서가 오지 않을 뿐입니다.</h2>
    <p class="sub reveal" style="max-width:none;">전화를 받는 방법은 원래 세 가지였습니다.
      각각 얼마가 들고, 각각 무엇을 못 하는지를 같이 놓고 보시는 편이 정확합니다.</p>
    <div class="cmpwrap reveal">
      <table class="cmp">
        <thead><tr><th>방법</th><th>월 비용</th><th>못 하는 것</th></tr></thead>
        <tbody>
          <tr><td><b>그냥 놓치기</b></td><td><b>0원</b></td>
            <td>누가 왜 걸었는지 알 수 없습니다. 다시 걸어 주지도, 예약을 잡지도 못합니다.
              그 손님이 다음 가게에 거는 것을 막을 방법도 없습니다.</td></tr>
          <tr><td><b>직원 한 명 더</b></td><td><b>250만원 이상</b></td>
            <td>야간과 주말, 공휴일은 비어 있습니다. 통화 중에 걸려 온 두 번째 전화는 못 받습니다.
              휴가와 퇴사가 있습니다. 4대 보험과 퇴직금이 따로 붙습니다.</td></tr>
          <tr><td><b>전화대행 서비스</b></td><td><b>30만~80만원</b></td>
            <td>메모를 남길 뿐 캘린더에 예약을 넣지 못합니다. 우리 요금표를 모르니 견적을 못 냅니다.
              시술이나 서비스 내용을 묻는 질문에 답하지 못합니다.</td></tr>
          <tr><td><b>Saleringo</b></td><td><b>11만~82만원</b></td>
            <td>사람이 해야 하는 판단은 하지 않습니다. 진단, 법률 판단, 요금표에 없는 가격은
              답하지 않고 사람에게 넘깁니다. 그것이 설계입니다.</td></tr>
        </tbody>
      </table>
    </div>
    <p class="seccap reveal" style="margin-top:16px;">위 금액은 특정 업체의 견적이 아니라 국내에서 흔히
      제시되는 범위입니다. 직원 인건비는 2026년 최저임금 기준 월급에 4대 보험 사업자 부담분을
      더한 대략치입니다.</p>
  </div>
</section>

<section class="t-md sec-light bg-paper" id="not-paying">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>내지 않아도 되는 비용</span><span class="line"></span></div>
    <h2 class="h2 reveal">받지 않는 돈을<br>먼저 적어 둡니다.</h2>
    <p class="sub reveal">이 업계의 견적서는 아무도 소리 내어 읽지 않는 줄에서 비싸집니다.
      구축비, 계정 수, 연동비, 나갈 때의 반출비 &mdash; 계약서에 서명한 뒤에 알게 되는 것들입니다.
      아래 다섯 가지는 전부 0원이고, 그 사실이 서면 주문서에도 그대로 들어갑니다.</p>
    <ul class="kolist reveal" style="color:var(--l-tx2);">
      <li><b>초기 구축비 0원.</b> 설치비를 받지 않습니다. 설정은 셀프서브가 기본이고, 이번 회차
        5팀은 첫 답변 세트를 저희가 같이 씁니다. 그 이상 &mdash; 지식베이스 전체를 저희가 대신
        구축하는 작업 &mdash; 은 유료 부가 서비스이고, 작업을 시작하기 전에 견적을 먼저 알려 드립니다.</li>
      <li><b>약정 0개월.</b> 해지 위약금이 없습니다. 언제 해지하셔도 다음 달 청구가 멈추고,
        <b>남은 날수는 날짜로 계산해 돌려 드립니다.</b> 첫 결제일부터 14일 안에는 전액 환불입니다.</li>
      <li><b>계정당 과금 0원.</b> Start 2명, Grow 5명, Scale 15명까지
        같은 요금입니다. 직원이 한 명 늘 때마다 값이 오르는 구조가 아닙니다.</li>
      <li><b>연동비 0원.</b> 캘린더, 문자, 카카오톡 채널을 붙이는 데 따로 청구하지 않습니다.
        이미 쓰고 계신 것에 붙이는 것이 기본이고, 그것이 안 되면 그렇다고 먼저 말씀드립니다.</li>
      <li><b>반출비 0원.</b> 나가실 때 고객 기록, 통화 기록, 예약 내역을 전부 파일로 내려받고
        나가십니다. 데이터를 인질로 잡지 않습니다. <b>해지일부터 30일 안에는</b> 언제든 전체를
        반출하실 수 있고, 그 뒤에 저희 보유분을 삭제합니다. 통화 녹음은 백업까지
        <b>90일 안에</b> 파기합니다.</li>
    </ul>
    <p class="seccap reveal" style="margin-top:20px;">청구서에 올라가는 항목은
      <b>월정액 · 통화료 · 알림톡 · 대화 초과</b> 넷뿐입니다. 이 페이지에 단가가 적히지 않은 것은
      청구서에도 없습니다.</p>
  </div>
</section>

<section class="t-md sec-light2" id="faq">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>결제와 세금</span><span class="line"></span></div>
    <h2 class="h2 reveal">카드를 꺼내시기 전에<br>먼저 물어보시는 것들.</h2>
    <p class="sub reveal">「얼마인가」는 위에 다 적혀 있습니다. 여기는 그 뒤에 오는 질문들입니다
      &mdash; 세금계산서, 환불, 결제가 실패하면 어떻게 되는지, 그리고 조용히 응대를 멈추지는
      않는지.</p>
    <div class="qa reveal">
      <div class="q"><b>세금계산서 발행되나요?</b>
        <p>됩니다. 매월 결제일 기준으로 전자세금계산서를 발행해 드립니다. 사업자등록번호와
          받으실 이메일만 등록해 두시면 자동으로 나갑니다. 주문서에서 세금계산서 받으실 이메일을
          따로 지정하실 수 있습니다 &mdash; 담당자와 경리 담당이 다른 경우가 많기 때문입니다.</p></div>

      <div class="q"><b>부가세는 포함인가요?</b>
        <p>아닙니다. 이 페이지의 모든 금액은 <b>부가세 별도</b>입니다. 실제 청구액은 여기에
          10%를 더한 금액입니다. Scale 820,000원이면 청구서에는 902,000원으로 찍힙니다.
          주문서에서 부가세를 포함한 실제 청구액을 먼저 보여 드립니다.</p></div>

      <div class="q"><b>결제는 어떻게 하나요?</b>
        <p>카드 정기결제와 계좌이체 중에 고르십니다. 카드는 매월 같은 날 자동으로 결제되고,
          계좌이체는 사용량이 확정된 뒤 <b>전자세금계산서를 먼저 보내 드리고</b> 받으신 뒤에
          이체하시는 방식입니다. 계좌이체를 고르시면 저희에게 결제 정보를 맡기지 않으셔도 됩니다.</p></div>

      <div class="q"><b>첫 달은 한 달치를 다 내나요?</b>
        <p>아닙니다. 개시일부터 그 달 말일까지 <b>날짜로 나눠</b> 계산합니다. 20일에 시작하시면
          그 달은 열흘치입니다. 개시일이 정해지면 그 날짜로 계산한 확정 금액을 먼저 알려 드리고,
          그 뒤에 청구합니다.</p></div>

      <div class="q"><b>해지하면 남은 기간은요?</b>
        <p><b>첫 결제일부터 14일 안에는 전액 환불</b>합니다. 그 뒤에 해지하시면 월 정액 요금 가운데 <b>해지 신청일부터 그 달 남은 날수만큼 날짜로 계산해 환불</b>합니다. 이미 사용하신 통화료·메시지 요금은 게시된 단가로 차감하며 환불 대상이 아닙니다.</p></div>

      <div class="q"><b>자동으로 갱신되나요?</b>
        <p>카드 정기결제를 고르시면 <b>해지하시기 전까지</b> 매월 같은 날 자동으로 결제됩니다. <b>해지하신 뒤에는 갱신되지 않으며</b>, 이미 결제하신 기간까지는 그대로 이용하실 수 있습니다. 계좌이체를 고르시면 매월 세금계산서를 먼저 보내 드리고 받으신 뒤에 이체하시므로, 자동으로 빠져나가는 금액이 없습니다.</p></div>

      <div class="q"><b>결제가 실패하면 바로 멈추나요?</b>
        <p>아닙니다. 7일 동안 다시 시도하면서 이메일로 알려 드립니다. 그 뒤에도 해결되지 않으면
          7일의 유예 기간이 있고, 그동안에도 응대는 계속됩니다. <b>말없이 고객 응대를 멈추는 일은
          없습니다</b> &mdash; 멈춰야 하는 상황이면 멈추기 전에 먼저 알려 드립니다.</p></div>

      <div class="q"><b>요금이 오르면요?</b>
        <p>시행 30일 전에 알려 드립니다. 인상에 동의하지 않으시면 그 시점에 해지하실 수
          있고, 이미 결제하신 기간에는 인상 전 요금이 적용됩니다. 창립 고객 할인을 받고 계신
          동안에는 그 기간의 금액이 가입 시점에 확정되어 바뀌지 않습니다.</p></div>

      <div class="q"><b>지금 결제하는 건가요?</b>
        <p>아닙니다. 주문서를 보내시는 것은 청약이고, <b>계약은 서면 주문서에 양측이 서명한 때
          성립합니다.</b> 그 전까지는 어떤 금액도 청구되지 않습니다. 접수하시면 담당자가 영업일
          하루 안에 확인 연락을 드리고 서면 주문서를 보내 드립니다.</p></div>
    </div>
    <p class="seccap reveal" style="margin-top:20px;">여기 적힌 환불·갱신 조건과
      <a class="lnk" href="./terms.html#sec-6">이용약관 제5조</a>는 한 원문에서 함께 출력됩니다.
      그래서 두 곳이 다른 말을 할 수 없습니다.</p>
  </div>
</section>

<section class="t-md sec-light bg-paper" id="managed">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>이 페이지 밖의 상품</span><span class="line"></span></div>
    <h2 class="h2 reveal">지점이 많거나<br>도입을 맡기고 싶으시다면.</h2>
    <p class="sub reveal" style="max-width:none;">이 페이지의 요금제는 사장님이 직접 설정하는
      셀프서브 상품입니다. 그것과 별도로, 대화 설계부터 시스템 연동, 시험, 개시까지 저희가 함께
      진행하는 <b>매니지드(관리형) 도입 상품</b>이 있습니다. <b>60일 파일럿</b>과 <b>서면으로 정한
      범위</b>로 진행하고, <b>월 $1,500부터</b>입니다. 별도 상품이라 소재 국가와 관계없이
      <b>미국 달러로 청구</b>되고(<a class="lnk" href="./terms.html#sec-5">약관 제4조</a>의 예외),
      구축비는 견적으로 정합니다. 다른 상품이고 다른 가격이지만 같은 회사입니다. 지점 한 곳을 이번 주에 돌리고 싶으시면 이 페이지에 계시면 되고,
      지점 스무 곳과 구매 절차가 있으시면 그쪽이 맞습니다.</p>
    <p class="calccta reveal" style="margin-top:22px;">
      <a class="lnk" href="https://global.saleringo.com/en/pricing" rel="noopener">관리형 프로그램 보기 &rarr;</a>
    </p>
  </div>
</section>

<section class="founding t-xl bg-aurora" id="start">
  <div class="grainlayer grain" aria-hidden="true"></div>
  <div class="wrap">
    <h2 class="h2 onDark reveal">우리 경우에 얼마가 나오는지,<br>주문 전에 숫자로 보입니다.</h2>
    <p class="sub reveal" style="max-width:none;">위 계산기에 한 달 통화량을 넣으면 예상 청구액이 그 자리에서 나오고,
      그 구성 그대로 주문서로 이어집니다. 먼저 사람과 이야기하고 싶으시면 상담부터 하셔도 됩니다 &mdash;
      결제 정보는 그때 받지 않습니다.</p>
    <div class="ctas reveal">
      <a class="btn btn-teal" href="#quote-builder">내 한 달 계산 &rarr; 주문서<span class="cir">&uarr;</span></a>
      <a class="btn btn-ghostd" href="./get-started.html">먼저 상담</a>
    </div>
  </div>
</section>

{FOOT}
</main>

<div class="stickycta"><div class="wrap"><span class="msg">모든 금액 부가세 별도 &middot; 약정 없음.
  <b>내 한 달을 계산해 그대로 주문서로.</b> <a class="lnk" href="./get-started.html">먼저 상담</a></span><a class="btn btn-teal" href="#quote-builder">내 한 달 계산 &rarr; 주문서<span class="cir">&uarr;</span></a></div></div>
"""

page('pricing.html',
     '요금 &mdash; Saleringo AI 응대 &middot; 월 110,000원부터',
     'Saleringo 요금제와 통화 단가를 전부 공개합니다. 월 110,000원부터, 부가세 별도, 약정 없음, '
     '세금계산서 발행. 직원 채용, 전화대행과 비교한 표도 함께 실었습니다.',
     BODY.format(NAV=NAV, FOOT=FOOT, NB=NB), css=CSS, grade='trust',
     scripts=('site', 'balance', 'panels', 'wrap', 'rail', 'guide', 'quotebuild'),
     crumbs=[('홈', 'index.html'), ('요금', 'pricing.html')])
print('wrote ko/pricing.html')
