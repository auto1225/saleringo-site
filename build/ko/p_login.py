# -*- coding: utf-8 -*-
"""고객사 로그인 문 (한국어·영문).

왜 필요한가.

판매 사이트에 로그인 단추가 없었습니다. 요금을 내고 쓰시는 사장님이
claude.saleringo.com 에 오시면 자기 화면으로 들어갈 문이 아무 데도
없었습니다. 주소를 외우고 계신 분만 들어가셨습니다.

왜 "로그인 화면"이 아니라 "문"인가.

이 제품은 업체마다 자기 주소를 씁니다(heritique.saleringo.com,
saebom.saleringo.com …). 로그인 화면은 그 주소 안에 있고, 거기서 업체
이름과 색이 나옵니다. 그래서 모두가 함께 쓰는 로그인 주소라는 것이
없습니다. 여기서는 주소만 받아서 그 주소의 로그인 화면으로 보내
드립니다. 비밀번호는 여기서 받지 않습니다 — 판매 사이트가 남의
비밀번호를 만질 이유가 없습니다.

회원가입은 왜 없는가.

이 회사는 주문서를 받고, 사람이 확인하고, 서면 주문서에 양측이 서명한
뒤에 열어 드립니다. 요금·약관 페이지가 전부 그렇게 적혀 있습니다.
그 옆에 "회원가입" 단추를 두면 같은 사이트가 두 가지 다른 계약 방법을
말하게 됩니다. 그래서 여기서는 주문서와 상담으로 보냅니다.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import NAV, FOOT, page  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)


CSS = """
  .lgwrap{max-width:620px;margin:0 auto;}
  .lgform{margin-top:32px;}
  .lgfield{display:grid;gap:10px;}
  .lgfield > label{font-size:var(--fs-sm);font-weight:600;color:#141A1F;}
  .lgaddr{display:flex;align-items:stretch;border:1px solid var(--hair-d);border-radius:10px;
    background:#FFFFFF;overflow:hidden;}
  .lgaddr input{flex:1 1 auto;min-width:0;border:0;padding:14px 16px;font-size:var(--fs-body);
    font-family:var(--mono,ui-monospace,monospace);color:#141A1F;background:transparent;}
  .lgaddr input:focus{outline:none;}
  .lgaddr .suffix{display:flex;align-items:center;padding:0 16px;background:rgba(20,26,31,.045);
    border-left:1px solid var(--hair-d);font-family:var(--mono,ui-monospace,monospace);
    font-size:var(--fs-sm);color:var(--tx2);white-space:nowrap;}
  .lgaddr:focus-within{border-color:var(--teal);box-shadow:0 0 0 3px rgba(11,120,120,.12);}
  .lghint{font-size:var(--fs-xs);color:var(--tx3);line-height:1.7;}
  .lgpreview{font-family:var(--mono,ui-monospace,monospace);font-size:var(--fs-xs);color:var(--teal);}
  .lgerr{min-height:20px;font-size:var(--fs-xs);color:var(--red,#C0392B);font-weight:600;}
  .lgform .btn{margin-top:4px;}
  .lgcards{margin-top:44px;display:grid;grid-template-columns:1fr 1fr;gap:18px;}
  @media (max-width:700px){.lgcards{grid-template-columns:1fr;}}
  .lgcard{padding:24px 22px;border:1px solid var(--hair-d);border-radius:14px;
    background:rgba(20,26,31,.028);}
  .lgcard b{display:block;color:#141A1F;font-size:var(--fs-body);margin-bottom:8px;}
  .lgcard p{font-size:var(--fs-sm);line-height:1.8;color:var(--tx2);}
  .lgcard .lnk{display:inline-block;margin-top:12px;font-size:var(--fs-sm);font-weight:600;}
  .lgnote{margin-top:34px;padding-top:22px;border-top:1px solid var(--hair-d);
    font-size:var(--fs-xs);line-height:1.85;color:var(--tx3);}
"""

BODY = """
<header class="hero nophoto sec-dark bg-aurora">
  <div class="scrim" aria-hidden="true"></div>
  {NAV}
  <div class="wrap hero-inner">
    <span class="eyebrow"><i></i>{eyebrow}</span>
    <h1 style="margin-top:24px;">{h1}</h1>
    <p class="sub">{lead}</p>
  </div>
</header>

<main>
<section class="t-md sec-light bg-paper">
  <div class="wrap">
    <div class="lgwrap">
      <form class="lgform" data-workspace-login novalidate>
        <div class="lgfield">
          <label for="wsaddr">{fAddr}</label>
          <div class="lgaddr">
            <input id="wsaddr" name="workspace" type="text" data-ws-input
                   autocomplete="organization" autocapitalize="none" autocorrect="off"
                   spellcheck="false" inputmode="url" placeholder="{ph}"
                   aria-describedby="wshint">
            <span class="suffix" aria-hidden="true">.saleringo.com</span>
          </div>
          <p class="lgpreview" data-ws-preview hidden></p>
          <p class="lgerr" data-ws-error role="alert" aria-live="polite"></p>
          <p class="lghint" id="wshint">{addrHint}</p>
        </div>
        <p><button class="btn btn-teal" type="submit" data-ws-go>{cta}<span class="cir">&#8599;</span></button></p>
      </form>

      <noscript><p class="lghint" style="margin-top:16px;">{noscript}</p></noscript>

      <div class="lgcards">
        <div class="lgcard">
          <b>{c1t}</b>
          <p>{c1p}</p>
          <a class="lnk" href="./order-status.html">{c1a} &rarr;</a>
        </div>
        <div class="lgcard">
          <b>{c2t}</b>
          <p>{c2p}</p>
          <a class="lnk" href="./checkout.html">{c2a} &rarr;</a>
        </div>
      </div>

      <p class="lgnote">{note}</p>
    </div>
  </div>
</section>

{FOOT}
</main>
"""


def build(lang):
    ko = lang == 'ko'

    def t(k, e):
        return k if ko else e

    body = BODY.format(
        NAV=NAV,
        FOOT=FOOT,
        eyebrow=t('고객사 로그인', 'Customer sign-in'),
        h1=t('쓰고 계신 주소로<br>들어가십니다.',
             'Sign in at your own<br>address.'),
        lead=t('업체마다 주소가 다릅니다. 사장님 주소를 넣으시면 그 주소의 로그인 화면으로 '
               '보내 드립니다. 비밀번호는 이 화면에서 받지 않습니다.',
               'Every business has its own address. Enter yours and we send you to the sign-in '
               'screen there. This page never asks for your password.'),
        fAddr=t('쓰고 계신 주소', 'Your address'),
        ph=t('예: saebom', 'e.g. saebom'),
        addrHint=t('개통 안내 메일에 적힌 주소입니다. 주소창에서 통째로 복사해 붙여 넣으셔도 되고, '
                   '앞부분만 적으셔도 됩니다. 자기 도메인을 쓰고 계시면 그 도메인을 그대로 넣으십시오.',
                   'It is in your welcome email. Paste the whole address from your browser or type '
                   'just the first part. If you use your own domain, enter that instead.'),
        cta=t('로그인 화면으로', 'Go to sign-in'),
        noscript=t('자바스크립트가 꺼져 있습니다. 주소창에 '
                   '<b>사장님주소.saleringo.com/login</b> 을 바로 치시면 됩니다.',
                   'JavaScript is off. Type <b>youraddress.saleringo.com/login</b> in the address '
                   'bar instead.'),
        c1t=t('주문은 했는데 아직 안 열렸습니다', 'Ordered, not open yet'),
        c1p=t('개통 전에는 로그인할 화면이 아직 없습니다. 주문번호와 접수하실 때 쓰신 이메일로 '
              '지금 어느 단계인지 보실 수 있습니다.',
              'Before provisioning there is no screen to sign in to yet. Your order number and the '
              'email you used will show where it stands.'),
        c1a=t('주문 조회', 'Check my order'),
        c2t=t('아직 고객이 아닙니다', 'Not a customer yet'),
        c2p=t('계정은 주문서를 받고 사람이 확인한 뒤에 열어 드립니다. 스스로 가입하는 화면은 '
              '두지 않았습니다 — 회선과 지식베이스를 같이 준비해야 첫날부터 제대로 받기 '
              '때문입니다.',
              'Accounts are opened after we receive your order and a person confirms it. There is '
              'no self-serve sign-up, because the phone line and the answer set have to be ready '
              'together for day one to work.'),
        c2a=t('주문서 열기', 'Open the order form'),
        note=t('주소가 기억나지 않으시면 hello@saleringo.com 으로 회사 이름과 함께 보내 주십시오. '
               '사람이 확인해서 알려 드립니다. 직원 계정 추가와 비밀번호 재설정은 로그인하신 뒤 '
               '설정에서 하시거나, 같은 주소로 요청하시면 됩니다.',
               'If you cannot remember the address, email hello@saleringo.com with your company '
               'name and a person will look it up. Adding staff accounts and resetting passwords '
               'is done inside your workspace, or by writing to the same address.'),
    )

    return page(
        'login.html',
        t('고객사 로그인 &mdash; Saleringo', 'Customer sign-in &mdash; Saleringo'),
        t('쓰고 계신 주소를 넣으시면 그 주소의 로그인 화면으로 보내 드립니다. '
          '주문했지만 아직 개통 전이시면 주문 조회로 확인하십시오.',
          'Enter the address you use and we send you to the sign-in screen there. If you have '
          'ordered but are not open yet, check your order status instead.'),
        body,
        css=CSS,
        grade='trust',
        scripts=('site', 'balance', 'wrap', 'login'),
        lang=lang,
        crumbs=[
            (t('홈', 'Home'), 'index.html'),
            (t('고객사 로그인', 'Customer sign-in'), 'login.html'),
        ],
    )


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print(', '.join(build(l) for l in ('ko', 'en')))
