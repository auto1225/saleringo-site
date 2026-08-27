/* 접수한 주문을 다시 열어 본다.
 *
 * 예전에는 주문 성공 화면이 새로고침 한 번에 사라졌고, 그 번호를 다시
 * 조회할 곳이 사이트 어디에도 없었습니다. 확인 메일이 안 왔거나 지운
 * 사람은 자기가 무엇을 얼마에 주문했는지 확인할 방법이 없었습니다.
 */
(function () {
  'use strict';

  var form = document.querySelector('[data-order-lookup]');
  if (!form) return;

  var LANG = (document.documentElement.lang || 'ko').slice(0, 2) === 'en' ? 'en' : 'ko';
  var KO = LANG === 'ko';

  var T = KO
    ? {
        badNo: '주문번호를 SO-20260827-1001 형태로 넣어 주세요.',
        badEmail: '접수하실 때 쓰신 이메일을 넣어 주세요.',
        notFound:
          '그 번호와 이메일로 접수된 주문을 찾지 못했습니다. 둘 다 접수하실 때 쓰신 것과 같은지 확인해 주세요. ' +
          '그래도 안 되면 hello@saleringo.com 으로 번호와 함께 보내 주십시오.',
        busy: '조회가 잠시 몰렸습니다. 잠시 뒤 다시 눌러 주세요.',
        failed: '조회하지 못했습니다. 잠시 뒤 다시 시도해 주시거나 hello@saleringo.com 으로 연락 주세요.',
        looking: '찾는 중…',
        cta: '주문 찾기',
        heading: '접수 내용',
        order: '주문번호',
        company: '구매 주체',
        country: '청구 국가',
        plan: '요금제',
        monthly: '매월 결제 금액',
        after: '할인 종료 후',
        first: '첫 달(개시일 기준 일할)',
        tax: '세금 처리',
        received: '접수 시각',
        notCharged:
          '아직 결제되지 않았습니다. 계약은 서면 주문서에 양측이 서명한 때 성립하며, 그 전까지는 어떤 금액도 청구되지 않습니다.',
        taxTreat: {
          vat_charged: '부가세 10% 포함해 청구 · 전자세금계산서 발행',
          reverse: '대리납부(리버스 차지)',
          none: '세금 없음 (해당 국가에 세무 등록 없음)',
          review: '세금 별도 · 구매 법인 검증 후 확정'
        },
        steps: {
          received: ['주문 접수', '주문서를 받았습니다. 청약 단계이며 계약도 결제도 아직입니다.'],
          proposal_sent: ['제안서 발송', '구성과 금액을 담은 제안서를 보냈습니다.'],
          under_review: ['주문 검토', '구매 주체·청구 국가·세금 처리·국가 지원 여부를 확인하고 있습니다.'],
          contract_sent: ['서면 주문서 발송', '계약 주체·통화·세금·결제 일정·최종 금액이 적힌 주문서를 보냈습니다.'],
          contract_signed: ['계약 성립', '양측이 서명했습니다. 이 시점에 계약이 성립합니다.'],
          payment_pending: ['결제 대기', '서면 주문서의 일정에 따라 청구서가 발행됩니다.'],
          paid: ['결제 완료', '첫 청구가 처리되었습니다.'],
          active: ['서비스 개시', '응대가 동작하고 있습니다.'],
          cancelled: ['취소됨', '이 주문은 취소되었습니다.'],
          rejected: ['반려됨', '이 주문은 진행되지 않았습니다. 담당자가 사유를 안내드립니다.']
        }
      }
    : {
        badNo: 'Enter the order number as SO-20260827-1001.',
        badEmail: 'Enter the email you used when you ordered.',
        notFound:
          'No order matches that number and email. Check that both are the ones you used. ' +
          'If it still does not come up, email hello@saleringo.com with the number.',
        busy: 'Too many lookups just now. Try again in a moment.',
        failed: 'We could not look that up. Try again shortly, or email hello@saleringo.com.',
        looking: 'Looking…',
        cta: 'Find my order',
        heading: 'What was recorded',
        order: 'Order number',
        company: 'Buying organization',
        country: 'Billing country',
        plan: 'Plan',
        monthly: 'Charged every month',
        after: 'After the discount ends',
        first: 'First month (prorated)',
        tax: 'Tax treatment',
        received: 'Received',
        notCharged:
          'Nothing has been charged. The contract is formed when both sides sign the written order; until then nothing is taken.',
        taxTreat: {
          vat_charged: 'Korean VAT 10% added · tax invoice issued',
          reverse: 'Reverse charge',
          none: 'No tax added (no registration in your country)',
          review: 'Tax excluded · confirmed after we verify the buying entity'
        },
        steps: {
          received: ['Order received', 'We have your order form. This is an offer — not a contract, not a payment.'],
          proposal_sent: ['Proposal sent', 'We sent the scope and the price.'],
          under_review: ['Order review', 'We are confirming the buying entity, billing country, tax treatment, and eligibility.'],
          contract_sent: ['Written order sent', 'It states the seller, currency, tax, payment schedule, and final total.'],
          contract_signed: ['Contract formed', 'Both sides have signed. This is when the contract forms.'],
          payment_pending: ['Payment pending', 'The invoice follows the schedule in the written order.'],
          paid: ['Paid', 'The first invoice has been settled.'],
          active: ['Service running', 'Your answering is live.'],
          cancelled: ['Cancelled', 'This order was cancelled.'],
          rejected: ['Not proceeding', 'This order did not go ahead. A person will explain why.']
        }
      };

  /* 이 순서대로 흐릅니다. 취소·반려는 이 줄 밖에 있습니다. */
  var FLOW = [
    'received', 'proposal_sent', 'under_review', 'contract_sent',
    'contract_signed', 'payment_pending', 'paid', 'active'
  ];

  var errBox = form.querySelector('[data-lookup-error]');
  var result = document.querySelector('[data-lookup-result]');
  var btn = form.querySelector('[data-lookup-submit]');

  function fail(msg) {
    if (!errBox) return;
    errBox.textContent = msg;
    errBox.hidden = false;
  }
  function clearFail() {
    if (!errBox) return;
    errBox.hidden = true;
    errBox.textContent = '';
  }

  /* 서버에서 온 값은 무엇이든 여기를 지나서만 화면에 들어갑니다.
     주문번호·회사명·국가·요금제는 우리가 만든 값이지만, 회사명은
     구매자가 친 문자열입니다. "우리 데이터베이스에서 왔으니 괜찮다" 는
     가정은 돈이 오가는 화면에서 공짜로 두지 않습니다. */
  function esc(v) {
    return String(v == null ? '' : v).replace(/[&<>"']/g, function (ch) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch];
    });
  }

  /* 금액은 그 통화의 관습대로. 599 는 "$599", 0.14 는 "$0.14". */
  function money(n, cur) {
    var v = Number(n);
    if (!isFinite(v)) return '';
    var whole = Math.abs(v - Math.round(v)) < 1e-9;
    var s = new Intl.NumberFormat(cur === 'KRW' ? 'ko-KR' : 'en-US', {
      minimumFractionDigits: whole ? 0 : 2,
      maximumFractionDigits: whole ? 0 : 2
    }).format(v);
    return cur === 'KRW' ? s + '원' : '$' + s;
  }

  function when(iso) {
    if (!iso) return '';
    try {
      return new Intl.DateTimeFormat(KO ? 'ko-KR' : 'en-CA', {
        dateStyle: 'medium', timeStyle: 'short', timeZone: 'Asia/Seoul'
      }).format(new Date(iso)) + (KO ? ' (한국 시간)' : ' KST');
    } catch (e) { return iso; }
  }

  function row(label, value) {
    if (value === '' || value == null) return '';
    return '<div class="osrow"><span>' + esc(label) + '</span><b>' + value + '</b></div>';
  }

  function render(d) {
    var cur = d.currency || 'KRW';
    var reached = {};
    (d.timeline || []).forEach(function (e) { reached[e.state] = e.at; });

    var idx = FLOW.indexOf(d.state);
    var out = [];

    out.push('<p class="oshead">' + esc(T.heading) + '</p>');
    out.push(row(T.order, '<span class="osno">' + esc(d.orderNo) + '</span>'));
    out.push(row(T.company, esc(d.company)));
    out.push(row(T.country, esc(d.billingCountry)));
    var planName = {start: 'Start', grow: 'Grow', scale: 'Scale'}[d.plan] || d.plan;
    out.push(row(T.plan, esc(planName)));
    if (d.monthly) out.push(row(T.monthly, esc(money(d.monthly.total, cur))));
    if (d.afterDiscount) out.push(row(T.after, esc(money(d.afterDiscount, cur))));
    if (d.firstMonth && d.firstMonth.total != null) {
      out.push(row(T.first, esc(money(d.firstMonth.total, cur))));
    }
    out.push(row(T.tax, esc(T.taxTreat[d.taxTreatment] || d.taxTreatment)));
    out.push(row(T.received, esc(when(d.receivedAt))));

    /* 취소·반려는 흐름 밖입니다. 진행 단계로 그리면 사실과 다릅니다. */
    if (d.state === 'cancelled' || d.state === 'rejected') {
      var s = T.steps[d.state];
      out.push('<ul class="ostrack"><li class="now"><b>' + esc(s[0]) + '</b>' +
               '<span>' + esc(s[1]) + '</span></li></ul>');
    } else {
      out.push('<ul class="ostrack">');
      FLOW.forEach(function (st, i) {
        var s = T.steps[st];
        /* 온라인 주문은 proposal_sent 를 건너뜁니다. 밟지 않은 단계에
           체크를 그리면 「보낸 적 없는 제안서를 보냈다」가 됩니다 —
           timeline 에 시각이 있는 단계만 done 입니다. */
        var cls = i === idx ? 'now'
                : (i < idx && reached[st]) ? 'done'
                : (i < idx) ? 'skipped' : '';
        var at = reached[st] ? '<span>' + esc(when(reached[st])) + '</span>' : '';
        out.push('<li class="' + cls + '"><b>' + esc(s[0]) + '</b>' +
                 '<span>' + esc(s[1]) + '</span>' + at + '</li>');
      });
      out.push('</ul>');
      out.push('<p class="osnote">' + esc(T.notCharged) + '</p>');
    }

    result.innerHTML = out.join('');
    result.hidden = false;
    result.setAttribute('tabindex', '-1');
    result.focus({ preventScroll: true });
    result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    clearFail();
    result.hidden = true;

    var no = (form.querySelector('[name="orderNo"]').value || '').trim().toUpperCase();
    var email = (form.querySelector('[name="email"]').value || '').trim();

    if (!/^SO-\d{8}-\d{4}$/.test(no)) return fail(T.badNo);
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email)) return fail(T.badEmail);

    if (btn) { btn._label = btn.textContent; btn.disabled = true; btn.textContent = T.looking; }

    fetch('/api/order-status', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ orderNo: no, email: email })
    })
      .then(function (r) { return r.json().then(function (b) { return { s: r.status, b: b }; }); })
      .then(function (o) {
        if (o.s === 200 && o.b && o.b.ok) { render(o.b); return; }
        if (o.s === 429) return fail(T.busy);
        if (o.s === 404) return fail(T.notFound);
        fail(T.failed);
      })
      .catch(function () { fail(T.failed); })
      .then(function () {
        if (btn) { btn.disabled = false; btn.textContent = btn._label || T.cta; }
      });
  });

  /* 확인 메일의 링크에 번호가 붙어 있으면 미리 채워 둡니다.
     이메일은 절대 주소에 넣지 않습니다 — 브라우저 기록과 서버 로그에 남습니다. */
  try {
    var q = new URLSearchParams(location.search).get('no');
    if (q && /^SO-\d{8}-\d{4}$/i.test(q)) {
      form.querySelector('[name="orderNo"]').value = q.toUpperCase();
      form.querySelector('[name="email"]').focus();
    }
  } catch (e) {}
})();
