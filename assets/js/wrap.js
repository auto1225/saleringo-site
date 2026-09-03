/* ── lines that end where a thought ends ───────────────────────────────────
   A paragraph capped at a reading measure wraps wherever the last word
   happens to fall. The result is what the review kept pointing at:

       Every scenario below is a worked illustration of how the product behaves,
       built from the rate card and safety script a shop would load. They are not
       customer stories, and no shop named or implied here is a Saleringo
       customer. Every figure shown is one already published on this page,
       on the pricing page, or in the home-services worked examples — nothing
       here is invented, and your own rate card sets your numbers.

   "They are not" ends a line. "a Saleringo" ends a line. The eye has to carry
   half a clause down to the next line and reassemble it, six times a
   paragraph. Narrowing the column does not fix that; it causes it.

   So the column is widened to the page and the breaks are put where the
   sentence already breaks: after a comma, a dash, a semicolon, a full stop,
   or before the conjunction that starts the next clause. Each line is filled
   as far as it can go and then ended at the last sense boundary that still
   fits, which is how a subtitle is timed and how poetry is set.

       Every scenario below is a worked illustration of how the product behaves,
       built from the rate card and safety script a shop would load.
       They are not customer stories, and no shop named or implied here is a Saleringo customer.
       Every figure shown is one already published on this page, on the pricing page, or in the home-services worked examples
       — nothing here is invented, and your own rate card sets your numbers.

   Rules it holds to:

     · A clause longer than the line wraps normally. Never overflow to obey a
       break, and never break a clause in the middle to make one fit.
     · Below 560px there is not enough width for a clause to be a line, so the
       breaker stands down and the browser wraps as it always did.
     · Authored breaks are respected: text between two <br> is treated as its
       own run, because someone already decided where that line ends.
     · Everything is reversible. The original markup is kept, and a resize
       restores it before measuring again, so nothing accumulates.
     · Product mocks, chat bubbles and table cells are left alone. They are
       interface, not sentences.                                             */
(function () {
  'use strict';

  var PROSE = 'main p, main .lead, main .sub, main .secintro, main .standfirst, ' +
              'main figcaption, main blockquote, main .room-lead, main .room-d, ' +
              'main .sl-note, main .exlabel, main .seccap, main .note, main .fn, ' +
              'main h1, main h2, main .h2, main h3, main .sl-foot, main .secfoot';

  /* interface, not prose */
  var SKIP = '[data-qb], .qbcard, [aria-live], [data-commerce-verdict], [data-d60], .d60card, [data-status-live], .appwin, .bub, .exturn, .calmock, .pipeboard, .quotedoc, .custcard, ' +
             '.kpitiles, .repcard, .ledger, .transcript, .funnelrow, .browserframe, ' +
             '.msgthread, .callcard, .demo-body, .widget, .inboxmock, .queueboard, ' +
             '.colboard, .rampboard, td, th, .pstabs, .chiprow, .exfilter, .guiderail, ' +
             '.navpanel, .stickycta, .bigfooter';

  var MIN_WIDTH = 560;      /* below this a clause is wider than a line */
  /* Korean packs the same sentence into fewer 어절 than English does into
     words, so the floor that means "long enough to arrange" is lower. */
  var MIN_WORDS = document.documentElement.lang === 'ko' ? 9 : 14;

  /* after these, a line may end */
  var AFTER = /[,;:.!?—–·](["'”’)]*)$/;
  /* before these, a line may end */
  var BEFORE = /^(and|but|or|so|because|which|that|while|though|although|unless|rather|instead|before|after|until|since|whereas|yet|for)$/i;

  /* Korean marks its clause ends in the verb, not in punctuation. A sentence
     can run three clauses with one comma in it, so a breaker that only looks
     for punctuation finds nothing to work with and the paragraph wraps
     wherever the measure runs out - the exact fault this file exists to fix.
     These are the connective endings a Korean sentence actually turns on:
     -지만, -는데, -면서, -하고, -어서. A line ending on one of them ends
     where the thought does. */
  var AFTER_KO = /(지만|는데|면서|하고|하며|이며|어서|아서|이고|으며|므로|처럼|보다|까지|부터)$/;
  var BEFORE_KO = /^(그리고|하지만|그래서|그러나|그런데|즉|다만|또한|따라서|반면|한편|왜냐하면|예를)$/;

  function words(el) {
    return (el.textContent || '').trim().split(/\s+/).length;
  }

  /* the number of line boxes a range occupies */
  function lineCount(range) {
    var rects = range.getClientRects(), tops = [], i, r, mid, j, seen;
    for (i = 0; i < rects.length; i++) {
      r = rects[i];
      if (r.height < 4 || r.width < 0.5) continue;
      mid = r.top + r.height / 2;
      seen = false;
      for (j = 0; j < tops.length; j++) if (Math.abs(tops[j] - mid) < 6) { seen = true; break; }
      if (!seen) tops.push(mid);
    }
    return tops.length;
  }

  /* every text node under el that is not inside something we skip */
  function textNodes(el) {
    var out = [];
    var walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue || !n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        if (n.parentElement && n.parentElement.closest(SKIP)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var n;
    while ((n = walk.nextNode())) out.push(n);
    return out;
  }

  /* candidate break points, as [node, offset] pairs, in document order */
  function candidates(el) {
    var nodes = textNodes(el), out = [], i, t, m, k;
    for (i = 0; i < nodes.length; i++) {
      t = nodes[i].nodeValue;
      /* a break may go at a space; decide by what is on each side of it */
      var re = /\s+/g;
      while ((m = re.exec(t)) !== null) {
        var before = t.slice(0, m.index);
        var after = t.slice(m.index + m[0].length);
        if (!before || !after) continue;
        var lastWord = before.split(/\s+/).pop();
        var nextWord = after.split(/\s+/)[0].replace(/[^A-Za-z’'가-힣]/g, '');
        var ok = AFTER.test(lastWord) || BEFORE.test(nextWord) ||
                 AFTER_KO.test(lastWord.replace(/[^가-힣]/g, '')) ||
                 BEFORE_KO.test(nextWord);
        if (!ok) continue;
        out.push([nodes[i], m.index]);
      }
    }
    return out;
  }

  function apply(el) {
    var w = el.clientWidth;
    if (w < MIN_WIDTH) return;
    if (words(el) < MIN_WORDS) return;

    var cands = candidates(el);
    if (!cands.length) return;

    /* Greedy, and incremental: each break is inserted before the next
       measurement, so every measurement is of the layout as it will be. */
    var startNode = null, startOff = 0;
    var first = textNodes(el)[0];
    if (!first) return;
    startNode = first; startOff = 0;

    var lastFit = null;
    var i = 0;
    var guard = 0;

    while (i < cands.length && guard++ < 400) {
      var c = cands[i];
      var range = document.createRange();
      try {
        range.setStart(startNode, startOff);
        range.setEnd(c[0], c[1]);
      } catch (e) { i++; continue; }
      if (range.collapsed) { i++; continue; }

      if (lineCount(range) > 1) {
        if (lastFit) {
          /* end the line at the last boundary that still fitted */
          var node = lastFit[0], off = lastFit[1];
          var tail = node.splitText(off);
          /* the space that was there is now at the start of a line: drop it */
          tail.nodeValue = tail.nodeValue.replace(/^\s+/, '');
          var br = document.createElement('br');
          br.className = 'cw';
          tail.parentNode.insertBefore(br, tail);
          startNode = tail; startOff = 0;
          /* candidates after this point are still valid; the split kept them
             in nodes we did not touch, except the one we split */
          cands = candidates(el);
          i = 0;
          while (i < cands.length &&
                 (cands[i][0].compareDocumentPosition(startNode) & Node.DOCUMENT_POSITION_FOLLOWING ||
                  (cands[i][0] === startNode && cands[i][1] <= startOff))) i++;
          lastFit = null;
          continue;
        }
        /* this clause alone is wider than the line: let it wrap, carry on */
        lastFit = null;
        startNode = c[0]; startOff = c[1];
        i++;
        continue;
      }
      lastFit = c;
      i++;
    }
  }


  /* ── a label with a rule on one side cannot sit on a centred axis ────────
     The kicker is a short rule then the words. In a left-aligned block that is
     right: the rule starts where the text column starts. In a CENTRED block it
     is not, because the browser centres the rule and the words together, which
     pushes the words 21px right of the axis every other element is centred on
     - measured on the platform page's closing block: eyebrow centre 913,
     heading 892, standfirst 892, buttons 892. Three things on one axis and one
     just off it is exactly what reads as untidy.
     Where the block is centred, the rule is mirrored on the other side, so the
     words sit on the axis and the device still reads as one mark. */
  function axis() {
    var eb = document.querySelectorAll('.eyebrow'), i, e, p;
    for (i = 0; i < eb.length; i++) {
      e = eb[i];
      p = e.parentElement;
      if (!p) continue;
      var mid = getComputedStyle(p).textAlign === 'center';
      e.classList.toggle('is-mid', mid);
    }
  }

  function run() {
    var els = document.querySelectorAll(PROSE), i, el;
    for (i = 0; i < els.length; i++) {
      el = els[i];
      if (el.closest(SKIP)) continue;
      if (el.getAttribute('data-nowrapfix') !== null) continue;
      if (el._cwOrig === undefined) el._cwOrig = el.innerHTML;
      else el.innerHTML = el._cwOrig;
    }
    /* a second pass, after every element is back to its original markup, so
       one element's relayout cannot invalidate another's measurements */
    for (i = 0; i < els.length; i++) {
      el = els[i];
      if (el.closest(SKIP)) continue;
      if (el.getAttribute('data-nowrapfix') !== null) continue;
      try { apply(el); } catch (e) { el.innerHTML = el._cwOrig; }
    }
    axis();
    document.documentElement.classList.add('srwrap');
  }

  var t = null;
  function schedule() {
    clearTimeout(t);
    t = setTimeout(run, 180);
  }

  function start() {
    run();
    window.addEventListener('resize', schedule, { passive: true });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(schedule);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else { start(); }
})();
