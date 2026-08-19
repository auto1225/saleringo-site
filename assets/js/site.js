/* SALERINGO site.js v3 — global demos (USD), typing animation,
   timezone-aware default industry, lead capture, booking, staggered reveal */

/* ═══════════════════════════════════════════════════════════════════
   SITE CONFIG — the values that keep the purchase funnel intact.
   ───────────────────────────────────────────────────────────────────
   A buyer audit walked the whole site and scored the purchase path
   2/10: all 26 CTAs ended in a mailto: draft, the lead form captured
   nothing, and a company selling phone answering published no phone
   number anywhere. Two of those three are now closed without any
   external dependency — the phone is the company's real published
   line, and booking terminates on-site at /en/get-started.html, which
   collects preferred times itself.

   Anything still blank degrades honestly rather than breaking: a CTA
   always resolves to a real destination, and the form never claims a
   send it did not observe.
   ═══════════════════════════════════════════════════════════════════ */
window.SR_CONFIG = window.SR_CONFIG || {
  /* No lead endpoint is provisioned yet, so the form falls back to the composer
     and the on-site flow at /en/get-started.html carries the journey instead.
     Drop a Formspree / Netlify / Worker URL in here and the form starts POSTing
     the moment the page reloads - no markup changes needed. */
  formEndpoint: '',
  /* Booking terminates on-site rather than at a third-party scheduler, so the
     journey never leaves the domain and never depends on an account we do not
     control. Set a Cal.com/Calendly URL here to override. */
  bookingUrl:   '',
  bookingPage:  'get-started.html',
  /* The company's real published main line. Never invent a number: a phone
     nobody answers is worse than no phone at all. */
  phone:        '+827052770820',
  phoneLabel:   '+82 70-5277-0820',
  phoneHours:   'Seoul time, UTC+9 - leave a request any time'
};

(function () {
  'use strict';
  var CFG = window.SR_CONFIG;


  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── copy-to-clipboard helper (clipboard API + execCommand fallback) ── */
  function copyText(text, btn) {
    function done(okLabel) {
      if (!btn) return;
      var old = btn.textContent;
      btn.textContent = okLabel;
      setTimeout(function () { btn.textContent = old; }, 1800);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { done('Copied ✓'); }, function () { done('Press Ctrl+C'); });
    } else {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', '');
      ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); done('Copied ✓'); } catch (err) { done('Press Ctrl+C'); }
      document.body.removeChild(ta);
    }
  }

  /* ── booking + phone CTAs, rendered from SR_CONFIG ──
     Elements opt in with data-book / data-tel. If the owner has not filled
     in the config, the element is removed rather than left pointing nowhere:
     an inert "Book a demo" button is worse than no button at all. */
  function wireConfigCTAs() {
    document.querySelectorAll('[data-book]').forEach(function (el) {
      if (CFG.bookingUrl) {
        el.setAttribute('href', CFG.bookingUrl);
        el.setAttribute('target', '_blank');
        el.setAttribute('rel', 'noopener');
      } else {
        /* No external scheduler. The author may have named a destination on the
           element itself — honour that before falling back to the generic flow,
           otherwise data-fallback is markup that lies about what will happen. */
        var fb = el.getAttribute('data-fallback');
        if (fb) {
          el.setAttribute('href', fb);
        } else {
          var depth = /\/en\/industries\//.test(location.pathname) ? '../' : './';
          el.setAttribute('href', depth + (CFG.bookingPage || 'get-started.html'));
        }
      }
    });
    document.querySelectorAll('[data-tel]').forEach(function (el) {
      if (!CFG.phone) { el.remove(); return; }
      el.setAttribute('href', 'tel:' + CFG.phone.replace(/[^\d+]/g, ''));
      var slot = el.querySelector('[data-tel-label]');
      if (slot) slot.textContent = CFG.phoneLabel || CFG.phone;
    });
    document.querySelectorAll('[data-tel-hours]').forEach(function (el) {
      if (!CFG.phoneHours) { el.remove(); return; }
      el.textContent = CFG.phoneHours;
    });
  }
  wireConfigCTAs();

  /* ── say what the button does, before it is pressed ──
     With no formEndpoint provisioned the submit handler does not post: it
     writes the message and hands the visitor four ways to send it. The fine
     print beside all 37 lead forms promised "a person replies within one
     business day" and said nothing about that, so a visitor pressed the
     button believing they had submitted, and only then met a send step. The
     promise is true — the missing fact was who presses send. Stated here at
     runtime rather than in the markup, so the day an endpoint is configured
     every page silently goes back to the direct-submit wording. */
  function tellTheTruthAboutForms() {
    if (CFG.formEndpoint) return;
    var LEAD = 'One tap writes your message and opens it in your mail app, ' +
               'Gmail or Outlook — you press send. ';
    var notes = document.querySelectorAll('.eanote, .sp-fine');
    Array.prototype.forEach.call(notes, function (el) {
      if (el.getAttribute('data-ea-told') !== null) return;
      el.setAttribute('data-ea-told', '');
      var b = document.createElement('b');
      b.className = 'eanote-how';
      b.textContent = LEAD;
      el.insertBefore(b, el.firstChild);
    });
  }
  tellTheTruthAboutForms();

  /* ── lead capture ──
     v2 posted nothing: it fired a mailto: and printed a copy-paste box.
     On mobile webmail that captured close to zero leads. v3 POSTs to a real
     endpoint when one is configured and only falls back to the composer when
     the network call fails or no endpoint exists. We never claim success we
     did not observe — the "sent" state is set from the response, not on submit. */
  function postLead(url, payload) {
    return fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r;
    });
  }

  document.addEventListener('submit', function (e) {
    var form = e.target.closest('[data-earlyaccess]');
    if (!form) return;
    e.preventDefault();
    var get = function (n) { var f = form.querySelector('[name="' + n + '"]'); return f ? f.value : ''; };
    var btn = form.querySelector('button[type="submit"],.eaform button');
    var payload = { pageContext: get('context') || document.title, source: location.pathname };
    /* same rule as the composer: send every field the form actually has */
    Array.prototype.forEach.call(form.elements, function (el) {
      if (!el.name || el.type === 'submit' || el.type === 'button') return;
      if ((el.type === 'checkbox' || el.type === 'radio') && !el.checked) return;
      if (el.type === 'checkbox' || el.type === 'radio') { payload[el.name] = true; return; }
      if (el.value) payload[el.name] = el.value;
    });

    if (CFG.formEndpoint) {
      if (btn) { btn._label = btn.innerHTML; btn.disabled = true; btn.textContent = 'Sending…'; }
      postLead(CFG.formEndpoint, payload).then(function () {
        form.innerHTML = '<div class="easent" role="status">' +
          '<b>Sent — thank you.</b><span>A person reads every one of these. ' +
          'You\'ll get a reply within one business day with a setup plan for your industry attached.</span></div>';
      }).catch(function () {
        if (btn) { btn.disabled = false; btn.innerHTML = btn._label; }
        composeFallback(form, get);
      });
      return;
    }
    composeFallback(form, get);
  });

  /* composer fallback — unchanged behaviour, now only a fallback */
  /* Composer fallback.
     A buyer audit found this was where three qualified buyers — a US dental group,
     a Portuguese hotelier, an Indian clinic chain — reached the end of the funnel
     and were handed an unsent email. mailto: only works for people with a desktop
     mail client configured; on mobile, and for webmail users anywhere, it silently
     does nothing. So we no longer offer one route: we offer the visitor's own,
     including one-click compose links for the two webmail providers that between
     them cover most business users. */
  function composeFallback(form, get) {
    var lines = [
      'Hi Saleringo team,', '',
      'I would like to talk about using Saleringo for my business.', ''
    ];
    /* Read every named field the form actually has, rather than a fixed list.
       Industry forms add their own — locations, rooms, sites, trade, plan —
       and those are exactly the answers that decide the buyer's plan and price. */
    var LABEL = {
      email:'Work email', business:'Business', industry:'Industry', country:'Country',
      website:'Website / price list', channel:'Main channel', locations:'Locations',
      rooms:'Rooms', sites:'Sites', trade:'Trade', plan:'Plan viewed', note:'Notes'
    };
    var slots = [];
    Array.prototype.forEach.call(form.elements, function (el) {
      if (!el.name || el.name === 'context' || el.type === 'submit' || el.type === 'button') return;
      if (el.type === 'checkbox' || el.type === 'radio') {
        if (!el.checked) return;
        var lab = el.closest('label');
        var txt = lab ? lab.textContent.trim() : el.name.replace(/^slot_/, '');
        if (el.name.indexOf('slot_') === 0) { slots.push(txt); return; }
        lines.push((LABEL[el.name] || el.name.replace(/_/g, ' ')) + ': ' + txt);
        return;
      }
      var v = (el.value || '').trim();
      if (!v) return;
      lines.push((LABEL[el.name] || el.name.replace(/_/g, ' ')) + ': ' + v);
    });
    if (slots.length) lines.push('Best time to talk: ' + slots.join(', '));
    lines.push('', 'Sent from ' + location.hostname + location.pathname);
    var body = lines.join('\n');
    var subj = 'Saleringo — ' + (get('business') || get('email') || 'enquiry');
    var TO = 'hello@saleringo.com';
    var eb = encodeURIComponent(body), es = encodeURIComponent(subj);

    var fb = form.querySelector('[data-ea-fallback]');
    if (!fb) {
      fb = document.createElement('div');
      fb.className = 'eafallback full';
      fb.setAttribute('data-ea-fallback', '');
      fb.innerHTML =
        '<p class="eafallback-lead">Your message is written. Send it whichever way suits you — ' +
        'all three go to the same person.</p>' +
        '<div class="eafallback-routes">' +
          '<a class="btn btn-teal" data-r="mail" href="#">Open my mail app<span class="cir">↗</span></a>' +
          '<a class="btn btn-ghostd" data-r="gmail" target="_blank" rel="noopener" href="#">Gmail<span class="cir">↗</span></a>' +
          '<a class="btn btn-ghostd" data-r="outlook" target="_blank" rel="noopener" href="#">Outlook<span class="cir">↗</span></a>' +
        '</div>' +
        '<textarea class="eafallback-text" readonly rows="9" aria-label="Your message"></textarea>' +
        '<div class="eafallback-row">' +
          '<button type="button" class="eafallback-copy">Copy it instead</button>' +
          '<span class="eafallback-addr">and send to <b>' + TO + '</b></span>' +
        '</div>';
      form.appendChild(fb);
      fb.querySelector('.eafallback-copy').addEventListener('click', function () {
        copyText(fb.querySelector('.eafallback-text').value, this);
      });
    }
    fb.querySelector('[data-r="mail"]').href = 'mailto:' + TO + '?subject=' + es + '&body=' + eb;
    fb.querySelector('[data-r="gmail"]').href =
      'https://mail.google.com/mail/?view=cm&fs=1&to=' + TO + '&su=' + es + '&body=' + eb;
    fb.querySelector('[data-r="outlook"]').href =
      'https://outlook.office.com/mail/deeplink/compose?to=' + TO + '&subject=' + es + '&body=' + eb;
    fb.querySelector('.eafallback-text').value = 'To: ' + TO + '\nSubject: ' + subj + '\n\n' + body;
    fb.hidden = false;
    var ok = form.querySelector('[data-ea-done]');
    if (ok) ok.hidden = false;
    fb.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  /* ── mailto CTA fallback — a small notice for visitors without a mail app ── */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="mailto:"]');
    if (!a) return;
    var toast = document.querySelector('.mailtonote');
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'mailtonote';
      toast.setAttribute('role', 'status');
      var txt = document.createElement('span');
      txt.innerHTML = 'No email app opened? Write to <b>hello@saleringo.com</b>';
      var cp = document.createElement('button');
      cp.type = 'button';
      cp.textContent = 'Copy address';
      cp.addEventListener('click', function () { copyText('hello@saleringo.com', cp); });
      toast.appendChild(txt); toast.appendChild(cp);
      document.body.appendChild(toast);
    }
    toast.classList.add('show');
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { toast.classList.remove('show'); }, 9000);
  });

  /* ── scroll reveal (progressive enhancement + failsafe) ── */
  if (!reduce && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('srjs');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        /* stagger siblings so a grid composes itself instead of arriving
           all at once — the design audit called the single 0.9s fade the
           flattest possible motion for a 20-page site */
        var p = en.target.parentElement;
        if (p) {
          var sibs = [].slice.call(p.children).filter(function (c) {
            return c.classList && c.classList.contains('reveal');
          });
          var i = sibs.indexOf(en.target);
          if (i > 0) en.target.style.setProperty('--i', Math.min(i, 7));
        }
        en.target.classList.add('vis');
        io.unobserve(en.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -5% 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
    setTimeout(function () {
      document.querySelectorAll('.reveal:not(.vis)').forEach(function (el) { el.classList.add('vis'); });
    }, 1600);
  }

  /* ── mobile nav ── */
  var burger = document.querySelector('.nav .burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var links = document.querySelector('.nav .links');
      if (links) links.classList.toggle('open');
    });
  }

  /* ── sticky conversion bar — shared, IntersectionObserver only.
        DEV_SPEC 5.4 forbids window scroll listeners outright, so the bar is
        driven purely by two observers:
          • #cta-gate   — the point after which the offer is worth repeating
                          (falls back to the 2nd <main> section if absent)
          • #early-access / .closer — where the bar would compete with the
                          real CTA, so it steps aside
        Any page that ships a .stickycta element gets this for free. ── */
  (function () {
    var bar = document.querySelector('.stickycta');
    if (!bar || !('IntersectionObserver' in window)) return;

    var gate = document.getElementById('cta-gate') ||
               document.querySelectorAll('main > section')[1] || null;
    var quiet = [].slice.call(document.querySelectorAll('#early-access, .closer'));
    var past = false, atEnd = false;

    function sync() { bar.classList.toggle('show', past && !atEnd); }

    if (gate) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          past = e.isIntersecting || e.boundingClientRect.top < 0;
        });
        sync();
      }, { threshold: 0 }).observe(gate);
    }
    if (quiet.length) {
      var qo = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          e.target.setAttribute('data-inview', e.isIntersecting ? '1' : '0');
        });
        atEnd = quiet.some(function (el) { return el.getAttribute('data-inview') === '1'; });
        sync();
      }, { threshold: 0 });
      quiet.forEach(function (el) { qo.observe(el); });
    }
  })();


  /* ── back to top ──
     These pages run to 27,000px. Once a reader is three screens down there is
     no way back but a long drag, so the button appears then and not before —
     showing it at the top would just be furniture.

     DEV_SPEC 5.4 forbids window scroll listeners, so a 1px sentinel pinned two
     viewports down does the deciding: while it is still ahead of you the page
     is short enough to scroll by hand, and once you pass it the button arrives.
     The markup is injected rather than repeated across 26 files — it is chrome,
     it carries no content, and one definition cannot drift out of sync. ── */
  (function () {
    if (!('IntersectionObserver' in window)) return;
    if (document.querySelector('.totop')) return;

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'totop';
    btn.setAttribute('aria-label', 'Back to top');
    btn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
                    '<path d="M12 19V6M12 6l-6 6M12 6l6 6" fill="none" stroke="currentColor" ' +
                    'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

    var mark = document.createElement('span');
    mark.className = 'totop-mark';
    mark.setAttribute('aria-hidden', 'true');

    document.body.appendChild(mark);
    document.body.appendChild(btn);

    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        /* past the mark means it has left the top of the viewport */
        btn.classList.toggle('show', !e.isIntersecting && e.boundingClientRect.top < 0);
      });
    }, { threshold: 0 }).observe(mark);

    btn.addEventListener('click', function () {
      var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      /* Send focus somewhere sensible, or a keyboard user is left stranded at
         the bottom of the document with the page visually at the top. */
      var first = document.querySelector('a, button, [tabindex]:not([tabindex="-1"])');
      if (first) first.focus({ preventScroll: true });
    });
  })();

})();
