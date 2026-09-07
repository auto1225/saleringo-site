/* format.js — money, dates (stored UTC, shown Asia/Seoul), numbers,
   country/plan names from pricing.json. */
import { getLang, t } from './i18n.js';

const TZ = 'Asia/Seoul';
let pricing = null;
export function setPricing(p) { pricing = p || null; }
export function getPricing() { return pricing; }

export const DASH = '—';

export function fmtNum(v, digits) {
  if (v == null || v === '' || isNaN(Number(v))) return DASH;
  const n = Number(v);
  return n.toLocaleString(getLang() === 'en' ? 'en-US' : 'ko-KR', {
    minimumFractionDigits: digits || 0, maximumFractionDigits: digits == null ? 2 : digits,
  });
}

/** KRW integer with 원 / KRW; USD as $1,234.50. Negative keeps the sign in front. */
export function fmtMoney(v, cur) {
  if (v == null || v === '' || isNaN(Number(v))) return DASH;
  const n = Number(v);
  const neg = n < 0;
  const a = Math.abs(n);
  const c = (cur || 'KRW').toUpperCase();
  let s;
  if (c === 'USD') s = '$' + a.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  else if (c === 'KRW') s = Math.round(a).toLocaleString('ko-KR') + (getLang() === 'en' ? ' KRW' : '원');
  else s = a.toLocaleString('en-US', { maximumFractionDigits: 2 }) + ' ' + c;
  return (neg ? '−' : '') + s;
}

/** {KRW, USD} pair -> two lines; hides a zero currency when the other is non-zero. */
export function fmtMoneyPair(obj) {
  if (!obj) return [DASH];
  const out = [];
  if (obj.KRW != null && (obj.KRW !== 0 || obj.USD == null || obj.USD === 0)) out.push(fmtMoney(obj.KRW, 'KRW'));
  if (obj.USD != null && (obj.USD !== 0 || out.length === 0)) out.push(fmtMoney(obj.USD, 'USD'));
  return out.length ? out : [DASH];
}

export function fmtPct(v, digits) {
  if (v == null || isNaN(Number(v))) return DASH;
  return (Number(v) * 100).toLocaleString('en-US', { maximumFractionDigits: digits == null ? 1 : digits }) + '%';
}
export function fmtPctRaw(v) {
  if (v == null || isNaN(Number(v))) return DASH;
  return Number(v).toLocaleString('en-US', { maximumFractionDigits: 0 }) + '%';
}

function parts(d) {
  const f = new Intl.DateTimeFormat('en-US', { timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false });
  const o = {};
  f.formatToParts(d).forEach((p) => { o[p.type] = p.value; });
  if (o.hour === '24') o.hour = '00';
  return o;
}
function toDate(v) {
  if (v == null || v === '') return null;
  if (v instanceof Date) return isNaN(v) ? null : v;
  const s = String(v);
  const d = /^\d{4}-\d{2}-\d{2}$/.test(s) ? new Date(s + 'T00:00:00+09:00') : new Date(s);
  return isNaN(d) ? null : d;
}
/** 2026-09-07 (Asia/Seoul). */
export function fmtDate(v) {
  const d = toDate(v); if (!d) return DASH;
  const p = parts(d); return p.year + '-' + p.month + '-' + p.day;
}
/** 2026-09-07 14:05 (Asia/Seoul). */
export function fmtDateTime(v) {
  const d = toDate(v); if (!d) return DASH;
  const p = parts(d); return p.year + '-' + p.month + '-' + p.day + ' ' + p.hour + ':' + p.minute;
}
/** '2026-09' -> 2026년 9월 / Sep 2026. */
export function fmtMonth(v) {
  if (!v) return DASH;
  const s = String(v).slice(0, 7);
  const d = new Date(s + '-01T00:00:00+09:00');
  if (isNaN(d)) return s;
  return new Intl.DateTimeFormat(getLang() === 'en' ? 'en-US' : 'ko-KR', { timeZone: TZ, year: 'numeric', month: 'short' }).format(d);
}
/** datetime-local value (interpreted as Seoul time) -> UTC ISO string. */
export function seoulInputToISO(v) {
  if (!v) return null;
  const d = new Date(v.length === 16 ? v + ':00+09:00' : v + '+09:00');
  return isNaN(d) ? null : d.toISOString();
}
/** ISO -> 'YYYY-MM-DDTHH:mm' in Seoul for datetime-local inputs. */
export function isoToSeoulInput(v) {
  const d = toDate(v); if (!d) return '';
  const p = parts(d); return p.year + '-' + p.month + '-' + p.day + 'T' + p.hour + ':' + p.minute;
}
export function todayISO() { return fmtDate(new Date()); }
export function monthOf(v) { return fmtDate(v || new Date()).slice(0, 7); }
export function addMonths(ym, n) {
  const [y, m] = ym.split('-').map(Number);
  const d = new Date(Date.UTC(y, m - 1 + n, 1));
  return d.getUTCFullYear() + '-' + String(d.getUTCMonth() + 1).padStart(2, '0');
}
export function daysBetween(a, b) {
  const da = toDate(a), db = toDate(b); if (!da || !db) return null;
  return Math.round((db - da) / 86400000);
}
export function isPast(v) { const d = toDate(v); return !!d && d < new Date(); }
export function fmtDuration(sec) {
  if (sec == null || isNaN(Number(sec))) return DASH;
  const s = Number(sec);
  if (s < 60) return t('misc.seconds', { n: Math.round(s) });
  return t('misc.minutes', { n: fmtNum(Math.round(s / 60)) });
}

/** Presets for the dashboard range. */
export function rangePreset(name) {
  const today = todayISO();
  const ym = today.slice(0, 7);
  const y = today.slice(0, 4);
  if (name === 'last_month') { const lm = addMonths(ym, -1); return { from: lm + '-01', to: endOfMonth(lm) }; }
  if (name === 'last_90') { const d = new Date(Date.now() - 89 * 86400000); return { from: fmtDate(d), to: today }; }
  if (name === 'this_year') return { from: y + '-01-01', to: today };
  return { from: ym + '-01', to: endOfMonth(ym) };
}
export function endOfMonth(ym) {
  const [y, m] = ym.split('-').map(Number);
  const last = new Date(Date.UTC(y, m, 0)).getUTCDate();
  return ym + '-' + String(last).padStart(2, '0');
}

/* ── Pricing-derived names ───────────────────────────────────────── */
export function countryName(code) {
  if (!code) return DASH;
  const c = pricing && pricing.countries ? pricing.countries.find((x) => x.code === code) : null;
  if (!c) return String(code);
  const n = c.name[getLang()] || c.name.ko;
  return n + ' (' + c.code + ')';
}
export function countryShort(code) {
  if (!code) return DASH;
  const c = pricing && pricing.countries ? pricing.countries.find((x) => x.code === code) : null;
  return c ? (c.name[getLang()] || c.name.ko) : String(code);
}
export function planName(id) {
  if (!id) return DASH;
  const p = pricing && pricing.plans ? pricing.plans.find((x) => x.id === id) : null;
  return p ? (p.name[getLang()] || p.name.ko) : String(id);
}
export function planPrice(id, cur) {
  const p = pricing && pricing.plans ? pricing.plans.find((x) => x.id === id) : null;
  return p && p.price ? p.price[cur || 'KRW'] : null;
}
export function countryOptions() {
  return pricing && pricing.countries ? pricing.countries.map((c) => ({ value: c.code, label: (c.name[getLang()] || c.name.ko) + ' (' + c.code + ')' })) : [];
}
export function planOptions() {
  return pricing && pricing.plans ? pricing.plans.map((p) => ({ value: p.id, label: p.name[getLang()] || p.name.ko })) : [];
}
export function langLabel(code) {
  if (!code) return DASH;
  const k = String(code).toLowerCase().slice(0, 2);
  return k === 'ko' ? t('misc.lang_ko') : k === 'en' ? t('misc.lang_en') : String(code);
}
