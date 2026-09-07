/* schema-list.js — columns and filters per entity for DataTable.
   Column: {key, type, label?, prefix?, currency?, sub?, wrap?, sortable?}
   Filter: {key, type:'text'|'select'|'country'|'plan'|'currency'|'lang'|'date'|'month'|'checkbox', values?, prefix?, options?} */
import { STATUS_KIND } from './ui.js';

const LEAD = Object.keys(STATUS_KIND.lead), ORDER = Object.keys(STATUS_KIND.order), CUST = Object.keys(STATUS_KIND.cust);
const SUB = Object.keys(STATUS_KIND.sub), INV = Object.keys(STATUS_KIND.inv), CAMP = Object.keys(STATUS_KIND.camp);
const JOB = Object.keys(STATUS_KIND.job), NUM = Object.keys(STATUS_KIND.num);
export const CHANNELS = ['search', 'social', 'email', 'referral', 'event', 'partner', 'content', 'other'];
export const TASK_KINDS = ['call', 'email', 'followup', 'contract', 'provisioning', 'billing', 'other'];
export const METHODS = ['card', 'transfer', 'other'];
export const ENTITIES = ['lead', 'order', 'customer', 'invoice'];
export const ROLES = ['owner', 'staff', 'viewer'];
export const TAX = ['vat_charged', 'reverse_charge', 'none', 'exempt'];
export const BUYER = ['business', 'individual'];
export const LINE_KINDS = ['plan', 'voice', 'alimtalk', 'overage', 'setup', 'credit', 'other'];

const q = { key: 'q', type: 'text' };
const range = [{ key: 'from', type: 'date' }, { key: 'to', type: 'date' }];
const archived = { key: 'archived', type: 'checkbox' };

export const LIST = {
  leads: {
    sort: 'created_at:desc',
    columns: [
      { key: 'ref', type: 'text', mono: true }, { key: 'company', type: 'sub', sub: 'name' }, { key: 'email', type: 'text' },
      { key: 'locale', type: 'lang' }, { key: 'source', type: 'text' }, { key: 'status', type: 'status', prefix: 'lead' },
      { key: 'assignee', type: 'text', dim: true }, { key: 'next_action_at', type: 'datetime' }, { key: 'created_at', type: 'datetime' },
    ],
    filters: [q, { key: 'status', type: 'select', values: LEAD, prefix: 'lead' }, { key: 'lang', type: 'lang' }, { key: 'source', type: 'text' }, { key: 'country', type: 'country' }, ...range, archived],
  },
  orders: {
    sort: 'created_at:desc',
    columns: [
      { key: 'order_no', type: 'text', mono: true }, { key: 'company', type: 'sub', sub: 'contact' }, { key: 'state', type: 'status', prefix: 'order' },
      { key: 'plan', type: 'plan' }, { key: 'billing_country', type: 'country' }, { key: 'currency', type: 'text', mono: true },
      { key: 'method', type: 'enum', prefix: 'method' }, { key: 'monthly_total', type: 'money' }, { key: 'assignee', type: 'text', dim: true }, { key: 'created_at', type: 'datetime' },
    ],
    filters: [q, { key: 'state', type: 'select', values: ORDER, prefix: 'order' }, { key: 'country', type: 'country' }, { key: 'plan', type: 'plan' }, { key: 'currency', type: 'currency' },
      { key: 'method', type: 'select', values: METHODS, prefix: 'method' }, ...range, archived],
  },
  customers: {
    sort: 'created_at:desc',
    columns: [
      { key: 'code', type: 'text', mono: true }, { key: 'company', type: 'sub', sub: 'contact_name' }, { key: 'email', type: 'text' }, { key: 'country', type: 'country' },
      { key: 'status', type: 'status', prefix: 'cust' }, { key: 'subscription_plan', type: 'plan', label: 'col.plan' }, { key: 'subscription_status', type: 'status', prefix: 'sub', label: 'col.subscription' },
      { key: 'open_invoices', type: 'num' }, { key: 'receivable', type: 'money' }, { key: 'tags', type: 'tags', sortable: false }, { key: 'created_at', type: 'date' },
    ],
    filters: [q, { key: 'status', type: 'select', values: CUST, prefix: 'cust' }, { key: 'country', type: 'country' }, { key: 'plan', type: 'plan' }, { key: 'tag', type: 'text', labelText: null }, archived],
  },
  subscriptions: {
    sort: 'started_at:desc',
    columns: [
      { key: 'customer_code', type: 'text', mono: true }, { key: 'company', type: 'text' }, { key: 'plan', type: 'plan' }, { key: 'currency', type: 'text', mono: true },
      { key: 'list_price', type: 'money' }, { key: 'discount_percent', type: 'pctRaw' }, { key: 'status', type: 'status', prefix: 'sub' },
      { key: 'started_at', type: 'date' }, { key: 'current_period_end', type: 'date', label: 'col.current_period' }, { key: 'cancel_at', type: 'date' }, { key: 'tenant_name', type: 'text', label: 'col.tenant', dim: true },
    ],
    filters: [q, { key: 'status', type: 'select', values: SUB, prefix: 'sub' }, { key: 'plan', type: 'plan' }, { key: 'currency', type: 'currency' }],
  },
  invoices: {
    sort: 'issued_at:desc',
    columns: [
      { key: 'invoice_no', type: 'text', mono: true }, { key: 'company', type: 'sub', sub: 'customer_code' }, { key: 'period_start', type: 'date', label: 'col.period' },
      { key: 'currency', type: 'text', mono: true }, { key: 'total', type: 'money' }, { key: 'paid_amount', type: 'money' }, { key: 'status', type: 'status', prefix: 'inv' },
      { key: 'issued_at', type: 'date' }, { key: 'due_at', type: 'date' },
    ],
    filters: [q, { key: 'status', type: 'select', values: INV, prefix: 'inv' }, { key: 'currency', type: 'currency' }, ...range],
  },
  payments: {
    sort: 'received_at:desc',
    columns: [
      { key: 'received_at', type: 'datetime' }, { key: 'invoice_no', type: 'text', mono: true }, { key: 'company', type: 'text' }, { key: 'kind', type: 'status', prefix: 'pay' },
      { key: 'amount', type: 'money' }, { key: 'method', type: 'enum', prefix: 'method' }, { key: 'provider', type: 'text', dim: true }, { key: 'provider_ref', type: 'text', mono: true, dim: true },
    ],
    filters: [q, { key: 'kind', type: 'select', values: ['payment', 'refund'], prefix: 'pay' }, { key: 'method', type: 'select', values: METHODS, prefix: 'method' }, ...range],
  },
  campaigns: {
    sort: 'starts_on:desc',
    columns: [
      { key: 'name', type: 'text' }, { key: 'channel', type: 'enum', prefix: 'chan' }, { key: 'utm_campaign', type: 'text', mono: true }, { key: 'country', type: 'country' }, { key: 'lang', type: 'lang' },
      { key: 'status', type: 'status', prefix: 'camp' }, { key: 'budget', type: 'money' }, { key: 'starts_on', type: 'date' }, { key: 'ends_on', type: 'date' },
      { key: 'leads_count', type: 'num' }, { key: 'orders_count', type: 'num' },
    ],
    filters: [q, { key: 'status', type: 'select', values: CAMP, prefix: 'camp' }, { key: 'channel', type: 'select', values: CHANNELS, prefix: 'chan' }, { key: 'country', type: 'country' }, { key: 'lang', type: 'lang' }],
  },
  tasks: {
    sort: 'due_at:asc',
    columns: [
      { key: 'due_at', type: 'datetime' }, { key: 'kind', type: 'enum', prefix: 'task' }, { key: 'title', type: 'text', wrap: true }, { key: 'entity', type: 'enum', prefix: 'ent' },
      { key: 'assignee', type: 'text', dim: true }, { key: 'done_at', type: 'datetime' },
    ],
    filters: [q, { key: 'kind', type: 'select', values: TASK_KINDS, prefix: 'task' }, { key: 'entity', type: 'select', values: ENTITIES, prefix: 'ent' }, { key: 'assignee', type: 'text' }, { key: 'done', type: 'checkbox' }],
  },
  tenants: {
    sort: 'created_at:desc',
    columns: [
      { key: 'name', type: 'text' }, { key: 'plan_type', type: 'text' }, { key: 'industry', type: 'text', dim: true }, { key: 'phone_number', type: 'text', mono: true },
      { key: 'ai_phone', type: 'bool' }, { key: 'company', type: 'sub', sub: 'customer_code', label: 'col.customer' }, { key: 'calls_this_month', type: 'num' }, { key: 'conversations_this_month', type: 'num' }, { key: 'created_at', type: 'date' },
    ],
    filters: [q],
  },
  usage: {
    sort: 'conversations:desc',
    columns: [
      { key: 'tenant_name', type: 'sub', sub: 'company', label: 'col.tenant' }, { key: 'month', type: 'month' }, { key: 'calls', type: 'num' }, { key: 'voice_minutes', type: 'num' },
      { key: 'conversations', type: 'num' }, { key: 'chats_web', type: 'num' }, { key: 'chats_kakao', type: 'num' }, { key: 'chats_phone', type: 'num' }, { key: 'alimtalk', type: 'num' },
      { key: 'plan', type: 'plan' }, { key: 'limit_pct', type: 'meter' }, { key: 'computed_at', type: 'datetime', dim: true },
    ],
    filters: [q, { key: 'month', type: 'month' }, { key: 'plan', type: 'plan' }],
  },
  numbers: {
    sort: 'assigned_at:desc',
    columns: [
      { key: 'e164', type: 'text', mono: true }, { key: 'country', type: 'country' }, { key: 'provider', type: 'text' }, { key: 'status', type: 'status', prefix: 'num' },
      { key: 'tenant_name', type: 'text', label: 'col.tenant' }, { key: 'order_no', type: 'text', mono: true }, { key: 'assigned_at', type: 'date' }, { key: 'note', type: 'text', wrap: true, dim: true },
    ],
    filters: [q, { key: 'status', type: 'select', values: NUM, prefix: 'num' }, { key: 'country', type: 'country' }],
  },
  jobs: {
    sort: 'updated_at:desc',
    columns: [
      { key: 'updated_at', type: 'datetime' }, { key: 'order_no', type: 'text', mono: true }, { key: 'tenant_name', type: 'text', label: 'col.tenant' }, { key: 'step', type: 'text', mono: true },
      { key: 'status', type: 'status', prefix: 'job' }, { key: 'attempts', type: 'num' }, { key: 'needs_human', type: 'bool' }, { key: 'last_error', type: 'text', wrap: true, dim: true }, { key: 'due_at', type: 'datetime' },
    ],
    filters: [q, { key: 'status', type: 'select', values: JOB, prefix: 'job' }, { key: 'human', type: 'checkbox' }],
  },
  audit: {
    sort: 'at:desc',
    columns: [
      { key: 'at', type: 'datetime' }, { key: 'username', type: 'text' }, { key: 'action', type: 'text', mono: true }, { key: 'entity', type: 'text' },
      { key: 'entity_id', type: 'text', mono: true, dim: true }, { key: 'before', type: 'json', wrap: true, dim: true, sortable: false }, { key: 'after', type: 'json', wrap: true, sortable: false },
    ],
    filters: [q, { key: 'entity', type: 'text' }, ...range],
  },
  users: {
    sort: 'username:asc',
    columns: [
      { key: 'username', type: 'text', mono: true }, { key: 'display_name', type: 'text' }, { key: 'email', type: 'text' }, { key: 'role', type: 'enum', prefix: 'role' },
      { key: 'status', type: 'status', prefix: 'user' }, { key: 'must_change_password', type: 'bool' }, { key: 'last_login_at', type: 'datetime' },
    ],
    filters: [],
  },
};

/** Map filter keys the UI uses to what the API expects (jobs "human" -> kind). */
export function apiFilter(entity, f) {
  const out = Object.assign({}, f);
  if (entity === 'jobs' && out.human) { delete out.human; out.kind = 'needs_human'; }
  if (entity === 'customers' && out.tag) { out.q = out.q ? out.q + ' ' + out.tag : out.tag; delete out.tag; }
  return out;
}
