# -*- coding: utf-8 -*-
"""주문서 - 두 언어.

이 페이지는 지금까지 만든 어느 페이지와도 목적이 다릅니다. 나머지는 읽고
판단하게 만드는 페이지이고, 이건 이미 판단이 끝난 사람이 막히지 않고
빠져나가야 하는 페이지입니다. 그래서 규칙이 반대입니다.

  · 설득하지 않습니다. 마음을 바꾸려는 문장을 여기에 넣으면, 결정하고 온
    사람에게 "다시 생각해 보라"고 말하는 셈입니다.
  · 금액을 숨기지 않습니다. 무엇을 고르든 지금 얼마인지가 늘 보입니다.
    마지막 화면에서 처음 보는 숫자가 나오면 그 자리에서 닫힙니다.
  · 계정을 만들게 하지 않습니다. 비밀번호를 정하는 것은 산 다음에 할 일이지
    사기 전에 할 일이 아닙니다.
  · 단계를 나누지 않습니다. 한 화면 안에 네 덩어리로 두고 전부 보이게
    합니다. 몇 단계가 남았는지 세게 만드는 것이 이탈의 가장 흔한 원인입니다.

한국에서 이 화면이 반드시 담아야 하는 것들도 함께 넣었습니다.
전자상거래법상 결제 전 최종 확인, 필수 동의와 선택 동의의 분리,
정기결제 고지, 청약철회 안내, 그리고 판매자 정보입니다.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.dirname(os.path.dirname(HERE)))
from shell import page, NAV, FOOT
import json

# 「전자상거래법」 제13조가 주문 화면에 요구하는 판매자 정보입니다.
# 값을 지어내지 않습니다. build/company.json 에 채워진 것만 나갑니다.
CO = json.load(io.open('build/company.json', encoding='utf-8'))


def seller_line(lang):
    ko = lang == 'ko'
    L = lambda k: (CO[k][lang] if isinstance(CO.get(k), dict) else CO.get(k, '')) or ''
    bits = [L('name')]
    if L('ceo'):
        bits.append((ko and '대표자 ' or 'Representative ') + L('ceo'))
    if CO.get('bizNo'):
        bits.append((ko and '사업자등록번호 ' or 'Business reg. no. ') + CO['bizNo'])
    if CO.get('mailOrderNo'):
        bits.append((ko and '통신판매업신고 ' or 'Mail-order licence ') + CO['mailOrderNo'])
    if L('address'):
        bits.append(L('address'))
    if L('privacyOfficer'):
        bits.append((ko and '개인정보 보호책임자 ' or 'Data protection officer ') + L('privacyOfficer'))
    bits.append(CO.get('email', ''))
    bits.append(CO.get('phone', ''))
    return ' &middot; '.join(b for b in bits if b)

NB = '&nbsp;'

CSS = """
  .hero{display:block;padding:140px 0 40px;}
  .cowrap{display:grid;grid-template-columns:1fr 372px;gap:44px;align-items:start;}
  @media (max-width:1040px){.cowrap{grid-template-columns:1fr;gap:30px;}}

  .coform .two,.coform > .coblock > .fld{margin-bottom:14px;}
  .coform .two:last-child,.coform > .coblock > .fld:last-child{margin-bottom:0;}
  .coblock{padding-bottom:34px;margin-bottom:34px;border-bottom:1px solid var(--hair-d);}
  .coblock:last-of-type{border-bottom:0;}
  .coblock > h2{font-size:var(--fs-lead);color:#fff;display:flex;align-items:center;gap:12px;}
  .coblock > h2 i{flex:none;width:28px;height:28px;border-radius:50%;border:1px solid var(--teal);
    color:var(--teal);font-style:normal;font-size:14px;font-weight:700;
    display:grid;place-items:center;}
  .coblock > p{margin-top:10px;font-size:var(--fs-sm);line-height:1.8;color:var(--tx2);}

  /* 요금제와 결제수단 - 라디오를 카드로 */
  .picks{display:grid;gap:12px;margin-top:22px;}
  .pick{position:relative;}
  .pick input{position:absolute;opacity:0;width:0;height:0;}
  .pick span.body{display:grid;grid-template-columns:22px 1fr auto;gap:14px;align-items:start;
    padding:20px 22px;border:1px solid var(--hair-d);border-radius:12px;cursor:pointer;
    transition:border-color .2s var(--ease),background .2s var(--ease);}
  .pick input:checked + span.body{border-color:var(--teal);background:rgba(23,189,189,.07);}
  .pick input:focus-visible + span.body{outline:2px solid var(--teal);outline-offset:3px;}
  .pick span.dot{width:20px;height:20px;border-radius:50%;border:1.5px solid var(--hair2);
    margin-top:2px;position:relative;}
  .pick input:checked + span.body span.dot{border-color:var(--teal);}
  .pick input:checked + span.body span.dot::after{content:"";position:absolute;inset:4px;
    border-radius:50%;background:var(--teal);}
  .pick b{display:block;font-size:var(--fs-body);color:#fff;}
  .pick em{display:block;margin-top:6px;font-style:normal;font-size:var(--fs-sm);
    line-height:1.7;color:var(--tx2);}
  .pick .pr{font-size:var(--fs-body);font-weight:700;color:#fff;white-space:nowrap;
    font-family:'Space Grotesk','Noto Sans KR',sans-serif;}
  .pick .pr i{font-style:normal;font-size:var(--fs-xs);color:var(--tx2);font-weight:500;}
  @media (max-width:560px){
    .pick span.body{grid-template-columns:22px 1fr;}
    .pick .pr{grid-column:2;margin-top:10px;}
  }

  .usebox{margin-top:20px;display:grid;gap:14px;}
  .usebox .fld label{text-transform:none;letter-spacing:.01em;font-size:var(--fs-sm);
    font-weight:700;color:var(--tx2);}

  /* 동의 */
  .agrees{margin-top:22px;display:grid;gap:2px;border:1px solid var(--hair-d);
    border-radius:12px;padding:6px 4px;}
  .agree{display:grid;grid-template-columns:22px 1fr;gap:12px;align-items:start;
    padding:13px 16px;border-radius:9px;}
  .agree:hover{background:rgba(255,255,255,.03);}
  .agree input{width:19px;height:19px;margin-top:1px;accent-color:var(--teal);cursor:pointer;}
  .agree label{font-size:var(--fs-sm);line-height:1.7;color:var(--tx2);cursor:pointer;}
  .agree label b{color:#fff;font-weight:700;}
  .agree label a{color:var(--teal);}
  .agree .must{color:var(--teal);font-weight:700;}
  .agree .opt2{color:var(--tx3);font-weight:600;}
  .agree.has-err{background:rgba(226,88,88,.09);}
  /* 손가락으로 누르는 화면에서는 동의 한 줄이 손톱만 합니다. 정비소에서
     기름 묻은 손으로 19px 짜리 네모를 정확히 누르라는 것은 무리입니다.
     줄 전체를 누를 수 있게 하고, 높이를 손가락만큼 키웁니다. */
  @media (max-width:760px){
    .agree{padding:15px 16px;min-height:52px;align-items:center;}
    .agree input{width:24px;height:24px;margin-top:0;}
    .agree label{padding:4px 0;}
    .pick span.body{padding:22px 20px;}
  }

  .errline{display:block;margin-top:7px;font-size:var(--fs-xs);font-weight:600;
    color:#FF9B9B;line-height:1.6;}
  .fld.has-err input,.fld.has-err select{border-color:#E25858;}

  /* 요약 - 늘 붙어 있는다 */
  .sumcard{position:sticky;top:96px;padding:26px 24px;border:1px solid var(--hair-d);
    border-radius:14px;background:rgba(255,255,255,.035);}
  @media (max-width:1040px){.sumcard{position:static;}}
  .sumcard h3{font-size:var(--fs-sm);letter-spacing:.12em;text-transform:uppercase;
    color:var(--tx3);font-weight:800;}
  .sm-plan{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
    margin-top:16px;padding-bottom:16px;border-bottom:1px solid var(--hair-d);}
  .sm-plan b{font-size:var(--fs-lead);color:#fff;}
  .sm-plan span{font-size:var(--fs-sm);color:var(--tx2);}
  .sm-row{display:flex;justify-content:space-between;gap:14px;margin-top:11px;
    font-size:var(--fs-sm);color:var(--tx2);line-height:1.6;}
  .sm-row b{color:#fff;font-weight:600;white-space:nowrap;}
  .sm-row i{font-style:normal;color:var(--tx3);font-size:var(--fs-xs);}
  .sm-total{display:flex;justify-content:space-between;gap:14px;align-items:baseline;
    margin-top:18px;padding-top:16px;border-top:1px solid var(--hair-d);}
  .sm-total span{font-size:var(--fs-sm);font-weight:700;color:#fff;}
  .sm-total b{font-family:'Space Grotesk','Noto Sans KR',sans-serif;font-size:var(--fs-h2s);
    font-weight:600;color:var(--teal);letter-spacing:-.03em;white-space:nowrap;}
  .sm-next{margin-top:14px;padding-top:14px;border-top:1px dashed var(--hair-d);}
  .sm-est{margin-top:18px;padding-top:16px;border-top:1px solid var(--hair-d);}
  .sm-est p{font-size:var(--fs-xs);color:var(--tx3);font-weight:700;line-height:1.6;}
  .sm-est .sm-note{margin-top:10px;font-weight:500;}
  .fldnote{display:block;margin-top:7px;font-size:var(--fs-xs);
    line-height:1.6;color:var(--tx3);font-weight:600;}
  .sm-notnow{margin-top:12px;padding:10px 12px;border-radius:8px;
    background:rgba(23,189,189,.1);font-size:var(--fs-xs);line-height:1.6;
    color:var(--tx2);font-weight:700;}
  .sm-first{margin-top:16px;padding-top:14px;border-top:1px dashed var(--hair-d);}
  .sm-first p{font-size:var(--fs-xs);color:var(--tx3);font-weight:700;line-height:1.6;}
  .sm-first .sm-note{margin-top:6px;font-weight:500;color:var(--tx2);}
  .sm-over{margin-top:14px;padding-top:12px;border-top:1px solid var(--hair-d);
    font-size:var(--fs-xs);line-height:1.7;color:var(--tx3);}
  .sumfoot{margin-top:20px;padding-top:18px;border-top:1px solid var(--hair-d);
    font-size:var(--fs-xs);line-height:1.75;color:var(--tx3);}
  .sumfoot b{color:var(--tx2);}

  .cosubmit{margin-top:30px;display:grid;gap:14px;justify-items:start;}
  .cosubmit .btn{font-size:var(--fs-body);}
  .cofine{font-size:var(--fs-xs);line-height:1.8;color:var(--tx3);font-weight:600;}
  .cofine b{color:var(--tx2);}
  [data-order-error]{margin-top:18px;padding:16px 18px;border:1px solid #E25858;
    border-radius:11px;background:rgba(226,88,88,.09);font-size:var(--fs-sm);
    line-height:1.75;color:#FFC9C9;}

  /* 접수 화면 */
  .ordersent{padding:34px 30px;border:1px solid var(--teal);border-radius:16px;
    background:rgba(23,189,189,.07);outline:none;}
  .ordersent > b{display:block;font-size:var(--fs-h2s);color:#fff;letter-spacing:-.02em;}
  .orderno{display:inline-block;margin-top:16px;padding:9px 16px;border-radius:9px;
    border:1px solid var(--teal);background:rgba(0,0,0,.25);color:var(--teal);
    font-family:'Space Grotesk',monospace;font-size:var(--fs-lead);letter-spacing:.06em;}
  .os-money{margin-top:18px;font-size:var(--fs-body);color:var(--tx2);line-height:1.8;}
  .os-money b{color:#fff;}
  .os-note{margin-top:16px;font-size:var(--fs-sm);line-height:1.85;color:var(--tx2);}
  .os-note b{color:#fff;}
  .os-steps{margin-top:18px;display:grid;gap:11px;counter-reset:os;}
  .os-steps li{list-style:none;padding-left:32px;position:relative;counter-increment:os;
    font-size:var(--fs-sm);line-height:1.75;color:var(--tx2);}
  .os-steps li::before{content:counter(os);position:absolute;left:0;top:0;width:21px;height:21px;
    border-radius:50%;border:1px solid var(--teal);color:var(--teal);font-size:11px;
    font-weight:700;display:grid;place-items:center;}

  /* 모바일에서 금액을 손가락 옆에 붙여 둔다 */
  .paybar{position:fixed;left:0;right:0;bottom:0;z-index:60;display:none;
    padding:13px clamp(16px,4vw,26px);background:rgba(9,17,32,.96);
    backdrop-filter:blur(12px);border-top:1px solid var(--hair-d);
    align-items:center;gap:14px;}
  .paybar .lbl{font-size:var(--fs-xs);color:var(--tx3);font-weight:700;}
  .paybar .amt{font-family:'Space Grotesk','Noto Sans KR',sans-serif;font-size:var(--fs-lead);
    font-weight:600;color:var(--teal);margin-left:auto;white-space:nowrap;}
  @media (max-width:1040px){.paybar{display:flex;}
    main{padding-bottom:78px;}}
"""


def build(lang):
    ko = lang == 'ko'
    t = (lambda k, e: k if ko else e)

    plans = [
        ('start', 'Start', '110,000', t('홈페이지 채팅, 문의 수신함, 예약. 월 500건 대화.',
                                        'Website chat, lead inbox, bookings. 500 conversations.')),
        ('grow', 'Grow', '340,000', t('카카오톡, 견적, 예약 확인 추가. 월 2,000건 대화.',
                                      'Adds messengers, quotes and confirmations. 2,000 conversations.')),
        ('scale', 'Scale', '820,000', t('AI 전화 추가. 통화 1분당 190원부터.',
                                        'Adds AI phone, from 190 KRW a talk minute.')),
    ]
    pickrows = ''.join(
        '<label class="pick"><input type="radio" name="plan" value="%s"%s>'
        '<span class="body"><span class="dot"></span>'
        '<span><b>%s</b><em>%s</em></span>'
        '<span class="pr">%s원<i>%s</i></span></span></label>'
        % (pid, ' checked' if pid == 'grow' else '', nm, desc, price, t('/월', '/mo'))
        for pid, nm, price, desc in plans)

    methods = [
        ('card', t('카드 정기결제', 'Card, charged monthly'),
         t('카드를 한 번 등록해 두면 매월 같은 날 자동으로 결제됩니다. '
           '사용량이 있는 달은 사용량이 확정된 뒤 합산해 청구합니다.',
           'Register a card once; it is charged on the same day each month. '
           'Usage is added once it is final.')),
        ('transfer', t('계좌이체 · 세금계산서 후불', 'Bank transfer against an invoice'),
         t('매월 사용량이 확정되면 전자세금계산서를 먼저 보내 드리고, 받으신 뒤에 이체하시면 됩니다. '
           '결제 정보를 저희에게 맡기지 않아도 됩니다.',
           'We issue the tax invoice first; you transfer after you have it. '
           'No payment details are held by us.')),
    ]
    methodrows = ''.join(
        '<label class="pick"><input type="radio" name="method" value="%s"%s>'
        '<span class="body"><span class="dot"></span>'
        '<span><b>%s</b><em>%s</em></span></span></label>'
        % (mid, ' checked' if mid == 'card' else '', nm, desc)
        for mid, nm, desc in methods)

    body = """
<header class="hero nophoto sec-dark bg-aurora">
  <div class="scrim" aria-hidden="true"></div>
  {NAV}
  <div class="wrap hero-inner">
    <span class="eyebrow"><i></i>{kick}</span>
    <h1 style="margin-top:22px;">{h1}</h1>
    <p class="sub">{sub}</p>
  </div>
</header>

<main>
<section class="t-md sec-dark bg-grid" id="order">
  <div class="wrap">
    <div class="cowrap">

      <form class="coform" data-checkout novalidate>
        <input type="hidden" name="lang" value="{lang}">
        <input type="text" name="company_website_hp" tabindex="-1" autocomplete="off"
               aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;">

        <div class="coblock">
          <h2><i>1</i>{s1}</h2>
          <p>{s1p}</p>
          <div class="picks" role="radiogroup" aria-label="{s1}">{pickrows}</div>
          <div class="usebox">
            <div class="fld" data-voice-row hidden>
              <label for="coVoice">{voiceLbl}</label>
              <input id="coVoice" name="voiceMinutes" type="number" min="0" max="100000" step="10"
                     inputmode="numeric" placeholder="{voicePh}">
            </div>
            <div class="fld">
              <label for="coTalk">{talkLbl}</label>
              <input id="coTalk" name="alimtalk" type="number" min="0" max="100000" step="50"
                     inputmode="numeric" placeholder="{talkPh}">
            </div>
          </div>
        </div>

        <div class="coblock">
          <h2><i>2</i>{s2}</h2>
          <p>{s2p}</p>
          <div class="two" style="margin-top:22px;">
            <div class="fld">
              <label for="coCompany">{fCompany}</label>
              <input id="coCompany" name="company" type="text" required autocomplete="organization">
            </div>
            <div class="fld">
              <label for="coBiz">{fBiz}</label>
              <input id="coBiz" name="bizNo" type="text" required inputmode="numeric"
                     placeholder="000-00-00000" maxlength="12">
            </div>
          </div>
          <div class="two">
            <div class="fld">
              <label for="coCeo">{fCeo} <span class="opt">{optional}</span></label>
              <input id="coCeo" name="ceo" type="text">
            </div>
            <div class="fld">
              <label for="coContact">{fContact}</label>
              <input id="coContact" name="contact" type="text" required autocomplete="name">
            </div>
          </div>
          <div class="two">
            <div class="fld">
              <label for="coEmail">{fEmail}</label>
              <input id="coEmail" name="email" type="email" required autocomplete="email"
                     placeholder="name@company.co.kr">
            </div>
            <div class="fld">
              <label for="coPhone">{fPhone} <span class="opt">{optional}</span></label>
              <input id="coPhone" name="phone" type="tel" autocomplete="tel"
                     placeholder="010-0000-0000" maxlength="13">
            </div>
          </div>
          <div class="fld">
            <label for="coTax">{fTax} <span class="opt">{optional}</span></label>
            <input id="coTax" name="taxEmail" type="email" placeholder="tax@company.co.kr">
            <label class="agree" style="padding-left:0;padding-bottom:0;">
              <input type="checkbox" data-same-email>
              <span style="font-size:var(--fs-xs);color:var(--tx3);font-weight:600;">{sameEmail}</span>
            </label>
            <span class="fldnote">{taxNote}</span>
          </div>
          <div class="fld">
            <label for="coNote">{fNote} <span class="opt">{optional}</span></label>
            <textarea id="coNote" name="note" placeholder="{notePh}"></textarea>
          </div>
        </div>

        <div class="coblock">
          <h2><i>3</i>{s3}</h2>
          <p>{s3p}</p>
          <div class="picks" role="radiogroup" aria-label="{s3}">{methodrows}</div>
        </div>

        <div class="coblock">
          <h2><i>4</i>{s4}</h2>
          <p>{s4p}</p>
          <div class="agrees">
            <div class="agree">
              <input id="agTerms" type="checkbox" name="agreeTerms" required>
              <label for="agTerms"><span class="must">{must}</span>
                <a href="./terms.html" target="_blank" rel="noopener">{lTerms}</a>{agTerms}</label>
            </div>
            <div class="agree">
              <input id="agPrivacy" type="checkbox" name="agreePrivacy" required>
              <label for="agPrivacy"><span class="must">{must}</span>
                <a href="./privacy.html" target="_blank" rel="noopener">{lPrivacy}</a>{agPrivacy}</label>
            </div>
            <div class="agree">
              <input id="agTransfer" type="checkbox" name="agreeTransfer" required>
              <label for="agTransfer"><span class="must">{must}</span>{agTransfer}</label>
            </div>
            <div class="agree" data-recurring-agree>
              <input id="agRec" type="checkbox" name="agreeRecurring" required>
              <label for="agRec"><span class="must">{must}</span>{agRec}</label>
            </div>
            <div class="agree">
              <input id="agMkt" type="checkbox" name="agreeMarketing">
              <label for="agMkt"><span class="opt2">{may}</span>{agMkt}</label>
            </div>
          </div>

          <div class="cosubmit">
            <button class="btn btn-teal" type="submit" data-submit>{cta}<span class="cir">&#8599;</span></button>
            <p class="cofine">{fine}</p>
          </div>
          <div data-order-error hidden></div>
        </div>
      </form>

      <aside class="sumcard" aria-labelledby="sumh">
        <h3 id="sumh">{sumTitle}</h3>
        <div data-summary role="status" aria-live="polite"></div>
        <p class="sumfoot">{sumFoot}</p>
      </aside>

    </div>
  </div>
</section>

<section class="t-sm sec-dark" id="seller">
  <div class="wrap">
    <p style="font-size:var(--fs-xs);line-height:1.9;color:var(--tx3);max-width:none;">{seller}</p>
  </div>
</section>

{FOOT}
</main>

<div class="paybar"><span class="lbl">{barLbl}</span><span class="amt" data-paybar-total>&mdash;</span></div>
"""

    filled = body.format(
        NAV=NAV, FOOT=FOOT, lang=lang, pickrows=pickrows, methodrows=methodrows,
        kick=t('주문', 'Order'),
        h1=t('주문서입니다.<br>2분이면 끝납니다.',
             'The order form.<br>Two minutes, no account.'),
        sub=t('계정을 만들지 않아도 됩니다. 아래를 채우시면 접수되고, '
              '영업일 하루 안에 사람이 확인 연락을 드립니다. '
              '<b>이 화면에서 결제되는 금액은 없습니다.</b>',
              'No account needed. Fill this in and it is recorded; a person confirms within one '
              'business day. <b>Nothing is charged on this screen.</b>'),
        s1=t('무엇을 쓰실지', 'What you are taking'),
        s1p=t('나중에 바꾸실 수 있습니다. 요금제는 매달 올리거나 내릴 수 있고, 위약금이 없습니다.',
              'You can change this later. Plans move up or down monthly, with no penalty.'),
        voiceLbl=t('한 달 예상 통화 시간 (분)', 'Expected talk minutes a month'),
        voicePh=t('예: 600', 'e.g. 600'),
        talkLbl=t('한 달 예상 알림톡 발송 (건) — 선택', 'Expected notification messages a month — optional'),
        talkPh=t('예: 300', 'e.g. 300'),
        s2=t('세금계산서를 받으실 곳', 'Where the tax invoice goes'),
        s2p=t('사업자등록번호는 입력하시는 대로 확인합니다. 여기서 걸러 두지 않으면 '
              '세금계산서 발행 단계에서 다시 연락드려야 합니다.',
              'The registration number is checked as you type. Catching it here saves a second '
              'round of emails at invoicing.'),
        fCompany=t('상호', 'Company'), fBiz=t('사업자등록번호', 'Business registration no.'),
        fCeo=t('대표자명', 'Representative'), fContact=t('담당자 성명', 'Contact name'),
        fEmail=t('담당자 이메일', 'Contact email'), fPhone=t('연락처', 'Phone'),
        fTax=t('세금계산서 수신 이메일', 'Tax invoice email'),
        taxNote=t('비워 두시면 위 담당자 이메일로 보내 드립니다.',
                  'Left empty, it goes to the contact email above.'),
        sameEmail=t('담당자 이메일과 같습니다', 'Same as the contact email'),
        fNote=t('더 알려 주실 것', 'Anything we should know'),
        notePh=t('업종, 영업시간, 지금 쓰고 계신 예약 프로그램 같은 것을 적어 주시면 '
                 '첫 통화가 훨씬 짧아집니다.',
                 'Your trade, your hours, the booking software you already use — '
                 'it makes the first call much shorter.'),
        optional=t('— 선택', '— optional'),
        s3=t('어떻게 결제하실지', 'How you will pay'),
        s3p=t('둘 다 매월 청구입니다. 약정이 없어서 언제든 멈추실 수 있습니다.',
              'Both are billed monthly. There is no term, so you can stop at any time.'),
        s4=t('확인과 동의', 'Confirm'),
        s4p=t('오른쪽(휴대폰에서는 아래) 금액을 한 번 더 확인해 주십시오. '
              '[필수] 표시가 붙은 항목에 모두 동의하시면 접수됩니다. '
              '카드 정기결제를 고르시면 정기결제 동의가 하나 더 붙습니다.',
              'Check the amount on the right (below, on a phone). '
              'Everything marked [required] has to be ticked. '
              'Choosing card adds one more, for the recurring charge.'),
        must=t('[필수] ', '[required] '), may=t('[선택] ', '[optional] '),
        lTerms=t('이용약관', 'Terms of service'), lPrivacy=t('개인정보처리방침', 'Privacy policy'),
        agTerms=t('에 동의합니다.', ' — I agree.'),
        agPrivacy=t('에 따른 개인정보 수집·이용에 동의합니다. 수집 항목은 상호, 사업자등록번호, '
                    '대표자명, 담당자 성명·이메일·연락처, 세금계산서 수신 이메일, 그리고 남겨 주신 '
                    '메모이며, 계약 이행과 세금계산서 발행에 씁니다.',
                    ' — I agree to the collection of company name, registration number, representative, '
                    'contact name, email and phone, the tax invoice email and any note you leave, '
                    'for performing the contract and issuing invoices.'),
        agTransfer=t('<b>개인정보 국외 이전에 동의합니다.</b> 응대 문장을 만드는 처리가 미국에 있는 '
                     'Anthropic, PBC 에서 이루어집니다. 대화 내용이 이전되며 연락처 등 식별정보는 '
                     '가림 처리 후 전송합니다. 동의하지 않으시면 서비스의 핵심 기능을 쓰실 수 없습니다.',
                     '<b>I agree to the transfer of data outside Korea.</b> Replies are generated by '
                     'Anthropic, PBC in the United States. Conversation content is transferred with '
                     'identifying details masked. Without this the core function cannot run.'),
        agRec=t('<b>정기결제에 동의합니다.</b> 등록한 카드로 매월 같은 날 자동 결제되며, '
                '해지 전까지 계속됩니다. <b>해지는 hello@saleringo.com 으로 한 줄 보내시면 됩니다.</b> '
                '위약금이 없고, 다음 결제일부터 청구가 멈춥니다.',
                '<b>I agree to recurring payment.</b> The card is charged on the same day each month '
                'until cancelled. <b>One line to hello@saleringo.com cancels it.</b> '
                'No penalty, and billing stops from the next cycle.'),
        agMkt=t('제품 소식과 사용 팁을 이메일로 받겠습니다. 안 받으셔도 서비스 이용에 지장이 없습니다.',
                'Send me product notes by email. Declining changes nothing about the service.'),
        cta=t('주문 접수하기', 'Place the order'),
        fine=t('누르시면 위 내용이 저희에게 접수됩니다. <b>결제는 이 단계에서 이루어지지 않습니다.</b> '
               '담당자가 확인한 뒤 결제 안내를 보내 드리고, 그 전까지는 어떤 금액도 청구되지 않습니다. '
               '접수 후에도 이메일 한 통으로 취소하실 수 있습니다.',
               'This records your order with us. <b>No payment is taken at this step.</b> '
               'A person confirms first and sends the payment step; nothing is charged before that. '
               'One email cancels it afterwards.'),
        sumTitle=t('주문 요약', 'Your order'),
        sumFoot=t('요금표의 금액은 <b>부가세 별도</b>이고, 위 합계는 10%를 더한 실제 청구 금액입니다. '
                  '첫 달만 <b>개시일부터 그 달 말일까지 날짜로 나눠</b> 청구하며, 개시일이 정해지면 '
                  '그 날짜로 계산한 확정 금액을 먼저 알려 드립니다. '
                  '통화료와 알림톡은 <b>쓰신 만큼 다음 달에</b> 정산합니다.',
                  'Price-list figures are <b>net of VAT</b>; the total above adds the 10% you actually pay. '
                  'Only the first month is <b>prorated by days</b>, from the start date, and we send '
                  'the exact figure once that date is set. '
                  'Talk time and messages are settled <b>next month on actual use</b>.'),
        barLbl=t('매월 결제 금액', 'Every month'),
        seller=t(seller_line('ko') + '<br>'
                 '<b>청약철회</b> — 접수 후 서비스 개시 전에는 언제든 취소하실 수 있으며 금액이 청구되지 '
                 '않습니다. 개시 후에는 「이용약관」 제5조에 따라 해지 신청일부터 그 달 남은 날수만큼 '
                 '날짜로 계산해 환불합니다. 이미 사용한 통화료 등 사용량 요금은 환불 대상이 아닙니다. '
                 '위약금은 없습니다.',
                 seller_line('en') + '<br>'
                 '<b>Cancellation</b> — before service starts, cancelling costs nothing and no amount '
                 'is charged. After it starts, &sect;3 of the Terms applies: you can cancel any day, the '
                 'first payment is refunded in full within 14 days, and after that the service runs to '
                 'the end of the period you paid for with nothing renewing. Usage already spent is '
                 'deducted at the listed rates. There is no penalty.<br>'
                 'This order is invoiced in Korean won by the entity above, with 10% VAT added.'))

    page('checkout.html',
         t('주문서 &mdash; Saleringo', 'Order &mdash; Saleringo'),
         t('계정 없이 2분이면 끝나는 주문서. 부가세와 첫 달 일할계산까지 금액을 먼저 보여 드리고, '
           '결제는 확인 연락 뒤에 진행합니다.',
           'A two-minute order form, no account. Every figure including VAT and the prorated first '
           'month is shown before you commit; payment comes after a person confirms.'),
         filled, css=CSS, grade='trust',
         scripts=('site', 'balance', 'wrap', 'checkout'), lang=lang,
         crumbs=[(t('홈', 'Home'), 'index.html'), (t('주문', 'Order'), 'checkout.html')])


build('ko')
build('en')
print('ko/checkout.html, en/checkout.html')
