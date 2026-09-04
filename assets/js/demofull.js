/* ═══════════════════════════════════════════════════════════════════
   SR_DEMO — the full demo: a night call you can hear, the next
   morning's messages, and the owner's screen at nine.
   ───────────────────────────────────────────────────────────────────
   Chapter 1 is real audio: two synthetic voices (customer and AI) made
   for this demo with neural TTS, played through Web Audio so the
   customer sounds like a phone line and the waveform moves with the
   speech. Chapters 2 and 3 are text: KakaoTalk / WhatsApp the next
   morning, then the owner's morning list.

   Rules carried over from the rest of the site:
   · Every figure is one the site already publishes (crown 550,000원 /
     $1,100–1,600, exam $95, Thu 10:30, Estimate #2472). The stage is
     labelled as a simulation and the voices as synthetic.
   · Text lives in HTML; the canvas only draws the waveform.
   · prefers-reduced-motion gets the finished state, not a fast run.
   · Nothing plays until the visitor presses play.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var root = document.querySelector('[data-d60]');
  if (!root) return;

  var KO = (document.documentElement.lang || '').indexOf('ko') === 0;
  var LANG = KO ? 'ko' : 'en';
  function t(ko, en) { return KO ? ko : en; }
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* asset version: the same ?v= the page uses for site.css */
  var VER = (function () {
    var l = document.querySelector('link[href*="site.css?v="]');
    var m = l && l.getAttribute('href').match(/v=([0-9.]+)/);
    return m ? m[1] : '1';
  })();
  var AUDIO_BASE = root.getAttribute('data-d60-audio') || '../assets/audio/demo/';

  /* ── DOM ───────────────────────────────────────────────────── */
  function q(s) { return root.querySelector(s); }
  var convo = q('[data-d60-convo]'), fields = q('[data-d60-fields]'), record = q('[data-d60-record]'),
      work = q('[data-d60-work]'), hand = q('[data-d60-handoff]'), morning = q('[data-d60-morning]'),
      morningList = q('[data-d60-morninglist]'), barEl = q('[data-d60-bar]'), timeEl = q('[data-d60-time]'),
      totalEl = q('[data-d60-total]'), btn = q('[data-d60-play]'), capBtn = q('[data-d60-caption]'),
      restartBtn = q('[data-d60-restart]'), endrow = q('[data-d60-end]'), stateEl = q('[data-d60-callstate]'),
      speakerEl = q('[data-d60-speaker]'), wave = q('[data-d60-wave]'), summaryEl = q('[data-d60-summary]');
  var tabs = Array.prototype.slice.call(root.querySelectorAll('[data-d60-tab]'));
  if (!convo || !btn) return;

  /* ── script pieces that are not spoken ─────────────────────── */
  var F = {
    request: { k: t('요청', 'Request'), v: t('앞니 크라운 — 이번 주', 'Front-tooth crown — this week'), src: t('통화에서', 'from the call') },
    quote:   { k: t('견적', 'Quote'), v: t('지르코니아 크라운 550,000원', 'Crown $1,100–1,600 + exam $95'), src: t('사장님 요금표', 'your fee schedule') },
    name:    { k: t('이름', 'Name'), v: t('김지은', 'Jane Kim'), src: t('본인 발화', 'caller said it') },
    phone:   { k: t('전화', 'Phone'), v: t('010-4482-51··', '555-01··'), src: t('발신번호와 일치', 'matches caller ID') },
    slot:    { k: t('예약', 'Slot'), v: t('목 10:30', 'Thu 10:30'), src: t('캘린더의 빈 시간', 'free in your calendar') },
    pain:    { k: t('증상', 'Symptom'), v: t('시림 — 응급 아님', 'sensitive — not urgent'), src: t('본인 발화 · 진단 아님', 'caller said it · not a diagnosis') }
  };
  var W = {
    booked:   { icon: '✓', k: t('예약 확정', 'Booked'), v: t('목 10:30 · 캘린더에 들어감 · 확인 문자 발송', 'Thu 10:30 · in your calendar · confirmation text sent') },
    estimate: { icon: '#', k: 'Estimate #2472', v: t('지르코니아 크라운 550,000원 — 사장님 요금표에서', 'Crown $1,100–1,600 + exam $95 — from your own fee schedule') },
    owner:    { icon: '@', k: t('담당·기한', 'Owner & due'), v: t('데스크 담당 배정 · 목 09:00까지 차트 준비', 'assigned to the desk · chart ready by Thu 9:00') },
    follow:   { icon: '↻', k: t('후속 문자', 'Follow-up'), v: t('무응답 시 D+2 안내 문자 초안 — 발송 전 사장님 확인', 'D+2 nudge drafted — you approve before it sends') }
  };
  var CHAT = [
    { who: 'user', when: '7:40 AM', text: t('어제 예약한 김지은인데, 주차가 되나요?', 'Hi, Jane Kim from last night — is there parking?') },
    { who: 'ai',   when: '+2 sec',  text: t('네 — 건물 뒤에 전용 4자리가 있습니다. 목요일 10:30 예약은 그대로 유효합니다.', 'Yes — four spaces behind the building. Your Thursday 10:30 booking is unchanged.'), merge: true },
    { who: 'user', when: '7:41 AM', text: t('제 보험으로 크라운이 보장되나요?', 'Will my insurance cover the crown?') },
    { who: 'ai',   when: '+2 sec',  text: t('보험 보장 판단은 담당자가 확인해 드려야 합니다. 대화 내용을 그대로 전달해 두었고, 오전 중에 연락드리겠습니다.', 'Coverage is a call for the desk, not for me. I’ve passed our conversation along — someone will confirm this morning.'), handoff: true }
  ];
  var MORNING = [
    { icon: '✓', k: t('새 예약 1건', 'New booking'), v: t('김지은 · 목 10:30 · 캘린더에 있음', 'Jane Kim · Thu 10:30 · in the calendar') },
    { icon: '#', k: t('견적서 #2472', 'Estimate #2472'), v: t('550,000원 · 문자로 발송됨 · 열람 확인', '$1,100–1,600 · sent by text · opened') },
    { icon: '@', k: t('데스크 할 일', 'Desk task'), v: t('목 09:00까지 차트 준비 · 담당 이수진', 'chart ready by Thu 9:00 · owner: Sujin') },
    { icon: '!', k: t('답변 대기 1건', 'Waiting for a person'), v: t('보험 보장 문의 · 대화 전체 첨부 · 담당 이수진', 'insurance question · full thread attached · owner: Sujin') }
  ];
  var PERSON = { who: 'person', when: '9:12 AM',
    text: t('담당자 이수진입니다. 김지은 님, 보장 범위는 보험사 약관마다 달라서 목요일에 보험증권을 가져오시면 접수 때 바로 확인해 드릴게요.',
            'This is Sujin from the front desk. Hi Jane — coverage depends on your plan, so bring your insurance card on Thursday and we’ll confirm at check-in.') };

  /* ── timeline ──────────────────────────────────────────────── */
  var lines = [], STEPS = [], TOTAL = 0, CHAPTER_AT = [0, 0, 0];
  var SIDE = { 1: ['request'], 2: ['quote'], 5: ['name', 'phone'], 6: ['slot', 'crm', 'booked'], 7: ['pain'], 8: ['estimate', 'owner', 'follow'] };

  function build(man) {
    lines = (man && man[LANG]) || [];
    STEPS = []; var cur = 0;
    STEPS.push({ at: 0, chapter: 1, state: 'ring', sys: t('밤 11:42 — 전화벨이 울립니다. 진료는 끝났습니다.', '11:42 PM — the phone rings. The practice is closed.') });
    cur = 2.4;
    lines.forEach(function (ln, i) {
      var dur = ln.dur || 4;
      STEPS.push({ at: cur, chapter: 1, line: i, who: ln.who, text: ln.text, dur: dur, state: i === 0 ? 'live' : null });
      (SIDE[i] || []).forEach(function (key, j) {
        var st = { at: cur + Math.min(dur * 0.7, 1.4 + j * 1.1) };
        if (key === 'crm') st.crm = true; else if (F[key]) st.field = F[key]; else if (W[key]) st.work = W[key];
        STEPS.push(st);
      });
      cur += dur + 0.7;
    });
    var callLen = cur - 2.4;
    STEPS.push({ at: cur, state: 'ended', sys: t('통화 종료 · ' + mmss(callLen), 'Call ended · ' + mmss(callLen)) });
    cur += 2.6;
    CHAPTER_AT[1] = cur;
    STEPS.push({ at: cur, chapter: 2, state: 'chat', sys: t('다음 날 아침 7:40 — 같은 손님이 카카오톡으로.', 'Next morning, 7:40 AM — the same customer, on WhatsApp.') });
    cur += 2.4;
    CHAT.forEach(function (m) { STEPS.push({ at: cur, chat: m }); cur += m.who === 'ai' ? 5.2 : 3.6; });
    cur += 0.8;
    CHAPTER_AT[2] = cur;
    STEPS.push({ at: cur, chapter: 3, state: 'morning', sys: t('오전 9:00 — 사장님 화면.', '9:00 AM — the owner’s screen.') });
    cur += 2.2;
    MORNING.forEach(function (m) { STEPS.push({ at: cur, morning: m }); cur += 2.3; });
    STEPS.push({ at: cur, chat: PERSON, person: true }); cur += 5.5;
    STEPS.push({ at: cur, done: true });
    TOTAL = cur + 0.5;
    STEPS.sort(function (a, b) { return a.at - b.at; });
    if (totalEl) totalEl.textContent = mmss(TOTAL);
    tabs.forEach(function (tb, i) {
      var r = tb.querySelector('[data-d60-range]');
      var end = i < 2 ? CHAPTER_AT[i + 1] : TOTAL;
      if (r) r.textContent = r.getAttribute('data-base') + ' · ' + mmss(CHAPTER_AT[i]) + '–' + mmss(end);
    });
  }

  function mmss(s) { s = Math.max(0, Math.round(s)); return Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2); }
  function clock(sec) { /* 11:42:00 PM + seconds, for the call bubbles */
    var base = 23 * 3600 + 42 * 60 + Math.round(sec);
    var h = Math.floor(base / 3600) % 24, m = Math.floor(base / 60) % 60, s = base % 60;
    return (KO ? '오후 ' : '') + ((h % 12) || 12) + ':' + ('0' + m).slice(-2) + ':' + ('0' + s).slice(-2) + (KO ? '' : ' PM');
  }

  /* ── audio ─────────────────────────────────────────────────── */
  var ctx = null, analyser = null, cache = {}, current = null, voiceOn = true, curWho = null;
  function ensureCtx() {
    if (ctx || !(window.AudioContext || window.webkitAudioContext)) return;
    try {
      ctx = new (window.AudioContext || window.webkitAudioContext)();
      analyser = ctx.createAnalyser(); analyser.fftSize = 128; analyser.smoothingTimeConstant = 0.7;
      analyser.connect(ctx.destination);
    } catch (e) { ctx = null; }
  }
  function audioFor(i) {
    if (cache[i]) return cache[i];
    var ln = lines[i]; if (!ln) return null;
    var a = new Audio(AUDIO_BASE + LANG + '/' + ln.file + '?v=' + VER);
    a.preload = 'auto';
    if (ctx) {
      try {
        var src = ctx.createMediaElementSource(a);
        if (ln.who === 'user') {  /* a phone line: narrow band, a little hotter */
          var bp = ctx.createBiquadFilter(); bp.type = 'bandpass'; bp.frequency.value = 1500; bp.Q.value = 0.7;
          var g = ctx.createGain(); g.gain.value = 1.7;
          src.connect(bp); bp.connect(g); g.connect(analyser);
        } else { src.connect(analyser); }
      } catch (e) { /* fall back to plain playback */ }
    }
    cache[i] = a;
    return a;
  }
  function stopAudio() { if (current) { try { current.pause(); } catch (e) {} current = null; } curWho = null; if (speakerEl) speakerEl.textContent = ''; }
  function playLine(i, who) {
    stopAudio();
    curWho = who;
    if (speakerEl) speakerEl.textContent = who === 'user' ? t('손님이 말하는 중', 'Customer speaking') : t('AI가 답하는 중', 'AI speaking');
    if (!voiceOn) return;
    var a = audioFor(i); if (!a) return;
    current = a;
    try { a.currentTime = 0; } catch (e) {}
    var p = a.play(); if (p && p.catch) p.catch(function () {});
    if (lines[i + 1]) audioFor(i + 1);  /* warm the next line */
  }
  function tone(freqs, secs, gain) {  /* ring / message blip, synthesised */
    if (!ctx || !voiceOn) return;
    try {
      var g = ctx.createGain(); g.gain.value = gain; g.connect(ctx.destination);
      freqs.forEach(function (f) { var o = ctx.createOscillator(); o.type = 'sine'; o.frequency.value = f; o.connect(g); o.start(); o.stop(ctx.currentTime + secs); });
      g.gain.setValueAtTime(gain, ctx.currentTime + secs - 0.05); g.gain.linearRampToValueAtTime(0, ctx.currentTime + secs);
    } catch (e) {}
  }

  /* waveform */
  var wctx = wave && wave.getContext && wave.getContext('2d'), wdata = analyser ? null : null;
  function drawWave() {
    if (!wctx) return;
    var w = wave.width, h = wave.height, n = 40, gap = 3, bw = (w - gap * (n - 1)) / n;
    wctx.clearRect(0, 0, w, h);
    var live = current && !current.paused && analyser;
    if (live && !wdata) wdata = new Uint8Array(analyser.frequencyBinCount);
    if (live) analyser.getByteFrequencyData(wdata);
    for (var i = 0; i < n; i++) {
      var v = live ? wdata[Math.min(wdata.length - 1, 2 + i)] / 255 : 0.06;
      var bh = Math.max(3, v * h);
      wctx.fillStyle = live ? (curWho === 'user' ? '#616B75' : '#0B7878') : '#E2DDD3';
      wctx.fillRect(i * (bw + gap), h - bh, bw, bh);
    }
  }

  /* ── stage rendering ───────────────────────────────────────── */
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function scrollConvo() { convo.scrollTop = convo.scrollHeight; }
  function addSys(text) {
    var d = document.createElement('div'); d.className = 'd60sys'; d.textContent = text; convo.appendChild(d); scrollConvo();
  }
  function addMsg(m, when, chan) {
    var d = document.createElement('div');
    d.className = 'd60msg ' + m.who + (chan ? ' ' + chan : '');
    var who = m.who === 'user' ? t('손님', 'Customer') : m.who === 'ai' ? 'AI' : t('담당자', 'Front desk');
    d.innerHTML = '<span class="d60who"><b>' + esc(who) + '</b>' + (chan ? '<i class="d60chan">' + t('카카오톡', 'WhatsApp') + '</i>' : '') +
      '<span class="mono">' + esc(when) + '</span></span><div class="bub ' + (m.who === 'person' ? 'ai person' : m.who) + '">' + esc(m.text) + '</div>';
    convo.appendChild(d); scrollConvo();
  }
  function addField(f) {
    if (!fields) return;
    var d = document.createElement('div'); d.className = 'd60field';
    d.innerHTML = '<b>' + esc(f.k) + '</b><span>' + esc(f.v) + '</span><i class="ok">' + esc(f.src) + '</i>';
    fields.appendChild(d);
  }
  function addWork(w) {
    if (!work) return;
    var d = document.createElement('div'); d.className = 'd60work';
    d.innerHTML = '<i>' + esc(w.icon) + '</i><div><b>' + esc(w.k) + '</b><span>' + esc(w.v) + '</span></div>';
    work.appendChild(d);
  }
  function addMorning(m) {
    if (!morningList) return;
    if (morning) morning.hidden = false;
    var d = document.createElement('div'); d.className = 'd60work';
    d.innerHTML = '<i>' + esc(m.icon) + '</i><div><b>' + esc(m.k) + '</b><span>' + esc(m.v) + '</span></div>';
    morningList.appendChild(d);
  }
  function showRecord() { if (record) record.classList.add('on'); }
  function showMerge() {
    if (!record) return;
    record.classList.add('merged');
    var chip = record.querySelector('[data-d60-chans]');
    if (chip && !chip.querySelector('.d60wa')) chip.insertAdjacentHTML('beforeend', ' <i class="d60wa">' + t('카카오톡', 'WhatsApp') + '</i>');
    var note = record.querySelector('[data-d60-match]'); if (note) note.hidden = false;
  }
  function setState(s) {
    root.setAttribute('data-state', s);
    if (!stateEl) return;
    stateEl.textContent = s === 'ring' ? t('수신 전화 · 벨 울림', 'Incoming call · ringing')
      : s === 'live' ? t('통화 중', 'On the call')
      : s === 'ended' ? t('통화 종료', 'Call ended')
      : s === 'chat' ? t('카카오톡 · 다음 날 아침', 'WhatsApp · next morning')
      : s === 'morning' ? t('사장님 화면 · 오전 9:00', 'Owner’s screen · 9:00 AM') : '';
  }
  function setChapter(n) {
    tabs.forEach(function (tb) { tb.classList.toggle('on', tb.getAttribute('data-d60-tab') === String(n)); tb.setAttribute('aria-selected', tb.getAttribute('data-d60-tab') === String(n) ? 'true' : 'false'); });
  }

  /* ── applying steps ────────────────────────────────────────── */
  var idx = 0, t0 = 0, paused = true, doneAll = false, raf = 0, elapsed = 0, chapter = 1;

  function apply(step, silent) {
    if (step.chapter) { chapter = step.chapter; setChapter(chapter); }
    if (step.state) { setState(step.state); if (!silent && step.state === 'ring') tone([440, 480], 1.6, 0.04); if (step.state === 'ended') stopAudio(); }
    if (step.sys) addSys(step.sys);
    if (step.line !== undefined) {
      addMsg({ who: step.who, text: step.text }, clock(step.at - 2.4), null);
      if (!silent) playLine(step.line, step.who);
    }
    if (step.chat) { addMsg(step.chat, step.chat.when, step.person ? 'wa' : 'wa'); if (!silent) tone([880], 0.09, 0.03); if (step.chat.merge) showMerge(); if (step.chat.handoff && hand) hand.hidden = false; }
    if (step.field) addField(step.field);
    if (step.crm) showRecord();
    if (step.work) addWork(step.work);
    if (step.morning) addMorning(step.morning);
    if (step.done) finish();
  }

  function reset() {
    idx = 0; elapsed = 0; doneAll = false; chapter = 1;
    stopAudio();
    convo.innerHTML = '';
    if (fields) fields.innerHTML = '';
    if (work) work.innerHTML = '';
    if (morningList) morningList.innerHTML = '';
    if (morning) morning.hidden = true;
    if (record) {
      record.classList.remove('on', 'merged');
      var note = record.querySelector('[data-d60-match]'); if (note) note.hidden = true;
      var chip = record.querySelector('[data-d60-chans]'); if (chip) chip.innerHTML = '<i class="d60ph">' + t('전화', 'Phone') + '</i>';
    }
    if (hand) hand.hidden = true;
    if (endrow) endrow.hidden = true;
    if (barEl) barEl.style.width = '0%';
    if (timeEl) timeEl.textContent = '0:00';
    setChapter(1); setState('');
  }

  function finish() {
    doneAll = true; paused = true; stopAudio();
    btn.textContent = t('↺ 처음부터 다시', '↺ Play again');
    btn.setAttribute('aria-pressed', 'false');
    if (endrow) endrow.hidden = false;
    if (summaryEl) summaryEl.textContent = t('통화 ' + mmss(CHAPTER_AT[1] - 5) + ' · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 사장님이 자는 동안 끝났습니다.',
                                             'One ' + mmss(CHAPTER_AT[1] - 5) + ' call · four messages · what a person did: one reply. The rest happened while you slept.');
    root.classList.remove('playing');
    drawWave();
  }

  function frame(now) {
    if (paused) return;
    elapsed = (now - t0) / 1000;
    if (barEl) barEl.style.width = Math.min(100, elapsed / TOTAL * 100) + '%';
    if (timeEl) timeEl.textContent = mmss(elapsed);
    while (idx < STEPS.length && STEPS[idx].at <= elapsed) apply(STEPS[idx++], false);
    drawWave();
    if (idx < STEPS.length) raf = requestAnimationFrame(frame); else drawWave();
  }

  function play() {
    if (!STEPS.length) return;
    ensureCtx();
    if (ctx && ctx.state === 'suspended') ctx.resume();
    if (doneAll) reset();
    paused = false;
    root.classList.add('playing');
    btn.textContent = t('⏸ 일시정지', '⏸ Pause');
    btn.setAttribute('aria-pressed', 'true');
    if (current && voiceOn) { var p = current.play(); if (p && p.catch) p.catch(function () {}); }
    t0 = performance.now() - elapsed * 1000;
    raf = requestAnimationFrame(frame);
  }
  function pause() {
    paused = true;
    root.classList.remove('playing');
    btn.textContent = t('▶ 이어서', '▶ Resume');
    btn.setAttribute('aria-pressed', 'false');
    cancelAnimationFrame(raf);
    if (current) { try { current.pause(); } catch (e) {} }
    drawWave();
  }
  function seek(sec) {  /* jump to a chapter start: replay everything before it silently */
    var wasPaused = paused;
    cancelAnimationFrame(raf); stopAudio();
    reset();
    elapsed = sec;
    while (idx < STEPS.length && STEPS[idx].at < sec) apply(STEPS[idx++], true);
    if (barEl) barEl.style.width = Math.min(100, sec / TOTAL * 100) + '%';
    if (timeEl) timeEl.textContent = mmss(sec);
    if (!wasPaused || doneAll) { doneAll = false; play(); } else { doneAll = false; }
  }

  btn.addEventListener('click', function () { (paused ? play : pause)(); });
  if (restartBtn) restartBtn.addEventListener('click', function () { cancelAnimationFrame(raf); reset(); play(); });
  if (capBtn) capBtn.addEventListener('click', function () {
    voiceOn = !voiceOn;
    capBtn.setAttribute('aria-pressed', voiceOn ? 'false' : 'true');
    capBtn.textContent = voiceOn ? t('자막만 보기', 'Captions only') : t('음성 켜기', 'Voice on');
    if (!voiceOn) stopAudio();
  });
  tabs.forEach(function (tb) { tb.addEventListener('click', function () { var n = +tb.getAttribute('data-d60-tab') || 1; seek(CHAPTER_AT[n - 1]); }); });

  /* arriving via the hero CTA (#demo60) starts it once, when visible */
  var autolaunched = false;
  function autoplayIfAsked() {
    if (autolaunched || !STEPS.length) return;
    if (location.hash === '#demo60') { autolaunched = true; setTimeout(play, 600); }
  }
  document.addEventListener('visibilitychange', function () { if (document.hidden && !paused) pause(); });
  window.addEventListener('hashchange', autoplayIfAsked);

  /* ── boot: the manifest carries each line's length ─────────── */
  fetch(AUDIO_BASE + 'manifest.json?v=' + VER, { cache: 'force-cache' })
    .then(function (r) { return r.ok ? r.json() : null; })
    .catch(function () { return null; })
    .then(function (man) {
      build(man || {});
      drawWave();
      if (REDUCED) {
        STEPS.forEach(function (s) { if (!s.done) apply(s, true); });
        finish();
        btn.textContent = t('전체가 표시되어 있습니다', 'Shown in full');
        btn.disabled = true;
      } else {
        autoplayIfAsked();
      }
    });

  /* ── the video cut (assets/video, built by build/demo_video.py) ─ */
  (function () {
    var dlg = root.querySelector('[data-d60-dialog]'), open = root.querySelector('[data-d60-video]');
    if (!dlg || !open || !dlg.showModal) { if (open) open.hidden = true; return; }
    var vid = dlg.querySelector('[data-d60-vid]'), base = vid.getAttribute('data-src'), cut = '';
    function load() { vid.src = base + cut + '.mp4?v=' + VER; vid.poster = base + cut + '.jpg'; dlg.classList.toggle('vert', cut !== ''); }
    open.addEventListener('click', function () { pause(); load(); dlg.showModal(); vid.play().catch(function () {}); });
    dlg.querySelector('[data-d60-close]').addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('close', function () { vid.pause(); vid.removeAttribute('src'); vid.load(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    Array.prototype.forEach.call(dlg.querySelectorAll('[data-d60-cut]'), function (b) {
      b.addEventListener('click', function () {
        cut = b.getAttribute('data-d60-cut'); var at = vid.currentTime;
        Array.prototype.forEach.call(dlg.querySelectorAll('[data-d60-cut]'), function (x) { x.classList.toggle('on', x === b); });
        load(); vid.currentTime = at; vid.play().catch(function () {});
      });
    });
  })();
})();
