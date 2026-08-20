/* ── the lead form's other half ───────────────────────────────────────────
   Everything in front of this file was already right: the form validates, the
   client only claims a send it observed, and it degrades to a mail composer
   when the network fails. What was missing was somewhere for a lead to land.
   SR_CONFIG.formEndpoint was '', so every completed form ended in the
   visitor's own mail app with the send button still unpressed.

   This is the sink. It takes the POST, gives the lead a reference the visitor
   can quote, writes it to whichever destination the owner has configured, and
   only then reports success. If nothing is configured it says so plainly with
   a 503 and the client falls back to the composer — the same behaviour as
   before, never a silent loss.

   Configure ONE of these in the Vercel project's environment variables:

     LEAD_WEBHOOK_URL   any endpoint that accepts JSON — Zapier, Make, a Google
                        Apps Script bound to a Sheet, an n8n hook, your own API
     SLACK_WEBHOOK_URL  an incoming webhook; the lead arrives as a message
     RESEND_API_KEY     + LEAD_TO_EMAIL and LEAD_FROM_EMAIL — mails the team and
                        sends the applicant a confirmation with the reference

   Set several and every one of them gets the lead; the response reports which
   ones actually accepted it. Saving an environment variable in Vercel is
   enough — the site itself does not change.                                */

const FIELD_LIMIT = 4000;
const RATE = new Map();               /* per-instance; a speed bump, not a wall */

function ref() {
  const d = new Date();
  const day = d.toISOString().slice(0, 10).replace(/-/g, '');
  let tail = '';
  for (let i = 0; i < 4; i++) tail += '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'[Math.floor(Math.random() * 32)];
  return 'SR-' + day + '-' + tail;
}

/* strip control characters so a header or a log line cannot be forged */
const CTRL = new RegExp('[\\u0000-\\u001f\\u007f]', 'g');
function clean(v) {
  return String(v == null ? '' : v).replace(CTRL, ' ').slice(0, FIELD_LIMIT).trim();
}

function configured() {
  return {
    webhook: !!process.env.LEAD_WEBHOOK_URL,
    slack:   !!process.env.SLACK_WEBHOOK_URL,
    email:   !!(process.env.RESEND_API_KEY && process.env.LEAD_TO_EMAIL && process.env.LEAD_FROM_EMAIL)
  };
}

function limited(ip) {
  const now = Date.now();
  const hits = (RATE.get(ip) || []).filter(t => now - t < 60000);
  hits.push(now);
  RATE.set(ip, hits);
  if (RATE.size > 500) RATE.clear();
  return hits.length > 6;
}

async function post(url, body, headers) {
  const r = await fetch(url, {
    method: 'POST',
    headers: Object.assign({ 'Content-Type': 'application/json' }, headers || {}),
    body: JSON.stringify(body)
  });
  if (!r.ok) throw new Error('HTTP ' + r.status);
  return true;
}

function lines(lead) {
  return Object.keys(lead)
    .filter(k => k !== 'context' && lead[k] !== '' && lead[k] != null)
    .map(k => k.replace(/_/g, ' ') + ': ' + lead[k]);
}

async function sendEmail(to, subject, text, replyTo) {
  return post('https://api.resend.com/emails', {
    from: process.env.LEAD_FROM_EMAIL,
    to: [to],
    subject: subject,
    text: text,
    reply_to: replyTo || undefined
  }, { Authorization: 'Bearer ' + process.env.RESEND_API_KEY });
}

export default async function handler(req, res) {
  const cfg = configured();
  const ready = cfg.webhook || cfg.slack || cfg.email;

  /* The client asks before it promises anything: with no sink configured the
     form keeps telling the visitor that they are the one who presses send. */
  if (req.method === 'GET') {
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({ ready: ready, confirmation: cfg.email });
  }

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ error: 'method_not_allowed' });
  }

  /* Never pretend. The client turns this into the mail-composer route. */
  if (!ready) return res.status(503).json({ error: 'no_destination_configured' });

  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  if (limited(ip)) return res.status(429).json({ error: 'too_many' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = null; } }
  if (!body || typeof body !== 'object') return res.status(400).json({ error: 'bad_request' });

  /* a field no human ever fills in */
  if (clean(body.company_website_hp)) return res.status(200).json({ ok: true, reference: ref() });

  const email = clean(body.email);
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email)) return res.status(400).json({ error: 'email_invalid' });

  const lead = {};
  Object.keys(body).forEach(function (k) {
    if (k === 'company_website_hp') return;
    if (!/^[a-zA-Z0-9_]{1,40}$/.test(k)) return;
    const v = clean(body[k]);
    if (v) lead[k] = v;
  });

  const reference = ref();
  const received = new Date().toISOString();
  const record = Object.assign({ reference: reference, received: received, ip: ip }, lead);
  const bodyText = 'Reference: ' + reference + '\nReceived: ' + received + '\n\n' + lines(record).join('\n');

  const done = [], failed = [], tries = [];

  if (cfg.webhook) tries.push(['webhook', function () { return post(process.env.LEAD_WEBHOOK_URL, record); }]);
  if (cfg.slack) tries.push(['slack', function () {
    return post(process.env.SLACK_WEBHOOK_URL, {
      text: '*New Saleringo lead* ' + reference + '\n```' + lines(record).join('\n') + '```'
    });
  }]);
  if (cfg.email) tries.push(['email', function () {
    return sendEmail(process.env.LEAD_TO_EMAIL,
      'Lead ' + reference + ' — ' + (lead.business || email), bodyText, email);
  }]);

  for (const pair of tries) {
    try { await pair[1](); done.push(pair[0]); }
    catch (err) { failed.push(pair[0] + ': ' + err.message); }
  }

  if (!done.length) {
    console.error('lead ' + reference + ' delivered nowhere: ' + failed.join(' | '));
    return res.status(502).json({ error: 'delivery_failed' });
  }
  if (failed.length) console.warn('lead ' + reference + ' partial: ' + failed.join(' | '));

  /* the applicant's copy — sent only once the lead is safely somewhere */
  let confirmed = false;
  if (cfg.email) {
    try {
      await sendEmail(email,
        'We have your request — ' + reference,
        'Thank you — your request is with us.\n\n' +
        'Your reference is ' + reference + '. Quote it in any reply and we can find you straight away.\n\n' +
        'A person reads every one of these. You will hear back within one business day with a setup\n' +
        'plan for your trade — not a newsletter, and not an automated sequence.\n\n' +
        'This is what you sent us:\n\n' + lines(lead).join('\n') + '\n\n' +
        'If any of it is wrong, reply to this email and we will correct it.\n\n' +
        'Saleringo\nhttps://claude.saleringo.com\n',
        process.env.LEAD_TO_EMAIL);
      confirmed = true;
    } catch (err) {
      console.error('confirmation to ' + email + ' failed: ' + err.message);
    }
  }

  return res.status(200).json({ ok: true, reference: reference, confirmation: confirmed });
}
