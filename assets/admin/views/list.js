/* views/list.js — generic list page for an entity: title, "new" button,
   DataTable with filters from schema, list state kept in the hash query. */
import { el, btn, link } from '../dom.js';
import { t } from '../i18n.js';
import { api } from '../api.js';
import { DataTable } from '../table.js';
import { LIST, apiFilter } from '../schema-list.js';
import { FORMS } from '../schema-form.js';
import { modal, toast } from '../ui.js';
import { navigate, replaceQuery } from '../router.js';

const META = ['sort', 'page', 'size'];

/** Split hash query into table state. */
export function stateFromQuery(query, schema) {
  const filter = {};
  Object.keys(query || {}).forEach((k) => { if (!META.includes(k)) filter[k] = query[k]; });
  return { filter, sort: query.sort || schema.sort || null, page: Number(query.page) || 1, size: Number(query.size) || 50 };
}
export function queryFromState(s) {
  return Object.assign({}, s.filter, { sort: s.sort || null, page: s.page > 1 ? s.page : null, size: s.size !== 50 ? s.size : null });
}

/** Create-entity modal; navigates to the new detail on success. */
export async function createEntity(entity, detailPath, defaults, opts) {
  const fields = FORMS[entity](opts || {});
  const item = await modal({
    title: t('act.new_title', { entity: t('entity.' + entity.replace(/s$/, '')) }), fields, values: defaults || {}, wide: true,
    confirmLabel: t('btn.save'),
    onSubmit: async (data) => (await api.save(entity, null, data)).item,
  });
  if (!item) return null;
  toast(t('toast.saved'));
  if (detailPath && item.id) navigate(detailPath + '/' + item.id);
  return item;
}

/** listView(entity, {detail, detailKey, create, titleKey, tabsOf, fixed, extra}) -> render(root, ctx) */
export function listView(entity, o) {
  return function render(root, ctx) {
    const schema = LIST[entity];
    const title = t(o.titleKey || 'entity.' + entity);
    const actions = [];
    if (o.create) actions.push(btn(t('btn.new'), () => createEntity(entity, o.detail), 'btn-primary'));
    root.appendChild(el('div', { class: 'page-head' }, el('div', null, el('h1', null, title)), el('div', { class: 'page-actions' }, actions)));
    if (o.tabsOf === 'invoices') root.appendChild(invoiceTabs(entity));
    const table = new DataTable({
      entity, columns: schema.columns, filters: schema.filters, fixed: o.fixed || null,
      state: stateFromQuery(ctx.query, schema), mapFilter: (f) => apiFilter(entity, f),
      onRow: o.onRow ? o.onRow : (r) => navigate(o.detail + '/' + (o.detailKey ? r[o.detailKey] : r.id)),
      onState: (s) => replaceQuery(queryFromState(s)),
      extra: o.extra ? o.extra(ctx) : null,
    });
    table.mount(root);
    return table;
  };
}

export function invoiceTabs(active) {
  return el('div', { class: 'seg mb', role: 'tablist' },
    el('a', { href: '#/invoices', class: 'btn btn-sm' + (active === 'invoices' ? ' on' : ''), role: 'tab', 'aria-selected': active === 'invoices' ? 'true' : 'false', style: { border: 0, borderRadius: 0 } }, t('entity.invoices')),
    el('a', { href: '#/payments', class: 'btn btn-sm' + (active === 'payments' ? ' on' : ''), role: 'tab', 'aria-selected': active === 'payments' ? 'true' : 'false', style: { border: 0, borderRadius: 0 } }, t('entity.payments')));
}

export { link };
