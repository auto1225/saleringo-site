/* Supabase(PostgreSQL) 로 가는 유일한 통로.
 *
 * 왜 이 파일이 있는가.
 *
 * 예전에는 주문이 웹훅이나 메일로만 나갔습니다. 그 말은 받는 쪽이 못
 * 받으면 주문이 어디에도 남지 않는다는 뜻이고, 실제로 두 API 모두
 * ready:false 였으므로 아무 데도 남지 않았습니다. 주문번호도 서버
 * 인스턴스의 기억에서 만들었으므로, 인스턴스가 바뀌면 같은 주문이 서로
 * 다른 번호로 두 번 접수될 수 있었습니다.
 *
 * 이제 접수는 데이터베이스가 합니다. 금액 계산·주문번호 발번·중복 방지가
 * 한 트랜잭션 안에서 끝나므로, 그 셋이 서로 어긋날 수 없습니다.
 * 메일과 웹훅은 그 뒤에 붙는 알림일 뿐이고, 실패해도 주문은 이미 남아
 * 있습니다.
 *
 * 키에 대하여.
 *
 * 여기서 쓰는 것은 publishable 키입니다. 이 키로는 표를 한 줄도 읽거나
 * 쓸 수 없습니다 — sales 스키마는 RLS 로 전면 차단되어 있고 PostgREST 에
 * 노출되지도 않습니다. 이 키가 할 수 있는 일은 아래 다섯 개 함수를 부르는
 * 것뿐이고, 그 함수들은 각자 안에서 검증·유량제한·동의확인을 합니다.
 * 그래서 이 키가 새어 나가도 잃을 것이 없습니다. 반대로 service_role 키는
 * 이 코드 어디에도 두지 않습니다.
 */

/* 환경변수는 부를 때마다 읽습니다. 모듈을 불러온 순간에 한 번만 읽으면,
   그 뒤에 설정이 바뀌어도 이 파일은 옛 값을 계속 씁니다. 배포 직후
   환경변수를 넣은 경우가 그렇습니다. */
function base() {
  return (process.env.SUPABASE_URL || '').replace(/\/+$/, '');
}
function key() {
  return process.env.SUPABASE_PUBLISHABLE_KEY || process.env.SUPABASE_ANON_KEY || '';
}

export function dbConfigured() {
  return !!(base() && key());
}

/* 주소를 숨기지 않고 그대로 알려 줍니다. 진단할 때 필요하고,
   publishable 키와 프로젝트 주소는 원래 공개되는 값입니다. */
export function dbInfo() {
  return { configured: dbConfigured(), url: base() || null };
}

/** Postgres 함수를 부른다. 실패는 던지지 않고 형태를 맞춰 돌려준다. */
export async function rpc(fn, body, opts) {
  if (!dbConfigured()) {
    return { ok: false, error: 'db_unconfigured' };
  }
  const timeout = (opts && opts.timeoutMs) || 10000;
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), timeout);
  try {
    const k = key();
    const r = await fetch(base() + '/rest/v1/rpc/' + fn, {
      method: 'POST',
      headers: {
        apikey: k,
        authorization: 'Bearer ' + k,
        'content-type': 'application/json',
        accept: 'application/json',
      },
      body: JSON.stringify(body || {}),
      signal: ctl.signal,
    });
    const text = await r.text();
    if (!r.ok) {
      return { ok: false, error: 'db_error', status: r.status, detail: text.slice(0, 400) };
    }
    try {
      return text ? JSON.parse(text) : { ok: true };
    } catch (e) {
      return { ok: false, error: 'db_parse' };
    }
  } catch (e) {
    return { ok: false, error: e && e.name === 'AbortError' ? 'db_timeout' : 'db_unreachable' };
  } finally {
    clearTimeout(timer);
  }
}

/* IP 를 그대로 저장하지 않습니다. 유량 제한과 중복 판단에는 같은 사람인지만
   알면 되고, 그건 해시로 충분합니다. 처리방침이 접속 기록을 3개월만
   둔다고 적어 두었는데, 원본 IP 를 주문 기록(5년 보존)에 함께 넣으면
   그 약속이 깨집니다. */
export async function ipHash(req) {
  const raw =
    (req.headers['x-forwarded-for'] || '').split(',')[0].trim() ||
    req.headers['x-real-ip'] ||
    '';
  if (!raw) return null;
  const salt = process.env.IP_HASH_SALT || 'saleringo-public-intake';
  const data = new TextEncoder().encode(salt + '|' + raw);
  const buf = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(buf).slice(0, 16))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}

/* 요금표와 정책의 판이 DB 에 올라와 있는지.
   올라와 있지 않으면 주문을 받지 않습니다 — 금액을 계산할 근거가 없는
   상태에서 "접수되었습니다" 라고 말하는 것이 가장 나쁜 실패입니다. */
export async function readiness() {
  const r = await rpc('sales_readiness', {});
  if (r && r.ready) return r;
  /* 사이트가 막 배포되어 DB 가 아직 새 판을 모를 수 있습니다.
     그때는 DB 가 배포된 파일을 직접 읽어 오게 한 번 시켜 봅니다. */
  const refreshed = await rpc('sales_refresh', {});
  if (refreshed && refreshed.ok) {
    return await rpc('sales_readiness', {});
  }
  return r && typeof r === 'object' ? r : { ready: false };
}
