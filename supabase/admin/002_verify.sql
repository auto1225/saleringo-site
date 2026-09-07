-- =====================================================================
-- Saleringo 판매 관리자 — 001_admin.sql 적용 뒤 검증 (2026-09-07)
--
-- 순서대로 실행한다.
--   1. 객체·권한·시드 확인 (읽기만)
--   2. admin_health (읽기만)
--   3. admin_login 이 ok 를 돌려주는지 (세션 1개, admin 유량제한 5회/15분 중 1회)
--   4. 시나리오 DO 블록 — TEST 행을 만든다. 회사명 'ZZ-TEST-DELETE', 관리자 'zz_test_viewer',
--      설정 키 'zz_test'. 어느 assert 라도 실패하면 블록 전체가 되돌아가 아무것도 남지 않는다.
--      (admin 로그인 1회 더 — 3 과 합쳐 15분 안에 2회)
--   5. usage_monthly 와 운영 표 직접 집계 대조 (읽기만; 4 가 이달을 새로 고쳤다)
--   6. (선택) TEST 행 정리 — 주석을 풀어 실행
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. 만들어진 객체
-- ---------------------------------------------------------------------
select 'table' as kind, c.relname as name, c.relrowsecurity as rls
  from pg_class c
 where c.relnamespace = 'sales'::regnamespace and c.relkind = 'r'
   and c.relname in ('admin_users', 'admin_sessions', 'admin_audit', 'customers', 'subscriptions', 'invoices',
                     'payments', 'usage_monthly', 'campaigns', 'tasks', 'notes', 'settings')
union all
select 'sequence', s.relname, null from pg_class s
 where s.relnamespace = 'sales'::regnamespace and s.relkind = 'S' and s.relname in ('customer_seq', 'invoice_seq')
union all
select 'public fn', p.proname || '(' || pg_get_function_identity_arguments(p.oid) || ')', p.prosecdef
  from pg_proc p where p.pronamespace = 'public'::regnamespace and p.proname like 'admin\_%'
union all
select 'sales fn', p.proname || '(' || pg_get_function_identity_arguments(p.oid) || ')', null
  from pg_proc p where p.pronamespace = 'sales'::regnamespace
   and (p.proname like 'admin\_%' or p.proname like 'stats\_%' or p.proname like 'lf\_%'
        or p.proname in ('touch_updated_at', 'chk', 'chk_keys', 'is_uuid', 'to_uuid', 'is_num', 'is_date', 'is_ts',
                         'seoul_today', 'sdate', 'inv_status_expr', 'pricing_active', 'pricing_plan', 'plan_ids',
                         'next_customer_code', 'next_invoice_no', 'invoice_totals', 'invoice_recalc', 'invoice_json',
                         'invoice_generate', 'invoice_pay', 'customer_tax_rate', 'customer_upsert_from_order',
                         'subscription_activate', 'usage_refresh', 'campaign_attach', 'campaign_attach_all',
                         'order_transition_ok', 'money_pair'))
order by 1, 2;

-- 새 컬럼
select table_name, column_name, data_type
  from information_schema.columns
 where table_schema = 'sales'
   and ((table_name = 'leads'  and column_name in ('assignee', 'next_action_at', 'lost_reason', 'converted_order_id', 'campaign_id', 'archived_at'))
     or (table_name = 'orders' and column_name in ('assignee', 'next_action_at', 'customer_id', 'archived_at')))
 order by 1, 2;

-- 권한: public.admin_* 은 {postgres, anon, authenticated, service_role} 만 X (public 없음)
select p.proname, p.proacl::text
  from pg_proc p where p.pronamespace = 'public'::regnamespace and p.proname like 'admin\_%' order by 1;

-- 트리거
select c.relname, t.tgname from pg_trigger t join pg_class c on c.oid = t.tgrelid
 where c.relnamespace = 'sales'::regnamespace and not t.tgisinternal order by 1;

-- 시드: admin / owner / must_change_password = true (해시는 보지 않는다)
select username, display_name, role, status, must_change_password, created_at from sales.admin_users order by created_at;

-- ---------------------------------------------------------------------
-- 2. 헬스 (토큰 없이)
-- ---------------------------------------------------------------------
select public.admin_health();

-- ---------------------------------------------------------------------
-- 3. 로그인 (토큰은 출력하지 않는다)
-- ---------------------------------------------------------------------
select (r->>'ok')::boolean as ok, r->'user'->>'username' as username, r->'user'->>'role' as role,
       (r->'user'->>'must_change_password')::boolean as must_change, length(r->>'token') as token_len, r->>'error' as error
  from public.admin_login('admin', '1234', 'verify-ip', 'verify') as r;

-- 틀린 토큰은 unauthorized (login 이 아니므로 유량제한과 무관)
select public.admin_me(repeat('0', 64))->>'error' as bad_token, public.admin_me('junk')->>'error' as junk_token,
       public.admin_list('junk', 'orders')->>'error' as junk_list;

-- ---------------------------------------------------------------------
-- 4. 시나리오 (TEST 행 생성)
-- ---------------------------------------------------------------------
do $verify$
declare
  t   text;                  -- admin 세션 토큰
  vt  text;                  -- viewer 세션 토큰
  r   jsonb;
  cid uuid;
  sid uuid;
  iid uuid;
  vid uuid;
  inv text;
  ono text;
  m   text := to_char(timezone('Asia/Seoul', now()), 'YYYY-MM');
  n   int;
begin
  r := public.admin_login('admin', '1234', 'verify-ip', 'verify');
  assert (r->>'ok')::boolean, 'login: ' || r::text;
  t := r->>'token';

  r := public.admin_me(t);
  assert (r->>'ok')::boolean and r ? 'badges', 'me: ' || r::text;
  raise notice 'badges: %', r->'badges';

  -- 화이트리스트 밖 키 → invalid + fields
  r := public.admin_save(t, 'leads', null, '{"email":"zz-test-delete@example.com","hacker":1}'::jsonb);
  assert r->>'error' = 'invalid' and r->'fields' ? 'hacker', 'whitelist: ' || r::text;

  -- 고객 만들기 (이메일 소문자, 코드 발번)
  r := public.admin_save(t, 'customers', null, jsonb_build_object(
         'company', 'ZZ-TEST-DELETE', 'contact_name', '테스트', 'email', 'ZZ-TEST-DELETE@example.com',
         'country', 'kr', 'currency', 'KRW', 'tax_treatment', 'vat_charged', 'buyer_type', 'business',
         'tags', jsonb_build_array('test')));
  assert (r->>'ok')::boolean, 'customer: ' || r::text;
  cid := (r->'item'->>'id')::uuid;
  assert r->'item'->>'email' = 'zz-test-delete@example.com', 'email lower: ' || r::text;
  assert r->'item'->>'code' like 'CU-%' and r->'item'->>'country' = 'KR', 'code/country: ' || r::text;
  -- 같은 이메일 → conflict
  r := public.admin_save(t, 'customers', null, '{"company":"ZZ-TEST-DELETE-2","email":"zz-test-delete@example.com"}'::jsonb);
  assert r->>'error' = 'conflict', 'conflict: ' || r::text;

  -- 구독 (grow · KRW · 50% 할인 진행 중, 정가는 요금표에서)
  r := public.admin_save(t, 'subscriptions', null, jsonb_build_object(
         'customer_id', cid, 'plan', 'grow', 'currency', 'KRW', 'status', 'active',
         'started_at', sales.seoul_today(), 'discount_percent', 50, 'discount_until', sales.seoul_today() + 60));
  assert (r->>'ok')::boolean, 'subscription: ' || r::text;
  sid := (r->'item'->>'id')::uuid;
  assert (r->'item'->>'list_price')::numeric = 340000, 'list_price from pricing: ' || r::text;

  -- 인보이스 자동 초안: 340,000 × 50% = 170,000 / 세금 17,000 / 합계 187,000 (사용량 없음)
  r := public.admin_action(t, 'invoices', '*', 'generate', jsonb_build_object('customer_id', cid, 'month', m));
  assert (r->>'ok')::boolean, 'generate: ' || r::text;
  iid := (r->'item'->>'id')::uuid;
  inv := r->'item'->>'invoice_no';
  assert inv like 'IV-%', 'invoice_no: ' || inv;
  assert (r->'item'->>'net')::numeric = 170000 and (r->'item'->>'tax')::numeric = 17000
     and (r->'item'->>'total')::numeric = 187000, 'totals: ' || (r->'item')::text;
  assert r->'item'->>'status' = 'draft', 'draft';
  -- 같은 달 다시 → conflict
  r := public.admin_action(t, 'invoices', '*', 'generate', jsonb_build_object('customer_id', cid, 'month', m));
  assert r->>'error' = 'conflict', 'dup generate: ' || r::text;

  -- 발행 (인보이스 번호로 찾는다)
  r := public.admin_action(t, 'invoices', inv, 'issue', '{}'::jsonb);
  assert r->'item'->>'status' = 'issued' and r->'item'->>'due_at' is not null, 'issue: ' || r::text;
  -- 발행 뒤 본문 편집은 막히고 메모류는 된다
  r := public.admin_save(t, 'invoices', inv, '{"lines":[]}'::jsonb);
  assert r->>'error' = 'invalid', 'edit issued: ' || r::text;
  r := public.admin_save(t, 'invoices', inv, '{"tax_document":"TEST-TAXDOC"}'::jsonb);
  assert (r->>'ok')::boolean and r->'item'->>'tax_document' = 'TEST-TAXDOC', 'note on issued: ' || r::text;

  -- 부분 입금 → partially_paid
  r := public.admin_action(t, 'invoices', iid::text, 'record_payment', '{"amount":100000,"method":"transfer"}'::jsonb);
  assert r->'item'->>'status' = 'partially_paid' and (r->'item'->>'paid_amount')::numeric = 100000, 'partial: ' || r::text;
  -- 완납 → paid
  r := public.admin_action(t, 'invoices', iid::text, 'record_payment', '{"amount":87000,"method":"transfer"}'::jsonb);
  assert r->'item'->>'status' = 'paid' and r->'item'->>'paid_at' is not null, 'paid: ' || r::text;
  -- 초과 환불 → invalid, 정상 환불 → 입금 합계 감소
  r := public.admin_action(t, 'invoices', iid::text, 'refund', '{"amount":999999}'::jsonb);
  assert r->>'error' = 'invalid', 'over-refund: ' || r::text;
  r := public.admin_action(t, 'invoices', iid::text, 'refund', '{"amount":50000,"note":"test"}'::jsonb);
  assert (r->>'ok')::boolean and (r->'item'->>'paid_amount')::numeric = 137000, 'refund: ' || r::text;
  -- 입금된 인보이스 무효 → bad_transition
  r := public.admin_action(t, 'invoices', iid::text, 'void', '{}'::jsonb);
  assert r->>'error' = 'bad_transition', 'void paid: ' || r::text;

  -- 목록·정렬·상세·내보내기
  r := public.admin_list(t, 'invoices', '{"q":"ZZ-TEST"}'::jsonb, 'created_at:desc', 1, 50);
  assert (r->>'total')::int = 1 and jsonb_array_length(r->'rows') = 1, 'list invoices: ' || r::text;
  r := public.admin_list(t, 'customers', '{"q":"ZZ-TEST"}'::jsonb, 'bogus:desc', 1, 50);
  assert r->>'error' = 'invalid', 'bad sort: ' || r::text;
  r := public.admin_list(t, 'customers', '{"from":"2026-13-01"}'::jsonb, null, 1, 50);
  assert r->>'error' = 'invalid', 'bad date: ' || r::text;
  r := public.admin_get(t, 'customers', cid::text);
  assert jsonb_array_length(r->'related'->'invoices') = 1 and jsonb_array_length(r->'related'->'payments') = 3,
         'get customer: ' || left(r::text, 400);
  r := public.admin_get(t, 'invoices', inv);
  assert r->'item'->>'id' = iid::text and jsonb_array_length(r->'related'->'payments') = 3, 'get invoice by no';
  r := public.admin_export(t, 'payments', jsonb_build_object('customer_id', cid));
  assert jsonb_array_length(r->'rows') = 3 and jsonb_array_length(r->'columns') > 5, 'export: ' || left(r::text, 300);

  -- 주문 전이: 기존 주문(rejected) 에서 active 로는 못 간다
  select order_no into ono from sales.orders where state = 'rejected' limit 1;
  if ono is not null then
    r := public.admin_action(t, 'orders', ono, 'transition', '{"state":"active"}'::jsonb);
    assert r->>'error' = 'bad_transition', 'transition: ' || r::text;
    r := public.admin_action(t, 'orders', ono, 'transition', '{"state":"bogus"}'::jsonb);
    assert r->>'error' = 'invalid', 'bad state: ' || r::text;
  end if;

  -- 대시보드·통계
  r := public.admin_dashboard(t, null, null);
  assert (r->>'ok')::boolean and r->'kpi' ? 'mrr' and jsonb_array_length(r->'series'->'months') = 12, 'dashboard: ' || left(r::text, 300);
  assert (r->'kpi'->'mrr'->>'KRW')::numeric >= 170000, 'mrr: ' || (r->'kpi')::text;
  r := public.admin_stats(t, 'revenue', '{}'::jsonb);
  assert (r->>'ok')::boolean and jsonb_array_length(r->'rows') = 24, 'stats revenue: ' || left(r::text, 300);
  r := public.admin_stats(t, 'pipeline', '{}'::jsonb);
  assert (r->>'ok')::boolean and jsonb_array_length(r->'rows') = 4, 'stats pipeline: ' || left(r::text, 300);
  r := public.admin_stats(t, 'countries', '{}'::jsonb);
  assert (r->>'ok')::boolean and jsonb_array_length(r->'rows') > 10, 'stats countries: ' || left(r::text, 300);
  r := public.admin_stats(t, 'bogus', '{}'::jsonb);
  assert r->>'error' = 'invalid', 'bad report';

  -- 사용량 새로 고침 (이달) → 5 에서 대조한다
  r := public.admin_action(t, 'usage', '*', 'refresh', '{}'::jsonb);
  assert (r->>'ok')::boolean and (r->>'tenants')::int >= 1, 'usage refresh: ' || r::text;
  r := public.admin_list(t, 'usage', jsonb_build_object('month', m), 'conversations:desc', 1, 5);
  assert (r->>'total')::int >= 1, 'usage list: ' || left(r::text, 300);
  r := public.admin_list(t, 'tenants', '{}'::jsonb, 'name:asc', 1, 50);
  assert (r->>'total')::int >= 1 and not exists (
           select 1 from jsonb_array_elements(r->'rows') x where x->>'name' = '__system__'), 'tenants list: ' || left(r::text, 300);

  -- 설정 (owner)
  r := public.admin_settings_set(t, 'zz_test', '{"a":1}'::jsonb);
  assert (r->>'ok')::boolean, 'settings set: ' || r::text;
  r := public.admin_settings_get(t);
  assert r->'settings'->'zz_test'->>'a' = '1', 'settings get: ' || r::text;

  -- viewer: owner 가 만든다 → 로그인 → 쓰기 forbidden → 비밀번호 변경 → 틀린 비밀번호 유량제한
  r := public.admin_users_save(t, null, '{"username":"zz_test_viewer","display_name":"ZZ-TEST-DELETE","role":"viewer","temp_password":"viewer-temp-1"}'::jsonb);
  assert (r->>'ok')::boolean, 'user create: ' || r::text;
  vid := (r->'item'->>'id')::uuid;
  assert not (r->'item' ? 'password_hash'), 'hash leaked';
  r := public.admin_login('zz_test_viewer', 'viewer-temp-1', 'verify-ip-2', 'verify');
  assert (r->>'ok')::boolean and (r->'user'->>'must_change_password')::boolean, 'viewer login: ' || r::text;
  vt := r->>'token';
  r := public.admin_save(vt, 'customers', cid::text, '{"owner_note":"x"}'::jsonb);
  assert r->>'error' = 'forbidden', 'viewer save: ' || r::text;
  r := public.admin_action(vt, 'invoices', iid::text, 'void', '{}'::jsonb);
  assert r->>'error' = 'forbidden', 'viewer action: ' || r::text;
  r := public.admin_users_list(vt);
  assert r->>'error' = 'forbidden', 'viewer users: ' || r::text;
  r := public.admin_settings_set(vt, 'zz_test', '{"a":2}'::jsonb);
  assert r->>'error' = 'forbidden', 'viewer settings: ' || r::text;
  r := public.admin_list(vt, 'customers', '{"q":"ZZ-TEST"}'::jsonb, null, 1, 10);
  assert (r->>'total')::int = 1, 'viewer read: ' || r::text;
  r := public.admin_change_password(vt, 'viewer-temp-1', 'short');
  assert r->>'error' = 'invalid', 'pw short: ' || r::text;
  r := public.admin_change_password(vt, 'wrong-current', 'viewer-long-password-2');
  assert r->>'error' = 'invalid', 'pw wrong current: ' || r::text;
  r := public.admin_change_password(vt, 'viewer-temp-1', 'viewer-long-password-2');
  assert (r->>'ok')::boolean, 'pw change: ' || r::text;
  r := public.admin_me(vt);
  assert not (r->'user'->>'must_change_password')::boolean, 'must_change cleared: ' || r::text;
  -- 같은 아이디 5회/15분: 성공 1회 + 실패 4회 = 5회, 6번째는 rate_limited
  for n in 1..4 loop
    r := public.admin_login('zz_test_viewer', 'wrong', 'verify-ip-2', 'verify');
    assert r->>'error' = 'unauthorized', 'wrong pw ' || n || ': ' || r::text;
  end loop;
  r := public.admin_login('zz_test_viewer', 'wrong', 'verify-ip-2', 'verify');
  assert r->>'error' = 'rate_limited', 'rate limit: ' || r::text;
  -- 로그아웃 뒤 토큰 무효
  r := public.admin_logout(vt);
  r := public.admin_me(vt);
  assert r->>'error' = 'unauthorized', 'after logout: ' || r::text;
  -- viewer 비활성 (owner)
  r := public.admin_users_save(t, vid, '{"status":"disabled"}'::jsonb);
  assert r->'item'->>'status' = 'disabled', 'disable: ' || r::text;
  -- 자기 권한은 스스로 못 내린다
  r := public.admin_users_save(t, (select id from sales.admin_users where username = 'admin'), '{"role":"viewer"}'::jsonb);
  assert r->>'error' = 'invalid', 'self demote: ' || r::text;

  -- 감사 기록
  select count(*) into n from sales.admin_audit where entity_id in (cid::text, iid::text, sid::text, vid::text);
  assert n >= 10, 'audit rows: ' || n;

  -- 보관 → 기본 목록에서 사라지고 archived=true 로 보인다
  r := public.admin_action(t, 'customers', cid::text, 'archive', '{}'::jsonb);
  assert r->'item'->>'archived_at' is not null, 'archive: ' || r::text;
  r := public.admin_list(t, 'customers', '{"q":"ZZ-TEST"}'::jsonb, null, 1, 10);
  assert (r->>'total')::int = 0, 'archived hidden: ' || r::text;
  r := public.admin_list(t, 'customers', '{"q":"ZZ-TEST","archived":true}'::jsonb, null, 1, 10);
  assert (r->>'total')::int = 1, 'archived shown: ' || r::text;

  perform public.admin_logout(t);
  raise notice 'ALL OK — customer % / invoice % / viewer user %', cid, inv, vid;
end
$verify$;

-- ---------------------------------------------------------------------
-- 5. usage_monthly(이달) ↔ 운영 표 직접 집계. same 이 전부 true 여야 한다.
-- ---------------------------------------------------------------------
with b as (
  select date_trunc('month', timezone('Asia/Seoul', now()))::date as m
), w as (
  select b.m,
         (b.m::timestamp) at time zone 'Asia/Seoul' as lo,
         ((b.m + interval '1 month')::timestamp) at time zone 'Asia/Seoul' as hi
    from b
), direct as (
  select t.id as tenant_id, t.name,
         (select count(*) from public.calls c, w where c.tenant_id = t.id and c.started_at >= w.lo and c.started_at < w.hi) as calls,
         (select coalesce(sum(ceil(coalesce(c.duration_seconds, 0) / 60.0)), 0) from public.calls c, w
           where c.tenant_id = t.id and c.started_at >= w.lo and c.started_at < w.hi) as voice_minutes,
         (select count(*) from public.chat_conversations v, w where v.tenant_id = t.id and v.started_at >= w.lo and v.started_at < w.hi) as conversations,
         (select count(*) from public.chat_conversations v, w where v.tenant_id = t.id and v.channel = 'kakao'
           and v.started_at >= w.lo and v.started_at < w.hi) as chats_kakao,
         (select count(*) from public.messages mm, w where mm.tenant_id = t.id and mm.channel = 'kakao'
           and mm.status in ('sent', 'delivered') and mm.created_at >= w.lo and mm.created_at < w.hi) as alimtalk
    from public.tenants t
   where t.name <> '__system__'
)
select d.name,
       d.calls, um.calls as um_calls,
       d.voice_minutes, um.voice_minutes as um_voice_minutes,
       d.conversations, um.conversations as um_conversations,
       d.chats_kakao, um.chats_kakao as um_chats_kakao,
       d.alimtalk, um.alimtalk as um_alimtalk,
       (d.calls = um.calls and d.voice_minutes = um.voice_minutes and d.conversations = um.conversations
        and d.chats_kakao = um.chats_kakao and d.alimtalk = um.alimtalk) as same
  from direct d
  left join sales.usage_monthly um on um.tenant_id = d.tenant_id and um.month = (select m from b)
 order by same nulls first, d.name;

-- 감사 로그 최근 30건 (전부 남는지 눈으로 확인)
select a.at, a.username, a.action, a.entity, a.entity_id from sales.admin_audit a order by a.at desc limit 30;

-- ---------------------------------------------------------------------
-- 6. (선택) TEST 행 정리. 확인이 끝나면 주석을 풀어 한 번에 실행한다.
-- ---------------------------------------------------------------------
-- delete from sales.payments      where customer_id in (select id from sales.customers where company like 'ZZ-TEST%');
-- delete from sales.invoices      where customer_id in (select id from sales.customers where company like 'ZZ-TEST%');
-- delete from sales.subscriptions where customer_id in (select id from sales.customers where company like 'ZZ-TEST%');
-- delete from sales.customers     where company like 'ZZ-TEST%';
-- delete from sales.admin_sessions where user_id in (select id from sales.admin_users where username = 'zz_test_viewer');
-- delete from sales.admin_users   where username = 'zz_test_viewer';
-- delete from sales.settings      where key = 'zz_test';
-- delete from sales.admin_sessions where ip_hash like 'verify%';
-- delete from sales.rate_hits     where bucket like 'admin_login:%verify%' or bucket = 'admin_login:u:zz_test_viewer';
-- delete from sales.admin_audit   where username = 'zz_test_viewer' or entity_id in ('zz_test');
