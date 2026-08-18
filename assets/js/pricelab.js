/* ═══════════════════════════════════════════════════════════════════
   PRICE LAB — the one demo on this site that is not a script.

   Every other demo on this site replays a conversation we wrote. This
   one reads a price list the visitor pastes in, parses it in their own
   browser, and answers questions against *their* numbers. There is no
   network call in this file, by design: an owner who watches their own
   prices come back inside a finished quote stops wondering whether the
   demo was rigged, and that is the whole persuasion argument.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var root = document.querySelector('[data-lab]');
  if (!root) return;

  var ta      = root.querySelector('[data-lab-input]');
  var askIn   = root.querySelector('[data-lab-ask]');
  var goBtn   = root.querySelector('[data-lab-go]');
  var outEl   = root.querySelector('[data-lab-out]');
  var listEl  = root.querySelector('[data-lab-list]');
  var srEl    = root.querySelector('[data-lab-sr]');
  var samples = root.querySelectorAll('[data-lab-sample]');
  var items   = [];

  var SAMPLES = {
    dental: 'Consultation  45\n' +
            'Scale and polish  120\n' +
            'Composite filling  180\n' +
            'Porcelain crown  1100\n' +
            'Root canal, molar  950\n' +
            'Emergency after-hours visit  240',
    home:   'Diagnostic call-out  95\n' +
            'After-hours call-out  180\n' +
            'Furnace repair, per hour  140\n' +
            'AC service  220\n' +
            'Full system install  4800\n' +
            'Annual maintenance plan  320',
    venues: 'Saturday reception, up to 150 guests  9800\n' +
            'Friday reception  7400\n' +
            'Ceremony only  2200\n' +
            'Extra guest, per head  62\n' +
            'Bar package, per head  48\n' +
            'Cleanup and teardown  480',
    stays:  'Double room, weeknight  180\n' +
            'Double room, weekend  240\n' +
            'Garden cottage  320\n' +
            'Extra adult  45\n' +
            'Pet fee, per night  25\n' +
            'Airport transfer  60'
  };

  var STARTERS = {
    dental: 'How much is a crown?',
    home:   'What does an after-hours call-out cost?',
    venues: 'Saturday for 150 guests?',
    stays:  'How much is the garden cottage?'
  };

  function esc(t) {
    return String(t).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function money(n) {
    return '$' + n.toLocaleString('en-US', { maximumFractionDigits: n % 1 ? 2 : 0 });
  }

  /* ── parsing ──
     Owners paste whatever their price list already looks like: tab-separated
     columns out of a spreadsheet, "Item — $120", "Item: 120 USD", two ragged
     columns lifted out of a PDF. So take the LAST number on the line as the
     price and everything before it as the label — that one rule survives all
     of those shapes without asking the owner to reformat anything. */
  function parse(text) {
    var out = [];
    String(text).split(/\r?\n/).forEach(function (raw) {
      var line = raw.trim();
      if (!line) return;
      var m = line.match(/^(.*?)[\s:\u2014\u2013|\t-]*([$\u20ac\u00a3\u00a5\u20a9]?\s*\d[\d,.]*)\s*(?:USD|EUR|GBP|KRW|JPY)?$/i);
      if (!m) return;
      var label = m[1].replace(/[\s:\u2014\u2013|-]+$/, '').trim();
      var price = parseFloat(m[2].replace(/[^\d.]/g, ''));
      if (!label || !isFinite(price)) return;
      out.push({ label: label, price: price, key: label.toLowerCase() });
    });
    return out;
  }

  /* ── matching ──
     Score each line against the words in the question, weighting longer words
     so "crown" outranks an incidental "the". Deliberately not a fuzzy library
     and not a model: an owner can read this rule in one sentence and predict
     what it will do, which is the point of showing it at all. */
  function score(item, words) {
    var hay = item.key, s = 0;
    words.forEach(function (w) {
      if (w.length < 3) return;
      if (hay.indexOf(w) >= 0) s += w.length;
      else if (w.length > 4 && hay.indexOf(w.slice(0, w.length - 1)) >= 0) s += w.length - 2;
    });
    return s;
  }

  function renderList() {
    if (!items.length) {
      listEl.innerHTML = '<span class="labnone">No priced lines yet &mdash; one item and one number per line.</span>';
      return;
    }
    listEl.innerHTML =
      '<span class="lablbl">' + items.length + ' price' + (items.length === 1 ? '' : 's') +
      ' read from your list</span>' +
      items.map(function (i) {
        return '<span class="labpill">' + esc(i.label) + ' <b>' + money(i.price) + '</b></span>';
      }).join('');
  }

  function say(t) { if (srEl) srEl.textContent = t; }

  function answer() {
    items = parse(ta.value);
    renderList();
    var q = (askIn.value || '').trim();

    if (!items.length) {
      outEl.innerHTML = '<div class="labmsg">Paste a price list first, or load one of the samples above.</div>';
      say('No prices read yet.');
      return;
    }
    if (!q) {
      outEl.innerHTML = '<div class="labmsg">Now ask it what a customer would ask.</div>';
      return;
    }

    var words  = q.toLowerCase().replace(/[^a-z0-9\s]/g, ' ').split(/\s+/);
    var ranked = items
      .map(function (i) { return { i: i, s: score(i, words) }; })
      .filter(function (r) { return r.s > 0; })
      .sort(function (a, b) { return b.s - a.s; });

    /* Nothing in the list covers the question. This branch has to stay: an
       owner who never sees it decline will not believe the rest of it. */
    if (!ranked.length) {
      outEl.innerHTML =
        '<div class="labcard nomatch">' +
          '<div class="labh"><b>Not in your list</b>' +
            '<span class="labtag">Handed to a person</span></div>' +
          '<div class="labsay"><span class="labwho">It says</span>' +
            '&ldquo;I don&rsquo;t have a price for that in front of me. I&rsquo;ve passed it to the ' +
            'team &mdash; they&rsquo;ll come back to you with the exact figure.&rdquo;</div>' +
          '<p class="labwhy">Nothing you pasted covers &ldquo;' + esc(q) + '&rdquo;, so it will not ' +
            'estimate, round up, or borrow a number off a neighbouring line. It files the question ' +
            'instead &mdash; you answer it once, and it is on the list from then on.</p>' +
        '</div>';
      say('No matching price. Handed to a person.');
      return;
    }

    /* "4 nights", "3 hours", "150 guests" — a quantity in the question may
       multiply the best-matching line. It may NOT multiply a flat package:
       "Saturday reception, up to 150 guests  9800" × 150 quotes $1.47m, which
       is the single fastest way to lose a room. So only lines that price a
       unit get multiplied, and a line that already names the same number is
       treated as the package it is. */
    var qty = 1, sawQty = 0;
    var qm  = q.match(/\b(\d{1,3})\b/);
    if (qm && +qm[1] > 1 && +qm[1] < 1000) {
      var perUnit = /\bper\b|\beach\b|\/\s*(?:night|head|person|hour|guest|adult|day|room)\b/i;
      var namesIt = ranked[0].i.key.indexOf(qm[1]) >= 0;
      if (perUnit.test(ranked[0].i.key) && !namesIt) qty = +qm[1];
      else if (!namesIt) sawQty = +qm[1];   /* heard it, deliberately did not apply it */
    }

    /* Only carry a second or third line if it matched nearly as strongly as
       the first. Without this, "deep clean" quietly picks up "gutter
       clearing" — a quote with a line the customer never asked for is worse
       than no quote at all. */
    var cut = ranked[0].s * 0.7;
    var top = ranked.filter(function (r) { return r.s >= cut; }).slice(0, 3);
    var lines = top.map(function (r, n) {
      var k = n === 0 ? qty : 1;
      return '<div class="qline">' +
               '<span class="d">' + esc(r.i.label) + '</span>' +
               '<span class="s">' + (k > 1 ? k + ' \u00d7 ' + money(r.i.price) : 'from your list') + '</span>' +
               '<span class="v">' + money(r.i.price * k) + '</span>' +
             '</div>';
    }).join('');
    var total = top.reduce(function (a, r, n) { return a + r.i.price * (n === 0 ? qty : 1); }, 0);

    outEl.innerHTML =
      '<div class="labcard">' +
        '<div class="labh"><b>Quote &mdash; built from your list</b>' +
          '<span class="labtag ok">Ready to send</span></div>' +
        '<div class="quotedoc bare">' + lines +
          '<div class="qline tot"><span class="d">Total</span>' +
          '<span class="v">' + money(total) + '</span></div>' +
        '</div>' +
        '<div class="labsay"><span class="labwho">It says</span>&ldquo;' +
          esc(top[0].i.label) + ' is ' + money(top[0].i.price * qty) +
          (qty > 1 ? ' for ' + qty : '') + '. I can hold a slot for you now &mdash; would a morning ' +
          'or an afternoon suit you better?&rdquo;</div>' +
        (sawQty
          ? '<p class="labwhy warn">It heard &ldquo;' + sawQty + '&rdquo; but did not multiply by it: ' +
            'your list does not say whether <b>' + esc(top[0].i.label) + '</b> is priced per unit. ' +
            'Guessing either way is how a quote goes out wrong, so it quotes the line as written and ' +
            'flags the quantity for a person to confirm.</p>'
          : '') +
        '<p class="labwhy">Every figure above came out of the box you filled in. Nothing was ' +
          'estimated, and nothing left your browser.</p>' +
      '</div>';
    say('Quote built. Total ' + money(total) + '.');
  }

  goBtn.addEventListener('click', answer);
  askIn.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') { e.preventDefault(); answer(); }
  });
  ta.addEventListener('input', function () { items = parse(ta.value); renderList(); });

  Array.prototype.forEach.call(samples, function (b) {
    b.addEventListener('click', function () {
      var k = b.getAttribute('data-lab-sample');
      ta.value    = SAMPLES[k]  || '';
      askIn.value = STARTERS[k] || '';
      Array.prototype.forEach.call(samples, function (o) {
        o.classList.toggle('on', o === b);
        o.setAttribute('aria-pressed', o === b ? 'true' : 'false');
      });
      answer();
    });
  });

  items = parse(ta.value);
  renderList();
})();
