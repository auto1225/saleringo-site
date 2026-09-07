/* views/leads.js — lead detail: facts, message, UTM, status buttons,
   convert, spam, assignee/next action, notes, tasks, timeline. */
import { el, btn, link } from '../dom.js';
import { t, enumLabel } from '../i18n.js';
import { fmtDateTime, langLabel } from '../format.js';
import { statusPill, card, STATUS_KIND } from '../ui.js';
import { ACTION_FORMS } from '../schema-form.js';
import { loadDetail, detailHead, facts, runAction, editButton, archiveButton, notesPanel, tasksPanel, timeline, baseTimeline } from './detail.js';

export function renderLead(root, ctx) {
  loadDetail(root, 'leads', ctx.params.id, (item, rel, reload) => {
    const statuses = Object.keys(STATUS_KIND.lead).filter((s) => s !== item.status);
    const setStatus = (status) => runAction({
      entity: 'leads', id: item.id, action: 'leads.set_status', data: { status }, fields: ACTION_FORMS.set_status(status),
      title: t('act.set_status_title', { status: enumLabel('lead', status) }), body: status === 'spam' ? t('confirm.generic') : t('confirm.generic'), danger: status === 'spam' || status === 'lost', reload,
    });
    const actions = [
      item.converted_order_id ? null : btn(t('act.convert'), () => runAction({ entity: 'leads', id: item.id, action: 'leads.convert', title: t('act.convert'), body: t('act.convert_body'), reload }), 'btn-primary'),
      editButton('leads', item, reload),
      archiveButton('leads', item, reload, '/leads'),
    ];
    root.appendChild(detailHead({
      crumbs: [{ href: '#/leads', text: t('entity.leads') }], code: item.ref || item.id, title: item.company || item.name || item.email || '—',
      pill: statusPill('lead', item.status, true), archived: !!item.archived_at,
      meta: [langLabel(item.locale), item.source, fmtDateTime(item.created_at)].filter(Boolean).join(' · '), actions,
    }));
    const trans = el('div', { class: 'transitions' }, el('span', { class: 'muted small', style: { alignSelf: 'center' } }, t('act.set_status') + ':'),
      statuses.map((s) => btn(enumLabel('lead', s), () => setStatus(s), 'btn-sm' + (s === 'spam' || s === 'lost' ? ' btn-danger' : ''))));
    const campaign = rel.campaign ? link('#/marketing/campaigns/' + rel.campaign.id, rel.campaign.name || rel.campaign.id) : (item.campaign_id ? link('#/marketing/campaigns/' + item.campaign_id, item.campaign_id) : null);
    const converted = rel.converted_order ? link('#/orders/' + rel.converted_order.id, rel.converted_order.order_no || rel.converted_order.id) : (item.converted_order_id ? link('#/orders/' + item.converted_order_id, item.converted_order_id) : null);
    const left = el('div', { class: 'stack' },
      card({ title: t('tab.overview'), body: [trans, el('hr'), facts([
        { label: 'col.name', value: item.name }, { label: 'col.company', value: item.company },
        { label: 'col.email', value: item.email ? link('mailto:' + item.email, item.email) : null }, { label: 'col.phone', value: item.phone, mono: true },
        { label: 'col.industry', value: item.industry }, { label: 'col.locale', value: langLabel(item.locale) },
        { label: 'col.source', value: item.source }, { label: 'col.campaign', value: campaign },
        { label: 'col.assignee', value: item.assignee || t('misc.unassigned') }, { label: 'col.next_action_at', value: fmtDateTime(item.next_action_at), mono: true },
        { label: 'col.lost_reason', value: item.lost_reason }, { label: 'col.converted_order', value: converted },
        { label: 'col.page_url', value: item.page_url ? link(item.page_url, item.page_url, { target: '_blank', rel: 'noopener' }) : null },
        { label: 'col.referrer', value: item.referrer },
        { label: 'lead.consent', value: item.consent == null ? null : (item.consent ? t('misc.yes') : t('misc.no')) },
        { label: 'col.created_at', value: fmtDateTime(item.created_at), mono: true },
      ])] }),
      card({ title: t('col.message'), body: el('pre', { style: { whiteSpace: 'pre-wrap', margin: 0, font: 'inherit' } }, item.message || '—') }),
      card({ title: t('col.utm'), body: el('pre', { class: 'mono small', style: { whiteSpace: 'pre-wrap', margin: 0 } }, item.utm ? (typeof item.utm === 'string' ? item.utm : JSON.stringify(item.utm, null, 2)) : '—') }),
      card({ title: t('col.owner_note'), body: el('pre', { style: { whiteSpace: 'pre-wrap', margin: 0, font: 'inherit' } }, item.owner_note || '—') }));
    const right = el('div', { class: 'stack' },
      notesPanel('lead', item.id, rel.notes, reload),
      tasksPanel('lead', item.id, rel.tasks, reload),
      card({ title: t('tab.timeline'), body: timeline(baseTimeline(item, rel)) }));
    root.appendChild(el('div', { class: 'grid grid-side' }, left, right));
  });
}
