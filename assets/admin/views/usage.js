/* views/usage.js — tenants' usage by month with limit meter, number
   pool, provisioning jobs; refresh button. */
import { el, btn } from '../dom.js';
import { t } from '../i18n.js';
import { DataTable } from '../table.js';
import { LIST, apiFilter } from '../schema-list.js';
import { ACTION_FORMS } from '../schema-form.js';
import { monthOf } from '../format.js';
import { navigate, replaceQuery } from '../router.js';
import { stateFromQuery, queryFromState } from './list.js';
import { runAction } from './detail.js';

const TABS = ['usage', 'numbers', 'jobs', 'tenants'];

export function renderUsage(root, ctx) {
  const tab = TABS.includes(ctx.params.tab) ? ctx.params.tab : 'usage';
  const seg = el('div', { class: 'seg', role: 'tablist' }, TABS.map((id) => el('button', { type: 'button', role: 'tab', 'aria-selected': id === tab ? 'true' : 'false', 'aria-pressed': id === tab ? 'true' : 'false', onClick: () => navigate('/usage' + (id === 'usage' ? '' : '/' + id)) }, t(id === 'tenants' ? 'entity.tenants' : id === 'usage' ? 'entity.usage' : 'usage.' + id))));
  const actions = [];
  let table;
  if (tab === 'usage') {
    actions.push(btn(t('act.usage_refresh'), () => runAction({
      entity: 'usage', id: null, action: 'usage.refresh', fields: ACTION_FORMS.usage_refresh((table && table.state.filter.month) || monthOf()),
      title: t('act.usage_refresh'), body: t('act.usage_refresh_body', { month: (table && table.state.filter.month) || monthOf() }), toast: t('toast.refreshed'), reload: () => table && table.reload(),
    }), 'btn-primary'));
  }
  root.appendChild(el('div', { class: 'page-head' }, el('div', null, el('h1', null, t('usage.title')), tab === 'usage' ? el('div', { class: 'sub' }, t('usage.limit_note')) : null), el('div', { class: 'page-actions' }, seg, actions)));
  const entity = tab;
  const schema = LIST[entity];
  const state = stateFromQuery(ctx.query, schema);
  if (entity === 'usage' && !state.filter.month) state.filter.month = monthOf();
  table = new DataTable({
    entity, columns: schema.columns, filters: schema.filters, state, mapFilter: (f) => apiFilter(entity, f),
    onState: (s) => replaceQuery(queryFromState(s)),
    onRow: entity === 'tenants' || entity === 'usage' ? (r) => { if (r.customer_id) navigate('/customers/' + r.customer_id); } : (entity === 'jobs' || entity === 'numbers') ? (r) => { if (r.order_id) navigate('/orders/' + r.order_id); } : null,
  });
  table.mount(root);
}
