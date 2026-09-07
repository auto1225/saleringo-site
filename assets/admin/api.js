/* api.js — the only place that talks to /api/admin. Same-origin JSON,
   X-Admin header for CSRF, 401 -> login with next. Errors become
   ApiError{status, code, message:{ko,en}, fields}. */
import { pick, t } from './i18n.js';

export class ApiError extends Error {
  constructor(status, body, network) {
    super((body && body.error) || (network ? 'network' : 'http_' + status));
    this.status = status;
    this.code = (body && body.error) || (network ? 'network' : status >= 500 ? 'server' : 'unknown');
    this.body = body || null;
    this.msg = body && body.message ? body.message : null;
    this.fields = body && body.fields ? body.fields : null;
    this.network = !!network;
  }
}

/** Localized, human message for any error. Never a stack trace. */
export function errorMessage(err) {
  if (!err) return t('err.unknown');
  if (err instanceof ApiError) {
    if (err.status === 429) return t('err.rate_limited');
    if (err.msg) return pick(err.msg, null) || t('err.' + err.code);
    const k = 'err.' + err.code;
    const s = t(k);
    return s === k ? t(err.status >= 500 ? 'err.server' : 'err.unknown') : s;
  }
  if (err && err.name === 'TypeError') return t('err.network');
  return t('err.unknown');
}

function loginRedirect() {
  const next = location.pathname + location.search + location.hash;
  location.href = '/admin/login?next=' + encodeURIComponent(next);
}

async function request(method, path, body) {
  let r;
  try {
    r = await fetch(path, {
      method,
      credentials: 'same-origin',
      headers: body !== undefined ? { 'Content-Type': 'application/json', 'X-Admin': '1' } : { 'X-Admin': '1' },
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch (e) {
    throw new ApiError(0, null, true);
  }
  let data = null;
  try { data = await r.json(); } catch (e) { data = null; }
  if (r.status === 401) {
    if (!path.endsWith('/login') && !path.endsWith('/health')) loginRedirect();
    throw new ApiError(401, data || { error: 'unauthorized' });
  }
  if (!r.ok || !data || data.ok === false) throw new ApiError(r.status, data || { error: r.ok ? 'unknown' : 'http_' + r.status });
  return data;
}

export function call(action, body) { return request('POST', '/api/admin/' + action, body || {}); }
export function health() { return request('GET', '/api/admin/health'); }

export const api = {
  login: (username, password) => call('login', { username, password }),
  logout: () => call('logout', {}),
  me: () => call('me', {}),
  password: (current, next) => call('password', { current, new: next }),
  dashboard: (from, to) => call('dashboard', { from, to }),
  list: (entity, filter, sort, page, size) => call('list', { entity, filter: filter || {}, sort: sort || null, page: page || 1, size: size || 50 }),
  get: (entity, id) => call('get', { entity, id }),
  save: (entity, id, data) => call('save', { entity, id: id || null, data }),
  action: (entity, id, action, data) => call('action', { entity, id, action, data: data || {} }),
  stats: (report, params) => call('stats', { report, params: params || {} }),
  settingsGet: () => request('GET', '/api/admin/settings'),
  settingsSet: (key, value) => call('settings', { key, value }),
  usersGet: () => request('GET', '/api/admin/users'),
  usersSave: (id, data) => call('users', { id: id || null, data }),
};

export function exportUrl(entity, filter) {
  return '/api/admin/export?entity=' + encodeURIComponent(entity) + '&filter=' + encodeURIComponent(JSON.stringify(filter || {}));
}

let pricingPromise = null;
export function loadPricing() {
  if (!pricingPromise) {
    pricingPromise = fetch('/assets/data/pricing.json?v=1', { credentials: 'same-origin' })
      .then((r) => (r.ok ? r.json() : null))
      .catch(() => null);
  }
  return pricingPromise;
}
