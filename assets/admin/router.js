/* router.js — hash routes: #/path?query. Query holds list state so a
   filtered list survives reload and back/forward. replaceQuery() updates
   the URL without re-rendering. */

const ROUTES = [
  ['/dashboard', 'dashboard'],
  ['/leads', 'leads'], ['/leads/:id', 'lead'],
  ['/orders', 'orders'], ['/orders/:id', 'order'],
  ['/customers', 'customers'], ['/customers/:id', 'customer'],
  ['/subscriptions', 'subscriptions'], ['/subscriptions/:id', 'subscription'],
  ['/invoices', 'invoices'], ['/invoices/:id', 'invoice'], ['/invoices/:id/print', 'invoicePrint'],
  ['/payments', 'payments'], ['/tasks', 'tasks'],
  ['/usage', 'usage'], ['/usage/:tab', 'usage'],
  ['/stats', 'stats'], ['/stats/:report', 'stats'],
  ['/marketing', 'marketing'], ['/marketing/:tab', 'marketing'], ['/marketing/campaigns/:id', 'campaign'],
  ['/settings', 'settings'], ['/settings/:tab', 'settings'],
].map(([p, v]) => ({ pattern: p, view: v, parts: p.split('/').filter(Boolean) }));

export function parseHash(h) {
  const raw = (h == null ? location.hash : h).replace(/^#/, '') || '/dashboard';
  const i = raw.indexOf('?');
  const path = (i < 0 ? raw : raw.slice(0, i)).replace(/\/+$/, '') || '/dashboard';
  const query = {};
  if (i >= 0) new URLSearchParams(raw.slice(i + 1)).forEach((v, k) => { query[k] = v; });
  return { path, query };
}

export function match(path) {
  const parts = path.split('/').filter(Boolean);
  for (const r of ROUTES) {
    if (r.parts.length !== parts.length) continue;
    const params = {};
    let ok = true;
    for (let i = 0; i < parts.length; i++) {
      if (r.parts[i].startsWith(':')) params[r.parts[i].slice(1)] = decodeURIComponent(parts[i]);
      else if (r.parts[i] !== parts[i]) { ok = false; break; }
    }
    if (ok) return { view: r.view, params, path };
  }
  return null;
}

export function buildHash(path, query) {
  const qs = query ? Object.keys(query).filter((k) => query[k] != null && query[k] !== '').map((k) => encodeURIComponent(k) + '=' + encodeURIComponent(typeof query[k] === 'object' ? JSON.stringify(query[k]) : query[k])).join('&') : '';
  return '#' + path + (qs ? '?' + qs : '');
}
export function navigate(path, query) { location.hash = buildHash(path, query); }
export function replaceQuery(query) {
  const { path } = parseHash();
  history.replaceState(null, '', buildHash(path, query));
}

/** Top-level section for nav highlighting. */
export function sectionOf(path) {
  const first = '/' + (path.split('/').filter(Boolean)[0] || 'dashboard');
  if (first === '/payments') return '/invoices';
  return first;
}

export function start(onChange) {
  let last = null;
  const run = () => {
    const { path, query } = parseHash();
    const m = match(path);
    const key = path;
    onChange(m, query, key !== last);
    last = key;
  };
  window.addEventListener('hashchange', run);
  run();
  return run;
}
