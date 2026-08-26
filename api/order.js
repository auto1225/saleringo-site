/* 주문 접수.
 *
 * 예전에는 이 파일이 금액을 계산하고, 주문번호를 만들고, 중복을 막고,
 * 웹훅과 메일로 내보내는 일을 모두 했습니다. 그 셋이 서로 다른 곳에
 * 있었기 때문에 어긋날 수 있었고, 실제로 어긋났습니다.
 *
 *   · 주문번호를 서버 인스턴스의 기억에서 만들었습니다. Vercel 은 요청마다
 *     다른 인스턴스로 보낼 수 있으므로, 같은 주문이 두 번 접수될 수
 *     있었습니다.
 *   · 유량 제한도 인스턴스마다 따로 셌으므로 사실상 제한이 없었습니다.
 *   · 무엇보다, 받는 곳이 하나도 설정되지 않으면 주문이 **아무 데도**
 *     남지 않았습니다. 그리고 실제로 하나도 설정되어 있지 않았습니다.
 *
 * 이제 접수는 데이터베이스가 합니다. 검증·금액 계산·발번·중복 방지가
 * 한 트랜잭션에서 끝나므로 서로 어긋날 수 없습니다. 메일과 웹훅은 그
 * 뒤에 붙는 알림일 뿐이고, 실패해도 주문은 이미 남아 있습니다.
 *
 * 금액은 이 파일에서 계산하지 않습니다. 화면이 보낸 금액도 쓰지 않습니다.
 * 선택만 데이터베이스로 넘기고, 데이터베이스가 그때 유효한 요금표로
 * 처음부터 다시 계산한 값을 받아 적습니다.
 */
import fs from 'node:fs';
import path from 'node:path';
import { rpc, readiness, ipHash, dbConfigured } from './_db.js';

const CTRL = new RegExp('[\\u0000-\\u001f\\u007f]', 'g');
const FIELD_LIMIT = 400;

function clean(v, limit) {
  return String(v == null ? '' : v)
    .replace(CTRL, ' ')
    .trim()
    .slice(0, limit || FIELD_LIMIT);
}

let PRICING = null;
function pricing() {
  if (!PRICING) {
    const p = path.join(process.cwd(), 'assets', 'data', 'pricing.json');
    PRICING = JSON.parse(fs.readFileSync(p, 'utf8'));
  }
  return PRICING;
}

/* 알림 경로. 주문이 남는 것과는 별개입니다 — 하나도 없어도 주문은
   데이터베이스에 남고, 사장님이 나중에 열어 보실 수 있습니다. */
function notifiers() {
  const to = process.env.ORDER_TO_EMAIL || process.env.LEAD_TO_EMAIL;
  return {
    webhook: !!(process.env.ORDER_WEBHOOK_URL || process.env.LEAD_WEBHOOK_URL),
    slack: !!process.env.SLACK_WEBHOOK_URL,
    email: !!(process.env.RESEND_API_KEY && to && process.env.LEAD_FROM_EMAIL),
    to: to,
    provider: (process.env.PAYMENT_PROVIDER || '').toLowerCase(),
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

/* 메일 본문은 여러 줄입니다. 이 환경의 도구가 백슬래시를 삼키는 일이 있어
   줄바꿈을 상수로 두고 이어 붙입니다. 읽기에도 더 분명합니다. */
const BR = String.fromCharCode(10);

/* 금액을 그 통화의 관습대로 씁니다. 599 는 "$599", 0.14 는 "$0.14".
   자리수를 하나로 고정하면 둘 중 하나가 틀립니다. */
function amount(n, cur) {
  const c = pricing().currencies[cur] || pricing().currencies.KRW;
  const v = Number(n) || 0;
  const whole = Math.abs(v - Math.round(v)) < 1e-9;
  const s = new Intl.NumberFormat(c.locale, {
    minimumFractionDigits: whole ? 0 : c.decimals,
    maximumFractionDigits: whole ? 0 : c.decimals,
  }).format(v);
  return c.position === 'before' ? c.symbol + s : s + c.symbol;
}

function lambdaOf(ko) {
  return (k, e) => (ko ? k : e);
}

/* 세금 처리마다 다른 한 줄. 문장은 policy.json 이 정하고, 여기서는
   데이터베이스가 판정한 결과에 맞는 것을 고르기만 합니다. */
function taxLine(treat, ko) {
  const L = lambdaOf(ko);
  if (treat === 'vat_charged') {
    return L(
      '대한민국 사업자이시므로 부가세 10%를 더해 청구하고 전자세금계산서를 발행합니다.',
      'You are a Korean business, so 10% VAT is added and a Korean tax invoice is issued.',
    );
  }
  if (treat === 'reverse') {
    return L(
      '대리납부(리버스 차지) 대상입니다. 저희가 세금을 붙이지 않고 귀사가 자국에 신고·납부하십니다.',
      'This is a reverse-charge sale. We add no tax and you account for it in your own country.',
    );
  }
  if (treat === 'none') {
    return L(
      '저희는 대한민국 법인이고 귀사 국가에 세무 등록이 없어 세금을 걷지 않습니다.',
      'We are a Korean company with no tax registration in your country, so we add no tax.',
    );
  }
  return L(
    '세금 처리는 구매 주체와 청구 국가를 확인한 뒤 서면 주문서에서 확정합니다. 위 금액은 세전입니다.',
    'Tax treatment is confirmed in the written order after we verify the buying entity and billing country. The amounts above are pre-tax.',
  );
}

function receiptText(o, r, lang) {
  const ko = lang !== 'en';
  const L = lambdaOf(ko);
  const q = r.quote || {};
  const cur = q.currency || 'KRW';
  const A = (n) => amount(n, cur);
  const out = [];

  out.push(L('주문번호: ', 'Order: ') + r.orderNo);
  out.push(L('접수 시각: ', 'Received: ') + r.receivedAt);
  out.push(L('상태: ', 'State: ') + r.state);
  out.push('');

  out.push(L('-- 주문 내용 --', '-- Order --'));
  if (q.planName) out.push(L('요금제: ', 'Plan: ') + q.planName[ko ? 'ko' : 'en']);
  out.push(L('구매 주체: ', 'Buying as: ') + (o.buyerType || 'unknown'));
  out.push(L('청구 국가: ', 'Billing country: ') + o.country);
  if (o.billingAddress) out.push(L('청구 주소: ', 'Billing address: ') + o.billingAddress);
  if (o.serviceCountry && o.serviceCountry !== o.country) {
    out.push(L('서비스 이용 국가: ', 'Service country: ') + o.serviceCountry);
  }
  out.push('');

  if (q.monthly) {
    out.push(L('월 이용료: ', 'Monthly: ') + A(q.monthly.net));
    if (q.taxCollected) {
      const lbl = q.taxLabel ? q.taxLabel[ko ? 'ko' : 'en'] : L('세금', 'Tax');
      out.push(lbl + ': ' + A(q.monthly.tax));
    }
    out.push(L('매월 결제 금액: ', 'Charged every month: ') + A(q.monthly.total));
  }

  /* 할인이 끝나면 금액이 두 배가 됩니다. 그 사실이 이 메일에 없으면,
     구매자에게 남는 유일한 기록은 할인가 하나뿐입니다. */
  if (q.discount && q.afterDiscount) {
    out.push(
      '  ' +
        L(
          '위 금액은 ' +
            q.discount.name.ko +
            '(' +
            q.discount.percent +
            '% 할인)이 적용된 처음 ' +
            q.discount.months +
            '개월치입니다.',
          'That is the ' +
            q.discount.name.en +
            ' price (' +
            q.discount.percent +
            '% off) for your first ' +
            q.discount.months +
            ' months.',
        ),
    );
    out.push(
      '  ' +
        L(
          (q.discount.months + 1) + '개월째부터는 매월 ' + A(q.afterDiscount.total) + ' 입니다.',
          'From month ' + (q.discount.months + 1) + ' it is ' + A(q.afterDiscount.total) + ' a month.',
        ),
    );
  }
  out.push(L('결제 수단: ', 'Payment: ') + (o.methodName || o.method));
  out.push('');

  if (q.firstMonthIfToday) {
    out.push(
      L(
        '첫 달은 개시일부터 그 달 말일까지 날짜로 나눠 계산합니다.',
        'The first month is prorated by days from the start date.',
      ),
    );
    out.push(
      L(
        '참고로 ' +
          q.firstMonthIfToday.asOf +
          ' 에 개시한다면 그 달 ' +
          q.firstMonthIfToday.monthDays +
          '일 가운데 ' +
          q.firstMonthIfToday.days +
          '일치로 ' +
          A(q.firstMonthIfToday.total) +
          ' 입니다.',
        'For reference, starting on ' +
          q.firstMonthIfToday.asOf +
          ' would be ' +
          q.firstMonthIfToday.days +
          ' of that month’s ' +
          q.firstMonthIfToday.monthDays +
          ' days, ' +
          A(q.firstMonthIfToday.total) +
          '.',
      ),
    );
    out.push('');
  }

  out.push(L('-- 세금 --', '-- Tax --'));
  out.push(taxLine(q.taxTreatment, ko));
  out.push('');

  /* 화면에서 끝내지 못한 이유가 있으면 그대로 적습니다. 구매자가
     "왜 서면으로 가는지" 를 메일에서 다시 확인할 수 있어야 합니다. */
  if (Array.isArray(r.blockers) && r.blockers.length) {
    out.push(L('-- 서면 주문으로 진행하는 이유 --', '-- Why this goes to a written order --'));
    r.blockers.forEach((b) => out.push('· ' + (ko ? b.ko : b.en)));
    out.push('');
  }

  out.push(L('-- 지금 상태 --', '-- Where this stands --'));
  out.push(
    L(
      '아직 결제되지 않았습니다. 계약은 서면 주문서에 양측이 서명한 때 성립합니다.',
      'Nothing has been charged. The contract is formed when both sides sign the written order.',
    ),
  );
  out.push(
    L(
      '주문 조회: https://claude.saleringo.com/ko/order-status.html',
      'Check this order: https://claude.saleringo.com/en/order-status.html',
    ),
  );

  return out.join(BR);
}

export default async function handler(req, res) {
  const cfg = notifiers();

  if (req.method === 'GET') {
    res.setHeader('Cache-Control', 'no-store');
    if (!dbConfigured()) {
      return res.status(200).json({
        ready: false,
        reason: 'db_unconfigured',
        confirmation: false,
        payment: null,
      });
    }
    const r = await readiness();
    return res.status(200).json({
      /* 주문을 받을 수 있는가. 알림 설정이 아니라 **주문이 남을 수 있는가**로
         판정합니다. 남지 않는데 접수되었다고 말하는 것이 가장 나쁜 실패입니다. */
      ready: !!(r && r.ready),
      reason: r && r.ready ? null : (r && r.error) || 'pricing_not_loaded',
      confirmation: cfg.email,
      notify: cfg.webhook || cfg.slack || cfg.email,
      /* 결제사가 아직 없다는 사실을 화면이 알아야 "결제하기"가 아니라
         "주문 접수하기"라고 쓸 수 있습니다. */
      payment: cfg.provider || null,
      pricingVersion: (r && r.pricingVersion) || null,
      policyVersion: (r && r.policyVersion) || null,
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

  const lang = clean(body.lang) === 'en' ? 'en' : 'ko';

  const payload = {
    lang: lang,
    country: clean(body.country, 6).toUpperCase(),
    taxCountry: clean(body.taxCountry, 6).toUpperCase(),
    serviceCountry: clean(body.serviceCountry, 6).toUpperCase(),
    billingAddress: clean(body.billingAddress, 400),
    buyerType: clean(body.buyerType, 20),
    company: clean(body.company, 200),
    ceo: clean(body.ceo, 120),
    taxId: clean(body.bizNo || body.taxId, 60),
    contact: clean(body.contact, 120),
    email: clean(body.email, 200),
    phone: clean(body.phone, 60).replace(/[^0-9+\- ()]/g, ''),
    taxEmail: clean(body.taxEmail, 200),
    note: clean(body.note, 4000),
    plan: clean(body.plan, 40),
    method: clean(body.method, 40),
    voiceMinutes: Math.max(0, Math.min(1000000, Number(body.voiceMinutes) || 0)),
    alimtalk: Math.max(0, Math.min(1000000, Number(body.alimtalk) || 0)),
    idempotencyKey: clean(body.idempotencyKey, 120),
    pageUrl: clean(body.pageUrl, 500),
    userAgent: clean(req.headers['user-agent'], 400),
    ipHash: await ipHash(req),
    company_website_hp: clean(body.company_website_hp, 200),
    consent: {
      terms: body.agreeTerms === true ? 'true' : 'false',
      privacy: body.agreePrivacy === true ? 'true' : 'false',
      transfer: body.agreeTransfer === true ? 'true' : 'false',
      recurring: body.agreeRecurring === true ? 'true' : 'false',
      marketing: body.agreeMarketing === true ? 'true' : 'false',
    },
  };

  /* 요금표가 데이터베이스에 올라와 있지 않으면 금액을 계산할 근거가
     없습니다. 그 상태로 접수하지 않습니다. */
  const ready = await readiness();
  if (!ready || !ready.ready) {
    return res.status(503).json({ error: 'not_ready', reason: (ready && ready.error) || 'pricing_not_loaded' });
  }

  const r = await rpc('sales_submit_order', { p: payload });

  if (!r || r.ok !== true) {
    const code = r && r.error;
    if (code === 'rate_limited' || code === 'busy') return res.status(429).json({ error: 'too_many' });
    if (code === 'invalid') return res.status(400).json({ error: 'invalid', fields: r.fields || [] });
    if (code && code.startsWith('db_')) {
      console.error('order db failure: ' + code + ' ' + (r.detail || ''));
      return res.status(502).json({ error: 'store_failed' });
    }
    return res.status(400).json({ error: code || 'invalid' });
  }

  if (r.ignored) return res.status(200).json({ ok: true, orderNo: r.orderNo });

  /* 여기서부터 주문은 이미 데이터베이스에 남아 있습니다.
     아래 알림이 하나도 안 나가도 주문은 살아 있습니다. */
  const P = pricing();
  const m = P.methods.find((x) => x.id === (r.quote && r.quote.method));
  const o = {
    orderNo: r.orderNo,
    country: payload.country,
    serviceCountry: payload.serviceCountry,
    billingAddress: payload.billingAddress,
    buyerType: payload.buyerType,
    company: payload.company,
    email: payload.email,
    method: payload.method,
    methodName: m ? m.name[lang] : payload.method,
  };
  const text = receiptText(o, r, lang);

  const done = [];
  const failed = [];
  const tries = [];
  const hook = process.env.ORDER_WEBHOOK_URL || process.env.LEAD_WEBHOOK_URL;
  if (cfg.webhook) tries.push(['webhook', () => post(hook, { order: o, result: r })]);
  if (cfg.slack) {
    tries.push([
      'slack',
      () =>
        post(process.env.SLACK_WEBHOOK_URL, {
          text: '*새 주문* ' + r.orderNo + ' (' + r.state + ')' + BR + '```' + text + '```',
        }),
    ]);
  }
  if (cfg.email) {
    tries.push([
      'email',
      () => sendEmail(cfg.to, '주문 ' + r.orderNo + ' — ' + payload.company, text, payload.email),
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
  if (failed.length) console.warn('order ' + r.orderNo + ' partial notify: ' + failed.join(' | '));
  if (!tries.length) console.warn('order ' + r.orderNo + ' stored; no notifier configured');

  let confirmed = false;
  if (cfg.email && !r.duplicate) {
    const ko = lang !== 'en';
    const proposal = r.route === 'proposal';
    try {
      await sendEmail(
        payload.email,
        (ko ? '주문이 접수되었습니다 — ' : 'We have your order — ') + r.orderNo,
        (ko
          ? '주문해 주셔서 감사합니다.' + BR + BR +
            '아래 내용으로 접수되었습니다. 아직 결제된 것은 아닙니다.' + BR +
            (proposal
              ? '확인이 필요한 항목이 있어 서면 주문 제안으로 진행합니다. 담당자가 영업일 하루 안에 연락드립니다.'
              : '담당자가 영업일 하루 안에 확인 연락을 드리고, 서면 주문서를 보내 드립니다.') + BR +
            '계약은 서면 주문서에 양측이 서명한 때 성립하며, 그 전까지는 어떤 금액도 청구되지 않습니다.' + BR + BR
          : 'Thank you for your order.' + BR + BR +
            'It is recorded as below. Nothing has been charged yet.' + BR +
            (proposal
              ? 'Some details need checking, so this continues as a written order proposal. A person will contact you within one business day.'
              : 'A person will confirm within one business day and send the written order.') + BR +
            'The contract is formed when both sides sign the written order. Until then nothing is charged.' + BR + BR) +
          text + BR + BR +
          (ko
            ? '내용이 틀렸으면 이 메일에 그대로 답장해 주십시오. 고쳐 드립니다.' + BR +
              '취소하고 싶으시면 답장에 "취소"라고만 적어 주셔도 됩니다.' + BR + BR
            : 'If any of it is wrong, reply to this email and we will correct it.' + BR +
              'To cancel, replying with the word "cancel" is enough.' + BR + BR) +
          'Saleringo' + BR + 'https://claude.saleringo.com' + BR,
        cfg.to,
      );
      confirmed = true;
    } catch (err) {
      console.error('order confirmation to ' + payload.email + ' failed: ' + err.message);
    }
  }

  return res.status(200).json({
    ok: true,
    orderNo: r.orderNo,
    state: r.state,
    /* 'online' 이면 화면에서 확정된 주문, 'proposal' 이면 확인할 것이
       남아 서면 주문 제안으로 넘어간 주문입니다. */
    route: r.route,
    blockers: r.blockers || [],
    duplicate: !!r.duplicate,
    confirmation: confirmed,
    stored: true,
    notified: done.length > 0,
    payment: cfg.provider || null,
    receivedAt: r.receivedAt,
    quote: r.quote,
  });
}
