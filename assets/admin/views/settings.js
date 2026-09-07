/* views/settings.js — account (password), company, notifications/SLA,
   admin users (owner), audit log, system state, ops link. */
import { el, btn, link, clear } from '../dom.js';
import { t, enumLabel } from '../i18n.js';
import { api, health } from '../api.js';
import { fmtDateTime } from '../format.js';
import { card, modal, toast, loadingEl, errorEl } from '../ui.js';
import { buildForm } from '../form.js';
import { DataTable, staticTable } from '../table.js';
import { LIST, apiFilter } from '../schema-list.js';
import { FORMS, ACTION_FORMS } from '../schema-form.js';
import { navigate, replaceQuery } from '../router.js';
import { stateFromQuery, queryFromState } from './list.js';
import { facts } from './detail.js';

const TABS = ['account', 'company', 'notify', 'users', 'audit', 'system'];

export function renderSettings(root, ctx) {
  const tab = TABS.includes(ctx.params.tab) ? ctx.params.tab : 'account';
  const seg = el('div', { class: 'seg', role: 'tablist' }, TABS.map((id) => el('button', { type: 'button', role: 'tab', 'aria-selected': id === tab ? 'true' : 'false', 'aria-pressed': id === tab ? 'true' : 'false', onClick: () => navigate('/settings' + (id === 'account' ? '' : '/' + id)) }, t('tab.' + id))));
  root.appendChild(el('div', { class: 'page-head' }, el('div', null, el('h1', null, t('settings.title'))), el('div', { class: 'page-actions' }, seg)));
  const body = el('div'); root.appendChild(body);
  ({ account, company, notify, users, audit, system })[tab](body, ctx);
}

function account(body, ctx) {
  const u = ctx.user || {};
  const form = buildForm(ACTION_FORMS.password(), {}, { single: true });
  const save = btn(t('btn.change_pw'), async () => {
    if (!form.validate()) return;
    const d = form.get();
    const r = await modal({ title: t('btn.change_pw'), body: t('confirm.generic'), onSubmit: () => api.password(d.current, d.new).catch((e) => { if (e && e.fields) form.setErrors(e.fields); throw e; }) });
    if (r) { toast(t('toast.pw_changed')); form.set({ current: '', new: '', new2: '' }); ctx.refreshMe().catch(() => {}); }
  }, 'btn-primary');
  form.root.addEventListener('keydown', (e) => { if (e.key === 'Enter' && e.target.tagName === 'INPUT') { e.preventDefault(); save.click(); } });
  body.appendChild(el('div', { class: 'grid grid-2' },
    card({ title: t('settings.account'), body: facts([{ label: 'col.username', value: u.username, mono: true }, { label: 'col.display_name', value: u.display_name }, { label: 'col.email', value: u.email }, { label: 'col.role', value: enumLabel('role', u.role) }]) }),
    card({ title: t('btn.change_pw'), body: [form.root, el('div', { class: 'row mt-s', style: { justifyContent: 'flex-end' } }, save)] })));
}

function settingsForm(body, key, fields, title, transform) {
  clear(body); body.appendChild(loadingEl());
  api.settingsGet().then((r) => {
    clear(body);
    const cur = (r.settings && r.settings[key]) || {};
    const form = buildForm(fields, transform ? transform.toForm(cur) : cur);
    const save = btn(t('btn.save'), async () => {
      if (!form.validate()) return;
      const data = form.get();
      const ok = await modal({ title, body: t('confirm.save'), confirmLabel: t('btn.save'), onSubmit: () => api.settingsSet(key, transform ? transform.fromForm(data) : data) });
      if (ok) toast(t('toast.saved'));
    }, 'btn-primary');
    body.appendChild(card({ title, body: [form.root, el('div', { class: 'row mt', style: { justifyContent: 'flex-end' } }, save)] }));
  }).catch((err) => { clear(body); body.appendChild(errorEl(err, () => settingsForm(body, key, fields, title, transform))); });
}
function company(body) {
  settingsForm(body, 'company', [
    { key: 'name', type: 'text', label: 'settings.company_name', required: true }, { key: 'ceo', type: 'text', label: 'settings.company_ceo' },
    { key: 'tax_id', type: 'text', label: 'settings.company_tax_id' }, { key: 'phone', type: 'tel', label: 'settings.company_phone' },
    { key: 'email', type: 'email', label: 'settings.company_email' }, { key: 'bank', type: 'text', label: 'settings.company_bank' },
    { key: 'address', type: 'textarea', label: 'settings.company_address', span2: true, rows: 2 }, { key: 'note', type: 'textarea', label: 'settings.company_note', span2: true, rows: 2 },
  ], t('settings.company'));
}
function notify(body) {
  const rangeOpts = ['this_month', 'last_month', 'last_90', 'this_year'].map((v) => ({ value: v, label: t('range.' + v) }));
  clear(body); body.appendChild(loadingEl());
  api.settingsGet().then((r) => {
    clear(body);
    const s = r.settings || {};
    const form = buildForm([
      { key: 'emails', type: 'text', label: 'settings.notify_emails', hint: 'settings.notify_hint', span2: true },
      { key: 'range', type: 'select', label: 'settings.dashboard', options: rangeOpts, allowEmpty: false },
      { key: 'lead_hours', type: 'number', label: 'settings.sla_hours', min: 1 }, { key: 'review_hours', type: 'number', label: 'settings.sla_review', min: 1 },
    ], { emails: ((s.notify && s.notify.emails) || []).join(', '), range: (s.dashboard && s.dashboard.range) || 'this_month', lead_hours: s.pipeline_sla && s.pipeline_sla.lead_hours, review_hours: s.pipeline_sla && s.pipeline_sla.review_hours });
    const save = btn(t('btn.save'), async () => {
      if (!form.validate()) return;
      const d = form.get();
      const ok = await modal({ title: t('settings.notify'), body: t('confirm.save'), confirmLabel: t('btn.save'), onSubmit: async () => {
        await api.settingsSet('notify', { emails: (d.emails || '').split(',').map((x) => x.trim()).filter(Boolean) });
        await api.settingsSet('dashboard', { range: d.range });
        await api.settingsSet('pipeline_sla', { lead_hours: d.lead_hours, review_hours: d.review_hours });
      } });
      if (ok) toast(t('toast.saved'));
    }, 'btn-primary');
    body.appendChild(card({ title: t('settings.notify') + ' · ' + t('settings.sla'), body: [form.root, el('div', { class: 'row mt', style: { justifyContent: 'flex-end' } }, save)] }));
  }).catch((err) => { clear(body); body.appendChild(errorEl(err, () => notify(body))); });
}
function users(body, ctx) {
  const isOwner = ctx.user && ctx.user.role === 'owner';
  if (!isOwner) { body.appendChild(card({ title: t('settings.users'), body: el('p', { class: 'muted' }, t('settings.users_owner_only')) })); return; }
  const box = el('div');
  async function load() {
    clear(box); box.appendChild(loadingEl());
    try {
      const r = await api.usersGet();
      clear(box);
      box.appendChild(staticTable(LIST.users.columns, r.users || [], { onRow: (u) => edit(u) }));
    } catch (err) { clear(box); box.appendChild(errorEl(err, load)); }
  }
  async function edit(u) {
    const r = await modal({ title: u ? t('act.edit_title', { entity: t('entity.user') }) : t('settings.user_new'), fields: FORMS.users({ editing: !!u }), values: u || { role: 'staff', status: 'active' }, wide: true,
      confirmLabel: t('btn.save'), onSubmit: (d) => api.usersSave(u ? u.id : null, d) });
    if (r) { toast(t('toast.saved')); load(); }
  }
  body.appendChild(card({ title: t('settings.users'), actions: btn(t('settings.user_new'), () => edit(null), 'btn-primary btn-sm'), flat: true, body: box }));
  load();
}
function audit(body, ctx) {
  const schema = LIST.audit;
  body.appendChild(el('h2', { class: 'mb-s' }, t('settings.audit')));
  new DataTable({ entity: 'audit', columns: schema.columns, filters: schema.filters, state: stateFromQuery(ctx.query, schema), mapFilter: (f) => apiFilter('audit', f), onState: (s) => replaceQuery(queryFromState(s)) }).mount(body);
}
function system(body) {
  clear(body); body.appendChild(loadingEl());
  health().then((h) => {
    clear(body);
    const yn = (v) => (v == null ? '—' : v ? t('misc.yes') : t('misc.no'));
    const notifyRows = h.notify && typeof h.notify === 'object' ? Object.keys(h.notify).map((k) => ({ labelText: k, value: yn(h.notify[k]) })) : [];
    body.appendChild(el('div', { class: 'grid grid-2' },
      card({ title: t('settings.system'), body: facts([
        { labelText: 'DB', value: yn(h.db) }, { label: 'dash.pricing_version', value: h.pricingVersion, mono: true },
        { label: 'dash.policy_version', value: h.policyVersion, mono: true }, { label: 'settings.users', value: h.adminUsers, mono: true },
        { label: 'col.computed_at', value: fmtDateTime(new Date()), mono: true },
      ].concat(notifyRows)) }),
      card({ title: t('nav.ops'), body: [el('p', null, t('settings.ops_hint')), link('https://saleringo.com/admin', t('settings.ops_link'), { class: 'btn', target: '_blank', rel: 'noopener' })] })));
  }).catch((err) => { clear(body); body.appendChild(errorEl(err, () => system(body))); });
}
