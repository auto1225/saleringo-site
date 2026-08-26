/* ── 주문 접수 ─────────────────────────────────────────────────────────────
   구매 화면이 보여준 금액을 그대로 믿지 않습니다. 브라우저가 보낸 것은
   "어떤 요금제를 골랐고 통화를 몇 분 쓸 것 같다"까지이고, 실제 금액은
   여기서 assets/data/pricing.json 을 다시 읽어 처음부터 계산합니다.
   같은 파일을 화면도 읽으므로 두 값은 어긋날 수 없고, 어긋난다면 그건
   화면이 틀린 것이지 청구가 틀린 것이 아닙니다.

   결제 승인은 이 파일에서 하지 않습니다. 카드 번호는 결제사의 창에서
   결제사로 바로 가야 하고, 저희 서버를 지나가면 안 되는 정보입니다.
   그래서 이 엔드포인트가 하는 일은 다음 넷입니다.

     1. 주문 내용을 검증한다 (사업자등록번호 체크섬까지)
     2. 금액을 다시 계산한다
     3. 주문번호를 만들고 어딘가에 반드시 남긴다
     4. 구매자에게 주문 내역을 그대로 되돌려 준다

   결제사가 붙기 전까지 주문은 "접수"에서 멈춥니다. 결제된 척하지 않습니다.
   담당자가 확인 전화를 드리고 결제 링크를 보내 드리는 상태이며, 화면도
   그렇게 말합니다.

   Vercel 환경변수에 아래 중 하나만 넣으면 주문이 실제로 도착합니다.
   (리드 폼과 같은 것을 씁니다. 따로 만들 필요 없습니다.)

     ORDER_WEBHOOK_URL   JSON 을 받는 아무 엔드포인트
     LEAD_WEBHOOK_URL    위가 없으면 이것을 씁니다
     SLACK_WEBHOOK_URL   슬랙 수신 웹훅
     RESEND_API_KEY      + ORDER_TO_EMAIL(또는 LEAD_TO_EMAIL) 과 LEAD_FROM_EMAIL

   결제사를 붙일 때는 PAYMENT_PROVIDER 에 portone 또는 toss 를 넣고 해당
   비밀키를 넣으십시오. 그때부터 응답에 결제 요청 정보가 함께 나갑니다. */

import fs from 'fs';
import path from 'path';

const FIELD_LIMIT = 400;
const RATE = new Map();
const SEEN = new Map();               /* 같은 주문이 두 번 들어오는 것을 막는다 */

let PRICING = null;
function pricing() {
  if (PRICING) return PRICING;
  const p = path.join(process.cwd(), 'assets', 'data', 'pricing.json');
  PRICING = JSON.parse(fs.readFileSync(p, 'utf8'));
  return PRICING;
}

const CTRL = new RegExp('[\\u0000-\\u001f\\u007f]', 'g');
function clean(v) {
  return String(v == null ? '' : v).replace(CTRL, ' ').slice(0, FIELD_LIMIT).trim();
}

/* 주문번호는 주문서가 보낸 키에서 만듭니다. 무작위가 아니라 계산이라서,
   같은 주문서를 두 번 눌러도 같은 번호가 나옵니다.

   왜 이렇게까지 하냐면, 아래 SEEN 맵은 이 서버 인스턴스의 기억일 뿐이기
   때문입니다. Vercel 은 요청마다 다른 인스턴스로 보낼 수 있고, 그러면
   두 번째 요청은 첫 번째를 모릅니다. 그때 무작위 번호를 쓰면 같은 주문이
   서로 다른 번호로 두 건 접수되고, 받는 쪽에서는 그 둘이 같은 주문인지
   알 방법이 없습니다. 번호가 같으면 적어도 받는 쪽이 합칠 수 있습니다. */
const ALPHA = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ';
function orderNo(key) {
  const day = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  let tail = '';
  if (key) {
    let h = 2166136261;
    for (let i = 0; i < key.length; i++) {
      h ^= key.charCodeAt(i);
      h = Math.imul(h, 16777619) >>> 0;
    }
    for (let i = 0; i < 4; i++) { tail += ALPHA[h % 32]; h = Math.floor(h / 32) || (h ^ 0x9e3779b9) >>> 0; }
  } else {
    for (let i = 0; i < 4; i++) tail += ALPHA[Math.floor(Math.random() * 32)];
  }
  return 'SO-' + day + '-' + tail;
}

/* 국세청 사업자등록번호 검증식. 자리수만 세는 화면이 많은데, 그러면
   오타 하나가 세금계산서 발행 단계까지 살아남습니다. */
function bizNoValid(raw) {
  const n = String(raw || '').replace(/[^0-9]/g, '');
  if (n.length !== 10) return false;
  const w = [1, 3, 7, 1, 3, 7, 1, 3, 5];
  let sum = 0;
  for (let i = 0; i < 9; i++) sum += Number(n[i]) * w[i];
  sum += Math.floor((Number(n[8]) * 5) / 10);
  return (10 - (sum % 10)) % 10 === Number(n[9]);
}

function limited(ip) {
  const now = Date.now();
  const hits = (RATE.get(ip) || []).filter(t => now - t < 60000);
  hits.push(now);
  RATE.set(ip, hits);
  if (RATE.size > 500) RATE.clear();
  return hits.length > 5;
}

/* 한국 시간으로 오늘이 며칠인가.

   이것이 왜 함수여야 하냐면, 화면은 브라우저의 시간대로 돌고 서버는 UTC 로
   돌기 때문입니다. 한국은 UTC+9 이라 매일 아침 9시 전에는 서버가 어제를
   보고 있습니다. 그 상태로 첫 달을 일할 계산하면 화면에 뜬 금액과 확인
   메일의 금액이 하루치 어긋나고, 매달 1일 오전에는 한 달치가 통째로
   어긋납니다. 파는 쪽과 사는 쪽이 서로 다른 날짜를 보고 있으면 그건
   버그가 아니라 분쟁입니다. 그래서 양쪽 다 서울 날짜만 봅니다. */
function seoulToday(now) {
  var s = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit'
  }).format(now || new Date());
  var p = s.split('-');
  return { y: +p[0], m: +p[1], d: +p[2] };
}

/* 이번 달에 남은 날로 첫 달을 나눠 받습니다. 25일에 시작한 사람에게
   한 달치를 다 받으면 그건 첫인상이 아니라 첫 분쟁입니다. */
function proration(now) {
  const t = seoulToday(now);
  const daysInMonth = new Date(Date.UTC(t.y, t.m, 0)).getUTCDate();
  const remaining = daysInMonth - t.d + 1;
  return { daysInMonth, remaining, factor: remaining / daysInMonth,
           asOf: t.y + '-' + String(t.m).padStart(2, '0') + '-' + String(t.d).padStart(2, '0') };
}

function money(n) { return Math.round(n); }

/* 화면이 보낸 선택만 받아서 금액을 처음부터 다시 만든다.

   무엇을 앞에 세울 것인가가 이 함수의 진짜 결정입니다.

   처음에는 "첫 달 일할 금액"을 합계로 세웠습니다. 그런데 이 제품은 주문한
   날 개시되지 않습니다. 담당자가 확인 연락을 하고, 요금표를 받아 응대를
   만들고, 그것을 먼저 보여 드린 뒤에 시작합니다. 며칠에서 한두 주가
   걸립니다. 그러니 주문일 기준으로 계산한 일할 금액은 청구될 금액이 아니고,
   그걸 "첫 결제 예정액"이라고 적어 메일로 보내면 나중에 다른 금액의
   세금계산서가 갑니다. 월말에 주문할수록 싸 보이는 구조이기도 합니다.

   그래서 앞에 세우는 것은 날짜와 무관한 값, 즉 월 정액(부가세 포함)입니다.
   일할은 "오늘 개시한다면 이만큼"이라는 예시로만 따로 둡니다. */
function quote(sel, now) {
  const P = pricing();
  const plan = P.plans.find(p => p.id === sel.plan);
  if (!plan) return { error: 'plan_unknown' };

  const method = P.methods.find(m => m.id === sel.method);
  if (!method) return { error: 'method_unknown' };

  const pr = proration(now);

  /* 매달 같은 금액. 개시일이 언제든 이 값은 변하지 않습니다. */
  const planNet = plan.monthly;
  const planVat = money(planNet * P.vatRate);

  /* 사용량은 예상치입니다. 첫 청구서에 넣지 않고 따로 보여 줍니다.
     쓰지도 않은 통화료를 미리 받아 놓는 것은 이 제품이 하는 일이 아닙니다. */
  const estimates = [];
  P.usage.forEach(function (u) {
    if (u.planRequires === 'voice' && !plan.voice) return;
    if (u.planRequires === 'messenger' && !plan.messenger) return;
    const qty = Math.max(0, Math.min(100000, Number(sel[u.id]) || 0));
    if (!qty) return;
    estimates.push({ id: u.id, label: u.name, qty: qty, unit: u.unitPrice,
                     amount: money(qty * u.unitPrice), from: !!u.from });
  });
  const estNet = estimates.reduce((a, l) => a + l.amount, 0);

  const firstNet = money(planNet * pr.factor);

  return {
    planId: plan.id, planName: plan.name, method: method.id,
    recurring: method.recurring,
    /* 매달 나가는 값 — 화면이 크게 보여 주는 숫자 */
    monthly: { net: planNet, vat: planVat, total: planNet + planVat },
    /* 개시일이 정해지면 이 규칙으로 첫 달만 다시 계산합니다 */
    firstMonthIfToday: {
      net: firstNet, vat: money(firstNet * P.vatRate),
      total: firstNet + money(firstNet * P.vatRate),
      days: pr.remaining, monthDays: pr.daysInMonth, asOf: pr.asOf
    },
    estimates: estimates,
    estimatedUsage: { net: estNet, vat: money(estNet * P.vatRate),
                      total: estNet + money(estNet * P.vatRate) },
    overage: P.overage,
    currency: P.currency, vatRate: P.vatRate
  };
}

function configured() {
  const to = process.env.ORDER_TO_EMAIL || process.env.LEAD_TO_EMAIL;
  return {
    webhook: !!(process.env.ORDER_WEBHOOK_URL || process.env.LEAD_WEBHOOK_URL),
    slack: !!process.env.SLACK_WEBHOOK_URL,
    email: !!(process.env.RESEND_API_KEY && to && process.env.LEAD_FROM_EMAIL),
    to: to,
    provider: (process.env.PAYMENT_PROVIDER || '').toLowerCase()
  };
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

async function sendEmail(to, subject, text, replyTo) {
  return post('https://api.resend.com/emails', {
    from: process.env.LEAD_FROM_EMAIL, to: [to], subject: subject,
    text: text, reply_to: replyTo || undefined
  }, { Authorization: 'Bearer ' + process.env.RESEND_API_KEY });
}

/* 메일 본문은 여러 줄입니다. 이 환경의 도구가 백슬래시를 삼키는 일이 있어
   줄바꿈을 상수로 두고 이어 붙입니다. 읽기에도 더 분명합니다. */
const BR = String.fromCharCode(10);

function won(n) { return new Intl.NumberFormat('ko-KR').format(n) + '원'; }

function receiptText(o, q, lang) {
  const ko = lang !== 'en';
  const L = [];
  L.push(ko ? '주문번호: ' + o.orderNo : 'Order: ' + o.orderNo);
  L.push(ko ? '접수 시각: ' + o.received : 'Received: ' + o.received);
  L.push('');
  L.push(ko ? '── 주문 내용 ──' : '-- Order --');
  L.push((ko ? '요금제: ' : 'Plan: ') + q.planName[ko ? 'ko' : 'en']);
  L.push((ko ? '월 정액: ' : 'Monthly: ') + won(q.monthly.net) +
         (ko ? ' (부가세 ' : ' (VAT ') + won(q.monthly.vat) +
         (ko ? ') = 월 ' : ') = ') + won(q.monthly.total) + (ko ? '' : ' a month'));
  L.push((ko ? '결제 수단: ' : 'Payment: ') + o.methodName);
  L.push('');
  L.push(ko
    ? '첫 달은 개시일부터 그 달 말일까지 날짜로 나눠 계산합니다.' + BR +
      '개시일이 정해지면 그 날짜로 다시 계산한 확정 금액을 알려 드립니다.' + BR +
      '참고로 ' + q.firstMonthIfToday.asOf + ' 에 개시한다면 ' +
      q.firstMonthIfToday.days + '/' + q.firstMonthIfToday.monthDays + '일치인 ' +
      won(q.firstMonthIfToday.total) + ' 입니다.'
    : 'The first month is prorated by days from the start date.' + BR +
      'Once the start date is set we send the exact figure for it.' + BR +
      'For reference, starting on ' + q.firstMonthIfToday.asOf + ' would be ' +
      q.firstMonthIfToday.days + '/' + q.firstMonthIfToday.monthDays + ' days, ' +
      won(q.firstMonthIfToday.total) + '.');
  if (q.estimates.length) {
    L.push('');
    L.push(ko ? '── 사용량 예상 (청구 아님) ──' : '-- Usage estimate, not billed --');
    q.estimates.forEach(function (e) {
      L.push('  ' + e.label[ko ? 'ko' : 'en'] + ' ' + e.qty + ' × ' + won(e.unit) +
             (e.from ? (ko ? '부터' : ' and up') : '') + ' = ' + won(e.amount));
    });
    L.push(ko ? '  사용량은 쓰신 만큼 다음 달에 정산합니다.'
              : '  Usage is settled next month on what you actually use.');
  }
  L.push('');
  L.push(ko ? '── 사업자 정보 ──' : '-- Business --');
  L.push((ko ? '상호: ' : 'Company: ') + o.company);
  L.push((ko ? '사업자등록번호: ' : 'Registration no: ') + o.bizNo);
  L.push((ko ? '대표자: ' : 'Representative: ') + (o.ceo || '-'));
  L.push((ko ? '담당자: ' : 'Contact: ') + o.contact + ' / ' + o.email + ' / ' + (o.phone || '-'));
  L.push((ko ? '세금계산서 수신: ' : 'Tax invoice to: ') + (o.taxEmail || o.email) +
         (o.taxEmail ? '' : (ko ? ' (담당자 이메일과 동일)' : ' (same as contact)')));
  return L.join(BR);
}

export default async function handler(req, res) {
  const cfg = configured();
  const ready = cfg.webhook || cfg.slack || cfg.email;

  if (req.method === 'GET') {
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({
      ready: ready,
      confirmation: cfg.email,
      /* 결제사가 아직 없다는 사실을 화면이 알아야 "결제하기"가 아니라
         "주문 접수하기"라고 쓸 수 있습니다. */
      payment: cfg.provider || null
    });
  }

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  if (!ready) return res.status(503).json({ error: 'no_destination_configured' });

  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  if (limited(ip)) return res.status(429).json({ error: 'too_many' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = null; } }
  if (!body || typeof body !== 'object') return res.status(400).json({ error: 'bad_request' });

  if (clean(body.company_website_hp)) return res.status(200).json({ ok: true, orderNo: orderNo(clean(body.idempotencyKey)) });

  /* 같은 주문서를 두 번 눌러도 주문은 하나입니다. 브라우저가 보낸 키를
     기억해 두고, 두 번째 요청에는 첫 번째의 답을 그대로 돌려줍니다. */
  const idem = clean(body.idempotencyKey).slice(0, 64);
  if (idem && SEEN.has(idem)) return res.status(200).json(SEEN.get(idem));

  const o = {
    company: clean(body.company),
    bizNo: clean(body.bizNo).replace(/[^0-9]/g, ''),
    ceo: clean(body.ceo),
    contact: clean(body.contact),
    email: clean(body.email),
    phone: clean(body.phone).replace(/[^0-9]/g, ''),
    taxEmail: clean(body.taxEmail),
    note: clean(body.note),
    lang: clean(body.lang) === 'en' ? 'en' : 'ko'
  };

  const bad = [];
  if (!o.company) bad.push('company');
  if (!bizNoValid(o.bizNo)) bad.push('bizNo');
  if (!o.contact) bad.push('contact');
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(o.email)) bad.push('email');
  if (o.phone && (o.phone.length < 9 || o.phone.length > 11)) bad.push('phone');
  if (o.taxEmail && !/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(o.taxEmail)) bad.push('taxEmail');
  /* 전자상거래법상 필수 동의. 서버에서도 봅니다 — 화면의 체크박스는
     지우고 보낼 수 있기 때문입니다. */
  if (body.agreeTerms !== true) bad.push('agreeTerms');
  if (body.agreePrivacy !== true) bad.push('agreePrivacy');
  if (body.agreeTransfer !== true) bad.push('agreeTransfer');
  if (bad.length) return res.status(400).json({ error: 'invalid', fields: bad });

  const q = quote({
    plan: clean(body.plan), method: clean(body.method),
    voiceMinutes: body.voiceMinutes, alimtalk: body.alimtalk
  }, new Date());
  if (q.error) return res.status(400).json({ error: q.error });
  if (body.method === 'card' && body.agreeRecurring !== true) {
    return res.status(400).json({ error: 'invalid', fields: ['agreeRecurring'] });
  }

  const P = pricing();
  o.methodName = P.methods.find(m => m.id === q.method).name[o.lang];
  o.orderNo = orderNo(idem);
  o.received = new Date().toISOString();
  o.marketing = body.agreeMarketing === true;

  const record = Object.assign({}, o, { ip: ip, quote: q });
  const text = receiptText(o, q, o.lang);

  const done = [], failed = [], tries = [];
  const hook = process.env.ORDER_WEBHOOK_URL || process.env.LEAD_WEBHOOK_URL;
  if (cfg.webhook) tries.push(['webhook', () => post(hook, record)]);
  if (cfg.slack) tries.push(['slack', () => post(process.env.SLACK_WEBHOOK_URL,
    { text: '*새 주문* ' + o.orderNo + '\n```' + text + '```' })]);
  if (cfg.email) tries.push(['email', () => sendEmail(cfg.to,
    '주문 ' + o.orderNo + ' — ' + o.company, text, o.email)]);

  for (const t of tries) {
    try { await t[1](); done.push(t[0]); }
    catch (err) { failed.push(t[0] + ': ' + err.message); }
  }
  if (!done.length) {
    console.error('order ' + o.orderNo + ' delivered nowhere: ' + failed.join(' | '));
    return res.status(502).json({ error: 'delivery_failed' });
  }
  if (failed.length) console.warn('order ' + o.orderNo + ' partial: ' + failed.join(' | '));

  let confirmed = false;
  if (cfg.email) {
    const ko = o.lang !== 'en';
    try {
      await sendEmail(o.email,
        (ko ? '주문이 접수되었습니다 — ' : 'We have your order — ') + o.orderNo,
        (ko
          ? '주문해 주셔서 감사합니다.\n\n' +
            '아래 내용으로 접수되었습니다. 아직 결제된 것은 아닙니다.\n' +
            '담당자가 영업일 하루 안에 확인 연락을 드리고, 결제 안내를 함께 보내 드립니다.\n' +
            '그 전까지는 어떤 금액도 청구되지 않습니다.\n\n'
          : 'Thank you for your order.\n\n' +
            'It is recorded as below. Nothing has been charged yet.\n' +
            'A person will confirm within one business day and send the payment step.\n' +
            'Until then no amount is taken.\n\n') +
        text + '\n\n' +
        (ko
          ? '내용이 틀렸으면 이 메일에 그대로 답장해 주십시오. 고쳐 드립니다.\n' +
            '취소하고 싶으시면 답장에 "취소"라고만 적어 주셔도 됩니다.\n\n'
          : 'If any of it is wrong, reply to this email and we will correct it.\n' +
            'To cancel, replying with the word "cancel" is enough.\n\n') +
        'Saleringo\nhttps://claude.saleringo.com\n',
        cfg.to);
      confirmed = true;
    } catch (err) {
      console.error('order confirmation to ' + o.email + ' failed: ' + err.message);
    }
  }

  const out = {
    ok: true, orderNo: o.orderNo, confirmation: confirmed,
    /* 결제사가 붙기 전까지 상태는 "접수"입니다. 화면이 이 값을 보고
       "결제 완료"라고 쓰지 않게 합니다. */
    status: cfg.provider ? 'awaiting_payment' : 'received',
    payment: cfg.provider || null,
    quote: q
  };
  if (idem) {
    SEEN.set(idem, out);
    if (SEEN.size > 500) SEEN.clear();
  }
  return res.status(200).json(out);
}
