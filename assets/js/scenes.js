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
          c.font = '600 10px "Space Grotesk", system-ui, sans-serif';
          c.fillStyle = K.muted;
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
            c.font = '700 10px "Space Grotesk", system-ui, sans-serif';
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
        c.font = '700 ' + (size < 26 ? 9 : 10) + 'px "Plus Jakarta Sans", system-ui, sans-serif';
        c.fillStyle = K.muted;
        c.fillText('HOURS CLOSED', cx, cy + (size < 26 ? 19 : 22));

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
            c.font = '700 9px "Space Grotesk", system-ui, sans-serif';
            c.fillStyle = K.strong; c.textAlign = 'center'; c.textBaseline = 'bottom';
            /* sit on top of the bar, not at a fixed height: at 3 AM the reader's
               own bar is the shortest one on the chart and a floating label
               would point at nothing */
            c.fillText('YOU', x + cw / 2, Math.max(10, y - 6));
          }
        });

        /* axis: a few offsets, not all twenty-four */
        if (W > 520) {
          c.font = '600 9px "Space Grotesk", system-ui, sans-serif';
          c.fillStyle = K.muted;
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
      { label: 'PHONE',     gets: 'the number',   c: '#17BDBD' },
      { label: 'CHAT',      gets: 'name + email', c: '#5B9DFF' },
      { label: 'MESSENGER', gets: 'the account',  c: '#34D186' }
    ];
    var OUT = ['Message', 'Email', 'Next offer'];
    var CYCLE = 6.4;
    var dots = [];
    for (var i = 0; i < CH.length; i++) {
      for (var k = 0; k < 3; k++) dots.push({ lane: i, t0: i * 0.5 + k * 1.5 });
    }

    function ease(t) { return t < 0 ? 0 : t > 1 ? 1 : t * t * (3 - 2 * t); }

    return {
      settleSeconds: CYCLE,
      frame: function (c, W, H, t) {
        var narrow = W < 560;
        var padY = 16;
        var laneY = [], n = CH.length;
        for (var i = 0; i < n; i++) laneY.push(padY + (H - padY * 2) * (i + 0.5) / n);
        var midY = H / 2;
        var xIn = narrow ? 92 : 132;         /* where the inlet labels end   */
        var xMid = W * 0.5;                  /* the record                    */
        var xOut = W - (narrow ? 84 : 124);  /* where the outlets begin       */
        var boxW = narrow ? 76 : 104, boxH = narrow ? 40 : 46;

        /* the three inlets */
        c.textBaseline = 'middle';
        CH.forEach(function (ch, i) {
          var y = laneY[i];
          c.textAlign = 'left';
          c.font = '800 ' + (narrow ? 8 : 9) + 'px "Space Grotesk", system-ui, sans-serif';
          c.fillStyle = ch.c;
          c.fillText(ch.label, 2, y - (narrow ? 7 : 8));
          if (!narrow) {
            c.font = '600 10px "Plus Jakarta Sans", system-ui, sans-serif';
            c.fillStyle = K.muted;
            c.fillText(ch.gets, 2, y + 8);
          }
          /* the path in */
          c.strokeStyle = K.faint; c.lineWidth = 1.5;
          c.beginPath();
          c.moveTo(xIn, y);
          c.bezierCurveTo(xIn + (xMid - xIn) * 0.5, y, xIn + (xMid - xIn) * 0.5, midY, xMid - boxW / 2, midY);
          c.stroke();
        });

        /* the paths out */
        OUT.forEach(function (_, i) {
          var y = laneY[i];
          c.strokeStyle = K.faint; c.lineWidth = 1.5;
          c.beginPath();
          c.moveTo(xMid + boxW / 2, midY);
          c.bezierCurveTo(xMid + (xOut - xMid) * 0.5, midY, xMid + (xOut - xMid) * 0.5, y, xOut, y);
          c.stroke();
          c.textAlign = 'left';
          c.font = '600 ' + (narrow ? 9 : 10) + 'px "Plus Jakarta Sans", system-ui, sans-serif';
          c.fillStyle = K.muted;
          c.fillText(OUT[i], xOut + 6, y);
        });

        /* the record in the middle */
        c.fillStyle = K.onLight ? 'rgba(11,27,51,.06)' : 'rgba(255,255,255,.07)';
        c.strokeStyle = K.accent; c.lineWidth = 1.5;
        c.beginPath();
        if (c.roundRect) c.roundRect(xMid - boxW / 2, midY - boxH / 2, boxW, boxH, 10);
        else c.rect(xMid - boxW / 2, midY - boxH / 2, boxW, boxH);
        c.fill(); c.stroke();
        c.textAlign = 'center';
        c.fillStyle = K.strong;
        c.font = '700 ' + (narrow ? 10 : 11) + 'px "Space Grotesk", system-ui, sans-serif';
        c.fillText('1 record', xMid, midY - 6);
        c.font = '600 ' + (narrow ? 8 : 9) + 'px "Plus Jakarta Sans", system-ui, sans-serif';
        c.fillStyle = K.muted;
        c.fillText('per customer', xMid, midY + 9);

        /* what is moving along the paths */
        var loop = env.reduced ? CYCLE * 0.999 : (t % CYCLE);
        dots.forEach(function (d) {
          var age = loop - d.t0;
          if (age < 0 || age > 3.4) return;
          var y0 = laneY[d.lane], x, y, col;
          if (age < 1.6) {                      /* inlet -> record */
            var u = ease(age / 1.6);
            x = xIn + (xMid - boxW / 2 - xIn) * u;
            y = y0 + (midY - y0) * ease(Math.min(1, u * 1.25));
            col = CH[d.lane].c;
          } else if (age < 2.0) {
            return;                             /* it rests in the record */
          } else {                              /* record -> outlet */
            var v = ease((age - 2.0) / 1.4);
            x = xMid + boxW / 2 + (xOut - xMid - boxW / 2) * v;
            y = midY + (y0 - midY) * ease(Math.min(1, v * 1.25));
            col = K.accent;
          }
          c.fillStyle = col;
          c.beginPath(); c.arc(x, y, 3, 0, Math.PI * 2); c.fill();
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
})();