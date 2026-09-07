/* login.js — the public sign-in page. Health line from /api/admin/health,
   show/hide password, language toggle, error line per code, safe `next`. */
import { t, initLang, getLang, setLang, onLang } from './i18n.js';
import { api, health, ApiError } from './api.js';

const $ = (id) => document.getElementById(id);

function applyTheme() {
  let s = null; try { s = localStorage.getItem('sra_theme'); } catch (e) { /* ignore */ }
  if (s) document.documentElement.dataset.theme = s;
}
function relabel() {
  document.querySelectorAll('[data-i18n]').forEach((n) => { n.textContent = t(n.dataset.i18n); });
  $('lang').textContent = getLang() === 'ko' ? 'EN' : 'KO';
  document.title = t('login.title') + ' · Saleringo';
  const pw = $('password');
  $('togglePw').textContent = t(pw.type === 'password' ? 'btn.show' : 'btn.hide');
}
function safeNext() {
  const n = new URLSearchParams(location.search).get('next') || '';
  return n.startsWith('/admin/') || n.startsWith('/admin#') || n === '/admin' ? n : '/admin';
}
async function showHealth() {
  const box = $('health'); const dot = box.querySelector('.dot'); const txt = box.querySelector('span:last-child');
  try {
    const h = await health();
    if (h && h.db) {
      dot.className = 'dot ' + (h.adminUsers ? 'ok' : 'warn');
      txt.textContent = h.adminUsers ? t('login.db_ok', { p: h.pricingVersion || '—', q: h.policyVersion || '—', n: h.adminUsers }) : t('login.db_noadmin');
    } else { dot.className = 'dot bad'; txt.textContent = t('login.db_bad'); }
    txt.dataset.i18n = '';
  } catch (e) { dot.className = 'dot bad'; txt.textContent = t('login.db_bad'); txt.dataset.i18n = ''; }
}
function errorFor(err) {
  if (err instanceof ApiError) {
    if (err.status === 429 || err.code === 'rate_limited') return t('err.login_rate');
    if (err.status === 401 || err.code === 'invalid_credentials' || err.code === 'unauthorized') return t('err.invalid_credentials');
    if (err.network) return t('err.network');
    if (err.msg) return err.msg[getLang()] || err.msg.ko || err.msg.en;
    if (err.status >= 500) return t('err.server');
  }
  return t('err.unknown');
}

window.addEventListener('DOMContentLoaded', () => {
  initLang(); applyTheme(); relabel(); showHealth();
  onLang(() => { relabel(); showHealth(); $('err').textContent = ''; });
  $('lang').addEventListener('click', () => setLang(getLang() === 'ko' ? 'en' : 'ko'));
  $('togglePw').addEventListener('click', () => {
    const pw = $('password'); const show = pw.type === 'password';
    pw.type = show ? 'text' : 'password'; $('togglePw').setAttribute('aria-pressed', show ? 'true' : 'false'); relabel(); pw.focus();
  });
  const form = $('loginForm'); const err = $('err'); const submit = $('submit');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const u = $('username').value.trim(); const p = $('password').value;
    err.textContent = '';
    if (!u || !p) { err.textContent = t('login.fill'); (u ? $('password') : $('username')).focus(); return; }
    submit.disabled = true;
    try {
      await api.login(u, p);
      location.href = safeNext();
    } catch (ex) {
      err.textContent = errorFor(ex);
      submit.disabled = false;
      $('password').focus(); $('password').select();
    }
  });
});
