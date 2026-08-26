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
  .os-after{margin-top:8px;font-size:var(--fs-sm);color:var(--tx3);line-height:1.7;}


  /* 서버가 판정한 세금 처리와, 화면에서 끝낼 수 없는 이유. */
  .cotax{margin-top:18px;padding:14px 16px;border-radius:10px;
    background:rgba(255,255,255,.04);border:1px solid var(--line);
    font-size:var(--fs-sm);line-height:1.75;color:var(--tx2);}
  .cotax b{display:block;color:#fff;font-weight:600;}
  .cotax-block{display:block;margin-top:8px;padding-left:14px;position:relative;color:var(--tx2);}
  .cotax-block::before{content:'';position:absolute;left:0;top:.62em;width:6px;height:6px;
    border-radius:50%;background:var(--amber, #d8a13a);}
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

    PR = json.load(io.open('assets/data/pricing.json', encoding='utf-8'))
    cur = 'KRW' if ko else 'USD'
    cinfo = PR['currencies'][cur]

    def price(n):
        # 599 는 "$599", 0.14 는 "$0.14". 자리수를 하나로 고정하면 둘 중
        # 하나가 틀립니다. $599.00 은 금액이 아니라 회계 장부처럼 보입니다.
        whole = abs(n - round(n)) < 1e-9
        txt = ('{:,.0f}' if whole else ('{:,.%df}' % cinfo['decimals'])).format(n)
        return (cinfo['symbol'] + txt) if cinfo['position'] == 'before' else (txt + cinfo['symbol'])

    blurbs = {
        'start': t('홈페이지 채팅, 문의 수신함, 예약. 월 500건 대화.',
                   'Website chat, lead inbox, bookings. 500 conversations.'),
        'grow': t('카카오톡, 견적, 예약 확인 추가. 월 2,000건 대화.',
                  'Adds messengers, quotes and confirmations. 2,000 conversations.'),
        # 단가를 여기 적으면 나라가 바뀔 때 통화가 어긋납니다. 정확한 단가는
        # 바로 아래 요약이 고른 나라의 통화로 보여 줍니다.
        'scale': t('AI 전화 추가. 통화료는 쓰신 만큼 다음 달 정산. 월 6,000건 대화.',
                   'Adds AI phone; talk time billed next month on actual use. '
                   '6,000 conversations.'),
    }
    plans = [(pl['id'], pl['name'][lang], price(pl['price'][cur]), blurbs[pl['id']])
             for pl in PR['plans']]

    countries = ''.join(
        '<option value="%s"%s>%s</option>'
        % (c['code'], ' selected' if c['code'] == ('KR' if ko else 'US') else '', c['name'][lang])
        for c in PR['countries'])

    # 구매 주체가 사업자인지 개인인지 공공기관인지에 따라 세금 처리가
    # 완전히 달라집니다. 예전에는 묻지 않고 전부 "세금 0" 으로 처리했습니다.
    buyer_opts = [
        ('business', t('사업자 (법인·개인사업자)', 'A business (company or sole trader)')),
        ('consumer', t('개인', 'An individual')),
        ('public',   t('공공기관·학교', 'A public body or school')),
    ]
    buyerTypes = '<option value="" disabled selected>%s</option>' % t('선택해 주세요', 'Choose one')         + ''.join('<option value="%s">%s</option>' % (v, n) for v, n in buyer_opts)

    # 청구 국가와 실제로 서비스를 쓰는 나라가 다를 수 있습니다.
    serviceCountries = '<option value="">%s</option>' % t('청구 국가와 같습니다', 'Same as billing country')         + ''.join('<option value="%s">%s</option>' % (c['code'], c['name'][lang])
                  for c in PR['countries'] if c['code'] != 'OTHER')

    pickrows = ''.join(
        '<label class="pick"><input type="radio" name="plan" value="%s"%s>'
        '<span class="body"><span class="dot"></span>'
        '<span><b>%s</b><em>%s</em></span>'
        '<span class="pr" data-plan-price="%s">%s<i>%s</i></span></span></label>'
        % (pid, ' checked' if pid == 'grow' else '', nm, desc, pid, ptxt, t('/월', '/mo'))
        for pid, nm, ptxt, desc in plans)

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
          <h2><i>1</i>{s0}</h2>
          <p>{s0p}</p>
          <div class="two" style="margin-top:20px;">
            <div class="fld">
              <label for="coCountry">{fCountry}</label>
              <select id="coCountry" name="country" required autocomplete="country">{countries}</select>
            </div>
            <div class="fld">
              <label for="coBuyer">{fBuyer}</label>
              <select id="coBuyer" name="buyerType" required>{buyerTypes}</select>
              <span class="hint">{buyerHint}</span>
            </div>
          </div>
          <div class="fld" data-service-row hidden>
            <label for="coServiceCountry">{fServiceCountry} <span class="opt">{optional}</span></label>
            <select id="coServiceCountry" name="serviceCountry">{serviceCountries}</select>
            <span class="hint">{serviceHint}</span>
          </div>
          <p class="cotax" data-commerce-verdict hidden></p>
        </div>

        <div class="coblock">
          <h2><i>2</i>{s1}</h2>
          <p>{s1p}</p>
          <div class="picks" role="radiogroup" aria-label="{s1}">{pickrows}</div>
          <div class="usebox">
            <div class="fld" data-voice-row hidden>
              <label for="coVoice">{voiceLbl}</label>
              <input id="coVoice" name="voiceMinutes" type="number" min="0" max="100000" step="10"
                     inputmode="numeric" placeholder="{voicePh}">
            </div>
            <div class="fld" data-talk-row hidden>
              <label for="coTalk">{talkLbl}</label>
              <input id="coTalk" name="alimtalk" type="number" min="0" max="100000" step="50"
                     inputmode="numeric" placeholder="{talkPh}">
            </div>
          </div>
        </div>

        <div class="coblock">
          <h2><i>3</i>{s2}</h2>
          <p>{s2p}</p>
          <div class="two" style="margin-top:22px;">
            <div class="fld">
              <label for="coCompany">{fCompany}</label>
              <input id="coCompany" name="company" type="text" required autocomplete="organization">
            </div>
            <div class="fld">
              <label for="coBiz"><span data-biz-label>{fBiz}</span>
                <span class="opt" data-biz-optional hidden>{optional}</span></label>
              <input id="coBiz" name="bizNo" type="text" required inputmode="numeric"
                     placeholder="000-00-00000" maxlength="12" autocomplete="off">
            </div>
          </div>
          <div class="fld">
            <label for="coAddress">{fAddress}</label>
            <input id="coAddress" name="billingAddress" type="text" required
                   autocomplete="street-address" placeholder="{addressPh}">
            <span class="hint">{addressHint}</span>
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
                     placeholder="010-0000-0000" maxlength="24">
            </div>
          </div>
          <div class="fld">
            <label for="coTax"><span data-tax-email-label>{fTax}</span> <span class="opt">{optional}</span></label>
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
          <h2><i>4</i>{s3}</h2>
          <p>{s3p}</p>
          <div class="picks" role="radiogroup" aria-label="{s3}">{methodrows}</div>
        </div>

        <div class="coblock">
          <h2><i>5</i>{s4}</h2>
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
        countries=countries,
        kick=t('주문', 'Order'),
        h1=t('주문서입니다.<br>2분이면 끝납니다.',
             'The order form.<br>Two minutes, no account.'),
        sub=t('계정을 만들지 않아도 됩니다. 아래를 채우시면 접수되고, '
              '영업일 하루 안에 사람이 확인 연락을 드립니다. '
              '<b>이 화면에서 결제되는 금액은 없습니다.</b>',
              'No account needed, wherever you are. Fill this in and it is recorded; a person confirms '
              'within one business day. <b>Nothing is charged on this screen.</b>'),
        s0=t('어디에서 쓰시는지', 'Where you are'),
        s0p=t('나라에 따라 통화와 세금 처리, 그리고 인보이스에 들어갈 번호가 달라집니다. '
              '먼저 고르시면 아래 금액이 그 기준으로 바뀝니다.',
              'Your country sets the currency, how tax is handled, and which number goes on the '
              'invoice. Pick it first and the figures below follow.'),
        fCountry=t('청구받으실 나라', 'Where we invoice you'),
        buyerTypes=buyerTypes,
        serviceCountries=serviceCountries,
        fBuyer=t('구매 주체', 'Buying as'),
        buyerHint=t('세금 처리가 여기서 갈립니다. 사업자와 개인, 공공기관이 서로 다릅니다.',
                    'This decides the tax treatment. Businesses, individuals, and public bodies differ.'),
        fServiceCountry=t('실제로 쓰실 나라', 'Where you will actually use it'),
        serviceHint=t('청구받으실 나라와 다른 경우에만 골라 주세요.',
                      'Only if it differs from the country we invoice.'),
        fAddress=t('청구 주소', 'Billing address'),
        addressPh=t('세금계산서·인보이스에 적힐 주소', 'The address that goes on the invoice'),
        addressHint=t('세금계산서와 인보이스에 그대로 들어갑니다.',
                      'This goes on the tax invoice or invoice exactly as written.'),
        s1=t('무엇을 쓰실지', 'What you are taking'),
        s1p=t('나중에 바꾸실 수 있습니다. 요금제는 매달 올리거나 내릴 수 있고, 위약금이 없습니다.',
              'You can change this later. Plans move up or down monthly, with no penalty.'),
        voiceLbl=t('한 달 예상 통화 시간 (분) — 선택', 'Expected talk minutes a month — optional'),
        voicePh=t('예: 600', 'e.g. 600'),
        talkLbl=t('한 달 예상 알림톡 발송 (건) — 선택',
                  'Expected notification messages a month — optional'),
        talkPh=t('예: 300', 'e.g. 300'),
        s2=t('세금계산서를 받으실 곳', 'Where the tax invoice goes'),
        s2p=t('한국 사업자이시면 사업자등록번호를 입력하시는 대로 확인합니다. 세금계산서 발행에 '
              '필요하기 때문입니다. 그 밖의 나라에서는 인보이스에 찍을 번호일 뿐이라 선택입니다.',
              'If you are in Korea the registration number is checked as you type, because the '
              'tax invoice needs it. Everywhere else it just goes on the invoice, so it is optional.'),
        fCompany=t('상호', 'Company'), fBiz=t('사업자등록번호', 'Business registration number'),
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
        agTransfer=t('<b>개인정보 국외 이전에 동의합니다.</b> 응대 문장을 만드는 언어모델이 미국에서 '
                     '돌아갑니다. 이전받는 회사와 그 나라는 '
                     '<a href="./privacy.html#transfer" target="_blank" rel="noopener">개인정보처리방침 4항</a>에 '
                     '적어 두었습니다. 동의하지 않으시면 서비스의 핵심 기능을 쓰실 수 없습니다.',
                     '<b>I agree to processing outside my country.</b> The service is operated from '
                     'South Korea, and the language model that drafts each reply runs in the United '
                     'States. Every company in that chain is named, with the country it operates in, '
                     'in <a href="./security.html#subprocessors" target="_blank" rel="noopener">the '
                     'subprocessor list</a>. For transfers out of the UK or EEA our Data Processing '
                     'Agreement incorporates the Standard Contractual Clauses &mdash; ask for it at '
                     'hello@saleringo.com. Without this the core function cannot run.'),
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
        sumFoot=t('금액은 <b>세금 별도</b>로 표시하고, 세금이 붙는 경우에만 위 합계에 더합니다. '
                  '첫 달만 <b>개시일부터 그 달 말일까지 날짜로 나눠</b> 청구하며, 개시일이 정해지면 '
                  '그 날짜로 계산한 확정 금액을 먼저 알려 드립니다. '
                  '통화료와 알림톡은 <b>쓰신 만큼 다음 달에</b> 정산합니다.',
                  'Figures are shown <b>net of tax</b>; tax is added to the total only where we collect it. '
                  'Only the first month is <b>prorated by days</b>, from the start date, and we send '
                  'the exact figure once that date is set. '
                  'Talk time and messages are settled <b>next month on actual use</b>.'),
        barLbl=t('매월 결제 금액', 'Every month'),
        seller=t(seller_line('ko') + '<br>'
                 '<b>청약철회</b> — 접수 후 서비스 개시 전에는 언제든 취소하실 수 있으며 금액이 청구되지 '
                 '않습니다. 개시 후에는 「이용약관」 제5조에 따라, <b>첫 결제일부터 14일 안에는 전액 '
                 '환불</b>하고, 그 뒤에는 해지 신청일부터 그 달 남은 날수만큼 날짜로 계산해 환불합니다. '
                 '이미 사용한 통화료 등 사용량 요금은 게시된 단가로 차감합니다. 위약금은 없습니다.',
                 seller_line('en') + '<br>'
                 '<b>Cancellation</b> — before service starts, cancelling costs nothing and no amount '
                 'is charged. After it starts, &sect;3 of the Terms applies: you can cancel any day, the '
                 'first payment is refunded <b>in full within 14 days</b>, and after that we refund '
                 'the unused part of the month, counted by date. Nothing renews. Usage already spent is '
                 'deducted at the listed rates. There is no penalty.<br>'
                 'Invoices come from the Korean entity above. Korean customers are billed in won with 10% '
                 'VAT; everywhere else it is US dollars with no tax added by us.'))

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
