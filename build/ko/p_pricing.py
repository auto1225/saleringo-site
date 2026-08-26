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
    background:rgba(255,255,255,.03);display:flex;flex-direction:column;}
  .kplan.best{border-color:var(--teal);background:rgba(23,189,189,.06);}
  .kplan .nm{font-size:var(--fs-sm);letter-spacing:.12em;text-transform:uppercase;
    color:var(--tx2);}
  .kplan .pr{margin-top:12px;font-family:'Space Grotesk','Noto Sans KR',sans-serif;
    font-size:var(--fs-h2s);font-weight:600;color:#fff;letter-spacing:-.03em;}
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
  .cmp th{color:#fff;font-weight:600;}
  .cmp td{color:var(--tx2);}
  .cmp td b{color:#fff;}
  .cmpwrap{overflow-x:auto;}
  @media (max-width:700px){.cmp{min-width:620px;}}
  .qa{margin-top:34px;display:grid;gap:0;}
  .qa .q{padding:22px 0;border-top:1px solid #E3E7EE;}
  .qa .q b{display:block;font-size:var(--fs-lead);color:var(--l-ink);}
  .qa .q p{margin-top:9px;font-size:var(--fs-sm);color:var(--l-tx2);line-height:1.8;}
  .ratebox{margin-top:32px;padding:26px 24px;border:1px solid var(--hair-d);
    border-radius:12px;display:grid;gap:14px;}
  .ratebox div{display:flex;justify-content:space-between;gap:20px;
    font-size:var(--fs-sm);color:var(--tx2);flex-wrap:wrap;}
  .ratebox div b{color:#fff;}
  .ratebox div span{color:var(--teal);font-weight:700;white-space:nowrap;}
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
          <li>상담 기록 내려받기</li>
        </ul>
        <a class="btn btn-ghostd go" href="./get-started.html">이 요금제로 시작</a>
      </div>
      <div class="kplan best">
        <span class="nm">Grow</span>
        <span class="pr">340,000원<i>/월</i></span>
        <span class="vat">부가세 별도 &middot; 약정 없음</span>
        <ul>
          <li>Start의 모든 기능</li>
          <li>카카오톡 채널 응대</li>
          <li>요금표 기반 견적 발송</li>
          <li>예약 확인과 노쇼 방지 안내</li>
          <li>월 2,000건 대화</li>
        </ul>
        <a class="btn btn-teal go" href="./get-started.html">이 요금제로 시작<span class="cir">&#8599;</span></a>
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
        </ul>
        <a class="btn btn-ghostd go" href="./get-started.html">이 요금제로 시작</a>
      </div>
    </div>
    <div class="ratebox reveal" id="rates">
      <div><b>AI 전화 &mdash; 통화 요금</b><span>1분당 190원부터</span></div>
      <div><b>카카오톡 알림톡 &mdash; 발송 건당</b><span>건당 15원부터</span></div>
      <div><b>추가 대화 &mdash; 한도 초과분</b><span>100건당 9,000원</span></div>
      <div><b>도입 지원과 초기 설정</b><span>무료</span></div>
    </div>
    <p class="seccap reveal" style="margin-top:18px;">통화 요금은 발신 지역과 회선에 따라 달라지므로,
      계약 전에 그 회선과 지역으로 계산한 금액을 문서로 먼저 드립니다. 추정치로 시작해서 나중에
      바뀌는 방식으로는 청구하지 않습니다.</p>
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
    <h2 class="h2 reveal">받지 않는 돈을 적어 둡니다.</h2>
    <ul class="kolist reveal" style="color:var(--l-tx2);">
      <li><b>초기 구축비 없음.</b> 요금표와 영업시간을 넣는 작업은 저희가 합니다.</li>
      <li><b>약정 없음.</b> 해지 위약금이 없습니다. 다음 달부터 청구가 멈춥니다.</li>
      <li><b>계정당 과금 없음.</b> 직원이 늘어도 요금은 그대로입니다.</li>
      <li><b>데이터 반출 비용 없음.</b> 나가실 때 전부 내려받고 나가시면 됩니다.</li>
      <li><b>연동 비용 없음.</b> 캘린더, 문자, 카카오 채널 연동에 따로 청구하지 않습니다.</li>
    </ul>
  </div>
</section>

<section class="t-md sec-light2" id="faq">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>결제와 세금</span><span class="line"></span></div>
    <h2 class="h2 reveal">먼저 물어보시는 것들.</h2>
    <div class="qa reveal">
      <div class="q"><b>세금계산서 발행되나요?</b>
        <p>됩니다. 매월 결제일 기준으로 전자세금계산서를 발행해 드립니다.
          사업자등록번호와 담당자 이메일만 등록해 두시면 자동으로 나갑니다.</p></div>
      <div class="q"><b>결제는 어떻게 하나요?</b>
        <p>신용카드 자동결제와 계좌이체 중에 고르실 수 있습니다.
          계좌이체는 월 단위 후불로, 사용량이 확정된 뒤에 청구합니다.</p></div>
      <div class="q"><b>부가세는 포함인가요?</b>
        <p>아닙니다. 이 페이지의 모든 금액은 부가세 별도입니다.
          실제 청구액은 여기에 10%를 더한 금액입니다.</p></div>
      <div class="q"><b>통화료가 예상보다 많이 나오면요?</b>
        <p>월 사용 한도를 미리 걸어 두실 수 있습니다. 한도에 닿으면 더 쓰지 않고 알림을 보냅니다.
          모르는 사이에 요금이 불어나는 일이 없도록 하려는 것입니다.</p></div>
      <div class="q"><b>쓰던 번호를 그대로 쓸 수 있나요?</b>
        <p>됩니다. 번호는 그대로 두고, 못 받은 전화만 AI로 넘기는 방식이 가장 흔합니다.
          처음부터 AI가 받게 하고 필요할 때만 사람에게 돌리는 방식도 됩니다.</p></div>
      <div class="q"><b>해지하면 데이터는 어떻게 되나요?</b>
        <p>해지 신청과 함께 전체 내보내기를 만들어 드립니다. 고객 정보, 상담 기록, 녹취를 포함합니다.
          내려받으신 뒤 저희 쪽 데이터는 파기합니다. 자세한 보관 기간은
          <a href="./privacy.html">개인정보처리방침</a>에 적어 두었습니다.</p></div>
    </div>
  </div>
</section>

<section class="founding t-xl bg-aurora" id="start">
  <div class="grainlayer grain" aria-hidden="true"></div>
  <div class="wrap">
    <h2 class="h2 onDark reveal">우리 경우에 얼마가 나오는지,<br>계약 전에 문서로 드립니다.</h2>
    <p class="sub reveal" style="max-width:none;">업종과 영업시간, 한 달에 받는 전화가 몇 통인지만 알려 주시면
      예상 통화량과 월 청구액을 계산해 보내 드립니다. 결제 정보는 그때 받지 않습니다.</p>
    <div class="ctas reveal">
      <a class="btn btn-teal" href="./get-started.html">우리 조건으로 견적 받기<span class="cir">&#8599;</span></a>
      <a class="btn btn-ghostd" href="./index.html#how">먼저 작동 방식 보기</a>
    </div>
  </div>
</section>

{FOOT}
</main>

<div class="stickycta"><div class="wrap"><span class="msg">모든 금액 부가세 별도 &middot; 약정 없음.
  <b>우리 기준으로 계산한 금액을 문서로 받아 보세요.</b></span><a class="btn btn-teal" href="./get-started.html">견적 받기<span class="cir">&#8599;</span></a></div></div>
"""

page('pricing.html',
     '요금 &mdash; Saleringo AI 응대 &middot; 월 110,000원부터',
     'Saleringo 요금제와 통화 단가를 전부 공개합니다. 월 110,000원부터, 부가세 별도, 약정 없음, '
     '세금계산서 발행. 직원 채용, 전화대행과 비교한 표도 함께 실었습니다.',
     BODY.format(NAV=NAV, FOOT=FOOT, NB=NB), css=CSS, grade='trust',
     crumbs=[('홈', 'index.html'), ('요금', 'pricing.html')])
print('wrote ko/pricing.html')
