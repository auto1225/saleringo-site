/* views/orders.js — order detail: full order, quote snapshot, allowed
   transitions with reason, events timeline, provisioning jobs, numbers,
   customer link, notes, tasks, status page link. */
import { el, btn, link } from '../dom.js';
import { t, enumLabel } from '../i18n.js';
import { fmtDateTime, fmtMoney, fmtNum, fmtPct, langLabel, countryName, planName } from '../format.js';
import { statusPill, card, tabs } from '../ui.js';
import { staticTable } from '../table.js';
import { LIST } from '../schema-list.js';
import { ACTION_FORMS } from '../schema-form.js';
import { loadDetail, detailHead, facts, runAction, editButton, archiveButton, notesPanel, tasksPanel, timeline, baseTimeline, customerLink } from './detail.js';

export const TRANSITIONS = {
  received: ['under_review', 'contract_sent', 'cancelled', 'rejected'],
  under_review: ['proposal_sent', 'contract_sent', 'cancelled', 'rejected'],
  proposal_sent: ['contract_sent', 'cancelled', 'rejected'],
  contract_sent: ['contract_signed', 'cancelled'],
  contract_signed: ['payment_pending', 'active'],
  payment_pending: ['paid', 'cancelled'],
  paid: ['active'],
  active: ['cancelled'],
  cancelled: [], rejected: [],
};

export function renderOrder(root, ctx) {
  loadDetail(root, 'orders', ctx.params.id, (item, rel, reload) => {
    const allowed = TRANSITIONS[item.state] || [];
    const go = (state) => runAction({
      entity: 'orders', id: item.id, action: 'orders.transition', data: { state }, fields: ACTION_FORMS.transition(state),
      title: t('act.transition_title', { state: enumLabel('order', state) }), body: item.order_no + ' · ' + enumLabel('order', item.state) + ' → ' + enumLabel('order', state),
      danger: state === 'cancelled' || state === 'rejected', reload,
    });
    const statusUrl = '/' + (String(item.locale || 'ko').startsWith('en') ? 'en' : 'ko') + '/order-status.html?no=' + encodeURIComponent(item.order_no || '');
    root.appendChild(detailHead({
      crumbs: [{ href: '#/orders', text: t('entity.orders') }], code: item.order_no || item.id, title: item.company || item.contact || '—',
      pill: statusPill('order', item.state, true), archived: !!item.archived_at,
      meta: [planName(item.plan), item.currency, enumLabel('method', item.method), fmtDateTime(item.created_at)].filter(Boolean).join(' · '),
      actions: [link(statusUrl, t('act.order_page'), { class: 'btn', target: '_blank', rel: 'noopener' }), editButton('orders', item, reload), archiveButton('orders', item, reload, '/orders')],
    }));
    const trans = el('div', { class: 'transitions' }, el('span', { class: 'muted small', style: { alignSelf: 'center' } }, t('act.transition') + ':'),
      allowed.length ? allowed.map((s) => btn(enumLabel('order', s), () => go(s), 'btn-sm' + (s === 'cancelled' || s === 'rejected' ? ' btn-danger' : s === 'active' || s === 'paid' || s === 'contract_signed' ? ' btn-primary' : ''))) : el('span', { class: 'muted small' }, t('state.none')));
    const d = item.discount || {}; const fm = item.first_month || {};
    const quote = facts([
      { label: 'col.plan', value: planName(item.plan) }, { label: 'col.currency', value: item.currency, mono: true },
      { label: 'col.voice_minutes', value: fmtNum(item.voice_minutes), mono: true }, { label: 'col.alimtalk', value: fmtNum(item.alimtalk), mono: true },
      { label: 'col.monthly_net', value: fmtMoney(item.monthly_net, item.currency), mono: true }, { label: 'col.monthly_tax', value: fmtMoney(item.monthly_tax, item.currency), mono: true },
      { label: 'col.monthly_total', value: fmtMoney(item.monthly_total, item.currency), mono: true }, { label: 'col.after_discount', value: fmtMoney(item.after_discount, item.currency), mono: true },
      { label: 'col.discount', value: d.percent != null ? d.percent + '% · ' + t('misc.months', { n: d.months || 0 }) : null, mono: true },
      { label: 'col.first_month', value: fm.total != null ? fmtMoney(fm.total, item.currency) + ' (' + t('misc.days', { n: fm.days || 0 }) + ' / ' + (fm.monthDays || 0) + ')' : null, mono: true },
      { label: 'col.tax_treatment', value: enumLabel('tax', item.tax_treatment) }, { label: 'col.tax_rate', value: item.tax_rate == null ? null : fmtPct(item.tax_rate), mono: true },
    ]);
    const blocked = item.blocked_reason || item.block_reason || item.blocked;
    const left = el('div', { class: 'stack' },
      card({ title: t('tab.overview'), body: [trans, blocked ? el('p', { class: 'mt-s', style: { color: 'var(--red)' } }, t('ord.blocked') + ': ' + String(blocked)) : null, el('hr'), facts([
        { label: 'col.buyer_type', value: enumLabel('buyer', item.buyer_type) }, { label: 'col.locale', value: langLabel(item.locale) },
        { label: 'col.company', value: item.company }, { label: 'col.ceo', value: item.ceo },
        { label: 'col.contact', value: item.contact }, { label: 'col.email', value: item.email ? link('mailto:' + item.email, item.email) : null },
        { label: 'col.phone', value: item.phone, mono: true }, { label: 'col.tax_email', value: item.tax_email },
        { label: 'col.tax_id', value: item.tax_id, mono: true }, { label: 'col.method', value: enumLabel('method', item.method) },
        { label: 'col.billing_country', value: countryName(item.billing_country) }, { label: 'col.service_country', value: countryName(item.service_country) },
        { label: 'col.billing_address', value: item.billing_address }, { label: 'col.customer', value: item.customer_id ? customerLink(item.customer_id, (item.customer_code || '') + ' ' + (rel.customer && rel.customer.company ? rel.customer.company : '')) : null },
        { label: 'col.assignee', value: item.assignee || t('misc.unassigned') }, { label: 'col.next_action_at', value: fmtDateTime(item.next_action_at), mono: true },
        { label: 'col.note', value: item.note, pre: true }, { label: 'col.owner_note', value: item.owner_note, pre: true },
      ])] }),
      card({ title: t('tab.quote'), body: quote }));
    const events = (rel.events || []).map((e) => ({ when: e.created_at, what: enumLabel('order', e.from_state) + ' → ' + enumLabel('order', e.to_state) + (e.actor ? ' · ' + e.actor : ''), why: e.reason }));
    const tb = tabs([
      { id: 'events', label: t('tab.events'), count: events.length, render: (p) => p.appendChild(timeline(events.concat(baseTimeline(item, rel)))) },
      { id: 'jobs', label: t('tab.jobs'), count: (rel.jobs || []).length, render: (p) => p.appendChild(staticTable(LIST.jobs.columns.filter((c) => c.key !== 'order_no'), rel.jobs || [])) },
      { id: 'numbers', label: t('tab.numbers'), count: (rel.numbers || []).length, render: (p) => p.appendChild(staticTable(LIST.numbers.columns.filter((c) => c.key !== 'order_no'), rel.numbers || [])) },
    ]);
    const right = el('div', { class: 'stack' }, notesPanel('order', item.id, rel.notes, reload), tasksPanel('order', item.id, rel.tasks, reload));
    root.appendChild(el('div', { class: 'grid grid-side' }, el('div', { class: 'stack' }, left, card({ body: tb.root })), right));
  });
}
