/* 관리자 세션의 바깥쪽 절반 — 쿠키와 요청 검사.
 *
 * 세션의 진짜 판정은 DB 함수(admin_me 등)가 토큰 해시로 합니다. 이 파일은
 * 그 토큰을 쿠키에서 꺼내고 넣고 지우는 일, 그리고 DB 를 부르기 전에
 * 걸러 낼 수 있는 것(CSRF 헤더·Origin·본문 크기·형식)을 맡습니다.
 * 여기서 걸러진 요청은 DB 에 닿지 않으므로 유량제한 비용도 쓰지 않습니다.
 *
 * 라이브러리는 쓰지 않습니다. 쿠키 하나를 읽고 쓰는 데 의존성을 들이면
 * 공개 저장소에 공급망 하나가 더 생길 뿐입니다.
 */

export const COOKIE = 'sra';

/* 32바이트 랜덤을 16진수로 쓴 것. 이 모양이 아니면 쿠키가 없는 것으로
   봅니다 — 남이 넣은 값이 DB 까지 가서 검색되는 일을 막습니다. */
const TOKEN_RE = /^[a-f0-9]{64}$/;

/* 절대 7일. 유휴 12시간은 DB 가 last_seen 으로 따로 잽니다. */
const MAX_AGE = 604800;

/* 응답 본문 크기의 상한. 관리자 화면이 보내는 JSON 은 수 KB 를 넘지
   않습니다. 200 KB 는 실수(붙여넣기)와 고의(부하)를 함께 거릅니다. */
export const BODY_LIMIT = 200 * 1024;

/* 로컬(vercel dev)에서는 Secure 가 붙은 쿠키를 브라우저가 버립니다. */
export function isLocal(req) {
  const h = String((req.headers && req.headers.host) || '').toLowerCase();
  return h.startsWith('localhost') || h.startsWith('127.0.0.1');
}

function attrs(req) {
  return '; Path=/; HttpOnly' + (isLocal(req) ? '' : '; Secure') + '; SameSite=Lax';
}

export function tokenLooksValid(t) {
  return TOKEN_RE.test(String(t || ''));
}

/* 쿠키 머리글에서 sra 만 꺼낸다. 형식이 맞지 않으면 없는 것과 같다. */
export function readToken(req) {
  const raw = String((req.headers && req.headers.cookie) || '');
  for (const part of raw.split(';')) {
    const i = part.indexOf('=');
    if (i < 0) continue;
    if (part.slice(0, i).trim() !== COOKIE) continue;
    const v = part.slice(i + 1).trim();
    return TOKEN_RE.test(v) ? v : null;
  }
  return null;
}

export function setSessionCookie(res, req, token) {
  res.setHeader('Set-Cookie', COOKIE + '=' + token + '; Max-Age=' + MAX_AGE + attrs(req));
}

export function clearSessionCookie(res, req) {
  res.setHeader('Set-Cookie', COOKIE + '=; Max-Age=0' + attrs(req));
}

/* 모든 응답에 붙는 머리글. 관리자 화면과 API 는 검색엔진에도, 캐시에도,
   다른 사이트로 나가는 Referer 에도 남지 않아야 합니다. */
export function baseHeaders(res) {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex, nofollow');
  res.setHeader('Referrer-Policy', 'same-origin');
}

/* CSRF 의 두 번째 벽. 첫 번째는 X-Admin 헤더(남의 사이트의 폼은 임의
   헤더를 못 붙인다)이고, 이것은 브라우저가 붙이는 Origin 이 우리 호스트인지
   봅니다. Origin 이 없으면(옛 브라우저·일부 다운로드) Referer 로 대신
   봅니다. 둘 다 없으면 통과시키지 않습니다. */
export function sameOrigin(req) {
  const h = req.headers || {};
  const host = String(h.host || '').toLowerCase();
  const src = h.origin || h.referer || '';
  if (!host || !src) return false;
  try {
    return new URL(String(src)).host.toLowerCase() === host;
  } catch (e) {
    return false;
  }
}

/* DB 오류 코드 → HTTP 상태. 본문은 DB 가 만든 객체를 그대로 씁니다. */
export function statusOf(code) {
  switch (code) {
    case 'unauthorized':
      return 401;
    case 'forbidden':
      return 403;
    case 'rate_limited':
      return 429;
    case 'invalid':
      return 400;
    case 'not_found':
      return 404;
    case 'conflict':
    case 'bad_transition':
      return 409;
    case 'db_unconfigured':
      return 503;
    default:
      return code && code.startsWith('db_') ? 502 : 400;
  }
}

/* RPC 결과를 내보낸다.
   · ok:true → 200, 객체 그대로.
   · DB 가 만든 오류 → 상태 매핑, 객체 그대로(ko/en 메시지와 fields 가
     이미 들어 있다). unauthorized 면 죽은 쿠키를 지운다.
   · db_* 는 DB 가 아니라 전송층의 오류. _db.js 가 붙인 PostgREST 본문
     (SQL 메시지가 섞일 수 있다)은 로그로만 남기고 코드만 보낸다. */
export function sendRpc(req, res, r) {
  if (!r || typeof r !== 'object' || Array.isArray(r) || (r.ok !== true && r.ok !== false)) {
    console.error('admin rpc: unexpected shape');
    return res.status(502).json({ ok: false, error: 'db_parse' });
  }
  if (r.ok === true) return res.status(200).json(r);
  const code = typeof r.error === 'string' && r.error ? r.error : 'invalid';
  const status = statusOf(code);
  if (code === 'unauthorized') clearSessionCookie(res, req);
  if (code.startsWith('db_')) {
    console.error('admin rpc failure: ' + code + ' ' + (r.status || '') + ' ' + (r.detail || ''));
    return res.status(status).json({ ok: false, error: code });
  }
  return res.status(status).json(r);
}

/* POST 본문. Vercel 은 content-type 이 JSON 이면 미리 풀어 주고, 아니면
   문자열이나 Buffer 로 줍니다. 어느 쪽이든 "JSON 객체 하나"만 받습니다.
   빈 본문은 {} 로 봅니다(로그아웃처럼 보낼 것이 없는 요청).
   돌려주는 것: {ok:true, body} 또는 {ok:false, status, error}. */
export function parseBody(req) {
  let b = req.body;
  if (Buffer.isBuffer(b)) b = b.toString('utf8');
  if (b == null || b === '') return { ok: true, body: {} };
  if (typeof b === 'string') {
    if (b.length > BODY_LIMIT) return { ok: false, status: 413, error: 'too_large' };
    try {
      b = JSON.parse(b);
    } catch (e) {
      return { ok: false, status: 400, error: 'bad_json' };
    }
  } else if (b && typeof b === 'object' && !Array.isArray(b)) {
    /* 이미 풀린 객체. 크기는 다시 재 봅니다 — 풀린 뒤라도 한도는 같습니다. */
    let n = 0;
    try {
      n = JSON.stringify(b).length;
    } catch (e) {
      n = BODY_LIMIT + 1;
    }
    if (n > BODY_LIMIT) return { ok: false, status: 413, error: 'too_large' };
  }
  if (!b || typeof b !== 'object' || Array.isArray(b)) {
    return { ok: false, status: 400, error: 'bad_request' };
  }
  return { ok: true, body: b };
}
