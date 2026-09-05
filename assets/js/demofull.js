/* ══════════════════════════════════════════════════════════════════
   SR_DEMO v2 — the full demo, driven by a per-industry script.
   ──────────────────────────────────────────────────────────────────
   The player reads assets/demo/<slug>.json (one script per industry,
   both languages) and plays chapter 1 with real audio: two synthetic
   voices made with neural TTS, the customer routed through a phone-line
   filter so the waveform and the ear both know who is talking. Chapters
   2 and 3 are text: KakaoTalk / WhatsApp the next morning, then the
   owner's screen at nine.

   Rules carried over from the rest of the site:
   · Every figure comes from the script, which is labelled as a
     simulation with an example price list; the voices as synthetic.
   · Text lives in the DOM; the canvas only draws the waveform.
   · prefers-reduced-motion gets the finished state, not a fast run.
   · Nothing plays until the visitor presses play.

   Markup contract (build/demo_block.py):
     [data-d60 data-d60-script=".../assets/demo/dental.json" data-d60-audio=".../assets/audio/demo/"]
     [data-d60-pick]   optional <select> of slugs — switches the script
     [data-d60-speed]  optional button cycling 1× / 1.25× / 1.5×
   ══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var root = document.querySelector('[data-d60]');
  if (!root) return;

  var KO = (document.documentElement.lang || '').indexOf('ko') === 0;
  var LANG = KO ? 'ko' : 'en';
  function t(ko, en) { return KO ? ko : en; }
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var VER = (function () {
    var l = document.querySelector('link[href*="site.css?v="]');
    var m = l && l.getAttribute('href').match(/v=([0-9.]+)/);
    return m ? m[1] : '1';
  })();
  var AUDIO_BASE = root.getAttribute('data-d60-audio') || '../assets/audio/demo/';
  var SCRIPT_URL = root.getAttribute('data-d60-script') || '../assets/demo/dental.json';

  /* ── DOM ───────────────────────────────────────────────────────── */
  function q(s) { return root.querySelector(s); }
  var convo = q('[data-d60-convo]'), fields = q('[data-d60-fields]'), record = q('[data-d60-record]'),
      work = q('[data-d60-work]'), hand = q('[data-d60-handoff]'), morning = q('[data-d60-morning]'),
      morningList = q('[data-d60-morninglist]'), barEl = q('[data-d60-bar]'), timeEl = q('[data-d60-time]'),
      totalEl = q('[data-d60-total]'), btn = q('[data-d60-play]'), capBtn = q('[data-d60-caption]'),
      restartBtn = q('[data-d60-restart]'), endrow = q('[data-d60-end]'), stateEl = q('[data-d60-callstate]'),
      speakerEl = q('[data-d60-speaker]'), wave = q('[data-d60-wave]'), summaryEl = q('[data-d60-summary]'),
      bizEl = q('[data-d60-biz]'), metaEl = q('[data-d60-meta]'), custEl = q('[data-d60-custname]'),
      handList = q('[data-d60-handlist]'), honestEl = q('[data-d60-honest]'), pick = q('[data-d60-pick]'),
      speedBtn = q('[data-d60-speed]'), videoBtn = q('[data-d60-video]'), callerEl = q('[data-d60-caller]');
  var tabs = Array.prototype.slice.call(root.querySelectorAll('[data-d60-tab]'));
  if (!convo || !btn) return;

  /* ── script state ──────────────────────────────────────────────── */
  var S = null, SLUG = '', STEPS = [], TOTAL = 0, CHAPTER_AT = [0, 0, 0], CALL_LEN = 0;
  var SPEED = 1;

  function mmss(s) { s = Math.max(0, Math.round(s)); return Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2); }

  /* the call clock: script callTime (e.g. "11:42 PM") + seconds into the call */
  var clockBase = 23 * 3600 + 42 * 60;
  function parseClock(s) {
    var m = /(\d{1,2}):(\d{2})\s*(AM|PM)?/i.exec(s || '');
    if (!m) return 23 * 3600 + 42 * 60;
    var h = +m[1] % 12, mi = +m[2];
    if ((m[3] || '').toUpperCase() === 'PM') h += 12;
    return h * 3600 + mi * 60;
  }
  function clock(sec) {
    var base = clockBase + Math.round(sec);
    var h = Math.floor(base / 3600) % 24, m = Math.floor(base / 60) % 60, s = base % 60;
    var pm = h >= 12;
    return (KO ? (pm ? '오후 ' : '오전 ') : '') + ((h % 12) || 12) + ':' + ('0' + m).slice(-2) + ':' + ('0' + s).slice(-2) + (KO ? '' : (pm ? ' PM' : ' AM'));
  }

  function build(sc) {
    S = sc; STEPS = []; var cur = 0; CHAPTER_AT = [0, 0, 0];
    clockBase = parseClock(S.callTime);
    STEPS.push({ at: 0, chapter: 1, state: 'ring', sys: S.sys.ring });
    cur = 2.4;
    (S.lines || []).forEach(function (ln, i) {
      var dur = ln.dur || Math.max(2.5, ln.text.length * (KO ? 0.16 : 0.06));
      STEPS.push({ at: cur, chapter: 1, line: i, who: ln.who, text: ln.text, dur: dur, state: i === 0 ? 'live' : null });
      (ln.side || []).forEach(function (s, j) {
        var st = { at: cur + Math.min(dur * 0.7, 1.4 + j * 1.1) };
        if (s.crm) st.crm = true; else if (s.field) st.field = s.field; else if (s.work) st.work = s.work;
        STEPS.push(st);
      });
      cur += dur + 0.7;
    });
    CALL_LEN = cur - 2.4;
    STEPS.push({ at: cur, state: 'ended', sys: t('통화 종료 · ', 'Call ended · ') + mmss(CALL_LEN) });
    cur += 2.6;
    CHAPTER_AT[1] = cur;
    STEPS.push({ at: cur, chapter: 2, state: 'chat', sys: S.sys.chat });
    cur += 2.4;
    (S.chat || []).forEach(function (m) { STEPS.push({ at: cur, chat: m }); cur += m.who === 'ai' ? 5.2 : 3.6; });
    cur += 0.8;
    CHAPTER_AT[2] = cur;
    STEPS.push({ at: cur, chapter: 3, state: 'morning', sys: S.sys.morning });
    cur += 2.2;
    (S.morning || []).forEach(function (m) { STEPS.push({ at: cur, morning: m }); cur += 2.3; });
    if (S.person) { STEPS.push({ at: cur, chat: { who: 'person', when: S.person.when, text: S.person.text }, person: true }); cur += 5.5; }
    STEPS.push({ at: cur, done: true });
    TOTAL = cur + 0.5;
    STEPS.sort(function (a, b) { return a.at - b.at; });
    if (totalEl) totalEl.textContent = mmss(TOTAL);
    tabs.forEach(function (tb, i) {
      var b = tb.querySelector('b'), r = tb.querySelector('[data-d60-range]');
      if (b && S.chapters && S.chapters[i]) b.textContent = (i + 1) + ' · ' + S.chapters[i];
      var end = i < 2 ? CHAPTER_AT[i + 1] : TOTAL;
      if (r) r.textContent = ((S.chapterSubs && S.chapterSubs[i]) || r.getAttribute('data-base') || '') + ' · ' + mmss(CHAPTER_AT[i]) + '–' + mmss(end);
    });
    /* static parts of the stage */
    if (bizEl) bizEl.textContent = S.biz || '';
    if (metaEl) metaEl.textContent = S.meta || '';
    if (custEl) custEl.textContent = (S.customer && S.customer.name) || '';
    if (callerEl) callerEl.textContent = S.customer ? (S.customer.phone || '') : '';
    if (handList) handList.innerHTML = (S.handoff || []).map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('');
    if (honestEl && S.honest) honestEl.firstChild && honestEl.firstChild.nodeType === 3 ? (honestEl.firstChild.textContent = S.honest + ' ') : (honestEl.textContent = S.honest);
    if (videoBtn) videoBtn.hidden = !S.video;
  }

  /* ── audio ─────────────────────────────────────────────────────── */
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
    var key = SLUG + ':' + i;
    if (cache[key]) return cache[key];
    var ln = S.lines[i]; if (!ln || !ln.file) return null;
    var a = new Audio(AUDIO_BASE + SLUG + '/' + LANG + '/' + ln.file + '?v=' + VER);
    a.preload = 'auto';
    if (ctx) {
      try {
        var src = ctx.createMediaElementSource(a);
        if (ln.who === 'user') {  /* a phone line: narrow band, a little hotter */
          var bp = ctx.createBiquadFilter(); bp.type = 'bandpass'; bp.frequency.value = 1500; bp.Q.value = 0.7;
          var g = ctx.createGain(); g.gain.value = 1.7;
          src.connect(bp); bp.connect(g); g.connect(analyser);
        } else { src.connect(analyser); }
      } catch (e) { /* plain playback */ }
    }
    cache[key] = a;
    return a;
  }
  function stopAudio() { if (current) { try { current.pause(); } catch (e) {} current = null; } curWho = null; if (speakerEl) speakerEl.textContent = ''; }
  function playLine(i, who) {
    stopAudio();
    curWho = who;
    if (speakerEl) speakerEl.textContent = who === 'user' ? t('손님이 말하는 중 · 전화 음질', 'Customer speaking · phone line') : t('AI가 답하는 중', 'AI speaking');
    if (!voiceOn) return;
    var a = audioFor(i); if (!a) return;
    current = a;
    try { a.currentTime = 0; a.playbackRate = SPEED; } catch (e) {}
    var p = a.play(); if (p && p.catch) p.catch(function () {});
    if (S.lines[i + 1]) audioFor(i + 1);
  }
  function tone(freqs, secs, gain) {
    if (!ctx || !voiceOn) return;
    try {
      var g = ctx.createGain(); g.gain.value = gain; g.connect(ctx.destination);
      freqs.forEach(function (f) { var o = ctx.createOscillator(); o.type = 'sine'; o.frequency.value = f; o.connect(g); o.start(); o.stop(ctx.currentTime + secs); });
      g.gain.setValueAtTime(gain, ctx.currentTime + secs - 0.05); g.gain.linearRampToValueAtTime(0, ctx.currentTime + secs);
    } catch (e) {}
  }

  var wctx = wave && wave.getContext && wave.getContext('2d'), wdata = null;
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

  /* ── stage rendering ───────────────────────────────────────────── */
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function scrollConvo() { convo.scrollTop = convo.scrollHeight; }
  function addSys(text) {
    var d = document.createElement('div'); d.className = 'd60sys'; d.textContent = text; convo.appendChild(d); scrollConvo();
  }
  var activeCap = null;  /* progressive caption of the line being spoken */
  function addMsg(m, when, chan, progressive, at, dur) {
    var d = document.createElement('div');
    d.className = 'd60msg ' + m.who + (chan ? ' ' + chan : '');
    var who = m.who === 'user' ? t('손님', 'Customer') : m.who === 'ai' ? 'AI' : t('담당자', 'Front desk');
    d.innerHTML = '<span class="d60who"><b>' + esc(who) + '</b>' + (chan ? '<i class="d60chan">' + esc(S.chan) + '</i>' : '') +
      '<span class="mono">' + esc(when) + '</span></span><div class="bub ' + (m.who === 'person' ? 'ai person' : m.who) + '"></div>';
    var bub = d.querySelector('.bub');
    if (progressive) { bub.textContent = ''; bub.classList.add('typing'); activeCap = { el: bub, text: m.text, at: at, dur: dur }; }
    else bub.textContent = m.text;
    convo.appendChild(d); scrollConvo();
  }
  function tickCaption(elapsed) {
    if (!activeCap) return;
    var f = Math.min(1, (elapsed - activeCap.at) / Math.max(0.5, activeCap.dur * 0.92));
    var n = Math.max(1, Math.floor(activeCap.text.length * f));
    if (activeCap.el.textContent.length !== n) { activeCap.el.textContent = activeCap.text.slice(0, n); scrollConvo(); }
    if (f >= 1) { activeCap.el.classList.remove('typing'); activeCap = null; }
  }
  function flushCaption() { if (activeCap) { activeCap.el.textContent = activeCap.text; activeCap.el.classList.remove('typing'); activeCap = null; } }
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
    if (chip && !chip.querySelector('.d60wa')) chip.insertAdjacentHTML('beforeend', ' <i class="d60wa">' + esc(S.chan) + '</i>');
    var note = record.querySelector('[data-d60-match]'); if (note) note.hidden = false;
  }
  function setState(s) {
    root.setAttribute('data-state', s);
    if (!stateEl) return;
    stateEl.textContent = s === 'ring' ? t('수신 전화 · 벨 울림', 'Incoming call · ringing')
      : s === 'live' ? t('통화 중', 'On the call')
      : s === 'ended' ? t('통화 종료', 'Call ended')
      : s === 'chat' ? (S.chan + t(' · 다음 날 아침', ' · next morning'))
      : s === 'morning' ? t('사장님 화면 · 오전 9:00', 'Owner’s screen · 9:00 AM') : '';
  }
  function setChapter(n) {
    tabs.forEach(function (tb) { var on = tb.getAttribute('data-d60-tab') === String(n); tb.classList.toggle('on', on); tb.setAttribute('aria-selected', on ? 'true' : 'false'); });
  }

  /* ── applying steps ────────────────────────────────────────────── */
  var idx = 0, t0 = 0, paused = true, doneAll = false, raf = 0, elapsed = 0, chapter = 1;

  function apply(step, silent) {
    if (step.chapter) { chapter = step.chapter; setChapter(chapter); }
    if (step.state) { setState(step.state); if (!silent && step.state === 'ring') tone([440, 480], 1.6, 0.04); if (step.state === 'ended') stopAudio(); }
    if (step.sys) addSys(step.sys);
    if (step.line !== undefined) {
      flushCaption();
      addMsg({ who: step.who, text: step.text }, clock(step.at - 2.4), null, !silent && !REDUCED, step.at, step.dur);
      if (!silent) playLine(step.line, step.who);
    }
    if (step.chat) {
      addMsg(step.chat, step.chat.when, 'wa');
      if (!silent) tone([880], 0.09, 0.03);
      if (step.chat.merge) showMerge();
      if (step.chat.handoff && hand) { hand.hidden = false; root.classList.add('handoff'); }
    }
    if (step.field) addField(step.field);
    if (step.crm) showRecord();
    if (step.work) addWork(step.work);
    if (step.morning) addMorning(step.morning);
    if (step.done) finish();
  }

  function reset() {
    idx = 0; elapsed = 0; doneAll = false; chapter = 1; activeCap = null;
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
    root.classList.remove('handoff');
    if (endrow) endrow.hidden = true;
    if (barEl) barEl.style.width = '0%';
    if (timeEl) timeEl.textContent = '0:00';
    setChapter(1); setState('');
  }

  function finish() {
    doneAll = true; paused = true; stopAudio(); flushCaption();
    btn.textContent = t('↺ 처음부터 다시', '↺ Play again');
    btn.setAttribute('aria-pressed', 'false');
    if (endrow) endrow.hidden = false;
    if (summaryEl) summaryEl.textContent = (S.summary || '').replace('{call}', mmss(CALL_LEN));
    root.classList.remove('playing');
    drawWave();
  }

  function frame(now) {
    if (paused) return;
    elapsed = (now - t0) / 1000 * SPEED;
    if (barEl) barEl.style.width = Math.min(100, elapsed / TOTAL * 100) + '%';
    if (timeEl) timeEl.textContent = mmss(elapsed);
    while (idx < STEPS.length && STEPS[idx].at <= elapsed) apply(STEPS[idx++], false);
    tickCaption(elapsed);
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
    if (current && voiceOn) { try { current.playbackRate = SPEED; } catch (e) {} var p = current.play(); if (p && p.catch) p.catch(function () {}); }
    t0 = performance.now() - elapsed / SPEED * 1000;
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
  function seek(sec) {
    var wasPaused = paused;
    cancelAnimationFrame(raf); stopAudio();
    reset();
    elapsed = sec;
    while (idx < STEPS.length && STEPS[idx].at < sec) apply(STEPS[idx++], true);
    if (barEl) barEl.style.width = Math.min(100, sec / TOTAL * 100) + '%';
    if (timeEl) timeEl.textContent = mmss(sec);
    if (!wasPaused || doneAll) { doneAll = false; play(); } else { doneAll = false; }
  }
  function setSpeed(v) {
    var wasPaused = paused;
    if (!wasPaused) { cancelAnimationFrame(raf); paused = true; }
    SPEED = v;
    if (speedBtn) { speedBtn.textContent = (v === 1 ? '1×' : v === 1.25 ? '1.25×' : '1.5×'); speedBtn.setAttribute('aria-label', t('재생 속도 ', 'Playback speed ') + v + 'x'); }
    if (current) { try { current.playbackRate = v; } catch (e) {} }
    if (!wasPaused) { paused = false; t0 = performance.now() - elapsed / SPEED * 1000; raf = requestAnimationFrame(frame); }
  }

  btn.addEventListener('click', function () { (paused ? play : pause)(); });
  if (restartBtn) restartBtn.addEventListener('click', function () { cancelAnimationFrame(raf); reset(); play(); });
  if (capBtn) capBtn.addEventListener('click', function () {
    voiceOn = !voiceOn;
    capBtn.setAttribute('aria-pressed', voiceOn ? 'false' : 'true');
    capBtn.textContent = voiceOn ? t('자막만 보기', 'Captions only') : t('음성 켜기', 'Voice on');
    if (!voiceOn) stopAudio();
  });
  if (speedBtn) speedBtn.addEventListener('click', function () { setSpeed(SPEED === 1 ? 1.25 : SPEED === 1.25 ? 1.5 : 1); });
  tabs.forEach(function (tb) { tb.addEventListener('click', function () { var n = +tb.getAttribute('data-d60-tab') || 1; seek(CHAPTER_AT[n - 1]); }); });

  /* ── loading a script (and switching industries) ───────────────── */
  function loadScript(url, slug, then) {
    fetch(url + '?v=' + VER, { cache: 'force-cache' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; })
      .then(function (j) {
        var sc = j && (j[LANG] || j.ko || j.en);
        if (!sc) { if (then) then(false); return; }
        SLUG = slug;
        build(sc);
        if (then) then(true);
      });
  }
  function slugOf(url) { var m = /([a-z0-9-]+)\.json/i.exec(url || ''); return m ? m[1] : 'dental'; }

  if (pick) pick.addEventListener('change', function () {
    var slug = pick.value; if (!slug) return;
    var wasPlaying = !paused;
    cancelAnimationFrame(raf); paused = true; stopAudio(); root.classList.remove('playing');
    var url = SCRIPT_URL.replace(/[a-z0-9-]+\.json$/i, slug + '.json');
    loadScript(url, slug, function (ok) {
      if (!ok) return;
      reset(); drawWave();
      btn.textContent = t('▶ 재생 — 듣고 보기', '▶ Play — watch and listen');
      if (REDUCED) { STEPS.forEach(function (s) { if (!s.done) apply(s, true); }); finish(); }
      else if (wasPlaying) play();
      try { history.replaceState(null, '', location.pathname + location.search + '#demo60'); } catch (e) {}
    });
  });

  var autolaunched = false;
  function autoplayIfAsked() {
    if (autolaunched || !STEPS.length) return;
    if (location.hash === '#demo60') { autolaunched = true; setTimeout(play, 600); }
  }
  document.addEventListener('visibilitychange', function () { if (document.hidden && !paused) pause(); });
  window.addEventListener('hashchange', autoplayIfAsked);

  /* ── boot ──────────────────────────────────────────────────────── */
  loadScript(SCRIPT_URL, slugOf(SCRIPT_URL), function (ok) {
    drawWave();
    if (!ok) { btn.disabled = true; btn.textContent = t('데모를 불러오지 못했습니다', 'The demo could not load'); return; }
    if (pick && pick.value !== SLUG) { try { pick.value = SLUG; } catch (e) {} }
    if (REDUCED) {
      STEPS.forEach(function (s) { if (!s.done) apply(s, true); });
      finish();
      btn.textContent = t('전체가 표시되어 있습니다', 'Shown in full');
      btn.disabled = true;
    } else {
      autoplayIfAsked();
    }
  });

  /* ── the video cut (assets/video, built by build/demo_video.py) — dental only */
  (function () {
    var dlg = root.querySelector('[data-d60-dialog]'), open = videoBtn;
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
