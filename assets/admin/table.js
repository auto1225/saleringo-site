/* table.js — cell rendering, static tables for related lists, the
   filter bar, and DataTable (server paging/sorting through api.list). */
import { el, clear, btn, link, debounce } from './dom.js';
import { t, enumLabel, has } from './i18n.js';
import { api, exportUrl } from './api.js';
import { fmtMoney, fmtMoneyPair, fmtNum, fmtPct, fmtPctRaw, fmtDate, fmtDateTime, fmtMonth, countryShort, planName, langLabel, DASH, countryOptions, planOptions } from './format.js';
import { statusPill, loadingEl, emptyEl, errorEl } from './ui.js';

/* ── Cells ───────────────────────────────────────────────────────── */
export function colLabel(c) {
  if (c.labelText != null) return c.labelText;
  const k = c.label || ('col.' + c.key);
  return has(k) ? t(k) : (has('col.' + k) ? t('col.' + k) : k);
}
function get(row, key) { return key.split('.').reduce((o, k) => (o == null ? undefined : o[k]), row); }

export function cellNode(c, row) {
  const v = get(row, c.key);
  const cur = c.currency ? (c.currency === 'KRW' || c.currency === 'USD' ? c.currency : get(row, c.currency)) : row.currency;
  switch (c.type) {
    case 'money': return fmtMoney(v, cur);
    case 'moneyPair': return el('span', null, fmtMoneyPair(v).map((s, i) => el('span', { style: i ? { display: 'block' } : null }, s)));
    case 'num': return fmtNum(v, c.digits);
    case 'pct': return fmtPct(v);
    case 'pctRaw': return fmtPctRaw(v);
    case 'date': return fmtDate(v);
    case 'datetime': return fmtDateTime(v);
    case 'month': return fmtMonth(v);
    case 'status': return statusPill(c.prefix, v);
    case 'enum': return v == null ? DASH : enumLabel(c.prefix, v);
    case 'country': return countryShort(v);
    case 'plan': return planName(v);
    case 'lang': return langLabel(v);
    case 'bool': return v == null ? DASH : (v ? t('misc.yes') : t('misc.no'));
    case 'tags': return Array.isArray(v) && v.length ? el('span', { class: 'tags' }, v.map((x) => el('span', { class: 'tag' }, x))) : DASH;
    case 'sub': return el('span', null, v == null || v === '' ? DASH : String(v), c.sub && get(row, c.sub) != null ? el('span', { class: 'sub' }, String(get(row, c.sub))) : null);
    case 'meter': {
      const p = v == null ? null : Number(v);
      if (p == null || isNaN(p)) return DASH;
      const kind = p >= 100 ? ' bad' : p >= 80 ? ' warn' : '';
      return el('span', null, el('span', { class: 'meter' + kind, 'aria-hidden': 'true' }, el('i', { style: { width: Math.min(100, p) + '%' } })), fmtPctRaw(p));
    }
    case 'custom': return c.render(row, v);
    case 'json': return v == null ? DASH : (typeof v === 'string' ? v : JSON.stringify(v));
    default: return v == null || v === '' ? DASH : String(v);
  }
}
function tdClass(c) {
  const cls = [];
  if (c.type === 'money' || c.type === 'num' || c.type === 'pct' || c.type === 'pctRaw' || c.type === 'moneyPair') cls.push('num');
  if (c.type === 'date' || c.type === 'datetime' || c.type === 'month' || c.mono) cls.push('mono');
  if (c.wrap) cls.push('wrap');
  if (c.dim) cls.push('dim');
  return cls.join(' ') || null;
}

/* ── Static table (client-side rows) ─────────────────────────────── */
export function staticTable(columns, rows, opts) {
  const o = opts || {};
  if (!rows || !rows.length) return emptyEl(o.empty || t('state.empty'), false);
  const thead = el('thead', null, el('tr', null, columns.map((c) => el('th', { class: tdClass(c), scope: 'col' }, colLabel(c)))));
  const tbody = el('tbody', null, rows.map((r) => {
    const tr = el('tr', { class: o.onRow ? 'clickable' : null, tabindex: o.onRow ? '0' : null }, columns.map((c) => el('td', { class: tdClass(c) }, cellNode(c, r))));
    if (o.onRow) {
      tr.addEventListener('click', (e) => { if (e.target.closest('a,button,input,select')) return; o.onRow(r); });
      tr.addEventListener('keydown', (e) => { if (e.key === 'Enter' && e.target === tr) o.onRow(r); });
    }
    return tr;
  }));
  return el('div', { class: 'tbl-wrap' }, el('table', { class: 'tbl' }, thead, tbody));
}

/* ── Filter bar ──────────────────────────────────────────────────── */
function enumOptions(prefix, values) { return values.map((v) => ({ value: v, label: enumLabel(prefix, v) })); }
export function filterOptions(f) {
  if (f.options) return f.options;
  if (f.type === 'country') return countryOptions();
  if (f.type === 'plan') return planOptions();
  if (f.type === 'currency') return [{ value: 'KRW', label: 'KRW' }, { value: 'USD', label: 'USD' }];
  if (f.type === 'lang') return [{ value: 'ko', label: t('misc.lang_ko') }, { value: 'en', label: t('misc.lang_en') }];
  if (f.values) return enumOptions(f.prefix, f.values);
  return [];
}
export function filterBar(schema, values, onChange) {
  const bar = el('div', { class: 'filterbar', role: 'search' });
  const inputs = {};
  const emit = () => { const out = {}; Object.keys(inputs).forEach((k) => { const v = inputs[k].type === 'checkbox' ? (inputs[k].checked ? '1' : '') : inputs[k].value; if (v !== '' && v != null) out[k] = v; }); onChange(out); };
  const emitSlow = debounce(emit, 320);
  schema.forEach((f) => {
    const id = 'flt_' + f.key;
    const label = f.labelText || (has('filter.' + f.key) ? t('filter.' + f.key) : has('col.' + f.key) ? t('col.' + f.key) : f.key);
    let input;
    if (f.type === 'text') { input = el('input', { id, type: 'search', placeholder: label, 'aria-label': label }); input.addEventListener('input', emitSlow); input.addEventListener('keydown', (e) => { if (e.key === 'Enter') emit(); }); }
    else if (f.type === 'date' || f.type === 'month') { input = el('input', { id, type: f.type, class: 'mono' }); input.addEventListener('change', emit); }
    else if (f.type === 'checkbox') { input = el('input', { id, type: 'checkbox' }); input.addEventListener('change', emit); }
    else {
      input = el('select', { id }, el('option', { value: '' }, t('misc.all')));
      filterOptions(f).forEach((o) => input.appendChild(el('option', { value: o.value }, o.label)));
      input.addEventListener('change', emit);
    }
    if (values && values[f.key] != null) { if (f.type === 'checkbox') input.checked = values[f.key] === '1' || values[f.key] === true; else input.value = values[f.key]; }
    inputs[f.key] = input;
    bar.appendChild(f.type === 'checkbox'
      ? el('div', { class: 'fld inline' }, input, el('label', { for: id }, label))
      : el('div', { class: 'fld' + (f.type === 'text' ? ' q' : '') }, el('label', { for: id }, label), input));
  });
  bar.appendChild(btn(t('btn.reset'), () => { Object.keys(inputs).forEach((k) => { if (inputs[k].type === 'checkbox') inputs[k].checked = false; else inputs[k].value = ''; }); emit(); }, 'btn-ghost btn-sm'));
  return { root: bar, inputs };
}

/* ── DataTable ───────────────────────────────────────────────────── */
const SIZES = [20, 50, 100, 200];
export class DataTable {
  /** {entity, columns, filters, sort, size, fixed, state, onRow, onState, csv, extra} */
  constructor(o) {
    this.o = o;
    this.state = Object.assign({ filter: {}, sort: o.sort || null, page: 1, size: o.size || 50 }, o.state || {});
    this.root = el('div', { class: 'datatable' });
    this.wrap = el('div', { class: 'tbl-wrap' });
    this.foot = el('div', { class: 'tbl-foot' });
    this.rows = []; this.total = 0; this.req = 0;
  }
  mount(parent) {
    const top = el('div', { class: 'row between', style: { alignItems: 'flex-end' } });
    if (this.o.filters && this.o.filters.length) {
      this.fb = filterBar(this.o.filters, this.state.filter, (f) => { this.state.filter = f; this.state.page = 1; this.load(); });
      top.appendChild(this.fb.root);
    }
    if (this.o.extra) top.appendChild(el('div', { class: 'row', style: { marginBottom: '12px' } }, this.o.extra));
    this.root.appendChild(top);
    this.root.appendChild(this.wrap);
    this.root.appendChild(this.foot);
    parent.appendChild(this.root);
    this.load();
    return this;
  }
  fullFilter() {
    const f = Object.assign({}, this.state.filter, this.o.fixed || {});
    return this.o.mapFilter ? this.o.mapFilter(f) : f;
  }
  async load() {
    const my = ++this.req;
    this.wrap.classList.add('busy');
    if (!this.rows.length) { clear(this.wrap); this.wrap.appendChild(loadingEl()); }
    if (this.o.onState) this.o.onState(this.state);
    try {
      const r = await api.list(this.o.entity, this.fullFilter(), this.state.sort, this.state.page, this.state.size);
      if (my !== this.req) return;
      this.rows = r.rows || []; this.total = r.total || 0;
      this.render();
    } catch (err) {
      if (my !== this.req) return;
      this.rows = [];
      clear(this.wrap); this.wrap.classList.remove('busy');
      this.wrap.appendChild(errorEl(err, () => this.load()));
      clear(this.foot);
    }
  }
  reload() { return this.load(); }
  setSort(key) {
    const [k, d] = (this.state.sort || ':').split(':');
    this.state.sort = k === key && d === 'asc' ? key + ':desc' : key + ':asc';
    this.state.page = 1; this.load();
  }
  render() {
    const o = this.o; const cols = o.columns;
    clear(this.wrap); this.wrap.classList.remove('busy');
    if (!this.rows.length) { this.wrap.appendChild(emptyEl()); this.renderFoot(); return; }
    const [sk, sd] = (this.state.sort || ':').split(':');
    const thead = el('thead', null, el('tr', null, cols.map((c) => {
      const sortable = c.sortable !== false && c.type !== 'custom';
      const th = el('th', { class: tdClass(c), scope: 'col', 'aria-sort': sk === c.key ? (sd === 'desc' ? 'descending' : 'ascending') : null });
      th.appendChild(sortable ? el('button', { type: 'button', onClick: () => this.setSort(c.key) }, colLabel(c), el('span', { class: 'arr', 'aria-hidden': 'true' }, sk === c.key ? (sd === 'desc' ? '↓' : '↑') : '↕')) : el('span', null, colLabel(c)));
      return th;
    })));
    const tbody = el('tbody', null, this.rows.map((r) => {
      const tr = el('tr', { class: o.onRow ? 'clickable' : null, tabindex: o.onRow ? '0' : null }, cols.map((c) => el('td', { class: tdClass(c) }, cellNode(c, r))));
      if (o.onRow) {
        tr.addEventListener('click', (e) => { if (e.target.closest('a,button,input,select')) return; o.onRow(r); });
        tr.addEventListener('keydown', (e) => { if (e.key === 'Enter' && e.target === tr) o.onRow(r); });
      }
      return tr;
    }));
    this.wrap.appendChild(el('table', { class: 'tbl' }, thead, tbody));
    this.renderFoot();
  }
  renderFoot() {
    clear(this.foot);
    const s = this.state; const from = this.total ? (s.page - 1) * s.size + 1 : 0; const to = Math.min(this.total, s.page * s.size);
    const pages = Math.max(1, Math.ceil(this.total / s.size));
    const sizeSel = el('select', { 'aria-label': t('misc.per_page'), style: { width: 'auto', minHeight: '30px', padding: '4px 26px 4px 8px' } }, SIZES.map((n) => el('option', { value: n }, String(n))));
    sizeSel.value = String(s.size);
    sizeSel.addEventListener('change', () => { s.size = Number(sizeSel.value); s.page = 1; this.load(); });
    const csv = this.o.csv === false ? null : link(exportUrl(this.o.entity, this.fullFilter()), t('btn.csv'), { class: 'btn btn-sm', download: '' });
    this.foot.appendChild(el('div', { class: 'row' }, el('span', { class: 'mono' }, t('misc.of_total', { from: fmtNum(from), to: fmtNum(to), total: fmtNum(this.total) })),
      el('label', { class: 'row small' }, t('misc.per_page'), sizeSel), csv));
    this.foot.appendChild(el('div', { class: 'pager' },
      btn(t('btn.prev'), () => { s.page = Math.max(1, s.page - 1); this.load(); }, 'btn-sm', { disabled: s.page <= 1 }),
      el('span', { class: 'pg' }, s.page + ' / ' + pages),
      btn(t('btn.next'), () => { s.page = Math.min(pages, s.page + 1); this.load(); }, 'btn-sm', { disabled: s.page >= pages })));
  }
}
