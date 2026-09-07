/* views/index.js — route name -> render(root, ctx). */
import { renderDashboard } from './dashboard.js';
import { listView } from './list.js';
import { renderLead } from './leads.js';
import { renderOrder } from './orders.js';
import { renderCustomer } from './customers.js';
import { renderSubscription } from './subscriptions.js';
import { renderInvoices, renderInvoice } from './invoices.js';
import { renderInvoicePrint } from './invoice-print.js';
import { renderUsage } from './usage.js';
import { renderStats } from './stats.js';
import { renderMarketing, renderCampaign } from './marketing.js';
import { renderSettings } from './settings.js';

export const VIEWS = {
  dashboard: renderDashboard,
  leads: listView('leads', { detail: '/leads', create: true }),
  lead: renderLead,
  orders: listView('orders', { detail: '/orders' }),
  order: renderOrder,
  customers: listView('customers', { detail: '/customers', create: true }),
  customer: renderCustomer,
  subscriptions: listView('subscriptions', { detail: '/subscriptions' }),
  subscription: renderSubscription,
  invoices: renderInvoices,
  invoice: renderInvoice,
  invoicePrint: renderInvoicePrint,
  payments: listView('payments', { detail: '/invoices', detailKey: 'invoice_id', titleKey: 'nav.payments', tabsOf: 'invoices' }),
  tasks: listView('tasks', { titleKey: 'entity.tasks', onRow: (r) => { if (r.entity && r.entity_id) location.hash = '#/' + r.entity + 's/' + r.entity_id; } }),
  usage: renderUsage,
  stats: renderStats,
  marketing: renderMarketing,
  campaign: renderCampaign,
  settings: renderSettings,
};
