# 주문을 실제로 받으려면 — 사장님이 하실 일

**접수는 이미 살아 있습니다.** `/api/order` 와 `/api/lead` 가 `ready: true` 이고,
들어온 주문과 문의는 PostgreSQL 에 남습니다. 잃어버리지 않습니다.

남은 것은 두 가지입니다. 하나는 법이 요구하는 것이고, 하나는 편의입니다.

---

## 지금 어떻게 동작하는가

```
구매자가 주문서를 채움
        ↓
/api/order  ─ 화면이 보낸 금액은 버리고, 선택만 데이터베이스로 넘깁니다
        ↓
PostgreSQL  ─ 여기서 한 트랜잭션 안에 전부 끝납니다
              · 나라·구매자 유형·세금번호로 세금 처리를 판정
              · 전화 회선이 없는 나라면 서면 검토로 보냄
              · 그때 유효한 요금표로 금액을 처음부터 다시 계산
              · 주문번호 발번, 중복 방지, 유량 제한
        ↓
메일·웹훅·슬랙 ─ 알림입니다. 하나도 안 나가도 주문은 이미 남아 있습니다.
```

주문을 보시는 곳: **Supabase → Saleringo 프로젝트 → SQL Editor**

```sql
select order_no, state, company, billing_country, plan,
       currency, monthly_total, tax_treatment, created_at
  from sales.orders
 order by created_at desc;
```

문의는 `sales.leads`, 상태가 바뀐 기록은 `sales.order_events` 에 있습니다.

---

## 0단계 — 판매자 정보 채우기 (필수, 2분)

`build/company.json` 에 아래를 채우고 `python build/build.py` 를 돌리십시오.

    "ceo":            대표자명
    "bizNo":          사업자등록번호
    "mailOrderNo":    통신판매업 신고번호
    "address":        사업장 주소
    "privacyOfficer": 개인정보 보호책임자

「전자상거래법」 제13조가 주문 화면에 요구하는 항목입니다. 저는 없는 번호를
지어낼 수 없어 비워 두었고, **비어 있는 항목은 화면에 아예 나가지 않습니다.**
채우기 전까지 빌드할 때마다 경고가 뜹니다. 실제 주문을 받기 시작하면
이건 선택이 아니라 위반입니다.

---

## 1단계 — 주문이 들어오면 알림 받기 (권장, 5분)

주문은 이미 데이터베이스에 남으므로 이걸 안 하셔도 잃어버리지 않습니다.
다만 안 하시면 **직접 열어 보실 때까지 모르십니다.**

Vercel → claude-saleringo → Settings → Environment Variables 에
아래 중 **하나만** 넣으시면 됩니다.

| 변수 | 값 | 결과 |
|---|---|---|
| `LEAD_WEBHOOK_URL` | JSON 을 받는 아무 주소 (Zapier, Make, 구글 시트 Apps Script, n8n) | 주문이 그 주소로 도착 |
| `SLACK_WEBHOOK_URL` | 슬랙 Incoming Webhook 주소 | 슬랙 채널에 주문 내용이 그대로 |
| `RESEND_API_KEY` + `LEAD_TO_EMAIL` + `LEAD_FROM_EMAIL` | Resend 키와 받을 주소, 보내는 주소 | 사장님께 메일 + **구매자에게 확인 메일** |

세 번째를 넣으시면 하나가 더 생깁니다 — **구매자가 확인 메일을 받습니다.**
지금은 주문번호가 화면에만 뜨고, 구매자는 그것을 적어 두거나
[주문 조회](https://claude.saleringo.com/ko/order-status.html) 에서
다시 여셔야 합니다. 확인 메일이 있으면 그 수고가 없어집니다.

`/api/order` 를 열어 보시면 지금 상태를 알 수 있습니다.

```
{"ready":true, "confirmation":false, "notify":false}
             └ 접수 O      └ 확인메일 X   └ 알림 X
```

---

## 2단계 — 결제사 붙이기 (나중에)

지금은 **접수까지만** 갑니다. 그것이 화면·메일·약관에 일관되게 적혀 있습니다.

> 계약은 서면 주문서에 양측이 서명한 때 성립합니다.
> 주문 접수는 청약이며, 그 단계에서는 어떤 금액도 청구되지 않습니다.

결제사가 붙으면 `PAYMENT_PROVIDER` 에 이름을 넣으십시오
(`toss`, `stripe`, `nicepay` …). 그러면 화면이 "주문 접수하기" 대신
결제 단계를 안내하도록 바뀝니다. 넣기 전까지는 결제라고 말하지 않습니다.

---

## 데이터베이스에 대해

이미 쓰고 계신 **Saleringo** 프로젝트(Supabase · 서울 리전 · PostgreSQL 17)
안에 `sales` 스키마를 새로 만들어 두었습니다. 제품 운영 테이블(`public.*`)은
한 줄도 건드리지 않습니다.

| 표 | 무엇 |
|---|---|
| `sales.orders` | 주문. 그때 본 요금표 판과 동의 기록을 함께 담습니다 |
| `sales.leads` | 도입 문의 |
| `sales.order_events` | 상태가 바뀐 시각·주체·사유 |
| `sales.pricing_versions` / `policy_versions` | 요금표·정책의 판 |

**잠금.** `sales` 스키마는 RLS 로 전면 차단되어 있고 PostgREST 에 노출되지도
않습니다. 웹사이트가 쓰는 키는 publishable 키인데, 이 키로는 표를 한 줄도
읽거나 쓸 수 없습니다. 할 수 있는 일은 검증을 자기 안에 가진 함수 몇 개를
부르는 것뿐입니다. `service_role` 키는 사이트 코드 어디에도 없습니다.

**요금표.** `assets/data/pricing.json` 과 `assets/data/policy.json` 을 고치고
배포하시면, 데이터베이스가 배포된 파일을 스스로 읽어 새 판으로 바꿉니다.
따로 올리실 것이 없습니다. 판이 올라오기 전에는 주문을 받지 않습니다 —
금액을 계산할 근거가 없는 상태로 "접수되었습니다" 라고 말하지 않기 위해서입니다.

---

## 주문 상태 옮기기

주문이 들어오면 `received`(또는 확인할 것이 있으면 `under_review`)로 시작합니다.
다음 단계로 옮기실 때는 SQL Editor 에서:

```sql
-- 상태를 옮기고 기록을 남깁니다. 둘을 함께 하셔야 이력이 맞습니다.
with moved as (
  update sales.orders
     set state = 'contract_sent', updated_at = now()
   where order_no = 'SO-20260827-1001'
  returning id, state
)
insert into sales.order_events (order_id, to_state, actor, reason)
select id, state, '사장님', '서면 주문서 발송' from moved;
```

상태는 이 순서입니다.

```
received → proposal_sent → under_review → contract_sent
        → contract_signed → payment_pending → paid → active
```

`contract_signed` 가 **계약이 성립한 시점**입니다. 약관과 주문서가 모두
그렇게 적혀 있으므로, 이 값을 다른 뜻으로 쓰지 마십시오.
취소·반려는 이 줄 밖의 `cancelled` · `rejected` 입니다.

구매자는 [주문 조회](https://claude.saleringo.com/ko/order-status.html) 에서
주문번호와 이메일로 지금 어느 단계인지 볼 수 있습니다.

---

## 나라별로 무엇이 열려 있는가

서버가 판정합니다. 화면은 그 답을 그대로 씁니다.

| 경우 | 세금 | 온라인 주문 |
|---|---|---|
| 한국 사업자 (검증식 통과한 번호) | 부가세 10% · 세금계산서 | 열림 |
| EU 사업자 + 유효한 VAT 번호 | 대리납부(리버스 차지) | 열림 |
| EU 사업자, VAT 번호 없음 | 확정 전 | 서면 주문 |
| 한국 밖 개인 | 확정 전 | 서면 주문 |
| 공공기관·학교 | 확정 전 | 서면 주문 |
| 그 밖의 나라 사업자 | 세금 없음 | 열림 |
| 나라 미지정 | 확정 전 | 서면 주문 |
| AI 전화가 든 요금제 + 회선 없는 나라 | — | 서면 주문 |

정책을 바꾸시려면 `sales.commerce()` 함수 하나만 고치시면 됩니다.
화면·메일·주문 기록이 모두 그 답을 따라갑니다.

바꾸신 뒤에는 `build/test_commerce.sql` 을 Supabase SQL Editor 에 붙여
돌려 보십시오. 16가지 상황을 확인합니다.

---

## 확인하는 방법

```
node build/test_order.mjs      API 전달 계층 61건 (네트워크 없이)
node build/test_strings.mjs    화면에 나가는 문장과 전화번호 서식
python build/pricecheck.py     요금표와 페이지의 숫자가 같은지
python build/policy.py --check 두 언어의 약관이 같은 정책을 말하는지
python build/a11ycheck.py      키보드와 스크린리더가 같은 화면을 보는지
python build/mailcheck.py      안내하는 이메일이 실제로 메일을 받는지
python build/deadclass.py      스타일을 통째로 잃은 원소가 있는지
python build/routes.py --check 주소 규칙
python build/build.py          142장 다시 짓기
```

`mailcheck` 는 지금 **실패합니다.** saleringo.com 에 MX 레코드가 없어
`hello@saleringo.com`(142개 페이지에 188번)과 `security@saleringo.com`
으로 보내는 메일이 전부 반송되기 때문입니다. 주문 접수 실패 안내, 해지
요청, 문서 요청, 약관의 소송 이전 연락 — 구매자가 막혔을 때 가라고
안내하는 곳이 전부 이 주소입니다.

도메인에 MX·SPF·DMARC 를 거시면 이 검사가 통과합니다. 그때까지는 주문
실패 안내가 이메일 대신 「다시 눌러 주십시오」와 「서면 주문 제안 요청」을
먼저 가리키도록 해 두었습니다 — 주문이 데이터베이스에 남으므로 그쪽이
사실입니다.

`build/test_commerce.sql` 은 데이터베이스에 직접 물어봅니다 — Supabase
SQL Editor 에 붙여 넣으십시오.
