/* 도입 문의 접수.
 *
 * 예전에는 받는 곳(웹훅·슬랙·메일)이 하나도 없으면 ready:false 를
 * 돌려주고, 화면은 그걸 보고 메일 작성 창을 대신 열었습니다. 그래서
 * 문의는 어디에도 남지 않았고, 사장님은 누가 왔다 갔는지 알 수 없었습니다.
 *
 * 이제 문의는 먼저 데이터베이스에 남습니다. 알림은 그 뒤에 붙는 것이고,
 * 실패해도 문의는 살아 있습니다.
 */
import { rpc, ipHash, dbConfigured } from './_db.js';

const CTRL = new RegExp('[\\u0000-\\u001f\\u007f]', 'g');
const FIELD_LIMIT = 4000;

function clean(v, limit) {
  return String(v == null ? '' : v)
    .replace(CTRL, ' ')
    .trim()
    .slice(0, limit || FIELD_LIMIT);
}

function notifiers() {
  const to = process.env.LEAD_TO_EMAIL;
  return {
    webhook: !!process.env.LEAD_WEBHOOK_URL,
    slack: !!process.env.SLACK_WEBHOOK_URL,
    email: !!(process.env.RESEND_API_KEY && to && process.env.LEAD_FROM_EMAIL),
    to: to,
  };
}

async function post(url, body, headers) {
  const r = await fetch(url, {
    method: 'POST',
    headers: Object.assign({ 'Content-Type': 'application/json' }, headers || {}),
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error('HTTP ' + r.status);
  return true;
}

async function sendEmail(to, subject, text, replyTo) {
  return post(
    'https://api.resend.com/emails',
    {
      from: process.env.LEAD_FROM_EMAIL,
      to: [to],
      subject: subject,
      text: text,
      reply_to: replyTo || undefined,
    },
    { Authorization: 'Bearer ' + process.env.RESEND_API_KEY },
  );
}

const BR = String.fromCharCode(10);

function lines(lead, ref) {
  return [
    '참조번호: ' + ref,
    '이름: ' + (lead.name || '-'),
    '이메일: ' + lead.email,
    '연락처: ' + (lead.phone || '-'),
    '회사: ' + (lead.company || '-'),
    '업종: ' + (lead.industry || '-'),
    '',
    lead.message || '(남기신 말씀 없음)',
    '',
    '들어온 페이지: ' + (lead.pageUrl || '-'),
  ].join(BR);
}

export default async function handler(req, res) {
  const cfg = notifiers();

  if (req.method === 'GET') {
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({
      /* 문의가 남을 수 있는가. 알림 설정과는 별개입니다. */
      ready: dbConfigured(),
      reason: dbConfigured() ? null : 'db_unconfigured',
      confirmation: cfg.email,
      notify: cfg.webhook || cfg.slack || cfg.email,
    });
  }

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  if (!dbConfigured()) return res.status(503).json({ error: 'db_unconfigured' });

  let body = req.body;
  if (typeof body === 'string') {
    try {
      body = JSON.parse(body);
    } catch (e) {
      body = null;
    }
  }
  if (!body || typeof body !== 'object') return res.status(400).json({ error: 'bad_request' });

  const lead = {
    lang: clean(body.lang, 8) === 'en' ? 'en' : 'ko',
    source: clean(body.source, 60) || 'lead-form',
    name: clean(body.name, 200),
    email: clean(body.email, 200),
    phone: clean(body.phone, 60),
    company: clean(body.company, 200),
    industry: clean(body.industry, 120),
    message: (function () {
      /* get-started 폼의 업종·웹사이트·채널·희망 시간 같은 칸은 DB 열이 없다.
         버리지 않고 메모 뒤에 줄로 붙인다 — 담당자가 읽는 것은 결국 이 칸이다. */
      var base = clean(body.message, 3000);
      var known = { lang: 1, source: 1, name: 1, email: 1, phone: 1, company: 1, industry: 1,
                    message: 1, pageUrl: 1, dedupeKey: 1, utm: 1, company_website_hp: 1,
                    agreePrivacy: 1, agreeMarketing: 1, pageContext: 1 };
      var extra = [];
      Object.keys(body || {}).forEach(function (k) {
        if (known[k]) return;
        var v = body[k];
        if (typeof v !== 'string' && typeof v !== 'number' && typeof v !== 'boolean') return;
        var t = clean(String(v), 300);
        if (t) extra.push(clean(k, 40) + ': ' + t);
      });
      return clean(base + (extra.length ? '\n\n' + extra.join('\n') : ''), 4000);
    })(),
    pageUrl: clean(body.pageUrl, 500),
    referrer: clean(req.headers.referer, 500),
    dedupeKey: clean(body.dedupeKey, 120),
    userAgent: clean(req.headers['user-agent'], 400),
    ipHash: await ipHash(req),
    company_website_hp: clean(body.company_website_hp, 200),
    utm: body.utm && typeof body.utm === 'object' ? body.utm : null,
    consent: {
      privacy: body.agreePrivacy === true ? 'true' : 'false',
      marketing: body.agreeMarketing === true ? 'true' : 'false',
    },
  };

  const r = await rpc('sales_submit_lead', { p: lead });

  if (!r || r.ok !== true) {
    const code = r && r.error;
    if (code === 'rate_limited' || code === 'busy') return res.status(429).json({ error: 'too_many' });
    if (code === 'invalid') return res.status(400).json({ error: 'invalid', fields: r.fields || [] });
    if (code && code.startsWith('db_')) {
      console.error('lead db failure: ' + code + ' ' + (r.detail || ''));
      return res.status(502).json({ error: 'store_failed' });
    }
    return res.status(400).json({ error: code || 'invalid' });
  }
  if (r.ignored) return res.status(200).json({ ok: true, ref: r.ref });

  const text = lines(lead, r.ref);
  const done = [];
  const failed = [];
  const tries = [];
  if (cfg.webhook) tries.push(['webhook', () => post(process.env.LEAD_WEBHOOK_URL, { lead, ref: r.ref })]);
  if (cfg.slack) {
    tries.push([
      'slack',
      () => post(process.env.SLACK_WEBHOOK_URL, { text: '*새 문의* ' + r.ref + BR + '```' + text + '```' }),
    ]);
  }
  if (cfg.email) {
    tries.push([
      'email',
      () => sendEmail(cfg.to, '문의 ' + r.ref + ' — ' + (lead.company || lead.name || lead.email), text, lead.email),
    ]);
  }
  for (const t of tries) {
    try {
      await t[1]();
      done.push(t[0]);
    } catch (err) {
      failed.push(t[0] + ': ' + err.message);
    }
  }
  if (failed.length) console.warn('lead ' + r.ref + ' partial notify: ' + failed.join(' | '));

  let confirmed = false;
  if (cfg.email && !r.duplicate) {
    const ko = lead.lang !== 'en';
    try {
      await sendEmail(
        lead.email,
        (ko ? '문의가 접수되었습니다 — ' : 'We have your message — ') + r.ref,
        (ko
          ? '문의해 주셔서 감사합니다.' + BR + BR +
            '아래 내용으로 접수되었습니다. 영업일 하루 안에 담당자가 연락드립니다.' + BR + BR
          : 'Thank you for getting in touch.' + BR + BR +
            'We have it as below. A person will reply within one business day.' + BR + BR) +
          text + BR + BR +
          'Saleringo' + BR + 'https://claude.saleringo.com' + BR,
        cfg.to,
      );
      confirmed = true;
    } catch (err) {
      console.error('lead confirmation to ' + lead.email + ' failed: ' + err.message);
    }
  }

  return res.status(200).json({
    ok: true,
    ref: r.ref,
    duplicate: !!r.duplicate,
    stored: true,
    notified: done.length > 0,
    confirmation: confirmed,
  });
}
