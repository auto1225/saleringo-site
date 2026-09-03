/* ── 주문서 ────────────────────────────────────────────────────────────────
   구매자가 막히는 자리를 하나씩 없애는 것이 이 파일이 하는 일의 전부입니다.
   기능을 더하는 것이 아니라, 이미 알고 있는 실패를 미리 막습니다.

     · 금액이 화면 밖으로 나가지 않습니다. 오른쪽(모바일에서는 아래) 요약이
       항상 붙어 있어서, 무엇을 고르든 지금 얼마인지가 늘 보입니다.
     · 사업자등록번호는 자리수만 세지 않고 국세청 검증식으로 확인합니다.
       오타 하나가 세금계산서 발행까지 살아남으면 그때는 고치기가 훨씬
       비쌉니다. 하이픈은 치는 대로 저절로 들어갑니다.
     · 오류는 타이핑하는 중에 뜨지 않습니다. 칸을 벗어날 때 한 번,
       그리고 제출을 누를 때 못 채운 첫 칸으로 데려다 줍니다.
     · 새로고침하거나 뒤로 갔다 와도 입력이 남아 있습니다. 주소와
       사업자번호를 두 번 치게 만드는 주문서는 두 번째에 닫힙니다.
     · 제출 버튼은 한 번만 눌립니다. 그리고 같은 주문에는 같은 키를 붙여
       보내므로, 두 번 눌려도 주문은 하나로 접수됩니다.
     · 결제된 척하지 않습니다. 결제사가 붙기 전까지 화면은 "접수"라고만
       말하고, 다음에 무슨 일이 일어나는지 적습니다.

   금액 계산은 assets/data/pricing.json 하나만 봅니다. 서버도 같은 파일을
   읽고 다시 계산하므로, 여기 보이는 숫자와 청구되는 숫자는 같은 뿌리에서
   나옵니다.                                                                */
(function () {
  'use strict';

  var form = document.querySelector('[data-checkout]');
  if (!form) return;

  var LANG = (document.documentElement.lang || 'ko').slice(0, 2) === 'en' ? 'en' : 'ko';
  var KO = LANG === 'ko';
  var P = null, STATE = null, READY = null;
  var KEY = 'sr-order-draft';

  var T = {
    ko: {
      monthly: '월 이용료', total: '매월 결제 금액', tax: '세금',
      firstLabel: '첫 달은 개시일 기준 일할',
      firstIf: '오늘 개시한다면 {amount} — 이번 달 {total}일 가운데 {left}일치입니다.',
      notNow: '이 버튼은 접수만 합니다. 지금 청구되는 금액은 없습니다.',
      usage: '사용량 예상 — 청구에 포함되지 않습니다',
      from: '부터', estimateNote: '쓰신 만큼 다음 달에 정산합니다.',
      overage: '월 {included}건이 포함되어 있고, 넘긴 만큼만 건당 {rate}이 붙습니다. 한도를 미리 걸어 두실 수 있습니다.',
      discount: '{name} 적용 — 처음 {months}개월 {percent}% 할인. 그 뒤에는 월 {after} 입니다.',
      noVoiceHere: '이 나라에서는 AI 전화 회선이 아직 열려 있지 않습니다. 채팅과 메신저는 ' +
                   '지금 되고, 이 요금제의 나머지도 그대로 씁니다. 회선이 열리기 전에는 ' +
                   '전화 부분을 시작하지도, 그 몫을 청구하지도 않습니다.',
      soonVoiceHere: '이 나라는 지금 AI 전화 회선을 여는 중입니다. 채팅과 메신저는 지금 ' +
                   '됩니다. 개통 날짜가 정해지면 시작 전에 먼저 알려 드립니다.',
      taxNone: '저희는 대한민국 법인이고 귀사 국가에 세무 등록이 없어 세금을 걷지 않습니다. 현지 규정에 따른 신고 의무는 귀사에 남습니다.',
      taxReverse: '리버스 차지 대상입니다. 저희가 세금을 붙이지 않고, 귀사에서 신고하시게 됩니다. 세금 번호를 주시면 인보이스에 찍어 드립니다.',
      required: '필수 항목입니다',
      bizBadKR: '사업자등록번호가 올바르지 않습니다. 10자리를 다시 확인해 주세요.',
      bizBad: '번호 형식을 다시 확인해 주세요.',
      emailBad: '이메일 형식이 올바르지 않습니다.',
      phoneBad: '전화번호를 다시 확인해 주세요.',
      agreeBad: '필수 동의 항목을 확인해 주세요.',
      sending: '접수하는 중…',
      failNet: '전송에 실패했습니다. 입력하신 내용은 그대로 남아 있습니다. 잠시 뒤 다시 눌러 주십시오. 같은 주문이 두 번 접수되는 일은 없습니다. 계속 안 되면 hello@saleringo.com 으로 보내 주십시오.',
      failDest: '지금은 온라인 접수를 받을 수 없습니다. 위 「서면 주문 제안 요청」을 눌러 주시면 담당자가 같은 내용으로 서면 주문서를 만들어 보내 드립니다.',
      offline: '지금은 온라인 주문 접수가 열려 있지 않습니다. 아래 내용을 그대로 두시고 「서면 주문 제안 요청」을 눌러 주시면, 담당자가 같은 내용으로 서면 주문서를 만들어 보내 드립니다.',
      proposalCta: '서면 주문 제안 요청',
      payCta: '주문 접수하기',
      taxTreat: {
        vat_charged: '부가세 10% 포함해 청구하고 전자세금계산서를 발행합니다.',
        reverse: '대리납부(리버스 차지) 대상입니다. 저희가 세금을 붙이지 않고 귀사가 자국에 신고하십니다.',
        none: '저희는 대한민국 법인이고 귀사 국가에 세무 등록이 없어 세금을 걷지 않습니다.',
        review: '세금 별도 · 구매 법인 검증 후 서면 주문서에서 확정합니다.'
      },
      noPrice: '요금표를 불러오지 못했습니다. 금액을 확인하실 수 없는 상태로 주문을 받지 않겠습니다. 새로고침해 보시고, 계속 이러면 hello@saleringo.com 으로 알려 주십시오.'
    },
    en: {
      monthly: 'Monthly', total: 'Charged every month', tax: 'Tax',
      firstLabel: 'First month prorated from the start date',
      firstIf: 'Starting today that would be {amount} — {left} of this month’s {total} days.',
      notNow: 'This button records the order. Nothing is charged now.',
      usage: 'Usage estimate — not part of the charge',
      from: ' and up', estimateNote: 'Settled next month on what you actually use.',
      overage: '{included} conversations are included; past that it is {rate} each. You can cap the month.',
      discount: '{name} applied — {percent}% off for your first {months} months. After that it is {after} a month.',
      noVoiceHere: 'AI phone is not open in your country yet. Chat and messengers work today, ' +
                   'and the rest of this plan works in full. We will not start the voice part, ' +
                   'or bill you for it, until a line is live where you are.',
      soonVoiceHere: 'AI phone is being opened in your country now. Chat and messengers work ' +
                   'today. We will tell you the date the line goes live before anything starts.',
      taxNone: 'We are a Korean company with no tax registration in your country, so we add no tax. Any local filing duty stays with you.',
      taxReverse: 'This is a reverse-charge sale. We add no tax and you account for it. A tax number you give us goes on the invoice.',
      required: 'Required',
      bizBadKR: 'That registration number does not check out. Please look at the 10 digits again.',
      bizBad: 'Please check the format of that number.',
      emailBad: 'That email address does not look right.',
      phoneBad: 'Please check the phone number.',
      agreeBad: 'Please tick the required agreements.',
      sending: 'Sending…',
      failNet: 'That did not go through. What you entered is still here. Try again in a moment — the same order cannot be recorded twice. If it keeps failing, send it to hello@saleringo.com.',
      failDest: 'Online orders are not being taken right now. Press “Request a written order” above and a person will prepare the same order in writing.',
      offline: 'Online ordering is not open at the moment. Leave what you have entered and press “Request a written order”, and a person will prepare the same order in writing.',
      proposalCta: 'Request a written order',
      payCta: 'Place the order',
      taxTreat: {
        vat_charged: 'Korean VAT 10% is added and a Korean tax invoice is issued.',
        reverse: 'This is a reverse-charge sale. We add no tax and you account for it at home.',
        none: 'We are a Korean company with no tax registration in your country, so we add no tax.',
        review: 'Tax excluded · confirmed in the written order after we verify the buying entity.'
      },
      noPrice: 'The price list did not load. We will not take an order while you cannot see the amount. Try reloading; if it keeps happening, tell us at hello@saleringo.com.'
    }
  }[LANG];

  function $(s, r) { return (r || form).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || form).querySelectorAll(s)); }
  /* 금액을 그 통화의 관습대로 씁니다. 원화는 뒤에 "원", 달러는 앞에 "$".
     79.00 달러라고 쓰면 아무도 그렇게 읽지 않고, 110000.00 원은 잘못 쓴
     것처럼 보입니다. */
  function money(n, cur) {
    var c = (P && P.currencies[cur]) || { symbol: '', position: 'after', decimals: 0, locale: 'en-US' };
    /* 599 는 "$599", 0.14 는 "$0.14". 자리수를 하나로 고정하면 둘 중 하나가
       틀립니다. */
    var whole = Math.abs(n - Math.round(n)) < 1e-9;
    var t = new Intl.NumberFormat(c.locale, {
      minimumFractionDigits: whole ? 0 : c.decimals,
      maximumFractionDigits: whole ? 0 : c.decimals
    }).format(n);
    return c.position === 'before' ? c.symbol + t : t + c.symbol;
  }

  /* ── 저장과 복구 ───────────────────────────────────────────────────── */
  /* 동의는 저장하지도 복원하지도 않습니다. 새로고침 한 번에 동의가
     저절로 다시 체크되어 있으면, 그건 그 사람이 동의한 것이 아닙니다. */
  function isConsent(el) {
    return el.type === 'checkbox' && /^agree/.test(el.name || '');
  }
  /* 초안은 오래 두지 않습니다. 회사명·사업자등록번호·담당자 이름·이메일·
     연락처가 기한 없이 브라우저에 남아 있으면, 공용 컴퓨터나 남의 자리에서
     한 번 열어 본 사람의 정보가 다음 사람에게 그대로 보입니다.
     탭을 닫으면 sessionStorage 는 지워지지만, 탭을 켜 둔 채로 자리를
     비우는 일이 훨씬 흔합니다. */
  var DRAFT_TTL = 2 * 60 * 60 * 1000;   /* 두 시간 */

  function snapshot() {
    var o = {};
    $$('input,select,textarea').forEach(function (el) {
      if (!el.name || el.name === 'company_website_hp') return;
      if (isConsent(el)) return;
      /* 페이지의 언어는 그 페이지가 정합니다. 저장했다가 되살리면,
         영어 주문서를 쓰다 한국어로 바꾼 사람의 제출 언어가 en 으로
         남습니다. 화면은 한국어인데 접수 언어는 영어인 상태입니다. */
      if (el.name === 'lang') return;

      if (el.type === 'radio') {
        /* 라디오는 이름 하나에 여러 칸입니다. 선택된 것만 적어야 합니다.
           예전에는 미선택 칸이 돌아올 때마다 값을 지웠기 때문에,
           목록의 마지막에 있는 것을 고르지 않으면 선택이 저장되지
           않았습니다. 그래서 언어를 바꾸면 요금제가 기본값으로 돌아갔습니다. */
        if (el.checked) o[el.name] = el.value;
        return;
      }
      if (el.type === 'checkbox') {
        if (el.checked) o[el.name] = el.value || true;
        return;
      }
      if (el.value !== '') o[el.name] = el.value;
    });
    try {
      sessionStorage.setItem(KEY, JSON.stringify({
        savedAt: Date.now(),
        /* 멱등성 열쇠도 함께 둡니다. 예전에는 자바스크립트 변수에만
           있었으므로 새로고침하면 새 열쇠가 생겼고, 응답이 끊긴 주문을
           다시 누르면 같은 주문이 두 건이 됐습니다. */
        idem: form._idem || null,
        fields: o
      }));
    } catch (e) {}
  }

  function restore() {
    var raw;
    try { raw = JSON.parse(sessionStorage.getItem(KEY) || 'null'); } catch (e) { return; }
    if (!raw) return;

    /* 옛 형식(칸만 담긴 것)은 만료를 알 수 없으므로 버립니다. */
    if (!raw.fields || !raw.savedAt) {
      try { sessionStorage.removeItem(KEY); } catch (e) {}
      return;
    }
    if (Date.now() - raw.savedAt > DRAFT_TTL) {
      try { sessionStorage.removeItem(KEY); } catch (e) {}
      return;
    }

    if (raw.idem) form._idem = raw.idem;

    var o = raw.fields;
    $$('input,select,textarea').forEach(function (el) {
      if (!el.name || !(el.name in o) || isConsent(el)) return;
      if (el.name === 'lang') return;
      if (el.type === 'checkbox') el.checked = true;
      else if (el.type === 'radio') { if (el.value === o[el.name]) el.checked = true; }
      else el.value = o[el.name];
    });
  }

  /* 같은 주문서에는 같은 열쇠. 응답이 끊겨 다시 눌러도 주문은 하나입니다.
     열쇠는 만들자마자 저장하므로 새로고침을 견딥니다. */
  function idemKey() {
    if (!form._idem) {
      form._idem = 'ck' + Date.now().toString(36) + Math.random().toString(36).slice(2, 12);
      snapshot();
    }
    return form._idem;
  }

  /* ── 입력을 치는 대로 다듬는다 ─────────────────────────────────────── */
  function fmtBiz(v) {
    var n = v.replace(/[^0-9]/g, '').slice(0, 10);
    if (n.length > 5) return n.slice(0, 3) + '-' + n.slice(3, 5) + '-' + n.slice(5);
    if (n.length > 3) return n.slice(0, 3) + '-' + n.slice(3);
    return n;
  }
  /* 한국 전화번호는 자리수와 국번에 따라 끊는 위치가 다릅니다.
     휴대폰 11자리는 3-4-4, 서울 02 는 2로 시작하고, 나머지 지역번호는
     3자리입니다. 한 가지 규칙으로 밀어붙이면 010123-4-5678 같은 것이
     나오고, 그걸 본 사람은 자기가 잘못 친 줄 압니다. */
  function fmtPhone(v) {
    var raw = String(v || '');
    /* 국제 표기는 손대지 않습니다. +82 10-1234-5678 을 한국 규칙으로 밀면
       821-0123-4567 이 되어, 친 번호와 다른 번호가 칸에 남습니다. */
    if (raw.indexOf('+') >= 0) return raw;

    var n = raw.replace(/[^0-9]/g, '');

    /* 국번의 길이는 번호마다 다릅니다. 서울은 두 자리(02), 안심번호와
       인터넷전화는 네 자리(0505·0507·0303), 나머지는 세 자리입니다.
       예전에는 이것을 무시하고 숫자를 11자리로 잘라 3-4-4 로 밀어붙였고,
       그래서 0507-1234-5678 이 050-7123-4567 이 되었습니다. 마지막 자리가
       사라지고 앞자리가 한 칸씩 밀렸는데, 친 사람은 알아채기 어렵습니다.
       접수된 번호로 전화를 걸면 다른 사람이 받습니다. */
    var head;
    if (/^1[5-9]/.test(n)) {
      /* 대표번호 1588·1600·1877 — 여덟 자리, 4-4 */
      if (n.length > 8) return raw;
      return n.length <= 4 ? n : n.slice(0, 4) + '-' + n.slice(4);
    } else if (/^0(50|30)/.test(n)) {
      head = 4;
    } else if (n.slice(0, 2) === '02') {
      head = 2;
    } else {
      head = 3;
    }

    /* 아는 모양보다 길면 손대지 않습니다. 모르는 번호를 다듬는 것보다
       친 그대로 두는 편이 낫습니다. */
    if (n.length > head + 8) return raw;
    if (n.length <= head) return n;

    var rest = n.length - head;
    /* 다 치기 전에는 하이픈을 하나만 넣습니다. 끊을 위치는 마지막 네 자리가
       나와야 정해지는데, 그 전에 미리 끊으면 치는 중에 숫자가 이리저리
       옮겨 다녀서 자기가 잘못 친 줄 알게 됩니다. */
    if (rest < 7) return n.slice(0, head) + '-' + n.slice(head);
    var mid = rest >= 8 ? 4 : 3;
    return n.slice(0, head) + '-' + n.slice(head, head + mid) + '-' + n.slice(head + mid);
  }
  function krBizValid(raw) {
    var n = String(raw || '').replace(/[^0-9]/g, '');
    if (n.length !== 10) return false;
    var w = [1, 3, 7, 1, 3, 7, 1, 3, 5], sum = 0;
    for (var i = 0; i < 9; i++) sum += Number(n[i]) * w[i];
    sum += Math.floor((Number(n[8]) * 5) / 10);
    return (10 - (sum % 10)) % 10 === Number(n[9]);
  }
  /* 검증은 그 번호가 실제로 검증 가능한 나라에서만 합니다. 세계의 모든
     사업자 번호 규칙을 안다고 주장하면, 멀쩡한 번호를 가진 사람이 통과할
     수 없는 칸이 생깁니다. */
  function bizValidFor(c, raw) {
    var v = String(raw || '').trim();
    if (!v) return !c || !c.taxIdRequired;
    if (c && c.taxIdCheck === 'kr') return krBizValid(v);
    /* 세계의 모든 사업자 번호 규칙을 안다고 주장하지 않고 형식만 봅니다.
       다만 허용 글자를 너무 좁게 잡으면 멀쩡한 번호가 막힙니다.
       멕시코 RFC 에는 &(예: ABC&850101AB1), 구형 아일랜드 VAT 에는
       + 와 * 가 들어갑니다(예: IE8Z*4928F). 그 사람들은 자기 나라
       번호를 그대로 쳤을 뿐인데 "올바르지 않습니다" 를 보게 됩니다. */
    return /^[A-Za-z0-9][A-Za-z0-9 .\-\/&+*]{3,29}$/.test(v);
  }
  var emailOk = function (v) { return /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(v); };

  /* ── 오류 표시 ─────────────────────────────────────────────────────── */
  function setErr(el, msg) {
    var fld = el.closest('.fld') || el.closest('.agree') || el.parentNode;
    var slot = fld.querySelector('.errline');
    if (!slot) {
      slot = document.createElement('span');
      slot.className = 'errline';
      slot.setAttribute('role', 'status');
      fld.appendChild(slot);
    }
    slot.textContent = msg || '';
    fld.classList.toggle('has-err', !!msg);
    el.setAttribute('aria-invalid', msg ? 'true' : 'false');
    return !msg;
  }
  function checkField(el) {
    var v = (el.value || '').trim();
    var c = countryOf(selection().country);
    if (el.name === 'bizNo') {
      if (!v) return setErr(el, (c && c.taxIdRequired) ? T.required : '');
      return setErr(el, bizValidFor(c, v) ? ''
        : ((c && c.taxIdCheck === 'kr') ? T.bizBadKR : T.bizBad));
    }
    if (el.hasAttribute('required') && !v && el.type !== 'checkbox') return setErr(el, T.required);
    if (el.type === 'email' && v) return setErr(el, emailOk(v) ? '' : T.emailBad);
    if (el.name === 'phone' && v) {
      /* 전화번호 규칙은 나라마다 다릅니다. 자리수를 세는 대신 숫자가 몇 개
         있는지만 봅니다. 그 이상을 검사하면 멀쩡한 번호를 거절합니다. */
      var d = v.replace(/[^0-9]/g, '');
      return setErr(el, d.length >= 6 && d.length <= 15 ? '' : T.phoneBad);
    }
    return setErr(el, '');
  }

  /* ── 금액 ──────────────────────────────────────────────────────────── */
  function selection() {
    var plan = $('input[name="plan"]:checked');
    var method = $('input[name="method"]:checked');
    var cty = $('[name="country"]');
    return {
      plan: plan ? plan.value : '',
      method: method ? method.value : '',
      country: cty ? cty.value : '',
      voiceMinutes: Number(($('[name="voiceMinutes"]') || {}).value) || 0,
      alimtalk: Number(($('[name="alimtalk"]') || {}).value) || 0
    };
  }

  function countryOf(code) {
    if (!P) return null;
    for (var i = 0; i < P.countries.length; i++) {
      if (P.countries[i].code === code) return P.countries[i];
    }
    return null;
  }

  /* 한국 시간으로 오늘이 며칠인가.
  
     이것이 왜 함수여야 하냐면, 화면은 브라우저의 시간대로 돌고 서버는 UTC 로
     돌기 때문입니다. 한국은 UTC+9 이라 매일 아침 9시 전에는 서버가 어제를
     보고 있습니다. 그 상태로 첫 달을 일할 계산하면 화면에 뜬 금액과 확인
     메일의 금액이 하루치 어긋나고, 매달 1일 오전에는 한 달치가 통째로
     어긋납니다. 파는 쪽과 사는 쪽이 서로 다른 날짜를 보고 있으면 그건
     버그가 아니라 분쟁입니다. 그래서 양쪽 다 서울 날짜만 봅니다. */
  function seoulToday(now) {
    var s = new Intl.DateTimeFormat('en-CA', {
      timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit'
    }).format(now || new Date());
    var p = s.split('-');
    return { y: +p[0], m: +p[1], d: +p[2] };
  }

  function proration(now) {
    var t = seoulToday(now);
    var daysInMonth = new Date(Date.UTC(t.y, t.m, 0)).getUTCDate();
    var remaining = daysInMonth - t.d + 1;
    return { daysInMonth: daysInMonth, remaining: remaining, factor: remaining / daysInMonth };
  }
  function quote() {
    var sel = selection();
    var plan = P.plans.filter(function (p) { return p.id === sel.plan; })[0];
    var c = countryOf(sel.country);
    if (!plan || !c) return null;
    var cur = c.currency;
    var rule = P.tax[c.code] || P.tax['default'];
    var rate = rule.collected ? rule.rate : 0;
    var round = function (n) { return cur === 'KRW' ? Math.round(n) : Math.round(n * 100) / 100; };
    var pr = proration(new Date());
    var est = [];
    P.usage.forEach(function (u) {
      if (u.planRequires === 'voice' && !plan.voice) return;
      if (u.planRequires === 'messenger' && !plan.messenger) return;
      var qty = Math.max(0, Number(sel[u.id]) || 0);
      if (!qty) return;
      est.push({ label: u.name[LANG], qty: qty, unit: u.unitPrice[cur], unitName: (u.unit && u.unit[LANG]) || '',
                 amount: round(qty * u.unitPrice[cur]), from: !!u.from });
    });
    var list = plan.price[cur];
    var disc = (P.discount && P.discount.active) ? P.discount : null;
    var net = disc ? round(list * (100 - disc.percent) / 100) : list;
    var firstNet = round(net * pr.factor);
    return {
      plan: plan, country: c, cur: cur, pr: pr, est: est,
      rate: rate, collected: !!rule.collected, taxLabel: rule.label || null,
      reverse: !!(c.reverseCharge && !rule.collected),
      list: list, disc: disc,
      after: round(list + round(list * rate)),
      net: net, tax: round(net * rate), total: round(net + round(net * rate)),
      firstTotal: round(firstNet + round(firstNet * rate)),
      /* 'live' 만 지금 됩니다. 'soon' 은 여는 중, 'no' 는 아직입니다.
         예전에는 이 값이 세 나라에만 붙어 있어서, 요금 페이지가 "안 된다"고
         적은 나라의 구매자가 AI 전화가 든 요금제를 골라도 조용했습니다. */
      voiceGap: !!(plan.voice && c.voice !== 'live') ? (c.voice === 'soon' ? 'soon' : 'no') : ''
    };
  }

  // 한국어와 영어는 어순이 다릅니다. "처음 3개월 50%" 와 "50% off for your
  // first 3 months" 는 숫자가 반대로 놓입니다. 자리를 순서로 채우면 한쪽이
  // 반드시 뒤집히고, 실제로 뒤집혀서 "처음 50개월 3% 할인" 이 나갔습니다.
  // 이름으로 채우면 어순이 달라도 각자 제자리에 들어갑니다.
  function fill(tpl, vals) {
    return String(tpl).replace(/\{(\w+)\}/g, function (m, k) {
      return Object.prototype.hasOwnProperty.call(vals, k) ? String(vals[k]) : m;
    });
  }

  function paint() {
    var box = document.querySelector('[data-summary]');
    if (!box || !P) return;
    var q = quote();
    if (!q) { box.innerHTML = ''; return; }
    var A = function (n) { return money(n, q.cur); };
    var r = [];
    r.push('<div class="sm-plan"><b>' + q.plan.name[LANG] + '</b><span>' +
      q.plan.channels[LANG] + '</span></div>');
    r.push('<div class="sm-row"><span>' + T.monthly + '</span><b>' +
      (q.disc ? '<s>' + A(q.list) + '</s> ' : '') + A(q.net) + '</b></div>');
    if (q.collected) {
      r.push('<div class="sm-row"><span>' +
        (q.taxLabel ? q.taxLabel[LANG] : T.tax) + '</span><b>' + A(q.tax) + '</b></div>');
    }
    r.push('<div class="sm-total"><span>' + T.total + '</span><b>' + A(q.total) + '</b></div>');
    if (q.disc) {
      r.push('<p class="sm-note sm-disc">' + fill(T.discount, {
        name: q.disc.name[LANG], percent: q.disc.percent,
        months: q.disc.months, after: A(q.after)
      }) + '</p>');
    }
    r.push('<p class="sm-notnow">' + T.notNow + '</p>');
    if (q.voiceGap) {
      r.push('<p class="sm-note sm-warn">' +
        (q.voiceGap === 'soon' ? T.soonVoiceHere : T.noVoiceHere) + '</p>');
    }
    if (!q.collected) {
      r.push('<p class="sm-note sm-tax">' + (q.reverse ? T.taxReverse : T.taxNone) + '</p>');
    }
    r.push('<div class="sm-first"><p>' + T.firstLabel + '</p><p class="sm-note">' +
      fill(T.firstIf, { amount: A(q.firstTotal), left: q.pr.remaining,
                        total: q.pr.daysInMonth }) + '</p></div>');
    if (q.est.length) {
      r.push('<div class="sm-est"><p>' + T.usage + '</p>' +
        q.est.map(function (e) {
          return '<div class="sm-row"><span>' + e.label + ' ' +
            new Intl.NumberFormat(LANG === 'ko' ? 'ko-KR' : 'en-US').format(e.qty) + (e.unitName ? (LANG === 'ko' ? e.unitName : ' ' + e.unitName) : '') +
            '</span><b>' + A(e.amount) + (e.from ? T.from : '') + '</b></div>';
        }).join('') + '<p class="sm-note">' + T.estimateNote + '</p></div>');
    }
    if (P.overage) {
      var fmt = new Intl.NumberFormat(LANG === 'ko' ? 'ko-KR' : 'en-US');
      r.push('<p class="sm-note sm-over">' + fill(T.overage, {
        included: fmt.format(q.plan.conversations),
        rate: A(P.overage.perConversation[q.cur])
      }) + '</p>');
    }
    box.innerHTML = r.join('');
    var bar = document.querySelector('[data-paybar-total]');
    if (bar) bar.textContent = A(q.total);
  }

  /* 고를 수 없는 것을 띄워 두면 고를 수 있는 줄 알고 채우게 됩니다.
     그리고 나라가 바뀌면 사업자 번호의 이름과 필수 여부, 전화번호의
     국번 안내가 함께 바뀌어야 합니다. 라벨이 "사업자등록번호"인 채로
     미국 구매자에게 남아 있으면, 그 사람은 자기가 낼 수 없는 것을
     요구받았다고 읽습니다. */
  function syncCountry() {
    var sel = selection();
    var plan = P ? P.plans.filter(function (p) { return p.id === sel.plan; })[0] : null;
    var c = countryOf(sel.country);

    /* 요금제 타일의 금액은 페이지에 박혀 있었습니다. 한국어 페이지에서
       나라를 미국으로 바꾸면 타일은 "820,000원", 요약은 "$599" 를 같이
       보여 줬습니다. 자기가 무슨 통화로 얼마를 내는지 알 수 없습니다.
       국가가 바뀌면 타일도 함께 다시 그립니다. */
    if (P && c) {
      P.plans.forEach(function (pl) {
        var el = document.querySelector('[data-plan-price="' + pl.id + '"]');
        if (!el) return;
        var per = el.querySelector('i');
        el.textContent = money(pl.price[c.currency], c.currency);
        if (per) el.appendChild(per);
      });
    }

    /* 청구 국가와 실제 사용 국가가 다를 수 있습니다. 한국 밖에서만
       물어봅니다 — 한국 안에서는 거의 언제나 같습니다. */
    var svc = document.querySelector('[data-service-row]');
    if (svc) svc.hidden = !(c && c.code !== 'KR');

    /* 나라·요금제·구매 주체가 바뀌면 서버 판정도 바뀝니다. */
    askServerSoon();

    /* 숨은 칸의 값은 그대로 전송되고 있었습니다 — Scale 에서 넣은
       통화량이 Start 주문에 실려 갔습니다. 숨기면 지웁니다. */
    var row = document.querySelector('[data-voice-row]');
    if (row) {
      row.hidden = !(plan && plan.voice);
      if (row.hidden) { var vi = row.querySelector('input'); if (vi) vi.value = ''; }
    }
    var talk = document.querySelector('[data-talk-row]');
    if (talk) {
      talk.hidden = !(plan && plan.messenger && sel.country === 'KR');
      if (talk.hidden) { var ti = talk.querySelector('input'); if (ti) ti.value = ''; }
    }

    var rec = document.querySelector('[data-recurring-agree]');
    if (rec) {
      var isCard = sel.method === 'card';
      rec.hidden = !isCard;
      var cb = rec.querySelector('input');
      if (cb) { cb.required = isCard; if (!isCard) cb.checked = false; }
    }

    var biz = $('[name="bizNo"]');
    if (biz && c) {
      var lab = document.querySelector('[data-biz-label]');
      var opt = document.querySelector('[data-biz-optional]');
      if (lab) lab.textContent = c.taxIdLabel[LANG];
      if (opt) opt.hidden = !!c.taxIdRequired;
      biz.required = !!c.taxIdRequired;
      biz.placeholder = c.taxIdPlaceholder || '';
      biz.setAttribute('inputmode', c.taxIdCheck === 'kr' ? 'numeric' : 'text');
      biz.setAttribute('maxlength', c.taxIdCheck === 'kr' ? '12' : '30');
    }
    var phone = $('[name="phone"]');
    if (phone && c) phone.placeholder = c.dial ? c.dial + ' …' : '';

    /* 한국 밖에서는 세금계산서가 아니라 인보이스입니다. */
    var taxLab = document.querySelector('[data-tax-email-label]');
    if (taxLab) {
      taxLab.textContent = (sel.country === 'KR')
        ? (LANG === 'ko' ? '세금계산서 수신 이메일' : 'Tax invoice email')
        : (LANG === 'ko' ? '인보이스 수신 이메일' : 'Invoice email');
    }
  }
  var syncVoice = syncCountry;

  function gate() {
    var btn = $('[data-submit]');
    if (!btn) return;
    var missing = $$('input[required]').filter(function (el) {
      return el.type === 'checkbox' ? !el.checked : !(el.value || '').trim();
    }).length;
    btn.classList.toggle('is-waiting', missing > 0);
  }

  /* ── 영수 화면 ─────────────────────────────────────────────────────── */
  function receipt(res) {
    var q = res.quote || {};
    /* 주문번호는 저희 서버가 만든 값이지만, 화면에 그대로 심는 유일한
       외부 문자열입니다. 아는 글자만 통과시킵니다. 돈이 오가는 화면에서
       "우리가 만든 값이니 괜찮다"는 가정은 공짜로 두지 않습니다. */
    var no = String(res.orderNo || '').replace(/[^A-Z0-9-]/g, '').slice(0, 20);
    var cur = q.currency || 'KRW';
    /* 재시도(멱등 중복)의 응답에는 quote 가 실려 오지 않습니다. 그때
       「매월 __」 처럼 빈 금액을 그리는 것보다, 금액 줄을 빼고 주문
       조회로 안내하는 쪽이 맞습니다. */
    var monthly = (q.monthly && q.monthly.total != null) ? money(q.monthly.total, cur) : '';
    var first = q.firstMonthIfToday ? money(q.firstMonthIfToday.total, cur) : '';
    var after = (q.discount && q.afterDiscount)
      ? money(q.afterDiscount.total, cur) : '';
    var steps = KO
      ? ['영업일 하루 안에 담당자가 확인 연락을 드립니다.',
         '우리 요금표와 영업시간을 받아 응대를 만들어 드립니다.',
         '만들어진 응대를 먼저 보시고, 그때 결제 안내를 보내 드립니다.']
      : ['A person confirms within one business day.',
         'We build your answering from your price list and hours.',
         'You read it first; the payment step comes after that.'];
    if (!(READY && READY.confirmation)) {
      steps.unshift(KO ? '확인 메일은 아직 발송되지 않습니다 — 이 번호를 적어 두시거나 주문 조회 페이지를 이용해 주세요.'
                       : 'No confirmation email is sent yet — write this number down, or use the order status page.');
    }
    form.innerHTML =
      '<div class="ordersent" role="status" tabindex="-1">' +
        '<b>' + (KO ? '주문이 접수되었습니다.' : 'Your order is in.') + '</b>' +
        '<code class="orderno">' + no + '</code>' +
        (monthly ? '<p class="os-money">' +
          (KO ? '매월 ' : 'Every month ') + '<b>' + monthly + '</b>' +
          (first ? (KO ? ' · 첫 달은 개시일 기준 일할(오늘이면 ' : ' · first month prorated (today, ')
                 + first + ')' : '') +
        '</p>' : '<p class="os-money">' +
          (KO ? '금액은 <a class="lnk" href="./order-status.html?no=' + no +
                '">주문 조회</a>에서 확인하실 수 있습니다.'
              : 'The amounts are on <a class="lnk" href="./order-status.html?no=' + no +
                '">your order page</a>.') + '</p>') +
        /* 할인이 끝나면 금액이 두 배가 됩니다. 이 화면과 확인 메일이
           구매자에게 남는 전부인데, 여기에 할인가만 적혀 있으면 넉 달째
           청구서를 보고 "듣던 것과 다르다"고 하는 것이 당연합니다. */
        (after ? '<p class="os-after">' +
          (KO ? '위 금액은 ' + (q.discount.percent) + '% 할인이 적용된 처음 ' +
                q.discount.months + '개월치입니다. ' + (q.discount.months + 1) +
                '개월째부터는 매월 ' + after + ' 입니다.'
              : 'That is the first ' + q.discount.months + ' months at ' +
                q.discount.percent + '% off. From month ' + (q.discount.months + 1) +
                ' it is ' + after + ' a month.') +
        '</p>' : '') +
        '<p class="os-note"><b>' +
          (KO ? '아직 결제되지 않았습니다.' : 'Nothing has been charged yet.') +
        '</b> ' +
          (KO ? '카드나 계좌에서 빠져나간 금액이 없습니다. 아래 순서로 진행됩니다.'
              : 'No money has moved. This is what happens next.') +
        '</p>' +
        '<ol class="os-steps">' + steps.map(function (s) { return '<li>' + s + '</li>'; }).join('') + '</ol>' +
        ((res.route === 'proposal' && res.blockers && res.blockers.length)
          ? '<p class="os-note">' +
            (KO ? '이 주문은 서면 주문서로 진행됩니다 — ' : 'This order continues as a written order — ') +
            res.blockers.map(function (b) {
              /* 서버는 {ko, en} 짝으로 보냅니다 */
              return String((b && (KO ? b.ko : b.en)) || '').replace(/[<>]/g, '');
            }).join(' · ') + '</p>'
          : '') +
        '<p class="os-note">' +
          (res.confirmation
            ? (KO ? '같은 내용을 이메일로 보내 드렸습니다. 1분 안에 오지 않으면 스팸함을 확인해 주십시오. '
                  : 'A copy is in your inbox. If it is not there within a minute, look in spam. ')
            : '') +
          (KO ? '주문번호 <b>' + no + '</b> 를 말씀하시면 바로 찾을 수 있습니다. ' +
                '이 화면을 닫으셔도 <a class="lnk" href="./order-status.html?no=' + no + '">주문 조회</a>' +
                '에서 주문번호와 이메일로 다시 여실 수 있습니다. ' +
                '취소하시려면 hello@saleringo.com 으로 주문번호와 함께 “취소”라고만 보내 주시면 됩니다.'
              : 'Quote <b>' + no + '</b> and we find you at once. ' +
                'You can close this and reopen it any time at ' +
                '<a class="lnk" href="./order-status.html?no=' + no + '">order status</a>' +
                ' with the number and your email. ' +
                'To cancel, email hello@saleringo.com with the number and the word cancel.') +
        '</p>' +
      '</div>';
    try { sessionStorage.removeItem(KEY); } catch (e) {}
    var box = form.querySelector('.ordersent');
    if (box) { box.focus(); box.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
    var bar = document.querySelector('.paybar');
    if (bar) bar.remove();
  }

  /* 실패는 들려야 합니다. 예전에는 제출 버튼이 비활성화되면서 포커스가
     사라지고, 오류 상자에는 role 도 aria-live 도 없어서 스크린리더로는
     아무 일도 일어나지 않은 것과 같았습니다. */
  function fail(msg) {
    var slot = $('[data-order-error]');
    if (!slot) return;
    slot.setAttribute('role', 'alert');
    slot.setAttribute('tabindex', '-1');
    /* 이 배너는 이번 시도에 대한 것입니다. 다음 시도에서는 지워져야 합니다. */
    slot.setAttribute('data-transient', '1');
    slot.textContent = msg;
    slot.hidden = false;
    slot.scrollIntoView({ behavior: 'smooth', block: 'center' });
    try { slot.focus({ preventScroll: true }); } catch (e) {}
  }

  /* 한 번 뜬 실패 배너가 사라지지 않아, 다음 시도에서 칸마다 오류가 붙는
     동안에도 "전송에 실패했습니다. 잠시 뒤 다시 눌러 주세요" 가 위에 남아
     있었습니다. 두 문구가 서로 다른 말을 하니 어느 쪽을 따라야 할지
     알 수 없습니다. 접수를 못 받는 상태나 금액을 못 읽은 상태를 알리는
     배너는 계속 남아야 하므로, 이번 시도 때문에 뜬 것만 지웁니다. */
  function clearFail() {
    var slot = $('[data-order-error]');
    if (!slot || slot.getAttribute('data-transient') !== '1') return;
    slot.hidden = true;
    slot.textContent = '';
    slot.removeAttribute('data-transient');
    slot.removeAttribute('role');
  }

  /* 요금표에도 페이지와 같은 판 번호를 붙입니다.
     사이트의 모든 자산에는 ?v= 가 붙는데, 정작 돈의 유일한 출처인
     요금표만 그냥 부르고 있었습니다. 캐시가 한 시간이라, 새 코드가
     옛 요금표를 읽는 시간이 배포마다 한 시간씩 생겼습니다.
     실제로 그 사이 한국 구매자에게 "이 나라는 AI 전화가 안 됩니다"가
     떴습니다 — 옛 요금표에는 그 값이 아예 없었기 때문입니다.
     값이 아니라 금액이 어긋났다면 알아채지도 못했을 것입니다.
     판 번호는 이 파일을 불러온 <script> 태그에서 그대로 가져옵니다.
     따로 적어 두면 언젠가 한쪽만 올리게 됩니다. */
  function assetVer() {
    var me = document.currentScript;
    if (!me) {
      var all = document.querySelectorAll('script[src*="checkout.js"]');
      me = all[all.length - 1];
    }
    var m = me && me.src && me.src.match(/[?&]v=([^&]+)/);
    return m ? m[1] : '';
  }

  /* ── 이 거래를 화면에서 끝낼 수 있는가 ────────────────────────────── */
  /*
     예전에는 화면이 혼자 판단했습니다. 그래서 프랑스 구매자에게
     "AI 전화가 아직 지원되지 않습니다" 라고 안내하면서도 그 전화가 든
     Scale $599 를 그대로 주문할 수 있었고, VAT 번호가 없어도 리버스
     차지라고 적었으며, 독일 개인에게도 세금 0 으로 팔았습니다.

     이제 판정은 서버가 합니다. 화면은 무엇을 골랐는지만 보내고,
     돌아온 답 그대로 씁니다. 판단이 두 곳에 있으면 언젠가 갈라집니다.
  */
  var VERDICT = null;
  var verdictTimer = null;

  function askServer() {
    var sel = selection();
    if (!sel.country || !sel.plan) return;
    var bt = ($('[name="buyerType"]') || {}).value || '';
    var biz = ($('[name="bizNo"]') || {}).value || '';

    fetch('/api/quote', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        country: sel.country, plan: sel.plan, method: sel.method,
        buyerType: bt, bizNo: biz,
        voiceMinutes: sel.voiceMinutes, alimtalk: sel.alimtalk
      })
    }).then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) {
        if (!j || j.error) { quoteQuiet(); return; }
        VERDICT = j;
        paintVerdict();
      }).catch(function () { quoteQuiet(); });
  }

  /* 견적 서버가 잠시 조용할 때. 예전에는 아무 말 없이 넘어갔고,
     서면 주문 경로의 구매자가 그 사실을 모른 채 접수를 눌렀습니다.
     판정을 지어내지 않고, 확인이 접수 뒤에 온다는 사실만 적습니다. */
  function quoteQuiet() {
    if (VERDICT) return;               /* 이미 받은 판정이 있으면 그대로 */
    var slot = document.querySelector('[data-commerce-verdict]');
    if (!slot) return;
    slot.hidden = false;
    slot.textContent = KO
      ? '세금과 접수 가능 여부는 접수 뒤 담당자가 확인합니다 — 주문 조회 페이지에서 보실 수 있습니다.'
      : 'Tax and availability are settled after you order — you can follow it on the order status page.';
  }

  /* 고르는 중에 매번 묻지 않습니다. 손을 멈추면 그때 한 번 묻습니다. */
  function askServerSoon() {
    clearTimeout(verdictTimer);
    verdictTimer = setTimeout(askServer, 350);
  }

  function paintVerdict() {
    var box = document.querySelector('[data-commerce-verdict]');
    var com = VERDICT && VERDICT.commerce;
    if (!box || !com) return;
    var bt = ($('[name="buyerType"]') || {}).value || '';
    if (!bt) {
      box.innerHTML = '<b>' + (KO ? '구매 주체를 고르시면 세금과 온라인 주문 가능 여부가 정해집니다.'
                                 : 'Pick \u201cBuying as\u201d and we settle tax and online ordering.') + '</b>';
      box.hidden = false;
      return;
    }

    var lines = [];
    var treat = com.taxTreatment;
    lines.push('<b>' + (T.taxTreat[treat] || T.taxTreat.review) + '</b>');

    var bl = com.blockers || [];
    if (bl.length) {
      bl.forEach(function (b) {
        lines.push('<span class="cotax-block">' + (KO ? b.ko : b.en) + '</span>');
      });
    }
    box.innerHTML = lines.join('');
    box.hidden = false;

    /* 화면에서 확정할 수 없는 거래면, 버튼이 무엇을 하는지 그대로 씁니다.
       "주문 접수하기" 를 눌렀는데 서면 검토로 넘어가면 속은 기분이 듭니다. */
    /* 아직 안 채운 칸(구매자 유형·세금번호) 때문에 서버가 "판정 보류"를
       돌려준 것은 서면 경로가 아니라 "마저 채우라"는 뜻입니다. 그때 버튼을
       「서면 주문 요청」으로 바꾸면 첫 방문자는 온라인 주문이 없다고 읽습니다.
       회선 없음처럼 화면에서 풀 수 없는 막힘일 때만 바꿉니다. */
    var hard = bl.some(function (b) { return !/_required$/.test(b.code || ''); });
    var btn = $('[data-submit]');
    if (btn && !btn.getAttribute('data-proposal')) {
      var proposal = !com.orderable && hard;
      var label = proposal ? T.proposalCta : (btn._orig || btn.textContent);
      if (!btn._orig) btn._orig = btn.innerHTML;
      if (proposal) {
        btn.innerHTML = label;
        btn.setAttribute('data-route', 'proposal');
      } else {
        btn.innerHTML = btn._orig;
        btn.removeAttribute('data-route');
      }
    }
    /* 결제 막대에는 단추가 없고 「Every month · 금액」뿐입니다. 제안
       경로에서도 금액은 참이지만, 이 주문이 화면에서 끝나지 않는다는
       사실은 막대도 말해야 합니다. */
    var barLbl = document.querySelector('.paybar .lbl');
    if (barLbl) {
      if (!barLbl._orig) barLbl._orig = barLbl.textContent;
      barLbl.textContent = (com.orderable || !hard) ? barLbl._orig : T.proposalCta;
    }
  }

  /* ── 시작 ──────────────────────────────────────────────────────────── */
  var PRICING_URL = '/assets/data/pricing.json' +
    (assetVer() ? '?v=' + encodeURIComponent(assetVer()) : '');

  fetch(PRICING_URL).then(function (r) { return r.json(); }).then(function (j) {
    P = j;
    restore();
    var wanted = new URLSearchParams(location.search).get('plan');
    if (wanted) {
      var r = $('input[name="plan"][value="' + wanted.replace(/[^a-z]/g, '') + '"]');
      if (r) r.checked = true;
    }
    if (!$('input[name="plan"]:checked')) {
      var g = $('input[name="plan"][value="grow"]'); if (g) g.checked = true;
    }
    /* 가격 페이지에서 실어 보낸 구성은 초안과 기본값을 이긴다 — 여기서, 초안 복원 뒤에 */
    restoreFromBuilder();
    if (!$('input[name="method"]:checked')) {
      var m = $('input[name="method"]'); if (m) m.checked = true;
    }
    /* 나라의 기본값은 페이지의 언어입니다. 한국어 페이지를 보고 있는
       사람은 대개 한국 사업자이고, 영어 페이지를 보고 있는 사람은 대개
       아닙니다. 틀렸으면 첫 칸에서 바로 바꾸면 됩니다. */
    var cty = $('[name="country"]');
    if (cty && !cty.value) cty.value = (LANG === 'ko') ? 'KR' : 'US';
    syncCountry(); paint(); gate();
  }).catch(function () {
    /* 금액을 볼 수 없는 사람에게서 주문을 받지 않습니다. 요약 카드가 빈
       채로 접수되면, 나중에 청구서를 보고 처음 금액을 알게 됩니다. */
    var slot = $('[data-order-error]');
    if (slot) {
      slot.setAttribute('role', 'alert');
      slot.textContent = T.noPrice;
      slot.hidden = false;
      form.insertBefore(slot, form.firstChild);
    }
    var b = $('[data-submit]');
    if (b) { b.disabled = true; b.setAttribute('aria-disabled', 'true'); }
  });

  /* 접수를 못 받는 상태라는 걸 페이지는 뜨자마자 압니다. 그걸 알면서
     다 채우게 두었다가 마지막에 알리는 것은 시간을 뺏는 일입니다.
     알자마자 위에 띄우고, 버튼도 그렇게 바꿉니다. */
  fetch('/api/order').then(function (r) { return r.json(); }).then(function (j) {
    READY = j;
    if (j && j.ready) return;
    offlineMode();
  }).catch(function () { offlineMode(); });

  /* 접수를 받을 수 없으면 주문 버튼을 **없앱니다**.
     예전에는 "온라인 주문이 열려 있지 않습니다" 라고 적어 두고 바로 아래에
     살아 있는 「주문 접수하기」 버튼을 함께 보여 줬습니다. 그 버튼은
     반드시 실패하는 요청을 보냈고, 구매자는 자기가 뭘 잘못했는지 몰랐습니다.
     한 화면이 서로 반대되는 두 가지를 말하면, 사람은 버튼을 믿습니다. */
  /* 가격 페이지의 「내 한 달 만들기」가 실어 보낸 구성.
     사용자가 이미 만진 필드는 이기지 않습니다 — 프리필은 빈칸에만. */
  function restoreFromBuilder() {
    if (!window.srCarry) return;
    var c = window.srCarry.read() || {};
    if (!c.qbPlan && !c.qbCountry) return;
    /* 「이 구성 그대로 주문서로」를 누른 것은 명시적 선택이므로 주문서의
       기본값(미국·Grow)을 이깁니다. 한 번 적용하면 키를 지워, 나중에 손으로
       바꾼 것을 새로고침이 되돌리지 않게 합니다. */
    if (c.qbCountry) {
      var sel = $('[name="country"]');
      if (sel) { sel.value = c.qbCountry; sel.dispatchEvent(new Event('change', { bubbles: true })); }
      var sv = $('[name="serviceCountry"]');
      if (sv) sv.value = c.qbCountry;
    }
    if (c.qbPlan) {
      var r = form.querySelector('[name="plan"][value="' + c.qbPlan + '"]');
      if (r) { r.checked = true; r.dispatchEvent(new Event('change', { bubbles: true })); }
    }
    ['qbVoiceMinutes', 'qbAlimtalk'].forEach(function (k) {
      var name = k === 'qbVoiceMinutes' ? 'voiceMinutes' : 'alimtalk';
      var el = $('[name="' + name + '"]');
      if (el && c[k]) { el.value = c[k]; el.dispatchEvent(new Event('input', { bubbles: true })); }
    });
    window.srCarry.write({ qbPlan: '', qbCountry: '', qbVoiceMinutes: '', qbAlimtalk: '' });
    snapshot();
  }

  function carryDraft() {
    if (!window.srCarry) return;
    var take = ['company', 'country', 'plan', 'email', 'contact'];
    var parts = [];
    take.forEach(function (k) {
      var el = k === 'plan' ? form.querySelector('[name="plan"]:checked')
                            : $('[name="' + k + '"]');
      var v = el && (el.value || '').trim();
      if (v) parts.push(k + ': ' + v);
    });
    if (parts.length) {
      window.srCarry.write({ orderDraft: parts.join(' · '), orderDraftLang: LANG });
    }
  }

  function offlineMode() {
    var slot = $('[data-order-error]');
    if (slot) {
      slot.setAttribute('role', 'status');
      slot.textContent = T.offline;
      slot.hidden = false;
      form.insertBefore(slot, form.firstChild);
    }

    var btn = $('[data-submit]');
    if (btn && btn.parentNode) {
      var a = document.createElement('a');
      a.className = btn.className;
      a.setAttribute('data-proposal', '1');
      a.href = './get-started.html#request';
      a.textContent = T.proposalCta;
      /* 「같은 내용으로 만들어 드린다」를 사실로: 문의 폼의 메모 칸에
         보이게 옮겨 적힐 요약을 싣습니다. site.js 의 srCarry 가 받습니다. */
      a.addEventListener('click', function () { carryDraft(); });
      btn.parentNode.replaceChild(a, btn);
    }

    /* 접수가 닫혔으면 금액 막대도 접습니다. */
    var pbar = document.querySelector('.paybar');
    if (pbar) pbar.style.display = 'none';

    /* 결제 바의 버튼도 같은 것으로 바꿉니다. 화면 아래에 고정된 버튼만
       살아 있으면 위에서 없앤 의미가 없습니다. */
    var barBtn = document.querySelector('.paybar [data-submit], .paybar button[type="submit"]');
    if (barBtn && barBtn.parentNode) barBtn.parentNode.removeChild(barBtn);

    /* 엔터로 제출되는 길도 막습니다. */
    form.setAttribute('data-offline', '1');
  }

  form.addEventListener('input', function (e) {
    var el = e.target;
    /* 하이픈을 저절로 넣는 것은 한국 번호에서만 맞습니다. VAT 번호에
       하이픈을 끼워 넣으면 그건 다른 번호가 됩니다. */
    if (el.name === 'bizNo') {
      var cc = countryOf(selection().country);
      if (cc && cc.taxIdCheck === 'kr') el.value = fmtBiz(el.value);
    }
    if (el.name === 'phone') {
      var pc = countryOf(selection().country);
      if (pc && pc.code === 'KR') el.value = fmtPhone(el.value);
    }
    /* 세금 처리는 구매 주체와 세금번호로 갈립니다. 둘 중 하나가 바뀌면
       서버에 다시 물어봐야 화면이 사실을 말합니다. */
    if (el.name === 'buyerType' || el.name === 'bizNo') askServerSoon();
    if (el.closest('.fld') && el.closest('.fld').classList.contains('has-err')) checkField(el);
    syncCountry(); paint(); gate(); snapshot();
  });
  form.addEventListener('change', function () { syncCountry(); paint(); gate(); snapshot(); });
  form.addEventListener('blur', function (e) {
    if (e.target.name && e.target.tagName !== 'BUTTON') checkField(e.target);
  }, true);

  /* 담당자 이메일과 같게 쓰겠다는 체크 */
  var same = $('[data-same-email]');
  if (same) same.addEventListener('change', function () {
    var tax = $('[name="taxEmail"]');
    if (!tax) return;
    tax.disabled = same.checked;
    if (same.checked) { tax.value = ($('[name="email"]') || {}).value || ''; checkField(tax); }
    snapshot();
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    /* 접수를 받을 수 없는 상태면 아예 보내지 않습니다. */
    if (form.getAttribute('data-offline') === '1') return;
    var btn = $('[data-submit]');
    /* 지난 시도의 실패 배너를 먼저 지웁니다. 남겨 두면 이번 시도의
       칸 오류와 나란히 서서 서로 다른 말을 합니다. */
    clearFail();

    var firstBad = null;
    $$('input,select,textarea').forEach(function (el) {
      if (!el.name || el.disabled) return;
      if (el.type === 'checkbox') {
        if (el.required && !el.checked) {
          setErr(el, T.agreeBad);
          if (!firstBad) firstBad = el;
        } else if (el.required) setErr(el, '');
        return;
      }
      if (!checkField(el) && !firstBad) firstBad = el;
    });
    if (firstBad) {
      (firstBad.closest('.fld') || firstBad.closest('.agree') || firstBad)
        .scrollIntoView({ behavior: 'smooth', block: 'center' });
      if (firstBad.focus) firstBad.focus({ preventScroll: true });
      return;
    }

    if (btn) { btn._label = btn.innerHTML; btn.disabled = true; btn.textContent = T.sending; }

    var sel = selection();
    var payload = {
      plan: sel.plan, method: sel.method, country: sel.country,
      voiceMinutes: sel.voiceMinutes, alimtalk: sel.alimtalk,
      lang: LANG,
      idempotencyKey: idemKey()
    };
    $$('input,select,textarea').forEach(function (el) {
      if (!el.name || el.disabled) return;
      if (el.name === 'plan' || el.name === 'method') return;
      /* 숨은 함정 칸은 절대 보내지 않습니다. 비밀번호 관리자가 이 칸을
         채우는 일이 실제로 있고, 그러면 서버는 봇으로 보고 주문을 버리는데
         화면은 "접수되었습니다"라고 말합니다. 사람이 그 함정에 걸릴 길을
         아예 없앱니다. 직접 POST 하는 봇에는 그대로 작동합니다. */
      if (el.name === 'company_website_hp') return;
      if (el.type === 'checkbox') { if (el.checked) payload[el.name] = true; return; }
      if (el.value) payload[el.name] = el.value;
    });
    if (same && same.checked) payload.taxEmail = payload.email;

    fetch('/api/order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        return { ok: r.ok, status: r.status, body: j };
      });
    }).then(function (out) {
      /* 서버가 받았다고 답한 뒤에는, 화면을 그리다 무엇이 잘못되더라도
         "실패했다"고 말하지 않습니다. 주문은 이미 접수되었고 메일도 나갔기
         때문입니다. 그 상태에서 실패 문구를 띄우면 구매자는 다시 누르고,
         같은 주문이 두 번 들어갑니다. 그래서 성공 경로를 아래 catch 밖으로
         꺼내고, 화면 조립이 깨지면 최소한 주문번호만이라도 남깁니다. */
      if (out.ok && out.body && out.body.ok) {
        try {
          receipt(out.body);
        } catch (e) {
          var no = String(out.body.orderNo || '').replace(/[^A-Z0-9-]/g, '').slice(0, 20);
          form.innerHTML = '<div class="ordersent" role="status" tabindex="-1"><b>' +
            (KO ? '주문이 접수되었습니다.' : 'Your order is in.') + '</b>' +
            (no ? '<code class="orderno">' + no + '</code>' : '') +
            '<p class="os-note"><b>' +
            (KO ? '아직 결제되지 않았습니다.' : 'Nothing has been charged yet.') + '</b> ' +
            (KO ? '영업일 하루 안에 담당자가 연락드립니다. 이 번호를 말씀해 주십시오.'
                : 'A person will confirm within one business day. Quote this number.') +
            '</p></div>';
          try { sessionStorage.removeItem(KEY); } catch (e2) {}
          var pb = document.querySelector('.paybar');
          if (pb) pb.remove();
        }
        return;
      }
      if (btn) { btn.disabled = false; btn.innerHTML = btn._label; }
      if (out.status === 503) { offlineMode(); return fail(T.failDest); }
      if (out.body && out.body.fields && out.body.fields.length) {
        /* 서버는 세금 번호를 taxId 라고 부릅니다. 화면의 칸은 bizNo 입니다. */
        var fname = out.body.fields[0] === 'taxId' ? 'bizNo' : out.body.fields[0];
        var el = $('[name="' + fname + '"]');
        if (el) {
          setErr(el, el.name === 'bizNo' ? T.bizBad
                   : el.type === 'checkbox' ? T.agreeBad : T.required);
          (el.closest('.fld') || el).scrollIntoView({ behavior: 'smooth', block: 'center' });
          return;
        }
      }
      fail(T.failNet);
    }).catch(function () {
      if (btn) { btn.disabled = false; btn.innerHTML = btn._label; }
      fail(T.failNet);
    });
  });
})();
