/* 판매 관리자(/admin)의 단 하나의 서버 함수.
 *
 * 왜 하나인가. Vercel Hobby 플랜은 함수 12개가 한도입니다. 화면(HTML)과
 * API 를 이 함수 하나가 맡고, vercel.json 의 rewrite 가 /admin/* 과
 * /api/admin/* 을 여기로 보냅니다 — 원래 경로는 ?page= / ?p= 로 들어옵니다.
 *
 * 왜 화면까지 함수가 내보내는가. api/_admin/pages/ 아래의 HTML 은 정적으로
 * 서빙되지 않습니다(api/ 아래 밑줄 파일은 404). 세션이 있는 사람에게만 이
 * 함수가 읽어서 보내므로, 로그인 없이는 화면 껍데기도 열리지 않습니다.
 *
 * 이 파일은 금액·권한·상태 전이를 판단하지 않습니다. 그 판단은 전부 DB 의
 * admin_* 함수 안에 있고(SECURITY DEFINER, 토큰 검증 포함), 여기서는
 * 요청을 걸러서 넘기고 결과에 HTTP 상태를 붙일 뿐입니다. 관리자 권한의
 * DB 키는 어디에도 없습니다 — _db.js 의 publishable 키로 RPC 만 부릅니다.
 */
import fs from 'node:fs';
import path from 'node:path';
import { rpc, ipHash } from './_db.js';
import {
  readToken,
  tokenLooksValid,
  setSessionCookie,
  clearSessionCookie,
  baseHeaders,
  sameOrigin,
  parseBody,
  sendRpc,
} from './_admin/session.js';
import { toCsv, csvFilename } from './_admin/csv.js';

const CTRL = new RegExp('[\\u0000-\\u001f\\u007f]', 'g');

function str(v, limit) {
  return String(v == null ? '' : v)
    .replace(CTRL, ' ')
    .trim()
    .slice(0, limit || 200);
}
/* 비밀번호는 다듬지 않습니다. 앞뒤 공백도 그 사람의 비밀번호입니다. */
function raw(v, limit) {
  return typeof v === 'string' ? v.slice(0, limit) : '';
}
function obj(v) {
  return v && typeof v === 'object' && !Array.isArray(v) ? v : {};
}
function int(v, def, min, max) {
  const n = Number.parseInt(v, 10);
  if (!Number.isFinite(n)) return def;
  return Math.max(min, Math.min(max, n));
}
function orNull(s) {
  return s === '' ? null : s;
}

/* ---------- 요청 해석 ---------- */

/* rewrite 가 넘긴 ?page= / ?p= 를 읽는다. Vercel 이 풀어 둔 req.query 를
   먼저 믿고, 없으면 req.url 을 직접 푼다. rewrite 를 거치지 않고 원래
   경로 그대로 들어온 경우(vercel dev 등)도 같은 뜻으로 읽는다. */
function query(req) {
  const out = {};
  const q = req.query;
  if (q && typeof q === 'object') {
    for (const k of Object.keys(q)) {
      const v = q[k];
      if (typeof v === 'string') out[k] = v;
      else if (Array.isArray(v) && typeof v[0] === 'string') out[k] = v[0];
    }
  }
  let u = null;
  try {
    u = new URL(req.url || '/', 'https://x');
  } catch (e) {
    u = null;
  }
  if (u) {
    for (const [k, v] of u.searchParams) if (!(k in out)) out[k] = v;
    if (!('page' in out) && !('p' in out)) {
      const api = u.pathname.match(/^\/api\/admin\/(.+)$/);
      const pg = u.pathname.match(/^\/admin(?:\/(.*))?$/);
      if (api) out.p = api[1];
      else if (pg) out.page = pg[1] || 'index';
    }
  }
  return out;
}

function notAllowed(res, allow) {
  res.setHeader('Allow', allow);
  return res.status(405).json({ ok: false, error: 'method_not_allowed' });
}

/* ---------- 화면 ---------- */

/* page 값이 파일 이름을 고르지 않습니다. 아는 파일 둘뿐입니다. */
const PAGES = { login: 'login.html', app: 'app.html' };

function pagesDir() {
  return process.env.ADMIN_PAGES_DIR || path.join(process.cwd(), 'api', '_admin', 'pages');
}

function sendHtml(res, which) {
  let html;
  try {
    html = fs.readFileSync(path.join(pagesDir(), PAGES[which]), 'utf8');
  } catch (e) {
    console.error('admin page missing: ' + which);
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    return res.status(500).send('Admin page is not available.');
  }
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  return res.status(200).send(html);
}

function redirect(res, loc) {
  res.setHeader('Location', loc);
  return res.status(302).end();
}

/* 로그인 뒤 돌아갈 곳. /admin/ 아래의 단순한 경로만. '..' 이나 '//' 가
   들어간 값은 버립니다 — next 는 로그인 화면이 그대로 location 에 넣는
   값이라, 바깥으로 보내는 문이 되어서는 안 됩니다. */
const NEXT_RE = /^[A-Za-z0-9_\-./]{1,200}$/;
function nextParam(name) {
  if (name === 'index' || !NEXT_RE.test(name)) return '';
  if (name.includes('..') || name.includes('//')) return '';
  return '?next=' + encodeURIComponent('/admin/' + name);
}

async function servePage(req, res, page) {
  res.setHeader('X-Frame-Options', 'DENY');
  if (req.method !== 'GET' && req.method !== 'HEAD') return notAllowed(res, 'GET, HEAD');

  /* admin_me 는 싸고, 부르는 김에 세션의 last_seen 도 늘려 줍니다. */
  const token = readToken(req);
  let valid = false;
  if (token) {
    const me = await rpc('admin_me', { p_token: token });
    valid = !!(me && me.ok === true);
    if (!valid && me && me.error === 'unauthorized') clearSessionCookie(res, req);
  }

  const name = str(page, 200).replace(/^\/+/, '').replace(/\/+$/, '') || 'index';
  if (name === 'login') return valid ? redirect(res, '/admin') : sendHtml(res, 'login');
  if (valid) return sendHtml(res, 'app');
  return redirect(res, '/admin/login' + nextParam(name));
}

/* ---------- 액션 ---------- */

/* 액션 → DB 함수. 화면이 보낸 이름을 그대로 DB 로 넘기지 않고, 이 표에
   있는 것만, 이 표가 정한 인자만 넘깁니다. 인자의 뜻(어느 표, 어느 상태가
   허용되는지)은 DB 가 검증합니다. p_token 은 부를 때 앞에 붙습니다. */
const ACTIONS = {
  me: { POST: ['admin_me', () => ({})] },
  password: {
    POST: ['admin_change_password', (b) => ({ p_current: raw(b.current, 200), p_new: raw(b.new, 200) })],
  },
  dashboard: {
    POST: ['admin_dashboard', (b) => ({ p_from: orNull(str(b.from, 20)), p_to: orNull(str(b.to, 20)) })],
  },
  list: {
    POST: [
      'admin_list',
      (b) => ({
        p_entity: str(b.entity, 40),
        p_filter: obj(b.filter),
        p_sort: orNull(str(b.sort, 80)),
        p_page: int(b.page, 1, 1, 100000),
        p_size: int(b.size, 50, 1, 200),
      }),
    ],
  },
  get: { POST: ['admin_get', (b) => ({ p_entity: str(b.entity, 40), p_id: orNull(str(b.id, 64)) })] },
  save: {
    POST: [
      'admin_save',
      (b) => ({ p_entity: str(b.entity, 40), p_id: orNull(str(b.id, 64)), p_data: obj(b.data) }),
    ],
  },
  action: {
    POST: [
      'admin_action',
      (b) => ({
        p_entity: str(b.entity, 40),
        p_id: orNull(str(b.id, 64)),
        p_action: str(b.action, 40),
        p_data: obj(b.data),
      }),
    ],
  },
  stats: { POST: ['admin_stats', (b) => ({ p_report: str(b.report, 40), p_params: obj(b.params) })] },
  settings: {
    GET: ['admin_settings_get', () => ({})],
    POST: ['admin_settings_set', (b) => ({ p_key: str(b.key, 80), p_value: b.value === undefined ? null : b.value })],
  },
  users: {
    GET: ['admin_users_list', () => ({})],
    POST: ['admin_users_save', (b) => ({ p_id: orNull(str(b.id, 64)), p_data: obj(b.data) })],
  },
};

/* 표 밖에서 따로 다루는 액션과 그 메서드. */
const SPECIAL = { health: ['GET'], login: ['POST'], logout: ['POST'], export: ['GET', 'POST'] };

function allowedMethods(p) {
  if (Object.hasOwn(SPECIAL, p)) return SPECIAL[p];
  if (Object.hasOwn(ACTIONS, p)) return Object.keys(ACTIONS[p]);
  return null;
}

/* CSRF. X-Admin 은 남의 사이트의 폼이 붙일 수 없는 헤더이고, Origin 은
   브라우저가 붙이는 출처입니다. 둘 다 맞아야 DB 로 갑니다. */
function postGuard(req) {
  if (String(req.headers['x-admin'] || '') !== '1') {
    return {
      ok: false,
      error: 'forbidden',
      message: { ko: '요청 헤더가 없습니다.', en: 'Missing request header.' },
    };
  }
  if (!sameOrigin(req)) {
    return {
      ok: false,
      error: 'forbidden',
      message: { ko: '다른 출처에서 온 요청입니다.', en: 'Cross-origin request.' },
    };
  }
  return null;
}

async function login(req, res, body) {
  const username = str(body.username, 80);
  const password = raw(body.password, 200);
  if (!username || !password) {
    const fields = [];
    if (!username) fields.push('username');
    if (!password) fields.push('password');
    return res.status(400).json({
      ok: false,
      error: 'invalid',
      fields: fields,
      message: { ko: '아이디와 비밀번호를 입력하세요.', en: 'Enter your username and password.' },
    });
  }
  const r = await rpc('admin_login', {
    p_username: username,
    p_password: password,
    p_ip_hash: await ipHash(req),
    p_user_agent: str(req.headers['user-agent'], 400),
  });
  if (!r || r.ok !== true) return sendRpc(req, res, r);
  /* 토큰은 쿠키로만 나갑니다. 본문에 넣으면 화면 스크립트가 만질 수 있고,
     그러면 HttpOnly 로 숨긴 뜻이 없어집니다. */
  if (!tokenLooksValid(r.token)) {
    console.error('admin_login returned a token in an unexpected format');
    return res.status(502).json({ ok: false, error: 'token_format' });
  }
  setSessionCookie(res, req, r.token);
  return res.status(200).json({ ok: true, user: r.user || null });
}

async function logout(req, res) {
  const token = readToken(req);
  if (token) await rpc('admin_logout', { p_token: token });
  /* DB 가 실패해도 쿠키는 지웁니다. 로그아웃은 실패하지 않아야 합니다. */
  clearSessionCookie(res, req);
  return res.status(200).json({ ok: true });
}

async function exportCsv(req, res, method, body, q, token) {
  let entity;
  let filter;
  if (method === 'GET') {
    /* 다운로드 링크. filter 는 URL 인코딩된 JSON. */
    entity = str(q.entity, 40);
    const f = str(q.filter, 20000);
    if (f) {
      try {
        filter = JSON.parse(f);
      } catch (e) {
        return res.status(400).json({ ok: false, error: 'invalid', fields: ['filter'] });
      }
    }
  } else {
    entity = str(body.entity, 40);
    filter = body.filter;
  }
  const r = await rpc(
    'admin_export',
    { p_token: token, p_entity: entity, p_filter: obj(filter) },
    { timeoutMs: 12000 },
  );
  if (!r || r.ok !== true) return sendRpc(req, res, r);
  res.setHeader('Content-Type', 'text/csv; charset=utf-8');
  res.setHeader('Content-Disposition', 'attachment; filename="' + csvFilename(entity) + '"');
  return res.status(200).send(toCsv(r.columns, r.rows));
}

async function runAction(req, res, q) {
  const p = str(q.p, 80).replace(/^\/+|\/+$/g, '');
  const method = req.method;
  const allow = allowedMethods(p);
  if (!allow) return res.status(404).json({ ok: false, error: 'not_found' });
  if (!allow.includes(method)) return notAllowed(res, allow.join(', '));

  let body = {};
  if (method === 'POST') {
    const bad = postGuard(req);
    if (bad) return res.status(403).json(bad);
    const pb = parseBody(req);
    if (!pb.ok) return res.status(pb.status).json({ ok: false, error: pb.error });
    body = pb.body;
  }

  if (p === 'health') return sendRpc(req, res, await rpc('admin_health', {}));
  if (p === 'login') return login(req, res, body);
  if (p === 'logout') return logout(req, res);

  /* 여기서부터는 세션이 있어야 합니다. 쿠키가 없으면 DB 까지 가지 않습니다. */
  const token = readToken(req);
  if (!token) return res.status(401).json({ ok: false, error: 'unauthorized' });

  if (p === 'export') return exportCsv(req, res, method, body, q, token);

  const route = ACTIONS[p][method];
  const args = Object.assign({ p_token: token }, route[1](body));
  return sendRpc(req, res, await rpc(route[0], args));
}

export default async function handler(req, res) {
  baseHeaders(res);
  try {
    const q = query(req);
    /* ?page= 가 있으면 화면, 아니면 ?p= 가 액션 이름. */
    if (q.page !== undefined) return await servePage(req, res, q.page);
    return await runAction(req, res, q);
  } catch (e) {
    /* 스택은 로그로만. 응답에는 코드 하나. */
    console.error('admin handler error: ' + ((e && e.message) || e));
    if (!res.headersSent) return res.status(500).json({ ok: false, error: 'internal' });
    return undefined;
  }
}
