/* views/stats.js — report tabs (revenue, pipeline, marketing, usage,
   cohort, countries): range, chart per report, generic table, CSV. */
import { el, btn, link, clear } from '../dom.js';
import { t, pick } from '../i18n.js';
import { api } from '../api.js';
import { fmtNum, rangePreset, countryShort, planName, fmtMonth } from '../format.js';
import { loadingEl, errorEl, card } from '../ui.js';
import { staticTable } from '../table.js';
import { barChart, funnelChart, hbarChart } from '../charts.js';
import { navigate, replaceQuery } from '../router.js';

export const REPORTS = ['revenue', 'pipeline', 'marketing', 'usage', 'cohort', 'countries'];
const MONEY = /^(net|tax|total|amount|paid|mrr|receivable|revenue|refunded|list_price)$/;

function colType(key, sample) {
  if (key === 'month') return 'month';
  if (key === 'country') return 'country';
  if (key === 'plan') return 'plan';
  if (key === 'lang' || key === 'locale') return 'lang';
  if (/_at$/.test(key)) return 'datetime';
  if (/_on$|^date$|^cohort$/.test(key)) return 'date';
  if (/pct|rate|conversion/.test(key)) return 'pct';
  if (MONEY.test(key)) return 'money';
  if (typeof sample === 'number') return 'num';
  return 'text';
}
function toColumns(columns, rows) {
  const s = rows[0] || {};
  return (columns || Object.keys(s).map((k) => ({ key: k }))).map((c) => ({ key: c.key, labelText: c.ko || c.en ? pick({ ko: c.ko, en: c.en }) : c.key, type: colType(c.key, s[c.key]), sortable: false }));
}
function csvUrl(columns, rows) {
  const esc = (v) => { const s = v == null ? '' : (typeof v === 'object' ? JSON.stringify(v) : String(v)); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
  const lines = [columns.map((c) => esc(c.labelText)).join(',')].concat(rows.map((r) => columns.map((c) => esc(r[c.key])).join(',')));
  return 'data:text/csv;charset=utf-8,' + encodeURIComponent('﻿' + lines.join('\r\n'));
}

function labelOf(row, key) {
  const v = row[key];
  if (key === 'country') return countryShort(v);
  if (key === 'plan') return planName(v);
  if (key === 'month') return fmtMonth(v);
  return v == null ? '—' : String(v);
}
function chartFor(report, columns, rows) {
  if (!rows.length) return null;
  const numeric = columns.filter((c) => c.type === 'num' || c.type === 'money').map((c) => c.key);
  const textKey = (columns.find((c) => c.type !== 'num' && c.type !== 'money' && c.type !== 'pct') || {}).key;
  if (!numeric.length || !textKey) return null;
  if (report === 'revenue') {
    const months = Array.from(new Set(rows.map((r) => r.month))).filter(Boolean).sort();
    const curs = Array.from(new Set(rows.map((r) => r.currency))).filter(Boolean);
    const vk = numeric.includes('total') ? 'total' : numeric[0];
    if (months.length && curs.length) {
      return barChart({ label: t('report.revenue'), categories: months.map((m) => String(m).slice(2, 7)), stacked: true,
        series: curs.map((cu) => ({ label: cu, values: months.map((m) => rows.filter((r) => r.month === m && r.currency === cu).reduce((a, r) => a + (Number(r[vk]) || 0), 0)) })), format: (v) => fmtNum(v) });
    }
  }
  if (report === 'pipeline') return funnelChart({ label: t('report.pipeline'), steps: rows.map((r) => ({ label: labelOf(r, textKey), value: Number(r[numeric[0]]) || 0 })) });
  const top = rows.slice(0, 20);
  return hbarChart({ label: t('report.' + report), categories: top.map((r) => labelOf(r, textKey)), series: numeric.slice(0, 2).map((k) => ({ label: (columns.find((c) => c.key === k) || {}).labelText || k, values: top.map((r) => Number(r[k]) || 0) })) });
}

/** Chart + table + CSV for a report; used by stats and marketing. */
export function reportBlock(report, params) {
  const box = el('div');
  async function load() {
    clear(box); box.appendChild(loadingEl());
    try {
      const r = await api.stats(report, params);
      const rows = r.rows || []; const cols = toColumns(r.columns, rows);
      clear(box);
      const chart = chartFor(report, cols, rows);
      if (chart) box.appendChild(card({ title: t('misc.chart'), body: chart, cls: 'mb' }));
      box.appendChild(card({ title: t('misc.table'), actions: rows.length ? link(csvUrl(cols, rows), t('btn.csv'), { class: 'btn btn-sm', download: report + '-' + (params.from || '') + '.csv' }) : null, flat: true,
        body: staticTable(cols, rows) }));
    } catch (err) { clear(box); box.appendChild(errorEl(err, load)); }
  }
  load();
  return box;
}

export function renderStats(root, ctx) {
  const report = REPORTS.includes(ctx.params.report) ? ctx.params.report : 'revenue';
  let range = ctx.query.from && ctx.query.to ? { from: ctx.query.from, to: ctx.query.to } : rangePreset('this_year');
  const fromIn = el('input', { type: 'date', class: 'mono', value: range.from, 'aria-label': t('range.from') });
  const toIn = el('input', { type: 'date', class: 'mono', value: range.to, 'aria-label': t('range.to') });
  const body = el('div');
  const seg = el('div', { class: 'seg', role: 'tablist' }, REPORTS.map((id) => el('button', { type: 'button', role: 'tab', 'aria-selected': id === report ? 'true' : 'false', 'aria-pressed': id === report ? 'true' : 'false', onClick: () => navigate('/stats/' + id, range) }, t('report.' + id))));
  const apply = btn(t('btn.apply'), () => { if (fromIn.value && toIn.value) { range = { from: fromIn.value, to: toIn.value }; replaceQuery(range); draw(); } }, 'btn-sm');
  root.appendChild(el('div', { class: 'page-head' }, el('div', null, el('h1', null, t('report.title'))),
    el('div', { class: 'page-actions' }, seg, el('div', { class: 'row' }, fromIn, el('span', { class: 'muted' }, '–'), toIn, apply))));
  root.appendChild(body);
  function draw() { clear(body); body.appendChild(reportBlock(report, range)); }
  draw();
}
