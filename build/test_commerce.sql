-- 상거래 규칙 시험.
--
-- 감사에서 나온 지적이 전부 이 규칙에 걸립니다.
--   · 독일·프랑스도 VAT 번호 없이 리버스 차지로 표시됐다
--   · 사업자·소비자·공공기관 구분이 없었다
--   · 'Somewhere else' 도 USD·세금 0 으로 주문이 끝났다
--   · 전화 미지원 국가에서도 Scale 을 그대로 주문할 수 있었다
--
-- 고쳤다는 말로는 다음에 또 풀립니다. 여기서 실제로 물어봅니다.
--
--   psql < build/test_commerce.sql
--   또는 Supabase SQL 편집기에 붙여 넣기

\set ON_ERROR_STOP on

do $test$
declare
  pass int := 0;
  fail int := 0;
  msgs text[] := '{}';


  r jsonb;

  i int;
  KRNO text := '0010000003';   -- 국세청 검증식을 통과하는 번호
begin
  -- 요금표가 올라와 있어야 합니다
  if not exists (select 1 from sales.pricing_versions where active) then
    raise exception '요금표가 DB 에 없습니다. sales.refresh_from_site() 를 먼저 부르십시오.';
  end if;

  -- ── 한국 ──────────────────────────────────────────────────────────
  r := sales.commerce('KR', 'business', KRNO, 'grow');
  if (r->>'taxTreatment') = 'vat_charged' and (r->>'taxRate')::numeric = 0.1
     and (r->>'orderable')::boolean then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || (format('한국 사업자 + 유효 사업자번호 → 부가세 10%% 부과, 주문 가능이어야 함. 실제: %s', r))::text;
  end if;

  r := sales.commerce('KR', 'business', '111-11-11111', 'grow');
  if (r->>'taxTreatment') = 'review' and not (r->>'orderable')::boolean then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || (format('한국 + 검증식 실패 번호 → 주문 불가여야 함. 실제: %s', r))::text;
  end if;

  -- ── EU 사업자: VAT 번호가 있어야 리버스 차지 ──────────────────────
  r := sales.commerce('DE', 'business', 'DE123456789', 'grow');
  if (r->>'taxTreatment') = 'reverse' and (r->>'orderable')::boolean is not false then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || (format('독일 사업자 + VAT 번호 → 리버스 차지여야 함. 실제: %s', r))::text;
  end if;

  r := sales.commerce('DE', 'business', '', 'grow');
  if (r->>'taxTreatment') = 'review' and not (r->>'orderable')::boolean then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || (format('독일 사업자 + VAT 번호 없음 → 리버스 차지로 적으면 안 됨. 실제: %s', r))::text;
  end if;

  -- ── EU 개인: 한국 법인은 현지 부가세 등록이 없다 ──────────────────
  r := sales.commerce('FR', 'consumer', '', 'grow');
  if (r->>'taxTreatment') = 'review' and not (r->>'orderable')::boolean then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || (format('프랑스 개인 → 온라인 주문 불가여야 함. 실제: %s', r))::text;
  end if;

  -- ── 공공기관: 조달·원천징수 확인이 필요하다 ────────────────────────
  r := sales.commerce('US', 'public', '', 'grow');
  if (r->>'taxTreatment') = 'review' and not (r->>'orderable')::boolean then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || (format('공공기관 → 서면 주문이어야 함. 실제: %s', r))::text;
  end if;

  -- ── 나라를 특정하지 않으면 통화도 세금도 정할 수 없다 ──────────────
  r := sales.commerce('OTHER', 'business', 'ABC12345', 'grow');
  if (r->>'taxTreatment') = 'review' and not (r->>'orderable')::boolean then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || (format('OTHER → 주문 불가여야 함. 실제: %s', r))::text;
  end if;

  -- ── 전화가 없는 나라에 전화가 든 요금제 ────────────────────────────
  r := sales.commerce('FR', 'business', 'FR12345678901', 'scale');
  if not (r->>'orderable')::boolean
     and r->'blockers' @> '[{"code":"voice_unavailable"}]'::jsonb then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || (format('프랑스 + Scale(AI 전화) → 주문 막고 이유를 알려야 함. 실제: %s', r))::text;
  end if;

  r := sales.commerce('DE', 'business', 'DE123456789', 'scale');
  if not (r->>'orderable')::boolean
     and r->'blockers' @> '[{"code":"voice_soon"}]'::jsonb then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || (format('독일(개통 중) + Scale → 개통 중이라고 알려야 함. 실제: %s', r))::text;
  end if;

  -- 전화가 되는 나라에서는 Scale 이 열려 있어야 합니다
  r := sales.commerce('US', 'business', 'EIN123456', 'scale');
  if (r->>'orderable')::boolean and (r->>'taxTreatment') = 'none' then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || (format('미국 사업자 + Scale → 주문 가능, 세금 없음이어야 함. 실제: %s', r))::text;
  end if;

  -- 전화가 없는 나라라도 전화가 없는 요금제는 팔 수 있어야 합니다
  r := sales.commerce('FR', 'business', 'FR12345678901', 'start');
  if (r->>'orderable')::boolean then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || (format('프랑스 + Start(전화 없음) → 주문 가능해야 함. 실제: %s', r))::text;
  end if;

  -- ── 통화 ──────────────────────────────────────────────────────────
  if (sales.commerce('KR','business',KRNO,'grow')->>'currency') = 'KRW'
     and (sales.commerce('US','business','EIN1','grow')->>'currency') = 'USD' then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || '통화는 한국 KRW, 그 밖 USD 여야 함'::text;
  end if;

  -- ── 금액 ──────────────────────────────────────────────────────────
  r := sales.quote(jsonb_build_object(
        'plan','grow','method','transfer','country','KR',
        'buyerType','business','taxId',KRNO));
  if (r->'monthly'->>'tax')::numeric > 0
     and (r->'monthly'->>'total')::numeric
         = (r->'monthly'->>'net')::numeric + (r->'monthly'->>'tax')::numeric then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || (format('한국 금액: 합계 = 이용료 + 세금 이어야 함. 실제: %s', r->'monthly'))::text;
  end if;

  r := sales.quote(jsonb_build_object(
        'plan','grow','method','transfer','country','US',
        'buyerType','business','taxId','EIN123456'));
  if (r->'monthly'->>'tax')::numeric = 0 then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || (format('미국 금액: 세금 0 이어야 함. 실제: %s', r->'monthly'))::text;
  end if;

  -- 화면이 보낸 금액은 쓰지 않는다 (그런 열쇠를 넣어도 무시되어야 함)
  r := sales.quote(jsonb_build_object(
        'plan','grow','method','transfer','country','KR',
        'buyerType','business','taxId',KRNO,
        'monthly', jsonb_build_object('total', 1)));
  if (r->'monthly'->>'total')::numeric > 1000 then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || '화면이 보낸 금액이 결과에 새어 들어감'::text;
  end if;

  -- ── 사업자등록번호 검증식 ─────────────────────────────────────────
  if sales.kr_bizno_valid(KRNO)
     and not sales.kr_bizno_valid('220-88-01002')
     and not sales.kr_bizno_valid('12345')
     and not sales.kr_bizno_valid('') then
    pass := pass + 1;
  else
    fail := fail + 1;
    msgs := msgs || '사업자등록번호 검증식이 틀림'::text;
  end if;

  -- ── 결과 ──────────────────────────────────────────────────────────
  raise notice '';
  raise notice '통과 %, 실패 %', pass, fail;
  if fail > 0 then
    raise notice '';
    for i in 1..array_length(msgs, 1) loop
      raise notice '  X %', msgs[i];
    end loop;
    raise exception '상거래 규칙 시험 % 건 실패', fail;
  end if;
  raise notice '상거래 규칙은 위 % 가지 상황에서 모두 옳게 답합니다.', pass;
end;
$test$;
