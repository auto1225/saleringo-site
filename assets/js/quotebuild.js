/* ═══════════════════════════════════════════════════════════════════
   SR_QB — the month builder on the pricing page.
   ───────────────────────────────────────────────────────────────────
   "가격 보기 → 문의하기"의 간극을 메운다: 내 통화량·채널·나라를
   넣으면 한 달이 얼마인지 지금 보이고, 그 구성이 그대로 주문서에
   실린다.

   Judgement stays on the server, exactly as checkout does it: this
   file computes the arithmetic from pricing.json (the same file the
   plans table renders from), and asks /api/quote for what the screen
   must not decide — tax treatment, voice availability, orderability.
   Amounts here are estimates and say so; the binding figure is the
   prorated one the order confirmation carries.

   The handoff is srCarry: checkout.js reads qb* keys at boot and
   pre-selects plan, country and usage so nothing is retyped.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var root = document.querySelector('[data-qb]');
  if (!root) return;

  var KO = (document.documentElement.lang || '').indexOf('ko') === 0;
  function t(ko, en) { return KO ? ko : en; }

  /* pricing.json under the same ?v= this script was loaded with, so a
     new deploy is never read through last hour's cache. */
  var me = document.querySelector('script[src*="quotebuild.js"]');
  var ver = (me && (me.src.match(/[?&]v=([0-9.]+)/) || [])[1]) || '';
  var PRICING_URL = (KO ? '../' : '../') + 'assets/data/pricing.json' + (ver ? '?v=' + ver : '');

  var P = null, VERDICT = null, timer = null;

  var $ = function (sel) { return root.querySelector(sel); };
  var country = $('[data-qb-country]');
  var chVoice = $('[data-qb-voice]');
  var chMsg   = $('[data-qb-msg]');
  var calls   = $('[data-qb-calls]');
  var mins    = $('[data-qb-mins]');
  var talks   = $('[data-qb-talks]');
  var planEl  = $('[data-qb-plan]');
  var sumEl   = $('[data-qb-sum]');
  var taxEl   = $('[data-qb-tax]');
  var noteEl  = $('[data-qb-note]');
  var incEl   = $('[data-qb-inc]');
  var goBtn   = $('[data-qb-go]');
  var rowCalls = $('[data-qb-row-calls]');
  var rowTalks = $('[data-qb-row-talks]');

  function fmt(n, cur) {
    n = Math.round(n);
    var s = String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return cur === 'KRW' ? s + t('원', ' KRW') : '$' + s;
  }

  function planFor() {
    if (chVoice && chVoice.checked) return 'scale';
    if (chMsg && chMsg.checked) return 'grow';
    return 'start';
  }

  function countryRow() {
    if (!P) return null;
    var code = country ? country.value : 'KR';
    for (var i = 0; i < P.countries.length; i++) {
      if (P.countries[i].code === code) return P.countries[i];
    }
    return null;
  }

  function usageRate(id) {
    for (var i = 0; i < P.usage.length; i++) if (P.usage[i].id === id) return P.usage[i];
    return null;
  }

  function calc() {
    if (!P) return;
    var c = countryRow(); if (!c) return;
    var cur = c.currency === 'KRW' ? 'KRW' : 'USD';
    var pid = planFor();
    var plan = null;
    P.plans.forEach(function (p) { if (p.id === pid) plan = p; });
    if (!plan) return;

    /* 전화를 켰는데 그 나라에 회선이 없는 경우: 숫자를 보여 주기 전에
       사실부터. 서버 판정(blockers)이 오면 그쪽 문구가 이깁니다. */
    var voiceBlocked = chVoice && chVoice.checked && c.voice !== 'live';

    var vmin = 0, atalk = 0, usage = 0;
    if (chVoice && chVoice.checked && !voiceBlocked) {
      vmin = (Number(calls && calls.value) || 0) * (Number(mins && mins.value) || 3);
      var vr = usageRate('voiceMinutes');
      if (vr) usage += vmin * vr.unitPrice[cur];
    }
    if (chMsg && chMsg.checked && c.code === 'KR') {
      atalk = Number(talks && talks.value) || 0;
      var ar = usageRate('alimtalk');
      if (ar) usage += atalk * ar.unitPrice[cur];
    }
    if (rowCalls) rowCalls.hidden = !(chVoice && chVoice.checked);
    if (rowTalks) rowTalks.hidden = !(chMsg && chMsg.checked && c.code === 'KR');

    var base = plan.price[cur];
    var total = base + usage;

    if (planEl) planEl.innerHTML =
      '<b>' + plan.name[KO ? 'ko' : 'en'] + '</b> — ' +
      t('고르신 채널이 이 요금제를 정합니다. CRM은 셋 다 같습니다.',
        'your channels decide the plan. The CRM is identical on all three.');

    if (sumEl) sumEl.innerHTML =
      '<span class="qb-big">' + fmt(total, cur) + t('/월', '/mo') + '</span>' +
      '<span class="qb-split">' + fmt(base, cur) + ' ' + t('요금제', 'plan') +
      (usage ? ' + ' + fmt(usage, cur) + ' ' + t('사용량(추정)', 'usage (est.)') : '') + '</span>' +
      '<span class="qb-split">' + t('최초 구축비 0원 · 약정 없음', 'Setup fee $0 · no contract') + '</span>';

    if (noteEl) {
      var notes = [];
      if (voiceBlocked) notes.push(t(
        '<b>이 나라는 아직 AI 전화 회선이 없습니다.</b> 채팅·메신저(Grow)로 시작하시거나, 서면 주문으로 회선 상황을 먼저 확인해 드립니다.',
        '<b>No live phone line in this country yet.</b> Start with chat and messaging (Grow), or a written order checks line availability first.'));
      notes.push(t(
        '첫 달만 개시일부터 말일까지 날짜로 나눠 청구합니다 — 확정 금액은 주문 확인 때 함께 보내 드립니다.',
        'Only the first month is prorated by days from your start date — the exact figure comes with the order confirmation.'));
      notes.push(t(
        '<b>파일럿 = 첫 14일.</b> 그 기간의 실제 응대 기록을 보고 판단하시고, 아니면 전액 환불입니다.',
        '<b>The pilot is your first 14 days.</b> Judge it on the real response log; if it fails you, the first payment refunds in full.'));
      noteEl.innerHTML = notes.map(function (x) { return '<p>' + x + '</p>'; }).join('');
    }

    if (incEl) incEl.innerHTML = [
      t('대화 ' + plan.conversations.toLocaleString() + '건/월', plan.conversations.toLocaleString() + ' conversations/mo'),
      t('사용자 ' + plan.seats + '명', plan.seats + ' seats'),
      plan.channels[KO ? 'ko' : 'en'],
      t('업종별 CRM 전체', 'the full trade CRM'),
      t('연동비 0원', 'integrations at $0')
    ].map(function (x) { return '<li>' + x + '</li>'; }).join('');

    askServerSoon({ country: c.code, plan: pid, voiceMinutes: vmin, alimtalk: atalk, cur: cur, total: total, base: base });
  }

  /* ── the server's verdict: tax + availability, never invented here ── */
  function askServerSoon(sel) {
    clearTimeout(timer);
    timer = setTimeout(function () { askServer(sel); }, 350);
  }
  function askServer(sel) {
    fetch('/api/quote', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ country: sel.country, plan: sel.plan, buyerType: 'business',
                             voiceMinutes: sel.voiceMinutes, alimtalk: sel.alimtalk })
    }).then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) {
        if (!taxEl) return;
        if (!j || j.error || !j.commerce) {
          taxEl.textContent = t('세금과 접수 가능 여부는 주문서에서 확인됩니다.',
                                'Tax and availability are confirmed on the order form.');
          return;
        }
        VERDICT = j;
        var com = j.commerce, lines = [];
        var TREAT = {
          vat_charged: t('부가세 10%가 위 금액에 더해집니다.', 'Korean VAT 10% is added to the figure above.'),
          vat_reverse: t('세금은 저희가 걷지 않습니다 — 리버스 차지 대상입니다.', 'We add no tax — reverse charge applies.'),
          none:        t('저희가 더하는 세금이 없습니다.', 'No tax added by us.'),
          review:      t('세금 처리는 주문 확인 때 확정됩니다.', 'Tax treatment is confirmed with your order.')
        };
        lines.push(TREAT[com.taxTreatment] || TREAT.review);
        (com.blockers || []).forEach(function (b) {
          lines.push('<b>' + (KO ? b.ko : b.en) + '</b>');
        });
        taxEl.innerHTML = lines.join('<br>');
      }).catch(function () { /* the note above already covers the quiet case */ });
  }

  /* ── carry the exact configuration into the order form ───────── */
  if (goBtn) goBtn.addEventListener('click', function () {
    if (!window.srCarry || !P) return;
    var c = countryRow(); if (!c) return;
    var pid = planFor();
    var vmin = (chVoice && chVoice.checked && c.voice === 'live')
      ? (Number(calls && calls.value) || 0) * (Number(mins && mins.value) || 3) : 0;
    var atalk = (chMsg && chMsg.checked && c.code === 'KR') ? (Number(talks && talks.value) || 0) : 0;
    window.srCarry.write({
      qbPlan: pid, qbCountry: c.code,
      qbVoiceMinutes: vmin || '', qbAlimtalk: atalk || ''
    });
  });

  /* ── boot ────────────────────────────────────────────────────── */
  fetch(PRICING_URL).then(function (r) { return r.json(); }).then(function (j) {
    P = j;
    if (country) {
      P.countries.forEach(function (c) {
        var o = document.createElement('option');
        o.value = c.code;
        o.textContent = c.name[KO ? 'ko' : 'en'] +
          (c.voice === 'live' ? '' : t(' — 전화 준비 중', ' — phone pending'));
        country.appendChild(o);
      });
      country.value = KO ? 'KR' : 'US';
    }
    ['change', 'input'].forEach(function (ev) { root.addEventListener(ev, calc); });
    calc();
  }).catch(function () {
    root.querySelectorAll('[data-qb-live]').forEach(function (el) {
      el.innerHTML = '<p>' + t('계산기를 불러오지 못했습니다 — 위 요금표의 숫자가 그대로 유효합니다.',
                               'The builder failed to load — the plan table above still holds.') + '</p>';
    });
  });
})();
