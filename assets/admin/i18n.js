/* i18n.js — every visible string goes through t(). The dictionary is a
   flat map key -> [ko, en]; one entry always carries both languages, so
   a missing translation is impossible by construction. A missing KEY
   returns the key itself, which makes gaps visible in testing. */
import { CORE } from './i18n-core.js';
import { ENT } from './i18n-entities.js';

const DICT = Object.assign({}, CORE, ENT);
const KEY = 'sra_lang';
let lang = 'ko';
const listeners = new Set();

export function initLang() {
  let v = null;
  try { v = localStorage.getItem(KEY); } catch (e) { /* storage blocked */ }
  lang = v === 'en' ? 'en' : 'ko';
  document.documentElement.lang = lang;
  return lang;
}
export function getLang() { return lang; }
export function setLang(next) {
  lang = next === 'en' ? 'en' : 'ko';
  try { localStorage.setItem(KEY, lang); } catch (e) { /* ignore */ }
  document.documentElement.lang = lang;
  listeners.forEach((fn) => fn(lang));
}
export function onLang(fn) { listeners.add(fn); return () => listeners.delete(fn); }

/** t('key', {name:'x'}) — {placeholders} are replaced; unknown key -> key. */
export function t(key, vars) {
  const row = DICT[key];
  let s = row ? row[lang === 'en' ? 1 : 0] : key;
  if (vars) s = s.replace(/\{(\w+)\}/g, (m, k) => (vars[k] == null ? '' : String(vars[k])));
  return s;
}
export function has(key) { return Object.prototype.hasOwnProperty.call(DICT, key); }

/** Pick from a {ko,en} object coming from the server; fall back sensibly. */
export function pick(obj, fallback) {
  if (obj == null) return fallback == null ? '' : fallback;
  if (typeof obj === 'string') return obj;
  return obj[lang] || obj.ko || obj.en || (fallback == null ? '' : fallback);
}

/** Label for an enum value: t('lead.new') etc. Unknown values show raw. */
export function enumLabel(prefix, value) {
  if (value == null || value === '') return '';
  const k = prefix + '.' + value;
  return has(k) ? t(k) : String(value);
}

/** For tests: list keys of the dictionary. */
export function allKeys() { return Object.keys(DICT); }
