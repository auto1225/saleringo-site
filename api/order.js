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

/* 사업자 번호는 나라마다 다릅니다.

   처음에는 한국 국세청 검증식 하나만 두고 모든 구매자에게 필수로 걸었습니다.
   그러면 런던에 있는 사람은 이 주문서를 끝낼 수 없습니다 - 통과할 방법이
   없는 칸이기 때문입니다. 영문 사이트가 광고하는 가격을 보고 들어온 사람이
   한국 사업자등록번호를 요구받는 것은, 팔 생각이 없다는 뜻으로 읽힙니다.

   그래서 검증은 그 번호가 실제로 검증 가능한 나라에서만 합니다. 한국은
   세금계산서 발행에 번호가 있어야 하므로 필수이고 체크섬까지 봅니다.
   나머지 나라에서는 인보이스에 찍어 드릴 뿐이라 선택이고, 형식만 봅니다.
   확인할 수 없는 것을 확인한 척하지 않습니다. */
function krBizNoValid(raw) {
  const n = String(raw || '').replace(/[^0-9]/g, '');
  if (n.length !== 10) return false;
  const w = [1, 3, 7, 1, 3, 7, 1, 3, 5];
  let sum = 0;
  for (let i = 0; i < 9; i++) sum += Number(n[i]) * w[i];
  sum += Math.floor((Number(n[8]) * 5) / 10);
  return (10 - (sum % 10)) % 10 === Number(n[9]);
}

function country(code) {
  const P = pricing();
  return P.countries.find(c => c.code === code) || null;
}

function taxIdOk(c, raw) {
  const v = String(raw || '').trim();
  if (!v) return !c.taxIdRequired;
  if (c.taxIdCheck === 'kr') return krBizNoValid(v);
  /* 그 밖의 나라는 형식만 봅니다. 세계의 모든 사업자 번호 규칙을 안다고
     주장하는 것보다, 사람이 보고 확인하는 편이 정직합니다. */
  return /^[A-Za-z0-9][A-Za-z0-9 .\-\/]{3,29}$/.test(v);
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

   무엇을 앞에 세울 것인가가 이 함수의 첫 번째 결정이었습니다.
   처음에는 "첫 달 일할 금액"을 합계로 세웠는데, 이 제품은 주문한 날
   개시되지 않습니다. 담당자가 확인하고, 요금표를 받아 응대를 만들고,
   그것을 보여 드린 뒤에 시작합니다. 그러니 주문일 기준 일할 금액은
   청구될 금액이 아니고, 그걸 "첫 결제 예정액"이라고 메일로 보내면
   나중에 다른 금액의 인보이스가 갑니다. 그래서 앞에 세우는 것은 날짜와
   무관한 값, 월 정액입니다.

   두 번째 결정은 세금입니다. 저희는 대한민국 법인이고, 한국 밖에서
   세금을 걷을 권한이 있는 곳에 등록되어 있지 않습니다. 그래서 한국에는
   부가세 10%를 붙이고, 그 밖에는 붙이지 않습니다. 없는 등록을 있는 것처럼
   적지 않습니다. EU 처럼 리버스 차지 대상이면 신고 의무가 구매자 쪽에
   생기고, 그 사실을 화면과 인보이스에 적습니다. */
function quote(sel, now) {
  const P = pricing();
  const plan = P.plans.find(p => p.id === sel.plan);
  if (!plan) return { error: 'plan_unknown' };

  const method = P.methods.find(m => m.id === sel.method);
  if (!method) return { error: 'method_unknown' };

  const c = country(sel.country);
  if (!c) return { error: 'country_unknown' };

  const cur = c.currency;
  const money = n => (cur === 'KRW' ? Math.round(n) : Math.round(n * 100) / 100);

  const rule = P.tax[c.code] || P.tax.default;
  const rate = rule.collected ? rule.rate : 0;

  const pr = proration(now);

  const listNet = plan.price[cur];
  /* 창립 코호트 할인. 영문 약관 제2조가 "가입 시 확정"이라고 적은 약속이라,
     주문서가 정가만 보여 주면 그 약관에 동의하라고 하면서 약관을 어기는
     꼴이 됩니다. */
  const disc = P.discount && P.discount.active ? P.discount : null;
  const planNet = disc ? money(listNet * (100 - disc.percent) / 100) : listNet;
  const planTax = money(planNet * rate);

  const estimates = [];
  P.usage.forEach(function (u) {
    if (u.planRequires === 'voice' && !plan.voice) return;
    if (u.planRequires === 'messenger' && !plan.messenger) return;
    const qty = Math.max(0, Math.min(1000000, Number(sel[u.id]) || 0));
    if (!qty) return;
    estimates.push({ id: u.id, label: u.name, qty: qty, unit: u.unitPrice[cur],
                     amount: money(qty * u.unitPrice[cur]), from: !!u.from });
  });
  const estNet = estimates.reduce((a, l) => a + l.amount, 0);

  const firstNet = money(planNet * pr.factor);

  return {
    planId: plan.id, planName: plan.name, method: method.id,
    recurring: method.recurring,
    country: c.code, currency: cur,
    taxRate: rate, taxCollected: !!rule.collected,
    taxLabel: rule.label || null,
    reverseCharge: !!(c.reverseCharge && !rule.collected),
    monthly: { net: planNet, tax: planTax, total: money(planNet + planTax) },
    firstMonthIfToday: {
      net: firstNet, tax: money(firstNet * rate),
      total: money(firstNet + money(firstNet * rate)),
      days: pr.remaining, monthDays: pr.daysInMonth, asOf: pr.asOf
    },
    estimates: estimates,
    estimatedUsage: { net: estNet, tax: money(estNet * rate),
                      total: money(estNet + money(estNet * rate)) },
    listPrice: listNet,
    discount: disc ? { percent: disc.percent, months: disc.months,
                       name: disc.name, saves: money(listNet - planNet) } : null,
    afterDiscount: disc ? { net: listNet, tax: money(listNet * rate),
                            total: money(listNet + money(listNet * rate)) } : null,
    seats: plan.seats,
    /* 요금 페이지가 "이 나라는 아직 음성이 안 된다"고 적어 두었습니다.
       그 나라 구매자에게 AI 전화가 든 요금제를 말없이 파는 것은
       곧 환불 요청입니다. */
    voiceAvailable: c.voice !== false,
    voiceUnavailableHere: !!(plan.voice && c.voice === false),
    overage: { perConversation: P.overage.perConversation[cur],
               conversations: plan.conversations },
    vatRate: rate
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

/* 금액을 그 통화의 관습대로 씁니다. 원화는 뒤에 "원", 달러는 앞에 "$",
   소수점 자리수도 다릅니다. 79.00 달러라고 쓰면 아무도 그렇게 읽지 않고,
   110000.00 원은 잘못 쓴 것처럼 보입니다. */
function amount(n, cur) {
  const c = pricing().currencies[cur] || pricing().currencies.KRW;
  /* 599 는 "$599", 0.14 는 "$0.14". 자리수를 하나로 고정하면 둘 중 하나가
     틀립니다. 0 으로 고정하면 분당 요금이 "$0" 이 되고 - 실제로 그렇게
     나가고 있었습니다 - 2 로 고정하면 요금제가 "$599.00" 이 됩니다. */
  const whole = Math.abs(n - Math.round(n)) < 1e-9;
  const s = new Intl.NumberFormat(c.locale, {
    minimumFractionDigits: whole ? 0 : c.decimals,
    maximumFractionDigits: whole ? 0 : c.decimals
  }).format(n);
  return c.position === 'before' ? c.symbol + s : s + c.symbol;
}

function receiptText(o, q, lang) {
  const ko = lang !== 'en';
  const L = lambdaOf(ko);
  const A = n => amount(n, q.currency);
  const out = [];
  out.push(L('주문번호: ', 'Order: ') + o.orderNo);
  out.push(L('접수 시각: ', 'Received: ') + o.received);
  out.push('');
  out.push(L('-- 주문 내용 --', '-- Order --'));
  out.push(L('요금제: ', 'Plan: ') + q.planName[ko ? 'ko' : 'en']);
  out.push(L('월 이용료: ', 'Monthly: ') + A(q.monthly.net));
  if (q.taxCollected) {
    out.push((q.taxLabel ? q.taxLabel[ko ? 'ko' : 'en'] : L('세금', 'Tax')) + ': ' + A(q.monthly.tax));
  }
  out.push(L('매월 결제 금액: ', 'Charged every month: ') + A(q.monthly.total) +
           (q.taxCollected ? '' : L(' (세금 별도 - 아래 참조)', ' (tax not added - see below)')));
  out.push(L('결제 수단: ', 'Payment: ') + o.methodName);
  out.push('');
  out.push(L('첫 달은 개시일부터 그 달 말일까지 날짜로 나눠 계산합니다.',
             'The first month is prorated by days from the start date.'));
  out.push(L('개시일이 정해지면 그 날짜로 다시 계산한 확정 금액을 알려 드립니다.',
             'Once the start date is set we send the exact figure.'));
  out.push(L('참고로 ' + q.firstMonthIfToday.asOf + ' 에 개시한다면 ' +
             q.firstMonthIfToday.days + '/' + q.firstMonthIfToday.monthDays + '일치인 ' +
             A(q.firstMonthIfToday.total) + ' 입니다.',
             'For reference, starting on ' + q.firstMonthIfToday.asOf + ' would be ' +
             q.firstMonthIfToday.days + '/' + q.firstMonthIfToday.monthDays + ' days, ' +
             A(q.firstMonthIfToday.total) + '.'));
  out.push('');
  out.push(L('-- 세금 --', '-- Tax --'));
  if (q.taxCollected) {
    out.push(L('한국 사업자이시므로 부가세 10%를 더해 청구하고 전자세금계산서를 발행합니다.',
               'You are in Korea, so 10% VAT is added and a Korean tax invoice is issued.'));
  } else if (q.reverseCharge) {
    out.push(L('저희는 대한민국 법인이고 귀사 국가에 세무 등록이 없어 세금을 걷지 않습니다. ' +
               '리버스 차지 대상이면 귀사에서 신고하시게 됩니다. 세금 번호를 주시면 인보이스에 찍어 드립니다.',
               'We are a Korean company with no tax registration in your country, so we add none. ' +
               'Under reverse charge you account for it. A tax number you give us goes on the invoice.'));
  } else {
    out.push(L('저희는 대한민국 법인이고 귀사 국가에 세무 등록이 없어 세금을 걷지 않습니다. ' +
               '현지 규정에 따라 신고 의무가 생길 수 있으니 세무 담당자에게 확인해 주십시오.',
               'We are a Korean company with no tax registration in your country, so we add none. ' +
               'Local rules may still put a filing duty on you - please check with your accountant.'));
  }
  if (q.estimates.length) {
    out.push('');
    out.push(L('-- 사용량 예상 (청구 아님) --', '-- Usage estimate, not billed --'));
    q.estimates.forEach(function (e) {
      out.push('  ' + e.label[ko ? 'ko' : 'en'] + ' ' + e.qty + ' x ' + A(e.unit) +
               (e.from ? L('부터', ' and up') : '') + ' = ' + A(e.amount));
    });
    out.push(L('  사용량은 쓰신 만큼 다음 달에 정산합니다.',
               '  Usage is settled next month on what you actually use.'));
  }
  out.push('');
  out.push(L('-- 사업자 정보 --', '-- Business --'));
  out.push(L('국가: ', 'Country: ') + o.country);
  out.push(L('상호: ', 'Company: ') + o.company);
  out.push(L('사업자 번호: ', 'Tax / registration no: ') + (o.bizNo || '-'));
  out.push(L('대표자: ', 'Representative: ') + (o.ceo || '-'));
  out.push(L('담당자: ', 'Contact: ') + o.contact + ' / ' + o.email + ' / ' + (o.phone || '-'));
  out.push(L('인보이스 수신: ', 'Invoice to: ') + (o.taxEmail || o.email) +
           (o.taxEmail ? '' : L(' (담당자 이메일과 동일)', ' (same as contact)')));
  return out.join(BR);
}

function lambdaOf(ko) { return (k, e) => (ko ? k : e); }

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
    country: clean(body.country).toUpperCase().slice(0, 6),
    company: clean(body.company),
    bizNo: clean(body.bizNo),
    ceo: clean(body.ceo),
    contact: clean(body.contact),
    email: clean(body.email),
    phone: clean(body.phone).replace(/[^0-9+\- ()]/g, ''),
    taxEmail: clean(body.taxEmail),
    note: clean(body.note),
    lang: clean(body.lang) === 'en' ? 'en' : 'ko'
  };

  const c = country(o.country);
  const bad = [];
  if (!c) bad.push('country');
  if (!o.company) bad.push('company');
  if (c && !taxIdOk(c, o.bizNo)) bad.push('bizNo');
  if (!o.contact) bad.push('contact');
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(o.email)) bad.push('email');
  /* 전화번호 규칙은 나라마다 다릅니다. 자리수를 세는 대신 "숫자가 몇 개
     있는가"만 봅니다. 그 이상을 검사하면 멀쩡한 번호를 거절하게 됩니다. */
  if (o.phone) {
    const digits = o.phone.replace(/[^0-9]/g, '');
    if (digits.length < 6 || digits.length > 15) bad.push('phone');
  }
  if (o.taxEmail && !/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(o.taxEmail)) bad.push('taxEmail');
  /* 전자상거래법상 필수 동의. 서버에서도 봅니다 - 화면의 체크박스는
     지우고 보낼 수 있기 때문입니다. */
  if (body.agreeTerms !== true) bad.push('agreeTerms');
  if (body.agreePrivacy !== true) bad.push('agreePrivacy');
  if (body.agreeTransfer !== true) bad.push('agreeTransfer');
  if (bad.length) return res.status(400).json({ error: 'invalid', fields: bad });

  const q = quote({
    plan: clean(body.plan), method: clean(body.method), country: o.country,
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
