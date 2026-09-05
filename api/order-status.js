/* 접수한 주문을 다시 열어 보는 창구.
 *
 * 예전에는 주문 성공 화면이 새로고침하면 사라졌고, 주문번호를 다시
 * 조회할 곳이 없었습니다. 메일이 안 왔거나 지웠으면 자기가 무엇을
 * 주문했는지 확인할 방법이 없었습니다.
 *
 * 주문번호만으로는 열리지 않습니다. 접수할 때 쓴 이메일이 함께 맞아야
 * 합니다. 남의 주문 내용이 번호를 찍어 보는 것만으로 열리면 안 됩니다.
 */
import { rpc, dbConfigured } from './_db.js';

const CTRL = new RegExp('[\\u0000-\\u001f\\u007f]', 'g');

function clean(v, limit) {
  return String(v == null ? '' : v)
    .replace(CTRL, ' ')
    .trim()
    .slice(0, limit || 200);
}

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');

  if (req.method !== 'GET' && req.method !== 'POST') {
    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ error: 'method_not_allowed' });
  }
  if (!dbConfigured()) return res.status(503).json({ error: 'db_unconfigured' });

  let src = {};
  if (req.method === 'POST') {
    let body = req.body;
    if (typeof body === 'string') {
      try {
        body = JSON.parse(body);
      } catch (e) {
        body = null;
      }
    }
    src = body && typeof body === 'object' ? body : {};
  } else {
    /* 주소창에 이메일이 남는 것을 원치 않는 분이 많습니다. GET 도 받되,
       화면에서는 POST 를 씁니다. */
    const url = new URL(req.url, 'https://claude.saleringo.com');
    // 사이트는 ?no= 를 쓰지만, 안내 문서나 메일이 ?orderNo= 라고 쓸 수 있습니다.
    src = { orderNo: url.searchParams.get('no') || url.searchParams.get('orderNo'),
            email: url.searchParams.get('email') };
  }

  const orderNo = clean(src.orderNo, 40).toUpperCase();
  const email = clean(src.email, 200).toLowerCase();

  const bad = [];
  if (!/^SO-\d{8}-\d{4}$/.test(orderNo)) bad.push('orderNo');
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email)) bad.push('email');
  if (bad.length) return res.status(400).json({ error: 'invalid', fields: bad });

  const r = await rpc('sales_order_status', { p_order_no: orderNo, p_email: email });

  if (!r || r.ok !== true) {
    const code = r && r.error;
    if (code === 'rate_limited' || code === 'busy') return res.status(429).json({ error: 'too_many' });
    /* 있는데 이메일이 틀린 것과 아예 없는 것을 구분해 알려 주지 않습니다.
       구분해 주면 어떤 번호가 실재하는지 훑어볼 수 있게 됩니다. */
    if (code === 'not_found') return res.status(404).json({ error: 'not_found' });
    if (code && code.startsWith('db_')) return res.status(502).json({ error: 'lookup_failed' });
    return res.status(400).json({ error: code || 'invalid' });
  }

  /* 개통 단계. 결제 뒤에 무엇이 어디까지 됐는지 — 번호 배정, 착신 검증, 채널,
     테스트 통화, 개통 게이트. 같은 번호·이메일 검증을 다시 거치는 함수라서
     주문 내용이 열린 사람에게만 열립니다. 함수가 아직 없거나 실패하면
     주문 내용은 그대로 보여 주고 개통 단계만 비웁니다. */
  try {
    const p = await rpc('sales_provisioning_status', { p_order_no: orderNo, p_email: email });
    r.provisioning = p && p.ok === true && Array.isArray(p.jobs) ? p.jobs : [];
    if (p && p.ok === true && p.tenant) r.tenant = p.tenant;
  } catch (e) {
    r.provisioning = [];
  }

  return res.status(200).json(r);
}
