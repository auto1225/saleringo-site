/* views/marketing.js — campaigns (list, detail, UTM builder), sources
   report, pricing countries (read only). */
import { el, btn, link } from '../dom.js';
import { t, enumLabel, getLang, pick } from '../i18n.js';
import { fmtDate, fmtMoney, fmtNum, fmtPct, countryName, langLabel, rangePreset, getPricing } from '../format.js';
import { statusPill, card, toast } from '../ui.js';
import { DataTable, staticTable } from '../table.js';
import { LIST, apiFilter } from '../schema-list.js';
import { navigate, replaceQuery } from '../router.js';
import { stateFromQuery, queryFromState, createEntity } from './list.js';
import { loadDetail, detailHead, facts, editButton, archiveButton, notesPanel } from './detail.js';
import { reportBlock } from './stats.js';

const TABS = ['campaigns', 'sources', 'countries'];

export function buildUtm(url, source, medium, campaign) {
  const base = (url || '').trim(); if (!base) return '';
  const p = [];
  if (source) p.push('utm_source=' + encodeURIComponent(source));
  if (medium) p.push('utm_medium=' + encodeURIComponent(medium));
  if (campaign) p.push('utm_campaign=' + encodeURIComponent(campaign));
  if (!p.length) return base;
  return base + (base.includes('?') ? '&' : '?') + p.join('&');
}
async function copyText(s) {
  try { await navigator.clipboard.writeText(s); toast(t('toast.copied')); }
  catch (e) { const ta = el('textarea', { value: s, style: { position: 'fixed', opacity: 0 } }); document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); toast(t('toast.copied')); } catch (e2) { /* nothing */ } ta.remove(); }
}
export function utmBuilder(values) {
  const v = values || {};
  const url = el('input', { type: 'url', placeholder: 'https://claude.saleringo.com/ko/', value: v.landing_url || '', 'aria-label': t('col.landing_url') });
  const src = el('input', { type: 'text', placeholder: 'google', value: v.utm_source || '', 'aria-label': 'utm_source' });
  const med = el('input', { type: 'text', placeholder: 'cpc', value: v.utm_medium || '', 'aria-label': 'utm_medium' });
  const cam = el('input', { type: 'text', placeholder: 'spring-2026', value: v.utm_campaign || '', 'aria-label': 'utm_campaign' });
  const out = el('input', { type: 'text', readOnly: true, class: 'mono', 'aria-label': t('mkt.generated') });
  const upd = () => { out.value = buildUtm(url.value, src.value, med.value, cam.value); };
  [url, src, med, cam].forEach((i) => i.addEventListener('input', upd)); upd();
  return card({ title: t('mkt.utm_builder'), body: el('div', { class: 'form-grid' },
    el('div', { class: 'fld span2' }, el('label', null, t('col.landing_url')), url),
    el('div', { class: 'fld' }, el('label', null, 'utm_source'), src), el('div', { class: 'fld' }, el('label', null, 'utm_medium'), med), el('div', { class: 'fld' }, el('label', null, 'utm_campaign'), cam),
    el('div', { class: 'fld span2' }, el('label', null, t('mkt.generated')), el('div', { class: 'row' }, el('div', { style: { flex: '1 1 240px' } }, out), btn(t('btn.copy'), () => { if (out.value) copyText(out.value); }, 'btn-sm')))) });
}

function countriesTable() {
  const p = getPricing() || { countries: [], tax: {} };
  const rows = (p.countries || []).map((c) => ({ code: c.code, name: c.name[getLang()] || c.name.ko, currency: c.currency, voice: c.voice, tax: c.code === 'KR' && p.tax && p.tax.KR ? pick(p.tax.KR.label) : (c.reverseCharge ? t('tax.reverse_charge') : t('tax.none')), taxId: pick(c.taxIdLabel), dial: c.dial }));
  return staticTable([
    { key: 'code', type: 'text', mono: true }, { key: 'name', type: 'text', label: 'col.country' }, { key: 'currency', type: 'text', mono: true },
    { key: 'voice', type: 'status', prefix: 'voice' }, { key: 'tax', type: 'text', label: 'col.tax_label' }, { key: 'taxId', type: 'text', label: 'col.tax_id' }, { key: 'dial', type: 'text', mono: true },
  ], rows);
}

export function renderMarketing(root, ctx) {
  const tab = TABS.includes(ctx.params.tab) ? ctx.params.tab : 'campaigns';
  const seg = el('div', { class: 'seg', role: 'tablist' }, TABS.map((id) => el('button', { type: 'button', role: 'tab', 'aria-selected': id === tab ? 'true' : 'false', 'aria-pressed': id === tab ? 'true' : 'false', onClick: () => navigate('/marketing' + (id === 'campaigns' ? '' : '/' + id)) }, t('tab.' + id))));
  const actions = [seg];
  if (tab === 'campaigns') actions.push(btn(t('mkt.new_campaign'), () => createEntity('campaigns', '/marketing/campaigns', { status: 'planned', currency: 'KRW' }), 'btn-primary'));
  root.appendChild(el('div', { class: 'page-head' }, el('div', null, el('h1', null, t('mkt.title')), tab === 'countries' ? el('div', { class: 'sub' }, t('mkt.countries_note')) : null), el('div', { class: 'page-actions' }, actions)));
  if (tab === 'campaigns') {
    root.appendChild(el('div', { class: 'mb' }, utmBuilder()));
    const schema = LIST.campaigns;
    new DataTable({ entity: 'campaigns', columns: schema.columns, filters: schema.filters, state: stateFromQuery(ctx.query, schema), mapFilter: (f) => apiFilter('campaigns', f),
      onRow: (r) => navigate('/marketing/campaigns/' + r.id), onState: (s) => replaceQuery(queryFromState(s)) }).mount(root);
  } else if (tab === 'sources') {
    root.appendChild(reportBlock('marketing', rangePreset('this_year')));
  } else {
    root.appendChild(countriesTable());
  }
}

export function renderCampaign(root, ctx) {
  loadDetail(root, 'campaigns', ctx.params.id, (item, rel, reload) => {
    const leads = rel.leads_count != null ? rel.leads_count : item.leads_count;
    const orders = rel.orders_count != null ? rel.orders_count : item.orders_count;
    root.appendChild(detailHead({
      crumbs: [{ href: '#/marketing', text: t('mkt.title') }], code: item.utm_campaign || item.id, title: item.name || '—',
      pill: statusPill('camp', item.status, true), archived: !!item.archived_at,
      meta: [enumLabel('chan', item.channel), countryName(item.country), langLabel(item.lang), fmtDate(item.starts_on) + ' – ' + fmtDate(item.ends_on)].filter(Boolean).join(' · '),
      actions: [editButton('campaigns', item, reload), archiveButton('campaigns', item, reload, '/marketing')],
    }));
    const kpi = (label, value) => el('div', { class: 'card kpi' }, el('div', { class: 'lbl' }, label), el('div', { class: 'val' }, value));
    root.appendChild(el('div', { class: 'grid grid-3 mb' }, kpi(t('col.leads_count'), fmtNum(leads)), kpi(t('col.orders_count'), fmtNum(orders)), kpi(t('col.conversion'), leads ? fmtPct((orders || 0) / leads) : '—')));
    const left = el('div', { class: 'stack' },
      card({ title: t('tab.overview'), body: facts([
        { label: 'col.channel', value: enumLabel('chan', item.channel) }, { label: 'col.status', value: enumLabel('camp', item.status) },
        { label: 'col.utm_source', value: item.utm_source, mono: true }, { label: 'col.utm_medium', value: item.utm_medium, mono: true },
        { label: 'col.utm_campaign', value: item.utm_campaign, mono: true }, { label: 'col.budget', value: fmtMoney(item.budget, item.currency), mono: true },
        { label: 'col.country', value: countryName(item.country) }, { label: 'col.lang', value: langLabel(item.lang) },
        { label: 'col.starts_on', value: fmtDate(item.starts_on), mono: true }, { label: 'col.ends_on', value: fmtDate(item.ends_on), mono: true },
        { label: 'col.landing_url', value: item.landing_url ? link(item.landing_url, item.landing_url, { target: '_blank', rel: 'noopener' }) : null }, { label: 'col.note', value: item.note, pre: true },
      ]) }),
      utmBuilder(item),
      card({ title: t('tab.leads'), actions: link('#/leads?campaign_id=' + encodeURIComponent(item.id), t('btn.view_all')), body: staticTable(LIST.leads.columns.filter((c) => c.key !== 'assignee' && c.key !== 'next_action_at'), rel.recent_leads || [], { onRow: (r) => navigate('/leads/' + r.id) }) }));
    root.appendChild(el('div', { class: 'grid grid-side' }, left, el('div', { class: 'stack' }, notesPanel('campaign', item.id, rel.notes, reload))));
  });
}
