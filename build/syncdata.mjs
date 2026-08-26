/* 요금표와 정책을 Supabase 로 올린다.
 *
 * 금액과 계약 조건은 두 곳에서 쓰인다 — 브라우저가 화면에 그리고,
 * 서버가 주문을 받을 때 다시 계산한다. 그 둘이 다른 파일을 보면
 * 구매자가 본 금액과 청구된 금액이 달라진다.
 *
 * 그래서 파일은 이 저장소의 assets/data/*.json 하나뿐이고,
 * 배포할 때마다 그 내용을 판 번호와 함께 DB 에 올린다.
 * 주문 기록은 자기가 어느 판을 보고 접수됐는지 가리키므로,
 * 나중에 요금이 바뀌어도 그때 무엇에 동의했는지 되짚을 수 있다.
 *
 *     node build/syncdata.mjs            올리고 확인
 *     node build/syncdata.mjs --check    올리지 않고 어긋난 것만 알림
 *
 * 필요한 환경변수 (.env.local 또는 셸):
 *     SUPABASE_URL                프로젝트 주소
 *     SUPABASE_SERVICE_ROLE_KEY   쓰기 권한 키 — 이 스크립트에서만 씁니다
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const CHECK = process.argv.includes('--check');

/* .env.local 을 읽는다. Vercel CLI 가 `vercel env pull` 로 만드는 파일이다. */
function loadEnv() {
  for (const name of ['.env.local', '.env']) {
    const p = path.join(ROOT, name);
    if (!fs.existsSync(p)) continue;
    for (const line of fs.readFileSync(p, 'utf8').split(/\r?\n/)) {
      const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)$/);
      if (!m) continue;
      let v = m[2].trim();
      if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
        v = v.slice(1, -1);
      }
      if (!process.env[m[1]]) process.env[m[1]] = v;
    }
  }
}
loadEnv();

const URL_ = (process.env.SUPABASE_URL || '').replace(/\/+$/, '');
const KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || '';

function readJson(rel) {
  const raw = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  return { raw, data: JSON.parse(raw) };
}

/* 판 번호는 내용에서 만든다. 손으로 올리면 언젠가 안 올린다. */
function stamp(data, declared) {
  const canonical = JSON.stringify(data, Object.keys(data).sort());
  const hash = crypto.createHash('sha256').update(canonical).digest('hex').slice(0, 12);
  return `${declared}+${hash}`;
}

async function rpc(fn, body) {
  const res = await fetch(`${URL_}/rest/v1/rpc/${fn}`, {
    method: 'POST',
    headers: {
      apikey: KEY,
      authorization: `Bearer ${KEY}`,
      'content-type': 'application/json',
      'content-profile': 'sales',
    },
    body: JSON.stringify(body),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`${fn} → ${res.status} ${text.slice(0, 400)}`);
  return text ? JSON.parse(text) : null;
}

const pricing = readJson('assets/data/pricing.json');
const policy = readJson('assets/data/policy.json');

const priceVer = stamp(pricing.data, pricing.data.version || 'pricing');
const policyVer = stamp(policy.data, policy.data.version || 'policy');

console.log('요금표 판 :', priceVer);
console.log('정책   판 :', policyVer);

if (!URL_ || !KEY) {
  console.log();
  console.log('SUPABASE_URL 과 SUPABASE_SERVICE_ROLE_KEY 가 없어 올리지 못했습니다.');
  console.log('  vercel env pull .env.local     로 받아 오거나 셸에 직접 넣으십시오.');
  console.log('  판 번호는 위 값이고, DB 에 같은 번호가 이미 있으면 올릴 것이 없습니다.');
  process.exit(CHECK ? 0 : 1);
}

if (CHECK) {
  const rows = await rpc('sync_versions_status', {});
  const same =
    rows && rows.pricing_version === priceVer && rows.policy_version === policyVer;
  console.log();
  console.log('DB 요금표 판 :', rows ? rows.pricing_version : '(없음)');
  console.log('DB 정책   판 :', rows ? rows.policy_version : '(없음)');
  console.log(same ? '\n파일과 DB 가 같은 판입니다.' : '\n어긋났습니다 — node build/syncdata.mjs 로 올리십시오.');
  process.exit(same ? 0 : 1);
}

await rpc('sync_pricing', { p_version: priceVer, p_data: pricing.data });
await rpc('sync_policy', { p_version: policyVer, p_data: policy.data });

const rows = await rpc('sync_versions_status', {});
console.log();
console.log('올렸습니다.');
console.log('  DB 요금표 판 :', rows.pricing_version);
console.log('  DB 정책   판 :', rows.policy_version);
if (rows.pricing_version !== priceVer || rows.policy_version !== policyVer) {
  console.log('\n!! 올린 판과 유효한 판이 다릅니다. 확인이 필요합니다.');
  process.exit(1);
}
