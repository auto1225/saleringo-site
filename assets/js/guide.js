/* ═══════════════════════════════════════════════════════════════════════════
   PART 1 — the header menus
   ───────────────────────────────────────────────────────────────────────────
   The header carried five links; the footer carried twenty-six. Twenty-one
   destinations were reachable only from the bottom of a thirteen-screen page,
   which is to say not reachable. Each top-level item is now a disclosure
   button over a panel of the pages beneath it.

   Everything here is click and keyboard. There is deliberately no hover
   trigger: a hover menu cannot be opened from a keyboard and misfires on
   touch, and this site is majority-mobile.

     button      Enter / Space   toggle (native <button>, no script needed)
                 ArrowDown       open and land on the first link
                 Escape          close
     panel       ArrowDown/Up    move between links
                 Home / End      first / last link
                 Escape          close and return focus to the button
                 Tab past end    closes on its way out (focusout)
   ═══════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var nav = document.querySelector('.nav');
  if (!nav) return;

  var items = [].slice.call(nav.querySelectorAll('.navitem'));
  if (!items.length) return;

  var open = null;
  var burger = nav.querySelector('.burger');

  function panelOf(btn) { return document.getElementById(btn.getAttribute('aria-controls')); }
  function linksIn(p) {
    return [].slice.call(p.querySelectorAll('a[href]')).filter(function (a) {
      return a.getClientRects().length > 0;
    });
  }

  function close(btn, refocus) {
    if (!btn) return;
    var p = panelOf(btn);
    btn.setAttribute('aria-expanded', 'false');
    if (p) p.hidden = true;
    if (open === btn) open = null;
    if (refocus) btn.focus();
  }
  function closeAll() {
    items.forEach(function (it) { close(it.querySelector('.navtop'), false); });
  }

  function show(btn) {
    if (open && open !== btn) close(open, false);
    var p = panelOf(btn);
    if (!p) return;
    p.hidden = false;
    btn.setAttribute('aria-expanded', 'true');
    open = btn;
  }

  items.forEach(function (item) {
    var btn = item.querySelector('.navtop');
    if (!btn || !panelOf(btn)) return;

    btn.addEventListener('click', function (ev) {
      ev.preventDefault();
      if (btn.getAttribute('aria-expanded') === 'true') close(btn, false);
      else show(btn);
    });

    btn.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowDown') {
        ev.preventDefault();
        show(btn);
        var l = linksIn(panelOf(btn));
        if (l.length) l[0].focus();
      } else if (ev.key === 'Escape') {
        close(btn, true);
      }
    });

    panelOf(btn).addEventListener('keydown', function (ev) {
      var l = linksIn(this), i = l.indexOf(document.activeElement);
      if (ev.key === 'Escape') { ev.preventDefault(); close(btn, true); }
      else if (ev.key === 'ArrowDown') { ev.preventDefault(); if (l.length) l[(i + 1 + l.length) % l.length].focus(); }
      else if (ev.key === 'ArrowUp')   { ev.preventDefault(); if (l.length) l[(i - 1 + l.length) % l.length].focus(); }
      else if (ev.key === 'Home')      { ev.preventDefault(); if (l.length) l[0].focus(); }
      else if (ev.key === 'End')       { ev.preventDefault(); if (l.length) l[l.length - 1].focus(); }
    });

    /* Tabbing out the far end of a panel has to close it, or the reader is
       left with an open overlay they can no longer see the focus inside. */
    item.addEventListener('focusout', function (ev) {
      if (!ev.relatedTarget) return;               /* focus left the document */
      if (item.contains(ev.relatedTarget)) return;
      close(btn, false);
    });
  });

  document.addEventListener('click', function (ev) {
    if (!open) return;
    if (ev.target.closest && ev.target.closest('.navitem')) return;
    close(open, false);
  });

  /* site.js owns the .open class on the mobile sheet and is not ours to edit,
     so this only reports the state it sets. site.js registers its click
     handler first (its script tag comes first), so by the time this one runs
     the class is already correct. */
  function syncBurger() {
    if (!burger) return;
    var links = nav.querySelector('.links');
    var isOpen = !!(links && links.classList.contains('open'));
    burger.setAttribute('aria-expanded', String(isOpen));
    if (!isOpen) closeAll();
  }
  if (burger) {
    burger.addEventListener('click', syncBurger);
    syncBurger();
  }

  document.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Escape') return;
    if (open) { close(open, true); return; }
    /* Escape also shuts the mobile sheet — the burger has no other way out. */
    var links = nav.querySelector('.links');
    if (links && links.classList.contains('open')) {
      links.classList.remove('open');
      syncBurger();
      if (burger) burger.focus();
    }
  });

  /* A resize across the 900px line swaps the panel between overlay and inline
     accordion; anything left open ends up in the wrong idiom. */
  var wasNarrow = window.matchMedia('(max-width:900px)').matches;
  window.addEventListener('resize', function () {
    var now = window.matchMedia('(max-width:900px)').matches;
    if (now !== wasNarrow) { wasNarrow = now; closeAll(); }
  });
}());

/* ═══════════════════════════════════════════════════════════════════════════
   PART 2a — the subject tours: the table, and which one is running
   ───────────────────────────────────────────────────────────────────────────
   The in-page tour further down walks one page. A subject tour walks the
   SITE: a reader picks a theme and is carried across the pages and anchors
   that answer it, using the same rail, docked in the same .stickycta, showing
   done / here / ahead.

   A tour is a query parameter (?tour=costs) remembered in sessionStorage so
   it survives every navigation until the reader ends it. ?tour=off ends it.
   Nothing is written to disk and nothing is sent anywhere.

   A step is { u: page, h: '#anchor', lab: rail label }. A step may instead
   carry sel — a CSS selector — for anchors whose id differs by page: the
   trade pages name their CRM section #dental-crm, #clinic-crm, #trades-crm,
   #stay-crm, #venue-crm and so on, so that step is written [id$="-crm"] and
   resolves on arrival. The six trade pages still being written will resolve
   the same way whatever they end up calling it.
   ═══════════════════════════════════════════════════════════════════════════ */
var SR_TOURS = {
  refuses: {
    title: 'What it refuses to do',
    steps: [
      { u: 'verified-ai.html', h: '#life',        lab: 'One answer' },
      { u: 'verified-ai.html', h: '#audit',       lab: 'The audit trail' },
      { u: 'index.html',       h: '#what-to-ask', lab: 'What to ask' },
      { u: 'pricing.html',     h: '#not-paying',  lab: 'Not paying for' },
      { u: 'security.html',    h: '#measures',    lab: 'The measures' },
      { u: 'privacy.html',     h: '#your-rights', lab: 'Your rights' }
    ]
  },
  keeps: {
    title: 'What it captures and keeps',
    steps: [
      { u: 'index.html',        h: '#what-it-keeps',    lab: 'What it keeps' },
      { u: 'platform.html',     h: '#inside',           lab: 'Inside one answer' },
      { u: 'voice.html',        h: '#after-the-call',   lab: 'After the call' },
      { u: 'webchat.html',      h: '#where-chats-land', lab: 'Where chats land' },
      { u: 'whatsapp.html',     h: '#one-inbox',        lab: 'One inbox' },
      { u: 'integrations.html', h: '#live-today',       lab: 'Where it syncs' },
      { u: 'privacy.html',      h: '#your-rights',      lab: 'And deletes' }
    ]
  },
  costs: {
    title: 'What it costs',
    steps: [
      { u: 'pricing.html',      h: '#alternatives',   lab: 'Compared to' },
      { u: 'pricing.html',      h: '#plans',          lab: 'The plans' },
      { u: 'pricing.html',      h: '#channels',       lab: 'Per channel' },
      { u: 'pricing.html',      h: '#calculator',     lab: 'Your number' },
      { u: 'pricing.html',      h: '#not-paying',     lab: 'Not paying for' },
      { u: 'pricing.html',      h: '#countries',      lab: 'Your currency' },
      { u: 'cross-border.html', h: '#both-timezones', lab: 'Two timezones' }
    ]
  },
  proof: {
    title: 'Prove it works',
    steps: [
      { u: 'demo.html',     h: '#yourprices',   lab: 'Your prices' },
      { u: 'index.html',    h: '#try',          lab: 'Try it here' },
      { u: 'index.html',    h: '#call-them',    lab: 'Call our AI' },
      { u: 'examples.html', h: '#pick-a-trade', lab: 'A real call' },
      { u: 'index.html',    h: '#calculator',   lab: 'The arithmetic' },
      { u: 'about.html',    h: '#people',       lab: 'Who built it' }
    ]
  },
  trade: {
    title: 'How it works in my trade',
    build: function (t) {
      var p = 'industries/' + (t || 'dental') + '.html';
      return [
        { u: 'industries.html', h: '#what-a-pack-is', lab: 'What a pack is' },
        { u: p, sel: '[id$="-crm"]',                  lab: 'Your CRM' },
        { u: p, h: '#worked-examples',                lab: 'Worked examples' },
        { u: p, h: '#the-pack',                       lab: 'In the pack' },
        { u: 'examples.html', h: '#pick-a-trade',     lab: 'A real call' },
        { u: 'pricing.html',  h: '#plans',            lab: 'What it costs' }
      ];
    }
  }
};

/* Which tour is running, if any. Read before anything else, because the
   in-page tour stands down while a subject tour is on: two rails docked in
   one .stickycta is two answers to "where am I". */
var SR_TOUR = (function () {
  function get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  function del(k) { try { sessionStorage.removeItem(k); } catch (e) {} }

  var q = {};
  location.search.replace(/^\?/, '').split('&').forEach(function (kv) {
    if (!kv) return;
    var i = kv.indexOf('='); if (i < 0) return;
    q[decodeURIComponent(kv.slice(0, i))] = decodeURIComponent(kv.slice(i + 1));
  });

  var id = q.tour;
  if (id === 'off') { del('sr.tour'); del('sr.t'); del('sr.seen'); return null; }
  if (id && SR_TOURS[id]) { set('sr.tour', id); if (q.t) set('sr.t', q.t); }
  else id = get('sr.tour');
  if (!id || !SR_TOURS[id]) return null;

  var t = q.t || get('sr.t') || null;
  /* landing on a trade page mid-tour without having named a trade: the page
     IS the answer, so take it rather than sending the reader to pick again */
  if (!t) {
    var m = location.pathname.match(/\/industries\/([a-z0-9-]+)\.html/i);
    if (m) { t = m[1]; set('sr.t', t); }
  }
  return { id: id, t: t, get: get, set: set, del: del };
}());
window.__SR_TOUR = SR_TOUR;

/* ═══════════════════════════════════════════════════════════════════════════
   guide.js — where the visitor is, and what to press next

   Measured problem: index.html offers 96 distinct labels across 35 destinations
   and 20 sections, and the first thing a reader can touch sits five screens
   down. Nothing told them where to begin, and nothing pointed at the control.

   Three things, and nothing else:
     1. .startpath   — marks which step the reader is in.
     2. .guiderail   — a fixed rail of the same steps, always reachable, showing
                       done / here / ahead. Desktop only; the sticky bar already
                       does this job on narrow screens.
     3. focus ring   — on arriving at a step, the ACTUAL control gets a ring and
                       a short label ("Pick a trade", "Paste here", "Drag me").
                       Pointing at the section is not enough; the reader has to
                       know which thing responds.

   DEV_SPEC 5.4 forbids window scroll listeners outright, so every state change
   comes from an IntersectionObserver. Nothing here reads layout on scroll.
   ═══════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* a subject tour owns the bar while it runs — see PART 2 */
  if (window.__SR_TOUR) return;

  var path = document.querySelector('[data-startpath]');
  if (!path || !('IntersectionObserver' in window)) return;

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Steps are declared in the markup so the copy stays with the copy.
     data-focus  — the control the reader is meant to press
     data-cue    — what to call it */
  var steps = [].slice.call(path.querySelectorAll('[data-step]')).map(function (el) {
    return {
      el: el,
      id: el.getAttribute('data-step'),
      next: el.getAttribute('data-next') || (el.querySelector('b') || {textContent:''}).textContent.trim(),
      short: el.getAttribute('data-short') || (el.querySelector('b') || {textContent:''}).textContent.trim(),
      focusSel: el.getAttribute('data-focus') || null,
      cue: el.getAttribute('data-cue') || 'Start here',
      sub: el.getAttribute('data-sub') || '',
      target: document.querySelector(el.getAttribute('data-step')),
      seen: false
    };
  }).filter(function (s) { return s.target; });

  if (!steps.length) return;

  /* ── 1 · the rail ─────────────────────────────────────────────────────── */
  var rail = document.createElement('nav');
  rail.className = 'guiderail';
  rail.setAttribute('aria-label', 'Tour progress');
  var railHead = document.createElement('p');
  railHead.className = 'gr-head';
  railHead.textContent = path.getAttribute('data-title') || 'Your 2-minute tour';
  rail.appendChild(railHead);
  var railList = document.createElement('ol');

  steps.forEach(function (s, i) {
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.href = s.id;
    a.setAttribute('data-rail', String(i));
    var dot = document.createElement('span');
    dot.className = 'gr-dot';
    dot.textContent = String(i + 1);
    var lab = document.createElement('span');
    lab.className = 'gr-lab';
    lab.textContent = s.short;
    a.appendChild(dot);
    a.appendChild(lab);
    li.appendChild(a);
    railList.appendChild(li);
    s.railItem = li;
  });

  /* the tour ends at the form, so the rail shows it as the last stop */
  var endTarget = document.querySelector(path.getAttribute('data-end') || '#early-access');
  var endItem = null;
  if (endTarget) {
    endItem = document.createElement('li');
    endItem.className = 'gr-end';
    var ea = document.createElement('a');
    ea.href = path.getAttribute('data-end') || '#early-access';
    var ed = document.createElement('span');
    ed.className = 'gr-dot';
    ed.textContent = '✓';
    var el2 = document.createElement('span');
    el2.className = 'gr-lab';
    el2.textContent = path.getAttribute('data-end-label') || 'Get my plan';
    ea.appendChild(ed);
    ea.appendChild(el2);
    endItem.appendChild(ea);
    railList.appendChild(endItem);
  }
  rail.appendChild(railList);

  /* ── 2 · the focus ring ───────────────────────────────────────────────── */
  var ring = document.createElement('div');
  ring.className = 'focusring';
  ring.setAttribute('aria-hidden', 'true');
  var cueEl = document.createElement('span');
  cueEl.className = 'fr-cue';
  ring.appendChild(cueEl);
  var subEl = document.createElement('span');
  subEl.className = 'fr-sub';
  ring.appendChild(subEl);
  var closeEl = document.createElement('button');
  closeEl.className = 'fr-x';
  closeEl.type = 'button';
  closeEl.setAttribute('aria-label', 'Dismiss this hint');
  closeEl.textContent = '\u00d7';
  ring.appendChild(closeEl);
  document.body.appendChild(ring);

  var ringTimer = null, ringTarget = null, ringRaf = null, ringWatch = null;
  closeEl.addEventListener('click', function (ev) {
    ev.preventDefault(); ev.stopPropagation(); clearRing();
  });

  /* Does this floating caption sit on top of anything a reader needs?
     Point-sampling missed it: the caption is 420x64 and the hero price is a
     16px-tall strip, so five sample points can straddle it and report clear.
     Rectangle intersection against real text elements is deterministic. */
  function overlapsText(el) { return overlapArea(el) > 0; }

  /* How much of a reader's text this floater covers, in square pixels. A
     boolean was enough while there were two placements to choose between; with
     three, "which is least bad" needs a number. */
  function overlapArea(el) {
    var b = el.getBoundingClientRect();
    if (!b.width || !b.height) return 0;
    var area = 0;
    var nodes = document.querySelectorAll('h1,h2,h3,h4,p,li,span,b,a,button,label');
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      if (ring.contains(n)) continue;
      /* The target's own label counts. It used to be skipped on the reasoning
         that the target is the point — but a hint laid across the words on the
         button it is pointing at hides the one thing the reader needs to read.
         Only the target's ancestors are skipped, since a hint inside a section
         necessarily sits within that section's box. */
      if (ringTarget && n.contains(ringTarget) && n !== ringTarget) continue;
      if (n.closest('.guiderail, .stickycta, .navwrap')) continue;
      var own = '';
      for (var k = 0; k < n.childNodes.length; k++) {
        if (n.childNodes[k].nodeType === 3) own += n.childNodes[k].nodeValue;
      }
      if (own.trim().length < 3) continue;
      var r = n.getBoundingClientRect();
      if (!r.width || !r.height) continue;
      if (r.bottom < 0 || r.top > window.innerHeight) continue;
      var ox = Math.min(r.right, b.right) - Math.max(r.left, b.left);
      var oy = Math.min(r.bottom, b.bottom) - Math.max(r.top, b.top);
      if (ox > 0 && oy > 0) area += ox * oy;
    }
    return area;
  }

  function placeRing() {
    if (!ringTarget) return;
    var r = ringTarget.getBoundingClientRect();
    ring.style.transform = 'translate(' + Math.round(r.left + window.scrollX - 8) + 'px,' +
                           Math.round(r.top + window.scrollY - 8) + 'px)';
    ring.style.width = Math.round(r.width + 16) + 'px';
    ring.style.height = Math.round(r.height + 16) + 'px';

    /* Put the hint where it does not land on anything. Both floaters count:
       the cue is the one that was covering the hero's sub-headline, and only
       the caption was ever being tested. Three placements are tried in order
       of preference and the first clear one wins; if none is clear, the one
       that covers the least text does. */
    var sideLeft = (r.left + r.width / 2) > window.innerWidth / 2;

    /* "Beside the control" has to mean beside the control CLUSTER. The hero's
       two buttons sit on one row, so anchoring to the target's own edge put the
       cue straight on top of the button next to it and the side placement lost
       to one that covered the price line instead. Clear the whole row. */
    var side = 0, row = ringTarget.parentElement;
    if (row) Array.prototype.forEach.call(row.children, function (c) {
      var cr = c.getBoundingClientRect();
      if (!cr.width || cr.top >= r.bottom || cr.bottom <= r.top) return;
      side = Math.max(side, sideLeft ? (r.left - cr.left) : (cr.right - r.right));
    });
    ring.style.setProperty('--fr-side', Math.round(Math.max(0, side)) + 'px');

    var best = null, bestCost = Infinity;
    ring.classList.remove('cue-hide');
    for (var pi = 0; pi < 3; pi++) {
      ring.classList.toggle('cue-above', pi === 1);
      ring.classList.toggle('cue-side',  pi === 2);
      ring.classList.toggle('side-left', pi === 2 && sideLeft);
      nudge();
      var cost = overlapArea(cueEl) + overlapArea(subEl) + offscreen(cueEl) + offscreen(subEl);
      if (cost === 0) { best = pi; bestCost = 0; break; }
      if (best === null || cost < bestCost) { best = pi; bestCost = cost; }
    }
    ring.classList.toggle('cue-above', best === 1);
    ring.classList.toggle('cue-side',  best === 2);
    ring.classList.toggle('side-left', best === 2 && sideLeft);
    nudge();
    /* A 20x20 nick on a descender is not worth suppressing a hint over; a
       placement that lies across a sentence is. */
    ring.classList.toggle('cue-hide', bestCost > 400);
  }

  /* Anything pushed past the edge is as unreadable as anything covered, so it
     is priced the same way and competes in the same comparison. */
  function offscreen(el) {
    var r = el.getBoundingClientRect();
    if (!r.width || !r.height) return 0;
    var dx = Math.max(0, 12 - r.left) + Math.max(0, r.right - (window.innerWidth - 12));
    return dx * Math.max(1, r.height);
  }

  /* Keep both floaters inside the viewport. This writes a custom property that
     the stylesheet folds into its own transform, so it no longer overrides the
     placement class it is supposed to cooperate with. */
  function nudge() {
    [cueEl, subEl].forEach(function (el) {
      if (!el) return;
      el.style.setProperty('--fr-dx', '0px');
      var r = el.getBoundingClientRect();
      if (!r.width) return;
      var d = 0;
      if (r.left < 12) d = 12 - r.left;
      else if (r.right > window.innerWidth - 12) d = (window.innerWidth - 12) - r.right;
      if (d) el.style.setProperty('--fr-dx', Math.round(d) + 'px');
    });
  }

  function clearRing() {
    ring.classList.remove('on');
    ringTarget = null;
    if (ringTimer) { clearTimeout(ringTimer); ringTimer = null; }
    if (ringRaf) { cancelAnimationFrame(ringRaf); ringRaf = null; }
    if (ringWatch) { ringWatch.disconnect(); ringWatch = null; }
  }

  /* Point at one control. Takes the element directly so the landing pointer and
     the per-step pointer go through exactly the same path — the earlier version
     called this and then reassigned ringTarget from outside, which raced with
     its own clearRing(). */
  function pointAt(t, cue, sub) {
    clearRing();
    if (!t || !t.getBoundingClientRect().width) return;
    ringTarget = t;
    cueEl.textContent = cue;
    subEl.textContent = sub || '';
    subEl.style.display = sub ? '' : 'none';
    placeRing();
    ring.classList.add('on');

    /* the target can move while the smooth scroll is still running, so follow
       it for a moment rather than pinning it once */
    var until = Date.now() + 1600;
    (function follow() {
      placeRing();
      if (Date.now() < until) ringRaf = requestAnimationFrame(follow);
    }());

    /* It has done its job the moment the reader touches the thing — or anything
       else in the same section. Listening only on the ringed control meant that
       clicking a demo question left the page dimmed while the answer played. */
    var scope = t.closest('section') || t;
    ['pointerdown', 'keydown', 'input'].forEach(function (ev) {
      scope.addEventListener(ev, clearRing, { once: true });
    });

    /* A pointer that times out is a hint you can miss, which is what happened:
       it "blinked and vanished" and the reader was no better off. It now stays
       until the reader either uses the control or scrolls it out of view. */
    if (ringWatch) { ringWatch.disconnect(); ringWatch = null; }
    var wasSeen = false;
    ringWatch = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { wasSeen = true; return; }
        /* only dismiss something the reader actually had on screen — the first
           callback can report "not intersecting" before anything has scrolled */
        if (wasSeen && ringTarget === t) clearRing();
      });
    }, { threshold: 0 });
    ringWatch.observe(t);
  }

  /* ── 3 · state ────────────────────────────────────────────────────────── */
  var bar = document.querySelector('.stickycta');
  /* Dock the rail inside the bar rather than floating it over the page. Three
     pages ship no .stickycta at all, and the old fallback dropped the rail on
     top of the content — the exact failure this docking was meant to end. If
     there is no bar, build one. */
  if (!bar) {
    bar = document.createElement('div');
    bar.className = 'stickycta';
    var w = document.createElement('div');
    w.className = 'wrap';
    var m = document.createElement('span');
    m.className = 'msg';
    var b = document.createElement('a');
    b.className = 'btn btn-teal';
    b.setAttribute('href', path.getAttribute('data-end') || '#early-access');
    b.textContent = path.getAttribute('data-end-label') || 'Get my plan';
    w.appendChild(m);
    w.appendChild(b);
    bar.appendChild(w);
    document.body.appendChild(bar);
  }
  bar.querySelector('.wrap').insertBefore(rail, bar.querySelector('.wrap').firstChild);
  bar.classList.add('hasguide');
  var barMsg = bar && bar.querySelector('.msg');
  var barBtn = bar && bar.querySelector('a.btn');
  var barHomeHref = barBtn ? barBtn.getAttribute('href') : '';
  var barHomeLabel = barBtn ? barBtn.cloneNode(true).childNodes : null;
  var current = -1, atEnd = false;

  function setBtn(label, href) {
    barBtn.setAttribute('href', href);
    barBtn.textContent = label;
    var cir = document.createElement('span');
    cir.className = 'cir';
    cir.textContent = '↗';
    barBtn.appendChild(cir);
  }

  function setMsg(parts) {
    barMsg.textContent = '';
    parts.forEach(function (p) {
      var n = p.tag ? document.createElement(p.tag) : document.createTextNode(p.text);
      if (p.tag) { n.textContent = p.text; if (p.cls) n.className = p.cls; }
      barMsg.appendChild(n);
    });
  }

  function render() {
    steps.forEach(function (s, i) {
      s.el.classList.toggle('is-now', i === current);
      s.el.classList.toggle('is-done', s.seen && i !== current);
      if (s.railItem) {
        s.railItem.classList.toggle('is-now', i === current);
        s.railItem.classList.toggle('is-done', s.seen && i !== current);
      }
    });

    var nextIdx = -1;
    for (var i = 0; i < steps.length; i++) {
      if (!steps[i].seen) { nextIdx = i; break; }
    }
    /* the last stop lights up when the reader is actually AT the form, not the
       moment the third step has been seen — otherwise two dots read as "now" */
    if (endItem) endItem.classList.toggle('is-now', atEnd);
    /* The rail is the answer to "where do I click", so it cannot wait until the
       reader has already found a step. It is visible from the moment the page
       loads; before any step is reached it simply shows the first one as next. */
    rail.classList.add('show');
    if (current < 0 && !steps.some(function (s) { return s.seen; })) {
      steps[0].railItem.classList.add('is-next');
    } else {
      steps.forEach(function (s) { s.railItem.classList.remove('is-next'); });
    }

    if (!bar || !barMsg || !barBtn) return;

    if (nextIdx === -1) {
      setMsg([
        { tag: 'b', text: 'That is the whole product.' },
        { text: ' You have tried it, priced it, and seen what it refuses to do.' }
      ]);
      barBtn.setAttribute('href', barHomeHref || '#early-access');
      barBtn.textContent = '';
      if (barHomeLabel) {
        [].slice.call(barHomeLabel).forEach(function (n) { barBtn.appendChild(n.cloneNode(true)); });
      }
      bar.setAttribute('data-guide', 'done');
      return;
    }

    var s = steps[nextIdx];
    setMsg([
      { tag: 'span', cls: 'stepnum', text: (nextIdx + 1) + ' of ' + steps.length },
      { text: ' Next: ' },
      { tag: 'b', text: s.next }
    ]);
    setBtn('Take me there', s.id);
    bar.setAttribute('data-guide', 'step');
  }

  /* A step is "current" while any part of it sits in the middle band of the
     viewport. The band is generous on the top edge so that a scrollIntoView
     landing — which puts the section top at y=0 — registers immediately;
     the earlier -20% top margin made that landing fall outside the root. */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var i = -1;
      steps.forEach(function (s, k) { if (s.target === e.target) i = k; });
      if (i < 0) return;
      if (e.isIntersecting) {
        steps[i].seen = true;
        current = i;
      } else if (current === i) {
        current = -1;
      }
    });
    render();
  }, { threshold: 0, rootMargin: '0px 0px -55% 0px' });

  steps.forEach(function (s) { io.observe(s.target); });

  /* the form is its own stop, so the rail's last dot tracks it directly */
  if (endTarget) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { atEnd = e.isIntersecting; });
      render();
    }, { threshold: 0, rootMargin: '0px 0px -40% 0px' }).observe(endTarget);
  }

  /* ── 4 · jumping ──────────────────────────────────────────────────────── */
  function jump(href) {
    var t = document.querySelector(href);
    if (!t) return false;
    /* A smooth scroll across thirteen screens is a long ride that tells the
       reader nothing on the way. Animate short hops, cut straight for long ones. */
    var far = Math.abs(t.getBoundingClientRect().top) > window.innerHeight * 2.5;
    t.scrollIntoView({ behavior: (reduce || far) ? 'auto' : 'smooth', block: 'start' });
    t.setAttribute('tabindex', '-1');
    t.focus({ preventScroll: true });
    var step = null;
    steps.forEach(function (s) { if (s.id === href) step = s; });
    /* jumping anywhere that is not a step means the previous pointer is stale */
    if (!step) clearRing();
    else setTimeout(function () {
      pointAt(document.querySelector(step.focusSel), step.cue, step.sub);
    }, (reduce || far) ? 80 : 480);
    return true;
  }

  function wire(root) {
    root.addEventListener('click', function (ev) {
      var a = ev.target.closest && ev.target.closest('a[href^="#"]');
      if (!a || !root.contains(a)) return;
      if (jump(a.getAttribute('href'))) ev.preventDefault();
    });
  }
  wire(path);
  /* the rail now lives inside the bar, so wiring both would run jump() twice on
     a single click — two scrollIntoView calls in one tick, and the state read
     afterwards was whatever the second one left behind */
  if (bar && bar.contains(rail)) wire(bar);
  else { wire(rail); if (bar) wire(bar); }

  /* the hero button and any other in-page link to a step gets the same
     treatment, so the pointer appears however the reader arrived */
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href^="#"]');
    if (!a || path.contains(a) || rail.contains(a) || (bar && bar.contains(a))) return;
    var href = a.getAttribute('href');
    var isStep = false;
    steps.forEach(function (s) { if (s.id === href) isStep = true; });
    if (!isStep) return;
    if (jump(href)) ev.preventDefault();
  });

  /* arriving with a hash from another page should point too */
  if (location.hash) {
    var h = location.hash;
    steps.forEach(function (s) {
      if (s.id === h) setTimeout(function () {
        pointAt(document.querySelector(s.focusSel), s.cue, s.sub);
      }, 700);
    });
  } else {
    /* Landing cold, the first question is "where do I click?" — so the pointer
       answers it before the reader has done anything, on the hero's own tour
       button. It clears the moment they press it, or after a few seconds. */
    var heroBtn = document.querySelector('.hero .ctas a.btn[href="#start-here"], header .ctas a.btn[href="#start-here"]');
    if (heroBtn) {
      setTimeout(function () {
        if (window.scrollY > 40) return;      /* they already started reading */
        /* cue only — a caption here would land on the price line or the
           sub-headline whichever way it flips, and the tour band repeats
           the same sentence one screen down */
        pointAt(heroBtn, 'Start here — 2 min');
      }, 1400);
    }
  }

  window.addEventListener('resize', function () { if (ringTarget) placeRing(); });
  render();
}());

/* ═══════════════════════════════════════════════════════════════════════════
   PART 2b — the subject tour runtime
   ───────────────────────────────────────────────────────────────────────────
   Reuses everything the in-page tour already established: the .guiderail
   markup, the done / here / ahead classes, and the dock inside .stickycta. It
   does not build a second, competing widget — it builds the SAME widget over a
   cross-page step list instead of a within-page one.

   DEV_SPEC 5.4: no window scroll listener. Progress on the current page is
   read by an IntersectionObserver, exactly as the in-page tour reads it.
   ═══════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var T = window.__SR_TOUR;
  if (!T) return;
  var def = SR_TOURS[T.id];
  if (!def) return;

  var steps = def.build ? def.build(T.t) : def.steps;
  if (!steps || !steps.length) return;

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── where am I ─────────────────────────────────────────────────────────
     Pages live at /en/x.html and /en/industries/x.html, so a step's page is
     stored relative to /en/ and resolved against the current depth. */
  var here = location.pathname.replace(/^.*\/en\//, '');
  if (!here || /\/$/.test(here)) here = 'index.html';
  var deep = here.indexOf('/') > -1;
  var base = deep ? '../' : './';

  function hrefOf(s) {
    return base + s.u + '?tour=' + T.id + (T.t ? '&t=' + T.t : '') + (s.h || '');
  }
  function targetOf(s) {
    if (s.h) return document.querySelector(s.h);
    if (s.sel) return document.querySelector(s.sel);
    return null;
  }
  function onThisPage(s) { return s.u === here; }

  /* ── what have I already seen ───────────────────────────────────────────
     Keyed by page+anchor so a reload does not un-tick a step. */
  function key(s, i) { return T.id + ':' + i; }
  var seen = {};
  try { seen = JSON.parse(T.get('sr.seen') || '{}') || {}; } catch (e) { seen = {}; }
  function markSeen(i) {
    if (seen[key(steps[i], i)]) return;
    seen[key(steps[i], i)] = 1;
    T.set('sr.seen', JSON.stringify(seen));
  }
  function isSeen(i) { return !!seen[key(steps[i], i)]; }

  /* ── the rail ───────────────────────────────────────────────────────────
     Same element, same classes, same CSS as the in-page rail. */
  var rail = document.createElement('nav');
  rail.className = 'guiderail tourrail';
  rail.setAttribute('aria-label', 'Site tour: ' + def.title);

  var head = document.createElement('p');
  head.className = 'gr-head';
  head.textContent = def.title;
  rail.appendChild(head);

  var list = document.createElement('ol');
  var railItems = [];
  steps.forEach(function (s, i) {
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.href = hrefOf(s);
    var dot = document.createElement('span');
    dot.className = 'gr-dot';
    dot.textContent = String(i + 1);
    var lab = document.createElement('span');
    lab.className = 'gr-lab';
    lab.textContent = s.lab;
    a.appendChild(dot); a.appendChild(lab);
    /* the rail is the only place the full sentence exists on a phone, where
       .gr-lab is hidden and the dot is all that is left */
    a.setAttribute('aria-label', 'Step ' + (i + 1) + ' of ' + steps.length + ': ' + s.lab);
    li.appendChild(a);
    list.appendChild(li);
    railItems.push(li);
  });
  rail.appendChild(list);

  /* ending the tour has to be one press away, and has to be a real control */
  var stop = document.createElement('a');
  stop.className = 'gr-stop';
  stop.href = base + here + '?tour=off';
  stop.textContent = 'End tour';
  rail.appendChild(stop);

  /* ── dock it, exactly where the in-page rail docks ──────────────────────
     Three pages ship no .stickycta, so one is built, same as the in-page
     tour does — otherwise the rail would float over the content. */
  var bar = document.querySelector('.stickycta');
  if (!bar) {
    bar = document.createElement('div');
    bar.className = 'stickycta';
    var w = document.createElement('div');
    w.className = 'wrap';
    var m = document.createElement('span');
    m.className = 'msg';
    w.appendChild(m);
    var b = document.createElement('a');
    b.className = 'btn btn-teal';
    b.href = base + 'get-started.html';
    b.textContent = 'Get my plan';
    w.appendChild(b);
    bar.appendChild(w);
    document.body.appendChild(bar);
  }
  var wrap = bar.querySelector('.wrap');
  wrap.insertBefore(rail, wrap.firstChild);
  bar.classList.add('hasguide', 'hastour');

  var barBtn = wrap.querySelector('a.btn');

  /* ── state ──────────────────────────────────────────────────────────────
     "Current" is the step whose section is in the middle band of the
     viewport — an IntersectionObserver, never a scroll listener. */
  var current = -1;

  function render() {
    steps.forEach(function (s, i) {
      railItems[i].classList.toggle('is-now', i === current);
      railItems[i].classList.toggle('is-done', isSeen(i) && i !== current);
    });
    var next = -1;
    for (var i = 0; i < steps.length; i++) if (!isSeen(i)) { next = i; break; }
    railItems.forEach(function (li) { li.classList.remove('is-next'); });
    if (next > -1 && next !== current) railItems[next].classList.add('is-next');

    if (!barBtn) return;
    if (next === -1) {
      barBtn.setAttribute('href', base + 'get-started.html');
      barBtn.textContent = 'That is the whole subject — get my plan';
      bar.setAttribute('data-tour', 'done');
    } else {
      barBtn.setAttribute('href', hrefOf(steps[next]));
      barBtn.textContent = (next + 1) + ' of ' + steps.length + ' · ' + steps[next].lab;
      bar.setAttribute('data-tour', 'step');
    }
    var cir = document.createElement('span');
    cir.className = 'cir';
    cir.textContent = '→';
    barBtn.appendChild(cir);
  }

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var i = Number(e.target.getAttribute('data-tourstep'));
        if (isNaN(i)) return;
        if (e.isIntersecting) { markSeen(i); current = i; }
        else if (current === i) { current = -1; }
      });
      render();
    }, { threshold: 0, rootMargin: '0px 0px -55% 0px' });

    steps.forEach(function (s, i) {
      if (!onThisPage(s)) return;
      var t = targetOf(s);
      if (!t) return;
      t.setAttribute('data-tourstep', String(i));
      io.observe(t);
    });
  } else {
    steps.forEach(function (s, i) { if (onThisPage(s) && targetOf(s)) markSeen(i); });
  }

  /* ── moving between stops on the same page ──────────────────────────────
     A same-page step is a scroll, not a page load; anything else is a normal
     link and the browser handles it. */
  function goto(i) {
    var s = steps[i];
    var t = targetOf(s);
    if (!t) return false;
    var far = Math.abs(t.getBoundingClientRect().top) > window.innerHeight * 2.5;
    t.scrollIntoView({ behavior: (reduce || far) ? 'auto' : 'smooth', block: 'start' });
    t.setAttribute('tabindex', '-1');
    t.focus({ preventScroll: true });
    markSeen(i);
    render();
    return true;
  }

  bar.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href]');
    if (!a || !bar.contains(a)) return;
    if (a === stop) return;                       /* let ?tour=off navigate */
    for (var i = 0; i < steps.length; i++) {
      if (a.getAttribute('href') !== hrefOf(steps[i])) continue;
      if (!onThisPage(steps[i])) return;          /* real navigation */
      if (goto(i)) ev.preventDefault();
      return;
    }
  });

  /* ── arriving ───────────────────────────────────────────────────────────
     A step written as a selector rather than an anchor has no hash for the
     browser to act on, so the landing is done here. A step that DOES have a
     hash the browser already handled; it only needs ticking off. */
  var landed = -1;
  for (var i = 0; i < steps.length; i++) {
    if (!onThisPage(steps[i])) continue;
    if (steps[i].h && location.hash === steps[i].h) { landed = i; break; }
    if (steps[i].sel && !location.hash) { landed = i; break; }
  }
  if (landed > -1) {
    var st = steps[landed];
    if (st.sel && !location.hash) setTimeout(function () { goto(landed); }, reduce ? 0 : 220);
    else { markSeen(landed); current = landed; }
  }

  render();
}());
