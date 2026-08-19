/* ═══════════════════════════════════════════════════════════════════════════
   canvas.js — figures that argue, not decoration.

   Three rules this file enforces, because a canvas breaks all three by default:

   1. It never animates off-screen. DEV_SPEC 5.4 forbids a scroll listener, so
      visibility comes from IntersectionObserver, and a backgrounded tab stops
      the loop entirely. A canvas painting behind a tab nobody is looking at is
      the most expensive thing a marketing page can do.
   2. It is invisible to assistive technology. Every canvas here is aria-hidden
      and its host element carries the same fact in text. If the canvas fails to
      start — old browser, blocked script, GPU crash — the sentence is still
      there and the page still makes its argument.
   3. It respects prefers-reduced-motion by drawing the finished state once,
      not by animating faster or not at all. The reader still gets the figure.

   Scenes register themselves and receive a context; they never touch layout.
   ═══════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var scenes = {};
  var live = [];
  var REDUCED = window.matchMedia &&
                window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Cap the backing store at 2×. Beyond that the pixel cost doubles again for
     a difference nobody can see on the kind of figure drawn here. */
  function dpr() { return Math.min(window.devicePixelRatio || 1, 2); }

  function sizeTo(cv, host) {
    var r = host.getBoundingClientRect();
    var w = Math.max(1, Math.round(r.width));
    var h = Math.max(1, Math.round(r.height));
    var d = dpr();
    if (cv.width === w * d && cv.height === h * d) return false;
    cv.width = w * d;
    cv.height = h * d;
    cv.style.width = w + 'px';
    cv.style.height = h + 'px';
    return true;
  }

  /* A canvas cannot inherit a colour. These figures sit on both the dark
     sections and the cream ones, so hard-coding white ink makes a scene
     invisible the first time it is reused on a light surface. Read the surface
     the host is actually painted on and hand the scene an ink set for it. */
  function inkFor(host) {
    var n = host, bg = null;
    while (n && n !== document.documentElement) {
      var c = getComputedStyle(n).backgroundColor;
      var m = c.match(/[\d.]+/g);
      if (m && (m[3] === undefined || +m[3] >= 0.6)) { bg = m; break; }
      n = n.parentElement;
    }
    var lum = bg ? (0.299 * +bg[0] + 0.587 * +bg[1] + 0.114 * +bg[2]) / 255 : 0.03;
    var light = lum > 0.55;
    return {
      onLight: light,
      strong: light ? '#0B1B33' : '#F2F6FB',                    /* headline ink   */
      muted:  light ? 'rgba(11,27,51,.62)' : 'rgba(242,246,251,.46)',
      faint:  light ? 'rgba(11,27,51,.13)' : 'rgba(242,246,251,.16)',
      inert:  light ? 'rgba(11,27,51,.16)' : 'rgba(148,162,184,.22)', /* "off" bars */
      accent: '#17BDBD',
      warm:   light ? '#B87A28' : '#E8A44C'
    };
  }

  function mount(host) {
    var name = host.getAttribute('data-scene');
    var make = scenes[name];
    if (!make) return;

    var cv = document.createElement('canvas');
    cv.className = 'scenecv';
    /* the host already states the same fact in text */
    cv.setAttribute('aria-hidden', 'true');
    var ctx = cv.getContext('2d', { alpha: true });
    if (!ctx) return;                       /* no 2d context: the text stands alone */
    host.insertBefore(cv, host.firstChild);
    host.classList.add('scene-on');

    var scene, raf = null, visible = false, started = 0, ok = true;

    function draw(t) {
      raf = null;
      if (!ok) return;
      var w = cv.width / dpr(), h = cv.height / dpr();
      ctx.save();
      ctx.scale(dpr(), dpr());
      ctx.clearRect(0, 0, w, h);
      var more = false;
      try {
        more = scene.frame(ctx, w, h, (t - started) / 1000);
      } catch (e) {
        ok = false;                          /* a broken scene must not loop forever */
        host.classList.remove('scene-on');
        cv.remove();
        return;
      }
      ctx.restore();
      if (more && visible && !document.hidden && !REDUCED) {
        raf = requestAnimationFrame(draw);
      }
    }

    function kick() {
      if (raf || !ok) return;
      if (!started) started = performance.now();
      raf = requestAnimationFrame(draw);
    }

    function stop() {
      if (raf) { cancelAnimationFrame(raf); raf = null; }
    }

    function relayout() {
      if (!sizeTo(cv, host)) return;
      if (scene.resize) scene.resize(cv.width / dpr(), cv.height / dpr());
      /* redraw the current frame at the new size even while paused */
      var keep = visible; visible = true; stop(); draw(performance.now()); visible = keep;
    }

    sizeTo(cv, host);
    scene = make({
      host: host,
      width: cv.width / dpr(),
      height: cv.height / dpr(),
      reduced: REDUCED,
      ink: inkFor(host)
    });
    if (!scene || typeof scene.frame !== 'function') { cv.remove(); return; }

    if (REDUCED) {
      /* one frame, at the end state: the figure without the motion */
      started = performance.now() - (scene.settleSeconds || 6) * 1000;
      draw(performance.now());
    } else {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          visible = e.isIntersecting;
          if (visible) kick(); else stop();
        });
      }, { rootMargin: '80px' }).observe(host);
    }

    if (window.ResizeObserver) {
      new ResizeObserver(relayout).observe(host);
    } else {
      window.addEventListener('resize', relayout);
    }

    live.push({ stop: stop, kick: function () { if (visible) kick(); } });
  }

  /* a backgrounded tab paints nothing */
  document.addEventListener('visibilitychange', function () {
    live.forEach(function (s) { document.hidden ? s.stop() : s.kick(); });
  });

  function mountAll(name) {
    var sel = name ? '[data-scene="' + name + '"]' : '[data-scene]';
    Array.prototype.forEach.call(document.querySelectorAll(sel), function (host) {
      if (host.dataset.sceneMounted) return;
      if (!scenes[host.getAttribute('data-scene')]) return;   /* not registered yet */
      host.dataset.sceneMounted = '1';
      mount(host);
    });
  }

  /* Both files are deferred, so this one finishes executing before the scene
     definitions do. Mounting only at boot would therefore find an empty
     registry, so registration mounts too — whichever happens last wins. */
  window.SR_SCENE = function (name, factory) {
    scenes[name] = factory;
    if (document.readyState !== 'loading') mountAll(name);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { mountAll(); });
  } else {
    mountAll();
  }
})();
