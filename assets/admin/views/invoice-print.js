/* views/invoice-print.js — clean A4 sheet: seller from settings.company,
   buyer, period, lines, totals, tax line. Print button; shell hidden. */
import { el, btn, link, clear } from '../dom.js';
import { t, enumLabel, getLang } from '../i18n.js';
import { api } from '../api.js';
import { fmtDate, fmtMoney, fmtNum, fmtPct, countryShort } from '../format.js';
import { loadingEl, errorEl } from '../ui.js';

export function renderInvoicePrint(root, ctx) {
  async function load() {
    clear(root); root.appendChild(loadingEl());
    try {
      const [inv, st] = await Promise.all([api.get('invoices', ctx.params.id), api.settingsGet().catch(() => ({ settings: {} }))]);
      clear(root);
      draw(root, inv.item, inv.related || {}, (st.settings && st.settings.company) || {});
    } catch (err) { clear(root); root.appendChild(errorEl(err, load)); }
  }
  load();
}

function draw(root, item, rel, co) {
  const cur = item.currency || 'KRW';
  const c = rel.customer || {};
  const balance = (Number(item.total) || 0) - (Number(item.paid_amount) || 0);
  root.appendChild(el('div', { class: 'row between no-print mb' },
    link('#/invoices/' + item.id, '← ' + t('btn.back'), { class: 'btn btn-sm' }),
    btn(t('btn.print'), () => window.print(), 'btn-primary')));
  const doc = el('article', { class: 'invoice-doc', lang: getLang() },
    el('div', { class: 'top' },
      el('div', null, el('h1', null, t('inv.print_title')), el('div', { class: 'mono' }, item.invoice_no || t('inv.draft'))),
      el('div', { class: 'right' },
        el('div', null, t('col.issued_at') + ': ', el('span', { class: 'mono' }, fmtDate(item.issued_at))),
        el('div', null, t('col.due_at') + ': ', el('span', { class: 'mono' }, fmtDate(item.due_at))),
        el('div', null, t('col.period') + ': ', el('span', { class: 'mono' }, fmtDate(item.period_start) + ' – ' + fmtDate(item.period_end))),
        el('div', null, t('col.status') + ': ', enumLabel('inv', item.status)))),
    el('div', { class: 'parties' },
      el('div', null, el('h4', null, t('inv.seller')),
        el('p', null, el('b', null, co.name || '—')), co.ceo ? el('p', null, t('settings.company_ceo') + ' ' + co.ceo) : null,
        co.tax_id ? el('p', { class: 'mono' }, co.tax_id) : null, co.address ? el('p', null, co.address) : null,
        co.email ? el('p', null, co.email) : null, co.phone ? el('p', { class: 'mono' }, co.phone) : null),
      el('div', null, el('h4', null, t('inv.buyer')),
        el('p', null, el('b', null, c.company || item.company || '—')), c.contact_name ? el('p', null, c.contact_name) : null,
        c.tax_id ? el('p', { class: 'mono' }, c.tax_id) : null, c.billing_address ? el('p', null, c.billing_address) : null,
        c.country ? el('p', null, countryShort(c.country)) : null, c.email ? el('p', null, c.email) : null)),
    el('table', null,
      el('thead', null, el('tr', null, el('th', null, t('col.kind')), el('th', null, t('col.lines')), el('th', { class: 'num' }, t('inv.qty')), el('th', { class: 'num' }, t('inv.unit')), el('th', { class: 'num' }, t('col.amount')))),
      el('tbody', null, (item.lines || []).map((l) => el('tr', null, el('td', null, enumLabel('line', l.kind)), el('td', null, l.label || ''),
        el('td', { class: 'num' }, l.qty == null ? '' : fmtNum(l.qty, 2)), el('td', { class: 'num' }, l.unit == null ? '' : fmtMoney(l.unit, cur)), el('td', { class: 'num' }, fmtMoney(l.amount, cur)))))),
    el('div', { class: 'totals' },
      el('div', null, el('span', null, t('inv.subtotal')), el('span', { class: 'mono' }, fmtMoney(item.net, cur))),
      el('div', null, el('span', null, t('inv.tax_line', { rate: fmtPct(item.tax_rate || 0, 0) })), el('span', { class: 'mono' }, fmtMoney(item.tax, cur))),
      el('div', { class: 'grand' }, el('span', null, t('inv.grand')), el('span', { class: 'mono' }, fmtMoney(item.total, cur))),
      Number(item.paid_amount) ? el('div', null, el('span', null, t('inv.paid_line')), el('span', { class: 'mono' }, fmtMoney(item.paid_amount, cur))) : null,
      Number(item.paid_amount) ? el('div', null, el('span', null, t('inv.balance_line')), el('span', { class: 'mono' }, fmtMoney(balance, cur))) : null),
    el('div', { class: 'foot' },
      co.bank ? el('p', null, t('settings.company_bank') + ': ', el('span', { class: 'mono' }, co.bank)) : null,
      item.due_at ? el('p', null, t('inv.pay_by', { date: fmtDate(item.due_at) })) : null,
      item.tax_document ? el('p', null, t('col.tax_document') + ': ', el('span', { class: 'mono' }, item.tax_document)) : null,
      el('p', null, co.note || t('inv.thanks'))));
  root.appendChild(doc);
}
