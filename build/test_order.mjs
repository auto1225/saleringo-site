/* 주문·문의 API 의 전달 계층 시험.
 *
 * 금액 계산·세금 판정·주문번호 발번·중복 방지는 이제 데이터베이스가 합니다.
 * 그 규칙은 build/test_commerce.sql 이 데이터베이스에 직접 물어봅니다.
 *
 * 여기서는 그 앞에 선 API 가 할 일을 봅니다:
 *   · 화면이 보낸 값을 다듬어 넘기는가 (제어문자·길이·형)
 *   · 데이터베이스가 없거나 요금표가 안 올라와 있으면 접수하지 않는가
 *   · 데이터베이스가 돌려준 판정을 그대로 전하는가
 *   · IP 를 원본 그대로 저장하지 않는가
 *   · 알림이 실패해도 주문은 성공으로 두는가
 *
 * 네트워크를 쓰지 않습니다. fetch 를 갈아 끼워 데이터베이스 응답을 흉내 냅니다.
 *
 *     node build/test_order.mjs
 */
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
process.chdir(ROOT);

let PASS = 0;
let FAIL = 0;
const FAILURES = [];

function ok(name, cond, detail) {
  if (cond) { PASS++; return; }
  FAIL++;
  FAILURES.push(name + (detail ? '  → ' + detail : ''));
}
function eq(name, got, want) {
  ok(name, JSON.stringify(got) === JSON.stringify(want),
     'got ' + JSON.stringify(got) + ', want ' + JSON.stringify(want));
}

/* ── 데이터베이스 흉내 ──────────────────────────────────────────────────
   fetch 를 갈아 끼우고, 어떤 함수에 무엇이 왔는지 기록해 둡니다.
   그래야 "API 가 데이터베이스에 무엇을 넘겼는가" 를 볼 수 있습니다. */
const CALLS = [];
let RESPOND = {};

function installFetch() {
  globalThis.fetch = async (url, opts) => {
    const u = String(url);
    if (u.indexOf('/rest/v1/rpc/') >= 0) {
      const fn = u.split('/rest/v1/rpc/')[1];
      const body = JSON.parse(opts.body || '{}');
      CALLS.push({ fn, body });
      const canned = RESPOND[fn];
      const value = typeof canned === 'function' ? canned(body) : canned;
      if (value === undefined) return new Response('{}', { status: 200 });
      if (value instanceof Error) return new Response('boom', { status: 500 });
      return new Response(JSON.stringify(value), {
        status: 200, headers: { 'content-type': 'application/json' },
      });
    }
    /* 알림(웹훅·슬랙·Resend) — 기본은 실패시켜 둡니다. 실패해도 주문이
       살아 있어야 한다는 것이 이 설계의 요점이기 때문입니다. */
    CALLS.push({ notify: u });
    return new Response('nope', { status: 500 });
  };
}

function mockRes() {
  const r = { statusCode: 0, body: null, headers: {} };
  r.setHeader = (k, v) => { r.headers[k] = v; };
  r.status = (c) => { r.statusCode = c; return r; };
  r.json = (o) => { r.body = o; return r; };
  return r;
}

async function call(mod, method, body, headers) {
  const m = await import('../api/' + mod + '.js?t=' + Math.random());
  const req = {
    method,
    body,
    url: '/api/' + mod,
    headers: Object.assign({ 'user-agent': 'probe/1.0' }, headers || {}),
  };
  const res = mockRes();
  await m.default(req, res);
  return res;
}

function reset(responses) {
  CALLS.length = 0;
  RESPOND = responses || {};
}

const KRNO = '0010000003';    /* 국세청 검증식을 통과하는 번호 */

const GOOD = {
  plan: 'grow', method: 'transfer', country: 'KR', buyerType: 'business',
  company: '정직한마케팅', bizNo: KRNO, contact: '홍길동',
  email: 'owner@example.co.kr', billingAddress: '서울시 송파구 법원로 92',
  agreeTerms: true, agreePrivacy: true, agreeTransfer: true,
  lang: 'ko', idempotencyKey: 'probe-key-00000001',
};

const READY_OK = { ready: true, pricingVersion: 'pricing+abc', policyVersion: 'policy+def' };
const SUBMIT_OK = {
  ok: true, orderNo: 'SO-20260827-1001', state: 'received', route: 'online',
  blockers: [], receivedAt: '2026-08-27T00:00:00Z',
  quote: {
    planId: 'grow', planName: { ko: 'Grow', en: 'Grow' }, method: 'transfer',
    currency: 'KRW', taxRate: 0.1, taxTreatment: 'vat_charged', taxCollected: true,
    taxLabel: { ko: '부가세 10%', en: 'Korean VAT 10%' },
    monthly: { net: 170000, tax: 17000, total: 187000 },
    firstMonthIfToday: { net: 27419, tax: 2742, total: 30161, days: 5, monthDays: 31, asOf: '2026-08-27' },
    discount: { percent: 50, months: 3, name: { ko: '창립 고객 할인', en: 'Founding cohort' }, saves: 170000 },
    afterDiscount: { net: 340000, tax: 34000, total: 374000 },
  },
};

/* 환경변수를 시험 안에서만 켭니다. */
process.env.SUPABASE_URL = 'https://example.supabase.co';
process.env.SUPABASE_PUBLISHABLE_KEY = 'sb_publishable_probe';

installFetch();

/* ── 1. 준비 상태 ─────────────────────────────────────────────────────── */
{
  reset({ sales_readiness: READY_OK });
  const r = await call('order', 'GET');
  eq('GET: 요금표가 올라와 있으면 ready', r.body.ready, true);
  ok('  판 번호를 함께 알려 준다', r.body.pricingVersion === 'pricing+abc');
  eq('  캐시하지 않는다', r.headers['Cache-Control'], 'no-store');

  reset({ sales_readiness: { ready: false }, sales_refresh: { ok: false, error: 'policy_fetch' } });
  const r2 = await call('order', 'GET');
  eq('GET: 요금표가 없으면 ready 가 아니다', r2.body.ready, false);
  ok('  왜 아닌지 알려 준다', typeof r2.body.reason === 'string');
}

/* 요금표가 없으면 데이터베이스가 사이트에서 다시 읽어 오게 한 번 시켜 본다 */
{
  reset({
    sales_readiness: (() => { let n = 0; return () => (++n === 1 ? { ready: false } : READY_OK); })(),
    sales_refresh: { ok: true },
  });
  const r = await call('order', 'GET');
  eq('요금표가 없으면 스스로 다시 읽어 온다', r.body.ready, true);
  ok('  실제로 refresh 를 불렀다', CALLS.some((c) => c.fn === 'sales_refresh'));
}

/* ── 2. 접수 ──────────────────────────────────────────────────────────── */
{
  reset({ sales_readiness: READY_OK, sales_submit_order: SUBMIT_OK });
  const r = await call('order', 'POST', GOOD, { 'x-forwarded-for': '203.0.113.9, 10.0.0.1' });
  eq('접수 → 200', r.statusCode, 200);
  eq('  주문번호를 그대로 전한다', r.body.orderNo, 'SO-20260827-1001');
  eq('  저장되었다고 알린다', r.body.stored, true);
  eq('  알림이 다 실패해도 주문은 성공이다', r.body.ok, true);
  eq('  알림은 실패했다고 정직하게 말한다', r.body.notified, false);

  const sent = CALLS.find((c) => c.fn === 'sales_submit_order').body.p;
  ok('  IP 를 원본 그대로 보내지 않는다',
     sent.ipHash && sent.ipHash.indexOf('203.0.113.9') < 0, JSON.stringify(sent.ipHash));
  ok('  IP 해시는 16진수다', /^[0-9a-f]{32}$/.test(sent.ipHash), sent.ipHash);
  eq('  동의를 문자열로 정규화해 넘긴다', sent.consent.terms, 'true');
  eq('  안 받은 동의는 false 로 넘긴다', sent.consent.marketing, 'false');
  ok('  화면이 보낸 금액은 넘기지 않는다',
     !('monthly' in sent) && !('total' in sent) && !('price' in sent));
}

/* ── 3. 데이터베이스가 준비되지 않았으면 접수하지 않는다 ───────────────── */
{
  reset({ sales_readiness: { ready: false }, sales_refresh: { ok: false }, sales_submit_order: SUBMIT_OK });
  const r = await call('order', 'POST', GOOD);
  eq('요금표가 없으면 접수하지 않는다', r.statusCode, 503);
  ok('  submit 을 부르지도 않는다', !CALLS.some((c) => c.fn === 'sales_submit_order'));
}

{
  const url = process.env.SUPABASE_URL;
  delete process.env.SUPABASE_URL;
  reset({});
  const r = await call('order', 'POST', GOOD);
  eq('데이터베이스가 설정되지 않으면 접수하지 않는다', r.statusCode, 503);
  const g = await call('order', 'GET');
  eq('  GET 도 ready 가 아니라고 답한다', g.body.ready, false);
  eq('  이유를 말한다', g.body.reason, 'db_unconfigured');
  process.env.SUPABASE_URL = url;
}

/* ── 4. 데이터베이스의 판정을 그대로 전한다 ─────────────────────────────── */
{
  reset({
    sales_readiness: READY_OK,
    sales_submit_order: { ok: false, error: 'invalid', fields: ['agreeTransfer'] },
  });
  const r = await call('order', 'POST', GOOD);
  eq('동의가 빠지면 400', r.statusCode, 400);
  eq('  어느 항목인지 전한다', r.body.fields, ['agreeTransfer']);

  reset({ sales_readiness: READY_OK, sales_submit_order: { ok: false, error: 'rate_limited' } });
  eq('유량 제한 → 429', (await call('order', 'POST', GOOD)).statusCode, 429);

  reset({ sales_readiness: READY_OK, sales_submit_order: { ok: false, error: 'busy' } });
  eq('전체가 몰리면 → 429', (await call('order', 'POST', GOOD)).statusCode, 429);

  reset({ sales_readiness: READY_OK, sales_submit_order: new Error('down') });
  const r5 = await call('order', 'POST', GOOD);
  eq('데이터베이스 오류 → 502', r5.statusCode, 502);
  ok('  "접수되었습니다" 라고 말하지 않는다', !r5.body.ok);
}

/* ── 5. 서면 주문으로 넘어가는 경우 ─────────────────────────────────────── */
{
  const proposal = Object.assign({}, SUBMIT_OK, {
    state: 'under_review', route: 'proposal',
    blockers: [{ code: 'voice_unavailable', ko: '전화 회선이 없습니다', en: 'No voice line' }],
  });
  reset({ sales_readiness: READY_OK, sales_submit_order: proposal });
  const r = await call('order', 'POST', Object.assign({}, GOOD, { country: 'FR', plan: 'scale' }));
  eq('전화가 없는 나라 → 접수는 된다', r.statusCode, 200);
  eq('  서면 주문 경로라고 알려 준다', r.body.route, 'proposal');
  eq('  상태는 검토 중이다', r.body.state, 'under_review');
  ok('  왜 그런지 이유를 함께 준다', r.body.blockers.length === 1);
}

/* ── 6. 같은 주문을 두 번 눌러도 ───────────────────────────────────────── */
{
  reset({
    sales_readiness: READY_OK,
    sales_submit_order: Object.assign({}, SUBMIT_OK, { duplicate: true }),
  });
  const r = await call('order', 'POST', GOOD);
  eq('중복 제출 → 같은 번호', r.body.orderNo, 'SO-20260827-1001');
  eq('  중복이라고 알려 준다', r.body.duplicate, true);
}

/* ── 7. 입력 다듬기 ───────────────────────────────────────────────────── */
{
  reset({ sales_readiness: READY_OK, sales_submit_order: SUBMIT_OK });
  await call('order', 'POST', Object.assign({}, GOOD, {
    country: '  kr  ',
    company: 'A' + String.fromCharCode(0) + 'B',
    note: 'x'.repeat(9000),
    voiceMinutes: -50,
    alimtalk: 99999999,
    phone: '010-1234-5678<script>',
  }));
  const sent = CALLS.find((c) => c.fn === 'sales_submit_order').body.p;
  eq('  나라는 대문자로 다듬는다', sent.country, 'KR');
  ok('  제어문자를 걷어 낸다', sent.company.indexOf(String.fromCharCode(0)) < 0, sent.company);
  ok('  지나치게 긴 값은 자른다', sent.note.length <= 4000, String(sent.note.length));
  eq('  음수 사용량은 0 으로', sent.voiceMinutes, 0);
  eq('  터무니없는 사용량은 상한으로', sent.alimtalk, 1000000);
  ok('  전화번호에서 이상한 글자를 걷어 낸다',
     !/[<>a-z]/i.test(sent.phone), sent.phone);
}

/* ── 8. 함정 칸 ───────────────────────────────────────────────────────── */
{
  reset({
    sales_readiness: READY_OK,
    sales_submit_order: { ok: true, orderNo: 'IGNORED', ignored: true },
  });
  const r = await call('order', 'POST', Object.assign({}, GOOD, { company_website_hp: 'bot' }));
  eq('함정 칸이 채워지면 조용히 성공을 돌려준다', r.statusCode, 200);
  const sent = CALLS.find((c) => c.fn === 'sales_submit_order').body.p;
  eq('  함정 값을 데이터베이스까지 넘겨 판단하게 한다', sent.company_website_hp, 'bot');
}

/* ── 9. 메서드 ────────────────────────────────────────────────────────── */
{
  reset({ sales_readiness: READY_OK });
  const r = await call('order', 'PUT', GOOD);
  eq('PUT → 405', r.statusCode, 405);
  eq('  무엇이 되는지 알려 준다', r.headers.Allow, 'GET, POST');
}

/* ── 10. 문의 ─────────────────────────────────────────────────────────── */
{
  reset({ sales_submit_lead: { ok: true, ref: 'IN-20260827-AB12E' } });
  const r = await call('lead', 'POST', {
    name: '김대표', email: 'hi@example.com', company: '예시상사',
    message: '도입 문의드립니다', lang: 'ko',
  }, { 'x-forwarded-for': '198.51.100.7' });
  eq('문의 접수 → 200', r.statusCode, 200);
  eq('  참조번호를 준다', r.body.ref, 'IN-20260827-AB12E');
  eq('  저장되었다고 알린다', r.body.stored, true);
  const sent = CALLS.find((c) => c.fn === 'sales_submit_lead').body.p;
  ok('  문의도 IP 를 원본으로 넘기지 않는다',
     sent.ipHash && sent.ipHash.indexOf('198.51.100.7') < 0);

  reset({ sales_submit_lead: { ok: false, error: 'invalid', fields: ['email'] } });
  const r2 = await call('lead', 'POST', { email: 'not-an-email' });
  eq('잘못된 이메일 → 400', r2.statusCode, 400);

  reset({});
  const g = await call('lead', 'GET');
  eq('문의 GET: 데이터베이스가 있으면 ready', g.body.ready, true);
}

/* ── 11. 주문 조회 ────────────────────────────────────────────────────── */
{
  reset({ sales_order_status: { ok: true, orderNo: 'SO-20260827-1001', state: 'received' } });
  const r = await call('order-status', 'POST', {
    orderNo: 'so-20260827-1001', email: 'Owner@Example.co.kr',
  });
  eq('조회 → 200', r.statusCode, 200);
  const sent = CALLS.find((c) => c.fn === 'sales_order_status').body;
  eq('  번호는 대문자로', sent.p_order_no, 'SO-20260827-1001');
  eq('  이메일은 소문자로', sent.p_email, 'owner@example.co.kr');

  reset({});
  eq('번호 형식이 틀리면 400',
     (await call('order-status', 'POST', { orderNo: '1234', email: 'a@b.co' })).statusCode, 400);
  eq('이메일이 없으면 400',
     (await call('order-status', 'POST', { orderNo: 'SO-20260827-1001', email: '' })).statusCode, 400);

  reset({ sales_order_status: { ok: false, error: 'not_found' } });
  const nf = await call('order-status', 'POST', {
    orderNo: 'SO-20260827-9999', email: 'a@b.co',
  });
  eq('없는 주문 → 404', nf.statusCode, 404);
  ok('  있는지 없는지 구분해 알려 주지 않는다',
     !JSON.stringify(nf.body).includes('email'), JSON.stringify(nf.body));
}

/* ── 12. 견적 ─────────────────────────────────────────────────────────── */
{
  reset({ sales_quote: { currency: 'USD', commerce: { orderable: false, blockers: [{ code: 'x' }] } } });
  const r = await call('quote', 'POST', { country: 'FR', plan: 'scale', buyerType: 'business' });
  eq('견적 → 200', r.statusCode, 200);
  eq('  서버 판정을 그대로 전한다', r.body.commerce.orderable, false);
  ok('  아무것도 저장하지 않는다', !CALLS.some((c) => c.fn === 'sales_submit_order'));

  reset({ sales_quote: { error: 'no_pricing' } });
  eq('요금표가 없으면 503', (await call('quote', 'POST', { country: 'KR', plan: 'grow' })).statusCode, 503);
}

/* ── 결과 ─────────────────────────────────────────────────────────────── */
console.log('');
if (FAIL) {
  for (const f of FAILURES) console.log('  ✕ ' + f);
  console.log('');
  console.log('통과 ' + PASS + ', 실패 ' + FAIL);
  process.exit(1);
}
console.log('통과 ' + PASS + ', 실패 0');
console.log('API 전달 계층은 위 ' + PASS + '가지 상황에서 모두 옳게 답합니다.');
console.log('상거래 규칙 자체는 build/test_commerce.sql 이 데이터베이스에 직접 물어봅니다.');
