# -*- coding: utf-8 -*-
"""The Korean home page.

Not a translation of the English one. The English home page argues with a
British plumber and an American dental office in mind; this one argues with a
Korean 원장님 and 사장님 in mind, so the money is in 원, the messenger is
KakaoTalk, the numbers are quoted with 부가세 별도 the way every Korean B2B
price is, and the refusal list names the things a Korean clinic is actually
not allowed to say on the phone.

The file name is index.html because ko/index.html must sit opposite
en/index.html for the language switch and the hreflang pair to find it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shell import page, NAV, FOOT

NB = '&nbsp;'
HERO = 'https://images.pexels.com/photos/18441167/pexels-photo-18441167.jpeg'

CSS = """
  .hero{position:relative;overflow:hidden;display:block;padding-bottom:96px;}
  .hero-inner{position:relative;z-index:2;padding-top:150px;}
  .heroband{max-width:780px;}
  .heroprice{margin-top:22px;font-size:var(--fs-sm);color:rgba(255,255,255,.8);}
  .heroprice i{font-style:normal;color:rgba(255,255,255,.55);}
  .heroshelf{position:relative;z-index:2;margin:56px auto 0;max-width:1060px;}
  /* the night conversation: one customer, one evening, in order */
  .nightline{display:grid;gap:16px;padding:26px 24px;}
  .nl{display:grid;grid-template-columns:104px 1fr;gap:16px;align-items:start;}
  .nl .t{font-size:var(--fs-2xs);letter-spacing:.14em;color:rgba(255,255,255,.42);
    text-transform:uppercase;padding-top:9px;}
  .nl .t em{display:block;font-style:normal;color:rgba(255,255,255,.66);
    letter-spacing:.02em;text-transform:none;font-size:var(--fs-xs);}
  .nl .t i{font-style:normal;margin-left:3px;}
  @media (max-width:640px){
    .nl{grid-template-columns:1fr;gap:6px;}
    .nl .t{padding-top:0;}
  }
  .ksum{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:40px;}
  .ksum .stat{padding:24px 22px;border:1px solid var(--hair-d);border-radius:12px;
    background:rgba(255,255,255,.03);}
  .ksum .stat p{margin-top:10px;font-size:var(--fs-sm);color:var(--tx2);line-height:1.75;}
  @media (max-width:840px){.ksum{grid-template-columns:1fr;}}
  .chanrow{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:36px;}
  @media (max-width:880px){.chanrow{grid-template-columns:1fr;}}
  .chan{padding:26px 24px;border:1px solid var(--hair-d);border-radius:12px;}
  .chan b{display:block;font-size:var(--fs-lead);color:#fff;}
  .chan p{margin-top:10px;font-size:var(--fs-sm);color:var(--tx2);line-height:1.75;}
  .chan .pr{display:block;margin-top:16px;font-size:var(--fs-sm);color:var(--teal);font-weight:700;}
  .kolist{margin-top:26px;display:grid;gap:14px;}
  .kolist li{list-style:none;padding-left:26px;position:relative;
    font-size:var(--fs-body);line-height:1.8;color:var(--tx2);}
  .kolist li::before{content:"";position:absolute;left:2px;top:.72em;width:9px;height:9px;
    border-radius:50%;border:1.5px solid var(--teal);}
  .kolist li b{color:var(--l-ink);}
  .sec-dark .kolist li b,.bg-dusk .kolist li b,.bg-aurora .kolist li b{color:#fff;}
  .tradechips{display:flex;flex-wrap:wrap;gap:10px;margin-top:30px;}
  .tradechips a{display:inline-flex;align-items:center;padding:11px 18px;
    border:1px solid #D5DBE4;border-radius:8px;text-decoration:none;
    color:var(--l-ink);font-size:var(--fs-sm);font-weight:500;transition:all .3s var(--ease);}
  .tradechips a:hover{border-color:var(--teal);background:rgba(23,189,189,.08);}
"""

BODY = """
<header class="hero photohero">
  <div class="bgimg" aria-hidden="true">
    <img class="ph" src="{HERO}?auto=compress&amp;cs=tinysrgb&amp;w=1600" alt=""
         width="1900" height="1425" loading="eager" fetchpriority="high" decoding="async"
         srcset="{HERO}?auto=compress&amp;cs=tinysrgb&amp;w=640 640w, {HERO}?auto=compress&amp;cs=tinysrgb&amp;w=1024 1024w, {HERO}?auto=compress&amp;cs=tinysrgb&amp;w=1600 1600w"
         sizes="(max-width:900px) 100vw, 60vw">
  </div>
  <div class="scrim" aria-hidden="true"></div>
  <div class="tint" aria-hidden="true"></div>
  <div class="grainlayer grain" aria-hidden="true"></div>

  {NAV}

  <div class="wrap hero-inner">
    <div class="heroband hero-panel">
      <span class="eyebrow"><i></i>AI 응대 + 업종별{NB}CRM</span>
      <h1>대부분의 AI는 전화를 받습니다.<br><span style="color:var(--teal);">저희는 예약까지 잡습니다.</span></h1>
      <p class="sub">전화와 홈페이지 채팅, 카카오톡을 대신 받고, 상담 내용을 그대로 받아 적어
        예약 시간을 잡고 고객 카드를 만들어 둡니다. 문 닫은 시간에도 그렇습니다.</p>
      <div class="ctas">
        <a class="btn btn-teal" href="#how">3분이면 파악됩니다<span class="cir">&darr;</span></a>
        <a class="btn btn-ghostd" href="./get-started.html">우리 매장 견적 받기</a>
      </div>
      <p class="heroprice"><b>월 110,000원부터.</b> 전화 응대는 월 820,000원부터.
        <i>부가세 별도 &middot; 약정 없음 &middot; 언제든 해지</i></p>
    </div>

    <div class="heroshelf">
      <div class="appwin">
        <div class="bar"><i></i><i></i><i></i>
          <span class="tt">김OO 고객 &mdash; <b>화요일 밤</b></span>
          <span class="illus">예시 &middot; 가상의 상담</span>
          <span class="closed">영업 종료 시간</span></div>
        <div class="body nightline">
          <div class="nl us">
            <span class="t"><em>고객</em>11:42<i>PM</i></span>
            <div class="bub user">크라운 다시 씌우는 것도 하시나요? 비용을 나눠서 낼 수 있는지도 궁금합니다.</div>
          </div>
          <div class="nl sr">
            <span class="t"><em>Saleringo</em>+38<i>초</i></span>
            <div class="bub ai">네, 하고 있습니다. 지르코니아 크라운은 <b>1개 55만원</b>이고,
              <b>3개월 무이자</b>로 나누면 매월 18만 3천원입니다.
              <b>목요일 오전 10시 30분</b>이 비어 있는데 잡아 드릴까요?</div>
          </div>
          <div class="nl us">
            <span class="t"><em>고객</em>11:44<i>PM</i></span>
            <div class="bub user">네, 그때로 부탁드립니다.</div>
          </div>
          <div class="nl sr">
            <span class="t"><em>Saleringo</em>+12<i>초</i></span>
            <div class="bub ai">예약 잡아 두었습니다. 성함과 연락처만 남겨 주시면
              확인 문자 보내 드리겠습니다.</div>
          </div>
        </div>
      </div>
      <p class="seccap" style="margin-top:16px;">위 대화는 실제 고객 사례가 아니라, 치과 요금표와
        안전 지침을 넣었을 때 제품이 어떻게 답하는지 보여 주는 예시입니다. 금액은 이 사이트의
        다른 페이지에 적힌 것과 같은 시장 가격대를 사용했습니다.</p>
    </div>
  </div>
</header>

<main>

<section class="t-xl sec-dark bg-grid" id="cost">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>놓친 전화 한 통의 값</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">전화를 못 받은 것이 아니라,<br>그 손님을 다음 가게에 넘긴 것입니다.</h2>
    <p class="sub reveal" style="max-width:none;">사장님이 시술 중이거나 점심 시간이거나 이미 퇴근한 뒤에
      걸려 온 전화는, 벨이 몇 번 울리다 끊깁니다. 그 손님은 다시 걸지 않습니다.
      검색 결과의 다음 줄에 있는 가게로 겁니다. 그 손실은 어떤 장부에도 적히지 않기 때문에,
      해마다 얼마인지 아무도 모릅니다.</p>
    <div class="ksum reveal">
      <div class="stat"><span class="n">밤 · 점심</span>
        <p>소상공인 문의 전화가 가장 많이 끊기는 두 구간입니다. 사람이 자리에 없는 시간이기 때문입니다.</p></div>
      <div class="stat"><span class="n">30초</span>
        <p>연결이 안 될 때 걸어 온 사람이 기다리는 시간. 그 뒤에는 검색 결과의 다음 가게에 겁니다.</p></div>
      <div class="stat"><span class="n">0원</span>
        <p>놓친 전화가 장부에 남기는 금액. 그래서 이 비용만 유일하게 관리되지 않습니다.</p></div>
    </div>
    <p class="seccap reveal" style="margin-top:18px;">위 숫자는 특정 조사 결과를 인용한 것이 아니라
      업종에 따라 크게 달라지는 값입니다. 우리 가게의 실제 값은
      <a href="./get-started.html" style="color:var(--teal);font-weight:700;">견적 요청</a> 시
      영업시간과 객단가를 알려 주시면 저희가 계산해 드립니다.</p>
  </div>
</section>

<section class="t-xl sec-light bg-paper" id="how">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>작동 방식</span><span class="line"></span></div>
    <h2 class="h2 reveal">세 단계입니다. 그 이상은 없습니다.</h2>
    <div class="steps reveal">
      <div class="step"><span class="num">1</span>
        <div><b>우리 가게의 말을 넣습니다.</b>
          <p>요금표, 시술과 서비스 목록, 영업시간, 그리고 절대 하면 안 되는 말.
            이것이 AI가 아는 전부입니다. 여기에 없는 것은 답하지 않고 사람에게 넘깁니다.</p></div></div>
      <div class="step"><span class="num">2</span>
        <div><b>전화와 채팅을 대신 받습니다.</b>
          <p>쓰던 번호를 그대로 두고 못 받은 전화만 넘길 수도 있고, 처음부터 받게 할 수도 있습니다.
            홈페이지 채팅과 카카오톡도 같은 내용으로 답합니다.</p></div></div>
      <div class="step"><span class="num">3</span>
        <div><b>예약과 고객 카드가 남습니다.</b>
          <p>통화가 끝나면 누가, 왜, 언제 걸었고 무엇을 약속했는지가 업종별 CRM에 기록됩니다.
            녹취와 요약, 그리고 다음에 할 일까지 함께 남습니다.</p></div></div>
    </div>
  </div>
</section>

<section class="t-xl sec-dark bg-spot" id="channels">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>응대하는 세 가지 채널</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">손님은 편한 곳으로 연락합니다.<br>세 곳 모두 같은 내용으로 답합니다.</h2>
    <div class="chanrow reveal">
      <div class="chan"><b>홈페이지 채팅</b>
        <p>가격과 시술 내용을 묻고, 그 자리에서 예약까지 잡습니다. 상담 내용은 그대로 남습니다.</p>
        <span class="pr">월 110,000원부터</span></div>
      <div class="chan"><b>카카오톡 &amp; 메신저</b>
        <p>채널로 온 문의를 사람이 답하는 것과 같은 말투로 받습니다. 읽고 넘어가는 문의가 없어집니다.</p>
        <span class="pr">월 340,000원부터</span></div>
      <div class="chan"><b>AI 전화</b>
        <p>실제 통화입니다. 사람 목소리로 받고, 묻고, 예약을 잡고, 필요하면 사람에게 돌립니다.</p>
        <span class="pr">월 820,000원 + 분당 190원부터</span></div>
    </div>
    <p class="seccap reveal" style="margin-top:22px;">모든 금액은 부가세 별도입니다.
      통화와 메시지는 사용한 만큼 청구됩니다. 저희도 사용한 만큼 원가가 들기 때문입니다.
      <a href="./pricing.html" style="color:var(--teal);font-weight:700;">요금 전체 보기</a></p>
  </div>
</section>

<section class="t-xl sec-light2" id="crm">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>대화가 남긴 것</span><span class="line"></span></div>
    <h2 class="h2 reveal">챗봇을 사는 것이 아닙니다.<br>업종에 맞는 고객 장부를 사는 것입니다.</h2>
    <p class="sub reveal" style="max-width:none;">치과의 예약 단계와 정비소의 입고 단계는 다릅니다.
      부동산의 매물 문의와 학원의 상담 문의도 다릅니다. 그래서 항목과 단계를 업종별로 미리 만들어 두었습니다.
      첫날부터 우리 업종의 말로 적힙니다.</p>
    <ul class="kolist reveal">
      <li><b>고객 카드</b> &mdash; 이름, 연락처, 무엇을 물었는지, 언제 다시 연락하기로 했는지.</li>
      <li><b>예약</b> &mdash; 캘린더에 바로 들어갑니다. 메모를 남기는 것이 아니라 시간을 잡습니다.</li>
      <li><b>견적</b> &mdash; 사장님이 넣은 요금표에서 계산합니다. AI가 지어내지 않습니다.</li>
      <li><b>통화 기록</b> &mdash; 녹취와 요약, 그리고 AI가 무엇을 근거로 그렇게 답했는지.</li>
      <li><b>내보내기</b> &mdash; 언제든 전부 내려받을 수 있습니다. 데이터는 사장님 것입니다.</li>
    </ul>
  </div>
</section>

<section class="t-xl sec-dark bg-grid" id="refuses">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>하지 않는 일</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">지어내지 않습니다.<br>모르면 모른다고 하고 사람에게 넘깁니다.</h2>
    <p class="sub reveal" style="max-width:none;">AI가 잘못 말해서 생기는 손해는 전부 사장님 몫입니다.
      그래서 답할 수 있는 범위를 좁게 정해 두었고, 그 범위 밖은 답하지 못하도록 막아 두었습니다.
      끄고 켜는 기능이 아니라 제품의 기본값입니다.</p>
    <ul class="kolist reveal">
      <li><b>진단하지 않습니다.</b> 증상을 듣고 병명이나 치료 방법을 말하지 않습니다. 내원 안내까지만 합니다.</li>
      <li><b>없는 가격을 말하지 않습니다.</b> 요금표에 없으면 &ldquo;확인 후 연락드리겠습니다&rdquo;로 넘깁니다.</li>
      <li><b>법률과 세무 판단을 하지 않습니다.</b> 상담 예약까지만 잡습니다.</li>
      <li><b>사람인 척하지 않습니다.</b> 물어보면 AI라고 답합니다.</li>
      <li><b>기록을 지우지 않습니다.</b> 무엇을 왜 답했는지가 전부 남고, 내려받을 수 있습니다.</li>
    </ul>
  </div>
</section>

<section class="t-xl sec-dark bg-dusk" id="plans">
  <div class="wrap">
    <div class="planstrip reveal">
      <div class="ps-head"><b>요금</b><span>통화와 메시지는 쓴 만큼 청구됩니다.
        모든 금액은 계약 전에 먼저 보여 드립니다. 부가세 별도입니다.</span></div>
      <ul class="ps-list">
        <li><b>Start</b><span class="ps-p">110,000원<i>/월</i></span><span class="ps-d">홈페이지 채팅, 문의 수신함, 예약. 월 500건 대화.</span></li>
        <li><b>Grow</b><span class="ps-p">340,000원<i>/월</i></span><span class="ps-d">카카오톡, 견적, 자동 안내 추가. 월 2,000건 대화.</span></li>
        <li><b>Scale</b><span class="ps-p">820,000원<i>/월</i></span><span class="ps-d">AI 전화 추가. 통화 1분당 190원부터.</span></li>
      </ul>
      <p class="ps-foot"><a class="linkcta" href="./pricing.html">요금제와 한도 전체 보기{NB}{NB}&rarr;</a><a class="linkcta" href="./pricing.html#alternatives">사람을 쓰는 것, 전화대행을 쓰는 것과 비교{NB}{NB}&rarr;</a></p>
    </div>
  </div>
</section>

<section class="t-xl sec-light bg-paper" id="trades">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>업종</span><span class="line"></span></div>
    <h2 class="h2 reveal">우리 업종에서 밤 11시에 걸려 오는 전화는<br>어떤 전화입니까?</h2>
    <p class="sub reveal" style="max-width:none;">업종마다 다릅니다. 그래서 업종별로 실제 걸려 올 법한 통화를
      그대로 적어 두었습니다. 우리 가게에 오는 그 전화가 맞는지 읽어 보고 판단하시면 됩니다.</p>
    <div class="tradechips reveal">
      <a href="./industries/dental.html">치과</a>
      <a href="./industries/clinics.html">의원 &middot; 피부과</a>
      <a href="./industries/academies.html">학원</a>
      <a href="./industries/salons.html">미용실</a>
      <a href="./industries/veterinary.html">동물병원</a>
      <a href="./industries/auto-repair.html">자동차 정비</a>
      <a href="./industries/real-estate.html">부동산</a>
      <a href="./industries/venues.html">웨딩홀 &middot; 행사장</a>
      <a href="./industries/senior-care.html">요양</a>
      <a href="./industries/fitness.html">헬스장</a>
    </div>
    <p class="ps-foot" style="margin-top:26px;"><a class="linkcta" href="./industries.html">업종 전체 보기{NB}{NB}&rarr;</a></p>
  </div>
</section>

<section class="founding t-xl bg-aurora" id="start">
  <div class="grainlayer grain" aria-hidden="true"></div>
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>시작하기</span><span class="line"></span></div>
    <h2 class="h2 onDark reveal">요금표를 보내 주시면,<br>그 요금표로 답하는 것을 보여 드립니다.</h2>
    <p class="sub reveal" style="max-width:none;">먼저 결제하지 않습니다. 업종과 영업시간, 그리고 가장 자주 받는
      질문 세 개만 알려 주시면, 그것으로 만든 응대를 보내 드립니다. 마음에 들지 않으면 거기서 끝내시면 됩니다.</p>
    <div class="ctas reveal">
      <a class="btn btn-teal" href="./get-started.html">우리 매장 견적 받기<span class="cir">&#8599;</span></a>
      <a class="btn btn-ghostd" href="./pricing.html">먼저 요금부터 보기</a>
    </div>
  </div>
</section>

{FOOT}
</main>

<div class="stickycta"><div class="wrap"><span class="msg">먼저 결제하지 않습니다.
  <b>우리 요금표로 답하는 것을 먼저 보세요.</b></span><a class="btn btn-teal" href="./get-started.html">견적 받기<span class="cir">&#8599;</span></a></div></div>
"""

body = BODY.format(NAV=NAV, FOOT=FOOT, NB=NB, HERO=HERO)
p = page('index.html',
         'Saleringo &mdash; 전화도 받고 예약까지 잡는 AI 응대',
         '전화, 홈페이지 채팅, 카카오톡을 AI가 대신 받고 업종별 CRM에 예약과 고객 카드로 남깁니다. '
         '월 110,000원부터, 약정 없음, 부가세 별도.',
         body, css=CSS, grade='voice',
         image=HERO + '?auto=compress&amp;cs=tinysrgb&amp;fit=crop&amp;w=1200&amp;h=630')
print('wrote', p)
