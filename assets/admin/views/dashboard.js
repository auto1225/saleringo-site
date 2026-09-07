/* views/dashboard.js — range picker, 8 KPI tiles, charts, to-do lists,
   system state. */
import { el, clear, btn, link } from '../dom.js';
import { t, enumLabel } from '../i18n.js';
import { api } from '../api.js';
import { fmtMoney, fmtMoneyPair, fmtNum, fmtPct, fmtDateTime, fmtDate, rangePreset, countryShort, planName, langLabel } from '../format.js';
import { loadingEl, errorEl, card, statusPill } from '../ui.js';
import { barChart, lineChart, donutChart, hbarChart } from '../charts.js';
import { replaceQuery } from '../router.js';

const PRESETS = ['this_month', 'last_month', 'last_90', 'this_year'];

export function renderDashboard(root, ctx) {
  let range = ctx.query.from && ctx.query.to ? { from: ctx.query.from, to: ctx.query.to, preset: 'custom' } : Object.assign({ preset: 'this_month' }, rangePreset('this_month'));
  const fromIn = el('input', { type: 'date', class: 'mono', value: range.from, 'aria-label': t('range.from') });
  const toIn = el('input', { type: 'date', class: 'mono', value: range.to, 'aria-label': t('range.to') });
  const seg = el('div', { class: 'seg', role: 'group', 'aria-label': t('range.custom') });
  PRESETS.forEach((p) => seg.appendChild(el('button', { type: 'button', 'aria-pressed': range.preset === p ? 'true' : 'false', onClick: () => { range = Object.assign({ preset: p }, rangePreset(p)); fromIn.value = range.from; toIn.value = range.to; sync(); load(); } }, t('range.' + p))));
  const apply = btn(t('btn.apply'), () => { if (fromIn.value && toIn.value) { range = { preset: 'custom', from: fromIn.value, to: toIn.value }; sync(); load(); } }, 'btn-sm');
  const body = el('div');
  root.appendChild(el('div', { class: 'page-head' }, el('div', null, el('h1', null, t('dash.title'))),
    el('div', { class: 'page-actions' }, seg, el('div', { class: 'row' }, fromIn, el('span', { class: 'muted' }, '–'), toIn, apply))));
  root.appendChild(body);
  function sync() {
    seg.querySelectorAll('button').forEach((b, i) => b.setAttribute('aria-pressed', PRESETS[i] === range.preset ? 'true' : 'false'));
    replaceQuery(range.preset === 'custom' ? { from: range.from, to: range.to } : {});
  }
  async function load() {
    clear(body); body.appendChild(loadingEl());
    try {
      const d = await api.dashboard(range.from, range.to);
      clear(body); draw(body, d);
    } catch (err) { clear(body); body.appendChild(errorEl(err, load)); }
  }
  load();
}

function kpi(label, value, sub, cls) {
  const val = Array.isArray(value) ? el('div', { class: 'val' + (value.length > 1 ? ' two' : '') }, value.map((v, i) => el('span', { style: i ? { display: 'block' } : null }, v))) : el('div', { class: 'val' }, value);
  return el('div', { class: 'card kpi' + (cls ? ' ' + cls : '') }, el('div', { class: 'lbl' }, label), val, sub ? el('div', { class: 'sub' }, sub) : null);
}

function draw(body, d) {
  const k = d.kpi || {};
  const s = (d.series && d.series.months) || [];
  body.appendChild(el('div', { class: 'grid grid-kpi' },
    kpi(t('kpi.mrr'), fmtMoneyPair(k.mrr), t('kpi.mrr_sub')),
    kpi(t('kpi.active_subs'), fmtNum(k.active_subscriptions)),
    kpi(t('kpi.orders_new'), fmtNum(k.orders_new)),
    kpi(t('kpi.leads_new'), fmtNum(k.leads_new)),
    kpi(t('kpi.conversion'), k.conversion_rate == null ? '—' : fmtPct(k.conversion_rate)),
    kpi(t('kpi.receivable'), fmtMoneyPair(k.receivable), t('kpi.receivable_sub'), (k.receivable && (k.receivable.KRW > 0 || k.receivable.USD > 0)) ? 'warn' : ''),
    kpi(t('kpi.paid'), fmtMoneyPair(k.paid_in_range)),
    kpi(t('kpi.jobs_human'), fmtNum(k.jobs_human), null, k.jobs_human > 0 ? 'bad' : '')));

  const cats = s.map((m) => m.month.slice(2));
  body.appendChild(el('div', { class: 'grid grid-2 mt' },
    card({ title: t('dash.chart_monthly') + ' · KRW', body: barChart({ label: t('dash.chart_monthly') + ' KRW', categories: cats, series: [{ label: t('dash.series_paid') + ' KRW', values: s.map((m) => m.paid_KRW || 0) }], format: (v) => fmtMoney(v, 'KRW') }) }),
    card({ title: t('dash.chart_monthly') + ' · USD', body: barChart({ label: t('dash.chart_monthly') + ' USD', categories: cats, series: [{ label: t('dash.series_paid') + ' USD', values: s.map((m) => m.paid_USD || 0) }], format: (v) => fmtMoney(v, 'USD') }) })));
  body.appendChild(el('div', { class: 'grid grid-2 mt' },
    card({ title: t('dash.series_orders') + ' · ' + t('dash.series_leads') + ' · ' + t('dash.series_subs'), body: lineChart({ label: t('dash.chart_monthly'), categories: cats, series: [
      { label: t('dash.series_orders'), values: s.map((m) => m.orders || 0) }, { label: t('dash.series_leads'), values: s.map((m) => m.leads || 0) }, { label: t('dash.series_subs'), values: s.map((m) => m.active_subscriptions || 0) }] }) }),
    card({ title: t('dash.chart_plan'), body: donutChart({ label: t('dash.chart_plan'), items: (d.by_plan || []).map((p) => ({ label: planName(p.plan), value: p.active })) }) })));
  const bc = (d.by_country || []).slice(0, 8);
  const bl = d.by_lang || [];
  body.appendChild(el('div', { class: 'grid grid-2 mt' },
    card({ title: t('dash.chart_country'), body: hbarChart({ label: t('dash.chart_country'), categories: bc.map((c) => countryShort(c.country)), series: [{ label: t('dash.series_leads'), values: bc.map((c) => c.leads) }, { label: t('dash.series_orders'), values: bc.map((c) => c.orders) }] }) }),
    card({ title: t('dash.chart_lang'), body: hbarChart({ label: t('dash.chart_lang'), categories: bl.map((c) => langLabel(c.lang)), series: [{ label: t('dash.series_leads'), values: bl.map((c) => c.leads) }, { label: t('dash.series_orders'), values: bl.map((c) => c.orders) }] }) })));

  const todo = d.todo || {};
  const li = (items, fn) => (items && items.length ? el('ul', { class: 'list-plain' }, items.slice(0, 8).map(fn)) : el('p', { class: 'muted' }, t('dash.no_todo')));
  body.appendChild(el('h2', { class: 'mt', style: { marginBottom: '10px' } }, t('dash.todo')));
  body.appendChild(el('div', { class: 'grid grid-3' },
    card({ title: t('dash.todo_leads'), actions: link('#/leads?status=new', t('btn.view_all')), body: li(todo.leads, (x) => el('li', null, link('#/leads/' + x.id, (x.company || x.name || x.email || x.ref || '—')), el('span', { class: 'when' }, fmtDateTime(x.created_at)))) }),
    card({ title: t('dash.todo_orders'), actions: link('#/orders?state=received', t('btn.view_all')), body: li(todo.orders, (x) => el('li', null, el('span', null, link('#/orders/' + x.id, x.order_no || '—'), ' ', el('span', { class: 'muted' }, x.company || '')), statusPill('order', x.state))) }),
    card({ title: t('dash.todo_invoices'), actions: link('#/invoices?status=overdue', t('btn.view_all')), body: li(todo.invoices, (x) => el('li', null, el('span', null, link('#/invoices/' + x.id, x.invoice_no || '—'), ' ', el('span', { class: 'muted' }, x.company || '')), el('span', { class: 'mono' }, fmtMoney(x.total, x.currency) + ' · ' + fmtDate(x.due_at)))) }),
    card({ title: t('dash.todo_jobs'), actions: link('#/usage/jobs?human=1', t('btn.view_all')), body: li(todo.jobs, (x) => el('li', null, el('span', null, (x.tenant_name || x.order_no || '—') + ' · ', el('span', { class: 'mono' }, x.step || '')), statusPill('job', x.status))) }),
    card({ title: t('dash.todo_tasks'), actions: link('#/tasks', t('btn.view_all')), body: li(todo.tasks, (x) => el('li', null, el('span', null, enumLabel('task', x.kind) + ' · ' + (x.title || '')), el('span', { class: 'when' }, fmtDateTime(x.due_at)))) }),
    card({ title: t('dash.system'), body: el('dl', { class: 'facts', style: { gridTemplateColumns: '1fr' } },
      el('div', null, el('dt', null, t('dash.pricing_version')), el('dd', { class: 'num' }, String((d.system && d.system.pricing_version) || '—'))),
      el('div', null, el('dt', null, t('dash.policy_version')), el('dd', { class: 'num' }, String((d.system && d.system.policy_version) || '—'))),
      el('div', null, el('dt', null, t('dash.usage_at')), el('dd', { class: 'num' }, fmtDateTime(d.system && d.system.usage_computed_at))),
      el('div', null, el('dt', null, t('dash.tenants')), el('dd', { class: 'num' }, fmtNum(d.system && d.system.tenants)))) })));
}
