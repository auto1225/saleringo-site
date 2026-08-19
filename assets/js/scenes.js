/* ═══════════════════════════════════════════════════════════════════════════
   scenes.js — the figures themselves.

   Each one states something the page already claims, and states it with
   arithmetic rather than with an invented statistic. Nothing here is a
   particle field: if a scene cannot be described in one true sentence, it does
   not belong on this site.
   ═══════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  if (!window.SR_SCENE) return;

  /* No palette constants here on purpose: a canvas cannot inherit a colour, and
     these figures sit on both the dark sections and the cream ones. Each scene
     takes its ink from env.ink, which is read off the surface it mounted on. */
  var TAU = Math.PI * 2;

  function ease(t) { return t < 0 ? 0 : t > 1 ? 1 : 1 - Math.pow(1 - t, 3); }
  function smooth(t) { return t < 0 ? 0 : t > 1 ? 1 : t * t * (3 - 2 * t); }

  /* ── shared drawing kit ───────────────────────────────────────────────────
     Four of these figures carry real labels, so the legibility rules live in
     one place rather than being re-derived per scene:

       MIN_PX  13px in CSS pixels is the floor. Nothing shrinks below it; text
               that will not fit at 13 is truncated instead, because a 10px
               label is not a smaller label, it is a missing one.
       SOFT    env.ink.muted is .46 alpha, which measures 4.38:1 on #081226 —
               under AA. The secondary ink here is .62 alpha (7.0:1) so every
               line of type on these figures clears 4.5:1 with room to spare.
  */
  var MIN_PX = 13;
  var GRO = '"Space Grotesk", system-ui, sans-serif';
  var JAK = '"Plus Jakarta Sans", system-ui, sans-serif';
  var CHAN = { voice: '#17BDBD', chat: '#5B9DFF', msg: '#34D186' };
  var AMBER = { dark: '#F0B454', light: '#8A5A10' };

  function soft(K) { return K.onLight ? 'rgba(11,27,51,.74)' : 'rgba(242,246,251,.62)'; }
  function panelFill(K) { return K.onLight ? 'rgba(11,27,51,.045)' : 'rgba(255,255,255,.055)'; }
  function hairLine(K) { return K.onLight ? 'rgba(11,27,51,.18)' : 'rgba(242,246,251,.20)'; }
  function amber(K) { return K.onLight ? AMBER.light : AMBER.dark; }

  function box(c, x, y, w, h, r) {
    c.beginPath();
    if (c.roundRect) c.roundRect(x, y, w, h, r);
    else c.rect(x, y, w, h);
  }

  /* set the font, then hand back a string guaranteed to fit `max` at >= 13px */
  function fit(c, s, max, weight, family, size) {
    var f = Math.max(MIN_PX, size);
    for (; f > MIN_PX; f--) {
      c.font = weight + ' ' + f + 'px ' + family;
      if (c.measureText(s).width <= max) return s;
    }
    c.font = weight + ' ' + MIN_PX + 'px ' + family;
    if (c.measureText(s).width <= max) return s;
    var t = s;
    while (t.length > 1 && c.measureText(t + '…').width > max) t = t.slice(0, -1);
    return t.replace(/[\s+\-·]+$/, '') + '…';
  }
  function label(c, s, x, y, max, weight, family, size, colour, align) {
    var t = fit(c, s, max, weight, family, size);
    c.fillStyle = colour;
    c.textAlign = align || 'left';
    c.fillText(t, x, y);
    return t;
  }
  /* a tint of a hex colour, for fills behind 13px type */
  function tint(hex, a) {
    var n = parseInt(hex.slice(1), 16);
    return 'rgba(' + (n >> 16) + ',' + ((n >> 8) & 255) + ',' + (n & 255) + ',' + a + ')';
  }
  function link(c, x1, y1, x2, y2, colour, width, alpha) {
    c.save();
    c.globalAlpha = alpha === undefined ? 0.42 : alpha;
    c.strokeStyle = colour; c.lineWidth = width || 2; c.lineCap = 'round';
    c.beginPath(); c.moveTo(x1, y1);
    c.bezierCurveTo((x1 + x2) / 2, y1, (x1 + x2) / 2, y2, x2, y2);
    c.stroke(); c.restore();
  }
  function vlink(c, x1, y1, x2, y2, colour, width, alpha) {
    c.save();
    c.globalAlpha = alpha === undefined ? 0.42 : alpha;
    c.strokeStyle = colour; c.lineWidth = width || 2; c.lineCap = 'round';
    c.beginPath(); c.moveTo(x1, y1);
    c.bezierCurveTo(x1, (y1 + y2) / 2, x2, (y1 + y2) / 2, x2, y2);
    c.stroke(); c.restore();
  }
  function tick(c, x, y, s, colour, w) {
    c.save();
    c.strokeStyle = colour; c.lineWidth = w || 2.2;
    c.lineCap = 'round'; c.lineJoin = 'round';
    c.beginPath();
    c.moveTo(x - s, y); c.lineTo(x - s * 0.25, y + s * 0.72); c.lineTo(x + s, y - s * 0.7);
    c.stroke(); c.restore();
  }
  function arrow(c, x, y, s, colour) {
    c.save();
    c.strokeStyle = colour; c.lineWidth = 2; c.lineCap = 'round'; c.lineJoin = 'round';
    c.beginPath(); c.moveTo(x - s, y); c.lineTo(x + s, y);
    c.moveTo(x + s * 0.3, y - s * 0.55); c.lineTo(x + s, y); c.lineTo(x + s * 0.3, y + s * 0.55);
    c.stroke(); c.restore();
  }
  /* scope a DOM read to the section this canvas is mounted in */
  function near(env, sel) {
    var s = env.host.closest ? env.host.closest('section') : null;
    return (s || document).querySelector(sel);
  }

  /* ── 1 · the shape of a day ───────────────────────────────────────────────
     A 24-hour dial. The claim it carries is arithmetic, not a survey: a desk
     that opens at nine and closes at six is shut for fifteen of the day's
     twenty-four hours. The sweep marks 2:47 AM, which is the headline three
     inches to its left. */
  window.SR_SCENE('nightclock', function (env) {
    var OPEN = 9, CLOSE = 18;             /* a nine-to-six desk */
    var K = env.ink;
    var w = env.width, h = env.height;
    var SWEEP = 7.2;                       /* seconds for one full day */

    function geom(W, H) {
      /* the ring plus its ticks plus the hour labels all have to fit inside the
         box, so the radius is the half-height minus that whole stack (labels
         sit at r+32 and need their own line height on top) */
      var r = Math.min(W, H) * 0.5 - 44;
      return { cx: W / 2, cy: H / 2, r: Math.max(40, r) };
    }
    /* midnight at the top, clockwise */
    function ang(hour) { return -Math.PI / 2 + (hour / 24) * TAU; }

    return {
      settleSeconds: SWEEP + 1.6,
      resize: function (W, H) { w = W; h = H; },
      frame: function (c, W, H, t) {
        var g = geom(W, H), cx = g.cx, cy = g.cy, r = g.r;
        var p = ease(t / SWEEP);
        var head = p * 24;                 /* the hour the sweep has reached */

        /* closed hours — the whole ring, drawn first and dim */
        c.lineWidth = Math.max(9, r * 0.13);
        c.lineCap = 'butt';
        c.strokeStyle = K.onLight ? 'rgba(184,122,40,.20)' : 'rgba(232,164,76,.16)';
        c.beginPath(); c.arc(cx, cy, r, 0, TAU); c.stroke();

        /* the part of the closed ring the sweep has already crossed, lit */
        function litArc(from, to, style) {
          var a = Math.min(head, to);
          if (a <= from) return;
          c.strokeStyle = style;
          c.beginPath(); c.arc(cx, cy, r, ang(from), ang(a)); c.stroke();
        }
        litArc(0, OPEN, K.warm);
        litArc(CLOSE, 24, K.warm);

        /* open hours sit inside the ring, quiet: this is the small part */
        c.strokeStyle = K.inert;
        c.lineWidth = Math.max(5, r * 0.07);
        var oa = Math.max(OPEN, Math.min(head, CLOSE));
        if (oa > OPEN) { c.beginPath(); c.arc(cx, cy, r, ang(OPEN), ang(oa)); c.stroke(); }

        /* hour ticks */
        c.lineWidth = 1;
        for (var i = 0; i < 24; i++) {
          var a2 = ang(i), major = i % 6 === 0;
          var r1 = r + (major ? 13 : 8), r2 = r + (major ? 20 : 13);
          c.strokeStyle = major ? K.muted : K.faint;
          c.beginPath();
          c.moveTo(cx + Math.cos(a2) * r1, cy + Math.sin(a2) * r1);
          c.lineTo(cx + Math.cos(a2) * r2, cy + Math.sin(a2) * r2);
          c.stroke();
        }

        /* quarter labels */
        if (r > 70) {
          c.font = '600 ' + MIN_PX + 'px ' + GRO;
          c.fillStyle = soft(K);
          c.textAlign = 'center'; c.textBaseline = 'middle';
          [[0, '12A'], [6, '6A'], [12, '12P'], [18, '6P']].forEach(function (q) {
            var a3 = ang(q[0]), rr = r + 32;
            c.fillText(q[1], cx + Math.cos(a3) * rr, cy + Math.sin(a3) * rr);
          });
        }

        /* the sweep hand */
        if (p < 1) {
          var ah = ang(head);
          var grd = c.createLinearGradient(cx, cy, cx + Math.cos(ah) * r, cy + Math.sin(ah) * r);
          grd.addColorStop(0, K.warm + '00');
          grd.addColorStop(1, K.warm);
          c.strokeStyle = grd; c.lineWidth = 2;
          c.beginPath(); c.moveTo(cx, cy);
          c.lineTo(cx + Math.cos(ah) * (r - 2), cy + Math.sin(ah) * (r - 2));
          c.stroke();
        }

        /* 2:47 AM — the moment the headline names */
        var TARGET = 2 + 47 / 60;
        if (head >= TARGET) {
          var at = ang(TARGET);
          var px = cx + Math.cos(at) * r, py = cy + Math.sin(at) * r;
          var age = (head - TARGET) / 24 * SWEEP;
          var pulse = Math.max(0, 1 - age / 1.5);
          if (pulse > 0) {
            c.globalAlpha = 0.22 * pulse; c.fillStyle = K.warm;
            c.beginPath(); c.arc(px, py, 5 + 22 * (1 - pulse), 0, TAU); c.fill();
            c.globalAlpha = 1;
          }
          c.fillStyle = K.strong;
          c.beginPath(); c.arc(px, py, 3.6, 0, TAU); c.fill();
          if (r > 70) {
            c.font = '700 ' + MIN_PX + 'px ' + GRO;
            c.fillStyle = K.warm; c.textAlign = 'right'; c.textBaseline = 'middle';
            c.fillText('2:47 AM', px - 12, py - 4);
          }
        }

        /* the count, in the middle */
        var shown = Math.min(15, Math.round(
          (Math.min(head, OPEN) + Math.max(0, head - CLOSE))));
        c.textAlign = 'center'; c.textBaseline = 'alphabetic';
        c.fillStyle = K.strong;
        /* Measure, don't guess. A fixed ratio of the radius overflowed the ring
           on a phone: "15 of 24" at 42px is wider than the dial's inner
           diameter. Shrink until it fits the clear space inside the stroke. */
        var label = shown + ' of 24';
        var room = (r - Math.max(9, r * 0.13)) * 1.72;
        var size = Math.min(46, r * 0.52);
        for (var g2 = 0; g2 < 12; g2++) {
          c.font = '600 ' + Math.round(size) + 'px "Space Grotesk", system-ui, sans-serif';
          if (c.measureText(label).width <= room || size <= 13) break;
          size -= 2;
        }
        c.fillText(label, cx, cy + 4);
        /* The caption under the count was computed at 9 or 10px, which is the one
           place in this scene that still sat under the floor. It is two short
           words and the dial's clear width is 1.72r, so 13px fits at every size
           the dial takes; the count above it gives way instead if it has to. */
        c.font = '700 ' + MIN_PX + 'px ' + JAK;
        c.fillStyle = soft(K);
        c.fillText('HOURS CLOSED', cx, cy + (size < 26 ? 22 : 26));

        return p < 1 || (head - TARGET) / 24 * SWEEP < 1.5;
      }
    };
  });

  /* ── 2 · who is awake, right now ──────────────────────────────────────────
     Twenty-four columns, one per UTC offset, lit when that offset is inside
     business hours at the moment the page is being read. No sample data: the
     only input is the reader's own clock, and the count under it is counted
     from what is drawn. */
  window.SR_SCENE('worldwake', function (env) {
    var OPEN = 9, CLOSE = 18;
    var K = env.ink;
    var OFFSETS = [];
    for (var o = -11; o <= 12; o++) OFFSETS.push(o);
    var mine = -new Date().getTimezoneOffset() / 60;
    var appear = [];
    OFFSETS.forEach(function (_, i) { appear[i] = i * 0.035; });

    function local(off) {
      var utc = new Date();
      var hh = utc.getUTCHours() + utc.getUTCMinutes() / 60 + off;
      return ((hh % 24) + 24) % 24;
    }

    return {
      settleSeconds: 2.2,
      frame: function (c, W, H, t) {
        var n = OFFSETS.length;
        var gap = W > 620 ? 4 : 2;
        var cw = (W - gap * (n - 1)) / n;
        var labelH = 18, barH = H - labelH - 20;
        var awake = 0, mineAwake = false;

        OFFSETS.forEach(function (off, i) {
          var lh = local(off);
          var on = lh >= OPEN && lh < CLOSE;
          if (on) awake++;
          if (Math.abs(off - mine) < 0.01) mineAwake = on;

          var a = ease((t - appear[i]) / 0.5);
          if (a <= 0) return;
          var x = i * (cw + gap);
          /* height carries the hour: tallest at midday, shortest at night */
          var noonness = 1 - Math.abs(lh - 12) / 12;
          var bh = barH * (0.22 + 0.78 * noonness) * a;
          var y = 20 + barH - bh;

          c.fillStyle = on ? K.accent : K.inert;
          var rr = Math.min(3, cw / 2);
          c.beginPath();
          if (c.roundRect) c.roundRect(x, y, cw, bh, rr); else c.rect(x, y, cw, bh);
          c.fill();

          if (Math.abs(off - mine) < 0.01) {
            c.strokeStyle = K.strong; c.lineWidth = 1.5;
            c.beginPath();
            if (c.roundRect) c.roundRect(x - 1.5, y - 1.5, cw + 3, bh + 3, rr + 1);
            else c.rect(x - 1.5, y - 1.5, cw + 3, bh + 3);
            c.stroke();
            c.font = '700 ' + MIN_PX + 'px ' + GRO;
            c.fillStyle = K.strong; c.textAlign = 'center'; c.textBaseline = 'bottom';
            /* sit on top of the bar, not at a fixed height: at 3 AM the reader's
               own bar is the shortest one on the chart and a floating label
               would point at nothing */
            c.fillText('YOU', x + cw / 2, Math.max(10, y - 6));
          }
        });

        /* axis: a few offsets, not all twenty-four */
        if (W > 520) {
          c.font = '600 ' + MIN_PX + 'px ' + GRO;
          c.fillStyle = soft(K);
          c.textAlign = 'center'; c.textBaseline = 'top';
          OFFSETS.forEach(function (off, i) {
            if (off % 6 !== 0) return;
            c.fillText('UTC' + (off >= 0 ? '+' : '') + off,
                       i * (cw + gap) + cw / 2, 20 + barH + 7);
          });
        }

        /* the count, read off what was just drawn. The canvas is the box; the
           sentence lives beside it in the figure, so look up, not down. */
        var fig = env.host.closest('.scenefig') || env.host.parentElement;
        var host = fig && fig.querySelector('[data-wake-count]');
        if (host) {
          host.textContent = awake + ' of 24';
          var note = fig.querySelector('[data-wake-note]');
          if (note) {
            note.textContent = mineAwake
              ? 'including yours — and the other ' + (awake - 1) + ' are somebody else’s working day.'
              : 'Yours is not one of them. Theirs is a working day; yours is not.';
          }
        }
        return t < 2.2;
      }
    };
  });

  /* ── 3 · a call being answered ────────────────────────────────────────────
     The voice pages sell a thing you cannot photograph. This is a waveform, so
     it must be said plainly on the page that it is a drawing and not a
     recording — we have no recordings to publish and will not imply one. What
     it does show truthfully is the shape of the exchange: the caller speaks,
     there is a short gap, the line answers. */
  window.SR_SCENE('callwave', function (env) {
    var K = env.ink;
    var BARS = 84;
    /* who is speaking across the timeline: 0 caller, 1 gap, 2 the line */
    var TURNS = [
      { at: 0.00, to: 0.34, who: 0 },
      { at: 0.34, to: 0.40, who: 1 },
      { at: 0.40, to: 0.78, who: 2 },
      { at: 0.78, to: 0.84, who: 1 },
      { at: 0.84, to: 1.00, who: 2 }
    ];
    var seedv = 7;
    function rnd() { seedv = (seedv * 1103515245 + 12345) & 0x7fffffff; return seedv / 0x7fffffff; }
    var amp = [];
    for (var i = 0; i < BARS; i++) amp.push(0.25 + rnd() * 0.75);

    function whoAt(f) {
      for (var i = 0; i < TURNS.length; i++)
        if (f >= TURNS[i].at && f < TURNS[i].to) return TURNS[i].who;
      return 2;
    }

    return {
      settleSeconds: 5,
      frame: function (c, W, H, t) {
        var CYCLE = 5.0;
        var p = env.reduced ? 1 : Math.min(1, (t % (CYCLE + 1.2)) / CYCLE);
        var gap = 3, bw = Math.max(1.5, (W - gap * (BARS - 1)) / BARS);
        var mid = H / 2;

        for (var i = 0; i < BARS; i++) {
          var f = i / (BARS - 1);
          var who = whoAt(f);
          var on = f <= p;
          var a = who === 1 ? 0.12 : amp[i];
          var hgt = (who === 1 ? 3 : (H * 0.42) * a);
          /* a small live wobble only on the bar the playhead is passing */
          if (on && !env.reduced && Math.abs(f - p) < 0.04 && who !== 1) {
            hgt *= 1 + 0.28 * Math.sin(t * 15 + i);
          }
          var x = i * (bw + gap);
          c.fillStyle = !on ? K.faint
                     : who === 0 ? K.muted
                     : who === 1 ? K.inert
                     : K.accent;
          c.beginPath();
          if (c.roundRect) c.roundRect(x, mid - hgt / 2, bw, hgt, bw / 2);
          else c.rect(x, mid - hgt / 2, bw, hgt);
          c.fill();
        }

        /* playhead */
        if (p < 1 && !env.reduced) {
          var px = p * W;
          c.strokeStyle = K.muted; c.lineWidth = 1;
          c.beginPath(); c.moveTo(px, H * 0.12); c.lineTo(px, H * 0.88); c.stroke();
        }
        return true;
      }
    };
  });

  /* ── 4 · what an answered conversation leaves behind ──────────────────────
     Three inlets, one record, three ways back out. This is the only figure on
     the site that draws a claim rather than a measurement, so it draws exactly
     what the sentences beside it say and nothing more: a phone call carries a
     number, a chat asks for a name and an address, a messenger thread arrives
     with the account attached — and all three land in the same record, which
     is the thing you can reach afterwards. */
  window.SR_SCENE('capturefan', function (env) {
    var K = env.ink;
    var CH = [
      { name: 'PHONE',     gets: 'the number',   c: CHAN.voice },
      { name: 'WEB CHAT',  gets: 'name + email', c: CHAN.chat  },
      { name: 'MESSENGER', gets: 'the account',  c: CHAN.msg   }
    ];
    var OUT = ['Message', 'Email', 'Next offer'];
    var CYCLE = 7.4;
    var dots = [];
    for (var i = 0; i < CH.length; i++) {
      for (var k = 0; k < 2; k++) dots.push({ lane: i, t0: i * 0.55 + k * 2.6 });
    }

    return {
      settleSeconds: CYCLE,
      frame: function (c, W, H, t) {
        var SOFT = soft(K), PANEL = panelFill(K), HAIR = hairLine(K);
        var narrow = W < 620;
        var loop = env.reduced ? CYCLE * 0.62 : (t % CYCLE);
        c.textBaseline = 'middle';

        /* ── the record card, drawn last but measured first ── */
        var recW, recH, recX, recY;

        if (!narrow) {
          /* ═══ wide: three lanes left → one record → three lanes right ═══ */
          var cw = Math.min(210, Math.max(158, W * 0.27));
          var cardH = Math.min(66, (H - 24) / 3 - 10);
          recW = Math.min(186, Math.max(148, W * 0.23)); recH = 92;
          recX = (W - recW) / 2; recY = (H - recH) / 2;
          var midY = H / 2;
          var laneY = [];
          for (var i = 0; i < 3; i++) laneY.push(12 + (H - 24) * (i + 0.5) / 3);

          /* paths first, so the cards sit on top of them */
          CH.forEach(function (ch, i) {
            link(c, cw, laneY[i], recX, midY, ch.c, 2.4, 0.5);
          });
          OUT.forEach(function (_, i) {
            link(c, recX + recW, midY, W - cw, laneY[i], K.accent, 2.4, 0.34);
          });

          /* inlets */
          CH.forEach(function (ch, i) {
            var y = laneY[i], top = y - cardH / 2;
            c.fillStyle = PANEL; box(c, 0, top, cw, cardH, 12); c.fill();
            c.fillStyle = ch.c; box(c, 0, top, 4, cardH, [12, 0, 0, 12]); c.fill();
            label(c, ch.name, 16, y - 11, cw - 26, '800', GRO, 14, ch.c);
            label(c, ch.gets, 16, y + 11, cw - 26, '600', JAK, 14, SOFT);
          });

          /* outlets */
          OUT.forEach(function (o, i) {
            var y = laneY[i], top = y - 20, x = W - cw;
            c.fillStyle = PANEL; box(c, x, top, cw, 40, 12); c.fill();
            c.strokeStyle = HAIR; c.lineWidth = 1; c.stroke();
            tick(c, x + 20, y, 5.5, K.accent);
            label(c, o, x + 34, y + 1, cw - 46, '700', JAK, 14, K.strong);
          });
        } else {
          /* ═══ narrow: three inlets on top, record, three outlets below ═══ */
          var gap = 9, colW = (W - gap * 2) / 3;
          var inH = 62, outH = 42;
          recW = Math.min(210, W * 0.66); recH = 78;
          recX = (W - recW) / 2; recY = (H - recH) / 2;
          var outTop = H - outH;

          for (var j = 0; j < 3; j++) {
            var cx = j * (colW + gap) + colW / 2;
            vlink(c, cx, inH, W / 2, recY, CH[j].c, 2.4, 0.5);
            vlink(c, W / 2, recY + recH, cx, outTop, K.accent, 2.4, 0.34);
          }
          CH.forEach(function (ch, i) {
            var x = i * (colW + gap);
            c.fillStyle = PANEL; box(c, x, 0, colW, inH, 12); c.fill();
            c.fillStyle = ch.c; box(c, x, 0, colW, 4, [12, 12, 0, 0]); c.fill();
            label(c, ch.name, x + colW / 2, 26, colW - 12, '800', GRO, 14, ch.c, 'center');
            label(c, ch.gets, x + colW / 2, 46, colW - 10, '600', JAK, 13, SOFT, 'center');
          });
          OUT.forEach(function (o, i) {
            var x = i * (colW + gap);
            c.fillStyle = PANEL; box(c, x, outTop, colW, outH, 11); c.fill();
            c.strokeStyle = HAIR; c.lineWidth = 1; c.stroke();
            label(c, o, x + colW / 2, outTop + outH / 2 + 1, colW - 10, '700', JAK, 13, K.strong, 'center');
          });
        }

        /* ── the record: the one thing all three doors write into ── */
        c.save();
        c.shadowColor = K.onLight ? 'rgba(11,27,51,.14)' : 'rgba(0,0,0,.5)';
        c.shadowBlur = 22; c.shadowOffsetY = 6;
        c.fillStyle = K.onLight ? '#FFFFFF' : '#0C1A31';
        box(c, recX, recY, recW, recH, 14); c.fill();
        c.restore();
        c.strokeStyle = K.accent; c.lineWidth = 2;
        box(c, recX, recY, recW, recH, 14); c.stroke();
        /* three colour pips on the card's top edge: which doors fed it */
        CH.forEach(function (ch, i) {
          c.fillStyle = ch.c;
          c.beginPath();
          c.arc(recX + recW / 2 + (i - 1) * 15, recY + 15, 4, 0, TAU);
          c.fill();
        });
        var rcx = recX + recW / 2;
        label(c, '1 record', rcx, recY + recH * 0.53, recW - 20, '700', GRO, 21, K.strong, 'center');
        label(c, 'per customer', rcx, recY + recH - 17, recW - 16, '600', JAK, 14, SOFT, 'center');

        /* ── what travels: a coloured packet in, a teal one out ── */
        dots.forEach(function (d) {
          var age = loop - d.t0;
          if (age < 0 || age > 3.6) return;
          var x, y, col, IN = 1.7;
          if (!narrow) {
            var lY = 12 + (H - 24) * (d.lane + 0.5) / 3, mY = H / 2;
            var cwx = Math.min(210, Math.max(158, W * 0.27));
            if (age < IN) {
              var u = smooth(age / IN);
              x = cwx + (recX - cwx) * u;
              y = lY + (mY - lY) * smooth(Math.min(1, u * 1.3));
              col = CH[d.lane].c;
            } else if (age < 2.1) { return; }
            else {
              var v = smooth((age - 2.1) / 1.5);
              x = recX + recW + (W - cwx - recX - recW) * v;
              y = mY + (lY - mY) * smooth(Math.min(1, v * 1.3));
              col = K.accent;
            }
          } else {
            var gp = 9, cW2 = (W - gp * 2) / 3;
            var cX = d.lane * (cW2 + gp) + cW2 / 2, oTop = H - 42;
            if (age < IN) {
              var u2 = smooth(age / IN);
              x = cX + (W / 2 - cX) * smooth(Math.min(1, u2 * 1.3));
              y = 62 + (recY - 62) * u2;
              col = CH[d.lane].c;
            } else if (age < 2.1) { return; }
            else {
              var v2 = smooth((age - 2.1) / 1.5);
              x = W / 2 + (cX - W / 2) * smooth(Math.min(1, v2 * 1.3));
              y = recY + recH + (oTop - recY - recH) * v2;
              col = K.accent;
            }
          }
          c.fillStyle = col;
          c.beginPath(); c.arc(x, y, 4, 0, TAU); c.fill();
        });

        return true;
      }
    };
  });

  /* ── 5 · the page they are already reading ────────────────────────────────
     The web-chat page argues that one script tag turns a page a visitor is
     already on into a conversation. Its hero sat on flat white, which said
     nothing. This draws the thing the sentence is about: the faint wireframe
     of a site — masthead, hero block, columns of text, an image well — with
     the widget arriving in the corner. It is a drawing of where the product
     lives, not a chart, so it carries no numbers and claims none. Kept at very
     low contrast: it is a ground, and the copy on top of it has to win. */
  window.SR_SCENE('sitewire', function (env) {
    var K = env.ink;
    var seed = 21;
    function rnd() { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; }
    var lines = [];
    for (var i = 0; i < 30; i++) lines.push(0.40 + rnd() * 0.60);

    return {
      settleSeconds: 3.4,
      frame: function (c, W, H, t) {
        var p = Math.min(1, t / 2.2);
        var light = K.onLight;
        var ink = light ? 'rgba(11,27,51,' : 'rgba(242,246,251,';

        /* One page, drawn as a page: a card with an edge, set off to the side
           and running past the bottom so it reads as a browser window sitting
           behind this one rather than as marks under the headline. */
        /* Big enough to read as a page and offset up-left of the code window,
           so its masthead and left edge stay visible behind it rather than
           being covered entirely. */
        var pw = Math.min(W * 0.62, 820);
        var ph = pw * 0.80;
        var x0 = W * 0.40;
        var y0 = H * 0.14;
        var u = pw / 26;

        c.save();
        c.globalAlpha = p;

        /* the page itself */
        /* a real card: it needs an edge and a shadow or it is just a wash */
        c.shadowColor = light ? 'rgba(11,27,51,.10)' : 'rgba(0,0,0,.5)';
        c.shadowBlur = 40; c.shadowOffsetY = 18;
        c.fillStyle = light ? 'rgba(255,255,255,.92)' : 'rgba(255,255,255,.04)';
        c.strokeStyle = ink + (light ? '0.14' : '0.11') + ')';
        c.lineWidth = 1;
        c.beginPath();
        if (c.roundRect) c.roundRect(x0, y0, pw, ph, 16); else c.rect(x0, y0, pw, ph);
        c.fill();
        c.shadowColor = 'transparent'; c.shadowBlur = 0; c.shadowOffsetY = 0;
        c.stroke();

        /* browser chrome */
        c.fillStyle = ink + '0.05)';
        c.beginPath();
        if (c.roundRect) c.roundRect(x0, y0, pw, u * 1.5, [16, 16, 0, 0]);
        else c.rect(x0, y0, pw, u * 1.5);
        c.fill();
        for (var k = 0; k < 3; k++) {
          c.fillStyle = ink + '0.18)';
          c.beginPath(); c.arc(x0 + u * (0.8 + k * 0.5), y0 + u * 0.75, 2.6, 0, Math.PI * 2); c.fill();
        }
        c.fillStyle = ink + '0.09)';
        c.beginPath();
        if (c.roundRect) c.roundRect(x0 + u * 3, y0 + u * 0.4, pw * 0.42, u * 0.7, 5);
        else c.rect(x0 + u * 3, y0 + u * 0.4, pw * 0.42, u * 0.7);
        c.fill();

        function bar(x, y, w, h, a, r) {
          c.fillStyle = ink + a + ')';
          c.beginPath();
          if (c.roundRect) c.roundRect(x, y, w, h, r === undefined ? 3 : r);
          else c.rect(x, y, w, h);
          c.fill();
        }

        /* the imagined page's own hero */
        bar(x0 + u * 1.4, y0 + u * 3.0, pw * 0.40, u * 0.62, 0.16, 4);
        bar(x0 + u * 1.4, y0 + u * 4.0, pw * 0.31, u * 0.62, 0.16, 4);
        bar(x0 + u * 1.4, y0 + u * 5.3, pw * 0.26, u * 0.28, 0.09, 3);
        bar(x0 + u * 1.4, y0 + u * 5.9, pw * 0.21, u * 0.28, 0.09, 3);
        bar(x0 + u * 1.4, y0 + u * 7.0, u * 4.0, u * 0.9, 0.15, 8);
        bar(x0 + pw * 0.60, y0 + u * 3.0, pw * 0.34, u * 5.0, 0.08, 10);

        /* body columns */
        for (var col = 0; col < 2; col++) {
          for (var L = 0; L < 12; L++) {
            bar(x0 + u * 1.4 + col * (pw * 0.46),
                y0 + u * 9.6 + L * u * 0.62,
                (pw * 0.40) * lines[col * 12 + L], u * 0.22, 0.08, 3);
          }
        }

        /* the widget, arriving where it actually sits */
        var q = Math.max(0, Math.min(1, (t - 1.3) / 0.9));
        if (q > 0) {
          var bw = u * 4.6, bh = u * 2.0;
          var bx = x0 + pw - u * 1.3 - bw, by = y0 + ph - u * 1.3 - bh + (1 - q) * 12;
          c.globalAlpha = p * q * 0.26; c.fillStyle = K.accent;
          c.beginPath();
          if (c.roundRect) c.roundRect(bx, by, bw, bh, 12); else c.rect(bx, by, bw, bh);
          c.fill();
          c.globalAlpha = p * q * 0.75; c.strokeStyle = K.accent; c.lineWidth = 1.4; c.stroke();
          c.globalAlpha = p * q * 0.6; c.fillStyle = K.accent;
          for (var d2 = 0; d2 < 3; d2++) {
            c.beginPath();
            c.arc(bx + bw / 2 - 9 + d2 * 9, by + bh / 2, 2.4, 0, Math.PI * 2); c.fill();
          }
        }
        c.restore();
        return t < 3.4;
      }
    };
  });

  /* ── 6 · one question, six finished objects ───────────────────────────────
     Claim: one customer question does not produce one answer — it produces six
     machine objects, and the ones that stay empty stayed empty on purpose.

     This figure does not invent its own state. It reads the six frames the
     demo beside it is actually filling in, so the count under it is counted
     off the page rather than authored: nothing here can drift out of step with
     what the reader just clicked. Before the first click it says so plainly. */
  window.SR_SCENE('sixjobs', function (env) {
    var K = env.ink;
    var LONG  = ['Pipeline', 'Calendar', 'Quote', 'Customer record', 'Staff task', 'Follow-up'];
    var TIGHT = ['Pipeline', 'Calendar', 'Quote', 'Record', 'Staff task', 'Follow-up'];
    var grid = null, gridTried = false;
    var last = ['wait', 'wait', 'wait', 'wait', 'wait', 'wait'];
    var mark = [-9, -9, -9, -9, -9, -9];

    function state() {
      if (!gridTried) { grid = near(env, '[data-play-out]'); gridTried = true; }
      var boxes = grid ? grid.querySelectorAll('.obox') : [];
      var out = [];
      for (var i = 0; i < 6; i++) {
        var b = boxes[i];
        out.push(!b ? 'wait'
               : b.classList.contains('filled') ? 'made'
               : b.classList.contains('empty')  ? 'blank' : 'wait');
      }
      return out;
    }

    return {
      settleSeconds: 2,
      frame: function (c, W, H, t) {
        var SOFT = soft(K), PANEL = panelFill(K), HAIR = hairLine(K), AM = amber(K);
        var st = state();
        var made = 0, blank = 0;
        for (var i = 0; i < 6; i++) {
          if (st[i] !== last[i]) { last[i] = st[i]; mark[i] = t; }
          if (st[i] === 'made') made++; else if (st[i] === 'blank') blank++;
        }
        var touched = made + blank;
        c.textBaseline = 'middle';

        var narrow = W < 700;
        var qx, qy, qw, qh, cols, rows, gx, gy, gw, gh;
        var gap = 10;
        if (narrow) {
          qx = 0; qy = 0; qw = W; qh = 72;
          gx = 0; gy = qh + 14; gw = W; gh = H - gy;
          cols = 2; rows = 3;
        } else {
          qw = Math.min(232, Math.max(192, W * 0.25));
          qx = 0; qy = 0; qh = H;
          gx = qw + 26; gw = W - gx; gy = 0; gh = H;
          cols = 3; rows = 2;
        }
        var tw = (gw - gap * (cols - 1)) / cols;
        var th = (gh - gap * (rows - 1)) / rows;

        function tileAt(i) {
          var r = Math.floor(i / cols), k = i % cols;
          return { x: gx + k * (tw + gap), y: gy + r * (th + gap), w: tw, h: th };
        }

        /* ── fan lines: one origin, six destinations ── */
        var ox = narrow ? W / 2 : qx + qw, oy = narrow ? qy + qh : qy + qh / 2;
        for (var f = 0; f < 6; f++) {
          var T = tileAt(f);
          var on = st[f] !== 'wait';
          var col = st[f] === 'made' ? K.accent : st[f] === 'blank' ? AM : HAIR;
          if (narrow) vlink(c, ox, oy, T.x + T.w / 2, T.y, col, on ? 2.4 : 1.4, on ? 0.5 : 0.5);
          else        link(c, ox, oy, T.x, T.y + T.h / 2, col, on ? 2.4 : 1.4, on ? 0.5 : 0.5);
          /* a packet runs the line for 0.7s after a frame changes state */
          var age = t - mark[f];
          if (on && age >= 0 && age < 0.7) {
            var u = smooth(age / 0.7);
            var px = narrow ? ox + (T.x + T.w / 2 - ox) * u : ox + (T.x - ox) * u;
            var py = narrow ? oy + (T.y - oy) * u : oy + (T.y + T.h / 2 - oy) * u;
            c.fillStyle = col;
            c.beginPath(); c.arc(px, py, 4.5, 0, TAU); c.fill();
          }
        }

        /* ── the question node, and the tally read off the six frames ── */
        c.fillStyle = PANEL; box(c, qx, qy, qw, qh, 14); c.fill();
        c.strokeStyle = HAIR; c.lineWidth = 1; c.stroke();
        var pad = 16;
        if (narrow) {
          label(c, '1 question', qx + pad, qy + 26, qw * 0.5, '700', GRO, 19, K.strong);
          label(c, 'in', qx + pad, qy + 50, qw * 0.5, '600', JAK, 14, SOFT);
          c.textAlign = 'right';
          if (touched === 0) {
            label(c, 'Nothing asked yet', qx + qw - pad, qy + 28, qw * 0.44, '700', JAK, 14, SOFT, 'right');
            label(c, 'click a question below', qx + qw - pad, qy + 50, qw * 0.44, '600', JAK, 13, SOFT, 'right');
          } else {
            label(c, made + ' of 6 built', qx + qw - pad, qy + 28, qw * 0.46, '800', GRO, 17, K.accent, 'right');
            label(c, blank ? blank + ' empty on purpose' : 'nothing left undone',
                  qx + qw - pad, qy + 50, qw * 0.46, '600', JAK, 13, blank ? AM : SOFT, 'right');
          }
        } else {
          var cy = qy + qh / 2;
          label(c, '1 question', qx + pad, cy - 52, qw - pad * 2, '700', GRO, 22, K.strong);
          label(c, 'from the customer', qx + pad, cy - 30, qw - pad * 2, '600', JAK, 14, SOFT);
          c.strokeStyle = HAIR; c.lineWidth = 1;
          c.beginPath(); c.moveTo(qx + pad, cy - 12); c.lineTo(qx + qw - pad, cy - 12); c.stroke();
          if (touched === 0) {
            label(c, 'Nothing asked yet', qx + pad, cy + 10, qw - pad * 2, '700', JAK, 15, K.strong);
            label(c, 'Click a question below and', qx + pad, cy + 32, qw - pad * 2, '600', JAK, 13, SOFT);
            label(c, 'watch all six fill in.', qx + pad, cy + 50, qw - pad * 2, '600', JAK, 13, SOFT);
          } else {
            label(c, made + ' of 6', qx + pad, cy + 16, qw - pad * 2, '800', GRO, 30, K.accent);
            label(c, 'from that one answer', qx + pad, cy + 40, qw - pad * 2, '600', JAK, 13, SOFT);
            if (blank) label(c, blank + ' empty on purpose', qx + pad, cy + 60, qw - pad * 2, '700', JAK, 13, AM);
          }
        }

        /* ── the six frames ── */
        for (var i2 = 0; i2 < 6; i2++) {
          var B = tileAt(i2), s = st[i2];
          var made2 = s === 'made', bl = s === 'blank';
          var col2 = made2 ? K.accent : bl ? AM : HAIR;
          /* Opaque base first. The six fan lines pass behind these tiles, and a
             translucent tint let the line to the third column read as a scratch
             across the first one. The tile has to be a surface, not a wash. */
          c.fillStyle = K.onLight ? '#FFFFFF' : '#0A1627';
          box(c, B.x, B.y, B.w, B.h, 12); c.fill();
          c.fillStyle = made2 ? tint(K.accent, K.onLight ? 0.10 : 0.15)
                      : bl    ? tint(AM, K.onLight ? 0.10 : 0.15)
                      : PANEL;
          box(c, B.x, B.y, B.w, B.h, 12); c.fill();
          c.save();
          c.strokeStyle = col2; c.lineWidth = made2 || bl ? 1.8 : 1;
          if (!made2 && !bl) c.setLineDash([4, 4]);
          box(c, B.x, B.y, B.w, B.h, 12); c.stroke();
          c.restore();

          /* a fresh frame flashes once, so the reader sees WHICH one landed */
          var age2 = t - mark[i2];
          if ((made2 || bl) && age2 >= 0 && age2 < 0.9) {
            c.save();
            c.globalAlpha = 0.5 * (1 - age2 / 0.9);
            c.strokeStyle = col2; c.lineWidth = 3;
            box(c, B.x - 2, B.y - 2, B.w + 4, B.h + 4, 14); c.stroke();
            c.restore();
          }

          var lx = B.x + 14, ly = B.y + B.h / 2;
          var name = (B.w < 168 ? TIGHT : LONG)[i2];
          label(c, name, lx, ly - 13, B.w - 28, '800', GRO, 15, K.strong);
          if (made2) {
            tick(c, lx + 6, ly + 13, 5, K.accent);
            label(c, 'built', lx + 20, ly + 13, B.w - 34, '700', JAK, 13, K.accent);
          } else if (bl) {
            arrow(c, lx + 6, ly + 13, 5, AM);
            label(c, 'empty on purpose', lx + 20, ly + 13, B.w - 34, '700', JAK, 13, AM);
          } else {
            label(c, 'waiting', lx, ly + 13, B.w - 28, '600', JAK, 13, SOFT);
          }
        }
        return true;
      }
    };
  });

  /* ── 7 · where the number came from ───────────────────────────────────────
     Claim: every figure in the answer is a line the reader typed, the lines it
     did not use stay dark, and a question the list does not cover produces no
     number at all.

     Like the figure above it, this one reads the lab beside it rather than
     holding its own copy of the data — the highlighted rows are the rows the
     quote actually used. "0 invented" is the whole product argument, so it is
     drawn at the size of a headline and not as a footnote. */
  window.SR_SCENE('pricetrace', function (env) {
    var K = env.ink;
    var listEl = null, outEl = null, tried = false;

    function read() {
      if (!tried) {
        listEl = near(env, '[data-lab-list]');
        outEl  = near(env, '[data-lab-out]');
        tried  = true;
      }
      var lines = [];
      if (listEl) {
        Array.prototype.forEach.call(listEl.querySelectorAll('.labpill'), function (p) {
          var b = p.querySelector('b');
          var txt = p.textContent || '';
          var price = b ? b.textContent.trim() : '';
          lines.push({ label: txt.replace(price, '').trim(), price: price, used: false });
        });
      }
      var card = outEl && outEl.querySelector('.labcard');
      var mode = !card ? 'idle' : card.classList.contains('nomatch') ? 'nomatch' : 'quote';
      var total = '', usedN = 0;
      if (mode === 'quote') {
        Array.prototype.forEach.call(card.querySelectorAll('.qline'), function (q) {
          if (q.classList.contains('tot')) {
            var v = q.querySelector('.v'); total = v ? v.textContent.trim() : '';
            return;
          }
          var d = q.querySelector('.d');
          if (!d) return;
          var nm = d.textContent.trim();
          for (var i = 0; i < lines.length; i++) {
            if (lines[i].label === nm) { lines[i].used = true; usedN++; break; }
          }
        });
      }
      return { lines: lines, mode: mode, total: total, used: usedN };
    }

    return {
      settleSeconds: 1.4,
      frame: function (c, W, H, t) {
        var SOFT = soft(K), PANEL = panelFill(K), HAIR = hairLine(K), AM = amber(K);
        var D = read();
        var narrow = W < 720;
        c.textBaseline = 'middle';

        var lx, ly, lw, lh, nx, ny, nw, nh;
        var rowH = 28;
        if (narrow) {
          lx = 0; ly = 0; lw = W; nh = 116;
          nx = 0; ny = H - nh; nw = W;
          lh = H - nh - 18;
        } else {
          lw = Math.min(360, W * 0.46); lx = 0; ly = 0; lh = H;
          nw = Math.min(320, W - lw - 54); nx = W - nw; ny = (H - 150) / 2; nh = 150;
        }

        /* A panel sized to the box rather than to the list left a short list
           floating in a field of nothing, and squeezed the traces down to a
           stub. Size the panel to what it actually holds, then let the traces
           have the space that frees up. */
        var maxRows = Math.max(1, Math.floor((lh - 58) / rowH));
        var show0 = Math.min(D.lines.length, maxRows);
        var more0 = D.lines.length - show0;
        if (more0 > 0 && show0 > 1) { show0 -= 1; more0 += 1; }
        var need = 58 + Math.max(D.lines.length ? show0 : 2, 1) * rowH + (more0 > 0 ? 22 : 8);
        lh = Math.min(lh, need);
        if (!narrow) ly = Math.max(0, (H - lh) / 2);

        /* ── the list panel ── */
        c.fillStyle = PANEL; box(c, lx, ly, lw, lh, 14); c.fill();
        c.strokeStyle = HAIR; c.lineWidth = 1; c.stroke();
        var head = D.lines.length
          ? D.lines.length + (D.lines.length === 1 ? ' line you typed' : ' lines you typed')
          : 'Your price list — nothing pasted yet';
        label(c, head, lx + 16, ly + 22, lw - 32, '800', GRO, 14, K.strong);
        c.strokeStyle = HAIR; c.lineWidth = 1;
        c.beginPath(); c.moveTo(lx + 16, ly + 38); c.lineTo(lx + lw - 16, ly + 38); c.stroke();

        var top = ly + 48, show = show0, more = more0;

        var anchors = [];
        for (var i = 0; i < show; i++) {
          var L = D.lines[i], ry = top + i * rowH;
          c.fillStyle = L.used ? tint(K.accent, K.onLight ? 0.14 : 0.18)
                               : (K.onLight ? 'rgba(11,27,51,.04)' : 'rgba(255,255,255,.04)');
          box(c, lx + 12, ry, lw - 24, rowH - 5, 7); c.fill();
          if (L.used) {
            c.fillStyle = K.accent;
            box(c, lx + 12, ry, 3, rowH - 5, [7, 0, 0, 7]); c.fill();
          }
          var pw = 0;
          if (L.price) {
            c.font = '800 13px ' + GRO;
            pw = c.measureText(L.price).width + 14;
            label(c, L.price, lx + lw - 22, ry + (rowH - 5) / 2, 92, '800', GRO, 13,
                  L.used ? K.accent : SOFT, 'right');
          }
          label(c, L.label, lx + 24, ry + (rowH - 5) / 2, lw - 46 - pw, '600', JAK, 13,
                L.used ? K.strong : SOFT);
          if (L.used) anchors.push({ x: lx + lw - 12, y: ry + (rowH - 5) / 2, bx: lx + lw / 2, by: ry });
        }
        if (more > 0) {
          label(c, '+ ' + more + ' more in your list', lx + 24, top + show * rowH + 8,
                lw - 48, '600', JAK, 13, SOFT);
        }
        if (!D.lines.length) {
          label(c, 'Load a sample on the left, or paste', lx + 16, top + 8, lw - 32, '600', JAK, 13, SOFT);
          label(c, 'the prices you actually charge.',    lx + 16, top + 28, lw - 32, '600', JAK, 13, SOFT);
        }

        /* ── the traces ── */
        var col = D.mode === 'nomatch' ? AM : K.accent;
        anchors.forEach(function (a) {
          if (narrow) vlink(c, a.bx, ly + lh, nx + nw / 2, ny, col, 2.2, 0.45);
          else        link(c, a.x, a.y, nx, ny + nh / 2, col, 2.2, 0.45);
        });
        if (D.mode === 'nomatch') {
          if (narrow) vlink(c, lx + lw / 2, ly + lh, nx + nw / 2, ny, AM, 2, 0.3);
          else        link(c, lx + lw, ly + lh / 2, nx, ny + nh / 2, AM, 2, 0.3);
        }

        /* ── the verdict ── */
        var vcol = D.mode === 'nomatch' ? AM : D.mode === 'quote' ? K.accent : HAIR;
        c.fillStyle = D.mode === 'idle' ? PANEL : tint(D.mode === 'nomatch' ? AM : K.accent,
                                                       K.onLight ? 0.09 : 0.12);
        box(c, nx, ny, nw, nh, 14); c.fill();
        c.save();
        c.strokeStyle = vcol; c.lineWidth = D.mode === 'idle' ? 1 : 2;
        if (D.mode === 'idle') c.setLineDash([4, 4]);
        box(c, nx, ny, nw, nh, 14); c.stroke();
        c.restore();

        var cx = nx + nw / 2;
        if (D.mode === 'quote') {
          label(c, 'IT QUOTED', cx, ny + 24, nw - 28, '800', GRO, 13, SOFT, 'center');
          label(c, D.total || '—', cx, ny + 56, nw - 28, '800', GRO, 34, K.accent, 'center');
          label(c, 'from ' + D.used + ' of ' + D.lines.length + ' lines you typed',
                cx, ny + 86, nw - 24, '600', JAK, 14, K.strong, 'center');
          label(c, '0 numbers invented', cx, ny + nh - 24, nw - 24, '800', GRO, 15, K.strong, 'center');
        } else if (D.mode === 'nomatch') {
          label(c, 'IT REFUSED TO GUESS', cx, ny + 24, nw - 28, '800', GRO, 13, SOFT, 'center');
          label(c, 'no number', cx, ny + 56, nw - 28, '800', GRO, 30, AM, 'center');
          label(c, 'nothing you typed covers it', cx, ny + 86, nw - 24, '600', JAK, 14, K.strong, 'center');
          label(c, 'handed to a person', cx, ny + nh - 24, nw - 24, '800', GRO, 15, AM, 'center');
        } else {
          label(c, 'THE ANSWER', cx, ny + 26, nw - 28, '800', GRO, 13, SOFT, 'center');
          label(c, 'Nothing asked yet', cx, ny + 58, nw - 24, '700', JAK, 17, K.strong, 'center');
          label(c, 'Every figure it gives back will be', cx, ny + 86, nw - 24, '600', JAK, 13, SOFT, 'center');
          label(c, 'one of the lines above — lit up.',   cx, ny + 106, nw - 24, '600', JAK, 13, SOFT, 'center');
        }
        return true;
      }
    };
  });

  /* ── 8 · three doors, one key ─────────────────────────────────────────────
     Claim: the three channels are three genuinely different arrivals — a ring,
     a typed bubble, a delivered message — and the colour on each is the same
     colour that channel wears everywhere else on this site, so you can tell at
     a glance which of the three you are looking at. All three drain into one
     record, which is the only thing they have in common.

     The three device mock-ups above it could not be told apart. This is the
     key to them, drawn once, with the labels large enough to read on a phone. */
  window.SR_SCENE('chankey', function (env) {
    var K = env.ink;
    var C3 = [
      { name: 'AI PHONE',  tight: 'PHONE', c: CHAN.voice, cap: 'It rings your number', tiny: 'It rings',   g: 'ring' },
      { name: 'WEB CHAT',  tight: 'CHAT',  c: CHAN.chat,  cap: 'It sits on your page', tiny: 'It types',   g: 'bubble' },
      { name: 'MESSENGER', tight: 'MSG',   c: CHAN.msg,   cap: 'Their app, your name', tiny: 'It messages', g: 'ticks' }
    ];

    function ring(c, x, y, s, col, t) {
      c.save();
      c.strokeStyle = col; c.lineCap = 'round';
      for (var i = 0; i < 3; i++) {
        var ph = ((t * 0.8 + i / 3) % 1);
        c.globalAlpha = 0.75 * (1 - ph);
        c.lineWidth = 2.4;
        c.beginPath();
        c.arc(x, y, s * (0.34 + ph * 0.72), -0.72, 0.72);
        c.stroke();
        c.beginPath();
        c.arc(x, y, s * (0.34 + ph * 0.72), Math.PI - 0.72, Math.PI + 0.72);
        c.stroke();
      }
      c.globalAlpha = 1; c.fillStyle = col;
      c.beginPath(); c.arc(x, y, s * 0.22, 0, TAU); c.fill();
      c.restore();
    }
    function bubble(c, x, y, s, col, t) {
      c.save();
      var w = s * 1.7, h = s * 0.98;
      c.fillStyle = tint(col, 0.24); c.strokeStyle = col; c.lineWidth = 2;
      box(c, x - w / 2, y - h / 2, w, h, 9); c.fill(); c.stroke();
      c.beginPath();
      c.moveTo(x - w / 2 + 8, y + h / 2);
      c.lineTo(x - w / 2 + 4, y + h / 2 + 8);
      c.lineTo(x - w / 2 + 18, y + h / 2);
      c.closePath(); c.fillStyle = tint(col, 0.24); c.fill();
      c.fillStyle = col;
      for (var d = 0; d < 3; d++) {
        c.globalAlpha = 0.4 + 0.6 * Math.abs(Math.sin(t * 3 + d * 0.7));
        c.beginPath(); c.arc(x - s * 0.4 + d * s * 0.4, y, 2.8, 0, TAU); c.fill();
      }
      c.restore();
    }
    function ticks(c, x, y, s, col, t) {
      c.save();
      var w = s * 1.8;
      c.fillStyle = tint(col, 0.14);
      box(c, x - w / 2, y - s * 0.62, w * 0.74, s * 0.46, 6); c.fill();
      c.fillStyle = tint(col, 0.3); c.strokeStyle = col; c.lineWidth = 1.6;
      box(c, x - w / 2 + w * 0.26, y + s * 0.1, w * 0.74, s * 0.46, 6); c.fill(); c.stroke();
      var on = (t % 2.4) > 0.7;
      c.globalAlpha = on ? 1 : 0.28;
      /* the pair of ticks has to sit INSIDE the outgoing bubble, whose right
         edge is at x + w*0.5 — at 0.36/0.50 the second one straddled it */
      tick(c, x + w * 0.28, y + s * 0.33, 4, col, 2);
      tick(c, x + w * 0.40, y + s * 0.33, 4, col, 2);
      c.restore();
    }

    return {
      settleSeconds: 2.2,
      frame: function (c, W, H, t) {
        var SOFT = soft(K), PANEL = panelFill(K), HAIR = hairLine(K);
        c.textBaseline = 'middle';
        var gap = W < 460 ? 8 : 16;
        var colW = (W - gap * 2) / 3;
        var tightCol = colW < 150;
        var baseH = W < 460 ? 62 : 70;
        var panelH = H - baseH - 26;

        C3.forEach(function (ch, i) {
          var x = i * (colW + gap);
          c.fillStyle = PANEL; box(c, x, 0, colW, panelH, 14); c.fill();
          c.strokeStyle = HAIR; c.lineWidth = 1; c.stroke();
          c.fillStyle = ch.c; box(c, x, 0, colW, 5, [14, 14, 0, 0]); c.fill();

          label(c, tightCol ? ch.tight : ch.name, x + colW / 2, 28,
                colW - 12, '800', GRO, 15, ch.c, 'center');

          var gy = panelH * 0.56, gs = Math.min(colW * 0.34, panelH * 0.26);
          if (ch.g === 'ring')   ring(c,   x + colW / 2, gy, gs, ch.c, t);
          if (ch.g === 'bubble') bubble(c, x + colW / 2, gy, gs, ch.c, t);
          if (ch.g === 'ticks')  ticks(c,  x + colW / 2, gy, gs, ch.c, t);

          label(c, tightCol ? ch.tiny : ch.cap, x + colW / 2, panelH - 22,
                colW - 10, '600', JAK, 13, SOFT, 'center');

          /* the drop into the shared record */
          var bx = x + colW / 2, by = H - baseH;
          vlink(c, bx, panelH, bx, by, ch.c, 2.4, 0.55);
          var ph = ((t * 0.55 + i * 0.33) % 1);
          c.fillStyle = ch.c;
          c.beginPath();
          c.arc(bx, panelH + (by - panelH) * smooth(ph), 4, 0, TAU);
          c.fill();
        });

        /* ── the one thing all three share ── */
        var by2 = H - baseH;
        c.fillStyle = tint(K.accent, K.onLight ? 0.09 : 0.12);
        box(c, 0, by2, W, baseH, 14); c.fill();
        c.strokeStyle = K.accent; c.lineWidth = 2;
        box(c, 0, by2, W, baseH, 14); c.stroke();
        label(c, 'ONE RECORD · ONE INBOX', W / 2, by2 + baseH * 0.38,
              W - 28, '800', GRO, 16, K.strong, 'center');
        label(c, 'whichever of the three doors they used', W / 2, by2 + baseH * 0.74,
              W - 24, '600', JAK, 13, SOFT, 'center');
        return true;
      }
    };
  });
})();