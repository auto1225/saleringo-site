/* ── four arguments, one screen ────────────────────────────────────────────
   The home page made the same case four times in a row: the work that follows
   a call, what the conversation leaves behind, one inbox, and the screen you
   open in the morning. Four full-height sections, 6,668px, four uppercase
   kickers, and a reader who by the third one has stopped asking what to press.

   They are the same beat, so they sit in one section and the reader chooses.
   The panel that is showing is a real tab panel: arrow keys move between tabs,
   the selected one is announced, and every deep link that used to land on one
   of those sections still lands on it — a hash, an in-page link, or the guided
   tour asking for an element inside a panel opens that panel first.

   With script off, every panel is visible and stacked, which is the page as it
   was. Nothing is hidden behind JavaScript that the reader needs.            */
(function () {
  'use strict';

  var sets = document.querySelectorAll('.panelset');
  if (!sets.length) return;
  /* the tab strip is hidden until script is present, and this file is the
     script that drives it - so it claims the hook itself rather than waiting
     for another file to set it */
  document.documentElement.classList.add('srjs');

  function panelsOf(set) {
    return [].slice.call(set.querySelectorAll(':scope > .pspanel'));
  }

  function select(set, panel, focusTab) {
    var panels = panelsOf(set);
    var tabs = [].slice.call(set.querySelectorAll(':scope > .pstabs > button'));
    panels.forEach(function (p, i) {
      var on = p === panel;
      p.hidden = !on;
      p.classList.toggle('on', on);
      if (tabs[i]) {
        tabs[i].setAttribute('aria-selected', on ? 'true' : 'false');
        tabs[i].tabIndex = on ? 0 : -1;
        tabs[i].classList.toggle('on', on);
      }
    });
    if (focusTab) {
      var t = tabs[panels.indexOf(panel)];
      if (t) t.focus();
    }
    /* a canvas or a mock that was hidden has just been given a width */
    window.dispatchEvent(new Event('resize'));
  }

  sets.forEach(function (set) {
    var panels = panelsOf(set);
    if (panels.length < 2) return;
    var strip = set.querySelector(':scope > .pstabs');
    if (!strip) return;
    var tabs = [].slice.call(strip.querySelectorAll('button'));

    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(set, panels[i], false); });
      t.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        select(set, panels[(i + d + panels.length) % panels.length], true);
      });
    });
    select(set, panels[0], false);
  });

  /* ── a link into a panel opens the panel ──
     Everything else on the site assumes a section is always in the document:
     the guided tour scrolls to it, the footer links to it, another page links
     to index.html#what-it-keeps. All of those keep working because the panel
     is opened before the browser is asked to go there. */
  function reveal(node) {
    if (!node || !node.closest) return false;
    var panel = node.closest('.pspanel');
    if (!panel) return false;
    var set = panel.parentElement;
    if (!set || !set.classList.contains('panelset')) return false;
    if (!panel.hidden) return true;
    select(set, panel, false);
    return true;
  }
  window.SR = window.SR || {};
  window.SR.revealPanelFor = reveal;

  function fromHash() {
    var h = location.hash.slice(1);
    if (!h) return;
    var el = document.getElementById(h);
    if (reveal(el)) {
      /* the panel was hidden when the browser tried to scroll to it */
      setTimeout(function () { el.scrollIntoView({ block: 'start' }); }, 0);
    }
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href*="#"]');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    var i = href.indexOf('#');
    if (i < 0) return;
    var id = href.slice(i + 1);
    if (!id) return;
    /* only same-page links */
    if (i > 0 && href.slice(0, i).replace(/^\.\//, '') &&
        href.slice(0, i).indexOf(location.pathname.split('/').pop()) < 0) return;
    reveal(document.getElementById(id));
  }, true);

  window.addEventListener('hashchange', fromHash);
  fromHash();
})();


/* ── twenty-five trades is depth, but a wall of twenty-five reads as breadth ──
   Every trade on the site has its own price rules, its own gates and its own
   refusals - that is the product. Printing all twenty-five as one wall of
   chips says the opposite: that the list is the product, and that it is a
   mile wide. So the wall opens on the ten a visitor is most likely to be, and
   the rest are one press away. The selected trade is always visible, whichever
   row it came from, and choosing from the full list keeps it visible after. */
(function () {
  'use strict';
  var SHOWN = 10;
  var walls = document.querySelectorAll('.chiprow[role="tablist"]');
  [].forEach.call(walls, function (wall) {
    var chips = [].slice.call(wall.querySelectorAll(':scope > .chip'));
    if (chips.length <= SHOWN + 2) return;

    var more = document.createElement('button');
    more.type = 'button';
    more.className = 'chip chipmore';
    more.setAttribute('aria-expanded', 'false');
    var rest = chips.length - SHOWN;
    more.textContent = rest + ' more trades';
    wall.appendChild(more);

    function fold(hide) {
      chips.forEach(function (c, i) {
        if (i < SHOWN) return;
        var keep = !hide || c.getAttribute('aria-selected') === 'true';
        c.hidden = !keep;
      });
      more.setAttribute('aria-expanded', hide ? 'false' : 'true');
      more.textContent = hide ? rest + ' more trades' : 'Show fewer';
      window.dispatchEvent(new Event('resize'));
    }

    more.addEventListener('click', function () {
      fold(more.getAttribute('aria-expanded') === 'true');
    });
    /* a trade chosen from the long list stays on screen afterwards */
    wall.addEventListener('click', function (e) {
      var c = e.target.closest('.chip');
      if (!c || c === more) return;
      setTimeout(function () {
        chips.forEach(function (x, i) {
          if (i >= SHOWN && x.getAttribute('aria-selected') === 'true') x.hidden = false;
        });
      }, 0);
    });
    fold(true);
  });
})();
