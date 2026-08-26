/* 서버가 판정한 금액과 거래 조건.
 *
 * 예전에는 화면이 혼자 계산했습니다. 그래서 화면은 "독일에서도 Scale
 * $599 주문 가능, 세금 0" 이라고 말할 수 있었고, 실제로 그렇게 말했습니다.
 * VAT 번호가 없어도 리버스 차지라고 적었고, 전화 회선이 없는 나라에서도
 * AI 전화가 든 요금제를 그대로 팔았습니다.
 *
 * 이제 화면은 무엇을 골랐는지만 보내고, 판정은 서버가 합니다.
 *   · 통화        나라로 정합니다
 *   · 세금 처리   나라 + 구매자 유형 + 세금번호로 정합니다
 *   · 전화 가용성 나라로 정합니다
 *   · 온라인 주문 가능 여부  위 셋이 전부 확정될 때만 참입니다
 *
 * 아무것도 저장하지 않습니다. 저장은 /api/order 가 합니다.
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

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
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

  const sel = {
    country: clean(body.country, 6).toUpperCase(),
    buyerType: clean(body.buyerType, 20),
    taxId: clean(body.bizNo || body.taxId, 60),
    plan: clean(body.plan, 40),
    method: clean(body.method, 40),
    voiceMinutes: Math.max(0, Math.min(1000000, Number(body.voiceMinutes) || 0)),
    alimtalk: Math.max(0, Math.min(1000000, Number(body.alimtalk) || 0)),
  };

  const q = await rpc('sales_quote', { p: sel });

  if (!q || q.error) {
    const code = (q && q.error) || 'quote_failed';
    if (code === 'busy') return res.status(429).json({ error: 'too_many' });
    if (code === 'no_pricing') return res.status(503).json({ error: 'not_ready' });
    if (code.startsWith('db_')) return res.status(502).json({ error: 'quote_unavailable' });
    return res.status(400).json({ error: code });
  }

  return res.status(200).json(q);
}
