/* views/detail.js — shared pieces of every detail page: loading wrapper,
   header, facts list, notes composer, tasks panel, timeline, edit and
   archive actions. Every write confirms in a modal and re-fetches. */
import { el, clear, btn, link } from '../dom.js';
import { t, enumLabel } from '../i18n.js';
import { api } from '../api.js';
import { fmtDateTime, fmtDate, isPast } from '../format.js';
import { modal, confirmDialog, toast, toastError, loadingEl, errorEl, card, statusPill } from '../ui.js';
import { FORMS } from '../schema-form.js';
import { navigate } from '../router.js';

/** Fetch entity+id, render via fn(item, related, reload). Handles loading/error. */
export function loadDetail(root, entity, id, fn) {
  let seq = 0;
  async function reload() {
    const my = ++seq;
    clear(root); root.appendChild(loadingEl());
    try {
      const r = await api.get(entity, id);
      if (my !== seq) return;
      clear(root);
      fn(r.item, r.related || {}, reload);
    } catch (err) {
      if (my !== seq) return;
      clear(root); root.appendChild(errorEl(err, reload));
    }
  }
  reload();
  return reload;
}

/** Header: crumbs, code, title with pill, meta, action buttons. */
export function detailHead(o) {
  return el('div', { class: 'detail-head' },
    el('div', null,
      o.crumbs ? el('div', { class: 'crumbs' }, o.crumbs.map((c, i) => [i ? ' / ' : null, c.href ? link(c.href, c.text) : el('span', null, c.text)])) : null,
      o.code ? el('div', { class: 'code' }, o.code) : null,
      el('h1', null, o.title || '—', o.pill || null, o.archived ? statusPill('user', 'disabled') : null),
      o.meta ? el('div', { class: 'meta' }, o.meta) : null),
    el('div', { class: 'page-actions' }, o.actions || []));
}

/** facts([{label, value, mono, pre}]) -> <dl class="facts">. label = i18n key or text. */
export function facts(items) {
  return el('dl', { class: 'facts' }, items.filter(Boolean).map((f) => el('div', null,
    el('dt', null, f.labelText != null ? f.labelText : t(f.label)),
    el('dd', { class: f.mono ? 'num' : null }, f.pre ? el('pre', null, f.value == null ? '—' : String(f.value)) : (f.value == null || f.value === '' ? '—' : f.value)))));
}

/** Generic "run an action" with confirm modal. Returns the response or null. */
export async function runAction(o) {
  const res = await modal({
    title: o.title, body: o.body || t('confirm.generic'), fields: o.fields || null, values: o.values || null, danger: o.danger, wide: o.wide,
    confirmLabel: o.confirmLabel || t('btn.confirm'),
    onSubmit: async (data) => api.action(o.entity, o.id, o.action, Object.assign({}, o.data || {}, typeof data === 'object' ? data : {})),
  });
  if (!res) return null;
  toast(o.toast || t('toast.done'));
  if (o.reload) o.reload();
  return res;
}

export function editButton(entity, item, reload, opts) {
  return btn(t('btn.edit'), async () => {
    const r = await modal({
      title: t('act.edit_title', { entity: t('entity.' + entity.replace(/s$/, '')) }), fields: FORMS[entity](Object.assign({ editing: true }, opts || {})), values: item, wide: true,
      confirmLabel: t('btn.save'), onSubmit: (data) => api.save(entity, item.id, data),
    });
    if (r) { toast(t('toast.saved')); reload(); }
  });
}
export function archiveButton(entity, item, reload, listPath) {
  const archived = !!item.archived_at;
  return btn(archived ? t('btn.restore') : t('btn.archive'), async () => {
    const ok = await confirmDialog(archived ? t('btn.restore') : t('btn.archive'), t(archived ? 'confirm.restore' : 'confirm.archive'), { danger: !archived });
    if (!ok) return;
    try { await api.action(entity, item.id, entity + (archived ? '.restore' : '.archive'), {}); toast(t('toast.done')); if (archived || !listPath) reload(); else navigate(listPath); }
    catch (e) { toastError(e); }
  }, archived ? '' : 'btn-danger');
}

/** Notes: list + composer (no confirm — notes are the exception). */
export function notesPanel(entity, entityId, notes, reload) {
  const ta = el('textarea', { placeholder: t('btn.add_note'), 'aria-label': t('btn.add_note'), rows: 2 });
  const send = btn(t('btn.add_note'), async () => {
    const body = ta.value.trim(); if (!body) { ta.focus(); return; }
    send.disabled = true;
    try { await api.save('notes', null, { entity, entity_id: entityId, body }); toast(t('toast.note_added')); reload(); }
    catch (e) { toastError(e); send.disabled = false; }
  }, 'btn-primary btn-sm');
  ta.addEventListener('keydown', (e) => { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) send.click(); });
  const list = (notes || []).length
    ? el('div', null, notes.map((n) => el('div', { class: 'note' }, el('div', { class: 'by' }, (n.author || '—') + ' · ' + fmtDateTime(n.created_at)), el('div', { class: 'body' }, n.body || ''))))
    : el('p', { class: 'muted' }, t('state.none'));
  return card({ title: t('tab.notes'), body: [list, el('div', { class: 'composer' }, ta, el('div', { class: 'row', style: { justifyContent: 'flex-end' } }, send))] });
}

/** Tasks: list with done/reopen + add button (confirm via modal form). */
export function tasksPanel(entity, entityId, tasks, reload) {
  const add = btn(t('btn.add_task'), async () => {
    const r = await modal({ title: t('btn.add_task'), fields: FORMS.tasks({ entity, entity_id: entityId }), confirmLabel: t('btn.save'), onSubmit: (d) => api.save('tasks', null, d) });
    if (r) { toast(t('toast.saved')); reload(); }
  }, 'btn-sm');
  const rows = (tasks || []).map((tk) => {
    const done = !!tk.done_at;
    const late = !done && tk.due_at && isPast(tk.due_at);
    return el('div', { class: 'task' + (done ? ' done' : '') },
      el('div', { class: 'grow' }, el('div', { class: 'title' }, enumLabel('task', tk.kind) + ' · ' + (tk.title || '')),
        el('div', { class: 'due' + (late ? ' late' : '') }, (tk.due_at ? fmtDateTime(tk.due_at) : '—') + (tk.assignee ? ' · ' + tk.assignee : '') + (late ? ' · ' + t('misc.overdue') : '')),
        tk.note ? el('div', { class: 'small muted' }, tk.note) : null),
      btn(done ? t('btn.reopen') : t('btn.done'), () => runAction({ entity: 'tasks', id: tk.id, action: done ? 'tasks.reopen' : 'tasks.done', title: t(done ? 'act.task_reopen' : 'act.task_done'), body: tk.title, reload }), 'btn-sm'));
  });
  return card({ title: t('tab.tasks'), actions: add, body: rows.length ? rows : el('p', { class: 'muted' }, t('state.none')) });
}

/** timeline([{when, what, why, dim}]) newest first. */
export function timeline(items) {
  const sorted = (items || []).filter((i) => i.when).sort((a, b) => new Date(b.when) - new Date(a.when));
  if (!sorted.length) return el('p', { class: 'muted' }, t('state.none'));
  return el('ul', { class: 'timeline' }, sorted.map((i) => el('li', { class: i.dim ? 'dim' : null },
    el('div', { class: 'when' }, fmtDateTime(i.when)), el('div', { class: 'what' }, i.what), i.why ? el('div', { class: 'why' }, i.why) : null)));
}

/** Timeline items from notes + tasks + creation. */
export function baseTimeline(item, related) {
  const out = [];
  if (item.created_at) out.push({ when: item.created_at, what: t('col.created_at'), dim: true });
  (related.notes || []).forEach((n) => out.push({ when: n.created_at, what: t('entity.note') + ' · ' + (n.author || ''), why: n.body }));
  (related.tasks || []).forEach((k) => { if (k.done_at) out.push({ when: k.done_at, what: t('btn.done') + ' · ' + (k.title || ''), dim: true }); });
  return out;
}

export function customerLink(id, label) { return id ? link('#/customers/' + id, label || t('entity.customer')) : el('span', { class: 'muted' }, '—'); }
export { fmtDate };
