/* views/subscriptions.js — subscription detail: plan change, cancel,
   pause/resume, discount window, next billing, invoices. */
import { el, btn } from '../dom.js';
import { t } from '../i18n.js';
import { fmtDate, fmtMoney, fmtNum, planName, daysBetween, todayISO } from '../format.js';
import { statusPill, card } from '../ui.js';
import { staticTable } from '../table.js';
import { LIST } from '../schema-list.js';
import { ACTION_FORMS } from '../schema-form.js';
import { navigate } from '../router.js';
import { loadDetail, detailHead, facts, runAction, editButton, customerLink, notesPanel, tasksPanel } from './detail.js';

function nextBilling(item) {
  if (!item.current_period_end) return null;
  const d = new Date(item.current_period_end + 'T00:00:00+09:00'); d.setDate(d.getDate() + 1);
  const on = fmtDate(d);
  const disc = item.discount_percent && (!item.discount_until || item.discount_until >= on) ? Number(item.discount_percent) : 0;
  const amt = item.list_price != null ? Number(item.list_price) * (1 - disc / 100) : null;
  return { on, amt: amt == null ? null : (item.currency === 'KRW' ? Math.round(amt) : Math.round(amt * 100) / 100), disc };
}

export function renderSubscription(root, ctx) {
  loadDetail(root, 'subscriptions', ctx.params.id, (item, rel, reload) => {
    const act = (action, title, body, fields, danger, confirmLabel) => runAction({ entity: 'subscriptions', id: item.id, action: 'subscriptions.' + action, title, body, fields, danger, reload, confirmLabel });
    const actions = [];
    if (item.status !== 'canceled') actions.push(btn(t('act.change_plan'), () => act('change_plan', t('act.change_plan'), planName(item.plan) + ' → ?', ACTION_FORMS.change_plan()), 'btn-primary'));
    if (item.status === 'active' || item.status === 'trial') actions.push(btn(t('act.pause'), () => act('pause', t('act.pause'), t('confirm.generic'))));
    if (item.status === 'paused') actions.push(btn(t('act.resume'), () => act('resume', t('act.resume'), t('confirm.generic'))));
    if (item.status !== 'canceled') actions.push(btn(t('act.cancel_sub'), () => act('cancel', t('act.cancel_sub'), t('act.cancel_sub_body'), ACTION_FORMS.cancel(), true, t('act.cancel_sub')), 'btn-danger'));
    actions.push(editButton('subscriptions', item, reload));
    const nb = nextBilling(item);
    root.appendChild(detailHead({
      crumbs: [{ href: '#/subscriptions', text: t('entity.subscriptions') }], code: item.customer_code || item.id, title: (item.company || '—') + ' · ' + planName(item.plan),
      pill: statusPill('sub', item.status, true), meta: [item.currency, fmtMoney(item.list_price, item.currency), item.tenant_name].filter(Boolean).join(' · '), actions,
    }));
    const discActive = item.discount_percent && (!item.discount_until || item.discount_until >= todayISO());
    const left = el('div', { class: 'stack' },
      card({ title: t('tab.overview'), body: facts([
        { label: 'col.customer', value: customerLink(item.customer_id, (item.customer_code || '') + ' ' + (item.company || '')) },
        { label: 'col.order', value: item.order_id ? el('a', { href: '#/orders/' + item.order_id }, item.order_no || t('entity.order')) : null },
        { label: 'col.plan', value: planName(item.plan) }, { label: 'col.currency', value: item.currency, mono: true },
        { label: 'col.list_price', value: fmtMoney(item.list_price, item.currency), mono: true },
        { label: 'col.discount_percent', value: item.discount_percent != null ? fmtNum(item.discount_percent) + '%' + (discActive ? '' : ' (' + t('camp.ended') + ')') : null, mono: true },
        { label: 'col.discount_until', value: fmtDate(item.discount_until), mono: true }, { label: 'col.started_at', value: fmtDate(item.started_at), mono: true },
        { label: 'col.current_period', value: item.current_period_start ? fmtDate(item.current_period_start) + ' – ' + fmtDate(item.current_period_end) + (item.current_period_end ? ' (' + t('misc.days', { n: daysBetween(todayISO(), item.current_period_end) }) + ')' : '') : null, mono: true },
        { label: 'col.cancel_at', value: fmtDate(item.cancel_at), mono: true }, { label: 'col.canceled_at', value: fmtDate(item.canceled_at), mono: true },
        { label: 'col.tenant', value: item.tenant_name || item.tenant_id }, { label: 'col.note', value: item.note, pre: true },
      ]) }),
      card({ title: t('sub.next_billing'), body: nb ? el('div', { class: 'grid grid-3' },
        el('div', { class: 'kpi' }, el('div', { class: 'lbl' }, t('col.due_at')), el('div', { class: 'val' }, nb.on)),
        el('div', { class: 'kpi' }, el('div', { class: 'lbl' }, t('col.amount')), el('div', { class: 'val' }, fmtMoney(nb.amt, item.currency))),
        el('div', { class: 'kpi' }, el('div', { class: 'lbl' }, t('col.discount')), el('div', { class: 'val' }, nb.disc ? nb.disc + '%' : '—'))) : el('p', { class: 'muted' }, t('state.none')) }),
      card({ title: t('tab.invoices'), body: staticTable(LIST.invoices.columns.filter((c) => c.key !== 'company'), rel.invoices || [], { onRow: (r) => navigate('/invoices/' + r.id) }) }));
    const right = el('div', { class: 'stack' }, notesPanel('subscription', item.id, rel.notes, reload), tasksPanel('subscription', item.id, rel.tasks, reload));
    root.appendChild(el('div', { class: 'grid grid-side' }, left, right));
  });
}
