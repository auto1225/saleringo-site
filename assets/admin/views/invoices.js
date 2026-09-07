/* views/invoices.js — invoice list (with generate) and invoice detail:
   lines editor for drafts, issue, record payment, refund, void, print,
   payments, notes. Totals shown here are previews; the server recomputes. */
import { el, btn, link } from '../dom.js';
import { t, enumLabel } from '../i18n.js';
import { api } from '../api.js';
import { fmtDate, fmtDateTime, fmtMoney, fmtPct } from '../format.js';
import { statusPill, card, modal, toast } from '../ui.js';
import { staticTable } from '../table.js';
import { LIST, LINE_KINDS } from '../schema-list.js';
import { ACTION_FORMS } from '../schema-form.js';
import { listView } from './list.js';
import { generateInvoice } from './customers.js';
import { loadDetail, detailHead, facts, runAction, editButton, customerLink, notesPanel } from './detail.js';

const list = listView('invoices', { detail: '/invoices', tabsOf: 'invoices' });
export function renderInvoices(root, ctx) {
  const table = list(root, ctx);
  const head = root.querySelector('.page-actions');
  head.appendChild(btn(t('act.generate'), () => generateInvoice(null, () => table.reload()), 'btn-primary'));
  head.appendChild(link('#/invoices?status=overdue', t('inv.receivable_view'), { class: 'btn' }));
  root.insertBefore(el('p', { class: 'muted small', style: { marginTop: '-8px', marginBottom: '12px' } }, t('act.psp_note')), root.children[1]);
}

function sum(lines) { return (lines || []).reduce((a, l) => a + (Number(l.amount) || 0), 0); }
function round(v, cur) { return cur === 'KRW' ? Math.round(v) : Math.round(v * 100) / 100; }

/** Editable lines table for drafts. Returns {root, get()}. */
function linesEditor(lines, cur) {
  const rows = (lines || []).map((l) => Object.assign({}, l));
  const body = el('tbody');
  const totalCell = el('td', { class: 'num' });
  function recalc() { totalCell.textContent = fmtMoney(round(sum(rows), cur), cur); }
  function draw() {
    body.textContent = '';
    rows.forEach((l, i) => {
      const kind = el('select', { 'aria-label': t('col.kind') }, LINE_KINDS.map((k) => el('option', { value: k }, enumLabel('line', k)))); kind.value = l.kind || 'other';
      const label = el('input', { type: 'text', value: l.label || '', 'aria-label': t('col.lines') });
      const qty = el('input', { type: 'number', step: 'any', class: 'mono', value: l.qty == null ? '' : l.qty, 'aria-label': t('inv.qty'), style: { width: '80px' } });
      const unit = el('input', { type: 'number', step: 'any', class: 'mono', value: l.unit == null ? '' : l.unit, 'aria-label': t('inv.unit'), style: { width: '110px' } });
      const amount = el('input', { type: 'number', step: 'any', class: 'mono', value: l.amount == null ? '' : l.amount, 'aria-label': t('col.amount'), style: { width: '130px' } });
      const upd = () => { l.kind = kind.value; l.label = label.value; l.qty = qty.value === '' ? null : Number(qty.value); l.unit = unit.value === '' ? null : Number(unit.value);
        if (l.qty != null && l.unit != null) { l.amount = round(l.qty * l.unit, cur); amount.value = l.amount; } else l.amount = amount.value === '' ? null : Number(amount.value); recalc(); };
      [kind, label, qty, unit].forEach((n) => n.addEventListener('input', upd));
      amount.addEventListener('input', () => { l.amount = amount.value === '' ? null : Number(amount.value); recalc(); });
      body.appendChild(el('tr', null, el('td', null, kind), el('td', null, label), el('td', null, qty), el('td', null, unit), el('td', null, amount),
        el('td', null, btn(t('act.remove_line'), () => { rows.splice(i, 1); draw(); recalc(); }, 'btn-sm btn-ghost'))));
    });
    body.appendChild(el('tr', null, el('td', { colspan: '4', class: 'right' }, el('b', null, t('inv.subtotal'))), totalCell, el('td')));
    recalc();
  }
  draw();
  const root = el('div', { class: 'tbl-wrap' }, el('table', { class: 'tbl' }, el('thead', null, el('tr', null, el('th', null, t('col.kind')), el('th', null, t('col.lines')), el('th', null, t('inv.qty')), el('th', null, t('inv.unit')), el('th', null, t('col.amount')), el('th'))), body));
  return { root, get: () => rows.map((l) => ({ kind: l.kind || 'other', label: l.label || '', qty: l.qty, unit: l.unit, amount: l.amount })), add: () => { rows.push({ kind: 'other', label: '', qty: 1, unit: null, amount: null }); draw(); } };
}

export function renderInvoice(root, ctx) {
  loadDetail(root, 'invoices', ctx.params.id, (item, rel, reload) => {
    const cur = item.currency || 'KRW';
    const st = item.status;
    const act = (action, title, body, fields, danger, values) => runAction({ entity: 'invoices', id: item.id, action: 'invoices.' + action, title, body, fields, danger, values, reload });
    const balance = round((Number(item.total) || 0) - (Number(item.paid_amount) || 0), cur);
    const actions = [];
    if (st === 'draft') actions.push(btn(t('act.issue'), () => act('issue', t('act.issue'), t('act.issue_body')), 'btn-primary'));
    if (st === 'issued' || st === 'partially_paid' || st === 'overdue') actions.push(btn(t('act.record_payment'), () => act('record_payment', t('act.record_payment'), (item.invoice_no || '') + ' · ' + t('col.balance') + ' ' + fmtMoney(balance, cur), ACTION_FORMS.record_payment(cur), false, { amount: balance }), 'btn-primary'));
    if (st === 'paid' || st === 'partially_paid') actions.push(btn(t('act.refund'), () => act('refund', t('act.refund'), item.invoice_no || '', ACTION_FORMS.refund(), true, { amount: item.paid_amount })));
    if (st === 'draft' || st === 'issued' || st === 'overdue') actions.push(btn(t('act.void'), () => act('void', t('act.void'), t('act.void_body'), null, true), 'btn-danger'));
    if (st === 'draft') actions.push(editButton('invoices', item, reload));
    actions.push(link('#/invoices/' + item.id + '/print', t('btn.print'), { class: 'btn' }));
    root.appendChild(detailHead({
      crumbs: [{ href: '#/invoices', text: t('entity.invoices') }], code: item.invoice_no || t('inv.draft'), title: item.company || '—',
      pill: statusPill('inv', st, true), archived: !!item.archived_at,
      meta: [fmtDate(item.period_start) + ' – ' + fmtDate(item.period_end), cur, item.due_at ? t('inv.pay_by', { date: fmtDate(item.due_at) }) : null].filter(Boolean).join(' · '), actions,
    }));
    root.appendChild(el('p', { class: 'muted small' }, t('act.psp_note')));

    let linesNode;
    if (st === 'draft') {
      const ed = linesEditor(item.lines, cur);
      linesNode = el('div', null, ed.root, el('div', { class: 'row mt-s' }, btn(t('act.add_line'), ed.add, 'btn-sm'),
        btn(t('act.save_lines'), async () => {
          const r = await modal({ title: t('act.save_lines'), body: t('confirm.save'), confirmLabel: t('btn.save'), onSubmit: () => api.save('invoices', item.id, { lines: ed.get() }) });
          if (r) { toast(t('toast.saved')); reload(); }
        }, 'btn-sm btn-primary')));
    } else {
      linesNode = staticTable([
        { key: 'kind', type: 'enum', prefix: 'line' }, { key: 'label', type: 'text', label: 'col.lines', wrap: true }, { key: 'qty', type: 'num', label: 'inv.qty', digits: 2 },
        { key: 'unit', type: 'money', label: 'inv.unit', currency: cur }, { key: 'amount', type: 'money', currency: cur },
      ], item.lines || []);
    }
    const totals = el('div', { class: 'invoice-doc', style: { padding: '0', border: 0, boxShadow: 'none', background: 'none', color: 'inherit', maxWidth: 'none' } },
      el('div', { class: 'totals', style: { marginLeft: 'auto' } },
        el('div', null, el('span', null, t('inv.subtotal')), el('span', { class: 'mono' }, fmtMoney(item.net, cur))),
        el('div', null, el('span', null, t('inv.tax_line', { rate: fmtPct(item.tax_rate || 0, 0) })), el('span', { class: 'mono' }, fmtMoney(item.tax, cur))),
        el('div', { class: 'grand' }, el('span', null, t('inv.grand')), el('span', { class: 'mono' }, fmtMoney(item.total, cur))),
        el('div', null, el('span', null, t('inv.paid_line')), el('span', { class: 'mono' }, fmtMoney(item.paid_amount, cur))),
        el('div', null, el('span', null, t('inv.balance_line')), el('span', { class: 'mono', style: { color: balance > 0 ? 'var(--amber)' : 'inherit' } }, fmtMoney(balance, cur)))));
    const left = el('div', { class: 'stack' },
      card({ title: t('tab.lines'), body: [linesNode, totals] }),
      card({ title: t('tab.overview'), body: facts([
        { label: 'col.customer', value: customerLink(item.customer_id, (item.customer_code || '') + ' ' + (item.company || '')) },
        { label: 'col.subscription', value: item.subscription_id ? link('#/subscriptions/' + item.subscription_id, t('entity.subscription')) : null },
        { label: 'col.order', value: item.order_id ? link('#/orders/' + item.order_id, t('entity.order')) : null },
        { label: 'col.period', value: fmtDate(item.period_start) + ' – ' + fmtDate(item.period_end), mono: true },
        { label: 'col.issued_at', value: fmtDateTime(item.issued_at), mono: true }, { label: 'col.due_at', value: fmtDate(item.due_at), mono: true },
        { label: 'col.paid_at', value: fmtDateTime(item.paid_at), mono: true }, { label: 'col.method', value: enumLabel('method', item.method) },
        { label: 'col.provider', value: item.provider }, { label: 'col.provider_ref', value: item.provider_ref, mono: true },
        { label: 'col.tax_document', value: item.tax_document, mono: true }, { label: 'col.tax_rate', value: fmtPct(item.tax_rate || 0, 0), mono: true },
        { label: 'col.note', value: item.note, pre: true },
      ]) }));
    const right = el('div', { class: 'stack' },
      card({ title: t('tab.payments'), body: staticTable(LIST.payments.columns.filter((c) => c.key !== 'company' && c.key !== 'invoice_no'), rel.payments || []) }),
      notesPanel('invoice', item.id, rel.notes, reload));
    root.appendChild(el('div', { class: 'grid grid-side' }, left, right));
  });
}
