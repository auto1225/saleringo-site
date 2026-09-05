-- 주문 조회 화면의 개통 체크리스트 (2026-09-05)
--
-- 주문번호와 이메일이 맞는 사람에게만 그 주문의 개통 단계를 돌려준다.
-- sales.order_status 와 같은 검증을 다시 거친다 — 이 함수가 anon 키로 호출되기
-- 때문이다. 번호만 알고 이메일을 모르면 아무것도 열리지 않는다.

create or replace function public.sales_provisioning_status(p_order_no text, p_email text)
returns jsonb
language plpgsql
security definer
set search_path to 'sales', 'public'
as $function$
declare
  v_order  sales.orders%rowtype;
  v_tenant public.tenants%rowtype;
  v_jobs   jsonb;
  v_number jsonb;
begin
  if not sales.global_ok('status', 120) then
    return jsonb_build_object('ok', false, 'error', 'busy');
  end if;
  if not sales.rate_ok('provision:' || coalesce(p_email, ''), 20, interval '10 minutes') then
    return jsonb_build_object('ok', false, 'error', 'rate_limited');
  end if;

  select * into v_order from sales.orders
   where order_no = upper(btrim(coalesce(p_order_no, '')))
     and lower(email) = lower(btrim(coalesce(p_email, '')));
  if not found then
    return jsonb_build_object('ok', false, 'error', 'not_found');
  end if;

  select coalesce(jsonb_agg(jsonb_build_object(
           'step', j.step, 'status', j.status, 'attempts', j.attempts,
           'needsHuman', j.needs_human, 'dueAt', j.due_at,
           'startedAt', j.started_at, 'finishedAt', j.finished_at,
           /* 구매자에게 보여도 되는 것만 — 오류 원문은 넘기지 않는다 */
           'note', j.detail->>'customer_note',
           'action', j.detail->>'customer_action'
         ) order by j.created_at), '[]'::jsonb)
    into v_jobs
    from public.provisioning_jobs j
   where j.order_no = v_order.order_no;

  select * into v_tenant from public.tenants t
   where t.id = (select j.tenant_id from public.provisioning_jobs j
                  where j.order_no = v_order.order_no and j.tenant_id is not null limit 1);

  if v_tenant.id is not null then
    select jsonb_build_object('e164', n.e164, 'country', n.country, 'owner', n.owner, 'status', n.status)
      into v_number
      from public.phone_numbers n
     where n.tenant_id = v_tenant.id and n.status in ('reserved', 'assigned')
     order by n.assigned_at desc nulls last limit 1;
  end if;

  return jsonb_build_object(
    'ok', true,
    'orderNo', v_order.order_no,
    'jobs', v_jobs,
    'tenant', case when v_tenant.id is null then null else
      jsonb_build_object('name', v_tenant.name, 'number', v_number) end
  );
end;
$function$;

revoke all on function public.sales_provisioning_status(text, text) from public;
grant execute on function public.sales_provisioning_status(text, text) to anon, authenticated, service_role;
