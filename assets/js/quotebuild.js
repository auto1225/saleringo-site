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

   Rounding, proration and the discount follow checkout.js line for
   line, so the number a buyer reads here is the number the order form
   opens with — $39.50, not $40.

   The handoff is srCarry plus ?plan= on the link: checkout.js reads
   qb* keys at boot and pre-selects plan, country and usage so nothing
   is retyped; the URL parameter is the fallback when storage is
   blocked or the link is opened in a new tab.
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
  var PRICING_URL = '../assets/data/pricing.json' + (ver ? '?v=' + ver : '');

  var P = null, VERDICT = null, timer = null, lastTaxOn = false;

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

  /* 원화는 정수, 달러는 센트까지 — 주문서와 같은 반올림 */
  function roundFor(cur) {
    return function (n) { return cur === 'KRW' ? Math.round(n) : Math.round(n * 100) / 100; };
  }
  function fmt(n, cur) {
    var v = roundFor(cur)(n);
    var neg = v < 0; v = Math.abs(v);
    var whole = Math.floor(v), cents = Math.round((v - whole) * 100);
    if (cents === 100) { whole += 1; cents = 0; }
    var s = String(whole).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    if (cur !== 'KRW' && cents > 0) s += '.' + (cents < 10 ? '0' : '') + cents;
    return (neg ? '-' : '') + (cur === 'KRW' ? s + t('원', ' KRW') : '$' + s);
  }
  /* 숫자 칸: 빈칸·음수·이상한 값은 0 — 음수 통화량이 음수 사용량이 되어 합계를 깎던 것 */
  function qty(el) {
    var n = Number(el && el.value);
    return isFinite(n) && n > 0 ? n : 0;
  }

  /* 전화를 켰는데 그 나라에 회선이 없으면 Scale 을 팔 수 없다 — 채팅·메신저(Grow)로 */
  function planFor(c) {
    var voiceOn = chVoice && chVoice.checked;
    if (voiceOn && c && c.voice === 'live') return 'scale';
    if ((chMsg && chMsg.checked) || voiceOn) return 'grow';
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

  /* 첫 달 일할 — checkout.js 와 같은 식(서울 날짜, 개시일 포함) */
  function proration() {
    var s = new Intl.DateTimeFormat('en-CA', {
      timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit'
    }).format(new Date());
    var p = s.split('-'), y = +p[0], m = +p[1], d = +p[2];
    var days = new Date(Date.UTC(y, m, 0)).getUTCDate();
    var left = days - d + 1;
    return { days: days, left: left, factor: left / days };
  }

  function calc() {
    if (!P) return;
    var c = countryRow(); if (!c) return;
    var cur = c.currency === 'KRW' ? 'KRW' : 'USD';
    var round = roundFor(cur);
    var pid = planFor(c);
    var plan = null;
    P.plans.forEach(function (p) { if (p.id === pid) plan = p; });
    if (!plan) return;

    var voiceOn = chVoice && chVoice.checked;
    var voiceBlocked = voiceOn && c.voice !== 'live';

    var vmin = 0, atalk = 0, usage = 0;
    if (voiceOn && !voiceBlocked) {
      vmin = qty(calls) * (Number(mins && mins.value) || 3);
      var vr = usageRate('voiceMinutes');
      if (vr) usage += vmin * vr.unitPrice[cur];
    }
    if (chMsg && chMsg.checked && c.code === 'KR') {
      atalk = qty(talks);
      var ar = usageRate('alimtalk');
      if (ar) usage += atalk * ar.unitPrice[cur];
    }
    usage = round(usage);
    if (rowCalls) rowCalls.hidden = !(voiceOn && !voiceBlocked);
    if (rowTalks) rowTalks.hidden = !(chMsg && chMsg.checked && c.code === 'KR');

    var base = plan.price[cur];
    var total = round(base + usage);
    /* 창립 할인은 주문서가 자동 적용한다 — 설정기가 정가만 보이면 한 클릭 뒤 숫자가 바뀐다.
       net 은 checkout.js 의 net 과 같은 식. */
    var disc = P.discount && P.discount.active !== false && P.discount.percent ? P.discount : null;
    var net = disc ? round(base * (100 - disc.percent) / 100) : base;
    var discounted = round(net + usage);
    var taxRule = P.tax && (P.tax[c.code] || P.tax['default']);
    var taxOn = !!(taxRule && taxRule.collected && taxRule.rate);
    lastTaxOn = taxOn;
    var pr = proration();
    var firstNet = round(net * pr.factor);

    if (planEl) planEl.innerHTML =
      '<b>' + plan.name[KO ? 'ko' : 'en'] + '</b> — ' +
      (voiceBlocked
        ? t('이 나라는 AI 전화 회선이 아직 없어 채팅·메신저 요금제로 잡았습니다. CRM은 셋 다 같습니다.',
            'no live phone line in this country yet, so this is the chat-and-messaging plan. The CRM is identical on all three.')
        : t('고르신 채널이 이 요금제를 정합니다. CRM은 셋 다 같습니다.',
            'your channels decide the plan. The CRM is identical on all three.'));

    if (sumEl) sumEl.innerHTML =
      '<span class="qb-big">' + fmt(discounted, cur) + t('/월', '/mo') + '</span>' +
      (disc ? '<span class="qb-split">' + t('처음 ' + disc.months + '개월 ' + disc.percent + '% 할인 · 그 뒤 ' + fmt(total, cur) + '/월',
                                             'First ' + disc.months + ' months at ' + disc.percent + '% off · then ' + fmt(total, cur) + '/mo') + '</span>' : '') +
      '<span class="qb-split">' + fmt(base, cur) + ' ' + t('요금제', 'plan') +
      (usage ? ' + ' + fmt(usage, cur) + ' ' + t('사용량(추정)', 'usage (est.)') : '') + '</span>' +
      (taxOn ? '<span class="qb-split">' + t('부가세 ' + Math.round(taxRule.rate * 100) + '% 별도 · 합계 ' + fmt(round(discounted + round(discounted * taxRule.rate)), cur),
                                              'Tax ' + Math.round(taxRule.rate * 100) + '% added · ' + fmt(round(discounted + round(discounted * taxRule.rate)), cur)) + '</span>' : '') +
      '<span class="qb-split">' + t('오늘 개시하면 이달 요금제분은 ' + pr.days + '일 중 ' + pr.left + '일치 · ' + fmt(firstNet, cur) + (taxOn ? ' + 부가세' : ''),
                                    'Start today and this month’s plan share is ' + pr.left + ' of ' + pr.days + ' days · ' + fmt(firstNet, cur) + (taxOn ? ' + tax' : '')) + '</span>' +
      '<span class="qb-split">' + t('최초 구축비 ' + (cur === 'KRW' ? '0원' : '$0') + ' · 약정 없음', 'Setup fee ' + (cur === 'KRW' ? '0 KRW' : '$0') + ' · no contract') + '</span>';

    if (noteEl) {
      var notes = [];
      if (voiceBlocked) notes.push(c.voice === 'soon'
        ? t('<b>이 나라는 AI 전화 회선을 개통하는 중입니다.</b> 지금은 채팅·메신저(Grow)로 시작하시고, 회선이 열리면 Scale로 올리실 수 있습니다. 서면 주문으로 개통 시점을 먼저 확인해 드립니다.',
            '<b>A phone line is being opened in this country.</b> Start with chat and messaging (Grow) and move to Scale once the line is live; a written order confirms the timing first.')
        : t('<b>이 나라는 아직 AI 전화 회선이 없습니다.</b> 채팅·메신저(Grow)로 시작하시거나, 쓰시던 번호를 연결할 수 있는지 주문 전에 물어보시면 그대로 말씀드립니다.',
            '<b>No AI phone line in this country yet.</b> Start with chat and messaging (Grow), or ask before you buy whether a number you already own can be connected — we answer plainly.'));
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

    /* 저장소가 막혀도, 새 탭으로 열어도 같은 요금제로 열리게 URL 에도 싣는다 */
    if (goBtn) goBtn.href = './checkout.html?plan=' + pid;

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
      body: JSON.stringify({ country: sel.country, plan: sel.plan, method: 'card', buyerType: 'business',
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
          /* 한국인데 사업자번호가 아직 없어 '검토' 인 경우: 위 줄의 부가세 10% 와 다른 말을 하지 않게 */
          review:      lastTaxOn
            ? t('부가세 10%는 주문서에 사업자등록번호를 넣으시면 세금계산서 기준으로 확정됩니다.',
                'The 10% VAT line is confirmed once your business registration number is on the order form.')
            : t('세금 처리는 주문 확인 때 확정됩니다.', 'Tax treatment is confirmed with your order.')
        };
        lines.push(TREAT[com.taxTreatment] || TREAT.review);
        /* 세금번호·구매자 유형처럼 주문서에서 넣을 것이 "없다"는 판정은
           여기서는 막힘이 아니라 예고입니다. 회선 없음 같은 진짜 막힘만 굵게. */
        var soft = /_required$/;
        (com.blockers || []).forEach(function (b) {
          if (soft.test(b.code || '')) return;
          lines.push('<b>' + (KO ? b.ko : b.en) + '</b>');
        });
        if (!lastTaxOn && (com.blockers || []).some(function (b) { return soft.test(b.code || ''); })) {
          lines.push(t('확정 세금은 주문서에서 사업자·세금번호를 넣으시면 그 자리에서 계산됩니다.',
                       'The exact tax line is settled on the order form once you enter your business and tax details.'));
        }
        taxEl.innerHTML = lines.join('<br>');
      }).catch(function () { /* the note above already covers the quiet case */ });
  }

  /* ── carry the exact configuration into the order form ───────── */
  if (goBtn) goBtn.addEventListener('click', function () {
    if (!window.srCarry || !P) return;
    var c = countryRow(); if (!c) return;
    var pid = planFor(c);
    var vmin = (chVoice && chVoice.checked && c.voice === 'live')
      ? qty(calls) * (Number(mins && mins.value) || 3) : 0;
    var atalk = (chMsg && chMsg.checked && c.code === 'KR') ? qty(talks) : 0;
    window.srCarry.write({
      qbPlan: pid, qbCountry: c.code,
      qbVoiceMinutes: vmin || '', qbAlimtalk: atalk || ''
    });
  });

  /* ── boot ────────────────────────────────────────────────────── */
  fetch(PRICING_URL).then(function (r) { return r.json(); }).then(function (j) {
    P = j;
    if (country) {
      /* soon(개통 중)과 no(회선 없음)는 다른 말이다 */
      var TAG = { live: '', soon: t(' — 전화 개통 중', ' — phone opening'), no: t(' — 전화 미지원', ' — no phone line') };
      P.countries.forEach(function (c) {
        var o = document.createElement('option');
        o.value = c.code;
        o.textContent = c.name[KO ? 'ko' : 'en'] + (c.voice in TAG ? TAG[c.voice] : TAG.no);
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
