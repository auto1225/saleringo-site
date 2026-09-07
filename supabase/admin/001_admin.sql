-- =====================================================================
-- Saleringo 판매 관리자(Sales Admin) — 마이그레이션 001 (2026-09-07)
-- 설계 원천: docs/admin-spec.md (§2 데이터 모델, §2.4 함수)
--
-- 몇 번을 다시 적용해도 같은 결과가 나오도록 썼다 (if not exists / or replace).
-- 새 표는 전부 RLS 만 켜고 정책을 두지 않는다 — 표에 닿는 길은
-- public.admin_* SECURITY DEFINER 함수뿐이다. 기존 표(leads, orders)는
-- 컬럼을 더하기만 하고 바꾸거나 지우지 않는다.
--
-- pgcrypto 는 이 프로젝트에서 extensions 스키마에 있다. 함수의
-- search_path 가 sales, public 이므로 crypt/gen_salt/digest/gen_random_bytes
-- 는 반드시 extensions. 을 붙여 부른다 (안 붙이면 "does not exist").
--
-- 오류 규약: 예상된 실패는 sales.admin_fail() 이 'admin:{json}' 메시지로
-- raise 하고, public 껍데기 함수가 sales.admin_catch() 로 받아 그 json 을
-- 돌려준다. raise 로 빠져나오면 그때까지의 쓰기는 전부 되돌아간다.
-- 로그인만은 예외 — 유량제한 기록이 되돌아가면 안 되므로 raise 없이
-- 오류 객체를 그대로 돌려준다.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 0. updated_at 트리거 함수
-- ---------------------------------------------------------------------
create or replace function sales.touch_updated_at()
returns trigger
language plpgsql
as $function$
begin
  new.updated_at = now();
  return new;
end;
$function$;

-- ---------------------------------------------------------------------
-- 1. 관리자 (§2.1)
-- ---------------------------------------------------------------------
create table if not exists sales.admin_users (
  id                   uuid primary key default gen_random_uuid(),
  username             text not null,
  display_name         text not null default '',
  email                text,
  password_hash        text not null,
  role                 text not null default 'viewer'
                       check (role in ('owner', 'staff', 'viewer')),
  status               text not null default 'active'
                       check (status in ('active', 'disabled')),
  must_change_password boolean not null default true,
  last_login_at        timestamptz,
  failed_logins        int not null default 0,
  created_at           timestamptz not null default now(),
  updated_at           timestamptz not null default now()
);
create unique index if not exists admin_users_username_key
  on sales.admin_users (lower(username));

create table if not exists sales.admin_sessions (
  id           uuid primary key default gen_random_uuid(),
  user_id      uuid not null references sales.admin_users (id) on delete cascade,
  token_hash   text not null unique,
  created_at   timestamptz not null default now(),
  last_seen_at timestamptz not null default now(),
  expires_at   timestamptz not null,
  ip_hash      text,
  user_agent   text,
  revoked_at   timestamptz
);
create index if not exists admin_sessions_user_idx
  on sales.admin_sessions (user_id, created_at desc);

create table if not exists sales.admin_audit (
  id        bigserial primary key,
  at        timestamptz not null default now(),
  user_id   uuid,
  username  text not null default '',
  action    text not null,
  entity    text,
  entity_id text,
  before    jsonb,
  after     jsonb,
  ip_hash   text
);
create index if not exists admin_audit_at_idx on sales.admin_audit (at desc);
create index if not exists admin_audit_entity_idx on sales.admin_audit (entity, entity_id);

-- ---------------------------------------------------------------------
-- 2. 고객·구독·청구 (§2.2)
-- ---------------------------------------------------------------------
create sequence if not exists sales.customer_seq;
create sequence if not exists sales.invoice_seq;

create table if not exists sales.customers (
  id              uuid primary key default gen_random_uuid(),
  code            text not null unique,                         -- CU-YYYYMMDD-NNNN
  company         text not null,
  contact_name    text,
  email           text not null,                                -- 항상 소문자
  phone           text,
  country         text,
  currency        text not null default 'KRW' check (currency in ('KRW', 'USD')),
  buyer_type      text not null default 'unknown'
                  check (buyer_type in ('business', 'consumer', 'public', 'unknown')),
  tax_id          text,
  tax_treatment   text not null default 'review'
                  check (tax_treatment in ('vat_charged', 'reverse', 'none', 'review')),
  billing_address text,
  lang            text not null default 'ko',
  tenant_id       uuid,                                         -- public.tenants.id, 느슨한 참조
  status          text not null default 'lead'
                  check (status in ('lead', 'trial', 'active', 'paused', 'churned')),
  source          text,
  tags            text[] not null default '{}',
  owner_note      text,
  first_order_id  uuid,
  archived_at     timestamptz,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);
-- 살아 있는 고객끼리 이메일이 겹치지 않는다 (보관된 고객은 예외)
create unique index if not exists customers_email_live_key
  on sales.customers (lower(email)) where archived_at is null;
create index if not exists customers_tenant_idx  on sales.customers (tenant_id);
create index if not exists customers_created_idx on sales.customers (created_at desc);
create index if not exists customers_status_idx  on sales.customers (status);

create table if not exists sales.subscriptions (
  id                   uuid primary key default gen_random_uuid(),
  customer_id          uuid not null references sales.customers (id),
  order_id             uuid,
  plan                 text not null,                            -- pricing.json plans[].id
  currency             text not null check (currency in ('KRW', 'USD')),
  list_price           numeric not null default 0 check (list_price >= 0),
  discount_percent     numeric not null default 0
                       check (discount_percent >= 0 and discount_percent <= 100),
  discount_until       date,
  status               text not null default 'pending'
                       check (status in ('pending', 'trial', 'active', 'paused', 'canceled')),
  started_at           date,
  current_period_start date,
  current_period_end   date,
  cancel_at            date,
  canceled_at          timestamptz,
  tenant_id            uuid,
  note                 text,
  created_at           timestamptz not null default now(),
  updated_at           timestamptz not null default now()
);
create index if not exists subscriptions_customer_idx on sales.subscriptions (customer_id);
create index if not exists subscriptions_order_idx    on sales.subscriptions (order_id);
create index if not exists subscriptions_status_idx   on sales.subscriptions (status);

create table if not exists sales.invoices (
  id              uuid primary key default gen_random_uuid(),
  invoice_no      text not null unique,                         -- IV-YYYYMM-NNNN
  customer_id     uuid not null references sales.customers (id),
  subscription_id uuid references sales.subscriptions (id),
  order_id        uuid,
  period_start    date,
  period_end      date,
  currency        text not null check (currency in ('KRW', 'USD')),
  lines           jsonb not null default '[]'::jsonb,
  net             numeric not null default 0,
  tax_rate        numeric not null default 0,
  tax             numeric not null default 0,
  total           numeric not null default 0,
  status          text not null default 'draft'
                  check (status in ('draft', 'issued', 'paid', 'partially_paid',
                                    'overdue', 'void', 'refunded')),
  issued_at       timestamptz,
  due_at          date,
  paid_at         timestamptz,
  method          text check (method is null or method in ('card', 'transfer', 'other')),
  provider        text,
  provider_ref    text,
  tax_document    text,                                         -- 세금계산서 번호 등
  note            text,
  archived_at     timestamptz,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);
create index if not exists invoices_customer_idx     on sales.invoices (customer_id);
create index if not exists invoices_subscription_idx on sales.invoices (subscription_id, period_start);
create index if not exists invoices_status_idx       on sales.invoices (status, due_at);
create index if not exists invoices_created_idx      on sales.invoices (created_at desc);

create table if not exists sales.payments (
  id           uuid primary key default gen_random_uuid(),
  invoice_id   uuid not null references sales.invoices (id),
  customer_id  uuid not null references sales.customers (id),
  amount       numeric not null check (amount > 0),             -- 환불도 양수 + kind 로 구분
  currency     text not null check (currency in ('KRW', 'USD')),
  method       text not null default 'other' check (method in ('card', 'transfer', 'other')),
  provider     text,
  provider_ref text,
  received_at  timestamptz not null default now(),
  kind         text not null default 'payment' check (kind in ('payment', 'refund')),
  note         text,
  recorded_by  uuid,
  created_at   timestamptz not null default now()
);
create index if not exists payments_invoice_idx  on sales.payments (invoice_id);
create index if not exists payments_customer_idx on sales.payments (customer_id);
create index if not exists payments_received_idx on sales.payments (received_at desc);

create table if not exists sales.usage_monthly (
  id            uuid primary key default gen_random_uuid(),
  tenant_id     uuid not null,
  month         date not null,                                  -- 항상 그 달 1일
  calls         int not null default 0,
  call_seconds  int not null default 0,
  voice_minutes numeric not null default 0,                     -- ceil(초/60) 의 합
  conversations int not null default 0,
  chats_web     int not null default 0,
  chats_kakao   int not null default 0,
  chats_phone   int not null default 0,
  alimtalk      int not null default 0,
  computed_at   timestamptz not null default now(),
  unique (tenant_id, month)
);
create index if not exists usage_monthly_month_idx on sales.usage_monthly (month desc);

-- ---------------------------------------------------------------------
-- 3. 파이프라인·마케팅 (§2.3)
-- ---------------------------------------------------------------------
alter table sales.leads
  add column if not exists assignee           text,
  add column if not exists next_action_at     timestamptz,
  add column if not exists lost_reason        text,
  add column if not exists converted_order_id uuid,
  add column if not exists campaign_id        uuid,
  add column if not exists archived_at        timestamptz;
create index if not exists leads_status_idx   on sales.leads (status);
create index if not exists leads_campaign_idx on sales.leads (campaign_id);

alter table sales.orders
  add column if not exists assignee       text,
  add column if not exists next_action_at timestamptz,
  add column if not exists customer_id    uuid,
  add column if not exists archived_at    timestamptz;
create index if not exists orders_customer_idx on sales.orders (customer_id);

create table if not exists sales.campaigns (
  id           uuid primary key default gen_random_uuid(),
  name         text not null,
  channel      text not null default 'other'
               check (channel in ('search', 'social', 'email', 'referral', 'event',
                                  'partner', 'content', 'other')),
  utm_source   text,
  utm_medium   text,
  utm_campaign text,
  country      text,
  lang         text,
  budget       numeric check (budget is null or budget >= 0),
  currency     text check (currency is null or currency in ('KRW', 'USD')),
  starts_on    date,
  ends_on      date,
  status       text not null default 'planned'
               check (status in ('planned', 'active', 'paused', 'ended')),
  landing_url  text,
  note         text,
  archived_at  timestamptz,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);
create index if not exists campaigns_utm_idx
  on sales.campaigns (lower(utm_source), lower(utm_medium), lower(utm_campaign));

create table if not exists sales.tasks (
  id         uuid primary key default gen_random_uuid(),
  kind       text not null default 'other'
             check (kind in ('call', 'email', 'followup', 'contract', 'provisioning',
                             'billing', 'other')),
  title      text not null,
  entity     text check (entity is null or entity in ('lead', 'order', 'customer', 'invoice')),
  entity_id  uuid,
  due_at     timestamptz,
  done_at    timestamptz,
  assignee   text,
  note       text,
  created_by text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists tasks_due_idx    on sales.tasks (done_at, due_at);
create index if not exists tasks_entity_idx on sales.tasks (entity, entity_id);

create table if not exists sales.notes (
  id         uuid primary key default gen_random_uuid(),
  entity     text not null
             check (entity in ('lead', 'order', 'customer', 'invoice', 'subscription', 'campaign')),
  entity_id  uuid not null,
  body       text not null,
  author     text not null default '',
  created_at timestamptz not null default now()
);
create index if not exists notes_entity_idx on sales.notes (entity, entity_id, created_at desc);

create table if not exists sales.settings (
  key        text primary key,
  value      jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  updated_by text
);

-- ---------------------------------------------------------------------
-- 4. RLS (정책 없음 = 함수만 접근) · updated_at 트리거
-- ---------------------------------------------------------------------
alter table sales.admin_users    enable row level security;
alter table sales.admin_sessions enable row level security;
alter table sales.admin_audit    enable row level security;
alter table sales.customers      enable row level security;
alter table sales.subscriptions  enable row level security;
alter table sales.invoices       enable row level security;
alter table sales.payments       enable row level security;
alter table sales.usage_monthly  enable row level security;
alter table sales.campaigns      enable row level security;
alter table sales.tasks          enable row level security;
alter table sales.notes          enable row level security;
alter table sales.settings       enable row level security;

drop trigger if exists touch_updated_at on sales.admin_users;
create trigger touch_updated_at before update on sales.admin_users
  for each row execute function sales.touch_updated_at();
drop trigger if exists touch_updated_at on sales.customers;
create trigger touch_updated_at before update on sales.customers
  for each row execute function sales.touch_updated_at();
drop trigger if exists touch_updated_at on sales.subscriptions;
create trigger touch_updated_at before update on sales.subscriptions
  for each row execute function sales.touch_updated_at();
drop trigger if exists touch_updated_at on sales.invoices;
create trigger touch_updated_at before update on sales.invoices
  for each row execute function sales.touch_updated_at();
drop trigger if exists touch_updated_at on sales.campaigns;
create trigger touch_updated_at before update on sales.campaigns
  for each row execute function sales.touch_updated_at();
drop trigger if exists touch_updated_at on sales.tasks;
create trigger touch_updated_at before update on sales.tasks
  for each row execute function sales.touch_updated_at();
drop trigger if exists touch_updated_at on sales.settings;
create trigger touch_updated_at before update on sales.settings
  for each row execute function sales.touch_updated_at();

-- ---------------------------------------------------------------------
-- 5. 시드: admin / 1234 (요청대로). 관리자가 하나도 없을 때만 넣는다.
-- ---------------------------------------------------------------------
insert into sales.admin_users (username, display_name, password_hash, role, must_change_password)
select 'admin', '관리자', extensions.crypt('1234', extensions.gen_salt('bf', 10)), 'owner', true
 where not exists (select 1 from sales.admin_users);

-- ---------------------------------------------------------------------
-- 6. 공통 도우미: 오류 규약 · 검증 · 코드 발번 · 세션 · 감사
-- ---------------------------------------------------------------------

-- 오류 코드별 사람 문구. 화면이 그대로 보여 준다.
create or replace function sales.admin_msg(p_code text)
returns jsonb
language sql
immutable
as $function$
  select case p_code
    when 'unauthorized'   then jsonb_build_object('ko', '로그인이 필요합니다.',                 'en', 'Please sign in.')
    when 'forbidden'      then jsonb_build_object('ko', '권한이 없습니다.',                     'en', 'You do not have permission to do that.')
    when 'rate_limited'   then jsonb_build_object('ko', '시도가 너무 많습니다. 잠시 뒤 다시 하세요.', 'en', 'Too many attempts. Please try again later.')
    when 'invalid'        then jsonb_build_object('ko', '입력값을 확인하세요.',                 'en', 'Please check the highlighted fields.')
    when 'not_found'      then jsonb_build_object('ko', '찾을 수 없습니다.',                    'en', 'Not found.')
    when 'conflict'       then jsonb_build_object('ko', '이미 있는 값입니다.',                  'en', 'That already exists.')
    when 'bad_transition' then jsonb_build_object('ko', '허용되지 않는 상태 변경입니다.',       'en', 'That state change is not allowed.')
    else                       jsonb_build_object('ko', '처리 중 오류가 났습니다.',             'en', 'Something went wrong.')
  end;
$function$;

-- 표준 오류 객체 {"ok":false,"error":code,"message":{ko,en}[,"fields":[..]]}
create or replace function sales.admin_error(p_code text, p_ko text, p_en text, p_fields jsonb default null)
returns jsonb
language sql
immutable
as $function$
  select jsonb_build_object('ok', false, 'error', p_code,
                            'message', jsonb_build_object('ko', p_ko, 'en', p_en))
         || case when p_fields is null then '{}'::jsonb
                 else jsonb_build_object('fields', p_fields) end;
$function$;

create or replace function sales.admin_err(p_code text, p_fields jsonb default null)
returns jsonb
language sql
immutable
as $function$
  select sales.admin_error(p_code, sales.admin_msg(p_code)->>'ko', sales.admin_msg(p_code)->>'en', p_fields);
$function$;

-- 예상된 실패: 'admin:{json}' 으로 raise. 껍데기 함수가 admin_catch 로 푼다.
create or replace function sales.admin_fail(p_code text, p_fields jsonb default null)
returns void
language plpgsql
as $function$
begin
  raise exception using message = 'admin:' || sales.admin_err(p_code, p_fields)::text, errcode = 'P0001';
end;
$function$;

-- 껍데기 함수의 exception 블록. SQLERRM 원문은 절대 밖으로 내보내지 않는다.
create or replace function sales.admin_catch(p_state text, p_msg text)
returns jsonb
language plpgsql
as $function$
begin
  if p_msg like 'admin:%' then
    return substr(p_msg, 7)::jsonb;
  end if;
  if p_msg = 'unauthorized' then
    return sales.admin_err('unauthorized');
  end if;
  if p_state = '23505' then                                   -- unique_violation
    return sales.admin_err('conflict');
  end if;
  if p_state in ('23502', '23503', '23514', '22P02', '22007', '22008', '22003') then
    return sales.admin_err('invalid');                        -- not null / fk / check / 형식
  end if;
  return sales.admin_err('db_error');
exception when others then
  return sales.admin_err('db_error');
end;
$function$;

-- --- 형식 검사 ---------------------------------------------------------
create or replace function sales.is_uuid(t text)
returns boolean
language sql
immutable
as $function$
  select t ~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$';
$function$;

create or replace function sales.to_uuid(t text)
returns uuid
language sql
immutable
as $function$
  select case when sales.is_uuid(t) then t::uuid else null end;
$function$;

create or replace function sales.is_num(t text)
returns boolean
language sql
immutable
as $function$
  select t ~ '^-?[0-9]{1,15}(\.[0-9]{1,6})?$';
$function$;

create or replace function sales.is_date(t text)
returns boolean
language plpgsql
immutable
as $function$
begin
  if t is null or t !~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' then return false; end if;
  perform t::date;
  return true;
exception when others then
  return false;
end;
$function$;

create or replace function sales.is_ts(t text)
returns boolean
language plpgsql
immutable
as $function$
begin
  if t is null or length(t) > 40 then return false; end if;
  perform t::timestamptz;
  return true;
exception when others then
  return false;
end;
$function$;

create or replace function sales.seoul_today()
returns date
language sql
stable
as $function$
  select (timezone('Asia/Seoul', now()))::date;
$function$;

-- p_data 의 한 키를 검사한다. 없거나 json null 이면 통과(= 지우기), 'req' 만 필수.
-- kind: req | text(maxlen) | enum(a,b,c) | date | ts | uuid | email | num(min) | int(min) | bool | arr
create or replace function sales.chk(p_data jsonb, p_key text, p_kind text, p_opt text default null)
returns void
language plpgsql
as $function$
declare
  v  text;
  ok boolean;
begin
  if p_kind = 'req' then
    if coalesce(btrim(p_data->>p_key), '') = '' then
      perform sales.admin_fail('invalid', jsonb_build_array(p_key));
    end if;
    return;
  end if;
  if not (p_data ? p_key) or jsonb_typeof(p_data->p_key) = 'null' then
    return;
  end if;
  v := p_data->>p_key;
  ok := case p_kind
    when 'text'  then length(v) <= coalesce(p_opt::int, 4000)
    when 'enum'  then v = any (string_to_array(p_opt, ','))
    when 'date'  then sales.is_date(v)
    when 'ts'    then sales.is_ts(v)
    when 'uuid'  then sales.is_uuid(v)
    when 'email' then v ~ '^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]{2,}$' and length(v) <= 200
    when 'num'   then case when sales.is_num(v) then v::numeric >= coalesce(p_opt::numeric, 0) else false end
    when 'int'   then case when v ~ '^-?[0-9]{1,9}$' then v::int >= coalesce(p_opt::int, 0) else false end
    when 'bool'  then jsonb_typeof(p_data->p_key) = 'boolean' or lower(v) in ('true', 'false')
    when 'arr'   then jsonb_typeof(p_data->p_key) = 'array'
    else false end;
  if not ok then
    perform sales.admin_fail('invalid', jsonb_build_array(p_key));
  end if;
end;
$function$;

-- --- 요금표 ----------------------------------------------------------
create or replace function sales.pricing_active()
returns jsonb
language sql
stable
as $function$
  select data from sales.pricing_versions where active limit 1;
$function$;

create or replace function sales.pricing_plan(p_plan text)
returns jsonb
language sql
stable
as $function$
  select value from jsonb_array_elements(coalesce(sales.pricing_active()->'plans', '[]'::jsonb))
   where value->>'id' = p_plan limit 1;
$function$;

-- --- 코드 발번 ---------------------------------------------------------
create or replace function sales.next_customer_code()
returns text
language sql
as $function$
  select 'CU-' || to_char(timezone('Asia/Seoul', now()), 'YYYYMMDD')
      || '-' || lpad(nextval('sales.customer_seq')::text, 4, '0');
$function$;

create or replace function sales.next_invoice_no()
returns text
language sql
as $function$
  select 'IV-' || to_char(timezone('Asia/Seoul', now()), 'YYYYMM')
      || '-' || lpad(nextval('sales.invoice_seq')::text, 4, '0');
$function$;

-- --- 세션·권한·감사 ---------------------------------------------------
-- 토큰 원문을 받아 sha256 으로 세션을 찾는다. 유휴 12시간·절대 7일.
-- last_seen_at 은 1분에 한 번만 갱신한다(모든 호출마다 쓰지 않는다).
create or replace function sales.admin_auth(p_token text)
returns sales.admin_users
language plpgsql
as $function$
declare
  v_s sales.admin_sessions%rowtype;
  v_u sales.admin_users%rowtype;
begin
  if p_token is null or p_token !~ '^[0-9a-f]{64}$' then
    raise exception 'unauthorized';
  end if;
  select s.* into v_s
    from sales.admin_sessions s
   where s.token_hash = encode(extensions.digest(p_token, 'sha256'), 'hex')
     and s.revoked_at is null
     and s.expires_at > now()
     and s.last_seen_at > now() - interval '12 hours';
  if not found then
    raise exception 'unauthorized';
  end if;
  select u.* into v_u from sales.admin_users u
   where u.id = v_s.user_id and u.status = 'active';
  if not found then
    raise exception 'unauthorized';
  end if;
  if v_s.last_seen_at < now() - interval '1 minute' then
    update sales.admin_sessions set last_seen_at = now() where id = v_s.id;
  end if;
  return v_u;
end;
$function$;

create or replace function sales.admin_role_rank(p_role text)
returns int
language sql
immutable
as $function$
  select case p_role when 'owner' then 3 when 'staff' then 2 when 'viewer' then 1 else 0 end;
$function$;

create or replace function sales.admin_require(u sales.admin_users, p_min_role text)
returns void
language plpgsql
as $function$
begin
  if sales.admin_role_rank(u.role) < sales.admin_role_rank(p_min_role) then
    perform sales.admin_fail('forbidden');
  end if;
end;
$function$;

create or replace function sales.admin_audit(u sales.admin_users, p_action text, p_entity text,
                                             p_entity_id text, p_before jsonb, p_after jsonb,
                                             p_ip_hash text default null)
returns void
language plpgsql
as $function$
begin
  insert into sales.admin_audit (user_id, username, action, entity, entity_id, before, after, ip_hash)
  values (u.id, coalesce(u.username, ''), p_action, p_entity, p_entity_id,
          case when p_before is null then null else p_before - 'password_hash' - 'token_hash' end,
          case when p_after  is null then null else p_after  - 'password_hash' - 'token_hash' end,
          p_ip_hash);
end;
$function$;

-- 사람 코드(SO-/IV-/CU-/IN-)나 uuid 를 uuid 로. 없으면 not_found.
create or replace function sales.admin_resolve(p_entity text, p_id text)
returns uuid
language plpgsql
as $function$
declare
  v text := btrim(coalesce(p_id, ''));
  r uuid;
begin
  if v = '' then
    perform sales.admin_fail('invalid', '["id"]'::jsonb);
  end if;
  if sales.is_uuid(v) then
    return v::uuid;
  end if;
  if length(v) > 60 then
    perform sales.admin_fail('not_found');
  end if;
  case p_entity
    when 'orders'    then select id into r from sales.orders    where order_no   = upper(v);
    when 'invoices'  then select id into r from sales.invoices  where invoice_no = upper(v);
    when 'customers' then select id into r from sales.customers where code       = upper(v);
    when 'leads'     then select id into r from sales.leads     where ref        = upper(v);
    else r := null;
  end case;
  if r is null then
    perform sales.admin_fail('not_found');
  end if;
  return r;
end;
$function$;

-- 인보이스 합계. 화면이 보낸 합계는 쓰지 않고 줄에서 다시 더한다.
-- 줄: {kind, label, qty, unit, amount}. unit 이 있으면 amount = round(qty×unit).
create or replace function sales.invoice_totals(p_lines jsonb, p_tax_rate numeric, p_cur text)
returns jsonb
language plpgsql
as $function$
declare
  l       jsonb;
  v_lines jsonb := '[]'::jsonb;
  v_kind  text;
  v_qty   numeric;
  v_unit  numeric;
  v_amt   numeric;
  v_net   numeric := 0;
  v_tax   numeric;
  i       int := 0;
begin
  if p_lines is null or jsonb_typeof(p_lines) <> 'array' then
    perform sales.admin_fail('invalid', '["lines"]'::jsonb);
  end if;
  for l in select value from jsonb_array_elements(p_lines) loop
    i := i + 1;
    if jsonb_typeof(l) <> 'object' then
      perform sales.admin_fail('invalid', jsonb_build_array('lines[' || i || ']'));
    end if;
    v_kind := coalesce(nullif(l->>'kind', ''), 'other');
    if v_kind not in ('plan', 'voice', 'alimtalk', 'overage', 'setup', 'credit', 'other') then
      perform sales.admin_fail('invalid', jsonb_build_array('lines[' || i || '].kind'));
    end if;
    if l ? 'qty' and jsonb_typeof(l->'qty') <> 'null' and not sales.is_num(l->>'qty') then
      perform sales.admin_fail('invalid', jsonb_build_array('lines[' || i || '].qty'));
    end if;
    if l ? 'unit' and jsonb_typeof(l->'unit') <> 'null' and not sales.is_num(l->>'unit') then
      perform sales.admin_fail('invalid', jsonb_build_array('lines[' || i || '].unit'));
    end if;
    if l ? 'amount' and jsonb_typeof(l->'amount') <> 'null' and not sales.is_num(l->>'amount') then
      perform sales.admin_fail('invalid', jsonb_build_array('lines[' || i || '].amount'));
    end if;
    v_qty  := coalesce(nullif(l->>'qty', '')::numeric, 1);
    v_unit := nullif(l->>'unit', '')::numeric;
    if v_qty < 0 then
      perform sales.admin_fail('invalid', jsonb_build_array('lines[' || i || '].qty'));
    end if;
    if v_unit is not null then
      v_amt := sales.round_money(v_qty * v_unit, p_cur);
    else
      v_amt := sales.round_money(coalesce(nullif(l->>'amount', '')::numeric, 0), p_cur);
    end if;
    if v_amt < 0 and v_kind <> 'credit' then
      perform sales.admin_fail('invalid', jsonb_build_array('lines[' || i || '].amount'));
    end if;
    v_net   := v_net + v_amt;
    v_lines := v_lines || jsonb_build_object(
      'kind', v_kind, 'label', left(coalesce(l->>'label', ''), 200),
      'qty', v_qty, 'unit', v_unit, 'amount', v_amt);
  end loop;
  v_net := sales.round_money(v_net, p_cur);
  v_tax := sales.round_money(v_net * coalesce(p_tax_rate, 0), p_cur);
  return jsonb_build_object('lines', v_lines, 'net', v_net, 'tax', v_tax,
                            'total', sales.round_money(v_net + v_tax, p_cur));
end;
$function$;

-- 고객의 세금 처리 → 세율. vat_charged 만 활성 요금표의 KR 세율, 그 밖은 0.
create or replace function sales.customer_tax_rate(p_treatment text)
returns numeric
language sql
stable
as $function$
  select case when p_treatment = 'vat_charged'
              then coalesce((sales.pricing_active()->'tax'->'KR'->>'rate')::numeric, 0.1)
              else 0 end;
$function$;

-- 통화별 합계 jsonb 를 {KRW, USD} 두 키로 고정한다.
create or replace function sales.money_pair(j jsonb)
returns jsonb
language sql
immutable
as $function$
  select jsonb_build_object('KRW', coalesce((j->>'KRW')::numeric, 0),
                            'USD', coalesce((j->>'USD')::numeric, 0));
$function$;

-- ---------------------------------------------------------------------
-- 7. 업무 도우미: 주문→고객·구독, 구독 개통, 사용량 집계, 캠페인 연결
-- ---------------------------------------------------------------------

-- 주문의 이메일로 고객을 찾거나 만들고, 주문에 고객을 잇고, 주문 하나에
-- 구독 하나를 만든다(없으면). 돌려주는 값은 고객 id.
create or replace function sales.customer_upsert_from_order(p_order_id uuid, p_actor text default 'system')
returns uuid
language plpgsql
as $function$
declare
  v_o      sales.orders%rowtype;
  v_c      sales.customers%rowtype;
  v_plan   jsonb;
  v_price  numeric;
  v_sub_id uuid;
begin
  select * into v_o from sales.orders where id = p_order_id;
  if not found then
    perform sales.admin_fail('not_found');
  end if;

  if v_o.customer_id is not null then
    select * into v_c from sales.customers where id = v_o.customer_id;
  end if;
  if v_c.id is null then
    select * into v_c from sales.customers
     where lower(email) = lower(v_o.email) and archived_at is null
     order by created_at limit 1;
  end if;
  if v_c.id is null then
    insert into sales.customers (
      code, company, contact_name, email, phone, country, currency, buyer_type,
      tax_id, tax_treatment, billing_address, lang, status, source, first_order_id
    ) values (
      sales.next_customer_code(), v_o.company, v_o.contact, lower(v_o.email), v_o.phone,
      v_o.billing_country, v_o.currency, v_o.buyer_type::text,
      v_o.tax_id, v_o.tax_treatment::text, v_o.billing_address,
      coalesce(v_o.locale, 'ko'), 'lead', 'order', v_o.id
    ) returning * into v_c;
  else
    update sales.customers
       set first_order_id  = coalesce(first_order_id, v_o.id),
           phone           = coalesce(phone, v_o.phone),
           tax_id          = coalesce(tax_id, v_o.tax_id),
           billing_address = coalesce(billing_address, v_o.billing_address)
     where id = v_c.id;
  end if;

  if v_o.customer_id is distinct from v_c.id then
    update sales.orders set customer_id = v_c.id, updated_at = now() where id = v_o.id;
  end if;

  -- 구독: 주문 하나에 하나. 정가는 활성 요금표, 할인은 주문에 찍힌 값.
  select id into v_sub_id from sales.subscriptions where order_id = v_o.id limit 1;
  if v_sub_id is null then
    v_plan  := sales.pricing_plan(v_o.plan);
    v_price := coalesce((v_plan->'price'->>v_o.currency)::numeric, v_o.after_discount, v_o.monthly_net, 0);
    insert into sales.subscriptions (
      customer_id, order_id, plan, currency, list_price, discount_percent, status, tenant_id, note
    ) values (
      v_c.id, v_o.id, v_o.plan, v_o.currency, v_price,
      least(100, greatest(0, coalesce((v_o.discount->>'percent')::numeric, 0))),
      'pending', v_c.tenant_id,
      '주문 ' || v_o.order_no || ' 에서 ' || coalesce(p_actor, 'system') || ' 이(가) 만듦'
    );
  end if;
  return v_c.id;
end;
$function$;

-- 주문이 active 가 될 때: 구독 시작·첫 청구 기간·할인 만료일, 고객 active.
create or replace function sales.subscription_activate(p_order_id uuid)
returns void
language plpgsql
as $function$
declare
  v_o      sales.orders%rowtype;
  v_s      sales.subscriptions%rowtype;
  v_start  date;
  v_months int;
begin
  select * into v_o from sales.orders where id = p_order_id;
  select * into v_s from sales.subscriptions where order_id = p_order_id order by created_at limit 1;
  if v_s.id is null then
    return;
  end if;
  v_start  := coalesce(v_s.started_at, sales.seoul_today());
  v_months := coalesce((v_o.discount->>'months')::int,
                       (sales.pricing_active()->'discount'->>'months')::int, 0);
  update sales.subscriptions
     set status               = 'active',
         started_at           = v_start,
         current_period_start = coalesce(current_period_start, v_start),
         current_period_end   = coalesce(current_period_end,
                                  (v_start + interval '1 month' - interval '1 day')::date),
         discount_until       = case when discount_percent > 0 and discount_until is null and v_months > 0
                                     then (v_start + make_interval(months => v_months) - interval '1 day')::date
                                     else discount_until end,
         cancel_at            = null,
         canceled_at          = null
   where id = v_s.id;
  update sales.customers set status = 'active' where id = v_s.customer_id and status <> 'active';
end;
$function$;

-- 인보이스의 입금 합계를 다시 세어 상태를 정한다.
create or replace function sales.invoice_recalc(p_invoice_id uuid)
returns jsonb
language plpgsql
as $function$
declare
  v_i    sales.invoices%rowtype;
  v_paid numeric := 0;
  v_ref  numeric := 0;
  v_new  text;
begin
  select * into v_i from sales.invoices where id = p_invoice_id;
  select coalesce(sum(amount) filter (where kind = 'payment'), 0),
         coalesce(sum(amount) filter (where kind = 'refund'), 0)
    into v_paid, v_ref
    from sales.payments where invoice_id = p_invoice_id;
  if v_i.status in ('draft', 'void') then
    return to_jsonb(v_i);
  end if;
  if v_paid > 0 and v_ref >= v_paid then
    v_new := 'refunded';
  elsif v_paid >= v_i.total and v_i.total > 0 then
    v_new := 'paid';
  elsif v_paid > 0 then
    v_new := 'partially_paid';
  elsif v_i.status = 'refunded' then
    v_new := 'issued';
  else
    v_new := case when v_i.status in ('paid', 'partially_paid') then 'issued' else v_i.status end;
  end if;
  update sales.invoices
     set status  = v_new,
         paid_at = case when v_new = 'paid' then coalesce(paid_at, now()) else paid_at end
   where id = p_invoice_id
   returning * into v_i;
  return to_jsonb(v_i) || jsonb_build_object('paid_amount', v_paid - v_ref);
end;
$function$;

-- 한 달치 사용량을 운영 표에서 다시 세어 upsert. __system__ 테넌트는 뺀다.
-- 달의 경계는 Asia/Seoul 자정.
create or replace function sales.usage_refresh(p_month date default null)
returns jsonb
language plpgsql
as $function$
declare
  v_m  date := date_trunc('month', coalesce(p_month, sales.seoul_today()))::date;
  v_lo timestamptz;
  v_hi timestamptz;
  n    int;
begin
  v_lo := (v_m::timestamp) at time zone 'Asia/Seoul';
  v_hi := ((v_m + interval '1 month')::timestamp) at time zone 'Asia/Seoul';

  with t as (
    select id from public.tenants where name <> '__system__'
  ), c as (
    select tenant_id,
           count(*)::int                                            as calls,
           coalesce(sum(duration_seconds), 0)::int                  as secs,
           coalesce(sum(ceil(coalesce(duration_seconds, 0) / 60.0)), 0) as mins
      from public.calls
     where started_at >= v_lo and started_at < v_hi
     group by tenant_id
  ), v as (
    select tenant_id,
           count(*)::int                                                       as conv,
           count(*) filter (where channel in ('web_widget', 'web'))::int       as web,
           count(*) filter (where channel = 'kakao')::int                      as kakao,
           count(*) filter (where channel in ('phone', 'voice'))::int          as ph
      from public.chat_conversations
     where started_at >= v_lo and started_at < v_hi
     group by tenant_id
  ), m as (
    select tenant_id, count(*)::int as alim
      from public.messages
     where channel = 'kakao' and status in ('sent', 'delivered')
       and created_at >= v_lo and created_at < v_hi
     group by tenant_id
  )
  insert into sales.usage_monthly (
    tenant_id, month, calls, call_seconds, voice_minutes, conversations,
    chats_web, chats_kakao, chats_phone, alimtalk, computed_at
  )
  select t.id, v_m,
         coalesce(c.calls, 0), coalesce(c.secs, 0), coalesce(c.mins, 0),
         coalesce(v.conv, 0), coalesce(v.web, 0), coalesce(v.kakao, 0), coalesce(v.ph, 0),
         coalesce(m.alim, 0), now()
    from t
    left join c on c.tenant_id = t.id
    left join v on v.tenant_id = t.id
    left join m on m.tenant_id = t.id
  on conflict (tenant_id, month) do update set
    calls         = excluded.calls,
    call_seconds  = excluded.call_seconds,
    voice_minutes = excluded.voice_minutes,
    conversations = excluded.conversations,
    chats_web     = excluded.chats_web,
    chats_kakao   = excluded.chats_kakao,
    chats_phone   = excluded.chats_phone,
    alimtalk      = excluded.alimtalk,
    computed_at   = excluded.computed_at;
  get diagnostics n = row_count;
  return jsonb_build_object('ok', true, 'month', to_char(v_m, 'YYYY-MM'),
                            'tenants', n, 'computed_at', now());
end;
$function$;

-- 리드의 utm (source, medium, campaign) 과 같은 캠페인을 잇는다.
-- 키 이름은 utm_source 와 source 두 형태를 모두 받는다.
create or replace function sales.campaign_attach(p_lead_id uuid)
returns uuid
language plpgsql
as $function$
declare
  v_l   sales.leads%rowtype;
  v_cid uuid;
  s     text;
  m     text;
  c     text;
begin
  select * into v_l from sales.leads where id = p_lead_id;
  if not found or v_l.utm is null then
    return null;
  end if;
  s := lower(nullif(btrim(coalesce(v_l.utm->>'utm_source',   v_l.utm->>'source',   '')), ''));
  m := lower(nullif(btrim(coalesce(v_l.utm->>'utm_medium',   v_l.utm->>'medium',   '')), ''));
  c := lower(nullif(btrim(coalesce(v_l.utm->>'utm_campaign', v_l.utm->>'campaign', '')), ''));
  if s is null and c is null then
    return v_l.campaign_id;
  end if;
  select id into v_cid from sales.campaigns
   where archived_at is null
     and lower(coalesce(utm_source,   '')) = coalesce(s, '')
     and lower(coalesce(utm_medium,   '')) = coalesce(m, '')
     and lower(coalesce(utm_campaign, '')) = coalesce(c, '')
   order by created_at desc limit 1;
  if v_cid is not null and v_l.campaign_id is distinct from v_cid then
    update sales.leads set campaign_id = v_cid, updated_at = now() where id = v_l.id;
  end if;
  return coalesce(v_cid, v_l.campaign_id);
end;
$function$;

-- 캠페인 쪽에서: 아직 캠페인이 없는 리드 가운데 utm 이 같은 것을 전부 잇는다.
create or replace function sales.campaign_attach_all(p_campaign_id uuid)
returns int
language plpgsql
as $function$
declare
  v_c sales.campaigns%rowtype;
  n   int;
begin
  select * into v_c from sales.campaigns where id = p_campaign_id;
  if not found or (v_c.utm_source is null and v_c.utm_campaign is null) then
    return 0;
  end if;
  update sales.leads l
     set campaign_id = v_c.id, updated_at = now()
   where l.campaign_id is null and l.utm is not null
     and lower(coalesce(l.utm->>'utm_source',   l.utm->>'source',   '')) = lower(coalesce(v_c.utm_source,   ''))
     and lower(coalesce(l.utm->>'utm_medium',   l.utm->>'medium',   '')) = lower(coalesce(v_c.utm_medium,   ''))
     and lower(coalesce(l.utm->>'utm_campaign', l.utm->>'campaign', '')) = lower(coalesce(v_c.utm_campaign, ''));
  get diagnostics n = row_count;
  return n;
end;
$function$;

-- 주문 상태 전이표 (§2.3). 그 밖은 전부 거절.
create or replace function sales.order_transition_ok(p_from text, p_to text)
returns boolean
language sql
immutable
as $function$
  select case p_from
    when 'received'        then p_to in ('under_review', 'contract_sent', 'cancelled', 'rejected')
    when 'under_review'    then p_to in ('proposal_sent', 'contract_sent', 'cancelled', 'rejected')
    when 'proposal_sent'   then p_to in ('contract_sent', 'cancelled', 'rejected')
    when 'contract_sent'   then p_to in ('contract_signed', 'cancelled')
    when 'contract_signed' then p_to in ('payment_pending', 'active')
    when 'payment_pending' then p_to in ('paid', 'cancelled')
    when 'paid'            then p_to = 'active'
    when 'active'          then p_to = 'cancelled'
    else false end;
$function$;

-- ---------------------------------------------------------------------
-- 8. 목록(admin_list): 엔티티별 SELECT 조각 + 필터 정규화 + 동적 SQL
--
-- 사용자 값은 전부 $1(정규화된 필터 jsonb) 로 바인딩되고, SQL 문자열에는
-- 여기 적힌 컬럼식만 들어간다. 정렬 컬럼은 엔티티별 화이트리스트로 푼다.
-- ---------------------------------------------------------------------

-- 조건 조각 만들기. %L 은 키 이름(리터럴), %s 는 컬럼식.
create or replace function sales.lf_eq(p_key text, p_col text)
returns text
language sql
immutable
as $function$
  select format('(nullif($1->>%L, '''') is null or %s = $1->>%L)', p_key, p_col, p_key);
$function$;

create or replace function sales.lf_uuid(p_key text, p_col text)
returns text
language sql
immutable
as $function$
  select format('(nullif($1->>%L, '''') is null or %s = sales.to_uuid($1->>%L))', p_key, p_col, p_key);
$function$;

-- 키가 없으면 false 로 본다 (archived: 기본은 보관 안 된 것만)
create or replace function sales.lf_bool(p_key text, p_expr text)
returns text
language sql
immutable
as $function$
  select format('(coalesce(($1->>%L)::boolean, false) = (%s))', p_key, p_expr);
$function$;

-- 키가 없으면 조건 없음 (done: 기본은 전부)
create or replace function sales.lf_optbool(p_key text, p_expr text)
returns text
language sql
immutable
as $function$
  select format('(nullif($1->>%L, '''') is null or ($1->>%L)::boolean = (%s))', p_key, p_key, p_expr);
$function$;

create or replace function sales.lf_range(p_date_expr text)
returns text
language sql
immutable
as $function$
  select format('(nullif($1->>''from'', '''') is null or %s >= ($1->>''from'')::date) and '
             || '(nullif($1->>''to'', '''') is null or %s <= ($1->>''to'')::date)',
                p_date_expr, p_date_expr);
$function$;

create or replace function sales.lf_q(p_cols text[])
returns text
language sql
immutable
as $function$
  select format('(nullif($1->>''qpat'', '''') is null or (%s))',
                (select string_agg(format('coalesce(%s, '''') ilike $1->>''qpat''', c), ' or ')
                   from unnest(p_cols) c));
$function$;

-- timestamptz 컬럼을 서울 날짜로
create or replace function sales.sdate(p_col text)
returns text
language sql
immutable
as $function$
  select format('(timezone(''Asia/Seoul'', %s))::date', p_col);
$function$;

-- 인보이스 표시 상태: issued 인데 기한이 지났으면 overdue 로 보인다.
create or replace function sales.inv_status_expr()
returns text
language sql
immutable
as $function$
  select $q$(case when i.status = 'issued' and i.due_at < sales.seoul_today() then 'overdue' else i.status end)$q$;
$function$;

-- 화면이 보낸 필터를 검사하고 정규화한다. 모르는 키는 무시, 값이 틀리면 invalid.
create or replace function sales.admin_filter_norm(p_filter jsonb)
returns jsonb
language plpgsql
as $function$
declare
  f     jsonb := coalesce(p_filter, '{}'::jsonb);
  o     jsonb := '{}'::jsonb;
  bad   jsonb := '[]'::jsonb;
  k     text;
  jv    jsonb;
  v     text;
begin
  if jsonb_typeof(f) <> 'object' then
    perform sales.admin_fail('invalid', '["filter"]'::jsonb);
  end if;
  for k, jv in select key, value from jsonb_each(f) loop
    if jv is null or jsonb_typeof(jv) = 'null' then continue; end if;
    v := case when jsonb_typeof(jv) = 'string' then jv #>> '{}' else jv::text end;
    v := nullif(btrim(v), '');
    if v is null then continue; end if;
    if k = 'q' then
      o := o || jsonb_build_object('qpat',
             '%' || replace(replace(replace(left(v, 100), '\', '\\'), '%', '\%'), '_', '\_') || '%');
    elsif k in ('from', 'to') then
      if sales.is_date(v) then o := o || jsonb_build_object(k, v); else bad := bad || to_jsonb(k); end if;
    elsif k in ('customer_id', 'tenant_id', 'subscription_id', 'invoice_id', 'campaign_id', 'order_id') then
      if sales.is_uuid(v) then o := o || jsonb_build_object(k, v); else bad := bad || to_jsonb(k); end if;
    elsif k = 'entity_id' then
      o := o || jsonb_build_object(k, left(v, 80));
    elsif k = 'month' then
      if v ~ '^[0-9]{4}-(0[1-9]|1[0-2])$' then o := o || jsonb_build_object(k, v || '-01');
      else bad := bad || to_jsonb(k); end if;
    elsif k in ('archived', 'done', 'needs_human') then
      if lower(v) in ('true', 'false', '1', '0') then
        o := o || jsonb_build_object(k, (lower(v) in ('true', '1'))::text);
      else bad := bad || to_jsonb(k); end if;
    elsif k = 'lang' then
      o := o || jsonb_build_object('locale', left(v, 8));
    elsif k in ('status', 'state', 'country', 'plan', 'currency', 'locale', 'source', 'method',
                'channel', 'kind', 'entity', 'assignee', 'role', 'step', 'action', 'username',
                'provider', 'owner', 'direction', 'tag') then
      o := o || jsonb_build_object(k, left(v, 80));
    end if;
  end loop;
  if jsonb_array_length(bad) > 0 then
    perform sales.admin_fail('invalid', bad);
  end if;
  return o;
end;
$function$;

-- '<col>:<asc|desc>' 를 화이트리스트로 풀어 order by 식으로.
create or replace function sales.admin_sort(p_sort text, p_allowed jsonb, p_default text)
returns text
language plpgsql
as $function$
declare
  parts text[];
  v_col text;
  v_dir text;
  v_ex  text;
begin
  parts := string_to_array(coalesce(nullif(btrim(coalesce(p_sort, '')), ''), p_default), ':');
  if array_length(parts, 1) > 2 then
    perform sales.admin_fail('invalid', '["sort"]'::jsonb);
  end if;
  v_col := lower(parts[1]);
  v_dir := lower(coalesce(parts[2], 'asc'));
  if v_dir not in ('asc', 'desc') then
    perform sales.admin_fail('invalid', '["sort"]'::jsonb);
  end if;
  v_ex := p_allowed->>v_col;
  if v_ex is null then
    perform sales.admin_fail('invalid', '["sort"]'::jsonb);
  end if;
  return v_ex || ' ' || v_dir || ' nulls last';
end;
$function$;

-- 엔티티별 조각 (1/2): 판매 쪽 표
create or replace function sales.admin_list_spec_a(p_entity text)
returns jsonb
language plpgsql
stable
as $function$
begin
  if p_entity = 'leads' then
    return jsonb_build_object(
      'from', $q$sales.leads l left join sales.campaigns cp on cp.id = l.campaign_id$q$,
      'sel',  $q$(to_jsonb(l) - 'ip_hash' - 'user_agent' - 'consent') || jsonb_build_object('campaign_name', cp.name)$q$,
      'where', sales.lf_q(array['l.company', 'l.name', 'l.email', 'l.phone', 'l.ref'])
        || $q$ and (nullif($1->>'status', '') is null or l.status = $1->>'status' or ($1->>'status' = 'new' and l.status = 'received'))$q$
        || ' and ' || sales.lf_eq('locale', 'l.locale')
        || ' and ' || sales.lf_eq('source', 'l.source')
        || ' and ' || sales.lf_eq('assignee', 'l.assignee')
        || ' and ' || sales.lf_uuid('campaign_id', 'l.campaign_id')
        || ' and ' || sales.lf_range(sales.sdate('l.created_at'))
        || ' and ' || sales.lf_bool('archived', 'l.archived_at is not null'),
      'sort', jsonb_build_object('created_at', 'l.created_at', 'updated_at', 'l.updated_at',
                'status', 'l.status', 'company', 'l.company', 'name', 'l.name', 'email', 'l.email',
                'next_action_at', 'l.next_action_at', 'locale', 'l.locale', 'source', 'l.source'),
      'def', 'created_at:desc', 'pk', 'l.id');
  elsif p_entity = 'orders' then
    return jsonb_build_object(
      'from', $q$sales.orders o left join sales.customers c on c.id = o.customer_id$q$,
      'sel',  $q$(to_jsonb(o) - 'ip_hash' - 'user_agent' - 'consent') || jsonb_build_object('customer_code', c.code)$q$,
      'where', sales.lf_q(array['o.company', 'o.contact', 'o.email', 'o.phone', 'o.order_no'])
        || $q$ and (nullif(coalesce($1->>'state', $1->>'status'), '') is null or o.state::text = coalesce($1->>'state', $1->>'status'))$q$
        || ' and ' || sales.lf_eq('country', 'o.billing_country')
        || ' and ' || sales.lf_eq('plan', 'o.plan')
        || ' and ' || sales.lf_eq('currency', 'o.currency')
        || ' and ' || sales.lf_eq('locale', 'o.locale')
        || ' and ' || sales.lf_eq('method', 'o.method')
        || ' and ' || sales.lf_eq('assignee', 'o.assignee')
        || ' and ' || sales.lf_uuid('customer_id', 'o.customer_id')
        || ' and ' || sales.lf_range(sales.sdate('o.created_at'))
        || ' and ' || sales.lf_bool('archived', 'o.archived_at is not null'),
      'sort', jsonb_build_object('created_at', 'o.created_at', 'updated_at', 'o.updated_at',
                'state', 'o.state', 'company', 'o.company', 'monthly_total', 'o.monthly_total',
                'order_no', 'o.order_no', 'plan', 'o.plan', 'currency', 'o.currency',
                'country', 'o.billing_country', 'next_action_at', 'o.next_action_at'),
      'def', 'created_at:desc', 'pk', 'o.id');
  elsif p_entity = 'customers' then
    return jsonb_build_object(
      'from', $q$sales.customers c
        left join lateral (select s.plan, s.status from sales.subscriptions s where s.customer_id = c.id
                           order by (s.status = 'active') desc, s.created_at desc limit 1) s on true
        left join public.tenants t on t.id = c.tenant_id
        left join lateral (select count(*) as open_invoices,
                                  coalesce(sum(i.total - coalesce((select sum(case when p.kind = 'payment' then p.amount else -p.amount end)
                                                                     from sales.payments p where p.invoice_id = i.id), 0)), 0) as receivable
                             from sales.invoices i
                            where i.customer_id = c.id and i.archived_at is null
                              and i.status in ('issued', 'overdue', 'partially_paid')) iv on true$q$,
      'sel',  $q$to_jsonb(c) || jsonb_build_object('subscription_plan', s.plan, 'subscription_status', s.status,
                'tenant_name', t.name, 'open_invoices', iv.open_invoices, 'receivable', iv.receivable)$q$,
      'where', sales.lf_q(array['c.company', 'c.contact_name', 'c.email', 'c.phone', 'c.code'])
        || ' and ' || sales.lf_eq('status', 'c.status')
        || ' and ' || sales.lf_eq('country', 'c.country')
        || ' and ' || sales.lf_eq('currency', 'c.currency')
        || ' and ' || sales.lf_eq('plan', 's.plan')
        || ' and ' || sales.lf_eq('locale', 'c.lang')
        || ' and ' || sales.lf_eq('source', 'c.source')
        || $q$ and (nullif($1->>'tag', '') is null or ($1->>'tag') = any (c.tags))$q$
        || ' and ' || sales.lf_uuid('tenant_id', 'c.tenant_id')
        || ' and ' || sales.lf_range(sales.sdate('c.created_at'))
        || ' and ' || sales.lf_bool('archived', 'c.archived_at is not null'),
      'sort', jsonb_build_object('created_at', 'c.created_at', 'updated_at', 'c.updated_at',
                'company', 'c.company', 'code', 'c.code', 'status', 'c.status', 'country', 'c.country',
                'email', 'c.email', 'receivable', 'iv.receivable', 'plan', 's.plan'),
      'def', 'created_at:desc', 'pk', 'c.id');
  elsif p_entity = 'subscriptions' then
    return jsonb_build_object(
      'from', $q$sales.subscriptions s join sales.customers c on c.id = s.customer_id
        left join public.tenants t on t.id = s.tenant_id$q$,
      'sel',  $q$to_jsonb(s) || jsonb_build_object('company', c.company, 'customer_code', c.code, 'tenant_name', t.name)$q$,
      'where', sales.lf_q(array['c.company', 'c.code', 'c.email'])
        || ' and ' || sales.lf_eq('status', 's.status')
        || ' and ' || sales.lf_eq('plan', 's.plan')
        || ' and ' || sales.lf_eq('currency', 's.currency')
        || ' and ' || sales.lf_uuid('customer_id', 's.customer_id')
        || ' and ' || sales.lf_uuid('tenant_id', 's.tenant_id')
        || ' and ' || sales.lf_uuid('order_id', 's.order_id')
        || ' and ' || sales.lf_range('coalesce(s.started_at, ' || sales.sdate('s.created_at') || ')'),
      'sort', jsonb_build_object('created_at', 's.created_at', 'started_at', 's.started_at',
                'status', 's.status', 'plan', 's.plan', 'list_price', 's.list_price',
                'current_period_end', 's.current_period_end', 'company', 'c.company'),
      'def', 'created_at:desc', 'pk', 's.id');
  elsif p_entity = 'invoices' then
    return jsonb_build_object(
      'from', $q$sales.invoices i join sales.customers c on c.id = i.customer_id
        left join lateral (select coalesce(sum(case when p.kind = 'payment' then p.amount else -p.amount end), 0) as paid
                             from sales.payments p where p.invoice_id = i.id) pm on true$q$,
      'sel',  $q$to_jsonb(i) || jsonb_build_object('company', c.company, 'customer_code', c.code,
                'paid_amount', pm.paid, 'status', $q$ || sales.inv_status_expr() || ')',
      'where', sales.lf_q(array['c.company', 'c.code', 'i.invoice_no'])
        || ' and ' || sales.lf_eq('status', sales.inv_status_expr())
        || ' and ' || sales.lf_eq('currency', 'i.currency')
        || ' and ' || sales.lf_eq('method', 'i.method')
        || ' and ' || sales.lf_uuid('customer_id', 'i.customer_id')
        || ' and ' || sales.lf_uuid('subscription_id', 'i.subscription_id')
        || ' and ' || sales.lf_range('coalesce(' || sales.sdate('i.issued_at') || ', ' || sales.sdate('i.created_at') || ')')
        || ' and ' || sales.lf_bool('archived', 'i.archived_at is not null'),
      'sort', jsonb_build_object('created_at', 'i.created_at', 'issued_at', 'i.issued_at',
                'due_at', 'i.due_at', 'total', 'i.total', 'status', 'i.status',
                'invoice_no', 'i.invoice_no', 'company', 'c.company', 'period_start', 'i.period_start'),
      'def', 'created_at:desc', 'pk', 'i.id');
  elsif p_entity = 'payments' then
    return jsonb_build_object(
      'from', $q$sales.payments p join sales.invoices i on i.id = p.invoice_id
        join sales.customers c on c.id = p.customer_id$q$,
      'sel',  $q$to_jsonb(p) || jsonb_build_object('invoice_no', i.invoice_no, 'company', c.company)$q$,
      'where', sales.lf_q(array['c.company', 'i.invoice_no', 'p.provider_ref', 'p.note'])
        || ' and ' || sales.lf_eq('kind', 'p.kind')
        || ' and ' || sales.lf_eq('method', 'p.method')
        || ' and ' || sales.lf_eq('currency', 'p.currency')
        || ' and ' || sales.lf_uuid('customer_id', 'p.customer_id')
        || ' and ' || sales.lf_uuid('invoice_id', 'p.invoice_id')
        || ' and ' || sales.lf_range(sales.sdate('p.received_at')),
      'sort', jsonb_build_object('received_at', 'p.received_at', 'created_at', 'p.created_at',
                'amount', 'p.amount', 'kind', 'p.kind', 'method', 'p.method'),
      'def', 'received_at:desc', 'pk', 'p.id');
  elsif p_entity = 'campaigns' then
    return jsonb_build_object(
      'from', $q$sales.campaigns cp
        left join lateral (select count(*) as leads,
                                  count(*) filter (where l.converted_order_id is not null) as orders
                             from sales.leads l where l.campaign_id = cp.id and l.archived_at is null) lc on true$q$,
      'sel',  $q$to_jsonb(cp) || jsonb_build_object('leads', lc.leads, 'orders', lc.orders)$q$,
      'where', sales.lf_q(array['cp.name', 'cp.utm_source', 'cp.utm_campaign', 'cp.utm_medium'])
        || ' and ' || sales.lf_eq('status', 'cp.status')
        || ' and ' || sales.lf_eq('channel', 'cp.channel')
        || ' and ' || sales.lf_eq('country', 'cp.country')
        || ' and ' || sales.lf_eq('locale', 'cp.lang')
        || ' and ' || sales.lf_range('coalesce(cp.starts_on, ' || sales.sdate('cp.created_at') || ')')
        || ' and ' || sales.lf_bool('archived', 'cp.archived_at is not null'),
      'sort', jsonb_build_object('created_at', 'cp.created_at', 'name', 'cp.name', 'status', 'cp.status',
                'starts_on', 'cp.starts_on', 'ends_on', 'cp.ends_on', 'budget', 'cp.budget',
                'leads', 'lc.leads', 'channel', 'cp.channel'),
      'def', 'created_at:desc', 'pk', 'cp.id');
  end if;
  return null;
end;
$function$;

-- 엔티티별 조각 (2/2): 할 일·메모·운영 표·감사·관리자
create or replace function sales.admin_list_spec_b(p_entity text)
returns jsonb
language plpgsql
stable
as $function$
begin
  if p_entity = 'tasks' then
    return jsonb_build_object(
      'from', $q$sales.tasks tk$q$,
      'sel',  $q$to_jsonb(tk)$q$,
      'where', sales.lf_q(array['tk.title', 'tk.note', 'tk.assignee'])
        || ' and ' || sales.lf_eq('kind', 'tk.kind')
        || ' and ' || sales.lf_eq('entity', 'tk.entity')
        || ' and ' || sales.lf_eq('assignee', 'tk.assignee')
        || ' and ' || sales.lf_uuid('entity_id', 'tk.entity_id')
        || ' and ' || sales.lf_optbool('done', 'tk.done_at is not null')
        || ' and ' || sales.lf_range('coalesce(' || sales.sdate('tk.due_at') || ', ' || sales.sdate('tk.created_at') || ')'),
      'sort', jsonb_build_object('created_at', 'tk.created_at', 'due_at', 'tk.due_at', 'kind', 'tk.kind',
                'title', 'tk.title', 'done_at', 'tk.done_at', 'assignee', 'tk.assignee'),
      'def', 'created_at:desc', 'pk', 'tk.id');
  elsif p_entity = 'notes' then
    return jsonb_build_object(
      'from', $q$sales.notes n$q$,
      'sel',  $q$to_jsonb(n)$q$,
      'where', sales.lf_q(array['n.body', 'n.author'])
        || ' and ' || sales.lf_eq('entity', 'n.entity')
        || ' and ' || sales.lf_uuid('entity_id', 'n.entity_id')
        || ' and ' || sales.lf_range(sales.sdate('n.created_at')),
      'sort', jsonb_build_object('created_at', 'n.created_at', 'author', 'n.author'),
      'def', 'created_at:desc', 'pk', 'n.id');
  elsif p_entity = 'tenants' then
    return jsonb_build_object(
      'from', $q$public.tenants t
        left join lateral (select c.id, c.code, c.company from sales.customers c
                            where c.tenant_id = t.id and c.archived_at is null order by c.created_at limit 1) c on true
        left join sales.usage_monthly um on um.tenant_id = t.id
             and um.month = date_trunc('month', sales.seoul_today())::date$q$,
      'sel',  $q$jsonb_build_object('id', t.id, 'name', t.name, 'plan_type', t.plan_type, 'industry', t.industry,
                'phone_number', t.phone_number, 'ai_phone', t.settings->>'aiPhone', 'created_at', t.created_at,
                'customer_id', c.id, 'customer_code', c.code, 'company', c.company,
                'calls_this_month', coalesce(um.calls, 0), 'conversations_this_month', coalesce(um.conversations, 0))$q$,
      'where', $q$t.name <> '__system__' and $q$
        || sales.lf_q(array['t.name', 't.phone_number', 't.industry', 'c.company', 't.settings->>''aiPhone'''])
        || ' and ' || sales.lf_eq('plan', 't.plan_type::text')
        || ' and ' || sales.lf_uuid('customer_id', 'c.id')
        || ' and ' || sales.lf_range(sales.sdate('t.created_at')),
      'sort', jsonb_build_object('created_at', 't.created_at', 'name', 't.name', 'plan_type', 't.plan_type',
                'industry', 't.industry', 'calls', 'um.calls', 'conversations', 'um.conversations',
                'company', 'c.company'),
      'def', 'created_at:desc', 'pk', 't.id');
  elsif p_entity = 'usage' then
    return jsonb_build_object(
      'from', $q$sales.usage_monthly um join public.tenants t on t.id = um.tenant_id
        left join lateral (select c.id, c.company, c.code from sales.customers c
                            where c.tenant_id = um.tenant_id and c.archived_at is null order by c.created_at limit 1) c on true
        left join lateral (select s.plan from sales.subscriptions s where s.customer_id = c.id
                            and s.status in ('active', 'paused') order by s.created_at desc limit 1) s on true
        left join lateral (select (pl.value->>'conversations')::int as conv_limit
                             from jsonb_array_elements(coalesce(sales.pricing_active()->'plans', '[]'::jsonb)) pl
                            where pl.value->>'id' = s.plan limit 1) lim on true$q$,
      'sel',  $q$to_jsonb(um) || jsonb_build_object('tenant_name', t.name, 'company', c.company, 'customer_id', c.id,
                'customer_code', c.code, 'plan', s.plan, 'conversation_limit', lim.conv_limit,
                'limit_pct', case when coalesce(lim.conv_limit, 0) > 0
                                  then round(100.0 * um.conversations / lim.conv_limit, 1) else null end)$q$,
      'where', $q$t.name <> '__system__' and $q$
        || sales.lf_q(array['t.name', 'c.company'])
        || ' and ' || sales.lf_uuid('tenant_id', 'um.tenant_id')
        || ' and ' || sales.lf_uuid('customer_id', 'c.id')
        || ' and ' || sales.lf_eq('plan', 's.plan')
        || $q$ and (nullif($1->>'month', '') is null or um.month = ($1->>'month')::date)$q$
        || ' and ' || sales.lf_range('um.month'),
      'sort', jsonb_build_object('month', 'um.month', 'tenant_name', 't.name', 'calls', 'um.calls',
                'conversations', 'um.conversations', 'voice_minutes', 'um.voice_minutes',
                'alimtalk', 'um.alimtalk', 'computed_at', 'um.computed_at'),
      'def', 'month:desc', 'pk', 'um.id');
  elsif p_entity = 'numbers' then
    return jsonb_build_object(
      'from', $q$public.phone_numbers pn left join public.tenants t on t.id = pn.tenant_id$q$,
      'sel',  $q$to_jsonb(pn) || jsonb_build_object('tenant_name', t.name)$q$,
      'where', sales.lf_q(array['pn.e164', 'pn.order_no', 't.name', 'pn.note'])
        || ' and ' || sales.lf_eq('status', 'pn.status::text')
        || ' and ' || sales.lf_eq('country', 'pn.country')
        || ' and ' || sales.lf_eq('provider', 'pn.provider')
        || ' and ' || sales.lf_eq('owner', 'pn.owner::text')
        || ' and ' || sales.lf_uuid('tenant_id', 'pn.tenant_id')
        || ' and ' || sales.lf_range(sales.sdate('pn.created_at')),
      'sort', jsonb_build_object('created_at', 'pn.created_at', 'e164', 'pn.e164', 'status', 'pn.status',
                'country', 'pn.country', 'assigned_at', 'pn.assigned_at', 'reserved_at', 'pn.reserved_at',
                'tenant_name', 't.name'),
      'def', 'created_at:desc', 'pk', 'pn.id');
  elsif p_entity = 'jobs' then
    return jsonb_build_object(
      'from', $q$public.provisioning_jobs pj left join public.tenants t on t.id = pj.tenant_id$q$,
      'sel',  $q$to_jsonb(pj) || jsonb_build_object('tenant_name', t.name)$q$,
      'where', sales.lf_q(array['pj.order_no', 't.name', 'pj.last_error'])
        || ' and ' || sales.lf_eq('status', 'pj.status::text')
        || ' and ' || sales.lf_eq('step', 'pj.step::text')
        || ' and ' || sales.lf_uuid('tenant_id', 'pj.tenant_id')
        || ' and ' || sales.lf_optbool('needs_human', $q$(pj.needs_human or pj.status = 'needs_human')$q$)
        || ' and ' || sales.lf_range(sales.sdate('pj.created_at')),
      'sort', jsonb_build_object('created_at', 'pj.created_at', 'updated_at', 'pj.updated_at',
                'due_at', 'pj.due_at', 'status', 'pj.status', 'step', 'pj.step', 'order_no', 'pj.order_no'),
      'def', 'created_at:desc', 'pk', 'pj.id');
  elsif p_entity = 'audit' then
    return jsonb_build_object(
      'from', $q$sales.admin_audit a$q$,
      'sel',  $q$to_jsonb(a)$q$,
      'where', sales.lf_q(array['a.username', 'a.action', 'a.entity_id', 'a.entity'])
        || ' and ' || sales.lf_eq('entity', 'a.entity')
        || ' and ' || sales.lf_eq('entity_id', 'a.entity_id')
        || ' and ' || sales.lf_eq('action', 'a.action')
        || ' and ' || sales.lf_eq('username', 'a.username')
        || ' and ' || sales.lf_range(sales.sdate('a.at')),
      'sort', jsonb_build_object('at', 'a.at', 'action', 'a.action', 'entity', 'a.entity', 'username', 'a.username'),
      'def', 'at:desc', 'pk', 'a.id');
  elsif p_entity = 'users' then
    return jsonb_build_object(
      'from', $q$sales.admin_users u$q$,
      'sel',  $q$to_jsonb(u) - 'password_hash'$q$,
      'where', sales.lf_q(array['u.username', 'u.display_name', 'u.email'])
        || ' and ' || sales.lf_eq('role', 'u.role')
        || ' and ' || sales.lf_eq('status', 'u.status'),
      'sort', jsonb_build_object('created_at', 'u.created_at', 'username', 'u.username', 'role', 'u.role',
                'status', 'u.status', 'last_login_at', 'u.last_login_at'),
      'def', 'created_at:desc', 'pk', 'u.id');
  end if;
  return null;
end;
$function$;

create or replace function sales.admin_list_spec(p_entity text)
returns jsonb
language plpgsql
stable
as $function$
declare
  s jsonb;
begin
  s := coalesce(sales.admin_list_spec_a(p_entity), sales.admin_list_spec_b(p_entity));
  if s is null then
    perform sales.admin_fail('invalid', '["entity"]'::jsonb);
  end if;
  return s;
end;
$function$;

-- 목록 본체. p_max 는 껍데기가 정한다(list 200, export 5000).
create or replace function sales.admin_list_impl(u sales.admin_users, p_entity text, p_filter jsonb,
                                                 p_sort text, p_page int, p_size int, p_max int default 200)
returns jsonb
language plpgsql
as $function$
declare
  spec    jsonb;
  f       jsonb;
  v_sql   text;
  v_rows  jsonb;
  v_total bigint;
  v_page  int;
  v_size  int;
  v_order text;
begin
  if p_entity = 'users' then
    perform sales.admin_require(u, 'owner');
  end if;
  spec    := sales.admin_list_spec(p_entity);
  f       := sales.admin_filter_norm(p_filter);
  v_page  := greatest(1, coalesce(p_page, 1));
  v_size  := least(p_max, greatest(1, coalesce(p_size, 50)));
  v_order := sales.admin_sort(p_sort, spec->'sort', spec->>'def') || ', ' || (spec->>'pk');
  v_sql := format(
    'select coalesce(jsonb_agg(x.r order by x.rn), ''[]''::jsonb), coalesce(max(x.t), 0) '
    || 'from (select %s as r, count(*) over () as t, row_number() over (order by %s) as rn '
    || 'from %s where %s order by %s limit %s offset %s) x',
    spec->>'sel', v_order, spec->>'from', spec->>'where', v_order, v_size, (v_page - 1) * v_size);
  execute v_sql into v_rows, v_total using f;
  return jsonb_build_object('ok', true, 'rows', v_rows, 'total', v_total,
                            'page', v_page, 'size', v_size);
end;
$function$;

-- ---------------------------------------------------------------------
-- 9. 상세(admin_get): 본문 + 연관
-- ---------------------------------------------------------------------
create or replace function sales.admin_notes(p_entity text, p_id uuid)
returns jsonb
language sql
stable
as $function$
  select coalesce(jsonb_agg(to_jsonb(n) order by n.created_at desc), '[]'::jsonb)
    from sales.notes n where n.entity = p_entity and n.entity_id = p_id;
$function$;

create or replace function sales.admin_tasks(p_entity text, p_id uuid)
returns jsonb
language sql
stable
as $function$
  select coalesce(jsonb_agg(to_jsonb(tk) order by (tk.done_at is not null), tk.due_at nulls last, tk.created_at), '[]'::jsonb)
    from sales.tasks tk where tk.entity = p_entity and tk.entity_id = p_id;
$function$;

-- 최근 12개월 사용량 (테넌트 없으면 빈 배열)
create or replace function sales.admin_usage_12(p_tenant uuid)
returns jsonb
language sql
stable
as $function$
  select coalesce(jsonb_agg(to_jsonb(um) order by um.month), '[]'::jsonb)
    from sales.usage_monthly um
   where p_tenant is not null and um.tenant_id = p_tenant
     and um.month >= (date_trunc('month', sales.seoul_today()) - interval '11 months')::date;
$function$;

create or replace function sales.admin_tenant_json(p_tenant uuid)
returns jsonb
language sql
stable
as $function$
  select jsonb_build_object('id', t.id, 'name', t.name, 'plan_type', t.plan_type, 'industry', t.industry,
                            'phone_number', t.phone_number, 'ai_phone', t.settings->>'aiPhone',
                            'business_no', t.business_no, 'address', t.address, 'created_at', t.created_at)
    from public.tenants t where t.id = p_tenant and t.name <> '__system__';
$function$;

-- 인보이스 한 건의 표시용 json (입금 합계·표시 상태·고객)
create or replace function sales.invoice_json(p_id uuid)
returns jsonb
language sql
stable
as $function$
  select to_jsonb(i) || jsonb_build_object(
           'company', c.company, 'customer_code', c.code,
           'paid_amount', coalesce((select sum(case when p.kind = 'payment' then p.amount else -p.amount end)
                                      from sales.payments p where p.invoice_id = i.id), 0),
           'status', case when i.status = 'issued' and i.due_at < sales.seoul_today() then 'overdue' else i.status end)
    from sales.invoices i join sales.customers c on c.id = i.customer_id
   where i.id = p_id;
$function$;

create or replace function sales.admin_get_lead(v_id uuid)
returns jsonb
language plpgsql
stable
as $function$
declare
  item jsonb;
begin
  select to_jsonb(l) || jsonb_build_object('campaign_name', cp.name) into item
    from sales.leads l left join sales.campaigns cp on cp.id = l.campaign_id where l.id = v_id;
  if item is null then perform sales.admin_fail('not_found'); end if;
  return jsonb_build_object('ok', true, 'item', item, 'related', jsonb_build_object(
    'notes', sales.admin_notes('lead', v_id),
    'tasks', sales.admin_tasks('lead', v_id),
    'campaign', (select to_jsonb(cp) from sales.campaigns cp where cp.id = sales.to_uuid(item->>'campaign_id')),
    'converted_order', (select jsonb_build_object('id', o.id, 'order_no', o.order_no, 'state', o.state,
                                                  'company', o.company, 'created_at', o.created_at)
                          from sales.orders o where o.id = sales.to_uuid(item->>'converted_order_id'))));
end;
$function$;

create or replace function sales.admin_get_order(v_id uuid)
returns jsonb
language plpgsql
stable
as $function$
declare
  o    sales.orders%rowtype;
  item jsonb;
begin
  select * into o from sales.orders where id = v_id;
  if not found then perform sales.admin_fail('not_found'); end if;
  item := to_jsonb(o) || jsonb_build_object('customer_code',
            (select c.code from sales.customers c where c.id = o.customer_id));
  return jsonb_build_object('ok', true, 'item', item, 'related', jsonb_build_object(
    'events', (select coalesce(jsonb_agg(to_jsonb(e) order by e.created_at), '[]'::jsonb)
                 from sales.order_events e where e.order_id = o.id),
    'notes', sales.admin_notes('order', o.id),
    'tasks', sales.admin_tasks('order', o.id),
    'customer', (select to_jsonb(c) from sales.customers c where c.id = o.customer_id),
    'subscription', (select to_jsonb(s) from sales.subscriptions s where s.order_id = o.id order by s.created_at limit 1),
    'jobs', (select coalesce(jsonb_agg(to_jsonb(j) order by j.created_at), '[]'::jsonb)
               from public.provisioning_jobs j where j.order_no = o.order_no),
    'numbers', (select coalesce(jsonb_agg(to_jsonb(n) order by n.created_at), '[]'::jsonb)
                  from public.phone_numbers n where n.order_no = o.order_no),
    'quote_snapshot', jsonb_build_object(
      'currency', o.currency, 'plan', o.plan, 'method', o.method,
      'monthly', jsonb_build_object('net', o.monthly_net, 'tax', o.monthly_tax, 'total', o.monthly_total),
      'after_discount', o.after_discount, 'discount', o.discount, 'first_month', o.first_month,
      'tax_rate', o.tax_rate, 'tax_treatment', o.tax_treatment,
      'voice_minutes', o.voice_minutes, 'alimtalk', o.alimtalk, 'voice_available', o.voice_available,
      'pricing_version', o.pricing_version, 'policy_version', o.policy_version)));
end;
$function$;

create or replace function sales.admin_get_customer(v_id uuid)
returns jsonb
language plpgsql
stable
as $function$
declare
  c    sales.customers%rowtype;
  item jsonb;
begin
  select * into c from sales.customers where id = v_id;
  if not found then perform sales.admin_fail('not_found'); end if;
  item := to_jsonb(c) || jsonb_build_object(
    'tenant_name', (select t.name from public.tenants t where t.id = c.tenant_id),
    'receivable', (select coalesce(sum(i.total - coalesce((select sum(case when p.kind = 'payment' then p.amount else -p.amount end)
                                                              from sales.payments p where p.invoice_id = i.id), 0)), 0)
                     from sales.invoices i where i.customer_id = c.id and i.archived_at is null
                      and i.status in ('issued', 'overdue', 'partially_paid')));
  return jsonb_build_object('ok', true, 'item', item, 'related', jsonb_build_object(
    'orders', (select coalesce(jsonb_agg((to_jsonb(o) - 'ip_hash' - 'user_agent' - 'consent') order by o.created_at desc), '[]'::jsonb)
                 from sales.orders o where o.customer_id = c.id),
    'subscriptions', (select coalesce(jsonb_agg(to_jsonb(s) order by s.created_at desc), '[]'::jsonb)
                        from sales.subscriptions s where s.customer_id = c.id),
    'invoices', (select coalesce(jsonb_agg(sales.invoice_json(i.id) order by i.created_at desc), '[]'::jsonb)
                   from sales.invoices i where i.customer_id = c.id),
    'payments', (select coalesce(jsonb_agg(to_jsonb(p) || jsonb_build_object('invoice_no', i.invoice_no) order by p.received_at desc), '[]'::jsonb)
                   from sales.payments p join sales.invoices i on i.id = p.invoice_id where p.customer_id = c.id),
    'usage', sales.admin_usage_12(c.tenant_id),
    'tenant', sales.admin_tenant_json(c.tenant_id),
    'notes', sales.admin_notes('customer', c.id),
    'tasks', sales.admin_tasks('customer', c.id)));
end;
$function$;

create or replace function sales.admin_get_invoice(v_id uuid)
returns jsonb
language plpgsql
stable
as $function$
declare
  item jsonb := sales.invoice_json(v_id);
begin
  if item is null then perform sales.admin_fail('not_found'); end if;
  return jsonb_build_object('ok', true, 'item', item, 'related', jsonb_build_object(
    'customer', (select to_jsonb(c) from sales.customers c where c.id = sales.to_uuid(item->>'customer_id')),
    'subscription', (select to_jsonb(s) from sales.subscriptions s where s.id = sales.to_uuid(item->>'subscription_id')),
    'payments', (select coalesce(jsonb_agg(to_jsonb(p) order by p.received_at), '[]'::jsonb)
                   from sales.payments p where p.invoice_id = v_id),
    'notes', sales.admin_notes('invoice', v_id)));
end;
$function$;

create or replace function sales.admin_get_subscription(v_id uuid)
returns jsonb
language plpgsql
stable
as $function$
declare
  item jsonb;
begin
  select to_jsonb(s) || jsonb_build_object('company', c.company, 'customer_code', c.code,
           'tenant_name', (select t.name from public.tenants t where t.id = s.tenant_id))
    into item
    from sales.subscriptions s join sales.customers c on c.id = s.customer_id where s.id = v_id;
  if item is null then perform sales.admin_fail('not_found'); end if;
  return jsonb_build_object('ok', true, 'item', item, 'related', jsonb_build_object(
    'customer', (select to_jsonb(c) from sales.customers c where c.id = sales.to_uuid(item->>'customer_id')),
    'invoices', (select coalesce(jsonb_agg(sales.invoice_json(i.id) order by i.created_at desc), '[]'::jsonb)
                   from sales.invoices i where i.subscription_id = v_id),
    'order', (select jsonb_build_object('id', o.id, 'order_no', o.order_no, 'state', o.state)
                from sales.orders o where o.id = sales.to_uuid(item->>'order_id')),
    'notes', sales.admin_notes('subscription', v_id)));
end;
$function$;

create or replace function sales.admin_get_campaign(v_id uuid)
returns jsonb
language plpgsql
stable
as $function$
declare
  item jsonb;
begin
  select to_jsonb(cp) into item from sales.campaigns cp where cp.id = v_id;
  if item is null then perform sales.admin_fail('not_found'); end if;
  return jsonb_build_object('ok', true, 'item', item, 'related', jsonb_build_object(
    'leads_count', (select count(*) from sales.leads l where l.campaign_id = v_id and l.archived_at is null),
    'orders_count', (select count(*) from sales.leads l where l.campaign_id = v_id and l.converted_order_id is not null),
    'recent_leads', (select coalesce(jsonb_agg((to_jsonb(l) - 'ip_hash' - 'user_agent' - 'consent') order by l.created_at desc), '[]'::jsonb)
                       from (select * from sales.leads l where l.campaign_id = v_id and l.archived_at is null
                              order by l.created_at desc limit 10) l),
    'notes', sales.admin_notes('campaign', v_id)));
end;
$function$;

create or replace function sales.admin_get_tenant(v_id uuid)
returns jsonb
language plpgsql
stable
as $function$
declare
  spec jsonb := sales.admin_list_spec('tenants');
  item jsonb;
begin
  execute format('select %s from %s where t.id = $1', spec->>'sel', spec->>'from') into item using v_id;
  if item is null then perform sales.admin_fail('not_found'); end if;
  return jsonb_build_object('ok', true, 'item', item, 'related', jsonb_build_object(
    'tenant', sales.admin_tenant_json(v_id),
    'customer', (select to_jsonb(c) from sales.customers c where c.tenant_id = v_id and c.archived_at is null
                  order by c.created_at limit 1),
    'usage', sales.admin_usage_12(v_id),
    'numbers', (select coalesce(jsonb_agg(to_jsonb(n) order by n.created_at), '[]'::jsonb)
                  from public.phone_numbers n where n.tenant_id = v_id),
    'jobs', (select coalesce(jsonb_agg(to_jsonb(j) order by j.created_at), '[]'::jsonb)
               from public.provisioning_jobs j where j.tenant_id = v_id)));
end;
$function$;

-- 그 밖의 엔티티: 목록 한 줄과 같은 모양을 pk 로 하나만
create or replace function sales.admin_get_generic(p_entity text, v_id uuid)
returns jsonb
language plpgsql
stable
as $function$
declare
  spec jsonb := sales.admin_list_spec(p_entity);
  item jsonb;
begin
  execute format('select %s from %s where %s = $1', spec->>'sel', spec->>'from', spec->>'pk')
     into item using v_id;
  if item is null then perform sales.admin_fail('not_found'); end if;
  return jsonb_build_object('ok', true, 'item', item, 'related', '{}'::jsonb);
end;
$function$;

create or replace function sales.admin_get_impl(u sales.admin_users, p_entity text, p_id text)
returns jsonb
language plpgsql
as $function$
declare
  v_id uuid;
  item jsonb;
begin
  if p_entity = 'users' then
    perform sales.admin_require(u, 'owner');
  end if;
  if p_entity = 'audit' then
    if coalesce(p_id, '') !~ '^[0-9]{1,18}$' then perform sales.admin_fail('not_found'); end if;
    select to_jsonb(a) into item from sales.admin_audit a where a.id = p_id::bigint;
    if item is null then perform sales.admin_fail('not_found'); end if;
    return jsonb_build_object('ok', true, 'item', item, 'related', '{}'::jsonb);
  end if;
  perform sales.admin_list_spec(p_entity);          -- 엔티티 이름 검사
  v_id := sales.admin_resolve(p_entity, p_id);
  return case p_entity
    when 'leads'         then sales.admin_get_lead(v_id)
    when 'orders'        then sales.admin_get_order(v_id)
    when 'customers'     then sales.admin_get_customer(v_id)
    when 'invoices'      then sales.admin_get_invoice(v_id)
    when 'subscriptions' then sales.admin_get_subscription(v_id)
    when 'campaigns'     then sales.admin_get_campaign(v_id)
    when 'tenants'       then sales.admin_get_tenant(v_id)
    else sales.admin_get_generic(p_entity, v_id) end;
end;
$function$;

-- ---------------------------------------------------------------------
-- 10. 저장(admin_save): 화이트리스트 컬럼만, 형식 검사 뒤 동적 UPDATE/INSERT
-- ---------------------------------------------------------------------

-- 화이트리스트 밖의 키가 있으면 invalid + fields
create or replace function sales.chk_keys(p_data jsonb, p_allowed text[])
returns void
language plpgsql
as $function$
declare
  bad jsonb;
begin
  if p_data is null or jsonb_typeof(p_data) <> 'object' then
    perform sales.admin_fail('invalid', '["data"]'::jsonb);
  end if;
  select coalesce(jsonb_agg(k), '[]'::jsonb) into bad
    from jsonb_object_keys(p_data) k where k <> all (p_allowed);
  if jsonb_array_length(bad) > 0 then
    perform sales.admin_fail('invalid', bad);
  end if;
end;
$function$;

-- 컬럼 타입에 맞춰 $1->>'col' 을 캐스팅하는 식. 컬럼이 없으면 invalid.
create or replace function sales.admin_cast_expr(p_table text, p_col text)
returns text
language plpgsql
stable
as $function$
declare
  v_type text;
begin
  select format_type(a.atttypid, a.atttypmod) into v_type
    from pg_attribute a
    join pg_class c on c.oid = a.attrelid
    join pg_namespace n on n.oid = c.relnamespace
   where n.nspname = 'sales' and c.relname = p_table and a.attname = p_col
     and a.attnum > 0 and not a.attisdropped;
  if v_type is null then
    perform sales.admin_fail('invalid', jsonb_build_array(p_col));
  end if;
  if v_type = 'jsonb' then
    return format('$1->%L', p_col);
  elsif v_type = 'text[]' then
    return format('(case when jsonb_typeof($1->%L) = ''array'' '
               || 'then array(select jsonb_array_elements_text($1->%L)) else null end)::text[]', p_col, p_col);
  elsif v_type = 'text' then
    return format('nullif(btrim($1->>%L), '''')', p_col);
  else
    return format('nullif($1->>%L, '''')::%s', p_col, v_type);
  end if;
end;
$function$;

create or replace function sales.admin_has_col(p_table text, p_col text)
returns boolean
language sql
stable
as $function$
  select exists (select 1 from pg_attribute a join pg_class c on c.oid = a.attrelid
                   join pg_namespace n on n.oid = c.relnamespace
                  where n.nspname = 'sales' and c.relname = p_table and a.attname = p_col
                    and a.attnum > 0 and not a.attisdropped);
$function$;

-- p_id 가 null 이면 insert, 아니면 update. 바뀐 행을 jsonb 로 돌려준다.
create or replace function sales.admin_write(p_table text, p_id uuid, p_data jsonb, p_allowed text[])
returns jsonb
language plpgsql
as $function$
declare
  k      text;
  v_cols text[] := '{}';
  v_vals text[] := '{}';
  v_sets text[] := '{}';
  v_row  jsonb;
begin
  perform sales.chk_keys(p_data, p_allowed);
  for k in select kk from jsonb_object_keys(p_data) kk loop
    v_cols := v_cols || k;
    v_vals := v_vals || sales.admin_cast_expr(p_table, k);
    v_sets := v_sets || format('%I = %s', k, sales.admin_cast_expr(p_table, k));
  end loop;
  if p_id is null then
    if array_length(v_cols, 1) is null then
      perform sales.admin_fail('invalid', '["data"]'::jsonb);
    end if;
    execute format('insert into sales.%I as t (%s) values (%s) returning to_jsonb(t)',
                   p_table,
                   (select string_agg(format('%I', c), ', ') from unnest(v_cols) c),
                   array_to_string(v_vals, ', '))
       into v_row using p_data;
  else
    if sales.admin_has_col(p_table, 'updated_at') then
      -- 리터럴엔 ::text 를 붙인다. 없으면 text[] || unknown 이 배열 이어붙이기(array_cat)로 풀려
      -- 'malformed array literal'(22P02) 이 난다.
      v_sets := v_sets || 'updated_at = now()'::text;
    end if;
    if array_length(v_sets, 1) is null then
      execute format('select to_jsonb(t) from sales.%I t where t.id = $2', p_table) into v_row using p_data, p_id;
    else
      execute format('update sales.%I as t set %s where t.id = $2 returning to_jsonb(t)',
                     p_table, array_to_string(v_sets, ', '))
         into v_row using p_data, p_id;
    end if;
    if v_row is null then
      perform sales.admin_fail('not_found');
    end if;
  end if;
  return v_row;
end;
$function$;

-- 활성 요금표의 플랜 id 목록 'start,grow,scale'
create or replace function sales.plan_ids()
returns text
language sql
stable
as $function$
  select coalesce(string_agg(value->>'id', ','), 'start,grow,scale')
    from jsonb_array_elements(coalesce(sales.pricing_active()->'plans', '[]'::jsonb));
$function$;

create or replace function sales.admin_save_lead(u sales.admin_users, p_id uuid, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  allowed text[] := array['name', 'email', 'phone', 'company', 'industry', 'message', 'status',
                          'owner_note', 'assignee', 'next_action_at', 'campaign_id', 'source', 'locale'];
  v_before jsonb;
  v_after  jsonb;
  v_ref    text;
begin
  perform sales.chk_keys(d, allowed);
  perform sales.chk(d, 'name', 'text', '200');
  perform sales.chk(d, 'email', 'email');
  perform sales.chk(d, 'phone', 'text', '60');
  perform sales.chk(d, 'company', 'text', '200');
  perform sales.chk(d, 'industry', 'text', '120');
  perform sales.chk(d, 'message', 'text', '4000');
  perform sales.chk(d, 'status', 'enum', 'new,contacted,qualified,proposal,won,lost,spam');
  perform sales.chk(d, 'owner_note', 'text', '4000');
  perform sales.chk(d, 'assignee', 'text', '80');
  perform sales.chk(d, 'next_action_at', 'ts');
  perform sales.chk(d, 'campaign_id', 'uuid');
  perform sales.chk(d, 'source', 'text', '60');
  perform sales.chk(d, 'locale', 'enum', 'ko,en');
  if d->>'email' is not null then
    d := d || jsonb_build_object('email', lower(btrim(d->>'email')));
  end if;
  if d->>'campaign_id' is not null
     and not exists (select 1 from sales.campaigns where id = (d->>'campaign_id')::uuid) then
    perform sales.admin_fail('invalid', '["campaign_id"]'::jsonb);
  end if;
  if p_id is null then
    perform sales.chk(d, 'email', 'req');
    v_ref := 'IN-' || to_char(timezone('Asia/Seoul', now()), 'YYYYMMDD')
          || '-' || upper(substr(encode(extensions.gen_random_bytes(3), 'hex'), 1, 5));
    d := d || jsonb_build_object('ref', v_ref,
           'status', coalesce(d->>'status', 'new'),
           'source', coalesce(d->>'source', 'admin'),
           'locale', coalesce(d->>'locale', 'ko'));
    v_after := sales.admin_write('leads', null, d, allowed || array['ref']);
  else
    select to_jsonb(l) into v_before from sales.leads l where l.id = p_id;
    if v_before is null then perform sales.admin_fail('not_found'); end if;
    v_after := sales.admin_write('leads', p_id, d, allowed);
  end if;
  perform sales.campaign_attach((v_after->>'id')::uuid);
  select to_jsonb(l) into v_after from sales.leads l where l.id = (v_after->>'id')::uuid;
  perform sales.admin_audit(u, case when p_id is null then 'leads.create' else 'leads.update' end,
                            'lead', v_after->>'id', v_before, v_after);
  return jsonb_build_object('ok', true, 'item', v_after);
end;
$function$;

create or replace function sales.admin_save_order(u sales.admin_users, p_id uuid, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  allowed text[] := array['assignee', 'next_action_at', 'owner_note', 'customer_id', 'tax_email',
                          'phone', 'billing_address', 'note'];
  v_before jsonb;
  v_after  jsonb;
begin
  if p_id is null then
    perform sales.admin_fail('invalid', '["id"]'::jsonb);      -- 주문은 사이트가 만든다
  end if;
  perform sales.chk_keys(d, allowed);
  perform sales.chk(d, 'assignee', 'text', '80');
  perform sales.chk(d, 'next_action_at', 'ts');
  perform sales.chk(d, 'owner_note', 'text', '4000');
  perform sales.chk(d, 'customer_id', 'uuid');
  perform sales.chk(d, 'tax_email', 'email');
  perform sales.chk(d, 'phone', 'text', '60');
  perform sales.chk(d, 'billing_address', 'text', '400');
  perform sales.chk(d, 'note', 'text', '4000');
  if d->>'customer_id' is not null
     and not exists (select 1 from sales.customers where id = (d->>'customer_id')::uuid) then
    perform sales.admin_fail('invalid', '["customer_id"]'::jsonb);
  end if;
  select to_jsonb(o) into v_before from sales.orders o where o.id = p_id;
  if v_before is null then perform sales.admin_fail('not_found'); end if;
  v_after := sales.admin_write('orders', p_id, d, allowed);
  perform sales.admin_audit(u, 'orders.update', 'order', p_id::text, v_before, v_after);
  return jsonb_build_object('ok', true, 'item', v_after);
end;
$function$;

create or replace function sales.admin_save_customer(u sales.admin_users, p_id uuid, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  allowed text[] := array['company', 'contact_name', 'email', 'phone', 'country', 'currency', 'buyer_type',
                          'tax_id', 'tax_treatment', 'billing_address', 'lang', 'tenant_id', 'status',
                          'source', 'tags', 'owner_note'];
  v_before jsonb;
  v_after  jsonb;
  v_email  text;
begin
  perform sales.chk_keys(d, allowed);
  perform sales.chk(d, 'company', 'text', '200');
  perform sales.chk(d, 'contact_name', 'text', '120');
  perform sales.chk(d, 'email', 'email');
  perform sales.chk(d, 'phone', 'text', '60');
  perform sales.chk(d, 'country', 'text', '8');
  perform sales.chk(d, 'currency', 'enum', 'KRW,USD');
  perform sales.chk(d, 'buyer_type', 'enum', 'business,consumer,public,unknown');
  perform sales.chk(d, 'tax_id', 'text', '60');
  perform sales.chk(d, 'tax_treatment', 'enum', 'vat_charged,reverse,none,review');
  perform sales.chk(d, 'billing_address', 'text', '400');
  perform sales.chk(d, 'lang', 'enum', 'ko,en');
  perform sales.chk(d, 'tenant_id', 'uuid');
  perform sales.chk(d, 'status', 'enum', 'lead,trial,active,paused,churned');
  perform sales.chk(d, 'source', 'text', '60');
  perform sales.chk(d, 'tags', 'arr');
  perform sales.chk(d, 'owner_note', 'text', '4000');
  if d ? 'tags' and jsonb_typeof(d->'tags') = 'array' then
    if jsonb_array_length(d->'tags') > 20 or exists (
         select 1 from jsonb_array_elements(d->'tags') x
          where jsonb_typeof(x) <> 'string' or length(x #>> '{}') > 40 or btrim(x #>> '{}') = '') then
      perform sales.admin_fail('invalid', '["tags"]'::jsonb);
    end if;
  end if;
  if d->>'country' is not null then
    d := d || jsonb_build_object('country', upper(btrim(d->>'country')));
  end if;
  if d->>'tenant_id' is not null and not exists (
       select 1 from public.tenants t where t.id = (d->>'tenant_id')::uuid and t.name <> '__system__') then
    perform sales.admin_fail('invalid', '["tenant_id"]'::jsonb);
  end if;
  if d->>'email' is not null then
    v_email := lower(btrim(d->>'email'));
    d := d || jsonb_build_object('email', v_email);
    if exists (select 1 from sales.customers c where lower(c.email) = v_email and c.archived_at is null
                  and c.id is distinct from p_id) then
      perform sales.admin_fail('conflict', '["email"]'::jsonb);
    end if;
  end if;
  if p_id is null then
    perform sales.chk(d, 'company', 'req');
    perform sales.chk(d, 'email', 'req');
    d := d || jsonb_build_object('code', sales.next_customer_code(),
           'source', coalesce(d->>'source', 'admin'));
    v_after := sales.admin_write('customers', null, d, allowed || array['code']);
  else
    select to_jsonb(c) into v_before from sales.customers c where c.id = p_id;
    if v_before is null then perform sales.admin_fail('not_found'); end if;
    v_after := sales.admin_write('customers', p_id, d, allowed);
  end if;
  perform sales.admin_audit(u, case when p_id is null then 'customers.create' else 'customers.update' end,
                            'customer', v_after->>'id', v_before, v_after);
  return jsonb_build_object('ok', true, 'item', v_after);
end;
$function$;

create or replace function sales.admin_save_subscription(u sales.admin_users, p_id uuid, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  allowed text[] := array['customer_id', 'order_id', 'plan', 'currency', 'list_price', 'discount_percent',
                          'discount_until', 'status', 'started_at', 'current_period_start',
                          'current_period_end', 'cancel_at', 'tenant_id', 'note'];
  v_before jsonb;
  v_after  jsonb;
begin
  perform sales.chk_keys(d, allowed);
  perform sales.chk(d, 'customer_id', 'uuid');
  perform sales.chk(d, 'order_id', 'uuid');
  perform sales.chk(d, 'plan', 'enum', sales.plan_ids());
  perform sales.chk(d, 'currency', 'enum', 'KRW,USD');
  perform sales.chk(d, 'list_price', 'num', '0');
  perform sales.chk(d, 'discount_percent', 'num', '0');
  perform sales.chk(d, 'discount_until', 'date');
  perform sales.chk(d, 'status', 'enum', 'pending,trial,active,paused,canceled');
  perform sales.chk(d, 'started_at', 'date');
  perform sales.chk(d, 'current_period_start', 'date');
  perform sales.chk(d, 'current_period_end', 'date');
  perform sales.chk(d, 'cancel_at', 'date');
  perform sales.chk(d, 'tenant_id', 'uuid');
  perform sales.chk(d, 'note', 'text', '4000');
  if d->>'discount_percent' is not null and (d->>'discount_percent')::numeric > 100 then
    perform sales.admin_fail('invalid', '["discount_percent"]'::jsonb);
  end if;
  if d->>'customer_id' is not null
     and not exists (select 1 from sales.customers where id = (d->>'customer_id')::uuid) then
    perform sales.admin_fail('invalid', '["customer_id"]'::jsonb);
  end if;
  if d->>'tenant_id' is not null and not exists (
       select 1 from public.tenants t where t.id = (d->>'tenant_id')::uuid and t.name <> '__system__') then
    perform sales.admin_fail('invalid', '["tenant_id"]'::jsonb);
  end if;
  if p_id is null then
    perform sales.chk(d, 'customer_id', 'req');
    perform sales.chk(d, 'plan', 'req');
    perform sales.chk(d, 'currency', 'req');
    if d->>'list_price' is null then
      d := d || jsonb_build_object('list_price',
             coalesce((sales.pricing_plan(d->>'plan')->'price'->>(d->>'currency'))::numeric, 0));
    end if;
    v_after := sales.admin_write('subscriptions', null, d, allowed);
  else
    select to_jsonb(s) into v_before from sales.subscriptions s where s.id = p_id;
    if v_before is null then perform sales.admin_fail('not_found'); end if;
    v_after := sales.admin_write('subscriptions', p_id, d, allowed);
  end if;
  perform sales.admin_audit(u, case when p_id is null then 'subscriptions.create' else 'subscriptions.update' end,
                            'subscription', v_after->>'id', v_before, v_after);
  return jsonb_build_object('ok', true, 'item', v_after);
end;
$function$;

-- 인보이스: draft 일 때만 본문 편집. 합계는 항상 줄에서 다시 계산한다.
create or replace function sales.admin_save_invoice(u sales.admin_users, p_id uuid, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  allowed text[] := array['customer_id', 'subscription_id', 'order_id', 'period_start', 'period_end',
                          'currency', 'lines', 'due_at', 'method', 'provider', 'provider_ref',
                          'tax_document', 'note'];
  always  text[] := array['tax_document', 'note', 'provider_ref'];
  v_before jsonb;
  v_after  jsonb;
  v_i      sales.invoices%rowtype;
  v_c      sales.customers%rowtype;
  v_cur    text;
  v_tot    jsonb;
  bad      jsonb;
begin
  perform sales.chk_keys(d, allowed);
  perform sales.chk(d, 'customer_id', 'uuid');
  perform sales.chk(d, 'subscription_id', 'uuid');
  perform sales.chk(d, 'order_id', 'uuid');
  perform sales.chk(d, 'period_start', 'date');
  perform sales.chk(d, 'period_end', 'date');
  perform sales.chk(d, 'currency', 'enum', 'KRW,USD');
  perform sales.chk(d, 'lines', 'arr');
  perform sales.chk(d, 'due_at', 'date');
  perform sales.chk(d, 'method', 'enum', 'card,transfer,other');
  perform sales.chk(d, 'provider', 'text', '60');
  perform sales.chk(d, 'provider_ref', 'text', '200');
  perform sales.chk(d, 'tax_document', 'text', '200');
  perform sales.chk(d, 'note', 'text', '4000');

  if p_id is not null then
    select * into v_i from sales.invoices where id = p_id;
    if not found then perform sales.admin_fail('not_found'); end if;
    v_before := to_jsonb(v_i);
    if v_i.status <> 'draft' then
      select coalesce(jsonb_agg(k), '[]'::jsonb) into bad from jsonb_object_keys(d) k where k <> all (always);
      if jsonb_array_length(bad) > 0 then
        perform sales.admin_fail('invalid', bad);
      end if;
      v_after := sales.admin_write('invoices', p_id, d, always);
      perform sales.admin_audit(u, 'invoices.update', 'invoice', p_id::text, v_before, v_after);
      return jsonb_build_object('ok', true, 'item', sales.invoice_json(p_id));
    end if;
  else
    perform sales.chk(d, 'customer_id', 'req');
  end if;

  select * into v_c from sales.customers
   where id = coalesce((d->>'customer_id')::uuid, v_i.customer_id);
  if not found then perform sales.admin_fail('invalid', '["customer_id"]'::jsonb); end if;
  if d->>'subscription_id' is not null and not exists (
       select 1 from sales.subscriptions s where s.id = (d->>'subscription_id')::uuid and s.customer_id = v_c.id) then
    perform sales.admin_fail('invalid', '["subscription_id"]'::jsonb);
  end if;
  v_cur := coalesce(d->>'currency', v_i.currency, v_c.currency);
  v_tot := sales.invoice_totals(coalesce(d->'lines', v_i.lines, '[]'::jsonb),
                                sales.customer_tax_rate(v_c.tax_treatment), v_cur);
  d := d || jsonb_build_object('currency', v_cur, 'lines', v_tot->'lines', 'net', v_tot->'net',
         'tax_rate', sales.customer_tax_rate(v_c.tax_treatment), 'tax', v_tot->'tax', 'total', v_tot->'total');
  if p_id is null then
    d := d || jsonb_build_object('invoice_no', sales.next_invoice_no(), 'status', 'draft');
    v_after := sales.admin_write('invoices', null, d,
                 allowed || array['net', 'tax_rate', 'tax', 'total', 'invoice_no', 'status']);
  else
    v_after := sales.admin_write('invoices', p_id, d, allowed || array['net', 'tax_rate', 'tax', 'total']);
  end if;
  perform sales.admin_audit(u, case when p_id is null then 'invoices.create' else 'invoices.update' end,
                            'invoice', v_after->>'id', v_before, v_after);
  return jsonb_build_object('ok', true, 'item', sales.invoice_json((v_after->>'id')::uuid));
end;
$function$;

create or replace function sales.admin_save_campaign(u sales.admin_users, p_id uuid, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  allowed text[] := array['name', 'channel', 'utm_source', 'utm_medium', 'utm_campaign', 'country', 'lang',
                          'budget', 'currency', 'starts_on', 'ends_on', 'status', 'landing_url', 'note'];
  v_before jsonb;
  v_after  jsonb;
begin
  perform sales.chk_keys(d, allowed);
  perform sales.chk(d, 'name', 'text', '200');
  perform sales.chk(d, 'channel', 'enum', 'search,social,email,referral,event,partner,content,other');
  perform sales.chk(d, 'utm_source', 'text', '120');
  perform sales.chk(d, 'utm_medium', 'text', '120');
  perform sales.chk(d, 'utm_campaign', 'text', '200');
  perform sales.chk(d, 'country', 'text', '8');
  perform sales.chk(d, 'lang', 'enum', 'ko,en');
  perform sales.chk(d, 'budget', 'num', '0');
  perform sales.chk(d, 'currency', 'enum', 'KRW,USD');
  perform sales.chk(d, 'starts_on', 'date');
  perform sales.chk(d, 'ends_on', 'date');
  perform sales.chk(d, 'status', 'enum', 'planned,active,paused,ended');
  perform sales.chk(d, 'landing_url', 'text', '500');
  perform sales.chk(d, 'note', 'text', '4000');
  if d->>'country' is not null then
    d := d || jsonb_build_object('country', upper(btrim(d->>'country')));
  end if;
  if p_id is null then
    perform sales.chk(d, 'name', 'req');
    v_after := sales.admin_write('campaigns', null, d, allowed);
  else
    select to_jsonb(cp) into v_before from sales.campaigns cp where cp.id = p_id;
    if v_before is null then perform sales.admin_fail('not_found'); end if;
    v_after := sales.admin_write('campaigns', p_id, d, allowed);
  end if;
  perform sales.campaign_attach_all((v_after->>'id')::uuid);
  perform sales.admin_audit(u, case when p_id is null then 'campaigns.create' else 'campaigns.update' end,
                            'campaign', v_after->>'id', v_before, v_after);
  return jsonb_build_object('ok', true, 'item', v_after);
end;
$function$;

create or replace function sales.admin_save_task(u sales.admin_users, p_id uuid, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  allowed text[] := array['kind', 'title', 'entity', 'entity_id', 'due_at', 'assignee', 'note'];
  v_before jsonb;
  v_after  jsonb;
begin
  perform sales.chk_keys(d, allowed);
  perform sales.chk(d, 'kind', 'enum', 'call,email,followup,contract,provisioning,billing,other');
  perform sales.chk(d, 'title', 'text', '200');
  perform sales.chk(d, 'entity', 'enum', 'lead,order,customer,invoice');
  perform sales.chk(d, 'entity_id', 'uuid');
  perform sales.chk(d, 'due_at', 'ts');
  perform sales.chk(d, 'assignee', 'text', '80');
  perform sales.chk(d, 'note', 'text', '4000');
  if p_id is null then
    perform sales.chk(d, 'title', 'req');
    d := d || jsonb_build_object('created_by', u.username, 'kind', coalesce(d->>'kind', 'other'));
    v_after := sales.admin_write('tasks', null, d, allowed || array['created_by']);
  else
    select to_jsonb(tk) into v_before from sales.tasks tk where tk.id = p_id;
    if v_before is null then perform sales.admin_fail('not_found'); end if;
    v_after := sales.admin_write('tasks', p_id, d, allowed);
  end if;
  perform sales.admin_audit(u, case when p_id is null then 'tasks.create' else 'tasks.update' end,
                            'task', v_after->>'id', v_before, v_after);
  return jsonb_build_object('ok', true, 'item', v_after);
end;
$function$;

create or replace function sales.admin_save_note(u sales.admin_users, p_id uuid, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  allowed text[] := array['entity', 'entity_id', 'body'];
  v_before jsonb;
  v_after  jsonb;
begin
  perform sales.chk_keys(d, allowed);
  perform sales.chk(d, 'entity', 'enum', 'lead,order,customer,invoice,subscription,campaign');
  perform sales.chk(d, 'entity_id', 'uuid');
  perform sales.chk(d, 'body', 'text', '8000');
  if p_id is null then
    perform sales.chk(d, 'entity', 'req');
    perform sales.chk(d, 'entity_id', 'req');
    perform sales.chk(d, 'body', 'req');
    d := d || jsonb_build_object('author', u.username);
    v_after := sales.admin_write('notes', null, d, allowed || array['author']);
  else
    select to_jsonb(n) into v_before from sales.notes n where n.id = p_id;
    if v_before is null then perform sales.admin_fail('not_found'); end if;
    v_after := sales.admin_write('notes', p_id, d, allowed);
  end if;
  perform sales.admin_audit(u, case when p_id is null then 'notes.create' else 'notes.update' end,
                            'note', v_after->>'id', v_before, v_after);
  return jsonb_build_object('ok', true, 'item', v_after);
end;
$function$;

create or replace function sales.admin_save_impl(u sales.admin_users, p_entity text, p_id text, p_data jsonb)
returns jsonb
language plpgsql
as $function$
declare
  v_id uuid;
  d    jsonb := coalesce(p_data, '{}'::jsonb);
begin
  perform sales.admin_require(u, 'staff');              -- viewer 는 쓰지 못한다
  if jsonb_typeof(d) <> 'object' then
    perform sales.admin_fail('invalid', '["data"]'::jsonb);
  end if;
  if nullif(btrim(coalesce(p_id, '')), '') is not null then
    v_id := sales.admin_resolve(p_entity, p_id);
  end if;
  return case p_entity
    when 'leads'         then sales.admin_save_lead(u, v_id, d)
    when 'orders'        then sales.admin_save_order(u, v_id, d)
    when 'customers'     then sales.admin_save_customer(u, v_id, d)
    when 'subscriptions' then sales.admin_save_subscription(u, v_id, d)
    when 'invoices'      then sales.admin_save_invoice(u, v_id, d)
    when 'campaigns'     then sales.admin_save_campaign(u, v_id, d)
    when 'tasks'         then sales.admin_save_task(u, v_id, d)
    when 'notes'         then sales.admin_save_note(u, v_id, d)
    else sales.admin_err('invalid', '["entity"]'::jsonb) end;
end;
$function$;

-- ---------------------------------------------------------------------
-- 11. 동작(admin_action): 부수효과가 있는 것. 전부 전후 값을 감사에 남긴다.
-- ---------------------------------------------------------------------

-- 보관/복구 (소프트 삭제). 인보이스는 draft/void 만.
create or replace function sales.admin_archive(u sales.admin_users, p_entity text, v_id uuid, p_restore boolean)
returns jsonb
language plpgsql
as $function$
declare
  v_table  text;
  v_before jsonb;
  v_after  jsonb;
begin
  v_table := case p_entity
    when 'leads' then 'leads' when 'orders' then 'orders' when 'customers' then 'customers'
    when 'campaigns' then 'campaigns' when 'invoices' then 'invoices' else null end;
  if v_table is null then
    perform sales.admin_fail('invalid', '["action"]'::jsonb);
  end if;
  execute format('select to_jsonb(t) from sales.%I t where t.id = $1', v_table) into v_before using v_id;
  if v_before is null then
    perform sales.admin_fail('not_found');
  end if;
  if p_entity = 'invoices' and not p_restore and (v_before->>'status') not in ('draft', 'void') then
    perform sales.admin_fail('bad_transition');
  end if;
  execute format('update sales.%I as t set archived_at = $2, updated_at = now() where t.id = $1 returning to_jsonb(t)', v_table)
     into v_after using v_id, (case when p_restore then null::timestamptz else now() end);
  perform sales.admin_audit(u, p_entity || '.' || case when p_restore then 'restore' else 'archive' end,
                            rtrim(p_entity, 's'), v_id::text, v_before, v_after);
  return jsonb_build_object('ok', true, 'item', v_after);
end;
$function$;

-- 주문 상태 전이. 사유는 detail 에 두고 reason 은 코드로 둔다
-- (주문 조회 화면이 order_events 를 보여 줄 수 있으므로 내부 메모를 흘리지 않는다).
create or replace function sales.admin_action_order(u sales.admin_users, v_id uuid, p_action text, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  v_o      sales.orders%rowtype;
  v_to     text;
  v_reason text;
  v_before jsonb;
  v_after  jsonb;
begin
  if p_action <> 'transition' then
    perform sales.admin_fail('invalid', '["action"]'::jsonb);
  end if;
  v_to := nullif(btrim(coalesce(d->>'state', '')), '');
  if v_to is null or v_to not in ('received', 'proposal_sent', 'under_review', 'contract_sent', 'contract_signed',
                                  'payment_pending', 'paid', 'active', 'cancelled', 'rejected') then
    perform sales.admin_fail('invalid', '["state"]'::jsonb);
  end if;
  v_reason := left(nullif(btrim(coalesce(d->>'reason', '')), ''), 500);
  select * into v_o from sales.orders where id = v_id for update;
  if not found then
    perform sales.admin_fail('not_found');
  end if;
  if v_o.archived_at is not null or not sales.order_transition_ok(v_o.state::text, v_to) then
    perform sales.admin_fail('bad_transition');
  end if;
  v_before := to_jsonb(v_o);

  update sales.orders set state = v_to::sales.order_state, updated_at = now() where id = v_id;
  insert into sales.order_events (order_id, from_state, to_state, actor, reason, detail)
  values (v_id, v_o.state, v_to::sales.order_state, u.username, 'admin',
          jsonb_build_object('note', v_reason, 'user_id', u.id));

  if v_to = 'contract_signed' or (v_to in ('active', 'paid') and v_o.customer_id is null) then
    perform sales.customer_upsert_from_order(v_id, u.username);
  end if;
  if v_to = 'active' then
    perform sales.subscription_activate(v_id);
  end if;
  if v_to in ('cancelled', 'rejected') then
    update sales.subscriptions
       set status = 'canceled', canceled_at = now(), cancel_at = sales.seoul_today()
     where order_id = v_id and status = 'pending';
  end if;
  -- 같은 이메일의 열린 리드를 이 주문에 잇는다 (계약 이상일 때)
  if v_to in ('contract_signed', 'active', 'paid') then
    update sales.leads
       set converted_order_id = v_id,
           status = case when status in ('new', 'received', 'contacted', 'qualified', 'proposal') then 'won' else status end,
           updated_at = now()
     where converted_order_id is null and archived_at is null and lower(email) = lower(v_o.email);
  end if;

  select * into v_o from sales.orders where id = v_id;
  v_after := to_jsonb(v_o);
  perform sales.admin_audit(u, 'orders.transition', 'order', v_id::text, v_before,
                            v_after || jsonb_build_object('reason', v_reason));
  return jsonb_build_object('ok', true,
    'item', v_after || jsonb_build_object('customer_code', (select c.code from sales.customers c where c.id = v_o.customer_id)),
    'events', (select coalesce(jsonb_agg(to_jsonb(e) order by e.created_at), '[]'::jsonb)
                 from sales.order_events e where e.order_id = v_id));
end;
$function$;

create or replace function sales.admin_action_lead(u sales.admin_users, v_id uuid, p_action text, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  v_l       sales.leads%rowtype;
  v_c       sales.customers%rowtype;
  v_status  text;
  v_after   jsonb;
  v_created boolean := false;
begin
  select * into v_l from sales.leads where id = v_id for update;
  if not found then
    perform sales.admin_fail('not_found');
  end if;
  if p_action = 'set_status' then
    v_status := nullif(btrim(coalesce(d->>'status', '')), '');
    if v_status is null or v_status not in ('new', 'contacted', 'qualified', 'proposal', 'won', 'lost', 'spam') then
      perform sales.admin_fail('invalid', '["status"]'::jsonb);
    end if;
    perform sales.chk(d, 'lost_reason', 'text', '500');
    update sales.leads as l
       set status = v_status,
           lost_reason = case when v_status = 'lost' then coalesce(nullif(btrim(d->>'lost_reason'), ''), l.lost_reason)
                              else l.lost_reason end,
           updated_at = now()
     where l.id = v_id
     returning to_jsonb(l) into v_after;
    perform sales.admin_audit(u, 'leads.set_status', 'lead', v_id::text, to_jsonb(v_l), v_after);
    return jsonb_build_object('ok', true, 'item', v_after);
  elsif p_action = 'convert' then
    select * into v_c from sales.customers
     where lower(email) = lower(v_l.email) and archived_at is null order by created_at limit 1;
    if not found then
      insert into sales.customers (code, company, contact_name, email, phone, lang, status, source)
      values (sales.next_customer_code(), coalesce(v_l.company, v_l.name, v_l.email), v_l.name,
              lower(v_l.email), v_l.phone, coalesce(v_l.locale, 'ko'), 'lead', 'lead')
      returning * into v_c;
      v_created := true;
    end if;
    perform sales.admin_audit(u, 'leads.convert', 'lead', v_id::text, to_jsonb(v_l),
                              jsonb_build_object('customer_id', v_c.id, 'created', v_created));
    return jsonb_build_object('ok', true, 'customer', to_jsonb(v_c), 'created', v_created);
  end if;
  perform sales.admin_fail('invalid', '["action"]'::jsonb);
  return null;
end;
$function$;

-- 구독 + 사용량으로 그 달의 인보이스 초안을 만든다.
create or replace function sales.invoice_generate(u sales.admin_users, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  v_c     sales.customers%rowtype;
  v_s     sales.subscriptions%rowtype;
  um      sales.usage_monthly%rowtype;
  v_i     sales.invoices%rowtype;
  v_month text;
  v_ps    date;
  v_pe    date;
  pr      jsonb;
  plan    jsonb;
  uv      jsonb;
  ua      jsonb;
  cur     text;
  lines   jsonb := '[]'::jsonb;
  v_unit  numeric;
  v_qty   numeric;
  v_tax   numeric;
  tot     jsonb;
begin
  perform sales.chk(d, 'customer_id', 'req');
  perform sales.chk(d, 'customer_id', 'uuid');
  v_month := coalesce(nullif(btrim(coalesce(d->>'month', '')), ''),
                      to_char(sales.seoul_today(), 'YYYY-MM'));
  if v_month !~ '^[0-9]{4}-(0[1-9]|1[0-2])$' then
    perform sales.admin_fail('invalid', '["month"]'::jsonb);
  end if;
  v_ps := (v_month || '-01')::date;
  v_pe := (v_ps + interval '1 month' - interval '1 day')::date;

  select * into v_c from sales.customers where id = (d->>'customer_id')::uuid;
  if not found then
    perform sales.admin_fail('not_found');
  end if;
  select * into v_s from sales.subscriptions
   where customer_id = v_c.id and status in ('active', 'paused')
   order by (status = 'active') desc, created_at desc limit 1;
  if not found then
    perform sales.admin_fail('invalid', '["subscription"]'::jsonb);
  end if;
  if exists (select 1 from sales.invoices i where i.subscription_id = v_s.id and i.period_start = v_ps
                and i.status <> 'void' and i.archived_at is null) then
    perform sales.admin_fail('conflict', '["month"]'::jsonb);
  end if;

  pr   := sales.pricing_active();
  plan := sales.pricing_plan(v_s.plan);
  cur  := v_s.currency;
  select * into um from sales.usage_monthly where tenant_id = v_c.tenant_id and month = v_ps;

  -- 플랜 월정액 (할인 기간이면 할인가)
  v_unit := case when v_s.discount_percent > 0 and v_s.discount_until is not null and v_s.discount_until >= v_ps
                 then sales.round_money(v_s.list_price * (100 - v_s.discount_percent) / 100, cur)
                 else v_s.list_price end;
  lines := lines || jsonb_build_object('kind', 'plan',
    'label', coalesce(plan->'name'->>'ko', initcap(v_s.plan)) || ' · ' || v_month
             || case when v_unit < v_s.list_price then ' (' || v_s.discount_percent || '% 할인)' else '' end,
    'qty', 1, 'unit', v_unit);

  -- 통화료: 플랜에 AI 전화가 있고 사용량이 있을 때
  select value into uv from jsonb_array_elements(coalesce(pr->'usage', '[]'::jsonb)) where value->>'id' = 'voiceMinutes';
  if coalesce((plan->>'voice')::boolean, false) and coalesce(um.voice_minutes, 0) > 0 and uv is not null then
    lines := lines || jsonb_build_object('kind', 'voice',
      'label', coalesce(uv->'name'->>'ko', 'AI 전화') || ' / ' || coalesce(uv->'name'->>'en', 'Voice') || ' · ' || v_month,
      'qty', um.voice_minutes, 'unit', (uv->'unitPrice'->>cur)::numeric);
  end if;
  -- 알림톡: 메신저 플랜 + 원화
  select value into ua from jsonb_array_elements(coalesce(pr->'usage', '[]'::jsonb)) where value->>'id' = 'alimtalk';
  if coalesce((plan->>'messenger')::boolean, false) and cur = 'KRW' and coalesce(um.alimtalk, 0) > 0 and ua is not null then
    lines := lines || jsonb_build_object('kind', 'alimtalk',
      'label', coalesce(ua->'name'->>'ko', '알림톡') || ' / ' || coalesce(ua->'name'->>'en', 'Messages') || ' · ' || v_month,
      'qty', um.alimtalk, 'unit', (ua->'unitPrice'->>cur)::numeric);
  end if;
  -- 대화 초과분
  v_qty := greatest(0, coalesce(um.conversations, 0) - coalesce((plan->>'conversations')::int, 0));
  if plan is not null and v_qty > 0 and (pr->'overage'->'perConversation'->>cur) is not null then
    lines := lines || jsonb_build_object('kind', 'overage',
      'label', '대화 초과분 / Extra conversations · ' || v_month,
      'qty', v_qty, 'unit', (pr->'overage'->'perConversation'->>cur)::numeric);
  end if;

  v_tax := sales.customer_tax_rate(v_c.tax_treatment);
  tot   := sales.invoice_totals(lines, v_tax, cur);
  insert into sales.invoices (
    invoice_no, customer_id, subscription_id, order_id, period_start, period_end, currency,
    lines, net, tax_rate, tax, total, status
  ) values (
    sales.next_invoice_no(), v_c.id, v_s.id, v_s.order_id, v_ps, v_pe, cur,
    tot->'lines', (tot->>'net')::numeric, v_tax, (tot->>'tax')::numeric, (tot->>'total')::numeric, 'draft'
  ) returning * into v_i;
  perform sales.admin_audit(u, 'invoices.generate', 'invoice', v_i.id::text, null,
                            to_jsonb(v_i) || jsonb_build_object('usage', to_jsonb(um)));
  return jsonb_build_object('ok', true, 'item', sales.invoice_json(v_i.id), 'usage', to_jsonb(um));
end;
$function$;

-- 입금·환불 기록. 인보이스 상태는 invoice_recalc 가 다시 정한다.
create or replace function sales.invoice_pay(u sales.admin_users, v_i sales.invoices, d jsonb, p_kind text)
returns jsonb
language plpgsql
as $function$
declare
  v_amt  numeric;
  v_paid numeric;
  v_ref  numeric;
  v_p    sales.payments%rowtype;
  v_aft  jsonb;
begin
  perform sales.chk(d, 'amount', 'req');
  perform sales.chk(d, 'amount', 'num', '0');
  perform sales.chk(d, 'method', 'enum', 'card,transfer,other');
  perform sales.chk(d, 'provider', 'text', '60');
  perform sales.chk(d, 'provider_ref', 'text', '200');
  perform sales.chk(d, 'received_at', 'ts');
  perform sales.chk(d, 'note', 'text', '2000');
  v_amt := sales.round_money((d->>'amount')::numeric, v_i.currency);
  if v_amt <= 0 then
    perform sales.admin_fail('invalid', '["amount"]'::jsonb);
  end if;
  select coalesce(sum(amount) filter (where kind = 'payment'), 0),
         coalesce(sum(amount) filter (where kind = 'refund'), 0)
    into v_paid, v_ref from sales.payments where invoice_id = v_i.id;
  if p_kind = 'payment' and v_i.status not in ('issued', 'overdue', 'partially_paid') then
    perform sales.admin_fail('bad_transition');
  end if;
  if p_kind = 'refund' then
    if v_i.status not in ('paid', 'partially_paid', 'refunded') then
      perform sales.admin_fail('bad_transition');
    end if;
    if v_amt > v_paid - v_ref then
      perform sales.admin_fail('invalid', '["amount"]'::jsonb);
    end if;
  end if;
  insert into sales.payments (invoice_id, customer_id, amount, currency, method, provider, provider_ref,
                              received_at, kind, note, recorded_by)
  values (v_i.id, v_i.customer_id, v_amt, v_i.currency,
          coalesce(nullif(d->>'method', ''), v_i.method, 'other'),
          nullif(btrim(coalesce(d->>'provider', '')), ''), nullif(btrim(coalesce(d->>'provider_ref', '')), ''),
          coalesce((d->>'received_at')::timestamptz, now()), p_kind,
          nullif(btrim(coalesce(d->>'note', '')), ''), u.id)
  returning * into v_p;
  if p_kind = 'payment' and v_i.method is null then
    update sales.invoices set method = v_p.method, provider = coalesce(provider, v_p.provider) where id = v_i.id;
  end if;
  v_aft := sales.invoice_recalc(v_i.id);
  perform sales.admin_audit(u, 'payments.create', 'payment', v_p.id::text, null, to_jsonb(v_p));
  perform sales.admin_audit(u, 'invoices.' || case when p_kind = 'payment' then 'record_payment' else 'refund' end,
                            'invoice', v_i.id::text, to_jsonb(v_i), v_aft);
  return jsonb_build_object('ok', true, 'item', sales.invoice_json(v_i.id), 'payment', to_jsonb(v_p));
end;
$function$;

create or replace function sales.admin_action_invoice(u sales.admin_users, p_id text, p_action text, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  v_id     uuid;
  v_i      sales.invoices%rowtype;
  v_before jsonb;
begin
  if p_action = 'generate' then
    return sales.invoice_generate(u, d);
  end if;
  v_id := sales.admin_resolve('invoices', p_id);
  select * into v_i from sales.invoices where id = v_id for update;
  if not found then
    perform sales.admin_fail('not_found');
  end if;
  if v_i.archived_at is not null then
    perform sales.admin_fail('bad_transition');
  end if;
  v_before := to_jsonb(v_i);
  if p_action = 'issue' then
    if v_i.status <> 'draft' then perform sales.admin_fail('bad_transition'); end if;
    update sales.invoices
       set status = 'issued', issued_at = now(), due_at = coalesce(due_at, sales.seoul_today() + 14)
     where id = v_id;
  elsif p_action = 'void' then
    if v_i.status not in ('draft', 'issued', 'overdue') then perform sales.admin_fail('bad_transition'); end if;
    update sales.invoices set status = 'void' where id = v_id;
  elsif p_action = 'record_payment' then
    return sales.invoice_pay(u, v_i, d, 'payment');
  elsif p_action = 'refund' then
    return sales.invoice_pay(u, v_i, d, 'refund');
  else
    perform sales.admin_fail('invalid', '["action"]'::jsonb);
  end if;
  perform sales.admin_audit(u, 'invoices.' || p_action, 'invoice', v_id::text, v_before,
                            (select to_jsonb(i) from sales.invoices i where i.id = v_id));
  return jsonb_build_object('ok', true, 'item', sales.invoice_json(v_id));
end;
$function$;

create or replace function sales.admin_action_subscription(u sales.admin_users, v_id uuid, p_action text, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  v_s      sales.subscriptions%rowtype;
  v_before jsonb;
  v_after  jsonb;
  v_plan   text;
  v_price  numeric;
  v_eff    date;
  v_at     date;
  today    date := sales.seoul_today();
begin
  select * into v_s from sales.subscriptions where id = v_id for update;
  if not found then
    perform sales.admin_fail('not_found');
  end if;
  v_before := to_jsonb(v_s);
  if p_action = 'change_plan' then
    v_plan := nullif(btrim(coalesce(d->>'plan', '')), '');
    perform sales.chk(d, 'plan', 'req');
    perform sales.chk(d, 'plan', 'enum', sales.plan_ids());
    perform sales.chk(d, 'effective_on', 'date');
    v_eff   := coalesce((d->>'effective_on')::date, today);
    v_price := (sales.pricing_plan(v_plan)->'price'->>v_s.currency)::numeric;
    if v_price is null then perform sales.admin_fail('invalid', '["plan"]'::jsonb); end if;
    update sales.subscriptions
       set plan = v_plan, list_price = v_price,
           note = concat_ws(E'\n', note,
                    format('%s 플랜 변경 %s → %s (적용일 %s, %s)', today, v_s.plan, v_plan, v_eff, u.username))
     where id = v_id;
  elsif p_action = 'cancel' then
    if v_s.status = 'canceled' then perform sales.admin_fail('bad_transition'); end if;
    perform sales.chk(d, 'cancel_at', 'date');
    v_at := coalesce((d->>'cancel_at')::date, today);
    update sales.subscriptions
       set cancel_at   = v_at,
           status      = case when v_at <= today then 'canceled' else status end,
           canceled_at = case when v_at <= today then now() else null end
     where id = v_id;
    if v_at <= today and not exists (select 1 from sales.subscriptions s
                                      where s.customer_id = v_s.customer_id and s.id <> v_id
                                        and s.status in ('pending', 'trial', 'active', 'paused')) then
      update sales.customers set status = 'churned' where id = v_s.customer_id;
    end if;
  elsif p_action = 'pause' then
    if v_s.status <> 'active' then perform sales.admin_fail('bad_transition'); end if;
    update sales.subscriptions set status = 'paused' where id = v_id;
    update sales.customers set status = 'paused' where id = v_s.customer_id and status = 'active';
  elsif p_action = 'resume' then
    if v_s.status <> 'paused' then perform sales.admin_fail('bad_transition'); end if;
    update sales.subscriptions set status = 'active' where id = v_id;
    update sales.customers set status = 'active' where id = v_s.customer_id and status = 'paused';
  else
    perform sales.admin_fail('invalid', '["action"]'::jsonb);
  end if;
  select to_jsonb(s) into v_after from sales.subscriptions s where s.id = v_id;
  perform sales.admin_audit(u, 'subscriptions.' || p_action, 'subscription', v_id::text, v_before,
                            v_after || coalesce(jsonb_build_object('effective_on', v_eff), '{}'::jsonb));
  return jsonb_build_object('ok', true, 'item', v_after);
end;
$function$;

-- 고객 ↔ 운영 테넌트 연결
create or replace function sales.admin_link_tenant(u sales.admin_users, v_id uuid, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  v_before jsonb;
  v_after  jsonb;
  v_t      uuid;
begin
  perform sales.chk(d, 'tenant_id', 'uuid');
  v_t := sales.to_uuid(d->>'tenant_id');
  if v_t is not null and not exists (select 1 from public.tenants t where t.id = v_t and t.name <> '__system__') then
    perform sales.admin_fail('invalid', '["tenant_id"]'::jsonb);
  end if;
  select to_jsonb(c) into v_before from sales.customers c where c.id = v_id;
  if v_before is null then perform sales.admin_fail('not_found'); end if;
  update sales.customers as c set tenant_id = v_t where c.id = v_id returning to_jsonb(c) into v_after;
  update sales.subscriptions set tenant_id = v_t where customer_id = v_id and (tenant_id is null or v_t is null);
  perform sales.admin_audit(u, 'customers.link_tenant', 'customer', v_id::text, v_before, v_after);
  return jsonb_build_object('ok', true, 'item', v_after, 'tenant', sales.admin_tenant_json(v_t));
end;
$function$;

create or replace function sales.admin_action_misc(u sales.admin_users, p_entity text, p_id text, p_action text, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  v_id     uuid;
  v_before jsonb;
  v_after  jsonb;
  v_month  text;
  r        jsonb;
begin
  if p_entity = 'usage' and p_action = 'refresh' then
    v_month := nullif(btrim(coalesce(d->>'month', '')), '');
    if v_month is not null and v_month !~ '^[0-9]{4}-(0[1-9]|1[0-2])$' then
      perform sales.admin_fail('invalid', '["month"]'::jsonb);
    end if;
    r := sales.usage_refresh(case when v_month is null then null else (v_month || '-01')::date end);
    perform sales.admin_audit(u, 'usage.refresh', 'usage', r->>'month', null, r);
    return r;
  elsif p_entity = 'tasks' and p_action in ('done', 'reopen') then
    v_id := sales.admin_resolve('tasks', p_id);
    select to_jsonb(tk) into v_before from sales.tasks tk where tk.id = v_id;
    if v_before is null then perform sales.admin_fail('not_found'); end if;
    update sales.tasks as tk set done_at = case when p_action = 'done' then now() else null end
     where tk.id = v_id returning to_jsonb(tk) into v_after;
    perform sales.admin_audit(u, 'tasks.' || p_action, 'task', v_id::text, v_before, v_after);
    return jsonb_build_object('ok', true, 'item', v_after);
  elsif p_entity = 'campaigns' and p_action = 'attach' then
    v_id := sales.admin_resolve('campaigns', p_id);
    r := jsonb_build_object('attached', sales.campaign_attach_all(v_id));
    perform sales.admin_audit(u, 'campaigns.attach', 'campaign', v_id::text, null, r);
    return jsonb_build_object('ok', true) || r;
  elsif p_entity = 'customers' and p_action = 'link_tenant' then
    return sales.admin_link_tenant(u, sales.admin_resolve('customers', p_id), d);
  end if;
  perform sales.admin_fail('invalid', '["action"]'::jsonb);
  return null;
end;
$function$;

create or replace function sales.admin_action_impl(u sales.admin_users, p_entity text, p_id text, p_action text, p_data jsonb)
returns jsonb
language plpgsql
as $function$
declare
  d        jsonb := coalesce(p_data, '{}'::jsonb);
  v_action text  := lower(btrim(coalesce(p_action, '')));
begin
  perform sales.admin_require(u, 'staff');
  if jsonb_typeof(d) <> 'object' then
    perform sales.admin_fail('invalid', '["data"]'::jsonb);
  end if;
  if v_action in ('archive', 'restore') then
    return sales.admin_archive(u, p_entity, sales.admin_resolve(p_entity, p_id), v_action = 'restore');
  end if;
  return case p_entity
    when 'orders'        then sales.admin_action_order(u, sales.admin_resolve('orders', p_id), v_action, d)
    when 'leads'         then sales.admin_action_lead(u, sales.admin_resolve('leads', p_id), v_action, d)
    when 'invoices'      then sales.admin_action_invoice(u, p_id, v_action, d)
    when 'subscriptions' then sales.admin_action_subscription(u, sales.admin_resolve('subscriptions', p_id), v_action, d)
    else sales.admin_action_misc(u, p_entity, p_id, v_action, d) end;
end;
$function$;

-- ---------------------------------------------------------------------
-- 12. 대시보드(admin_dashboard) · 내 정보(admin_me)
-- ---------------------------------------------------------------------
create or replace function sales.admin_user_json(u sales.admin_users)
returns jsonb
language sql
immutable
as $function$
  select jsonb_build_object('id', u.id, 'username', u.username, 'display_name', u.display_name,
                            'email', u.email, 'role', u.role, 'must_change_password', u.must_change_password,
                            'last_login_at', u.last_login_at);
$function$;

create or replace function sales.admin_me_impl(u sales.admin_users)
returns jsonb
language sql
stable
as $function$
  select jsonb_build_object('ok', true, 'user', sales.admin_user_json(u), 'badges', jsonb_build_object(
    'leads_new',      (select count(*) from sales.leads where archived_at is null and status in ('new', 'received')),
    'orders_pending', (select count(*) from sales.orders where archived_at is null and state in ('received', 'under_review')),
    'invoices_due',   (select count(*) from sales.invoices where archived_at is null
                        and status in ('issued', 'overdue', 'partially_paid')),
    'jobs_human',     (select count(*) from public.provisioning_jobs j
                        where (j.needs_human or j.status = 'needs_human') and j.status not in ('done', 'skipped')),
    'tasks_today',    (select count(*) from sales.tasks where done_at is null and due_at is not null
                        and (timezone('Asia/Seoul', due_at))::date <= sales.seoul_today())));
$function$;

create or replace function sales.admin_dash_kpi(p_from date, p_to date)
returns jsonb
language plpgsql
stable
as $function$
declare
  today    date := sales.seoul_today();
  v_orders bigint;
  v_leads  bigint;
begin
  select count(*) into v_orders from sales.orders o
   where o.archived_at is null and (timezone('Asia/Seoul', o.created_at))::date between p_from and p_to;
  select count(*) into v_leads from sales.leads l
   where l.archived_at is null and l.status <> 'spam'
     and (timezone('Asia/Seoul', l.created_at))::date between p_from and p_to;
  return jsonb_build_object(
    'mrr', sales.money_pair((select jsonb_object_agg(currency, amt) from (
             select s.currency,
                    sum(sales.round_money(s.list_price
                          * case when s.discount_percent > 0 and s.discount_until is not null and s.discount_until >= today
                                 then (100 - s.discount_percent) / 100 else 1 end, s.currency)) as amt
               from sales.subscriptions s where s.status = 'active' group by s.currency) x)),
    'active_subscriptions', (select count(*) from sales.subscriptions where status = 'active'),
    'orders_new', v_orders,
    'leads_new', v_leads,
    'conversion_rate', case when v_leads > 0 then round(v_orders::numeric / v_leads, 4) else null end,
    'receivable', sales.money_pair((select jsonb_object_agg(currency, amt) from (
             select i.currency,
                    sum(i.total - coalesce((select sum(case when p.kind = 'payment' then p.amount else -p.amount end)
                                              from sales.payments p where p.invoice_id = i.id), 0)) as amt
               from sales.invoices i
              where i.archived_at is null and i.status in ('issued', 'overdue', 'partially_paid')
              group by i.currency) x)),
    'paid_in_range', sales.money_pair((select jsonb_object_agg(currency, amt) from (
             select p.currency, sum(p.amount) as amt from sales.payments p
              where p.kind = 'payment' and (timezone('Asia/Seoul', p.received_at))::date between p_from and p_to
              group by p.currency) x)),
    'jobs_human', (select count(*) from public.provisioning_jobs j
                    where (j.needs_human or j.status = 'needs_human') and j.status not in ('done', 'skipped')));
end;
$function$;

-- p_to 가 든 달까지 12개월
create or replace function sales.admin_dash_series(p_to date)
returns jsonb
language sql
stable
as $function$
  with m as (
    select generate_series(date_trunc('month', p_to::timestamp) - interval '11 months',
                           date_trunc('month', p_to::timestamp), interval '1 month')::date as mo
  )
  select coalesce(jsonb_agg(jsonb_build_object(
    'month', to_char(m.mo, 'YYYY-MM'),
    'paid_KRW', (select coalesce(sum(p.amount), 0) from sales.payments p where p.kind = 'payment' and p.currency = 'KRW'
                  and date_trunc('month', timezone('Asia/Seoul', p.received_at))::date = m.mo),
    'paid_USD', (select coalesce(sum(p.amount), 0) from sales.payments p where p.kind = 'payment' and p.currency = 'USD'
                  and date_trunc('month', timezone('Asia/Seoul', p.received_at))::date = m.mo),
    'orders', (select count(*) from sales.orders o where o.archived_at is null
                and date_trunc('month', timezone('Asia/Seoul', o.created_at))::date = m.mo),
    'leads', (select count(*) from sales.leads l where l.archived_at is null and l.status <> 'spam'
               and date_trunc('month', timezone('Asia/Seoul', l.created_at))::date = m.mo),
    'active_subscriptions', (select count(*) from sales.subscriptions s
               where s.started_at is not null
                 and s.started_at <= (m.mo + interval '1 month' - interval '1 day')::date
                 and (s.status in ('active', 'paused')
                      or (s.status = 'canceled' and s.canceled_at is not null
                          and (timezone('Asia/Seoul', s.canceled_at))::date > (m.mo + interval '1 month' - interval '1 day')::date)))
  ) order by m.mo), '[]'::jsonb)
  from m;
$function$;

-- 나라·플랜·언어 분포. 리드에는 나라 칸이 없어 utm.country 가 있을 때만 센다.
create or replace function sales.admin_dash_breakdown(p_from date, p_to date)
returns jsonb
language sql
stable
as $function$
  select jsonb_build_object(
    'by_country', (
      select coalesce(jsonb_agg(jsonb_build_object('country', country, 'leads', leads, 'orders', orders)
                                order by (leads + orders) desc, country), '[]'::jsonb)
        from (select country, sum(leads) as leads, sum(orders) as orders from (
                select o.billing_country as country, 0::bigint as leads, count(*) as orders
                  from sales.orders o where o.archived_at is null
                   and (timezone('Asia/Seoul', o.created_at))::date between p_from and p_to
                 group by o.billing_country
                union all
                select upper(l.utm->>'country'), count(*), 0::bigint
                  from sales.leads l where l.archived_at is null and l.status <> 'spam' and l.utm->>'country' is not null
                   and (timezone('Asia/Seoul', l.created_at))::date between p_from and p_to
                 group by upper(l.utm->>'country')
              ) x where country is not null group by country
              order by sum(leads) + sum(orders) desc, country limit 8) y),
    'by_plan', (
      select coalesce(jsonb_agg(jsonb_build_object('plan', plan, 'active', n) order by n desc, plan), '[]'::jsonb)
        from (select s.plan, count(*) as n from sales.subscriptions s where s.status = 'active' group by s.plan) x),
    'by_lang', (
      select coalesce(jsonb_agg(jsonb_build_object('lang', lang, 'leads', leads, 'orders', orders) order by lang), '[]'::jsonb)
        from (select lang, sum(leads) as leads, sum(orders) as orders from (
                select coalesce(l.locale, 'ko') as lang, count(*) as leads, 0::bigint as orders
                  from sales.leads l where l.archived_at is null and l.status <> 'spam'
                   and (timezone('Asia/Seoul', l.created_at))::date between p_from and p_to group by 1
                union all
                select coalesce(o.locale, 'ko'), 0::bigint, count(*)
                  from sales.orders o where o.archived_at is null
                   and (timezone('Asia/Seoul', o.created_at))::date between p_from and p_to group by 1
              ) x group by lang) y));
$function$;

create or replace function sales.admin_dash_todo()
returns jsonb
language sql
stable
as $function$
  select jsonb_build_object(
    'leads', (select coalesce(jsonb_agg(to_jsonb(x) order by x.created_at desc), '[]'::jsonb) from (
                select l.id, l.ref, l.company, l.name, l.email, l.locale, l.source, l.status, l.created_at
                  from sales.leads l where l.archived_at is null and l.status in ('new', 'received')
                 order by l.created_at desc limit 10) x),
    'orders', (select coalesce(jsonb_agg(to_jsonb(x) order by x.created_at desc), '[]'::jsonb) from (
                select o.id, o.order_no, o.company, o.state, o.plan, o.currency, o.monthly_total,
                       o.billing_country, o.locale, o.created_at
                  from sales.orders o where o.archived_at is null and o.state in ('received', 'under_review')
                 order by o.created_at desc limit 10) x),
    'invoices', (select coalesce(jsonb_agg(to_jsonb(x) order by x.due_at nulls last, x.created_at), '[]'::jsonb) from (
                select i.id, i.invoice_no, c.company, c.code as customer_code, i.currency, i.total, i.due_at, i.created_at,
                       case when i.status = 'issued' and i.due_at < sales.seoul_today() then 'overdue' else i.status end as status
                  from sales.invoices i join sales.customers c on c.id = i.customer_id
                 where i.archived_at is null and i.status in ('issued', 'overdue', 'partially_paid')
                 order by i.due_at nulls last, i.created_at limit 10) x),
    'jobs', (select coalesce(jsonb_agg(to_jsonb(x) order by x.due_at nulls last, x.created_at), '[]'::jsonb) from (
                select j.id, j.order_no, j.step, j.status, j.needs_human, j.due_at, j.last_error, j.created_at,
                       t.name as tenant_name
                  from public.provisioning_jobs j left join public.tenants t on t.id = j.tenant_id
                 where (j.needs_human or j.status = 'needs_human') and j.status not in ('done', 'skipped')
                 order by j.due_at nulls last, j.created_at limit 10) x),
    'tasks', (select coalesce(jsonb_agg(to_jsonb(x) order by x.due_at), '[]'::jsonb) from (
                select tk.id, tk.kind, tk.title, tk.entity, tk.entity_id, tk.due_at, tk.assignee
                  from sales.tasks tk where tk.done_at is null and tk.due_at is not null
                   and (timezone('Asia/Seoul', tk.due_at))::date <= sales.seoul_today()
                 order by tk.due_at limit 10) x));
$function$;

create or replace function sales.admin_dash_system()
returns jsonb
language sql
stable
as $function$
  select jsonb_build_object(
    'pricing_version',   (select version from sales.pricing_versions where active limit 1),
    'policy_version',    (select version from sales.policy_versions where active limit 1),
    'usage_computed_at', (select max(computed_at) from sales.usage_monthly),
    'tenants',           (select count(*) from public.tenants where name <> '__system__'),
    'today',             sales.seoul_today());
$function$;

create or replace function sales.admin_dashboard_impl(u sales.admin_users, p_from date, p_to date)
returns jsonb
language plpgsql
as $function$
declare
  v_from date := coalesce(p_from, date_trunc('month', sales.seoul_today())::date);
  v_to   date := coalesce(p_to, sales.seoul_today());
begin
  if v_from > v_to then
    perform sales.admin_fail('invalid', '["from"]'::jsonb);
  end if;
  if v_to - v_from > 1100 then
    perform sales.admin_fail('invalid', '["to"]'::jsonb);
  end if;
  return jsonb_build_object(
    'ok', true,
    'range', jsonb_build_object('from', v_from, 'to', v_to),
    'kpi', sales.admin_dash_kpi(v_from, v_to),
    'series', jsonb_build_object('months', sales.admin_dash_series(v_to)))
    || sales.admin_dash_breakdown(v_from, v_to)
    || jsonb_build_object('todo', sales.admin_dash_todo(), 'system', sales.admin_dash_system());
end;
$function$;

-- ---------------------------------------------------------------------
-- 13. 통계(admin_stats) · 내보내기 열(admin_export) · 설정 · 관리자 · 로그인
-- ---------------------------------------------------------------------

-- 'key|한국어|English;key|...' → [{key,ko,en}]
create or replace function sales.admin_cols(p_spec text)
returns jsonb
language sql
immutable
as $function$
  select coalesce(jsonb_agg(jsonb_build_object(
           'key', btrim(split_part(x, '|', 1)), 'ko', btrim(split_part(x, '|', 2)), 'en', btrim(split_part(x, '|', 3)))
           order by ord), '[]'::jsonb)
    from unnest(string_to_array(p_spec, ';')) with ordinality as t(x, ord)
   where btrim(x) <> '';
$function$;

create or replace function sales.admin_export_cols(p_entity text)
returns jsonb
language sql
immutable
as $function$
  select sales.admin_cols(case p_entity
    when 'leads' then
      'ref|접수번호|Ref;created_at|접수일시|Received;status|상태|Status;company|회사|Company;name|이름|Name;'
      || 'email|이메일|Email;phone|전화|Phone;industry|업종|Industry;locale|언어|Language;source|출처|Source;'
      || 'campaign_name|캠페인|Campaign;assignee|담당자|Assignee;next_action_at|다음 액션|Next action;'
      || 'message|문의 내용|Message;page_url|페이지|Page;referrer|유입 경로|Referrer;utm|UTM|UTM;'
      || 'lost_reason|실패 사유|Lost reason;converted_order_id|전환 주문|Converted order;owner_note|메모|Note;'
      || 'updated_at|수정일시|Updated;id|ID|ID'
    when 'orders' then
      'order_no|주문번호|Order no;created_at|접수일시|Received;state|상태|State;company|회사|Company;'
      || 'contact|담당자|Contact;email|이메일|Email;phone|전화|Phone;billing_country|나라|Country;plan|플랜|Plan;'
      || 'method|결제수단|Method;currency|통화|Currency;monthly_net|월 공급가|Monthly net;monthly_tax|세금|Tax;'
      || 'monthly_total|월 합계|Monthly total;after_discount|할인 종료 후|After discount;tax_treatment|세금 처리|Tax treatment;'
      || 'tax_id|사업자번호|Tax ID;voice_minutes|예상 통화(분)|Est. voice min;alimtalk|예상 알림톡|Est. messages;'
      || 'locale|언어|Language;customer_code|고객 코드|Customer;assignee|담당자|Assignee;'
      || 'next_action_at|다음 액션|Next action;owner_note|메모|Note;pricing_version|요금표 판|Pricing version;'
      || 'updated_at|수정일시|Updated;id|ID|ID'
    when 'customers' then
      'code|고객 코드|Code;company|회사|Company;contact_name|담당자|Contact;email|이메일|Email;phone|전화|Phone;'
      || 'country|나라|Country;currency|통화|Currency;buyer_type|구매자 유형|Buyer type;tax_id|사업자번호|Tax ID;'
      || 'tax_treatment|세금 처리|Tax treatment;status|상태|Status;subscription_plan|구독 플랜|Plan;'
      || 'subscription_status|구독 상태|Subscription;tenant_name|테넌트|Tenant;open_invoices|미결 인보이스|Open invoices;'
      || 'receivable|미수금|Receivable;lang|언어|Language;source|출처|Source;tags|태그|Tags;owner_note|메모|Note;'
      || 'created_at|등록일시|Created;updated_at|수정일시|Updated;id|ID|ID'
    when 'subscriptions' then
      'company|회사|Company;customer_code|고객 코드|Customer;plan|플랜|Plan;currency|통화|Currency;'
      || 'list_price|정가|List price;discount_percent|할인 %|Discount %;discount_until|할인 종료|Discount until;'
      || 'status|상태|Status;started_at|시작일|Started;current_period_start|기간 시작|Period start;'
      || 'current_period_end|기간 끝|Period end;cancel_at|해지 예정|Cancel at;canceled_at|해지일시|Canceled;'
      || 'tenant_name|테넌트|Tenant;note|메모|Note;created_at|등록일시|Created;id|ID|ID'
    when 'invoices' then
      'invoice_no|인보이스 번호|Invoice no;company|회사|Company;customer_code|고객 코드|Customer;status|상태|Status;'
      || 'currency|통화|Currency;period_start|기간 시작|Period start;period_end|기간 끝|Period end;net|공급가|Net;'
      || 'tax_rate|세율|Tax rate;tax|세금|Tax;total|합계|Total;paid_amount|입금|Paid;issued_at|발행일시|Issued;'
      || 'due_at|기한|Due;paid_at|완납일시|Paid at;method|결제수단|Method;provider|결제사|Provider;'
      || 'provider_ref|결제 참조|Provider ref;tax_document|세금계산서|Tax document;note|메모|Note;'
      || 'created_at|등록일시|Created;id|ID|ID'
    when 'payments' then
      'received_at|입금일시|Received;kind|종류|Kind;amount|금액|Amount;currency|통화|Currency;method|결제수단|Method;'
      || 'provider|결제사|Provider;provider_ref|결제 참조|Provider ref;invoice_no|인보이스 번호|Invoice no;'
      || 'company|회사|Company;note|메모|Note;created_at|기록일시|Recorded;id|ID|ID'
    when 'campaigns' then
      'name|이름|Name;channel|채널|Channel;status|상태|Status;utm_source|utm_source|utm_source;'
      || 'utm_medium|utm_medium|utm_medium;utm_campaign|utm_campaign|utm_campaign;country|나라|Country;lang|언어|Language;'
      || 'budget|예산|Budget;currency|통화|Currency;starts_on|시작|Starts;ends_on|종료|Ends;leads|리드|Leads;'
      || 'orders|주문|Orders;landing_url|랜딩 URL|Landing URL;note|메모|Note;created_at|등록일시|Created;id|ID|ID'
    when 'tasks' then
      'kind|종류|Kind;title|제목|Title;entity|대상|Entity;entity_id|대상 ID|Entity ID;due_at|기한|Due;'
      || 'done_at|완료|Done;assignee|담당자|Assignee;note|메모|Note;created_by|만든 사람|Created by;'
      || 'created_at|등록일시|Created;id|ID|ID'
    when 'notes' then
      'created_at|작성일시|Created;entity|대상|Entity;entity_id|대상 ID|Entity ID;author|작성자|Author;body|내용|Body;id|ID|ID'
    when 'tenants' then
      'name|테넌트|Tenant;plan_type|운영 플랜|Plan type;industry|업종|Industry;phone_number|대표번호|Phone;'
      || 'ai_phone|AI 회선|AI line;company|고객사|Customer;customer_code|고객 코드|Customer code;'
      || 'calls_this_month|이달 통화|Calls this month;conversations_this_month|이달 대화|Conversations this month;'
      || 'created_at|등록일시|Created;id|ID|ID'
    when 'usage' then
      'month|월|Month;tenant_name|테넌트|Tenant;company|고객사|Customer;plan|플랜|Plan;calls|통화 수|Calls;'
      || 'call_seconds|통화 초|Call seconds;voice_minutes|통화 분|Voice minutes;conversations|대화 수|Conversations;'
      || 'conversation_limit|한도|Limit;limit_pct|한도 대비 %|% of limit;chats_web|웹 채팅|Web chats;'
      || 'chats_kakao|카카오|Kakao;chats_phone|전화 대화|Phone;alimtalk|알림톡|Messages;computed_at|집계 시각|Computed;'
      || 'tenant_id|테넌트 ID|Tenant ID'
    when 'numbers' then
      'e164|번호|Number;country|나라|Country;provider|사업자|Provider;owner|소유|Owner;status|상태|Status;'
      || 'tenant_name|테넌트|Tenant;order_no|주문번호|Order no;reserved_at|예약|Reserved;assigned_at|배정|Assigned;'
      || 'note|메모|Note;created_at|등록일시|Created;id|ID|ID'
    when 'jobs' then
      'order_no|주문번호|Order no;tenant_name|테넌트|Tenant;step|단계|Step;status|상태|Status;'
      || 'needs_human|사람 필요|Needs human;attempts|시도|Attempts;last_error|마지막 오류|Last error;due_at|기한|Due;'
      || 'started_at|시작|Started;finished_at|끝|Finished;created_at|등록일시|Created;id|ID|ID'
    when 'audit' then
      'at|시각|At;username|사용자|User;action|동작|Action;entity|대상|Entity;entity_id|대상 ID|Entity ID;'
      || 'ip_hash|IP 해시|IP hash;id|ID|ID'
    when 'users' then
      'username|아이디|Username;display_name|이름|Name;email|이메일|Email;role|역할|Role;status|상태|Status;'
      || 'must_change_password|비밀번호 변경 필요|Must change password;last_login_at|마지막 로그인|Last login;'
      || 'created_at|등록일시|Created;id|ID|ID'
    else '' end);
$function$;

create or replace function sales.admin_export_impl(u sales.admin_users, p_entity text, p_filter jsonb)
returns jsonb
language plpgsql
as $function$
declare
  r jsonb;
begin
  r := sales.admin_list_impl(u, p_entity, coalesce(p_filter, '{}'::jsonb) - 'sort', p_filter->>'sort', 1, 5000, 5000);
  return jsonb_build_object('ok', true, 'entity', p_entity, 'columns', sales.admin_export_cols(p_entity),
                            'rows', r->'rows', 'total', r->'total');
end;
$function$;

-- --- 통계 보고서 -------------------------------------------------------
create or replace function sales.stats_revenue(p_from date, p_to date)
returns jsonb
language sql
stable
as $function$
  with m as (
    select generate_series(date_trunc('month', p_from::timestamp), date_trunc('month', p_to::timestamp),
                           interval '1 month')::date as mo
  ), cur as (select unnest(array['KRW', 'USD']) as c)
  select coalesce(jsonb_agg(jsonb_build_object(
           'month', to_char(m.mo, 'YYYY-MM'), 'currency', cur.c,
           'invoices', iv.n, 'net', iv.net, 'tax', iv.tax, 'total', iv.total,
           'paid', pm.paid, 'refunded', pm.refunded) order by m.mo, cur.c), '[]'::jsonb)
    from m cross join cur
    cross join lateral (
      select count(*) as n, coalesce(sum(i.net), 0) as net, coalesce(sum(i.tax), 0) as tax, coalesce(sum(i.total), 0) as total
        from sales.invoices i
       where i.currency = cur.c and i.status not in ('draft', 'void') and i.archived_at is null
         and date_trunc('month', timezone('Asia/Seoul', i.issued_at))::date = m.mo) iv
    cross join lateral (
      select coalesce(sum(p.amount) filter (where p.kind = 'payment'), 0) as paid,
             coalesce(sum(p.amount) filter (where p.kind = 'refund'), 0) as refunded
        from sales.payments p
       where p.currency = cur.c and date_trunc('month', timezone('Asia/Seoul', p.received_at))::date = m.mo) pm;
$function$;

create or replace function sales.stats_pipeline(p_from date, p_to date)
returns jsonb
language plpgsql
stable
as $function$
declare
  v_leads  bigint;
  v_orders bigint;
  v_signed bigint;
  v_active bigint;
  d1       numeric;
  d2       numeric;
begin
  select count(*) into v_leads from sales.leads l
   where l.archived_at is null and l.status <> 'spam'
     and (timezone('Asia/Seoul', l.created_at))::date between p_from and p_to;
  select count(*), count(*) filter (where o.state in ('contract_signed', 'payment_pending', 'paid', 'active')),
         count(*) filter (where o.state = 'active')
    into v_orders, v_signed, v_active
    from sales.orders o
   where o.archived_at is null and (timezone('Asia/Seoul', o.created_at))::date between p_from and p_to;
  select avg(extract(epoch from (e.ts - o.created_at)) / 86400) into d1
    from sales.orders o
    join lateral (select min(e.created_at) as ts from sales.order_events e
                   where e.order_id = o.id and e.to_state = 'contract_signed') e on true
   where o.archived_at is null and (timezone('Asia/Seoul', o.created_at))::date between p_from and p_to
     and e.ts is not null;
  select avg(extract(epoch from (a.ts - s.ts)) / 86400) into d2
    from sales.orders o
    join lateral (select min(e.created_at) as ts from sales.order_events e
                   where e.order_id = o.id and e.to_state = 'contract_signed') s on true
    join lateral (select min(e.created_at) as ts from sales.order_events e
                   where e.order_id = o.id and e.to_state = 'active') a on true
   where o.archived_at is null and (timezone('Asia/Seoul', o.created_at))::date between p_from and p_to
     and s.ts is not null and a.ts is not null;
  return jsonb_build_array(
    jsonb_build_object('stage', 'leads', 'ko', '문의', 'en', 'Leads', 'count', v_leads, 'pct', null, 'avg_days_to_next', null),
    jsonb_build_object('stage', 'orders', 'ko', '주문', 'en', 'Orders', 'count', v_orders,
                       'pct', case when v_leads > 0 then round(100.0 * v_orders / v_leads, 1) end,
                       'avg_days_to_next', round(d1, 1)),
    jsonb_build_object('stage', 'contract_signed', 'ko', '계약 완료', 'en', 'Contract signed', 'count', v_signed,
                       'pct', case when v_orders > 0 then round(100.0 * v_signed / v_orders, 1) end,
                       'avg_days_to_next', round(d2, 1)),
    jsonb_build_object('stage', 'active', 'ko', '개통', 'en', 'Active', 'count', v_active,
                       'pct', case when v_signed > 0 then round(100.0 * v_active / v_signed, 1) end,
                       'avg_days_to_next', null));
end;
$function$;

create or replace function sales.stats_marketing(p_from date, p_to date)
returns jsonb
language sql
stable
as $function$
  with l as (
    select * from sales.leads
     where archived_at is null and status <> 'spam'
       and (timezone('Asia/Seoul', created_at))::date between p_from and p_to
  ), dims as (
    select 'source' as dimension, coalesce(l.source, '-') as value, count(*) as leads,
           count(*) filter (where l.converted_order_id is not null) as orders from l group by 2
    union all
    select 'utm_source', coalesce(l.utm->>'utm_source', l.utm->>'source', '-'), count(*),
           count(*) filter (where l.converted_order_id is not null) from l group by 2
    union all
    select 'utm_medium', coalesce(l.utm->>'utm_medium', l.utm->>'medium', '-'), count(*),
           count(*) filter (where l.converted_order_id is not null) from l group by 2
    union all
    select 'utm_campaign', coalesce(l.utm->>'utm_campaign', l.utm->>'campaign', '-'), count(*),
           count(*) filter (where l.converted_order_id is not null) from l group by 2
    union all
    select 'page_url', coalesce(l.page_url, '-'), count(*),
           count(*) filter (where l.converted_order_id is not null) from l group by 2
    union all
    select 'campaign', cp.name, count(*), count(*) filter (where l.converted_order_id is not null)
      from l join sales.campaigns cp on cp.id = l.campaign_id group by cp.name
    union all
    select 'lang', x.lang, sum(x.leads), sum(x.orders) from (
      select coalesce(l.locale, 'ko') as lang, count(*) as leads, 0::bigint as orders from l group by 1
      union all
      select coalesce(o.locale, 'ko'), 0::bigint, count(*) from sales.orders o
       where o.archived_at is null and (timezone('Asia/Seoul', o.created_at))::date between p_from and p_to group by 1
    ) x group by x.lang
  )
  select coalesce(jsonb_agg(jsonb_build_object('dimension', dimension, 'value', value, 'leads', leads, 'orders', orders)
                            order by dimension, leads desc, value), '[]'::jsonb)
    from dims;
$function$;

create or replace function sales.stats_cohort(p_from date, p_to date)
returns jsonb
language sql
stable
as $function$
  select coalesce(jsonb_agg(jsonb_build_object('cohort', c, 'customers', n, 'active', a, 'discounted', d, 'canceled', x,
                            'retention_pct', case when n > 0 then round(100.0 * a / n, 1) end) order by c), '[]'::jsonb)
    from (select to_char(s.started_at, 'YYYY-MM') as c,
                 count(distinct s.customer_id) as n,
                 count(distinct s.customer_id) filter (where s.status in ('active', 'paused')) as a,
                 count(distinct s.customer_id) filter (where s.discount_percent > 0) as d,
                 count(distinct s.customer_id) filter (where s.status = 'canceled') as x
            from sales.subscriptions s
           where s.started_at is not null and s.started_at between p_from and p_to
           group by 1) y;
$function$;

create or replace function sales.stats_countries(p_from date, p_to date)
returns jsonb
language sql
stable
as $function$
  select coalesce(jsonb_agg(jsonb_build_object(
           'code', c->>'code', 'name_ko', c->'name'->>'ko', 'name_en', c->'name'->>'en',
           'currency', c->>'currency', 'voice', c->>'voice',
           'tax_id_required', coalesce((c->>'taxIdRequired')::boolean, false),
           'leads', (select count(*) from sales.leads l where l.archived_at is null and l.status <> 'spam'
                      and upper(l.utm->>'country') = c->>'code'
                      and (timezone('Asia/Seoul', l.created_at))::date between p_from and p_to),
           'orders', (select count(*) from sales.orders o where o.archived_at is null and o.billing_country = c->>'code'
                       and (timezone('Asia/Seoul', o.created_at))::date between p_from and p_to),
           'active_subscriptions', (select count(*) from sales.subscriptions s join sales.customers cu on cu.id = s.customer_id
                                     where s.status = 'active' and cu.country = c->>'code')
         ) order by ord), '[]'::jsonb)
    from jsonb_array_elements(coalesce(sales.pricing_active()->'countries', '[]'::jsonb)) with ordinality as t(c, ord);
$function$;

create or replace function sales.admin_stats_impl(u sales.admin_users, p_report text, p_params jsonb)
returns jsonb
language plpgsql
as $function$
declare
  p      jsonb := coalesce(p_params, '{}'::jsonb);
  v_from date;
  v_to   date;
  v_rows jsonb;
  v_cols jsonb;
begin
  if jsonb_typeof(p) <> 'object' then
    perform sales.admin_fail('invalid', '["params"]'::jsonb);
  end if;
  perform sales.chk(p, 'from', 'date');
  perform sales.chk(p, 'to', 'date');
  v_from := coalesce((p->>'from')::date, (date_trunc('month', sales.seoul_today()) - interval '11 months')::date);
  v_to   := coalesce((p->>'to')::date, sales.seoul_today());
  if v_from > v_to or v_to - v_from > 1100 then
    perform sales.admin_fail('invalid', '["from","to"]'::jsonb);
  end if;
  case p_report
    when 'revenue' then
      v_rows := sales.stats_revenue(v_from, v_to);
      v_cols := sales.admin_cols('month|월|Month;currency|통화|Currency;invoices|인보이스 수|Invoices;net|공급가|Net;'
                || 'tax|세금|Tax;total|합계|Total;paid|입금|Paid;refunded|환불|Refunded');
    when 'pipeline' then
      v_rows := sales.stats_pipeline(v_from, v_to);
      v_cols := sales.admin_cols('stage|단계|Stage;ko|이름|Name (ko);en|이름(영문)|Name (en);count|건수|Count;'
                || 'pct|전 단계 대비 %|% of previous;avg_days_to_next|다음 단계까지 평균 일수|Avg days to next');
    when 'marketing' then
      v_rows := sales.stats_marketing(v_from, v_to);
      v_cols := sales.admin_cols('dimension|구분|Dimension;value|값|Value;leads|리드|Leads;orders|주문|Orders');
    when 'usage' then
      v_rows := sales.admin_list_impl(u, 'usage',
                  jsonb_build_object('from', date_trunc('month', v_from)::date, 'to', v_to),
                  'month:desc', 1, 5000, 5000)->'rows';
      v_cols := sales.admin_export_cols('usage');
    when 'cohort' then
      v_rows := sales.stats_cohort(v_from, v_to);
      v_cols := sales.admin_cols('cohort|시작 월|Cohort;customers|고객 수|Customers;active|유지 중|Active;'
                || 'discounted|할인 적용|Discounted;canceled|해지|Canceled;retention_pct|유지율 %|Retention %');
    when 'countries' then
      v_rows := sales.stats_countries(v_from, v_to);
      v_cols := sales.admin_cols('code|코드|Code;name_ko|나라|Country (ko);name_en|나라(영문)|Country (en);'
                || 'currency|통화|Currency;voice|AI 전화|Voice;tax_id_required|세금번호 필수|Tax ID required;'
                || 'leads|리드|Leads;orders|주문|Orders;active_subscriptions|활성 구독|Active subscriptions');
    else
      perform sales.admin_fail('invalid', '["report"]'::jsonb);
  end case;
  return jsonb_build_object('ok', true, 'report', p_report,
                            'range', jsonb_build_object('from', v_from, 'to', v_to),
                            'columns', v_cols, 'rows', v_rows);
end;
$function$;

-- --- 설정 --------------------------------------------------------------
create or replace function sales.admin_settings_get_impl(u sales.admin_users)
returns jsonb
language sql
stable
as $function$
  select jsonb_build_object('ok', true, 'settings',
           coalesce((select jsonb_object_agg(key, value) from sales.settings), '{}'::jsonb));
$function$;

create or replace function sales.admin_settings_set_impl(u sales.admin_users, p_key text, p_value jsonb)
returns jsonb
language plpgsql
as $function$
declare
  v_before jsonb;
begin
  perform sales.admin_require(u, 'owner');
  if p_key is null or p_key !~ '^[a-z][a-z0-9_]{0,39}$' then
    perform sales.admin_fail('invalid', '["key"]'::jsonb);
  end if;
  if p_value is null or length(p_value::text) > 20000 then
    perform sales.admin_fail('invalid', '["value"]'::jsonb);
  end if;
  select value into v_before from sales.settings where key = p_key;
  insert into sales.settings (key, value, updated_by) values (p_key, p_value, u.username)
  on conflict (key) do update set value = excluded.value, updated_at = now(), updated_by = excluded.updated_by;
  perform sales.admin_audit(u, 'settings.set', 'setting', p_key, v_before, p_value);
  return jsonb_build_object('ok', true, 'key', p_key, 'value', p_value);
end;
$function$;

-- --- 관리자 계정 (owner 만) ----------------------------------------------
create or replace function sales.admin_users_list_impl(u sales.admin_users)
returns jsonb
language plpgsql
as $function$
begin
  perform sales.admin_require(u, 'owner');
  return jsonb_build_object('ok', true, 'rows',
    (select coalesce(jsonb_agg((to_jsonb(x) - 'password_hash') order by x.created_at), '[]'::jsonb) from sales.admin_users x));
end;
$function$;

create or replace function sales.admin_users_save_impl(u sales.admin_users, p_id uuid, d jsonb)
returns jsonb
language plpgsql
as $function$
declare
  v_t      sales.admin_users%rowtype;
  v_before jsonb;
  v_after  jsonb;
  v_user   text;
  v_pw     text;
begin
  perform sales.admin_require(u, 'owner');
  perform sales.chk_keys(d, array['username', 'display_name', 'email', 'role', 'status', 'temp_password']);
  perform sales.chk(d, 'username', 'text', '40');
  perform sales.chk(d, 'display_name', 'text', '80');
  perform sales.chk(d, 'email', 'email');
  perform sales.chk(d, 'role', 'enum', 'owner,staff,viewer');
  perform sales.chk(d, 'status', 'enum', 'active,disabled');
  perform sales.chk(d, 'temp_password', 'text', '200');
  v_pw := nullif(d->>'temp_password', '');
  if v_pw is not null and length(v_pw) < 6 then
    perform sales.admin_fail('invalid', '["temp_password"]'::jsonb);
  end if;
  if p_id is null then
    v_user := lower(btrim(coalesce(d->>'username', '')));
    if v_user !~ '^[a-z0-9][a-z0-9._-]{2,39}$' then
      perform sales.admin_fail('invalid', '["username"]'::jsonb);
    end if;
    if v_pw is null then
      perform sales.admin_fail('invalid', '["temp_password"]'::jsonb);
    end if;
    if exists (select 1 from sales.admin_users where lower(username) = v_user) then
      perform sales.admin_fail('conflict', '["username"]'::jsonb);
    end if;
    insert into sales.admin_users (username, display_name, email, password_hash, role, status, must_change_password)
    values (v_user, coalesce(nullif(btrim(d->>'display_name'), ''), v_user), nullif(btrim(d->>'email'), ''),
            extensions.crypt(v_pw, extensions.gen_salt('bf', 10)),
            coalesce(d->>'role', 'viewer'), coalesce(d->>'status', 'active'), true)
    returning * into v_t;
    v_after := to_jsonb(v_t) - 'password_hash';
    perform sales.admin_audit(u, 'users.create', 'user', v_t.id::text, null, v_after);
    return jsonb_build_object('ok', true, 'item', v_after);
  end if;

  select * into v_t from sales.admin_users where id = p_id for update;
  if not found then
    perform sales.admin_fail('not_found');
  end if;
  v_before := to_jsonb(v_t) - 'password_hash';
  if d ? 'username' and lower(btrim(d->>'username')) <> lower(v_t.username) then
    perform sales.admin_fail('invalid', '["username"]'::jsonb);         -- 아이디는 바꾸지 않는다
  end if;
  if v_t.id = u.id and ((d ? 'role' and d->>'role' <> u.role) or (d ? 'status' and d->>'status' <> 'active')) then
    perform sales.admin_fail('invalid', '["role","status"]'::jsonb);     -- 자기 권한은 스스로 못 내린다
  end if;
  if v_t.role = 'owner' and v_t.status = 'active'
     and ((d ? 'role' and d->>'role' <> 'owner') or (d ? 'status' and d->>'status' = 'disabled'))
     and (select count(*) from sales.admin_users where role = 'owner' and status = 'active') <= 1 then
    perform sales.admin_fail('conflict', '["role"]'::jsonb);            -- 마지막 owner
  end if;
  update sales.admin_users
     set display_name = coalesce(nullif(btrim(d->>'display_name'), ''), display_name),
         email        = case when d ? 'email' then nullif(btrim(d->>'email'), '') else email end,
         role         = coalesce(d->>'role', role),
         status       = coalesce(d->>'status', status),
         password_hash = case when v_pw is not null then extensions.crypt(v_pw, extensions.gen_salt('bf', 10)) else password_hash end,
         must_change_password = case when v_pw is not null then true else must_change_password end
   where id = p_id
   returning * into v_t;
  if v_pw is not null or v_t.status = 'disabled' then
    update sales.admin_sessions set revoked_at = now() where user_id = p_id and revoked_at is null;
  end if;
  v_after := to_jsonb(v_t) - 'password_hash';
  perform sales.admin_audit(u, 'users.update', 'user', p_id::text, v_before,
                            v_after || jsonb_build_object('password_reset', v_pw is not null));
  return jsonb_build_object('ok', true, 'item', v_after);
end;
$function$;

create or replace function sales.admin_change_password_impl(u sales.admin_users, p_token text, p_current text, p_new text)
returns jsonb
language plpgsql
as $function$
begin
  if p_new is null or length(p_new) < 10 or length(p_new) > 200 then
    perform sales.admin_fail('invalid', '["new"]'::jsonb);
  end if;
  if p_current is null or u.password_hash <> extensions.crypt(p_current, u.password_hash) then
    perform sales.admin_fail('invalid', '["current"]'::jsonb);
  end if;
  if p_new = p_current then
    perform sales.admin_fail('invalid', '["new"]'::jsonb);
  end if;
  update sales.admin_users
     set password_hash = extensions.crypt(p_new, extensions.gen_salt('bf', 10)),
         must_change_password = false
   where id = u.id;
  -- 다른 세션은 전부 끊는다 (지금 세션만 남긴다)
  update sales.admin_sessions
     set revoked_at = now()
   where user_id = u.id and revoked_at is null
     and token_hash <> encode(extensions.digest(p_token, 'sha256'), 'hex');
  perform sales.admin_audit(u, 'users.change_password', 'user', u.id::text, null, jsonb_build_object('self', true));
  return jsonb_build_object('ok', true);
end;
$function$;

-- --- 로그인 · 로그아웃 (raise 하지 않는다: 유량제한 기록이 남아야 한다) --------
create or replace function sales.admin_login_impl(p_username text, p_password text, p_ip_hash text, p_user_agent text)
returns jsonb
language plpgsql
as $function$
declare
  v_user  text := lower(btrim(coalesce(p_username, '')));
  v_u     sales.admin_users%rowtype;
  v_ok    boolean := false;
  v_token text;
begin
  if v_user = '' or length(v_user) > 60 or p_password is null or p_password = '' or length(p_password) > 200 then
    return sales.admin_err('invalid', '["username","password"]'::jsonb);
  end if;
  if not sales.global_ok('admin_login', 60) then
    return sales.admin_err('rate_limited');
  end if;
  if not sales.rate_ok('admin_login:u:' || v_user, 5, interval '15 minutes') then
    return sales.admin_err('rate_limited');
  end if;
  if not sales.rate_ok('admin_login:ip:' || coalesce(nullif(p_ip_hash, ''), '-'), 20, interval '15 minutes') then
    return sales.admin_err('rate_limited');
  end if;
  select * into v_u from sales.admin_users where lower(username) = v_user;
  if found then
    v_ok := (v_u.password_hash = extensions.crypt(p_password, v_u.password_hash));
  else
    -- 없는 아이디도 같은 시간이 걸리게 한다
    perform extensions.crypt(p_password, extensions.gen_salt('bf', 10));
  end if;
  if not v_ok then
    if v_u.id is not null then
      update sales.admin_users set failed_logins = failed_logins + 1 where id = v_u.id;
    end if;
    return sales.admin_err('unauthorized');
  end if;
  if v_u.status <> 'active' then
    return sales.admin_err('unauthorized');
  end if;
  v_token := encode(extensions.gen_random_bytes(32), 'hex');
  insert into sales.admin_sessions (user_id, token_hash, expires_at, ip_hash, user_agent)
  values (v_u.id, encode(extensions.digest(v_token, 'sha256'), 'hex'), now() + interval '7 days',
          left(nullif(p_ip_hash, ''), 80), left(nullif(p_user_agent, ''), 400));
  update sales.admin_users set last_login_at = now(), failed_logins = 0 where id = v_u.id;
  perform sales.admin_audit(v_u, 'login', 'user', v_u.id::text, null,
                            jsonb_build_object('user_agent', left(p_user_agent, 200)), p_ip_hash);
  return jsonb_build_object('ok', true, 'token', v_token, 'user', sales.admin_user_json(v_u));
end;
$function$;

create or replace function sales.admin_logout_impl(p_token text)
returns jsonb
language plpgsql
as $function$
declare
  v_uid uuid;
  v_u   sales.admin_users%rowtype;
begin
  if p_token is null or p_token !~ '^[0-9a-f]{64}$' then
    return jsonb_build_object('ok', true);
  end if;
  update sales.admin_sessions s
     set revoked_at = now()
   where s.token_hash = encode(extensions.digest(p_token, 'sha256'), 'hex') and s.revoked_at is null
   returning s.user_id into v_uid;
  if v_uid is not null then
    select * into v_u from sales.admin_users where id = v_uid;
    perform sales.admin_audit(v_u, 'logout', 'user', v_uid::text, null, null);
  end if;
  return jsonb_build_object('ok', true);
end;
$function$;

-- ---------------------------------------------------------------------
-- 14. 공개 함수 public.admin_* (§2.4). PostgREST rpc 로 publishable 키가 부른다.
--     전부 SECURITY DEFINER, search_path = sales, public, returns jsonb.
--     예상된 실패는 sales.admin_catch 가 오류 객체로 바꾸고, 그 밖의 오류는
--     db_error 로만 알린다 (SQLERRM 은 절대 밖으로 나가지 않는다).
-- ---------------------------------------------------------------------
create or replace function public.admin_health()
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return jsonb_build_object(
    'ok', true, 'db', true,
    'pricingVersion', (select version from sales.pricing_versions where active limit 1),
    'policyVersion',  (select version from sales.policy_versions where active limit 1),
    'adminUsers',     (select count(*) from sales.admin_users where status = 'active'));
exception when others then
  return jsonb_build_object('ok', false, 'db', false, 'error', 'db_error');
end;
$function$;

create or replace function public.admin_login(p_username text, p_password text, p_ip_hash text default null, p_user_agent text default null)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_login_impl(p_username, p_password, p_ip_hash, p_user_agent);
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

create or replace function public.admin_logout(p_token text)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_logout_impl(p_token);
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

create or replace function public.admin_me(p_token text)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_me_impl(sales.admin_auth(p_token));
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

create or replace function public.admin_change_password(p_token text, p_current text, p_new text)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_change_password_impl(sales.admin_auth(p_token), p_token, p_current, p_new);
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

create or replace function public.admin_users_list(p_token text)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_users_list_impl(sales.admin_auth(p_token));
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

create or replace function public.admin_users_save(p_token text, p_id uuid default null, p_data jsonb default '{}'::jsonb)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_users_save_impl(sales.admin_auth(p_token), p_id, coalesce(p_data, '{}'::jsonb));
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

create or replace function public.admin_dashboard(p_token text, p_from date default null, p_to date default null)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_dashboard_impl(sales.admin_auth(p_token), p_from, p_to);
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

create or replace function public.admin_list(p_token text, p_entity text, p_filter jsonb default '{}'::jsonb,
                                             p_sort text default null, p_page int default 1, p_size int default 50)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_list_impl(sales.admin_auth(p_token), p_entity, p_filter, p_sort, p_page, p_size, 200);
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

create or replace function public.admin_get(p_token text, p_entity text, p_id text)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_get_impl(sales.admin_auth(p_token), p_entity, p_id);
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

create or replace function public.admin_save(p_token text, p_entity text, p_id text default null, p_data jsonb default '{}'::jsonb)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_save_impl(sales.admin_auth(p_token), p_entity, p_id, p_data);
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

create or replace function public.admin_action(p_token text, p_entity text, p_id text, p_action text, p_data jsonb default '{}'::jsonb)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_action_impl(sales.admin_auth(p_token), p_entity, p_id, p_action, p_data);
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

create or replace function public.admin_stats(p_token text, p_report text, p_params jsonb default '{}'::jsonb)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_stats_impl(sales.admin_auth(p_token), p_report, p_params);
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

create or replace function public.admin_export(p_token text, p_entity text, p_filter jsonb default '{}'::jsonb)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_export_impl(sales.admin_auth(p_token), p_entity, p_filter);
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

create or replace function public.admin_settings_get(p_token text)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_settings_get_impl(sales.admin_auth(p_token));
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

create or replace function public.admin_settings_set(p_token text, p_key text, p_value jsonb)
returns jsonb
language plpgsql
security definer
set search_path = sales, public
as $function$
begin
  return sales.admin_settings_set_impl(sales.admin_auth(p_token), p_key, p_value);
exception when others then
  return sales.admin_catch(sqlstate, sqlerrm);
end;
$function$;

-- ---------------------------------------------------------------------
-- 15. 권한: 기존 public.sales_* 와 같은 모양.
--     public 에서 거두고 anon, authenticated, service_role 에만 execute.
--     sales.* 내부 함수는 스키마 usage 가 없어 anon/authenticated 가 부를 수 없다.
-- ---------------------------------------------------------------------
revoke all on function public.admin_health() from public;
revoke all on function public.admin_login(text, text, text, text) from public;
revoke all on function public.admin_logout(text) from public;
revoke all on function public.admin_me(text) from public;
revoke all on function public.admin_change_password(text, text, text) from public;
revoke all on function public.admin_users_list(text) from public;
revoke all on function public.admin_users_save(text, uuid, jsonb) from public;
revoke all on function public.admin_dashboard(text, date, date) from public;
revoke all on function public.admin_list(text, text, jsonb, text, int, int) from public;
revoke all on function public.admin_get(text, text, text) from public;
revoke all on function public.admin_save(text, text, text, jsonb) from public;
revoke all on function public.admin_action(text, text, text, text, jsonb) from public;
revoke all on function public.admin_stats(text, text, jsonb) from public;
revoke all on function public.admin_export(text, text, jsonb) from public;
revoke all on function public.admin_settings_get(text) from public;
revoke all on function public.admin_settings_set(text, text, jsonb) from public;

grant execute on function public.admin_health() to anon, authenticated, service_role;
grant execute on function public.admin_login(text, text, text, text) to anon, authenticated, service_role;
grant execute on function public.admin_logout(text) to anon, authenticated, service_role;
grant execute on function public.admin_me(text) to anon, authenticated, service_role;
grant execute on function public.admin_change_password(text, text, text) to anon, authenticated, service_role;
grant execute on function public.admin_users_list(text) to anon, authenticated, service_role;
grant execute on function public.admin_users_save(text, uuid, jsonb) to anon, authenticated, service_role;
grant execute on function public.admin_dashboard(text, date, date) to anon, authenticated, service_role;
grant execute on function public.admin_list(text, text, jsonb, text, int, int) to anon, authenticated, service_role;
grant execute on function public.admin_get(text, text, text) to anon, authenticated, service_role;
grant execute on function public.admin_save(text, text, text, jsonb) to anon, authenticated, service_role;
grant execute on function public.admin_action(text, text, text, text, jsonb) to anon, authenticated, service_role;
grant execute on function public.admin_stats(text, text, jsonb) to anon, authenticated, service_role;
grant execute on function public.admin_export(text, text, jsonb) to anon, authenticated, service_role;
grant execute on function public.admin_settings_get(text) to anon, authenticated, service_role;
grant execute on function public.admin_settings_set(text, text, jsonb) to anon, authenticated, service_role;

-- 끝.
