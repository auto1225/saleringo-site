/* ═══════════════════════════════════════════════════════════════════
   SR_D60 — the 60-second demo that drives itself.
   ───────────────────────────────────────────────────────────────────
   #try (play.js) is the demo the visitor drives. This is the demo for
   the visitor who won't drive: press one button, and for sixty seconds
   watch a conversation become a record, the record become work, and a
   second channel land on the SAME customer.

   Rules carried over from the rest of the site:
   · Every figure is one the site already publishes (play.js dental set:
     crown $1,100–1,600, exam $95, Thu 10:30, Estimate #2461). Nothing
     is invented here, and the stage is labelled as a simulation.
   · Text lives in HTML, not canvas. The canvas behind the columns only
     draws flow — see the 'd60flow' scene at the bottom.
   · prefers-reduced-motion gets the finished state plus a step list,
     not a faster animation.
   · Voice is OFF by default. It is the browser's own synthesiser and
     says so on the toggle; the real voice is behind the tel: link.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var root = document.querySelector('[data-d60]');
  if (!root) return;

  var REDUCED = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var EN = (document.documentElement.lang || 'en').indexOf('ko') !== 0;
  function t(ko, en) { return EN ? en : ko; }

  /* ── the script ─────────────────────────────────────────────────
     One customer, three beats:
     A) 11:42 PM phone call  → fields fill → record forms → work lands
     B) 7:40 AM WhatsApp     → matched to the same record
     C) a question it must not answer → handed to a person, with what
        the person receives shown honestly.
     `at` is seconds on the 60s clock. */

  var STEPS = [
    { at: 0,  mark: 'ring',
      bub: { who: 'sys', text: t('밤 11:42 — 전화벨. 가게는 닫혀 있습니다.',
                                 '11:42 PM — the phone rings. You are closed.') } },
    { at: 2.5, bub: { who: 'user', when: '11:42 PM',
      text: t('앞니가 깨졌어요. 크라운이 얼마고, 이번 주에 볼 수 있나요?',
              'I chipped a front tooth. How much is a crown, and can anyone see me this week?') } },
    { at: 7, mark: 'answer', bub: { who: 'ai', when: '+3 sec',
      text: t('지르코니아 크라운은 55만원이고, 검진과 X-ray 후에 확정됩니다. 목요일 10:30이나 금요일 8:00이 비어 있습니다. 어느 쪽이 좋으세요?',
              'A crown runs $1,100 to $1,600 depending on the material, confirmed after an exam and X-ray. I have Thursday 10:30 or Friday 8:00 — which suits you?') },
      field: { k: t('요청', 'Request'), v: t('앞니 크라운 — 이번 주', 'Front-tooth crown — this week'),
               src: t('통화에서', 'from the call'), ok: true } },
    { at: 12, bub: { who: 'user', when: '11:44 PM', text: t('목요일이요. 김지은이고 010-4482-…', 'Thursday. It’s J. Kim, 010-4482-…') },
      field: { k: t('이름', 'Name'), v: 'J. Kim', src: t('본인 발화', 'caller said it'), ok: true } },
    { at: 15.5, field: { k: t('전화', 'Phone'), v: '010-4482-51··',
               src: t('발신번호와 일치', 'matches caller ID'), ok: true } },
    { at: 18, mark: 'captured', bub: { who: 'ai', when: '+2 sec',
      text: t('목요일 10:30으로 잡아 두었습니다. 확인 문자를 지금 보내 드릴게요.',
              'Thursday 10:30 is held for you. A confirmation text is on its way now.') },
      field: { k: t('예약', 'Slot'), v: t('목 10:30', 'Thu 10:30'), src: t('캘린더의 빈칸', 'free in your calendar'), ok: true } },
    { at: 22, mark: 'booked', crm: true,
      work: { icon: '✓', k: t('예약 확정', 'Booked'), v: t('목 10:30 · 캘린더에 들어감 · 확인 문자 발송', 'Thu 10:30 · in your calendar · confirmation sent') } },
    { at: 26, work: { icon: '#', k: 'Estimate #2461',
      v: t('지르코니아 크라운 55만원 — 사장님 요금표에서', 'Crown $1,100–1,600 + exam $95 — from your own fee schedule') } },
    { at: 30, work: { icon: '@', k: t('담당·기한', 'Owner & due'),
      v: t('데스크 담당 배정 · 목 09:00까지 차트 준비', 'assigned to the desk · chart ready by Thu 9:00') } },
    { at: 33.5, work: { icon: '↻', k: t('후속 예약', 'Follow-up queued'),
      v: t('무응답 시 D+2에 안내 문자 — 발송 전 사장님 확인', 'D+2 nudge drafted — you approve before it sends') } },

    /* B — same customer, second channel */
    { at: 39, mark: 'merged',
      bub: { who: 'sys', text: t('다음 날 아침 — 같은 손님이 카카오톡으로.', 'Next morning — the same customer, on WhatsApp.') } },
    { at: 41, bub: { who: 'user', chan: 'wa', when: '7:40 AM',
      text: t('어제 예약한 김지은인데, 주차가 되나요?', 'Hi, J. Kim from last night — is there parking?') },
      merge: true },
    { at: 46, bub: { who: 'ai', chan: 'wa', when: '+2 sec',
      text: t('네 — 건물 뒤에 전용 4자리가 있습니다. 목요일 10:30 예약은 그대로 유효합니다.',
              'Yes — four spaces behind the building. Your Thursday 10:30 booking is unchanged.') } },

    /* C — the refusal, and what a person receives */
    { at: 51, bub: { who: 'user', chan: 'wa', when: '7:41 AM',
      text: t('제 보험으로 크라운이 보장되나요?', 'Will my insurance cover the crown?') } },
    { at: 55, mark: 'handoff', handoff: true,
      bub: { who: 'ai', chan: 'wa', when: '+2 sec',
      text: t('보험 보장 판단은 담당자가 확인해 드려야 합니다. 대화 내용을 그대로 전달해 두었고, 오전 중에 연락드리겠습니다.',
              'Coverage is a call for the desk, not for me. I’ve passed our conversation along — someone will confirm this morning.') } },
    { at: 60, mark: 'done', done: true }
  ];

  var MARKS = [
    ['ring',     t('벨', 'Ring')],
    ['answer',   t('응답', 'Answered')],
    ['captured', t('수집', 'Captured')],
    ['booked',   t('업무', 'Worked')],
    ['merged',   t('합류', 'Merged')],
    ['handoff',  t('사람에게', 'Handed off')]
  ];

  /* ── DOM handles ────────────────────────────────────────────── */
  var convo  = root.querySelector('[data-d60-convo]');
  var fields = root.querySelector('[data-d60-fields]');
  var record = root.querySelector('[data-d60-record]');
  var work   = root.querySelector('[data-d60-work]');
  var hand   = root.querySelector('[data-d60-handoff]');
  var barEl  = root.querySelector('[data-d60-bar]');
  var ticks  = root.querySelector('[data-d60-ticks]');
  var btn    = root.querySelector('[data-d60-play]');
  var vbtn   = root.querySelector('[data-d60-voice]');
  var endrow = root.querySelector('[data-d60-end]');

  if (!convo || !btn) return;

  /* progress ticks */
  if (ticks) {
    MARKS.forEach(function (m) {
      var s = document.createElement('span');
      s.setAttribute('data-mk', m[0]);
      s.textContent = m[1];
      ticks.appendChild(s);
    });
  }

  /* ── voice (browser synthesiser, opt-in, honestly labelled) ─── */
  var voiceOn = false;
  function speak(text) {
    if (!voiceOn || !window.speechSynthesis) return;
    try {
      window.speechSynthesis.cancel();
      var u = new SpeechSynthesisUtterance(text);
      u.lang = EN ? 'en-US' : 'ko-KR';
      u.rate = 1.04;
      window.speechSynthesis.speak(u);
    } catch (e) { /* no voice is a fine outcome */ }
  }
  if (vbtn) vbtn.addEventListener('click', function () {
    voiceOn = !voiceOn;
    vbtn.setAttribute('aria-pressed', voiceOn ? 'true' : 'false');
    vbtn.classList.toggle('on', voiceOn);
    if (!voiceOn && window.speechSynthesis) window.speechSynthesis.cancel();
  });

  /* ── renderers ──────────────────────────────────────────────── */
  function esc(s) {
    var d = document.createElement('i'); d.textContent = s; return d.innerHTML;
  }

  function addBubble(b) {
    var row = document.createElement('div');
    if (b.who === 'sys') {
      row.className = 'd60sys';
      row.textContent = b.text;
    } else {
      row.className = 'nl ' + (b.who === 'ai' ? 'sr' : 'us');
      var chanTag = b.chan === 'wa'
        ? '<i class="d60chan">' + t('카카오톡', 'WhatsApp') + '</i>' : '';
      row.innerHTML =
        '<span class="t"><em>' + (b.who === 'ai' ? 'Saleringo' : t('손님', 'Customer')) + '</em>' +
        (b.when ? esc(b.when) : '') + '</span>' +
        '<div class="bub ' + (b.who === 'ai' ? 'ai' : 'user') + '">' + chanTag + esc(b.text) + '</div>';
      if (b.who === 'ai') speak(b.text);
    }
    convo.appendChild(row);
    convo.scrollTop = convo.scrollHeight;
  }

  function addField(f) {
    if (!fields) return;
    var row = document.createElement('div');
    row.className = 'd60field';
    row.innerHTML = '<b>' + esc(f.k) + '</b><span>' + esc(f.v) + '</span>' +
      '<i class="' + (f.ok ? 'ok' : 'guess') + '">' + esc(f.src) + '</i>';
    fields.appendChild(row);
  }

  function showRecord() {
    if (record) record.classList.add('on');
  }

  function addWork(w) {
    if (!work) return;
    var row = document.createElement('div');
    row.className = 'd60work';
    row.innerHTML = '<i>' + esc(w.icon) + '</i><b>' + esc(w.k) + '</b><span>' + esc(w.v) + '</span>';
    work.appendChild(row);
  }

  function showMerge() {
    if (!record) return;
    record.classList.add('merged');
    var chip = record.querySelector('[data-d60-chans]');
    if (chip) chip.innerHTML +=
      ' <i class="d60wa">' + t('카카오톡', 'WhatsApp') + '</i>';
    var note = record.querySelector('[data-d60-match]');
    if (note) { note.hidden = false; }
  }

  function showHandoff() {
    if (hand) hand.hidden = false;
  }

  function markTick(name) {
    if (!ticks) return;
    var el = ticks.querySelector('[data-mk="' + name + '"]');
    if (el) el.classList.add('on');
  }

  /* ── the clock ──────────────────────────────────────────────── */
  var idx = 0, t0 = 0, paused = true, doneAll = false, raf = 0, elapsed = 0;

  function apply(step) {
    if (step.mark)   markTick(step.mark);
    if (step.bub)    addBubble(step.bub);
    if (step.field)  addField(step.field);
    if (step.crm)    showRecord();
    if (step.work)   addWork(step.work);
    if (step.merge)  showMerge();
    if (step.handoff) showHandoff();
    if (step.done)   finish();
  }

  function reset() {
    idx = 0; elapsed = 0; doneAll = false;
    convo.innerHTML = '';
    if (fields) fields.innerHTML = '';
    if (work) work.innerHTML = '';
    if (record) {
      record.classList.remove('on', 'merged');
      var note = record.querySelector('[data-d60-match]');
      if (note) note.hidden = true;
      var chip = record.querySelector('[data-d60-chans]');
      if (chip) chip.innerHTML = '<i class="d60ph">' + t('전화', 'Phone') + '</i>';
    }
    if (hand) hand.hidden = true;
    if (endrow) endrow.hidden = true;
    if (ticks) ticks.querySelectorAll('.on').forEach(function (x) { x.classList.remove('on'); });
    if (barEl) barEl.style.width = '0%';
  }

  function finish() {
    doneAll = true; paused = true;
    btn.textContent = t('↺ 처음부터', '↺ Replay');
    btn.setAttribute('aria-pressed', 'false');
    if (endrow) endrow.hidden = false;
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    root.classList.remove('playing');
  }

  function frame(now) {
    if (paused) return;
    elapsed = (now - t0) / 1000;
    if (barEl) barEl.style.width = Math.min(100, elapsed / 60 * 100) + '%';
    while (idx < STEPS.length && STEPS[idx].at <= elapsed) apply(STEPS[idx++]);
    if (idx < STEPS.length) raf = requestAnimationFrame(frame);
  }

  function play() {
    if (doneAll) reset();
    paused = false;
    root.classList.add('playing');
    btn.textContent = t('⏸ 일시정지', '⏸ Pause');
    btn.setAttribute('aria-pressed', 'true');
    t0 = performance.now() - elapsed * 1000;
    raf = requestAnimationFrame(frame);
  }

  function pause() {
    paused = true;
    root.classList.remove('playing');
    btn.textContent = t('▶ 이어서', '▶ Resume');
    btn.setAttribute('aria-pressed', 'false');
    cancelAnimationFrame(raf);
    if (window.speechSynthesis) window.speechSynthesis.cancel();
  }

  btn.addEventListener('click', function () { (paused ? play : pause)(); });

  /* arriving via the hero CTA (#demo60) starts it once, when visible */
  var autolaunched = false;
  function autoplayIfAsked() {
    if (autolaunched) return;
    if (location.hash === '#demo60') { autolaunched = true; setTimeout(play, 500); }
  }

  /* ── reduced motion: the finished state, stepless ───────────── */
  if (REDUCED) {
    STEPS.forEach(function (s) { if (!s.done) apply(s); });
    finish();
    btn.textContent = t('전체가 표시되어 있습니다', 'Shown in full');
    btn.disabled = true;
  } else {
    window.addEventListener('hashchange', autoplayIfAsked);
    autoplayIfAsked();
    /* leaving the tab mid-run: pause honestly instead of skipping ahead */
    document.addEventListener('visibilitychange', function () {
      if (document.hidden && !paused) pause();
    });
  }
})();

/* ── the flow the canvas draws: three channels feeding one record ──
   Text never lives here; the columns beside it carry every fact.
   Contract per canvas.js: factory({ink,reduced,…}) → {frame(ctx,w,h,t)}. */
if (window.SR_SCENE) window.SR_SCENE('d60flow', function (env) {
  var teal = env.ink.accent, dim = env.ink.faint;
  return {
    settleSeconds: 4,
    frame: function (ctx, w, h, T) {
      var xs = w * 0.04, xm = w * 0.5, xe = w * 0.96;
      var ys = [h * 0.22, h * 0.5, h * 0.78];
      ctx.lineWidth = 1.5;
      ys.forEach(function (y, i) {
        ctx.strokeStyle = dim;
        ctx.beginPath();
        ctx.moveTo(xs, y);
        ctx.bezierCurveTo(xm * 0.7, y, xm * 0.7, h * 0.5, xm, h * 0.5);
        ctx.stroke();
        if (!env.reduced) {
          var p = ((T * 0.25) + i * 0.33) % 1;
          var x = xs + (xm - xs) * p;
          var yy = y + (h * 0.5 - y) * (p * p * (3 - 2 * p));
          ctx.fillStyle = teal;
          ctx.beginPath(); ctx.arc(x, yy, 3, 0, 6.283); ctx.fill();
        }
      });
      ctx.strokeStyle = teal;
      ctx.beginPath(); ctx.moveTo(xm, h * 0.5); ctx.lineTo(xe, h * 0.5); ctx.stroke();
      if (!env.reduced) {
        var q = (T * 0.35) % 1;
        ctx.fillStyle = teal;
        ctx.beginPath(); ctx.arc(xm + (xe - xm) * q, h * 0.5, 3.5, 0, 6.283); ctx.fill();
      }
      return true;   /* keep animating while visible */
    }
  };
});
