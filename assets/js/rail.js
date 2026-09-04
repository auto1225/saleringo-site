/* ── where you are on a page that is longer than a screen ──────────────────
   These pages are long by design - a trade page is a whole argument - and the
   cost of that is a reader who cannot tell whether they are a third of the way
   through or nine tenths, and cannot get back to the part they wanted.

   So the page carries a map of itself down the left edge: one mark per
   section, drawn on a canvas, with the section you are reading lit, the ones
   you have passed filled and the ones ahead as hairlines. A thin line grows
   through the marks as you scroll, so the map doubles as a progress bar. The
   mark you hover names its section; the mark you press scrolls to it.

   Why canvas rather than 20 divs: the rail redraws on every scroll frame, and
   a canvas draws the whole thing in one pass with no layout and no style
   recalculation. It is also the only way to draw the connecting line as a
   continuous thing rather than as a stack of boxes pretending to be one.

   It is decoration for a screen reader - aria-hidden - because the same
   destinations are already in the page as headings, and a second list of them
   is noise in a screen reader's outline. Keyboard users get real buttons: the
   canvas sits under an invisible list of links that focus normally.

   It hides itself when the page is short, when the window is narrow, when
   there is no room beside the content, and when the reader has asked for
   reduced motion it draws without the easing rather than not at all.        */
(function () {
  'use strict';

  var MIN_SECTIONS = 4;
  var MIN_PAGE = 2200;          /* shorter than this and there is nothing to map */
  var MIN_VIEWPORT = 1180;      /* narrower and the rail would sit on the words */

  var main = document.querySelector('main');
  if (!main) return;

  function title(sec) {
    var h = sec.querySelector('h2, .h2, h3, .room-h, .eyebrow');
    var t = h ? h.textContent : '';
    t = (t || '').replace(/\s+/g, ' ').trim();
    /* the eyebrow is often the better label - shorter, and already a name */
    var eb = sec.querySelector('.eyebrow');
    if (eb) {
      var e = eb.textContent.replace(/\s+/g, ' ').trim();
      if (e && e.length <= 34) t = e;
    }
    if (t.length > 40) t = t.slice(0, 38).replace(/[\s,.;:-]+$/, '') + '…';
    return t || 'Section';
  }

  var secs = [];
  [].forEach.call(main.querySelectorAll(':scope > section'), function (s) {
    if (s.offsetHeight < 200) return;
    secs.push({ el: s, name: title(s) });
  });

  /* Not every page is built out of top-level sections. The privacy policy and
     the terms are three sections holding numbered clauses; the buyer's guide
     is a document with no <section> at all; the site map's sections are mostly
     shorter than the 200px floor. Those are exactly the pages a reader gets
     lost in, and the first version of this rail skipped all four of them.

     So when the sections do not describe the page, the headings do. */
  if (secs.length < MIN_SECTIONS) {
    secs = [];
    var seen = [];
    [].forEach.call(main.querySelectorAll('h2, h3, .h2'), function (h) {
      if (h.closest('.pspanel[hidden]')) return;
      if (!h.getClientRects().length) return;
      var t = (h.textContent || '').replace(/\s+/g, ' ').trim();
      if (!t || t.length < 3) return;
      /* scroll to the block that holds the heading, not to the heading */
      var target = h.closest('section, article, .docsec, .doc, .wrap') || h;
      if (seen.indexOf(target) >= 0 && seen.length) {
        /* several headings in one block: keep the heading itself as the mark */
        target = h;
      }
      seen.push(target);
      if (t.length > 40) t = t.slice(0, 38).replace(/[\s,.;:-]+$/, '') + '…';
      secs.push({ el: target, name: t });
    });
    /* a document with fifty clauses does not want fifty marks */
    if (secs.length > 16) {
      var step = Math.ceil(secs.length / 16), thin = [];
      for (var q = 0; q < secs.length; q += step) thin.push(secs[q]);
      secs = thin;
    }
  }
  /* A page whose body is one tab strip already answers "where am I" better
     than a rail could: the strip names every part and shows which one is open.
     The pack pages are exactly that shape - one panelset and a way back - so
     the rail stands down rather than competing with the control beside it. */
  var sets = main.querySelectorAll('.panelset');
  if (sets.length === 1 && main.querySelectorAll(':scope > section').length < 4) return;

  if (secs.length < MIN_SECTIONS) return;
  if (document.documentElement.scrollHeight < MIN_PAGE) return;

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var rail = document.createElement('div');
  rail.className = 'pagerail';
  rail.innerHTML = '<canvas class="pagerail-cv" aria-hidden="true"></canvas>' +
                   '<ul class="pagerail-keys"></ul>' +
                   '<span class="pagerail-tip" aria-hidden="true"></span>';
  document.body.appendChild(rail);

  var cv = rail.querySelector('canvas');
  var ctx = cv.getContext('2d');
  var keys = rail.querySelector('.pagerail-keys');
  var tip = rail.querySelector('.pagerail-tip');

  /* the keyboard path: real links, visually hidden, in the same order */
  secs.forEach(function (s, i) {
    if (!s.el.id) s.el.id = 'sec-' + (i + 1);
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.href = '#' + s.el.id;
    a.textContent = s.name;
    li.appendChild(a);
    keys.appendChild(li);
  });

  var W = 26, dpr = 1, H = 0;
  var marks = [];              /* y position of each mark, in css px */
  var active = 0, progress = 0, shown = 0;

  function size() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    var r = rail.getBoundingClientRect();
    H = Math.max(120, Math.round(r.height));
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(H * dpr);
    cv.style.width = W + 'px';
    cv.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    layout();
  }

  function layout() {
    var pad = 14;
    var span = H - pad * 2;
    marks = secs.map(function (s, i) {
      return pad + (secs.length === 1 ? 0 : span * i / (secs.length - 1));
    });
  }

  function ink(name, fallback) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return v || fallback;
  }

  function draw() {
    if (!H) return;
    var teal = ink('--teal', '#0B7878');
    var hair = 'rgba(20,26,31,.208)';
    var soft = 'rgba(20,26,31,.42)';
    ctx.clearRect(0, 0, W, H);

    var x = W / 2;
    var top = marks[0], bottom = marks[marks.length - 1];

    /* the track */
    ctx.strokeStyle = hair;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x, top);
    ctx.lineTo(x, bottom);
    ctx.stroke();

    /* the part of the page already read */
    var y = top + (bottom - top) * shown;
    ctx.strokeStyle = teal;
    ctx.lineWidth = 1.5;
    ctx.globalAlpha = 0.85;
    ctx.beginPath();
    ctx.moveTo(x, top);
    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.globalAlpha = 1;

    /* the marks */
    marks.forEach(function (my, i) {
      var isNow = i === active;
      var passed = my <= y + 0.5;
      ctx.beginPath();
      if (isNow) {
        ctx.fillStyle = teal;
        ctx.arc(x, my, 4.2, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.strokeStyle = teal;
        ctx.globalAlpha = 0.3;
        ctx.lineWidth = 1;
        ctx.arc(x, my, 8, 0, Math.PI * 2);
        ctx.stroke();
        ctx.globalAlpha = 1;
      } else {
        ctx.fillStyle = passed ? soft : hair;
        ctx.arc(x, my, 2.4, 0, Math.PI * 2);
        ctx.fill();
      }
    });
  }

  function measure() {
    var vh = window.innerHeight;
    var mid = window.pageYOffset + vh * 0.38;
    var best = 0;
    secs.forEach(function (s, i) {
      var top = s.el.getBoundingClientRect().top + window.pageYOffset;
      if (top <= mid) best = i;
    });
    active = best;

    var docH = document.documentElement.scrollHeight - vh;
    progress = docH > 0 ? Math.min(1, Math.max(0, window.pageYOffset / docH)) : 0;
  }

  var raf = null;
  function tick() {
    raf = null;
    measure();
    if (reduce) { shown = progress; draw(); return; }
    var step = function () {
      shown += (progress - shown) * 0.18;
      if (Math.abs(progress - shown) < 0.0015) { shown = progress; draw(); return; }
      draw();
      requestAnimationFrame(step);
    };
    step();
  }
  function onScroll() { if (!raf) raf = requestAnimationFrame(tick); }

  /* pointer: name the mark under the cursor, jump on press */
  function markAt(clientY) {
    var r = cv.getBoundingClientRect();
    var y = clientY - r.top;
    var best = -1, dist = 12;
    marks.forEach(function (my, i) {
      var d = Math.abs(my - y);
      if (d < dist) { dist = d; best = i; }
    });
    return best;
  }
  rail.addEventListener('mousemove', function (e) {
    var i = markAt(e.clientY);
    if (i < 0) { tip.classList.remove('on'); rail.style.cursor = ''; return; }
    tip.textContent = secs[i].name;
    tip.style.top = marks[i] + 'px';
    tip.classList.add('on');
    rail.style.cursor = 'pointer';
  });
  rail.addEventListener('mouseleave', function () { tip.classList.remove('on'); });
  rail.addEventListener('click', function (e) {
    var i = markAt(e.clientY);
    if (i < 0) return;
    secs[i].el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  });

  function fits() {
    return window.innerWidth >= MIN_VIEWPORT &&
           document.documentElement.scrollHeight > MIN_PAGE;
  }
  function toggle() {
    rail.classList.toggle('on', fits());
    if (!fits()) return;
    size();
    /* Paint once, synchronously. The animated path runs inside
       requestAnimationFrame, and a frame callback is not guaranteed to fire
       promptly in a background or throttled tab - which would leave a blank
       canvas where the map should be. */
    measure();
    shown = progress;
    draw();
    onScroll();
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { toggle(); }, { passive: true });
  if (window.ResizeObserver) new ResizeObserver(function () { size(); draw(); }).observe(rail);
  toggle();
})();
