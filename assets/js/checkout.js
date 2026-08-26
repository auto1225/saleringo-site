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
      monthly: '월 이용료', vat: '부가세 10%', total: '매월 결제 금액',
      firstLabel: '첫 달은 개시일 기준 일할',
      firstIf: '오늘 개시한다면 %s (%d/%d일)',
      notNow: '이 버튼은 접수만 합니다. 지금 청구되는 금액은 없습니다.',
      usage: '사용량 예상 — 청구에 포함되지 않습니다',
      perMonth: '/월', from: '부터',
      estimateNote: '쓰신 만큼 다음 달에 정산합니다.',
      overage: '월 %s건을 넘기면 %s건당 %s이 붙습니다. 한도를 미리 걸어 두실 수 있습니다.',
      required: '필수 항목입니다',
      bizBad: '사업자등록번호가 올바르지 않습니다. 10자리를 다시 확인해 주세요.',
      emailBad: '이메일 형식이 올바르지 않습니다.',
      phoneBad: '전화번호를 다시 확인해 주세요.',
      agreeBad: '필수 동의 항목을 확인해 주세요.',
      sending: '접수하는 중…',
      failNet: '전송에 실패했습니다. 잠시 뒤 다시 눌러 주시거나, hello@saleringo.com 으로 보내 주십시오.',
      failDest: '지금은 온라인 접수를 받을 수 없습니다. hello@saleringo.com 으로 보내 주시면 사람이 바로 처리해 드립니다.',
      offline: '지금은 온라인 주문 접수가 열려 있지 않습니다. 아래를 채워 보내는 대신 hello@saleringo.com 으로 연락 주시면 사람이 바로 처리해 드립니다.',
      noPrice: '요금표를 불러오지 못했습니다. 금액을 확인하실 수 없는 상태로 주문을 받지 않겠습니다. 새로고침해 보시고, 계속 이러면 hello@saleringo.com 으로 알려 주십시오.'
    },
    en: {
      monthly: 'Monthly', vat: 'VAT 10%', total: 'Every month',
      firstLabel: 'First month prorated from the start date',
      firstIf: 'Starting today that would be %s (%d/%d days)',
      notNow: 'This button records the order. Nothing is charged now.',
      usage: 'Usage estimate — not part of the charge',
      perMonth: '/mo', from: ' and up',
      estimateNote: 'Settled next month on what you actually use.',
      overage: 'Past %s conversations a month, %s more cost %s per block. You can cap it.',
      required: 'Required',
      bizBad: 'That registration number does not check out. Please look at the 10 digits again.',
      emailBad: 'That email address does not look right.',
      phoneBad: 'Please check the phone number.',
      agreeBad: 'Please tick the required agreements.',
      sending: 'Sending…',
      failNet: 'That did not go through. Try again in a moment, or send it to hello@saleringo.com.',
      failDest: 'Online orders are not being taken right now. Send it to hello@saleringo.com and a person will pick it up.',
      offline: 'Online ordering is not open at the moment. Rather than filling this in, write to hello@saleringo.com and a person will pick it up.',
      noPrice: 'The price list did not load. We will not take an order while you cannot see the amount. Try reloading; if it keeps happening, tell us at hello@saleringo.com.'
    }
  }[LANG];

  function $(s, r) { return (r || form).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || form).querySelectorAll(s)); }
  function won(n) { return new Intl.NumberFormat('ko-KR').format(Math.round(n)) + (KO ? '원' : ' KRW'); }

  /* ── 저장과 복구 ───────────────────────────────────────────────────── */
  /* 동의는 저장하지도 복원하지도 않습니다. 새로고침 한 번에 동의가
     저절로 다시 체크되어 있으면, 그건 그 사람이 동의한 것이 아닙니다. */
  function isConsent(el) {
    return el.type === 'checkbox' && /^agree/.test(el.name || '');
  }
  function snapshot() {
    var o = {};
    $$('input,select,textarea').forEach(function (el) {
      if (!el.name || el.name === 'company_website_hp') return;
      if (isConsent(el)) return;
      o[el.name] = (el.type === 'checkbox' || el.type === 'radio')
        ? (el.checked ? el.value || true : undefined) : el.value;
      if (o[el.name] === undefined) delete o[el.name];
    });
    try { sessionStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {}
  }
  function restore() {
    var o;
    try { o = JSON.parse(sessionStorage.getItem(KEY) || '{}'); } catch (e) { return; }
    $$('input,select,textarea').forEach(function (el) {
      if (!el.name || !(el.name in o) || isConsent(el)) return;
      if (el.type === 'checkbox') el.checked = true;
      else if (el.type === 'radio') { if (el.value === o[el.name]) el.checked = true; }
      else el.value = o[el.name];
    });
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
    var n = v.replace(/[^0-9]/g, '').slice(0, 11);
    var head = n.slice(0, 2) === '02' ? 2 : 3;
    if (n.length <= head) return n;
    var rest = n.length - head;
    /* 다 치기 전에는 하이픈을 하나만 넣습니다. 끊을 위치는 마지막 네 자리가
       나와야 정해지는데, 그 전에 미리 끊으면 치는 중에 숫자가 이리저리
       옮겨 다녀서 자기가 잘못 친 줄 알게 됩니다. */
    if (rest < 7) return n.slice(0, head) + '-' + n.slice(head);
    var mid = rest >= 8 ? 4 : 3;
    return n.slice(0, head) + '-' + n.slice(head, head + mid) + '-' + n.slice(head + mid);
  }
  function bizValid(raw) {
    var n = String(raw || '').replace(/[^0-9]/g, '');
    if (n.length !== 10) return false;
    var w = [1, 3, 7, 1, 3, 7, 1, 3, 5], sum = 0;
    for (var i = 0; i < 9; i++) sum += Number(n[i]) * w[i];
    sum += Math.floor((Number(n[8]) * 5) / 10);
    return (10 - (sum % 10)) % 10 === Number(n[9]);
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
    if (el.hasAttribute('required') && !v && el.type !== 'checkbox') return setErr(el, T.required);
    if (el.name === 'bizNo' && v) return setErr(el, bizValid(v) ? '' : T.bizBad);
    if (el.type === 'email' && v) return setErr(el, emailOk(v) ? '' : T.emailBad);
    if (el.name === 'phone' && v) {
      var d = v.replace(/[^0-9]/g, '');
      return setErr(el, d.length >= 9 && d.length <= 11 ? '' : T.phoneBad);
    }
    return setErr(el, '');
  }

  /* ── 금액 ──────────────────────────────────────────────────────────── */
  function selection() {
    var plan = $('input[name="plan"]:checked');
    var method = $('input[name="method"]:checked');
    return {
      plan: plan ? plan.value : '',
      method: method ? method.value : '',
      voiceMinutes: Number(($('[name="voiceMinutes"]') || {}).value) || 0,
      alimtalk: Number(($('[name="alimtalk"]') || {}).value) || 0
    };
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
    if (!plan) return null;
    var pr = proration(new Date());
    var est = [];
    P.usage.forEach(function (u) {
      if (u.planRequires === 'voice' && !plan.voice) return;
      if (u.planRequires === 'messenger' && !plan.messenger) return;
      var qty = Math.max(0, Number(sel[u.id]) || 0);
      if (!qty) return;
      est.push({ label: u.name[LANG], qty: qty, unit: u.unitPrice,
                 amount: Math.round(qty * u.unitPrice), from: !!u.from });
    });
    var firstNet = Math.round(plan.monthly * pr.factor);
    return {
      plan: plan, pr: pr, est: est,
      monthNet: plan.monthly, monthVat: Math.round(plan.monthly * P.vatRate),
      firstNet: firstNet, firstVat: Math.round(firstNet * P.vatRate)
    };
  }

  function paint() {
    var box = document.querySelector('[data-summary]');
    if (!box || !P) return;
    var q = quote();
    if (!q) { box.innerHTML = ''; return; }
    var r = [];
    r.push('<div class="sm-plan"><b>' + q.plan.name[LANG] + '</b><span>' +
      q.plan.channels[LANG] + '</span></div>');
    r.push('<div class="sm-row"><span>' + T.monthly + '</span><b>' + won(q.monthNet) + '</b></div>');
    r.push('<div class="sm-row"><span>' + T.vat + '</span><b>' + won(q.monthVat) + '</b></div>');
    /* 매달 같은 금액이 가장 큰 글씨로 옵니다. 날짜에 따라 변하지 않는
       유일한 숫자이고, 구매자가 결재에 올리는 숫자이기도 합니다. */
    r.push('<div class="sm-total"><span>' + T.total + '</span><b>' +
      won(q.monthNet + q.monthVat) + '</b></div>');
    r.push('<p class="sm-notnow">' + T.notNow + '</p>');
    r.push('<div class="sm-first"><p>' + T.firstLabel + '</p><p class="sm-note">' +
      T.firstIf.replace('%s', won(q.firstNet + q.firstVat))
               .replace('%d', q.pr.remaining).replace('%d', q.pr.daysInMonth) + '</p></div>');
    if (q.est.length) {
      r.push('<div class="sm-est"><p>' + T.usage + '</p>' +
        q.est.map(function (e) {
          return '<div class="sm-row"><span>' + e.label + ' ' +
            new Intl.NumberFormat('ko-KR').format(e.qty) + '</span><b>' +
            won(e.amount) + (e.from ? T.from : '') + '</b></div>';
        }).join('') + '<p class="sm-note">' + T.estimateNote + '</p></div>');
    }
    if (P.overage) {
      r.push('<p class="sm-note sm-over">' + T.overage
        .replace('%s', new Intl.NumberFormat('ko-KR').format(q.plan.conversations))
        .replace('%s', new Intl.NumberFormat('ko-KR').format(P.overage.block))
        .replace('%s', won(P.overage.blockPrice)) + '</p>');
    }
    box.innerHTML = r.join('');
    var bar = document.querySelector('[data-paybar-total]');
    if (bar) bar.textContent = won(q.monthNet + q.monthVat);
  }

  /* 전화 요금제가 아닐 때 통화 예상 칸을 숨긴다. 고를 수 없는 것을
     띄워 두면 고를 수 있는 줄 알고 채우게 됩니다. */
  function syncVoice() {
    var sel = selection();
    var plan = P ? P.plans.filter(function (p) { return p.id === sel.plan; })[0] : null;
    var row = document.querySelector('[data-voice-row]');
    if (row) row.hidden = !(plan && plan.voice);
    var rec = document.querySelector('[data-recurring-agree]');
    if (rec) {
      var isCard = sel.method === 'card';
      rec.hidden = !isCard;
      var cb = rec.querySelector('input');
      if (cb) { cb.required = isCard; if (!isCard) cb.checked = false; }
    }
  }

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
    var monthly = q.monthly ? won(q.monthly.total) : '';
    var first = q.firstMonthIfToday ? won(q.firstMonthIfToday.total) : '';
    var steps = ko
      ? ['영업일 하루 안에 담당자가 확인 연락을 드립니다.',
         '우리 요금표와 영업시간을 받아 응대를 만들어 드립니다.',
         '만들어진 응대를 먼저 보시고, 그때 결제 안내를 보내 드립니다.']
      : ['A person confirms within one business day.',
         'We build your answering from your price list and hours.',
         'You read it first; the payment step comes after that.'];
    form.innerHTML =
      '<div class="ordersent" role="status" tabindex="-1">' +
        '<b>' + (ko ? '주문이 접수되었습니다.' : 'Your order is in.') + '</b>' +
        '<code class="orderno">' + no + '</code>' +
        '<p class="os-money">' +
          (ko ? '매월 ' : 'Every month ') + '<b>' + monthly + '</b>' +
          (first ? (ko ? ' · 첫 달은 개시일 기준 일할(오늘이면 ' : ' · first month prorated (today, ')
                 + first + ')' : '') +
        '</p>' +
        '<p class="os-note"><b>' +
          (ko ? '아직 결제되지 않았습니다.' : 'Nothing has been charged yet.') +
        '</b> ' +
          (ko ? '카드나 계좌에서 빠져나간 금액이 없습니다. 아래 순서로 진행됩니다.'
              : 'No money has moved. This is what happens next.') +
        '</p>' +
        '<ol class="os-steps">' + steps.map(function (s) { return '<li>' + s + '</li>'; }).join('') + '</ol>' +
        '<p class="os-note">' +
          (res.confirmation
            ? (ko ? '같은 내용을 이메일로 보내 드렸습니다. 1분 안에 오지 않으면 스팸함을 확인해 주십시오. '
                  : 'A copy is in your inbox. If it is not there within a minute, look in spam. ')
            : '') +
          (ko ? '주문번호 <b>' + no + '</b> 를 말씀하시면 바로 찾을 수 있습니다. ' +
                '취소하시려면 hello@saleringo.com 으로 주문번호와 함께 “취소”라고만 보내 주시면 됩니다.'
              : 'Quote <b>' + no + '</b> and we find you at once. ' +
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
    slot.textContent = msg;
    slot.hidden = false;
    slot.scrollIntoView({ behavior: 'smooth', block: 'center' });
    try { slot.focus({ preventScroll: true }); } catch (e) {}
  }

  /* ── 시작 ──────────────────────────────────────────────────────────── */
  fetch('/assets/data/pricing.json').then(function (r) { return r.json(); }).then(function (j) {
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
    if (!$('input[name="method"]:checked')) {
      var m = $('input[name="method"]'); if (m) m.checked = true;
    }
    syncVoice(); paint(); gate();
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
    if (!j || j.ready) return;
    var slot = $('[data-order-error]');
    if (slot) {
      slot.setAttribute('role', 'status');
      slot.textContent = T.offline;
      slot.hidden = false;
      form.insertBefore(slot, form.firstChild);
    }
    var b = $('[data-submit]');
    if (b) b.setAttribute('data-fallback', '1');
  }).catch(function () {});

  form.addEventListener('input', function (e) {
    var el = e.target;
    if (el.name === 'bizNo') el.value = fmtBiz(el.value);
    if (el.name === 'phone') el.value = fmtPhone(el.value);
    if (el.closest('.fld') && el.closest('.fld').classList.contains('has-err')) checkField(el);
    syncVoice(); paint(); gate(); snapshot();
  });
  form.addEventListener('change', function () { syncVoice(); paint(); gate(); snapshot(); });
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
    var btn = $('[data-submit]');

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
      plan: sel.plan, method: sel.method,
      voiceMinutes: sel.voiceMinutes, alimtalk: sel.alimtalk,
      lang: LANG,
      idempotencyKey: (form._idem = form._idem ||
        (Date.now().toString(36) + Math.random().toString(36).slice(2, 10)))
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
      if (out.ok && out.body.ok) return receipt(out.body);
      if (btn) { btn.disabled = false; btn.innerHTML = btn._label; }
      if (out.status === 503) return fail(T.failDest);
      if (out.body && out.body.fields && out.body.fields.length) {
        var el = $('[name="' + out.body.fields[0] + '"]');
        if (el) {
          setErr(el, el.name === 'bizNo' ? T.bizBad : T.required);
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
