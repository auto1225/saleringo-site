/* form.js — a form from a field schema. Field:
   {key, type, label (i18n key) | labelText, required, options:[{value,label}],
    allowEmpty, placeholder, hint (i18n key), span2, min, max, step, rows,
    currency ('KRW'|'USD'| key of another field), validate(value, all) -> error text|null}
   Types: text email tel password select date datetime month number textarea
          tags money checkbox json readonly hidden */
import { el } from './dom.js';
import { t, has, pick } from './i18n.js';
import { seoulInputToISO, isoToSeoulInput } from './format.js';

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function fieldLabel(f) {
  if (f.labelText != null) return f.labelText;
  if (f.label) return has(f.label) ? t(f.label) : t('col.' + f.label);
  return has('col.' + f.key) ? t('col.' + f.key) : f.key;
}

function makeInput(f, value, form) {
  const id = 'f_' + f.key + '_' + Math.random().toString(36).slice(2, 7);
  const base = { id, name: f.key, 'aria-required': f.required ? 'true' : null, placeholder: f.placeholder || null, disabled: f.disabled || null };
  let node;
  switch (f.type) {
    case 'select': {
      node = el('select', base);
      if (f.allowEmpty !== false) node.appendChild(el('option', { value: '' }, f.emptyLabel != null ? f.emptyLabel : t('misc.none')));
      (f.options || []).forEach((o) => node.appendChild(el('option', { value: o.value }, o.label)));
      node.value = value == null ? '' : String(value);
      if (node.selectedIndex < 0) node.selectedIndex = 0;
      break;
    }
    case 'textarea': case 'json':
      node = el('textarea', Object.assign(base, { rows: f.rows || 4 }));
      node.value = f.type === 'json' ? (value == null ? '' : typeof value === 'string' ? value : JSON.stringify(value, null, 2)) : (value == null ? '' : String(value));
      break;
    case 'checkbox':
      node = el('input', Object.assign(base, { type: 'checkbox' }));
      node.checked = !!value;
      break;
    case 'number': case 'money':
      node = el('input', Object.assign(base, { type: 'number', step: f.step || (f.type === 'money' ? 'any' : '1'), min: f.min, max: f.max, class: 'mono', inputmode: 'decimal' }));
      node.value = value == null ? '' : String(value);
      break;
    case 'date': node = el('input', Object.assign(base, { type: 'date', class: 'mono' })); node.value = value ? String(value).slice(0, 10) : ''; break;
    case 'month': node = el('input', Object.assign(base, { type: 'month', class: 'mono' })); node.value = value ? String(value).slice(0, 7) : ''; break;
    case 'datetime': node = el('input', Object.assign(base, { type: 'datetime-local', class: 'mono' })); node.value = value ? isoToSeoulInput(value) : ''; break;
    case 'password': node = el('input', Object.assign(base, { type: 'password', autocomplete: f.autocomplete || 'new-password' })); node.value = value || ''; break;
    case 'readonly': node = el('input', Object.assign(base, { type: 'text', readOnly: true })); node.value = value == null ? '' : String(value); break;
    case 'hidden': node = el('input', Object.assign(base, { type: 'hidden' })); node.value = value == null ? '' : String(value); break;
    case 'tags': return makeTags(f, value, id, form);
    default:
      node = el('input', Object.assign(base, { type: f.type === 'email' ? 'email' : f.type === 'tel' ? 'tel' : 'text', autocomplete: f.autocomplete || 'off' }));
      node.value = value == null ? '' : String(value);
  }
  return { input: node, id, get: () => readValue(f, node), set: (v) => { if (f.type === 'checkbox') node.checked = !!v; else node.value = v == null ? '' : (f.type === 'datetime' ? isoToSeoulInput(v) : String(v)); } };
}

function makeTags(f, value, id, form) {
  const items = Array.isArray(value) ? value.slice() : (typeof value === 'string' && value ? value.split(',').map((s) => s.trim()).filter(Boolean) : []);
  const wrap = el('div', { class: 'tags' });
  const input = el('input', { id, type: 'text', placeholder: f.placeholder || 'tag ⏎', style: { width: '140px', minHeight: '30px', padding: '4px 8px' } });
  const chips = el('span', { class: 'tags' });
  function draw() {
    chips.textContent = '';
    items.forEach((tg, i) => chips.appendChild(el('span', { class: 'tag' }, tg,
      el('button', { type: 'button', 'aria-label': t('act.remove_line') + ' ' + tg, onClick: () => { items.splice(i, 1); draw(); } }, '×'))));
  }
  function add() {
    const v = input.value.trim().replace(/,$/, '');
    if (v && !items.includes(v)) items.push(v);
    input.value = ''; draw();
  }
  input.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ',') { e.preventDefault(); e.stopPropagation(); add(); } });
  input.addEventListener('blur', () => { if (input.value.trim()) add(); });
  draw();
  wrap.appendChild(chips); wrap.appendChild(input);
  return { input: wrap, focusEl: input, id, get: () => items.slice(), set: (v) => { items.length = 0; (v || []).forEach((x) => items.push(x)); draw(); } };
}

function readValue(f, node) {
  if (f.type === 'checkbox') return !!node.checked;
  const raw = node.value;
  if (f.type === 'number' || f.type === 'money') return raw === '' ? null : Number(raw);
  if (f.type === 'datetime') return raw ? seoulInputToISO(raw) : null;
  if (f.type === 'json') { if (!raw.trim()) return null; try { return JSON.parse(raw); } catch (e) { return undefined; } }
  const s = typeof raw === 'string' ? raw.trim() : raw;
  return s === '' ? null : s;
}

function errText(msg) {
  if (!msg) return t('err.field');
  if (typeof msg === 'string') return has(msg) ? t(msg) : msg;
  return pick(msg, t('err.field'));
}

/** Build a form. Returns {root, get, set, setErrors, validate, focusFirst, fields}. */
export function buildForm(fields, values, opts) {
  const o = opts || {};
  const vals = values || {};
  const root = el('div', { class: o.single ? 'stack' : 'form-grid' });
  const ctl = {};
  fields.forEach((f) => {
    const cur = f.value !== undefined ? f.value : vals[f.key];
    const c = makeInput(f, cur, null);
    const err = el('div', { class: 'err', id: c.id + '_err', role: 'alert' });
    const label = el('label', { for: c.id, class: f.required ? 'req' : null }, fieldLabel(f));
    let wrap;
    if (f.type === 'hidden') wrap = c.input;
    else if (f.type === 'checkbox') wrap = el('div', { class: 'fld inline' + (f.span2 ? ' span2' : '') }, c.input, label, err);
    else wrap = el('div', { class: 'fld' + (f.span2 || o.single ? ' span2' : '') }, label, c.input, f.hint ? el('div', { class: 'hint' }, has(f.hint) ? t(f.hint) : f.hint) : null, err);
    c.err = err; c.wrap = wrap; c.field = f;
    ctl[f.key] = c;
    root.appendChild(wrap);
    const target = c.focusEl || c.input;
    if (target && target.addEventListener) target.addEventListener('input', () => setErr(c, null));
  });

  function setErr(c, msg) {
    c.err.textContent = msg ? errText(msg) : '';
    const target = c.focusEl || c.input;
    if (target && target.setAttribute) { if (msg) target.setAttribute('aria-invalid', 'true'); else target.removeAttribute('aria-invalid'); }
  }
  function get() {
    const out = {};
    Object.keys(ctl).forEach((k) => { out[k] = ctl[k].get(); });
    return out;
  }
  function validate() {
    const all = get();
    let first = null;
    Object.keys(ctl).forEach((k) => {
      const c = ctl[k]; const f = c.field; const v = all[k];
      let msg = null;
      const empty = v == null || v === '' || (Array.isArray(v) && !v.length);
      if (f.required && empty && f.type !== 'checkbox') msg = 'err.required';
      else if (!empty && f.type === 'email' && !EMAIL.test(String(v))) msg = 'err.email';
      else if (!empty && (f.type === 'number' || f.type === 'money') && isNaN(v)) msg = 'err.number';
      else if (f.type === 'json' && v === undefined) msg = 'err.invalid';
      else if (f.validate) msg = f.validate(v, all) || null;
      setErr(c, msg);
      if (msg && !first) first = c;
    });
    if (first) (first.focusEl || first.input).focus();
    return !first;
  }
  /** Server `fields`: {key: msg} | [key] | [{field, message}]. */
  function setErrors(fieldsErr) {
    if (!fieldsErr) return;
    let firstKey = null;
    const mark = (k, m) => { if (ctl[k]) { setErr(ctl[k], m || 'err.field'); if (!firstKey) firstKey = k; } };
    if (Array.isArray(fieldsErr)) fieldsErr.forEach((x) => (typeof x === 'string' ? mark(x, null) : mark(x.field || x.key, x.message)));
    else Object.keys(fieldsErr).forEach((k) => mark(k, fieldsErr[k]));
    if (firstKey) (ctl[firstKey].focusEl || ctl[firstKey].input).focus();
  }
  function set(v) { Object.keys(v || {}).forEach((k) => { if (ctl[k]) ctl[k].set(v[k]); }); }
  function focusFirst() {
    const k = Object.keys(ctl).find((x) => ctl[x].field.type !== 'hidden' && !ctl[x].field.disabled);
    if (k) (ctl[k].focusEl || ctl[k].input).focus();
  }
  return { root, get, set, setErrors, validate, focusFirst, fields: ctl };
}
