/* ui.js — toast, modal (focus trap, Esc, Enter), pills, tabs, states,
   cards. Every write in the app goes through modal() so the confirm
   step is never skipped by accident. */
import { el, clear, btn, glyph } from './dom.js';
import { t, enumLabel, pick } from './i18n.js';
import { buildForm } from './form.js';
import { ApiError, errorMessage } from './api.js';

/* ── Toast ───────────────────────────────────────────────────────── */
let toastRoot = null;
export function toast(msg, opts) {
  const o = opts || {};
  if (!toastRoot) { toastRoot = el('div', { class: 'toasts', 'aria-live': 'polite', role: 'status' }); document.body.appendChild(toastRoot); }
  const node = el('div', { class: 'toast' + (o.kind === 'err' ? ' err' : '') }, el('span', null, msg));
  if (o.action) node.appendChild(el('button', { type: 'button', class: 'btn-link', onClick: () => { remove(); o.action.fn(); } }, o.action.label));
  node.appendChild(el('button', { type: 'button', class: 'btn-link', 'aria-label': t('btn.close'), onClick: () => remove() }, glyph('close', 14)));
  toastRoot.appendChild(node);
  let timer = setTimeout(remove, o.timeout || (o.kind === 'err' ? 8000 : 4000));
  function remove() { clearTimeout(timer); if (node.parentNode) node.parentNode.removeChild(node); }
  return remove;
}
export function toastError(err, retry) {
  return toast(errorMessage(err), { kind: 'err', action: retry ? { label: t('btn.retry'), fn: retry } : null });
}

/* ── Modal ───────────────────────────────────────────────────────── */
const FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]):not([type=hidden]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';
let openCount = 0;

/**
 * modal({title, body (string|node), fields, values, confirmLabel, cancelLabel,
 *        danger, wide, single, onSubmit(data) -> may throw ApiError})
 * Resolves with form data (or true) on confirm, null on cancel.
 */
export function modal(o) {
  return new Promise((resolve) => {
    const prev = document.activeElement;
    const form = o.fields && o.fields.length ? buildForm(o.fields, o.values, { single: o.single }) : null;
    const errLine = el('p', { class: 'err-line', role: 'alert' });
    const okBtn = btn(o.confirmLabel || t('btn.confirm'), submit, o.danger ? 'btn-danger' : 'btn-primary');
    const cancelBtn = btn(o.cancelLabel || t('btn.cancel'), () => close(null));
    const bodyNode = el('div', { class: 'modal-body' }, typeof o.body === 'string' ? el('p', null, o.body) : o.body, form ? form.root : null);
    const box = el('div', { class: 'modal' + (o.wide ? ' wide' : ''), role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'mtitle' },
      el('div', { class: 'modal-head' }, el('h2', { id: 'mtitle' }, o.title || t('confirm.title'))),
      bodyNode, errLine,
      el('div', { class: 'modal-foot' }, cancelBtn, okBtn));
    const back = el('div', { class: 'modal-back' }, box);
    back.addEventListener('mousedown', (e) => { if (e.target === back) close(null); });
    document.addEventListener('keydown', onKey, true);
    document.body.appendChild(back);
    openCount++;
    if (form) form.focusFirst(); else okBtn.focus();

    let busy = false;
    async function submit() {
      if (busy) return;
      if (form && !form.validate()) return;
      const data = form ? form.get() : true;
      if (!o.onSubmit) return close(data);
      busy = true; okBtn.disabled = true; errLine.textContent = '';
      try {
        const r = await o.onSubmit(data);
        close(r === undefined ? data : r);
      } catch (err) {
        busy = false; okBtn.disabled = false;
        errLine.textContent = errorMessage(err);
        if (form && err instanceof ApiError && err.fields) form.setErrors(err.fields);
        if (!box.contains(document.activeElement)) okBtn.focus();
      }
    }
    function onKey(e) {
      if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); close(null); return; }
      const inside = box.contains(e.target);
      if (e.key === 'Enter' && inside && !e.shiftKey && e.target.tagName !== 'TEXTAREA' && e.target.tagName !== 'BUTTON' && e.target.tagName !== 'A') { e.preventDefault(); submit(); return; }
      if (e.key === 'Tab' && !inside) { e.preventDefault(); const f = box.querySelector(FOCUSABLE); if (f) f.focus(); return; }
      if (e.key === 'Tab') {
        const items = Array.from(box.querySelectorAll(FOCUSABLE)).filter((n) => n.offsetParent !== null);
        if (!items.length) return;
        const first = items[0], last = items[items.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    }
    function close(v) {
      if (!back.parentNode) return;
      document.removeEventListener('keydown', onKey, true);
      back.parentNode.removeChild(back);
      openCount--;
      if (prev && prev.focus) prev.focus();
      resolve(v);
    }
  });
}
export function confirmDialog(title, body, opts) {
  return modal(Object.assign({ title, body }, opts || {})).then((v) => v != null);
}
export function modalOpen() { return openCount > 0; }

/* ── Pills ───────────────────────────────────────────────────────── */
export const STATUS_KIND = {
  lead: { new: 'info', contacted: 'neutral', qualified: 'info', proposal: 'warn', won: 'good', lost: 'bad', spam: 'neutral' },
  order: { received: 'info', under_review: 'warn', proposal_sent: 'warn', contract_sent: 'warn', contract_signed: 'good', payment_pending: 'warn', paid: 'good', active: 'good', cancelled: 'neutral', rejected: 'bad' },
  cust: { lead: 'neutral', trial: 'info', active: 'good', paused: 'warn', churned: 'bad' },
  sub: { pending: 'neutral', trial: 'info', active: 'good', paused: 'warn', canceled: 'bad' },
  inv: { draft: 'neutral', issued: 'info', paid: 'good', partially_paid: 'warn', overdue: 'bad', void: 'neutral', refunded: 'warn' },
  camp: { planned: 'neutral', active: 'good', paused: 'warn', ended: 'neutral' },
  job: { pending: 'neutral', running: 'info', done: 'good', failed: 'bad', needs_human: 'warn' },
  num: { available: 'good', assigned: 'info', reserved: 'warn', released: 'neutral', porting: 'warn' },
  user: { active: 'good', disabled: 'neutral' },
  pay: { payment: 'good', refund: 'warn' },
  voice: { live: 'good', soon: 'warn', no: 'neutral' },
};
export function pill(kind, label, lg) {
  return el('span', { class: 'pill pill-' + (kind || 'neutral') + (lg ? ' pill-lg' : '') }, label);
}
export function statusPill(prefix, value, lg) {
  if (value == null || value === '') return el('span', { class: 'muted' }, '—');
  const map = STATUS_KIND[prefix] || {};
  return pill(map[value] || 'neutral', enumLabel(prefix, value), lg);
}

/* ── Tabs ────────────────────────────────────────────────────────── */
/** tabs([{id, label, count, render(panel)}], {initial, onChange}) */
export function tabs(defs, opts) {
  const o = opts || {};
  const bar = el('div', { class: 'tabs', role: 'tablist' });
  const panel = el('div', { role: 'tabpanel' });
  let cur = null;
  const buttons = {};
  defs.forEach((d) => {
    const b = el('button', { type: 'button', role: 'tab', 'aria-selected': 'false', id: 'tab_' + d.id, onClick: () => select(d.id) },
      d.label, d.count != null ? el('span', { class: 'n' }, String(d.count)) : null);
    buttons[d.id] = b; bar.appendChild(b);
  });
  bar.addEventListener('keydown', (e) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    const ids = defs.map((d) => d.id); const i = ids.indexOf(cur);
    const n = ids[(i + (e.key === 'ArrowRight' ? 1 : ids.length - 1)) % ids.length];
    select(n); buttons[n].focus();
  });
  function select(id) {
    const d = defs.find((x) => x.id === id) || defs[0];
    if (!d) return;
    cur = d.id;
    defs.forEach((x) => buttons[x.id].setAttribute('aria-selected', x.id === cur ? 'true' : 'false'));
    clear(panel);
    d.render(panel);
    if (o.onChange) o.onChange(cur);
  }
  const root = el('div', null, bar, panel);
  select(o.initial || (defs[0] && defs[0].id));
  return { root, panel, select, current: () => cur };
}

/* ── States ──────────────────────────────────────────────────────── */
export function loadingEl(inline) {
  return el('div', { class: 'state' + (inline ? ' inline' : ''), 'aria-busy': 'true' }, el('div', { class: 'spinner', 'aria-hidden': 'true' }), el('span', null, t('state.loading')));
}
export function emptyEl(msg, hint) {
  return el('div', { class: 'state' }, el('b', null, msg || t('state.empty')), hint === false ? null : el('span', null, hint || t('state.empty_hint')));
}
export function errorEl(err, retry) {
  return el('div', { class: 'state error' }, el('b', null, t('state.error')), el('span', null, errorMessage(err)),
    retry ? btn(t('btn.retry'), retry, 'btn-sm') : null);
}

/* ── Cards ───────────────────────────────────────────────────────── */
export function card(o) {
  const c = el('div', { class: 'card' + (o.flat ? ' flat' : '') + (o.cls ? ' ' + o.cls : '') });
  if (o.title || o.actions) c.appendChild(el('div', { class: 'card-head' }, el('h3', null, o.title || ''), o.actions ? el('div', { class: 'row' }, o.actions) : null));
  const body = el('div', { class: 'card-body' }, o.body);
  c.appendChild(body);
  c.body = body;
  return c;
}
export function sectionTitle(text, right) {
  return el('div', { class: 'section-title' }, el('h2', null, text), right ? el('div', { class: 'more' }, right) : null);
}
export function serverMsg(obj, fallback) { return pick(obj, fallback); }
