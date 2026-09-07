# Saleringo 판매 관리자(Sales Admin) 설계 명세 v1

작성 2026-09-07. 이 문서는 관리자 시스템의 유일한 설계 원천이다. DB·API·화면을 만드는 사람(에이전트)은 이 문서와 어긋나게 만들지 않는다. 어긋나야 한다면 이 문서를 먼저 고친다.

## 0. 한 문단 요약

`claude.saleringo.com/admin/` 은 **Saleringo 솔루션을 파는 회사(정직한마케팅 주식회사)의 운영자**가 쓰는 뒷사무실이다. 글로벌 판매 사이트(website-global)로 들어오는 **문의·주문**을 받아 **고객·구독·인보이스·결제**로 이어 가고, 운영 앱(saleringo.com, Supabase 같은 프로젝트)의 **테넌트 사용량**을 읽어 청구와 한도를 관리하며, **통계·마케팅** 화면으로 나라·언어·채널·캠페인별 성과를 본다. 운영 앱의 기존 관리자(`saleringo.com/admin`, 테넌트 운영·지식베이스·CMS)는 그대로 두고 링크로 잇는다. 두 관리자의 역할: **여기서는 돈과 고객과 시장을, 저기서는 테넌트의 내부 운영을.**

## 1. 기술 구조 (바꾸지 말 것)

| 층 | 결정 | 이유 |
|---|---|---|
| 저장소 | 이 저장소(website-global, 공개 GitHub `auto1225/saleringo-site`). | 주문·문의·요금표·정책 판이 이미 여기 `sales` 스키마에 있다. |
| DB | Supabase `Saleringo`(`lzqpdxsvleqyhkyhzgld`), 스키마 `sales` 에 표 추가(추가 전용, 기존 표 컬럼 삭제·변경 금지). 운영 표(`public.tenants`, `calls`, `chat_conversations`, `phone_numbers`, `provisioning_jobs`, `inquiries` …)는 **읽기만** 한다. | 한 프로젝트에 판매와 운영이 같이 있어 조인이 가능하다. 운영 표를 여기서 쓰면 운영 앱과 어긋난다. |
| 접근 방식 | **service_role 키를 쓰지 않는다.** 모든 접근은 `public.admin_*` SECURITY DEFINER 함수(RPC)를 publishable 키로 부르고, 함수 안에서 **세션 토큰**을 검증한다. `sales` 스키마는 PostgREST 에 노출하지 않는다. | 기존 `sales_*` 함수와 같은 원칙: 키가 새어도 잃을 것이 없다. 공개 저장소에 비밀이 들어갈 길을 없앤다. |
| API | Vercel 서버리스 함수 **하나** `api/admin.js` (ESM, 기존 `api/_db.js` 의 `rpc()` 재사용). `vercel.json` rewrite: `/api/admin/:path*` → `/api/admin?p=:path*`, `/admin` 과 `/admin/:path*` → `/api/admin?page=:path*`. | Hobby 플랜 함수 12개 제한. 화면 HTML 도 이 함수가 세션을 확인하고 내보내므로 로그인 없이는 화면 껍데기도 열리지 않는다. |
| 화면 파일 | `api/_admin/pages/*.html` (정적으로 서빙되지 않는 위치 — `api/` 아래 `_` 파일은 404 확인됨), CSS/JS 는 `assets/admin/` (공개, 비밀 없음). `vercel.json` `functions["api/admin.js"].includeFiles = "api/_admin/**"`. | 껍데기까지 로그인 뒤에만. |
| 인증 | 아이디+비밀번호. 해시는 DB 안에서 `pgcrypto crypt(pw, gen_salt('bf', 10))`. 세션 토큰 32바이트 랜덤(`gen_random_bytes`), DB 에는 `sha256(token)` 만 저장. 쿠키 `sra` HttpOnly·Secure·SameSite=Lax·Path=/, 유휴 12시간·절대 7일. 로그인 유량제한(같은 아이디 5회/15분, 같은 IP 20회/15분, `sales.rate_ok` 재사용). CSRF: POST 는 `X-Admin: 1` 헤더 + Origin 이 자기 도메인일 것. | 초기 계정 `admin` / `1234`(요청대로). 기본 비밀번호인 동안 모든 화면 상단에 붉은 띠로 변경을 요구한다. |
| 역할 | `owner`(전부) · `staff`(읽기+메모·상태 변경, 관리자 관리·설정·삭제 불가) · `viewer`(읽기만). | 처음엔 owner 하나. |
| 감사 | 쓰기 함수는 전부 `sales.admin_audit` 에 남긴다(누가·언제·무엇을·전후 값). 삭제는 소프트(archived_at). | 상업용. 되돌릴 수 있어야 한다. |
| 언어 | 화면 문구는 한국어 기본, `ko/en` 토글(`assets/admin/i18n.js`). 데이터(나라·통화)는 코드+이름. 금액은 통화 관습대로(KRW 정수, USD 센트). 시간은 Asia/Seoul 표시, 저장은 UTC. | 운영자는 한국인, 시장은 글로벌. |
| 외부 라이브러리 | 없음. 차트는 인라인 SVG 를 JS 로 그린다. 폰트는 사이트와 같은 Google Fonts. | CSP `script-src 'self'`, 의존성 0. |
| 노출 차단 | `/admin/*` 응답 헤더 `X-Robots-Tag: noindex, nofollow`, `Cache-Control: no-store`. 사이트맵·라우트 생성기(`build/routes.py`, `sitemapxml.py`)는 `admin` 을 절대 포함하지 않는다. | |

## 2. 데이터 모델 (스키마 `sales`, 마이그레이션 파일 `supabase/admin/001_admin.sql`)

공통: `id uuid default gen_random_uuid() pk`, `created_at/updated_at timestamptz default now()`, updated_at 트리거. 모든 새 표 `enable row level security` + 정책 없음(= 함수만 접근). 돈은 `numeric`, 통화 `text` (`KRW`|`USD`).

### 2.1 관리자
- `admin_users(id, username text unique (lower), display_name, email, password_hash, role text check in ('owner','staff','viewer'), status ('active','disabled'), must_change_password bool default true, last_login_at, failed_logins int, created_at, updated_at)`
- `admin_sessions(id, user_id fk, token_hash text unique, created_at, last_seen_at, expires_at, ip_hash, user_agent, revoked_at)`
- `admin_audit(id bigserial, at, user_id, username, action text, entity text, entity_id text, before jsonb, after jsonb, ip_hash)`
- 시드: `admin`/`1234`, role owner, display_name '관리자', must_change_password true.

### 2.2 고객·구독·청구
- `customers(id, code text unique 'CU-YYYYMMDD-NNNN', company, contact_name, email (lower), phone, country text, currency, buyer_type, tax_id, tax_treatment, billing_address, lang, tenant_id uuid (public.tenants.id, 느슨한 참조), status ('lead','trial','active','paused','churned'), source text, tags text[], owner_note text, first_order_id uuid, archived_at)`
  - 주문이 `contract_signed` 이상으로 가면 이메일 기준으로 고객을 만들거나 잇는다(함수 `sales.customer_upsert_from_order`). 운영자가 직접 만들 수도 있다.
- `subscriptions(id, customer_id fk, order_id uuid, plan text ('start','grow','scale' — pricing.json 의 id), currency, list_price numeric, discount_percent numeric default 0, discount_until date, status ('pending','trial','active','paused','canceled'), started_at date, current_period_start date, current_period_end date, cancel_at date, canceled_at, tenant_id uuid, note)`
- `invoices(id, invoice_no text unique 'IV-YYYYMM-NNNN', customer_id fk, subscription_id, order_id, period_start date, period_end date, currency, lines jsonb [{kind:'plan'|'voice'|'alimtalk'|'overage'|'setup'|'credit'|'other', label, qty, unit, amount}], net numeric, tax_rate numeric, tax numeric, total numeric, status ('draft','issued','paid','partially_paid','overdue','void','refunded'), issued_at, due_at date, paid_at, method text, provider text, provider_ref text, tax_document text (세금계산서 번호 등), note, archived_at)`
  - 발행 시 `issued_at` 세팅, `net/tax/total` 은 `lines` 에서 함수가 다시 합산한다(화면이 보낸 합계는 쓰지 않는다). 세율은 고객의 `tax_treatment`(vat_charged→활성 요금표 tax.KR.rate, 그 밖 0).
- `payments(id, invoice_id fk, customer_id fk, amount numeric, currency, method ('card','transfer','other'), provider text, provider_ref text, received_at timestamptz, kind ('payment','refund'), note, recorded_by uuid)`
  - 결제 기록 시 인보이스의 paid 합계를 다시 계산해 status 를 `paid`/`partially_paid` 로. 환불(kind refund, 음수 아님 — amount 양수 + kind 로 구분) 시 `refunded`.
- `usage_monthly(id, tenant_id uuid, month date (YYYY-MM-01), calls int, call_seconds int, voice_minutes numeric (ceil(seconds/60) 합), conversations int, chats_web int, chats_kakao int, chats_phone int, alimtalk int, computed_at)` — `sales.usage_refresh(p_month)` 가 `public.calls`, `public.chat_conversations`, `public.messages`(channel kakao, status sent) 에서 다시 계산해 upsert. 대시보드는 이 표를 읽고, "지금 새로 고침" 버튼이 함수를 부른다.

### 2.3 파이프라인·마케팅
- `sales.leads` (기존) — `status` 값은 'new','contacted','qualified','proposal','won','lost','spam'. `owner_note` 에 메모. 새 컬럼 추가: `assignee text`, `next_action_at timestamptz`, `lost_reason text`, `converted_order_id uuid`, `campaign_id uuid`, `archived_at`.
- `sales.orders` (기존) — 상태 전이는 `sales.order_state` 그대로. 새 컬럼: `assignee text`, `next_action_at`, `customer_id uuid`, `archived_at`. 전이는 `order_events` 에 남긴다(actor = 관리자 username).
  - 허용 전이(그 밖은 오류): received→under_review|contract_sent|cancelled|rejected; under_review→proposal_sent|contract_sent|cancelled|rejected; proposal_sent→contract_sent|cancelled|rejected; contract_sent→contract_signed|cancelled; contract_signed→payment_pending|active; payment_pending→paid|cancelled; paid→active; active→cancelled. `contract_signed` 로 갈 때 고객·구독을 만든다(없으면).
- `campaigns(id, name, channel ('search','social','email','referral','event','partner','content','other'), utm_source, utm_medium, utm_campaign, country text, lang, budget numeric, currency, starts_on, ends_on, status ('planned','active','paused','ended'), landing_url, note, archived_at)`
  - 리드의 `utm` jsonb 와 (source, medium, campaign) 이 같으면 `campaign_id` 로 잇는다(함수 `sales.campaign_attach`). 통계에서 캠페인별 리드·주문 수를 센다.
- `tasks(id, kind ('call','email','followup','contract','provisioning','billing','other'), title, entity ('lead','order','customer','invoice'), entity_id uuid, due_at, done_at, assignee text, note, created_by)`
- `notes(id, entity, entity_id uuid, body text, author text, created_at)`
- `settings(key text pk, value jsonb, updated_at, updated_by)` — 예: `company` (회사 정보), `notify` (알림 이메일), `dashboard` (기본 기간), `pipeline_sla` (응답 SLA 시간).

### 2.4 함수 (`public.admin_*`, 전부 `SECURITY DEFINER`, `set search_path = sales, public`, `returns jsonb`)

모든 함수는 첫 인자 `p_token text` (로그인·헬스 제외). 공통 오류 형식 `{"ok":false,"error":"<code>","message":{"ko":..,"en":..}}`. 오류 코드: `unauthorized`, `forbidden`, `rate_limited`, `invalid`(+`fields`), `not_found`, `conflict`, `bad_transition`.

| 함수 | 인자 | 하는 일 |
|---|---|---|
| `admin_login` | `p_username, p_password, p_ip_hash, p_user_agent` | 유량제한 → 검증 → 세션 생성 → `{ok, token, user:{id,username,display_name,role,must_change_password}}`. 실패도 같은 시간 걸리게(crypt 는 항상 부른다). |
| `admin_logout` | `p_token` | 세션 revoke. |
| `admin_me` | `p_token` | 세션 연장(last_seen) + 사용자 정보 + 대기 건수 뱃지(`badges`: 새 문의, 확인 대기 주문, 미납·연체 인보이스, 사람 손 필요한 개통 작업, 오늘 할 일). |
| `admin_change_password` | `p_token, p_current, p_new` | 새 비밀번호 10자 이상, 현재 비밀번호 검증, 다른 세션 전부 revoke, must_change_password false. |
| `admin_users_list/save/disable` | owner 만 | 관리자 관리. 비밀번호 재설정은 owner 가 임시 비밀번호를 정해 주고 must_change_password true. |
| `admin_dashboard` | `p_token, p_from date, p_to date` | KPI(아래 §4.1)와 월별 시계열, 나라·플랜·언어 분포, 할 일 목록. |
| `admin_list` | `p_token, p_entity, p_filter jsonb, p_sort text, p_page int, p_size int(≤200)` | `leads, orders, customers, subscriptions, invoices, payments, campaigns, tasks, tenants, usage, numbers, jobs, audit, users`. 반환 `{ok, rows, total, page, size}`. 검색 `q` 는 회사·이름·이메일·번호에 ilike. |
| `admin_get` | `p_token, p_entity, p_id` | 상세 + 연관(주문이면 events·notes·tasks·customer; 고객이면 orders·subscriptions·invoices·payments·usage·tenant). |
| `admin_save` | `p_token, p_entity, p_id (null=생성), p_data jsonb` | 생성/수정. 화이트리스트 컬럼만. 감사 기록. |
| `admin_action` | `p_token, p_entity, p_id, p_action, p_data` | 상태 전이·발행·입금·환불·취소·복구·병합 등 부수효과 있는 것. `orders.transition{state, reason}`, `leads.set_status{status, lost_reason}`, `leads.convert{}`(고객 생성), `invoices.issue`, `invoices.void`, `invoices.record_payment{amount,method,provider_ref,received_at}`, `invoices.refund{amount,note}`, `invoices.generate{customer_id, month}`(구독+사용량으로 초안 자동 생성), `subscriptions.change_plan{plan, effective_on}`, `subscriptions.cancel{cancel_at}`, `subscriptions.pause/resume`, `customers.link_tenant{tenant_id}`, `usage.refresh{month}`, `tasks.done`, `*.archive`, `*.restore`. |
| `admin_stats` | `p_token, p_report, p_params` | `revenue`(월별 net/tax/total, 통화별, 나라별, 플랜별), `pipeline`(문의→주문→계약→개통 전환, 단계 체류일), `marketing`(출처·UTM·캠페인·언어·페이지별 리드·주문), `usage`(테넌트별 월별, 한도 대비 %), `cohort`(창립 할인 고객 유지), `countries`(요금표 나라별 리드·주문·구독). |
| `admin_export` | `p_token, p_entity, p_filter` | 목록과 같은 필터로 최대 5,000행, 열 이름 한국어/영어 헤더 포함 `{ok, columns:[{key,ko,en}], rows}`. API 가 CSV(UTF-8 BOM)로 내려 준다. |
| `admin_settings_get/set` | | 설정. |
| `admin_health` | 토큰 불필요 | `{ok:true, db:true, pricingVersion, policyVersion, adminUsers:n}` — 로그인 화면이 DB 준비 여부를 보이는 데 쓴다. 비밀 정보 없음. |

내부 함수(`sales.*`, 노출 안 함): `admin_auth(p_token) returns admin_users`, `admin_require(role)`, `audit(...)`, `next_customer_code()`, `next_invoice_no()`, `invoice_totals(lines, tax_rate, cur)`, `customer_upsert_from_order(order_id)`, `usage_refresh(month)`, `campaign_attach(lead_id)`.

## 3. API (`api/admin.js`)

- 라우팅: `?page=` 가 있으면 화면 서빙, 아니면 `?p=` 가 액션 이름.
- 화면: `/admin` `/admin/` `/admin/index` → 세션 유효하면 `pages/app.html`(단일 셸, 해시 라우팅 `#/orders/…`), 아니면 302 `/admin/login`. `/admin/login` → `pages/login.html`(세션 유효하면 302 `/admin`). 그 밖의 `/admin/<x>` → `app.html`(셸이 해시로 처리) 또는 404.
- 액션(POST JSON, `X-Admin: 1` 필수, Origin 검사): `login, logout, me, password, dashboard, list, get, save, action, stats, export, settings, users` → 각각 `admin_*` RPC. `export` 는 GET 도 허용(다운로드 링크) — `Content-Disposition: attachment; filename=<entity>-<date>.csv`.
- 세션 쿠키 이름 `sra`. 로그인 성공 시 Set-Cookie, 로그아웃·401 시 삭제 쿠키.
- 모든 응답 `Cache-Control: no-store`, `X-Robots-Tag: noindex, nofollow`.
- IP 해시는 `api/_db.js` 의 `ipHash()`.
- 오류: RPC 가 `unauthorized` → 401(+쿠키 삭제), `forbidden` → 403, `rate_limited` → 429, `invalid` → 400, `not_found` → 404, `conflict|bad_transition` → 409, `db_*` → 502. 본문은 RPC 의 오류 객체 그대로.
- 파일은 500줄 이하로 나눈다: `api/admin.js`(라우터·쿠키·페이지), `api/_admin/csv.js`, `api/_admin/session.js`.

## 4. 화면 (`api/_admin/pages/login.html`, `app.html`; `assets/admin/admin.css`, `assets/admin/app.js`, `assets/admin/i18n.js`, `assets/admin/charts.js`, `assets/admin/views/*.js`)

셸: 왼쪽 세로 내비(대시보드 · 문의 · 주문 · 고객 · 구독 · 인보이스·결제 · 사용현황 · 통계 · 마케팅 · 설정), 상단에 검색·언어 토글·사용자·로그아웃, 기본 비밀번호면 붉은 띠. 반응형(모바일은 하단 탭). 표는 정렬·필터·페이지·CSV. 상세는 오른쪽 패널 또는 전체 화면. 모든 쓰기 동작은 확인 대화상자 + 결과 토스트 + 실패 이유 표시. 로딩·빈 상태·오류 상태 전부 디자인.

### 4.1 대시보드
- 기간 선택(이번 달·지난 달·최근 90일·올해·직접).
- KPI 8칸: MRR(활성 구독의 월 정가−할인, 통화별 KRW/USD 두 줄), 활성 구독 수, 이달 신규 주문, 이달 신규 문의, 문의→주문 전환율, 미수금(issued+overdue 합계, 통화별), 이달 결제 입금, 사람 손 필요한 개통 작업.
- 차트: 월별 매출(입금 기준)·주문·문의 12개월 막대/선, 나라별 리드·주문 상위 8, 플랜별 활성 구독 도넛, 언어별(ko/en) 문의.
- 할 일: 새 문의(24시간 안 응답 SLA), 확인 대기 주문(received/under_review), 연체 인보이스, needs_human 개통 작업, 오늘·지난 할 일.
- 시스템 상태: 요금표·정책 판, 알림 채널 설정 여부(API 가 env 존재 여부만 알려 줌), 마지막 사용량 집계 시각.

### 4.2 문의(리드)
목록(상태·언어·출처·나라·기간·검색), 상세(내용·UTM·페이지·동의·타임라인·메모·할 일), 상태 변경, 담당자, 다음 액션 날짜, 고객으로 전환, 스팸 표시, CSV.

### 4.3 주문
목록(상태·나라·플랜·통화·결제수단·기간·검색), 상세(주문 내용 전부·견적 스냅샷·차단 사유·이벤트 타임라인·개통 작업·메모·할 일·고객 링크), 상태 전이 버튼(허용 전이만 활성), 사유 입력, 담당자, CSV. 주문 조회 페이지 링크(`/ko/order-status.html`).

### 4.4 고객
목록(상태·나라·플랜·태그·검색), 상세(프로필·세금·구독·인보이스·결제·사용량 12개월·테넌트 연결·주문·메모·할 일·타임라인), 편집, 테넌트 연결(운영 앱 테넌트 검색), 태그, 보관.

### 4.5 구독
목록·상세, 플랜 변경(적용일), 할인 기간, 해지 예약·즉시, 일시정지·재개, 다음 청구 예정 표.

### 4.6 인보이스·결제
인보이스 목록(상태·통화·기간·고객), 생성(고객+월 → 구독 월정액 + 사용량 자동 초안, 줄 편집 가능), 발행, 입금 기록(부분 입금), 환불, 무효, 인쇄용 보기(브라우저 인쇄), 미수금 뷰, 결제 목록, CSV. 세금계산서 번호 기록 칸. 결제사(PSP) 연동은 없음을 화면에 명시("카드 결제 자동 수집은 결제사 계약 뒤 — 지금은 수동 기록").

### 4.7 사용현황
테넌트별 이번 달·지난 달 통화 수·분·대화 수·채널별, 구독 한도 대비 %(80·100% 색), 회선 풀(번호·상태·테넌트), 개통 작업(단계·상태·needs_human), 새로 고침 버튼, 월 선택, CSV.

### 4.8 통계
매출·파이프라인·마케팅·사용량·코호트·나라별 보고서 탭, 각각 차트+표+CSV.

### 4.9 마케팅
캠페인 목록·등록·편집(UTM 링크 생성기: 랜딩 URL + utm 3종 → 복사), 캠페인별 리드·주문·전환, 출처·언어·나라별 유입, 요금표 나라 목록(voice live/soon/no, 통화, 세금) 읽기.

### 4.10 설정
관리자 계정(내 비밀번호 변경, owner 면 관리자 추가·비활성·임시 비밀번호), 회사 정보, 알림 이메일, SLA, 감사 로그(필터·검색), 시스템 상태, 운영 앱 관리자 링크.

## 5. 검증 기준 (완료 정의)

1. `admin/1234` 로 로그인 → 대시보드가 실제 DB 값으로 뜬다. 틀린 비밀번호 5회 → 429. 로그아웃 뒤 `/admin` 은 302 login.
2. 로그인 없이 `/admin`, `/admin/app`, `/api/admin/list` → 각각 302·302·401. 화면 HTML 이 정적으로 열리지 않는다(`/api/_admin/pages/app.html` 404).
3. 모든 목록에 필터·정렬·페이지·CSV 가 실제로 동작(빈 결과·1행·1,000행).
4. 주문 상태 전이: 허용되지 않은 전이는 409, 허용 전이는 `order_events` 에 남고 `contract_signed` 에서 고객·구독이 생긴다. `/ko/order-status.html` 에서 같은 타임라인이 보인다.
5. 인보이스: 생성(자동 초안 금액 = 구독 정가×(1−할인) + 사용량×단가, 세율 적용) → 발행 → 부분 입금 → 완납 → 환불 상태 흐름이 맞고, 합계는 함수가 다시 계산한다. KRW 는 정수, USD 는 센트.
6. 사용량 새로 고침 결과가 `public.calls`/`chat_conversations` 직접 집계와 같다(검증 SQL 로 대조).
7. 감사 로그에 모든 쓰기가 남는다. viewer 로 쓰기 시도 → 403.
8. 화면: 데스크톱 1440·모바일 375 에서 깨짐 없음, 키보드로 모든 동작, 콘솔 오류 0, 다크/라이트 무관 대비 충분, ko/en 토글에 빈 문구 없음.
9. 보안: 비밀 없음(`grep service_role` 0), 쿠키 HttpOnly/Secure, CSRF 헤더 없으면 403, Origin 다르면 403, 오류 메시지에 스택·SQL 없음, XSS(`<script>` 넣은 회사명이 텍스트로만 보임).
10. 배포 뒤 라이브에서 1·2·3·9 를 다시 확인한다.

## 6. 파일 소유 (동시 작업 충돌 방지)

| 담당 | 파일 |
|---|---|
| DB | `supabase/admin/001_admin.sql`, `supabase/admin/002_verify.sql`(검증 쿼리) |
| API | `api/admin.js`, `api/_admin/session.js`, `api/_admin/csv.js`, `vercel.json` 의 rewrites/headers/functions 추가분 |
| UI | `api/_admin/pages/*.html`, `assets/admin/**` |
| 검증 | `build/admincheck.py`(정적 검사: 비밀·파일 크기·i18n 키 누락·라우트 제외), 브라우저 E2E |
