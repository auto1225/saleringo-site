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
  /* /api/lead is this site's own endpoint (api/lead.js). It answers GET with
     whether it has anywhere to put a lead, so a page can tell the truth before
     the visitor presses anything, and it answers POST with a reference number
     the visitor can quote. With no destination configured it returns 503 and
     the composer fallback below takes over - the same behaviour the site had
     when this was an empty string, and never a silent loss. Point it at
     Formspree or a Worker instead and nothing else has to change. */
  formEndpoint: '/api/lead',
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



/* ── the sentences this file writes at runtime ────────────────────────
   Everything the chrome says was moved into build/strings/<lang>.json and is
   rendered at build time. These are the sentences the *script* writes - the
   receipt after a form is sent, the fallback that appears when there is no
   endpoint, the notice when a mailto goes nowhere - and every one of them was
   in English on every page, including the Korean ones. A Korean owner filling
   in a Korean form was answered in English at the one moment that decides
   whether they trust the thing.

   So they live here, once, keyed by language, and T() picks by the page's own
   <html lang>. Adding a sentence means adding it in both columns, which is
   the point: a missing translation is visible in this file rather than
   invisible on the page.                                                   */
  var LANG = (document.documentElement.lang || 'en').slice(0, 2);
  var STR = {
    en: {
      hours: 'Seoul time, UTC+9 - leave a request any time',
      how: 'One tap writes your message and opens it in your mail app, ' +
           'Gmail or Outlook \u2014 you press send. ',
      sending: 'Sending\u2026',
      gotIt: 'Received. We have it \u2014 there is nothing left for you to send.',
      copySent: 'A copy is in your inbox now. If it is not there within a minute, look in spam. ',
      replyBy: 'A person reads every one of these. You will hear back by ',
      withPlan: ' with a setup plan for your trade attached',
      andRef: ', and quoting the reference above finds you straight away.',
      fullStop: '.',
      fbLead: 'Your message is written. Send it whichever way suits you \u2014 ' +
              'all three go to the same person.',
      fbMail: 'Open my mail app',
      fbCopy: 'Copy it instead',
      fbAnd: 'and send to ',
      fbLabel: 'Your message',
      greeting: 'Hi Saleringo team,',
      intro: 'I would like to talk about using Saleringo for my business.',
      bestTime: 'Best time to talk: ',
      sentFrom: 'Sent from ',
      subject: 'Saleringo \u2014 ',
      enquiry: 'enquiry',
      noMail: 'No email app opened? Write to <b>hello@saleringo.com</b>',
      copyAddr: 'Copy address',
      labels: { email: 'Work email', business: 'Business', industry: 'Industry',
                country: 'Country', website: 'Website / price list', phone: 'Phone',
                channel: 'Main channel', locations: 'Locations', rooms: 'Rooms',
                sites: 'Sites', trade: 'Trade', plan: 'Plan viewed', note: 'Notes' },
      dateLocale: 'en-GB'
    },
    ko: {
      hours: '한국 시간 기준 · 언제든 남겨 주시면 됩니다',
      how: '누르시면 메일 내용이 작성된 채로 메일 앱이나 Gmail이 열립니다. ' +
           '보내기만 누르시면 됩니다. ',
      sending: '보내는 중\u2026',
      gotIt: '접수되었습니다. 더 보내실 것은 없습니다.',
      copySent: '보내신 내용의 사본을 이메일로 보내 드렸습니다. 1분 안에 오지 않으면 스팸함을 확인해 주십시오. ',
      replyBy: '사람이 직접 읽고 답장드립니다. ',
      withPlan: '까지 우리 매장에 맞춘 응대 안을 함께 보내 드리겠습니다',
      andRef: '. 위 접수번호를 말씀하시면 바로 찾을 수 있습니다.',
      fullStop: '.',
      fbLead: '메일 내용이 작성되었습니다. 편하신 방법으로 보내 주십시오. ' +
              '세 가지 모두 같은 사람에게 갑니다.',
      fbMail: '메일 앱으로 열기',
      fbCopy: '복사하기',
      fbAnd: '보낼 곳 ',
      fbLabel: '작성된 메일 내용',
      greeting: 'Saleringo 담당자님께,',
      intro: 'Saleringo 도입에 대해 상담받고 싶습니다.',
      bestTime: '통화 가능한 시간: ',
      sentFrom: '보낸 페이지: ',
      subject: 'Saleringo 도입 문의 \u2014 ',
      enquiry: '문의',
      noMail: '메일 앱이 열리지 않으면 <b>hello@saleringo.com</b> 으로 보내 주십시오',
      copyAddr: '주소 복사',
      labels: { email: '이메일', business: '상호', industry: '업종',
                country: '국가', website: '홈페이지 / 요금표', phone: '연락처',
                channel: '주요 문의 경로', locations: '지점 수', rooms: '객실 수',
                sites: '사이트 수', trade: '업종', plan: '본 요금제', note: '추가 내용' },
      dateLocale: 'ko-KR'
    }
  };
  function T(k) {
    var t = STR[LANG] || STR.en;
    return (k in t) ? t[k] : STR.en[k];
  }


  /* ── the language you chose, remembered ───────────────────────
     The site guesses a language from the browser at the root, which is right
     for a first visit and wrong for every visit after someone has told us
     otherwise. A Korean reader who deliberately switches to English, or an
     English-speaking owner in Seoul whose browser reports ko, should not have
     to make the same choice twice.

     So the switch writes the choice down, and the root reads it before it
     guesses. Nothing else reads it, and clearing site data forgets it. */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a.langsw');
    if (!a) return;
    try { localStorage.setItem('sr-lang', a.getAttribute('hreflang') || ''); } catch (err) {}
  });

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
      el.textContent = T('hours') || CFG.phoneHours;
    });
  }
  wireConfigCTAs();

  /* ── reserve the sticky bar's height ──
     It is fixed, so the document does not account for it, and once the guide
     docks into it the bar is 165px tall on a phone. Measured and published as
     --stickycta-h; the stylesheet pads the body by it so the footer clears,
     and the hero adds it to its own bottom padding so the buttons are not
     underneath the bar at first paint. */
  function stickyctaHeight() {
    var bar = document.querySelector('.stickycta');
    var h = 0;
    if (bar) {
      var r = bar.getBoundingClientRect();
      /* the bar slides out of view rather than unmounting, so a bar that is
         translated past the bottom edge reserves nothing and the back-to-top
         button should sit at its normal height */
      h = r.top < window.innerHeight ? Math.round(r.height) : 0;
    }
    document.documentElement.style.setProperty('--stickycta-h', h + 'px');
  }
  stickyctaHeight();

  /* -- give the phone its screen back --
     The docked bar is one row and about 64px, which is little on a laptop and
     a lot on a 812px phone held in one hand. It behaves the way a good app bar
     behaves: reading downward tucks it away, the first upward gesture brings
     it back, and it is always there at the end of the page where the decision
     gets made. Only below 720px - on a desktop it never moves. */
  (function () {
    var bar = document.querySelector('.stickycta');
    if (!bar) return;
    var narrow = window.matchMedia('(max-width:720px)');
    var last = window.pageYOffset, tick = false;
    function onScroll() {
      if (tick) return;
      tick = true;
      requestAnimationFrame(function () {
        tick = false;
        var y = window.pageYOffset;
        var dy = y - last;
        if (Math.abs(dy) < 8) return;
        last = y;
        if (!narrow.matches) { bar.classList.remove('tuck'); return; }
        var atEnd = (window.innerHeight + y) >= (document.body.scrollHeight - 240);
        bar.classList.toggle('tuck', dy > 0 && y > 400 && !atEnd);
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    narrow.addEventListener('change', function () { bar.classList.remove('tuck'); });
  })();

  if (window.ResizeObserver) {
    var bar = document.querySelector('.stickycta');
    if (bar) new ResizeObserver(stickyctaHeight).observe(bar);
  }
  window.addEventListener('resize', stickyctaHeight);
  /* the guide rail is inserted after this file runs */
  setTimeout(stickyctaHeight, 0);
  setTimeout(stickyctaHeight, 400);
  var _bar = document.querySelector('.stickycta');
  if (_bar) _bar.addEventListener('transitionend', stickyctaHeight);
  if (window.MutationObserver && _bar) {
    new MutationObserver(stickyctaHeight)
      .observe(_bar, { attributes: true, attributeFilter: ['class'] });
  }

  /* -- a field no person can see and no person fills in --
     Added at runtime rather than in 34 pieces of markup: the form only submits
     with script running anyway, so a bot that never runs script gains nothing
     by ignoring it, and one that does fills it in and is answered with a
     reference that goes nowhere. */
  (function () {
    var forms = document.querySelectorAll('form[data-earlyaccess]'), i;
    for (i = 0; i < forms.length; i++) {
      if (forms[i].querySelector('[name="company_website_hp"]')) continue;
      var w = document.createElement('div');
      w.setAttribute('aria-hidden', 'true');
      w.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden';
      w.innerHTML = '<label>Company website<input type="text" name="company_website_hp" ' +
                    'tabindex="-1" autocomplete="off"></label>';
      forms[i].appendChild(w);
    }
  })();


  /* -- does the form have anywhere to send it? --
     An endpoint that exists is not the same as an endpoint wired to a
     destination. The page asks once: /api/lead answers GET with {ready}, and
     the answer decides which of two true things the fine print says - "we take
     it from here", or "you press send". A page that cannot reach the endpoint
     at all assumes the worse of the two. */
  var SR_READY = null;
  if (CFG.formEndpoint && CFG.formEndpoint.charAt(0) === '/' &&
      document.querySelector('form[data-earlyaccess]')) {
    fetch(CFG.formEndpoint, { method: 'GET', headers: { Accept: 'application/json' } })
      .then(function (r) { return r.ok ? r.json() : { ready: false }; })
      .then(function (j) { SR_READY = !!j.ready; if (!SR_READY) tellTheTruthAboutForms(); })
      .catch(function () { SR_READY = false; tellTheTruthAboutForms(); });
  }

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
    if (CFG.formEndpoint && SR_READY !== false) return;
    var LEAD = T('how');
    /* Only the fine print that sits under a lead form's own submit button.
       The first version matched every .eanote and .sp-fine on the page, which
       put the sentence in three wrong places: the post-submit success message,
       where it told someone who had already sent it how to send it; a .leadbox
       note that has nothing to do with the form, where it shoved the "Verified
       answers only" badge out of line; and the tour step, where the button it
       describes is still a screen away. */
    var forms = document.querySelectorAll('form[data-earlyaccess]');
    Array.prototype.forEach.call(forms, function (form) {
      var el = form.querySelector('.eanote:not([hidden]):not([data-ea-done])');
      if (!el || el.getAttribute('data-ea-told') !== null) return;
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
      if (btn) { btn._label = btn.innerHTML; btn.disabled = true; btn.textContent = T('sending'); }
      postLead(CFG.formEndpoint, payload).then(function (r) {
        return r.json().catch(function () { return {}; });
      }).then(function (j) {
        showReceipt(form, j);
      }).catch(function () {
        if (btn) { btn.disabled = false; btn.innerHTML = btn._label; }
        composeFallback(form, get);
      });
      return;
    }
    composeFallback(form, get);
  });

  /* -- the receipt --
     A form that vanishes into a thank-you leaves the visitor holding nothing.
     The endpoint returns a reference; the page shows it, says whether a copy is
     already in their inbox, and gives a date for the reply rather than a mood.
     The confirmation line is printed only when the server reports it actually
     sent one - the same rule as the send itself. */
  function showReceipt(form, j) {
    var reference = (j && j.reference) || '';
    var confirmed = !!(j && j.confirmation);
    var next = new Date();
    next.setDate(next.getDate() + (next.getDay() === 5 ? 3 : next.getDay() === 6 ? 2 : 1));
    /* the page is in English; the reader's device locale is not the page's */
    var by = next.toLocaleDateString(T('dateLocale'),
                                     { weekday: 'long', day: 'numeric', month: 'long' });
    form.innerHTML =
      '<div class="easent" role="status" tabindex="-1">' +
        '<b>' + T('gotIt') + '</b>' +
        (reference ? '<code class="earef">' + reference + '</code>' : '') +
        '<span>' +
          (confirmed
            ? T('copySent')
            : '') +
          T('replyBy') + '<b>' + by + '</b>' + T('withPlan') +
          (reference ? T('andRef') : T('fullStop')) +
        '</span>' +
      '</div>';
    var box = form.querySelector('.easent');
    if (box) { box.focus(); box.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
  }

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
      T('greeting'), '',
      T('intro'), ''
    ];
    /* Read every named field the form actually has, rather than a fixed list.
       Industry forms add their own — locations, rooms, sites, trade, plan —
       and those are exactly the answers that decide the buyer's plan and price. */
    var LABEL = T('labels');
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
    if (slots.length) lines.push(T('bestTime') + slots.join(', '));
    lines.push('', T('sentFrom') + location.hostname + location.pathname);
    var body = lines.join('\n');
    var subj = T('subject') + (get('business') || get('email') || T('enquiry'));
    var TO = 'hello@saleringo.com';
    var eb = encodeURIComponent(body), es = encodeURIComponent(subj);

    var fb = form.querySelector('[data-ea-fallback]');
    if (!fb) {
      fb = document.createElement('div');
      fb.className = 'eafallback full';
      fb.setAttribute('data-ea-fallback', '');
      fb.innerHTML =
        '<p class="eafallback-lead">' + T('fbLead') + '</p>' +
        '<div class="eafallback-routes">' +
          '<a class="btn btn-teal" data-r="mail" href="#">' + T('fbMail') + '<span class="cir">↗</span></a>' +
          '<a class="btn btn-ghostd" data-r="gmail" target="_blank" rel="noopener" href="#">Gmail<span class="cir">↗</span></a>' +
          '<a class="btn btn-ghostd" data-r="outlook" target="_blank" rel="noopener" href="#">Outlook<span class="cir">↗</span></a>' +
        '</div>' +
        '<textarea class="eafallback-text" readonly rows="9" aria-label="' + T('fbLabel') + '"></textarea>' +
        '<div class="eafallback-row">' +
          '<button type="button" class="eafallback-copy">' + T('fbCopy') + '</button>' +
          '<span class="eafallback-addr">' + T('fbAnd') + '<b>' + TO + '</b></span>' +
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
      txt.innerHTML = T('noMail');
      var cp = document.createElement('button');
      cp.type = 'button';
      cp.textContent = T('copyAddr');
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

  /* ── the watchdog: on screen and still unreadable ──
     Where the browser supports scroll-driven animation the reveal stops being
     this observer's job and becomes a function of scroll position - and an
     animation whose first frame is opacity 0 holds that frame until its range
     is reached. A block taller than the viewport can fail to reach it. On a
     desktop almost nothing is taller than the viewport; on a phone a great
     many blocks are, and each one stayed invisible with its space reserved.

     The ranges are fixed in CSS. This is the belt: anything actually on screen
     that still cannot be read after a moment is shown. It only ever fires for
     a block the reader is looking at, so it cannot flatten the effect for the
     rest of the page. */
  if ('IntersectionObserver' in window) {
    var watch = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        setTimeout(function () {
          if (!el.isConnected) return;
          var r = el.getBoundingClientRect();
          if (r.bottom < 0 || r.top > window.innerHeight) return;
          if (parseFloat(getComputedStyle(el).opacity) > 0.05) return;
          el.classList.add('sr-force');
        }, 420);
      });
    }, { threshold: 0 });
    document.querySelectorAll('.reveal').forEach(function (el) { watch.observe(el); });
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
          /* Past the gate means past it — not merely level with it.
             `isIntersecting` turns true the moment the gate scrolls INTO
             view, which on the home page is before the reader has left the
             hero: the bar arrived at scroll 0 and stood underneath the two
             hero buttons, making five calls to action visible at once on
             the screen that decides the sale. The gate's top being above
             the fold is the honest test. */
          past = e.boundingClientRect.top < 0;
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
