/* ═══════════════════════════════════════════════════════════════════
   status.js — the one check this page can make honestly.
   ───────────────────────────────────────────────────────────────────
   A status page that only says "all systems operational" in static
   text is a poster, not a status page. This page makes exactly one
   live claim, because exactly one is checkable from a browser:
   GET /api/order answers whether the order intake can store an order
   right now. Everything else on the page is hand-written history,
   and says so.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var KO = (document.documentElement.lang || '').indexOf('ko') === 0;
  var slot = document.querySelector('[data-status-live]');
  var when = document.querySelector('[data-status-when]');
  if (!slot) return;

  function paint(cls, txt) {
    slot.className = 'stbadge ' + cls;
    slot.textContent = txt;
    if (when) when.textContent = (KO ? '방금 이 브라우저에서 확인함 · ' : 'Checked from this browser just now · ') +
      new Date().toLocaleTimeString(KO ? 'ko-KR' : 'en-US');
  }

  fetch('/api/order', { cache: 'no-store' })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (j) {
      if (j && j.ready) {
        paint('ok', KO ? '● 주문 접수 — 정상 작동' : '● Order intake — operational');
      } else if (j) {
        paint('warn', KO ? '● 주문 접수 — 서면 주문으로 전환됨' : '● Order intake — written orders only right now');
      } else {
        paint('warn', KO ? '● 주문 접수 — 응답 없음' : '● Order intake — not responding');
      }
    })
    .catch(function () {
      paint('warn', KO ? '● 주문 접수 — 이 브라우저에서 확인 실패' : '● Order intake — check failed from this browser');
    });
})();
