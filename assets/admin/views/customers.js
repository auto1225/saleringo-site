/* views/customers.js — customer detail: profile, tax, tenant link,
   tabs for orders/subscriptions/invoices/payments/usage/tenant, notes,
   tasks, timeline, generate invoice. */
import { el, btn, link } from '../dom.js';
import { t, enumLabel } from '../i18n.js';
import { api } from '../api.js';
import { fmtDateTime, fmtDate, fmtMoney, countryName, langLabel, monthOf } from '../format.js';
import { statusPill, card, tabs, toastError } from '../ui.js';
import { staticTable } from '../table.js';
import { LIST } from '../schema-list.js';
import { ACTION_FORMS } from '../schema-form.js';
import { barChart } from '../charts.js';
import { navigate } from '../router.js';
import { loadDetail, detailHead, facts, runAction, editButton, archiveButton, notesPanel, tasksPanel, timeline, baseTimeline } from './detail.js';

export async function generateInvoice(customerId, reload) {
  let customers = [];
  try { customers = customerId ? [] : (await api.list('customers', { status: 'active' }, 'company:asc', 1, 200)).rows; } catch (e) { toastError(e); return; }
  const fields = ACTION_FORMS.generate(customers).filter((f) => !(customerId && f.key === 'customer_id'));
  const r = await runAction({
    entity: 'invoices', id: null, action: 'invoices.generate', data: customerId ? { customer_id: customerId } : {}, fields, values: { month: monthOf() },
    title: t('act.generate'), body: t('act.generate_body'), confirmLabel: t('act.generate'),
  });
  if (r && r.item && r.item.id) navigate('/invoices/' + r.item.id); else if (reload) reload();
}

export function renderCustomer(root, ctx) {
  loadDetail(root, 'customers', ctx.params.id, (item, rel, reload) => {
    const linkTenant = btn(t('act.link_tenant'), async () => {
      let tenants = [];
      try { tenants = (await api.list('tenants', {}, 'name:asc', 1, 200)).rows; } catch (e) { toastError(e); return; }
      runAction({ entity: 'customers', id: item.id, action: 'customers.link_tenant', fields: ACTION_FORMS.link_tenant(tenants), title: t('act.link_tenant'), body: t('act.link_tenant_body'), reload });
    });
    root.appendChild(detailHead({
      crumbs: [{ href: '#/customers', text: t('entity.customers') }], code: item.code || item.id, title: item.company || item.contact_name || '—',
      pill: statusPill('cust', item.status, true), archived: !!item.archived_at,
      meta: [countryName(item.country), item.currency, langLabel(item.lang), fmtDate(item.created_at)].filter(Boolean).join(' · '),
      actions: [btn(t('act.generate'), () => generateInvoice(item.id, reload), 'btn-primary'), linkTenant, editButton('customers', item, reload), archiveButton('customers', item, reload, '/customers')],
    }));
    const tenant = rel.tenant || null;
    const profile = facts([
      { label: 'col.company', value: item.company }, { label: 'col.contact_name', value: item.contact_name },
      { label: 'col.email', value: item.email ? link('mailto:' + item.email, item.email) : null }, { label: 'col.phone', value: item.phone, mono: true },
      { label: 'col.country', value: countryName(item.country) }, { label: 'col.currency', value: item.currency, mono: true },
      { label: 'col.lang', value: langLabel(item.lang) }, { label: 'col.source', value: item.source },
      { label: 'col.tags', value: Array.isArray(item.tags) && item.tags.length ? el('span', { class: 'tags' }, item.tags.map((x) => el('span', { class: 'tag' }, x))) : null },
      { label: 'col.tenant', value: tenant ? el('span', null, tenant.name, ' ', el('span', { class: 'mono muted small' }, tenant.phone_number || '')) : (item.tenant_name || item.tenant_id) },
      { label: 'col.subscription', value: item.subscription_plan ? el('span', null, enumLabel('sub', item.subscription_status), ' · ', item.subscription_plan) : null },
      { label: 'col.receivable', value: fmtMoney(item.receivable, item.currency), mono: true },
      { label: 'col.owner_note', value: item.owner_note, pre: true },
    ]);
    const tax = facts([
      { label: 'col.buyer_type', value: enumLabel('buyer', item.buyer_type) }, { label: 'col.tax_id', value: item.tax_id, mono: true },
      { label: 'col.tax_treatment', value: enumLabel('tax', item.tax_treatment) }, { label: 'col.billing_address', value: item.billing_address, pre: true },
    ]);
    const usage = rel.usage || [];
    const tb = tabs([
      { id: 'orders', label: t('tab.orders'), count: (rel.orders || []).length, render: (p) => p.appendChild(staticTable(LIST.orders.columns.filter((c) => c.key !== 'company'), rel.orders || [], { onRow: (r) => navigate('/orders/' + r.id) })) },
      { id: 'subs', label: t('tab.subscriptions'), count: (rel.subscriptions || []).length, render: (p) => p.appendChild(staticTable(LIST.subscriptions.columns.filter((c) => c.key !== 'company' && c.key !== 'customer_code'), rel.subscriptions || [], { onRow: (r) => navigate('/subscriptions/' + r.id) })) },
      { id: 'invoices', label: t('tab.invoices'), count: (rel.invoices || []).length, render: (p) => p.appendChild(staticTable(LIST.invoices.columns.filter((c) => c.key !== 'company'), rel.invoices || [], { onRow: (r) => navigate('/invoices/' + r.id) })) },
      { id: 'payments', label: t('tab.payments'), count: (rel.payments || []).length, render: (p) => p.appendChild(staticTable(LIST.payments.columns.filter((c) => c.key !== 'company'), rel.payments || [], { onRow: (r) => navigate('/invoices/' + r.invoice_id) })) },
      { id: 'usage', label: t('tab.usage'), count: usage.length, render: (p) => {
        if (usage.length) p.appendChild(el('div', { class: 'mb' }, barChart({ label: t('tab.usage'), categories: usage.map((u) => String(u.month).slice(2, 7)), series: [{ label: t('col.conversations'), values: usage.map((u) => u.conversations || 0) }, { label: t('col.calls'), values: usage.map((u) => u.calls || 0) }] })));
        p.appendChild(staticTable(LIST.usage.columns.filter((c) => c.key !== 'tenant_name' && c.key !== 'company'), usage));
      } },
      { id: 'tenant', label: t('tab.tenant'), render: (p) => p.appendChild(tenant ? facts([
        { label: 'col.name', value: tenant.name }, { label: 'col.plan_type', value: tenant.plan_type }, { label: 'col.industry', value: tenant.industry },
        { label: 'col.phone_number', value: tenant.phone_number, mono: true }, { label: 'col.ai_phone', value: tenant.ai_phone == null ? null : (tenant.ai_phone ? t('misc.yes') : t('misc.no')) },
        { label: 'col.created_at', value: fmtDateTime(tenant.created_at), mono: true }, { label: 'col.tenant_id', value: tenant.id, mono: true },
        { label: 'misc.open_in_ops', value: link('https://saleringo.com/admin', t('nav.ops'), { target: '_blank', rel: 'noopener' }) },
      ]) : el('p', { class: 'muted' }, t('state.none'))) },
    ]);
    const left = el('div', { class: 'stack' },
      el('div', { class: 'grid grid-2' }, card({ title: t('cust.profile'), body: profile }), card({ title: t('cust.taxinfo'), body: tax })),
      card({ body: tb.root }));
    const right = el('div', { class: 'stack' }, notesPanel('customer', item.id, rel.notes, reload), tasksPanel('customer', item.id, rel.tasks, reload),
      card({ title: t('tab.timeline'), body: timeline(baseTimeline(item, rel).concat((rel.orders || []).map((o) => ({ when: o.created_at, what: t('entity.order') + ' ' + (o.order_no || ''), dim: true })), (rel.payments || []).map((p) => ({ when: p.received_at, what: enumLabel('pay', p.kind) + ' ' + fmtMoney(p.amount, p.currency) })))) }));
    root.appendChild(el('div', { class: 'grid grid-side' }, left, right));
  });
}
