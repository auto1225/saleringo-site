/* ── 주문 접수의 시험대 ────────────────────────────────────────────────────
   구매 경로는 이 사이트에서 유일하게 "틀리면 돈 문제가 되는" 코드입니다.
   그래서 브라우저로 눌러 보는 것과 별개로, 서버가 어떤 입력에도 옳게
   답하는지를 여기서 기계적으로 확인합니다.

   특히 확인하는 것:
     · 브라우저가 보낸 금액을 서버가 절대 쓰지 않는다
     · 사업자등록번호를 자리수가 아니라 검증식으로 본다
     · 법정 필수 동의가 빠지면 접수되지 않는다 (화면의 체크박스는 지울 수 있다)
     · 같은 주문을 두 번 눌러도 주문은 하나다
     · 어디에도 저장되지 않으면 성공이라고 답하지 않는다

     node build/test_order.mjs
*/
import http from 'http';

const ROOT = process.cwd();
let PASS = 0, FAIL = 0;
const FAILURES = [];

function ok(name, cond, detail) {
  if (cond) { PASS++; return; }
  FAIL++; FAILURES.push(name + (detail ? '  → ' + detail : ''));
}
function eq(name, got, want) {
  ok(name, JSON.stringify(got) === JSON.stringify(want),
     'got ' + JSON.stringify(got) + ', want ' + JSON.stringify(want));
}

/* 주문이 실제로 도착했는지 보려면 받아 줄 곳이 있어야 한다 */
const received = [];
const sink = http.createServer((req, res) => {
  let b = '';
  req.on('data', c => { b += c; });
  req.on('end', () => {
    try { received.push(JSON.parse(b)); } catch (e) { received.push({ raw: b }); }
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end('{"ok":true}');
  });
});
await new Promise(r => sink.listen(0, '127.0.0.1', r));
const SINK = 'http://127.0.0.1:' + sink.address().port + '/hook';

function mockRes() {
  const r = { statusCode: 0, body: null, headers: {} };
  r.setHeader = (k, v) => { r.headers[k] = v; };
  r.status = c => { r.statusCode = c; return r; };
  r.json = o => { r.body = o; return r; };
  return r;
}

async function call(method, body, headers) {
  const mod = await import('../api/order.js?t=' + Math.random());
  const req = { method, body, headers: headers || {} };
  const res = mockRes();
  await mod.default(req, res);
  return res;
}

const GOOD = {
  plan: 'grow', method: 'transfer', country: 'KR',
  company: '정직한마케팅', bizNo: '220-88-01001',   /* 체크섬이 맞는 번호 */
  contact: '홍길동', email: 'owner@example.co.kr',
  agreeTerms: true, agreePrivacy: true, agreeTransfer: true,
  lang: 'ko'
};

/* 검증식을 만족하는 번호를 하나 만들어 둔다 — 시험이 특정 실제 회사의
   번호에 기대지 않도록 */
function makeBizNo() {
  const w = [1, 3, 7, 1, 3, 7, 1, 3, 5];
  for (let seed = 1000000; seed < 1000200; seed++) {
    const n9 = String(seed).padStart(9, '0');
    let sum = 0;
    for (let i = 0; i < 9; i++) sum += Number(n9[i]) * w[i];
    sum += Math.floor((Number(n9[8]) * 5) / 10);
    const check = (10 - (sum % 10)) % 10;
    return n9 + check;
  }
}
GOOD.bizNo = makeBizNo();

process.env.ORDER_WEBHOOK_URL = SINK;
delete process.env.RESEND_API_KEY;
delete process.env.SLACK_WEBHOOK_URL;
delete process.env.PAYMENT_PROVIDER;

console.log('사업자등록번호 시험값:', GOOD.bizNo);

/* ── 1. 상태 조회 ───────────────────────────────────────────────────── */
{
  const r = await call('GET');
  ok('GET 200', r.statusCode === 200);
  ok('GET ready=true (수신처가 있으므로)', r.body.ready === true, JSON.stringify(r.body));
  eq('GET payment=null (결제사 미설정)', r.body.payment, null);
}

/* ── 2. 수신처가 없으면 성공이라 말하지 않는다 ──────────────────────── */
{
  const keep = process.env.ORDER_WEBHOOK_URL;
  delete process.env.ORDER_WEBHOOK_URL;
  const r = await call('POST', { ...GOOD });
  eq('수신처 없음 → 503', r.statusCode, 503);
  eq('  이유를 밝힌다', r.body.error, 'no_destination_configured');
  process.env.ORDER_WEBHOOK_URL = keep;
}

/* ── 3. 정상 주문 ───────────────────────────────────────────────────── */
{
  received.length = 0;
  const r = await call('POST', { ...GOOD });
  eq('정상 주문 → 200', r.statusCode, 200);
  ok('주문번호가 SO- 로 시작', /^SO-\d{8}-[A-Z0-9]{4}$/.test(r.body.orderNo || ''), r.body.orderNo);
  eq('결제사 없으면 상태는 접수', r.body.status, 'received');
  ok('주문이 실제로 수신처에 도착', received.length === 1, '도착 ' + received.length + '건');
  ok('도착한 기록에 금액이 들어 있다', received[0] && received[0].quote &&
     received[0].quote.monthly && received[0].quote.monthly.total > 0);
}

/* ── 4. 금액은 서버가 다시 계산한다 ─────────────────────────────────── */
{
  received.length = 0;
  /* 브라우저가 "1원만 내겠다"고 우겨도 서버는 듣지 않는다 */
  const r = await call('POST', {
    ...GOOD, total: 1, dueNow: 1, amount: 1, price: 1,
    quote: { dueNow: { total: 1 } }
  });
  eq('금액을 위조해도 200', r.statusCode, 200);
  const q = r.body.quote;
  const honest = (await call('POST', { ...GOOD })).body.quote;
  ok('서버가 계산한 금액이 위조값(1원)을 무시한다',
     q.monthly.total === honest.monthly.total && q.monthly.total > 1,
     q.monthly.total + ' vs ' + honest.monthly.total);
  ok('한국은 부가세가 공급가액의 10%', q.monthly.tax === Math.round(q.monthly.net * 0.1),
     q.monthly.net + ' / ' + q.monthly.tax);
  ok('합계 = 공급가액 + 세금', q.monthly.total === q.monthly.net + q.monthly.tax);
}

/* ── 5. 사업자등록번호 ──────────────────────────────────────────────── */
{
  const cases = [
    ['빈 값', '', false], ['9자리', '12345678', false], ['11자리', '12345678901', false],
    ['체크섬 틀림', '123-45-67890', false], ['글자 섞임', 'abc-de-fghij', false],
    ['하이픈 있는 정상', GOOD.bizNo.slice(0, 3) + '-' + GOOD.bizNo.slice(3, 5) + '-' + GOOD.bizNo.slice(5), true],
    ['하이픈 없는 정상', GOOD.bizNo, true]
  ];
  for (const [label, val, want] of cases) {
    const r = await call('POST', { ...GOOD, bizNo: val });
    const accepted = r.statusCode === 200;
    ok('사업자번호 ' + label + ' → ' + (want ? '통과' : '거절'), accepted === want,
       'status ' + r.statusCode + ' ' + JSON.stringify(r.body.fields || ''));
  }
}

/* ── 6. 법정 필수 동의 ──────────────────────────────────────────────── */
{
  for (const k of ['agreeTerms', 'agreePrivacy', 'agreeTransfer']) {
    const body = { ...GOOD }; delete body[k];
    const r = await call('POST', body);
    eq(k + ' 없으면 400', r.statusCode, 400);
    ok('  어느 항목인지 알려 준다', (r.body.fields || []).includes(k),
       JSON.stringify(r.body.fields));
  }
  /* 체크박스는 지우고 보낼 수 있으므로 문자열 'true' 도 막는다 */
  const r = await call('POST', { ...GOOD, agreeTerms: 'true' });
  eq('동의를 문자열로 위조 → 400', r.statusCode, 400);
}

/* ── 7. 정기결제 동의는 카드일 때만 필수 ────────────────────────────── */
{
  const a = await call('POST', { ...GOOD, method: 'card' });
  eq('카드인데 정기결제 미동의 → 400', a.statusCode, 400);
  ok('  어느 항목인지 알려 준다', (a.body.fields || []).includes('agreeRecurring'));
  const b = await call('POST', { ...GOOD, method: 'card', agreeRecurring: true });
  eq('카드 + 정기결제 동의 → 200', b.statusCode, 200);
  const c = await call('POST', { ...GOOD, method: 'transfer' });
  eq('계좌이체는 정기결제 동의가 필요 없다', c.statusCode, 200);
}

/* ── 8. 나머지 입력 검증 ────────────────────────────────────────────── */
{
  const bad = [
    ['상호 없음', { company: '' }, 'company'],
    ['담당자 없음', { contact: '' }, 'contact'],
    ['이메일 형식', { email: 'not-an-email' }, 'email'],
    ['이메일 빈 값', { email: '' }, 'email'],
    ['세금계산서 이메일 형식', { taxEmail: 'nope' }, 'taxEmail'],
    ['전화번호가 숫자 몇 개뿐', { phone: '12' }, 'phone']
  ];
  for (const [label, patch, field] of bad) {
    const r = await call('POST', { ...GOOD, ...patch });
    eq(label + ' → 400', r.statusCode, 400);
    ok('  ' + field + ' 를 지목', (r.body.fields || []).includes(field),
       JSON.stringify(r.body.fields));
  }
  for (const [label, ph] of [['한국 형식', '010-1234-5678'],
                             ['미국 형식', '+1 (415) 555-0100'],
                             ['독일 형식', '+49 30 901820'],
                             ['공백만 있는 국제 형식', '+44 20 7946 0958']]) {
    const r = await call('POST', { ...GOOD, country: 'US', phone: ph });
    eq(label + ' 전화번호는 통과', r.statusCode, 200);
  }
}

/* ── 9. 요금제와 결제수단 ───────────────────────────────────────────── */
{
  const r = await call('POST', { ...GOOD, plan: 'enterprise' });
  eq('없는 요금제 → 400', r.statusCode, 400);
  eq('  이유', r.body.error, 'plan_unknown');
  const m = await call('POST', { ...GOOD, method: 'bitcoin' });
  eq('없는 결제수단 → 400', m.statusCode, 400);
  eq('  이유', m.body.error, 'method_unknown');

  for (const [plan, monthly] of [['start', 110000], ['grow', 340000], ['scale', 820000]]) {
    const q = (await call('POST', { ...GOOD, plan })).body.quote;
    ok(plan + ' 정가가 요금표와 같다', q.listPrice === monthly,
       q.listPrice + ' vs ' + monthly);
    /* 창립 할인이 켜져 있으면 실제 청구액은 정가의 절반이다. 영문 약관
       제2조가 "가입 시 확정"이라고 약속한 것이라, 주문서가 정가만 보여
       주면 그 약관을 어기는 셈이 된다. */
    if (q.discount) {
      ok(plan + ' 할인이 정가에 적용된다',
         q.monthly.net === Math.round(monthly * (100 - q.discount.percent) / 100),
         q.monthly.net + ' vs ' + monthly);
    }
  }
}

/* ── 10. 사용량은 첫 청구서에 들어가지 않는다 ───────────────────────── */
{
  const q = (await call('POST', { ...GOOD, plan: 'scale', voiceMinutes: 600 })).body.quote;
  const planOnly = (await call('POST', { ...GOOD, plan: 'scale' })).body.quote;
  ok('통화 예상이 있어도 월 정액은 그대로', q.monthly.total === planOnly.monthly.total,
     q.monthly.total + ' vs ' + planOnly.monthly.total);
  ok('통화 예상이 별도로 잡힌다', q.estimates.length === 1 && q.estimates[0].amount === 600 * 190,
     JSON.stringify(q.estimates));
  const noVoice = (await call('POST', { ...GOOD, plan: 'start', voiceMinutes: 600 })).body.quote;
  ok('전화 없는 요금제에서는 통화 예상이 무시된다',
     !noVoice.estimates.some(e => e.id === 'voiceMinutes'), JSON.stringify(noVoice.estimates));
  const neg = (await call('POST', { ...GOOD, plan: 'scale', voiceMinutes: -5000 })).body.quote;
  ok('음수 통화 시간으로 금액을 깎을 수 없다',
     !neg.estimates.some(e => e.amount < 0), JSON.stringify(neg.estimates));
}

/* ── 11. 같은 주문을 두 번 눌러도 하나 ──────────────────────────────── */
{
  /* (가) 같은 인스턴스 안에서는 두 번째가 수신처로 가지 않는다 */
  received.length = 0;
  const mod = await import('../api/order.js?idem=' + Math.random());
  const key = 'test-idem-' + Date.now();
  const one = mockRes(), two = mockRes();
  await mod.default({ method: 'POST', body: { ...GOOD, idempotencyKey: key }, headers: {} }, one);
  await mod.default({ method: 'POST', body: { ...GOOD, idempotencyKey: key }, headers: {} }, two);
  eq('두 번째도 200', two.statusCode, 200);
  eq('  같은 주문번호를 돌려준다', two.body.orderNo, one.body.orderNo);
  ok('  수신처에는 한 번만 갔다', received.length === 1, '도착 ' + received.length + '건');

  /* (나) 인스턴스가 달라도 번호는 같다. Vercel 에서 실제로 일어나는 상황이고,
     메모리 기억은 여기서 아무 도움이 안 된다. 번호가 같아야 받는 쪽이 합친다. */
  const c = await call('POST', { ...GOOD, idempotencyKey: key });
  eq('다른 인스턴스에서도 같은 주문번호', c.body.orderNo, one.body.orderNo);

  /* (다) 키가 다르면 번호도 달라야 한다 */
  const d = await call('POST', { ...GOOD, idempotencyKey: key + '-other' });
  ok('키가 다르면 번호도 다르다', d.body.orderNo !== one.body.orderNo,
     d.body.orderNo + ' vs ' + one.body.orderNo);
}

/* ── 12. 봇 ─────────────────────────────────────────────────────────── */
{
  received.length = 0;
  const r = await call('POST', { ...GOOD, company_website_hp: 'http://spam' });
  eq('허니팟 → 겉으로는 200', r.statusCode, 200);
  ok('  실제로는 아무 데도 가지 않는다', received.length === 0, '도착 ' + received.length + '건');
}

/* ── 13. 잘못된 요청 ────────────────────────────────────────────────── */
{
  eq('GET/POST 외 → 405', (await call('DELETE', {})).statusCode, 405);
  eq('본문 없음 → 400', (await call('POST', null)).statusCode, 400);
  eq('본문이 문자열 쓰레기 → 400', (await call('POST', 'not json')).statusCode, 400);
  const s = await call('POST', JSON.stringify(GOOD));
  eq('본문이 JSON 문자열이면 파싱한다', s.statusCode, 200);
}

/* ── 14. 과도한 요청 ────────────────────────────────────────────────── */
{
  const mod = await import('../api/order.js?rate=' + Math.random());
  const h = { 'x-forwarded-for': '203.0.113.9' };
  let last = 0;
  for (let i = 0; i < 8; i++) {
    const res = mockRes();
    await mod.default({ method: 'POST', body: { ...GOOD }, headers: h }, res);
    last = res.statusCode;
  }
  eq('같은 IP 에서 몰아치면 429', last, 429);
}

/* ── 15. 첫 달 일할계산 ─────────────────────────────────────────────── */
{
  const q = (await call('POST', { ...GOOD, plan: 'start' })).body.quote;
  const f = q.firstMonthIfToday;
  ok('남은 날이 이번 달 안에 있다', f.days >= 1 && f.days <= f.monthDays, JSON.stringify(f));
  const expect = Math.round(q.monthly.net * f.days / f.monthDays);
  ok('첫 달 예시 = 실제 월 청구액 × 남은날/이번달', f.net === expect, f.net + ' vs ' + expect);
  ok('첫 달 예시는 한 달치를 넘지 않는다', f.net <= q.monthly.net);
  ok('기준일이 서울 날짜로 찍혀 있다', /^\d{4}-\d{2}-\d{2}$/.test(f.asOf || ''), f.asOf);
  /* 화면이 보여준 금액과 서버가 기록하는 금액이 같아야 한다.
     예전에는 화면이 로컬시간, 서버가 UTC 라서 아침마다 하루씩 어긋났다. */
  const seoul = new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Seoul' }).format(new Date());
  ok('서버의 기준일이 서울의 오늘과 같다', f.asOf === seoul, f.asOf + ' vs ' + seoul);
}

/* ── 16. 긴 입력으로 밀어 넣기 ──────────────────────────────────────── */
{
  const r = await call('POST', { ...GOOD, note: 'x'.repeat(50000), company: 'y'.repeat(5000) });
  eq('아주 긴 입력도 200 (잘라서 받는다)', r.statusCode, 200);
  const last = received[received.length - 1];
  ok('  잘라서 저장한다', last && last.note.length <= 400 && last.company.length <= 400,
     last ? last.note.length + '/' + last.company.length : '없음');
  const ctrl = await call('POST', { ...GOOD, company: 'A B\nC' });
  const rec = received[received.length - 1];
  ok('  제어문자를 제거한다', rec && !/[ -]/.test(rec.company), JSON.stringify(rec && rec.company));
}


/* ── 17. 나라가 통화와 세금을 정한다 ────────────────────────────────── */
{
  const kr = (await call('POST', { ...GOOD, country: 'KR', plan: 'scale' })).body.quote;
  eq('한국은 원화', kr.currency, 'KRW');
  ok('한국은 세금을 걷는다', kr.taxCollected === true);
  ok('한국 Scale 정가 820,000', kr.listPrice === 820000, String(kr.listPrice));
  ok('한국 합계 = 청구액 + 10%',
     kr.monthly.total === kr.monthly.net + Math.round(kr.monthly.net * 0.1),
     String(kr.monthly.total));

  const us = (await call('POST', { ...GOOD, country: 'US', plan: 'scale', bizNo: '' })).body.quote;
  eq('미국은 달러', us.currency, 'USD');
  ok('미국은 세금을 걷지 않는다', us.taxCollected === false);
  ok('미국 Scale 정가 599', us.listPrice === 599, String(us.listPrice));
  ok('미국은 합계에 세금이 붙지 않는다', us.monthly.total === us.monthly.net,
     String(us.monthly.total));
  ok('미국은 리버스 차지가 아니다', us.reverseCharge === false);

  const de = (await call('POST', { ...GOOD, country: 'DE', plan: 'grow', bizNo: '' })).body.quote;
  ok('독일은 리버스 차지로 표시된다', de.reverseCharge === true);
  ok('독일도 세금을 걷지 않는다', de.taxCollected === false);
  ok('독일 Grow 정가 249', de.listPrice === 249, String(de.listPrice));

  const r = await call('POST', { ...GOOD, country: 'ZZ' });
  eq('없는 나라 → 400', r.statusCode, 400);
  eq('  이유', r.body.error, 'invalid');
  ok('  country 를 지목', (r.body.fields || []).includes('country'));

  const none = await call('POST', { ...GOOD, country: '' });
  eq('나라 없음 → 400', none.statusCode, 400);
}

/* ── 18. 사업자 번호는 나라가 정한다 ─────────────────────────────────── */
{
  /* 한국: 필수 + 체크섬 */
  const a = await call('POST', { ...GOOD, country: 'KR', bizNo: '' });
  eq('한국은 번호가 없으면 400', a.statusCode, 400);
  ok('  bizNo 를 지목', (a.body.fields || []).includes('bizNo'));
  const b = await call('POST', { ...GOOD, country: 'KR', bizNo: '1234567890' });
  eq('한국은 체크섬이 틀리면 400', b.statusCode, 400);

  /* 그 밖의 나라: 선택, 형식만 */
  for (const code of ['US', 'GB', 'DE', 'AU', 'SG', 'JP', 'BR', 'OTHER']) {
    const empty = await call('POST', { ...GOOD, country: code, bizNo: '' });
    eq(code + ' 는 번호 없이도 주문된다', empty.statusCode, 200);
  }
  const vat = await call('POST', { ...GOOD, country: 'DE', bizNo: 'DE123456789' });
  eq('독일 VAT 번호는 그대로 통과', vat.statusCode, 200);
  const abn = await call('POST', { ...GOOD, country: 'AU', bizNo: '51 824 753 556' });
  eq('공백 있는 ABN 도 통과', abn.statusCode, 200);
  const junk = await call('POST', { ...GOOD, country: 'US', bizNo: '<script>' });
  eq('이상한 문자열은 거절', junk.statusCode, 400);
  /* 한국 체크섬을 다른 나라에 강요하지 않는다 - 이것이 글로벌 판매를
     막고 있던 바로 그 규칙이었다 */
  const krNumInUS = await call('POST', { ...GOOD, country: 'US', bizNo: '1234567890' });
  eq('미국 구매자에게 한국 체크섬을 요구하지 않는다', krNumInUS.statusCode, 200);
}

/* ── 19. 금액 표기 ──────────────────────────────────────────────────── */
{
  const us = (await call('POST', { ...GOOD, country: 'US', plan: 'scale',
                                   bizNo: '', voiceMinutes: 1000 })).body.quote;
  const v = us.estimates.find(e => e.id === 'voiceMinutes');
  ok('달러 통화료는 소수점 둘째 자리까지', v && v.unit === 0.14, JSON.stringify(v));
  ok('1000분 = 140 달러', v && v.amount === 140, JSON.stringify(v));
  const kr = (await call('POST', { ...GOOD, country: 'KR', plan: 'scale',
                                   voiceMinutes: 1000 })).body.quote;
  const kv = kr.estimates.find(e => e.id === 'voiceMinutes');
  ok('원화 통화료는 1000분 = 190,000원', kv && kv.amount === 190000, JSON.stringify(kv));
}

sink.close();

console.log('');
console.log('통과 %d, 실패 %d', PASS, FAIL);
if (FAILURES.length) {
  console.log('');
  FAILURES.forEach(f => console.log('  ✕ ' + f));
  process.exit(1);
}
console.log('주문 접수는 위 %d가지 상황에서 모두 옳게 답합니다.', PASS);
