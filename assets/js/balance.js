/* ── a wall of chips picks the column count that divides it ────────────────
   `repeat(auto-fit, minmax(156px, 1fr))` answers one question: how many
   columns fit? It never asks the second one: how many divide the items
   evenly. Measured at 1440 — sixteen chips took five columns and rendered
   5,5,5,1, so the sixteenth sat alone under four full rows. Ten took three
   and rendered 3,3,3,1. Nine took three twice and left one.

   So the count is computed rather than inferred. Start at the most columns
   that fit at the wall's minimum chip width, then step down while the last
   row would hold less than half a full row. Four columns for sixteen, two
   for ten, three for nine — every wall ends flush or close to it.

   ResizeObserver, not a resize listener: it fires for the element, not for
   every pixel of the window, and it also catches the wall changing width
   without the window changing at all.                                    */
(function () {
  'use strict';
  var WALLS = '.langrow,.intwall,.kwrow,.chiprow,.exfilter,.langbig,' +
              '.tradewords,.tradetour,.smanch,.np-in,.bigfooter .ftgrid,' +
              /* card grids holding running text, not chips */
              '.tline,.cases,.whogrid,.stackrow,.tourcards,.funflow,' +
              '.gatesteps,.specstrip,.chanlinks,.approvedby';

  function minWidth(el) {
    var v = parseFloat(getComputedStyle(el).getPropertyValue('--chip-min'));
    return v > 0 ? v : 156;
  }

  function balance(el) {
    var kids = 0, i, c = el.children, cs;
    for (i = 0; i < c.length; i++) {
      cs = getComputedStyle(c[i]);
      if (cs.display === 'none') continue;
      /* A child told to span the row is a band, not one of the items being
         divided — counting the nav panel's footer link row as a sixth column
         is what made five groups render as four. */
      if (cs.gridColumn && cs.gridColumn.indexOf('-1') >= 0) continue;
      if (cs.gridColumnStart === '1' && cs.gridColumnEnd === '-1') continue;
      kids++;
    }
    if (!kids) return;

    var gap = parseFloat(getComputedStyle(el).columnGap) || 0;
    var w = el.clientWidth;
    /* A menu panel is hidden until it opens, and it opens with a transition.
       Measured mid-transition it reported 800-odd pixels of its eventual 1003
       and settled on four columns for five groups. Zero or a width still in
       motion is not an answer — the ResizeObserver fires again when it stops,
       and that reading is the one that counts. */
    if (w < 40) return;
    var min = minWidth(el);
    /* the most that fit: n columns need n*min + (n-1)*gap */
    var fit = Math.max(1, Math.floor((w + gap) / (min + gap)));
    var n = Math.min(fit, kids);

    /* step down while the tail row is a stub */
    while (n > 1) {
      var tail = kids % n;
      if (tail === 0 || tail * 2 >= n) break;
      n--;
    }
    el.style.setProperty('--cols', n);
  }

  function run() {
    var walls = document.querySelectorAll(WALLS), i;
    for (i = 0; i < walls.length; i++) balance(walls[i]);
  }

  function start() {
    run();
    if (!window.ResizeObserver) return;
    var ro = new ResizeObserver(function (entries) {
      for (var i = 0; i < entries.length; i++) balance(entries[i].target);
    });
    var walls = document.querySelectorAll(WALLS), j;
    for (j = 0; j < walls.length; j++) ro.observe(walls[j]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else { start(); }
  /* a web font landing changes chip widths, so measure again once it has */
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(run);
})();
