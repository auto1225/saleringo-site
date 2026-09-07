/* schema-form.js — field schemas for create/edit modals and action
   dialogs. Options are resolved at call time (language, pricing). */
import { t, enumLabel } from './i18n.js';
import { countryOptions, planOptions } from './format.js';
import { CHANNELS, TASK_KINDS, METHODS, ROLES, TAX, BUYER } from './schema-list.js';
import { STATUS_KIND } from './ui.js';

const opts = (prefix, values) => values.map((v) => ({ value: v, label: enumLabel(prefix, v) }));
const langOpts = () => [{ value: 'ko', label: t('misc.lang_ko') }, { value: 'en', label: t('misc.lang_en') }];
const curOpts = () => [{ value: 'KRW', label: 'KRW' }, { value: 'USD', label: 'USD' }];
const statusOpts = (prefix) => opts(prefix, Object.keys(STATUS_KIND[prefix]));

export const FORMS = {
  leads: () => [
    { key: 'name', type: 'text', required: true }, { key: 'company', type: 'text' },
    { key: 'email', type: 'email', required: true }, { key: 'phone', type: 'tel' },
    { key: 'industry', type: 'text' }, { key: 'locale', type: 'select', options: langOpts() },
    { key: 'source', type: 'text' }, { key: 'status', type: 'select', options: statusOpts('lead'), allowEmpty: false },
    { key: 'assignee', type: 'text' }, { key: 'next_action_at', type: 'datetime' },
    { key: 'campaign_id', type: 'text', label: 'col.campaign' }, { key: 'lost_reason', type: 'text' },
    { key: 'message', type: 'textarea', span2: true }, { key: 'owner_note', type: 'textarea', span2: true },
  ],
  orders: () => [
    { key: 'company', type: 'text', required: true }, { key: 'contact', type: 'text' },
    { key: 'email', type: 'email', required: true }, { key: 'phone', type: 'tel' },
    { key: 'ceo', type: 'text' }, { key: 'tax_id', type: 'text' }, { key: 'tax_email', type: 'email' },
    { key: 'billing_country', type: 'select', options: countryOptions() }, { key: 'service_country', type: 'select', options: countryOptions() },
    { key: 'billing_address', type: 'textarea', span2: true, rows: 2 },
    { key: 'assignee', type: 'text' }, { key: 'next_action_at', type: 'datetime' },
    { key: 'note', type: 'textarea', span2: true, rows: 2 }, { key: 'owner_note', type: 'textarea', span2: true },
  ],
  customers: () => [
    { key: 'company', type: 'text', required: true }, { key: 'contact_name', type: 'text' },
    { key: 'email', type: 'email', required: true }, { key: 'phone', type: 'tel' },
    { key: 'country', type: 'select', options: countryOptions(), required: true }, { key: 'currency', type: 'select', options: curOpts(), required: true, allowEmpty: false },
    { key: 'buyer_type', type: 'select', options: opts('buyer', BUYER) }, { key: 'tax_id', type: 'text' },
    { key: 'tax_treatment', type: 'select', options: opts('tax', TAX) }, { key: 'lang', type: 'select', options: langOpts() },
    { key: 'status', type: 'select', options: statusOpts('cust'), allowEmpty: false }, { key: 'source', type: 'text' },
    { key: 'billing_address', type: 'textarea', span2: true, rows: 2 }, { key: 'tags', type: 'tags', span2: true },
    { key: 'owner_note', type: 'textarea', span2: true },
  ],
  subscriptions: () => [
    { key: 'plan', type: 'select', options: planOptions(), required: true, allowEmpty: false }, { key: 'currency', type: 'select', options: curOpts(), required: true, allowEmpty: false },
    { key: 'list_price', type: 'money', required: true }, { key: 'discount_percent', type: 'number', min: 0, max: 100 },
    { key: 'discount_until', type: 'date' }, { key: 'status', type: 'select', options: statusOpts('sub'), allowEmpty: false },
    { key: 'started_at', type: 'date' }, { key: 'current_period_start', type: 'date', label: 'col.period_start' },
    { key: 'current_period_end', type: 'date', label: 'col.period_end' }, { key: 'tenant_id', type: 'text' },
    { key: 'note', type: 'textarea', span2: true },
  ],
  invoices: () => [
    { key: 'period_start', type: 'date' }, { key: 'period_end', type: 'date' },
    { key: 'due_at', type: 'date' }, { key: 'tax_document', type: 'text' },
    { key: 'note', type: 'textarea', span2: true },
  ],
  campaigns: () => [
    { key: 'name', type: 'text', required: true }, { key: 'channel', type: 'select', options: opts('chan', CHANNELS), required: true, allowEmpty: false },
    { key: 'utm_source', type: 'text' }, { key: 'utm_medium', type: 'text' }, { key: 'utm_campaign', type: 'text' },
    { key: 'status', type: 'select', options: statusOpts('camp'), allowEmpty: false },
    { key: 'country', type: 'select', options: countryOptions() }, { key: 'lang', type: 'select', options: langOpts() },
    { key: 'budget', type: 'money' }, { key: 'currency', type: 'select', options: curOpts() },
    { key: 'starts_on', type: 'date' }, { key: 'ends_on', type: 'date' },
    { key: 'landing_url', type: 'text', span2: true, placeholder: 'https://' }, { key: 'note', type: 'textarea', span2: true },
  ],
  tasks: (ctx) => [
    { key: 'kind', type: 'select', options: opts('task', TASK_KINDS), allowEmpty: false, required: true }, { key: 'due_at', type: 'datetime' },
    { key: 'title', type: 'text', required: true, span2: true }, { key: 'assignee', type: 'text' },
    { key: 'note', type: 'textarea', span2: true, rows: 2 },
    { key: 'entity', type: 'hidden', value: ctx && ctx.entity }, { key: 'entity_id', type: 'hidden', value: ctx && ctx.entity_id },
  ],
  users: (ctx) => [
    { key: 'username', type: 'text', required: true, disabled: !!(ctx && ctx.editing) }, { key: 'display_name', type: 'text' },
    { key: 'email', type: 'email' }, { key: 'role', type: 'select', options: opts('role', ROLES), allowEmpty: false, required: true },
    { key: 'status', type: 'select', options: statusOpts('user'), allowEmpty: false },
    { key: 'temp_password', type: 'password', label: 'settings.temp_password', required: !(ctx && ctx.editing), validate: (v) => (v && String(v).length < 10 ? 'err.min_pw' : null) },
  ],
};

export const ACTION_FORMS = {
  transition: (state) => [{ key: 'reason', type: 'textarea', label: 'act.reason', rows: 2 }],
  set_status: (status) => (status === 'lost' ? [{ key: 'lost_reason', type: 'text', required: true }] : []),
  record_payment: (cur) => [
    { key: 'amount', type: 'money', required: true, min: 0 }, { key: 'method', type: 'select', options: opts('method', METHODS), allowEmpty: false, required: true },
    { key: 'provider', type: 'text' }, { key: 'provider_ref', type: 'text' },
    { key: 'received_at', type: 'datetime', value: new Date().toISOString() }, { key: 'note', type: 'textarea', rows: 2, span2: true },
  ],
  refund: () => [
    { key: 'amount', type: 'money', required: true, min: 0 }, { key: 'method', type: 'select', options: opts('method', METHODS), allowEmpty: false },
    { key: 'note', type: 'textarea', rows: 2, span2: true },
  ],
  change_plan: () => [
    { key: 'plan', type: 'select', options: planOptions(), allowEmpty: false, required: true }, { key: 'effective_on', type: 'date', label: 'act.effective_on', required: true },
  ],
  cancel: () => [{ key: 'cancel_at', type: 'date', label: 'col.cancel_at' }],
  generate: (customers) => [
    { key: 'customer_id', type: 'select', label: 'col.customer', required: true, options: customers.map((c) => ({ value: c.id, label: (c.code || '') + ' ' + (c.company || '') })) },
    { key: 'month', type: 'month', required: true },
  ],
  link_tenant: (tenants) => [
    { key: 'tenant_id', type: 'select', label: 'col.tenant', required: true, options: tenants.map((x) => ({ value: x.id, label: x.name + (x.phone_number ? ' · ' + x.phone_number : '') })) },
  ],
  usage_refresh: (month) => [{ key: 'month', type: 'month', required: true, value: month }],
  password: () => [
    { key: 'current', type: 'password', label: 'settings.current_pw', required: true, autocomplete: 'current-password' },
    { key: 'new', type: 'password', label: 'settings.new_pw', required: true, validate: (v) => (v && String(v).length < 10 ? 'err.min_pw' : null) },
    { key: 'new2', type: 'password', label: 'settings.new_pw2', required: true, validate: (v, all) => (v !== all.new ? 'err.pw_mismatch' : null) },
  ],
};
