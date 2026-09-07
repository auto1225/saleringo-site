/* app.js — shell: side nav with badges, top bar (search, language,
   theme, user, logout), password banner, mobile tab bar, hash router. */
import { el, clear, btn, glyph, link } from './dom.js';
import { t, initLang, getLang, setLang, onLang } from './i18n.js';
import { api, loadPricing } from './api.js';
import { setPricing } from './format.js';
import { toast, toastError, confirmDialog, modalOpen } from './ui.js';
import * as router from './router.js';
import { VIEWS } from './views/index.js';

const NAV = [
  ['/dashboard', 'nav.dashboard', 'tasks_today', 'home'], ['/leads', 'nav.leads', 'leads_new', 'inbox'], ['/orders', 'nav.orders', 'orders_pending', 'cart'],
  ['/customers', 'nav.customers', null, 'people'], ['/subscriptions', 'nav.subscriptions', null], ['/invoices', 'nav.invoices', 'invoices_due'],
  ['/usage', 'nav.usage', 'jobs_human'], ['/stats', 'nav.stats', null], ['/marketing', 'nav.marketing', null], ['/settings', 'nav.settings', null],
];
const LIST_SECTIONS = ['/leads', '/orders', '/customers', '/subscriptions', '/invoices', '/payments', '/usage'];

const ctx = { user: null, badges: {}, pricing: null, refreshMe, navigate: router.navigate, replaceQuery: router.replaceQuery };
let shell = null, main = null, current = null;

/* ── Theme ───────────────────────────────────────────────────────── */
const THEME_KEY = 'sra_theme';
function storedTheme() { try { return localStorage.getItem(THEME_KEY); } catch (e) { return null; } }
function effectiveTheme() { return storedTheme() || (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'); }
function applyTheme() { const s = storedTheme(); if (s) document.documentElement.dataset.theme = s; else delete document.documentElement.dataset.theme; }
function toggleTheme() {
  const next = effectiveTheme() === 'dark' ? 'light' : 'dark';
  try { localStorage.setItem(THEME_KEY, next); } catch (e) { /* ignore */ }
  applyTheme(); renderShell();
  if (rerun) rerun();
}

/* ── Session ─────────────────────────────────────────────────────── */
async function refreshMe() {
  const r = await api.me();
  ctx.user = r.user; ctx.badges = r.badges || {};
  updateBadges();
  return r;
}
function updateBadges() {
  document.querySelectorAll('[data-badge]').forEach((b) => {
    const n = ctx.badges[b.dataset.badge] || 0;
    b.textContent = n ? String(n) : ''; b.dataset.n = String(n);
  });
  const bar = document.getElementById('pwbanner');
  if (bar) bar.hidden = !(ctx.user && ctx.user.must_change_password);
}
async function logout() {
  if (!(await confirmDialog(t('top.logout'), t('confirm.logout')))) return;
  try { await api.logout(); } catch (e) { /* cookie cleared either way */ }
  location.href = '/admin/login';
}

/* ── Shell ───────────────────────────────────────────────────────── */
function navLink(item, cls) {
  const [path, key, badge] = item;
  return el('a', { href: '#' + path, class: cls || null }, el('span', null, t(key)), badge ? el('span', { class: 'badge', 'data-badge': badge, 'aria-label': t(key) }) : null);
}
function renderShell() {
  const search = el('input', { type: 'search', id: 'gsearch', placeholder: t('top.search'), 'aria-label': t('top.search_label'), autocomplete: 'off' });
  search.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter') return;
    const q = search.value.trim(); if (!q) return;
    const sec = router.sectionOf(router.parseHash().path);
    router.navigate(LIST_SECTIONS.includes(sec) && sec !== '/usage' ? sec : '/leads', { q });
  });
  const theme = effectiveTheme();
  const top = el('div', { class: 'topbar' },
    el('div', { class: 'search' }, search),
    btn(getLang() === 'ko' ? 'EN' : 'KO', () => setLang(getLang() === 'ko' ? 'en' : 'ko'), 'btn-sm mono', { 'aria-label': t('top.lang') }),
    btn([glyph(theme === 'dark' ? 'sun' : 'moon', 16), el('span', { class: 'sr-only' }, t('top.theme'))], toggleTheme, 'btn-sm', { 'aria-label': t('top.theme') + ': ' + t(theme === 'dark' ? 'theme.dark' : 'theme.light'), title: t('top.theme') }),
    el('div', { class: 'who' }, el('span', { class: 'name' }, el('b', null, ctx.user ? (ctx.user.display_name || ctx.user.username) : '')), el('span', { class: 'role' }, ctx.user ? ctx.user.role : '')),
    btn(t('top.logout'), logout, 'btn-sm btn-ghost'));
  const banner = el('div', { class: 'banner-warn', id: 'pwbanner', role: 'alert', hidden: true }, el('span', null, t('banner.pw')), link('#/settings/account', t('banner.pw_link')));
  const side = el('nav', { class: 'sidenav', 'aria-label': t('app.title') },
    el('div', { class: 'brand' }, t('app.brand'), el('small', null, t('app.title'))),
    el('ul', { class: 'navlist' }, NAV.map((n) => el('li', null, navLink(n)))),
    el('div', { class: 'navfoot' }, el('a', { href: '/ko/', target: '_blank', rel: 'noopener' }, t('nav.site')), el('a', { href: 'https://saleringo.com/admin', target: '_blank', rel: 'noopener' }, t('nav.ops'))));
  main = el('div', { class: 'content', id: 'main', tabindex: '-1' });
  const tab = el('nav', { class: 'tabbar', 'aria-label': t('nav.more') },
    NAV.slice(0, 4).map((n) => el('a', { href: '#' + n[0] }, glyph(n[3], 20), el('span', null, t(n[1])), n[2] ? el('span', { class: 'badge', 'data-badge': n[2] }) : null)),
    btn([glyph('dots', 20), el('span', null, t('nav.more'))], openSheet, '', { 'aria-haspopup': 'dialog' }));
  shell = el('div', { class: 'shell' }, side, el('div', { class: 'main' }, banner, top, main), tab);
  const root = document.getElementById('app');
  clear(root); root.appendChild(shell);
  updateBadges(); highlightNav();
}
function highlightNav() {
  const sec = router.sectionOf(router.parseHash().path);
  document.querySelectorAll('.navlist a, .tabbar a').forEach((a) => {
    if (a.getAttribute('href') === '#' + sec) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
  });
}
function openSheet() {
  const back = el('div', { class: 'sheet-back' });
  const sheet = el('div', { class: 'sheet', role: 'dialog', 'aria-label': t('nav.more') },
    el('h3', null, t('nav.more')),
    NAV.slice(4).map((n) => { const a = navLink(n); a.addEventListener('click', close); return a; }),
    el('a', { href: 'https://saleringo.com/admin', target: '_blank', rel: 'noopener' }, t('nav.ops')),
    btn(t('btn.close'), close, 'btn-ghost', { style: { width: '100%', marginTop: '6px' } }));
  function close() { back.remove(); sheet.remove(); }
  back.addEventListener('click', close);
  document.addEventListener('keydown', function esc(e) { if (e.key === 'Escape') { close(); document.removeEventListener('keydown', esc); } });
  document.body.appendChild(back); document.body.appendChild(sheet);
  updateBadges();
  sheet.querySelector('a').focus();
}

/* ── Routing ─────────────────────────────────────────────────────── */
function renderRoute(m, query) {
  highlightNav();
  clear(main);
  document.body.classList.toggle('route-print', !!(m && m.view === 'invoicePrint'));
  if (!m || !VIEWS[m.view]) { router.navigate('/dashboard'); return; }
  const view = VIEWS[m.view];
  current = { m, query };
  document.title = t('app.title') + ' · ' + t('nav.' + (router.sectionOf(m.path).slice(1) === 'payments' ? 'invoices' : router.sectionOf(m.path).slice(1)));
  try {
    view(main, Object.assign({}, ctx, { params: m.params, query, path: m.path }));
  } catch (err) {
    toastError(err);
  }
  if (!modalOpen()) main.focus({ preventScroll: true });
}
let rerun = null;

/* ── Boot ────────────────────────────────────────────────────────── */

/* /admin/orders 처럼 경로로 들어온 주소를 해시 경로로 바꾼다.
   로그인 화면이 ?next=/admin/orders 로 돌려보내면 주소창은 그 경로인데
   화면을 고르는 것은 해시라서, 그대로 두면 주소는 주문인데 대시보드가
   떠 있는 상태가 된다. 주소를 먼저 맞춰 두고 라우터를 시작한다. */
function pathToHash() {
  if (location.hash) return;
  const p = location.pathname.replace(/^\/admin\/?/, '').replace(/\/+$/, '');
  if (!p || p === 'index' || p === 'login') return;
  if (!/^[A-Za-z0-9/_-]{1,120}$/.test(p)) return;
  try { history.replaceState(null, '', '/admin#/' + p + location.search); } catch (e) { /* ignore */ }
}

async function boot() {
  initLang(); applyTheme(); pathToHash();
  const [pricing] = await Promise.all([loadPricing(), refreshMe().catch((e) => { toastError(e); throw e; })]);
  ctx.pricing = pricing; setPricing(pricing);
  renderShell();
  rerun = router.start((m, query) => renderRoute(m, query));
  setInterval(() => refreshMe().catch(() => {}), 120000);
}
window.addEventListener('DOMContentLoaded', () => {
  boot().catch(() => {
    const root = document.getElementById('app');
    clear(root);
    root.appendChild(el('div', { class: 'state error', style: { minHeight: '60vh' } }, el('b', null, t('state.error')), btn(t('btn.retry'), () => location.reload(), 'btn-sm')));
  });
});
/* 셸 밖에 있는 정적 문구(건너뛰기 링크)도 언어를 따라간다. 껍데기 HTML 은
   로그인 뒤 한 번만 나가므로, 여기서 번역해 주지 않으면 영어로 바꿔도
   한국어로 남는다. */
function localizeStatic() {
  document.querySelectorAll('[data-i18n]').forEach((n) => { n.textContent = t(n.dataset.i18n); });
}
localizeStatic();
// Language switch re-renders shell and current route; theme handled in toggleTheme.
onLang(() => { localizeStatic(); renderShell(); if (rerun) rerun(); });
export { ctx, toast };
