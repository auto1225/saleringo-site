# -*- coding: utf-8 -*-
"""시작하기 - the Korean lead form.

Same endpoint, same data-earlyaccess hook, same honeypot handling as the
English form, because the form logic lives in site.js and neither language
should have its own copy of it. What changes is the shape of the questions.
A Korean owner answering "어디로 문의가 들어오나요" picks 카카오톡 before
anything else, and 통화 가능한 시간 is asked in the local working day rather
than in "your local timezone", because both ends of this call are in Korea.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shell import page, NAV, FOOT

NB = '&nbsp;'

CSS = """
  .hero{display:block;padding:150px 0 60px;}
  .gswrap{display:grid;grid-template-columns:1.25fr .75fr;gap:44px;align-items:start;}
  @media (max-width:980px){.gswrap{grid-template-columns:1fr;gap:34px;}}
  .gsaside{padding:28px 26px;border:1px solid var(--hair-d);border-radius:14px;
    background:rgba(20,26,31,.039);position:sticky;top:96px;}
  @media (max-width:980px){.gsaside{position:static;}}
  .gsaside h3{font-size:var(--fs-lead);color:#141A1F;}
  .gsaside ol{margin-top:18px;display:grid;gap:16px;counter-reset:g;}
  .gsaside li{list-style:none;padding-left:34px;position:relative;font-size:var(--fs-sm);
    line-height:1.75;color:var(--tx2);counter-increment:g;}
  .gsaside li::before{content:counter(g);position:absolute;left:0;top:1px;width:22px;height:22px;
    border-radius:50%;border:1px solid var(--teal);color:var(--teal);font-size:12px;
    display:grid;place-items:center;font-weight:700;}
  .gsaside li b{color:#141A1F;display:block;margin-bottom:3px;}
  .gsaside .tel{margin-top:24px;padding-top:20px;border-top:1px solid var(--hair-d);
    font-size:var(--fs-sm);color:var(--tx2);line-height:1.8;}
  .gsaside .tel b{display:block;color:#141A1F;font-size:var(--fs-lead);}
  .gsorder{margin-top:14px;font-size:var(--fs-sm);font-weight:700;}
  /* 개인정보 동의 한 줄. site.css 의 .eaform input 이 모든 input 에 칸 모양
     (테두리·둥근 모서리·width:100%)을 씌우므로 체크박스만 되돌립니다. */
  .gsagree{display:grid;grid-template-columns:22px 1fr;gap:12px;align-items:start;margin-top:4px;}
  .gsagree input{width:20px;height:20px;margin-top:2px;padding:0;border-radius:4px;
    accent-color:var(--teal);cursor:pointer;}
  .gsagree label{font-size:var(--fs-sm);line-height:1.7;color:var(--tx2);cursor:pointer;
    font-weight:500;letter-spacing:0;text-transform:none;}
  .gsagree label a{color:var(--teal);font-weight:700;}
  .gsagree label .opt{color:var(--tx3);font-weight:600;}
"""

BODY = """
<header class="hero nophoto sec-dark bg-aurora">
  <div class="scrim" aria-hidden="true"></div>
  {NAV}
  <div class="wrap hero-inner">
    <span class="eyebrow"><i></i>시작하기</span>
    <h1 style="margin-top:24px;">결제부터 하지 않습니다.<br>우리 요금표로 답하는 것을 먼저 들어 보십시오.</h1>
    <p class="sub">아래 내용을 남겨 주시면, 보내 주신 요금표로 첫 답변세트를 만들고 고객이 자주 묻는
      질문 10개에 AI 가 답하는 녹음을 영업일 기준 하루 안에 보내 드립니다.
      마음에 들지 않으면 거기서 끝내시면 됩니다. 결제 정보는 이 단계에서 받지 않습니다.</p>
  </div>
</header>

<main>

<section class="t-md sec-dark bg-grid" id="form">
  <div class="wrap">
    <div class="gswrap">
      <div class="reveal">
        <h2 class="h2 onDark" style="font-size:var(--fs-h2s);">어떤 곳인지 알려 주세요.</h2>
        <p class="sub" style="max-width:none;">필수는 이메일과 업종, 그리고 개인정보 동의뿐입니다. 나머지는
          있으면 더 정확한 답을 드릴 수 있는 것들입니다.</p>
        <p class="gsorder"><a class="lnk" href="./checkout.html">이미 결정하셨으면 주문서로 &rarr;</a></p>

        <form class="gsform eaform" data-earlyaccess method="post" style="margin-top:24px;">
          <input type="hidden" name="context" value="한국어 시작하기 페이지">
          <input type="hidden" name="locale" value="ko-KR">
          <div class="two">
            <div class="fld">
              <label for="gEmail">이메일</label>
              <input id="gEmail" name="email" type="email" required autocomplete="email"
                     placeholder="name@yourbusiness.co.kr" aria-label="이메일 주소">
            </div>
            <div class="fld">
              <label for="gIndustry">업종</label>
              <select id="gIndustry" name="industry" required>
                <option value="">선택해 주세요&hellip;</option>
                <option>치과</option>
                <option>의원 &middot; 피부과 &middot; 성형외과</option>
                <option>한의원</option>
                <option>학원 &middot; 교습소 &middot; 과외</option>
                <option>미용실 &middot; 바버샵 &middot; 네일</option>
                <option>동물병원</option>
                <option>자동차 정비 &middot; 공업사</option>
                <option>부동산 중개</option>
                <option>웨딩홀 &middot; 행사장 &middot; 스튜디오</option>
                <option>요양원 &middot; 방문요양 &middot; 주간보호</option>
                <option>헬스장 &middot; 필라테스 &middot; 요가</option>
                <option>음식점 &middot; 단체예약</option>
                <option>펜션 &middot; 숙박</option>
                <option>법무 &middot; 세무 &middot; 노무</option>
                <option>그 외</option>
              </select>
            </div>
          </div>
          <div class="two">
            <div class="fld">
              <label for="gBiz">상호 또는 병원 이름 <span class="opt">&mdash; 선택</span></label>
              <input id="gBiz" name="business" type="text" autocomplete="organization"
                     placeholder="홈페이지를 같이 보기 위해 여쭙습니다" aria-label="상호">
            </div>
            <div class="fld">
              <label for="gPhone">연락처 <span class="opt">&mdash; 선택</span></label>
              <input id="gPhone" name="phone" type="tel" autocomplete="tel"
                     placeholder="010-0000-0000" aria-label="연락처">
            </div>
          </div>
          <div class="fld">
            <label for="gSite">홈페이지 또는 요금표 <span class="opt">&mdash; 선택이지만, 저희가 실제로 보고 만드는 자료입니다</span></label>
            <input id="gSite" name="website" type="text"
                   placeholder="yourbusiness.co.kr &mdash; 또는 아래에 요금표를 붙여 넣어 주세요" aria-label="홈페이지 또는 요금표">
          </div>
          <div class="fld">
            <label for="gChannel">지금 문의가 주로 어디로 들어오나요 <span class="opt">&mdash; 선택</span></label>
            <select id="gChannel" name="channel">
              <option value="">선택해 주세요&hellip;</option>
              <option>대부분 전화</option>
              <option>대부분 카카오톡 채널</option>
              <option>대부분 홈페이지 문의나 예약 폼</option>
              <option>네이버 예약 &middot; 플레이스 문의</option>
              <option>전부 다 오는데, 어느 것도 제대로 못 받고 있습니다</option>
            </select>
          </div>

          <div class="fld">
            <label>통화 가능한 시간 <span class="opt">&mdash; 선택, 되는 것 모두</span></label>
            <div class="slots">
              <label class="slotchip"><input type="checkbox" name="slot_morning"><span>평일 오전</span></label>
              <label class="slotchip"><input type="checkbox" name="slot_midday"><span>평일 점심</span></label>
              <label class="slotchip"><input type="checkbox" name="slot_evening"><span>평일 저녁</span></label>
              <label class="slotchip"><input type="checkbox" name="slot_weekend"><span>주말</span></label>
              <label class="slotchip"><input type="checkbox" name="slot_email"><span>전화 말고 이메일로</span></label>
            </div>
            <p class="tzline">저희 팀은 서울에 있습니다. 20분이면 충분합니다.</p>
          </div>

          <div class="fld">
            <label for="gNote">더 알려 주실 것 <span class="opt">&mdash; 선택</span></label>
            <textarea id="gNote" name="note"
              placeholder="한 달에 몇 통이나 놓치는지, 지금까지 무엇을 써 보셨는지, 어떤 조건이면 쓸 만하다고 보실지."
              aria-label="더 알려 주실 것"></textarea>
          </div>

          <div class="gsagree">
            <input id="gAgree" type="checkbox" name="agreePrivacy" required>
            <label for="gAgree"><a href="./privacy.html" target="_blank" rel="noopener">개인정보 처리방침</a>에 따라
              남겨 주신 정보를 답장과 응대 제작에 쓰는 데 동의합니다. <span class="opt">&mdash; 필수</span></label>
          </div>

          <button class="btn btn-teal" type="submit" style="justify-self:start;margin-top:6px;">보내기<span class="cir">&#8599;</span></button>
          <p class="eanote" style="font-size:var(--fs-xs);color:var(--tx3);font-weight:600;line-height:1.7;">
            약정 없음 &middot; 언제든 해지 &middot; 세금계산서 발행 &middot; 남겨 주신 정보를 판매하거나 제3자에게 제공하지 않습니다.
          </p>
        </form>
      </div>

      <aside class="gsaside reveal">
        <h3>보내신 다음에 일어나는 일</h3>
        <ol>
          <li><b>영업일 하루 안에 답장</b>사람이 씁니다. 자동 회신이 아닙니다.</li>
          <li><b>질문 10개 녹음</b>보내 주신 자료로 첫 답변세트를 만들고, 고객이 자주 묻는 질문 10개에 AI 가 답하는 녹음을 드립니다. 각본으로 만든 예시이지 실제 통화가 아닙니다.</li>
          <li><b>20분 통화</b>맞다 싶으면 그때 시작 일정과 금액을 정합니다.</li>
          <li><b>아니면 여기서 끝</b>연락처를 남겨 두지 않습니다. 삭제해 달라고 하시면 삭제합니다.</li>
        </ol>
        <p class="tel"><b>전화가 더 편하시면</b>
          <a data-tel href="tel:+827052770820"><b data-tel-label>+82 70-5277-0820</b></a>
          로 걸어 주십시오. 언제 거셔도 저희 AI 가 먼저 받습니다. 그 통화를 듣고 판단하셔도 됩니다.</p>
      </aside>
    </div>
  </div>
</section>

<section class="t-md sec-light bg-paper" id="ready">
  <div class="wrap">
    <div class="secrule reveal"><span class="eyebrow"><i></i>준비하실 것</span><span class="line"></span></div>
    <h2 class="h2 reveal">세 가지만 있으면 시작됩니다.</h2>
    <ul class="kolist reveal" style="color:var(--l-tx2);">
      <li><b>요금표.</b> 사진이어도 되고 엑셀이어도 되고, 네이버 플레이스에 적어 두신
        것이어도 됩니다. AI 는 여기 적힌 금액만 말합니다 &mdash; 여기 없는 것을 물으면
        지어내는 대신 &ldquo;확인 후 연락드리겠습니다&rdquo;로 멈춥니다.
        그래서 이 자료가 정확할수록 답할 수 있는 범위가 넓어집니다.</li>
      <li><b>영업시간과 휴무일.</b> 언제 사람이 받고 언제 AI 가 받을지를 정하는 기준입니다.
        점심시간처럼 사람이 있어도 못 받는 시간을 따로 적어 주시면 그 시간대도 넘깁니다.
        명절과 임시 휴무는 나중에 화면에서 바꾸실 수 있습니다.</li>
      <li><b>하면 안 되는 말.</b> 업종마다 다르고, 이것이 가장 중요합니다.
        치과라면 진단 비슷한 말, 학원이라면 합격 가능성, 부동산이라면 시세 전망.
        업종별 기본 목록을 저희가 먼저 만들어 드리고, 사장님이 보시고 더하거나
        빼시면 됩니다.</li>
    </ul>

    <div class="trio reveal" style="margin-top:36px;">
      <div><b>하루 안에 무엇이 오는가</b><p>사장님 요금표로 답하는 질문 10개 녹음입니다.
        요금표에 있는 것은 그대로 답하고, 없는 것은 지어내는 대신 멈추는 것까지 같이
        들으실 수 있습니다 &mdash; 막힐 때 어떻게 멈추는지가 더 중요하기 때문입니다.</p></div>
      <div><b>그다음에 결정하십니다</b><p>읽어 보시고 아니다 싶으면 거기서 끝내시면
        됩니다. 결제 정보를 받지 않았으므로 해지하실 것도 없습니다. 보내 드린 자료는
        요청하시면 지웁니다.</p></div>
      <div><b>맞다 싶으면 설정</b><p>요금표와 영업시간을 사장님이 직접 넣으시는
        셀프서브 설정이 기본이고, 이번 회차 창립 고객 5팀은 첫 답변세트를 저희가 같이 씁니다.
        번호 착신전환을 걸면 그때부터 AI 가 받고, 맞지 않으면 착신전환만 풀면 원래대로입니다.</p></div>
    </div>
    <p class="seccap reveal" style="margin-top:20px;">보내 주신 자료는 응대를 만드는 데에만 씁니다.
      다른 고객의 AI를 학습시키는 데 쓰지 않습니다. 취급 방식은
      <a href="./privacy.html">개인정보처리방침</a>과 <a href="./security.html">보안</a> 페이지에
      적어 두었습니다.</p>
  </div>
</section>

{FOOT}
</main>
"""

page('get-started.html',
     '시작하기 &mdash; 우리 요금표로 질문 10개에 답하는 AI 녹음을 먼저 받아 보세요',
     '업종과 요금표만 알려 주시면, 그 요금표로 고객 질문 10개에 답하는 AI 녹음을 영업일 하루 안에 '
     '보내 드립니다. 결제 정보는 받지 않습니다. 약정 없음, 세금계산서 발행.',
     BODY.format(NAV=NAV, FOOT=FOOT, NB=NB), css=CSS, grade='trust',
     crumbs=[('홈', 'index.html'), ('시작하기', 'get-started.html')])
print('wrote ko/get-started.html')
