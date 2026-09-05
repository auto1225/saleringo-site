# -*- coding: utf-8 -*-
"""데모 대본 묶음 A — 의원·피부과, 동물병원, 요양, 학원, 대학 입학상담, 미용실, 헬스장, 설비·수리.
형식은 build/demo/validate.py 의 docstring, 본보기는 scripts_dental.py 를 따른다.
각 대본은 build/ko/trades*.py 의 같은 업종 'call' 시나리오를 8~14줄 통화로 늘린 것이고,
2장의 마지막 손님 질문은 그 업종의 'refuse' 규칙 하나를 건드려 사람에게 넘어간다."""

HONEST_KO = "각본이 있는 시연 · 예시 데이터 · 두 목소리는 이 데모를 위해 만든 합성 음성입니다 · 금액은 예시 요금표입니다."
HONEST_EN = "Scripted simulation · sample data · both voices were synthesised for this demo · figures are an example price list."
HANDOFF_KO = ["두 채널의 대화 전체", "받아 적은 항목 전부, 출처와 함께"]
HANDOFF_EN = ["The whole conversation, both channels", "Every captured field, with its source"]
SUMMARY_KO = "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 %s이 자는 동안 끝났습니다."
SUMMARY_EN = "One {call} call · four messages · what a person did: one reply. The rest happened while the owner slept."

SCRIPTS = {

 # ───────────────────────── 의원 · 피부과 ─────────────────────────
 "clinics": {
  "ko": {
   "biz": "맑은결피부과", "owner": "원장님",
   "meta": "수요일 9:18 PM · 진료 종료 후 · 가상의 피부과", "callTime": "9:18 PM", "chan": "카카오톡",
   "chapters": ["밤 9:18, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 원장님 화면"],
   "chapterSubs": ["보톡스 가격 · 첫 방문 · 목요일 상담", "상담비 질문 · 효과 질문은 사람에게", "상담 예약 · 안내 금액 · 담당 · 답변 대기"],
   "sys": {"ring": "밤 9:18 — 전화벨이 울립니다. 진료는 끝났습니다.",
           "chat": "다음 날 아침 7:52 — 같은 손님이 카카오톡으로.",
           "morning": "오전 9:00 — 원장님 화면."},
   "customer": {"name": "이서연", "phone": "010-2957-83··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 맑은결피부과입니다. 지금은 진료가 끝난 시간이지만, 상담 예약과 문의는 제가 도와드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "보톡스 시술 얼마인가요? 처음인데 아프지 않나요?",
     "side": [{"field": {"k": "문의 시술", "v": "보톡스 — 첫 방문", "src": "통화에서"}}]},
    {"who": "ai", "text": "저희 요금표 기준으로 이마와 미간은 부위당 9만원, 사각턱은 19만원부터예요. 통증이나 효과는 개인차가 있어서 전화로 말씀드리기 어렵고, 상담 때 원장님이 직접 보고 안내드립니다. 어느 부위를 생각하고 계세요?",
     "side": [{"field": {"k": "안내 금액", "v": "이마 · 미간 부위당 90,000원", "src": "원장님 요금표"}}]},
    {"who": "user", "text": "이마랑 미간이요. 상담은 언제 되나요?",
     "side": [{"field": {"k": "부위", "v": "이마 · 미간", "src": "본인 발화"}}]},
    {"who": "ai", "text": "이번 주 목요일 오후 3시에 상담 자리가 있어요. 그때로 잡아 드릴까요?"},
    {"who": "user", "text": "네, 그때로 할게요."},
    {"who": "ai", "text": "성함과 연락처를 말씀해 주시겠어요?"},
    {"who": "user", "text": "이서연이고요, 010-2957-8314예요.",
     "side": [{"field": {"k": "이름", "v": "이서연", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-2957-83··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "이서연 님, 목요일 오후 3시 상담 예약되었습니다. 첫 방문이시니 신분증만 챙겨 오시면 되고, 확인 문자를 지금 보내 드릴게요. 문자로 안내드려도 괜찮으세요? 그리고 저희는 어떻게 알고 연락 주셨어요?",
     "side": [{"field": {"k": "상담 예약", "v": "목 15:00 · 첫 상담", "src": "캘린더의 빈 시간"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "상담 예약 확정", "v": "목 15:00 · 캘린더에 들어감 · 확인 문자 발송"}}]},
    {"who": "user", "text": "네, 문자 괜찮아요. 검색해서 찾았어요.",
     "side": [{"field": {"k": "연락 수단", "v": "문자 — 동의함", "src": "본인 발화"}}, {"field": {"k": "유입 경로", "v": "검색", "src": "본인 발화"}}]},
    {"who": "ai", "text": "감사합니다. 목요일에 뵙겠습니다. 편안한 밤 되세요.",
     "side": [{"work": {"icon": "#", "k": "안내 금액 카드", "v": "이마 · 미간 부위당 90,000원 — 원장님 요금표에서"}},
              {"work": {"icon": "@", "k": "담당·기한", "v": "데스크 담당 배정 · 목 14:30까지 첫 방문 차트 준비"}},
              {"work": {"icon": "↻", "k": "후속 문자", "v": "무응답 시 D+2 안내 문자 초안 — 발송 전 원장님 확인"}}]}
   ],
   "chat": [
    {"who": "user", "when": "7:52 AM", "text": "어제 목요일 상담 예약한 이서연인데요, 상담비가 따로 있나요?"},
    {"who": "ai", "when": "+2 sec", "text": "첫 상담은 무료입니다. 목요일 오후 3시 예약은 그대로 유효해요.", "merge": True},
    {"who": "user", "when": "7:53 AM", "text": "제 피부엔 보톡스가 확실히 효과 있을까요? 부작용은 없죠?"},
    {"who": "ai", "when": "+2 sec", "text": "효과와 부작용은 개인차가 있어서 제가 답할 수 없는 부분이에요. 대화 내용을 원장님께 전달해 두었고, 오전 중에 데스크에서 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 효과와 부작용은 개인차가 있는 판단이지 요금표에 있는 사실이 아닙니다"],
   "morning": [
    {"icon": "✓", "k": "새 상담 예약 1건", "v": "이서연 · 목 15:00 · 첫 방문 · 캘린더에 있음"},
    {"icon": "#", "k": "안내 금액", "v": "이마 · 미간 부위당 90,000원 · 문자로 발송됨 · 열람 확인"},
    {"icon": "@", "k": "데스크 할 일", "v": "목 14:30까지 첫 방문 차트 준비 · 담당 한지원"},
    {"icon": "!", "k": "답변 대기 1건", "v": "효과 · 부작용 문의 · 대화 전체 첨부 · 담당 원장님"}
   ],
   "person": {"when": "9:12 AM", "text": "데스크 한지원입니다. 이서연 님, 효과와 부작용은 피부 상태에 따라 달라서 목요일 상담에서 원장님이 직접 보고 설명드릴 거예요. 궁금한 점을 적어 오시면 좋아요."},
   "summary": SUMMARY_KO % "원장님",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Clearline Dermatology", "owner": "the owner",
   "meta": "Wednesday 9:18 PM · after hours · a fictional clinic", "callTime": "9:18 PM", "chan": "WhatsApp",
   "chapters": ["9:18 PM, the call", "Next morning, WhatsApp", "9:00 AM, the owner’s screen"],
   "chapterSubs": ["Botox price · first visit · Thursday consult", "consult fee · the results question goes to a person", "consult · quoted price · owner · one reply waiting"],
   "sys": {"ring": "9:18 PM — the phone rings. The clinic closed hours ago.",
           "chat": "Next morning, 7:52 AM — the same customer, on WhatsApp.",
           "morning": "9:00 AM — the owner’s screen."},
   "customer": {"name": "Seoyeon Lee", "phone": "555-03··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Clearline Dermatology. We're closed for the night, but I can book consultations and answer questions. How can I help?"},
    {"who": "user", "text": "How much is Botox? It's my first time — does it hurt?",
     "side": [{"field": {"k": "Request", "v": "Botox — first visit", "src": "from the call"}}]},
    {"who": "ai", "text": "From our price list, the forehead and frown lines are one hundred ninety dollars per area, and the jawline starts at three hundred ninety. Pain and results vary from person to person, so I can't speak to those — the doctor goes through them with you at the consultation. Which area are you thinking of?",
     "side": [{"field": {"k": "Quote", "v": "Forehead · frown lines $190 per area", "src": "your price list"}}]},
    {"who": "user", "text": "Forehead and frown lines. When could I come in?",
     "side": [{"field": {"k": "Area", "v": "forehead · frown lines", "src": "caller said it"}}]},
    {"who": "ai", "text": "I have a consultation slot this Thursday at three PM. Shall I book that for you?"},
    {"who": "user", "text": "Yes, let's do that."},
    {"who": "ai", "text": "Can I get your name and a mobile number?"},
    {"who": "user", "text": "Seoyeon Lee, five five five, zero three one four.",
     "side": [{"field": {"k": "Name", "v": "Seoyeon Lee", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-03··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, Seoyeon. You're booked for Thursday at three. Since it's your first visit, just bring a photo ID. I'll text you a confirmation now — is text okay? And how did you find us?",
     "side": [{"field": {"k": "Consult", "v": "Thu 3:00 PM · first visit", "src": "free in your calendar"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "Consult booked", "v": "Thu 3:00 PM · in your calendar · confirmation text sent"}}]},
    {"who": "user", "text": "Text is fine. I found you on a search.",
     "side": [{"field": {"k": "Contact consent", "v": "text — agreed", "src": "caller said it"}}, {"field": {"k": "Source", "v": "search", "src": "caller said it"}}]},
    {"who": "ai", "text": "Thank you. We'll see you Thursday. Have a good night.",
     "side": [{"work": {"icon": "#", "k": "Quote card", "v": "Forehead · frown lines $190 per area — from your own price list"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "assigned to the desk · new-patient chart ready by Thu 2:30"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "D+2 nudge drafted — you approve before it sends"}}]}
   ],
   "chat": [
    {"who": "user", "when": "7:52 AM", "text": "Hi, Seoyeon Lee from last night — is there a fee for the consultation?"},
    {"who": "ai", "when": "+2 sec", "text": "The first consultation is free. Your Thursday 3:00 PM booking is unchanged.", "merge": True},
    {"who": "user", "when": "7:53 AM", "text": "Will Botox definitely work on my skin? No side effects, right?"},
    {"who": "ai", "when": "+2 sec", "text": "Results and side effects vary by person, so that's not something I can answer. I've passed our conversation to the doctor — the desk will reply this morning.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: results and side effects are a clinical judgement, not a fact on the price list"],
   "morning": [
    {"icon": "✓", "k": "New consultation", "v": "Seoyeon Lee · Thu 3:00 PM · first visit · in the calendar"},
    {"icon": "#", "k": "Quote", "v": "$190 per area · sent by text · opened"},
    {"icon": "@", "k": "Desk task", "v": "new-patient chart ready by Thu 2:30 · owner: Jiwon"},
    {"icon": "!", "k": "Waiting for a person", "v": "results and side-effects question · full thread attached · owner: the doctor"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Jiwon from the front desk. Hi Seoyeon — results depend on your skin, so the doctor will look and talk it through with you on Thursday. Bring any questions you have."},
   "summary": SUMMARY_EN,
   "honest": HONEST_EN
  }
 },

 # ───────────────────────── 동물병원 ─────────────────────────
 "veterinary": {
  "ko": {
   "biz": "하늘동물병원", "owner": "원장님",
   "meta": "금요일 10:51 PM · 진료 종료 후 · 가상의 동물병원", "callTime": "10:51 PM", "chan": "카카오톡",
   "chapters": ["밤 10:51, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 원장님 화면"],
   "chapterSubs": ["초콜릿 먹은 강아지 · 응급 분류 · 즉시 연결", "재진 예약 · 약 질문은 사람에게", "연결 기록 · 재진 · 담당 · 답변 대기"],
   "sys": {"ring": "밤 10:51 — 전화벨이 울립니다. 진료는 끝났습니다.",
           "chat": "다음 날 아침 7:35 — 같은 보호자가 카카오톡으로.",
           "morning": "오전 9:00 — 원장님 화면."},
   "customer": {"name": "정하늘", "phone": "010-5528-76··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 하늘동물병원입니다. 지금은 진료가 끝난 시간인데, 급한 일이면 바로 도와드릴게요. 무슨 일이세요?"},
    {"who": "user", "text": "강아지가 초콜릿을 먹은 것 같아요. 어떻게 해야 하나요?",
     "side": [{"field": {"k": "증상", "v": "초콜릿 섭취 의심 · 10:51 PM", "src": "통화에서 · 진단 아님"}}]},
    {"who": "ai", "text": "초콜릿 섭취는 응급 상황일 수 있어요. 예약을 잡는 대신 지금 바로 야간 진료 담당 선생님께 연결해 드릴게요. 먹은 양과 시간, 체중을 기억해 두시고, 억지로 토하게 하지는 마세요.",
     "side": [{"field": {"k": "응급 분류", "v": "응급 — 중독 표현 · 예약 대신 즉시 연결", "src": "원장님 규칙"}},
              {"work": {"icon": "✓", "k": "응급 분류", "v": "중독 표현 감지 · 야간 담당 호출 시작"}}]},
    {"who": "user", "text": "네, 부탁드려요. 한 시간쯤 전에 초콜릿 반 개 정도 먹었고, 5킬로 정도 나가요.",
     "side": [{"field": {"k": "섭취량 · 시각", "v": "초콜릿 반 개 · 약 1시간 전", "src": "본인 발화 · 진단 아님"}},
              {"field": {"k": "반려동물", "v": "개 · 약 5kg", "src": "본인 발화"}}]},
    {"who": "ai", "text": "알겠어요. 연결하기 전에 성함과 지금 쓰시는 번호만 말씀해 주세요. 끊기면 담당 선생님이 바로 다시 걸 수 있게요."},
    {"who": "user", "text": "정하늘이고요, 010-5528-7612예요. 강아지 이름은 콩이예요.",
     "side": [{"field": {"k": "보호자", "v": "정하늘", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-5528-76··", "src": "발신번호와 일치"}},
              {"field": {"k": "반려동물 이름", "v": "콩이", "src": "본인 발화"}}, {"crm": True}]},
    {"who": "ai", "text": "정하늘 님, 콩이 기록에 지금 내용을 남겼고 야간 담당 선생님께 그대로 전달했어요. 이제 연결합니다. 잠시만 기다려 주세요.",
     "side": [{"work": {"icon": "@", "k": "야간 담당 연결", "v": "10:52 PM · 박수진 원장 · 통화 내용 전달됨"}},
              {"work": {"icon": "#", "k": "응급 기록", "v": "섭취량 · 시각 · 체중 — 보호자 말 그대로, 진단 없음"}},
              {"work": {"icon": "↻", "k": "후속 문자", "v": "다음 날 아침 안부 문자 초안 — 발송 전 원장님 확인"}}]},
    {"who": "user", "text": "네, 감사합니다."},
    {"who": "ai", "text": "연결할게요. 콩이 잘 보살펴 주세요."}
   ],
   "chat": [
    {"who": "user", "when": "7:35 AM", "text": "어젯밤 콩이 보호자 정하늘이에요. 야간병원 다녀왔고 지금은 괜찮아요. 오늘 한 번 더 봐 주실 수 있나요?"},
    {"who": "ai", "when": "+2 sec", "text": "다행이에요. 오늘 오전 11시에 원장님 진료 자리가 있어 콩이 이름으로 잡아 두었어요. 어젯밤 기록은 이미 차트에 있습니다.", "merge": True},
    {"who": "user", "when": "7:36 AM", "text": "집에 사람 먹는 위장약이 있는데 조금 먹여도 될까요?"},
    {"who": "ai", "when": "+2 sec", "text": "약이나 용량은 제가 안내할 수 없는 부분이에요. 원장님께 바로 전달해 두었고, 진료 전에 병원에서 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 약과 용량은 수의사의 판단이지 차트에 있는 사실이 아닙니다"],
   "morning": [
    {"icon": "✓", "k": "새 예약 1건", "v": "콩이 · 오늘 11:00 · 재진 · 캘린더에 있음"},
    {"icon": "#", "k": "응급 기록", "v": "어젯밤 10:52 PM 야간 담당 연결 · 섭취량 · 시각 · 체중 기록됨"},
    {"icon": "@", "k": "원장님 할 일", "v": "11:00 전 어젯밤 기록 확인 · 담당 박수진 원장"},
    {"icon": "!", "k": "답변 대기 1건", "v": "투약 문의 · 대화 전체 첨부 · 담당 박수진 원장"}
   ],
   "person": {"when": "9:05 AM", "text": "원장 박수진입니다. 정하늘 님, 사람 약은 절대 먹이지 마시고 물만 조금씩 주세요. 11시에 콩이 보고 바로 말씀드릴게요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 야간 진료와 답장 한 줄. 급한 것은 즉시 사람에게, 나머지는 원장님이 자는 동안 정리됐습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Skyline Veterinary", "owner": "the owner",
   "meta": "Friday 10:51 PM · after hours · a fictional practice", "callTime": "10:51 PM", "chan": "WhatsApp",
   "chapters": ["10:51 PM, the call", "Next morning, WhatsApp", "9:00 AM, the owner’s screen"],
   "chapterSubs": ["dog ate chocolate · triaged · routed at once", "recheck booked · the medication question goes to a person", "routing record · recheck · owner · one reply waiting"],
   "sys": {"ring": "10:51 PM — the phone rings. The practice closed hours ago.",
           "chat": "Next morning, 7:35 AM — the same owner, on WhatsApp.",
           "morning": "9:00 AM — the owner’s screen."},
   "customer": {"name": "Haneul Jung", "phone": "555-07··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Skyline Veterinary. We're closed for the night, but if this is urgent I can help right away. What's going on?"},
    {"who": "user", "text": "I think my dog ate some chocolate. What should I do?",
     "side": [{"field": {"k": "Symptom", "v": "suspected chocolate ingestion · 10:51 PM", "src": "from the call · not a diagnosis"}}]},
    {"who": "ai", "text": "Chocolate can be an emergency, so I won't book an appointment — I'm connecting you to our on-call vet right now. Try to remember how much he ate, when, and his weight, and please don't make him vomit.",
     "side": [{"field": {"k": "Triage", "v": "emergency — poisoning keyword · route, don't book", "src": "your rule"}},
              {"work": {"icon": "✓", "k": "Triaged", "v": "poisoning keyword detected · on-call vet paged"}}]},
    {"who": "user", "text": "Okay, please. About half a bar, an hour ago. He's around eleven pounds.",
     "side": [{"field": {"k": "Amount · time", "v": "half a bar · about 1 hour ago", "src": "caller said it · not a diagnosis"}},
              {"field": {"k": "Pet", "v": "dog · about 11 lb", "src": "caller said it"}}]},
    {"who": "ai", "text": "Got it. Before I connect you, can I have your name and the number you're on, so the vet can call you straight back if we drop?"},
    {"who": "user", "text": "Haneul Jung, five five five, zero seven one two. The dog's name is Bean.",
     "side": [{"field": {"k": "Owner", "v": "Haneul Jung", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-07··", "src": "matches caller ID"}},
              {"field": {"k": "Pet name", "v": "Bean", "src": "caller said it"}}, {"crm": True}]},
    {"who": "ai", "text": "Thank you, Haneul. I've noted all of this on Bean's record and passed it to the on-call vet word for word. Connecting you now — one moment.",
     "side": [{"work": {"icon": "@", "k": "On-call vet", "v": "10:52 PM · Dr Sujin Park · call notes handed over"}},
              {"work": {"icon": "#", "k": "Emergency record", "v": "amount · time · weight — the owner's words, no diagnosis"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "next-morning check-in text drafted — you approve before it sends"}}]},
    {"who": "user", "text": "Okay, thank you."},
    {"who": "ai", "text": "Connecting you. Take care of Bean."}
   ],
   "chat": [
    {"who": "user", "when": "7:35 AM", "text": "Hi, Haneul Jung, Bean's owner from last night. We went to the night clinic and he's okay now. Could someone see him again today?"},
    {"who": "ai", "when": "+2 sec", "text": "That's a relief. The doctor has an opening at eleven this morning — I've booked it under Bean. Last night's notes are already on his chart.", "merge": True},
    {"who": "user", "when": "7:36 AM", "text": "I have some human stomach medicine at home — can I give him a little?"},
    {"who": "ai", "when": "+2 sec", "text": "Medication and doses aren't something I can advise on. I've passed this straight to the doctor, and the clinic will contact you before your visit.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: medication and dosing are the vet's call, not a fact on the chart"],
   "morning": [
    {"icon": "✓", "k": "New booking", "v": "Bean · today 11:00 · recheck · in the calendar"},
    {"icon": "#", "k": "Emergency record", "v": "10:52 PM · routed to the on-call vet · amount, time, weight on file"},
    {"icon": "@", "k": "Doctor's task", "v": "review last night's notes before 11:00 · owner: Dr Sujin Park"},
    {"icon": "!", "k": "Waiting for a person", "v": "medication question · full thread attached · owner: Dr Sujin Park"}
   ],
   "person": {"when": "9:05 AM", "text": "This is Dr Sujin Park. Haneul — please don't give Bean any human medicine, just small sips of water. I'll see him at eleven and tell you straight away."},
   "summary": "One {call} call · four messages · what people did: the night visit and one reply. The urgent part went to a person at once; the rest was sorted while the owner slept.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────── 요양 ─────────────────────────
 "senior-care": {
  "ko": {
   "biz": "늘봄주간보호센터", "owner": "원장님",
   "meta": "월요일 8:12 PM · 상담 시간 종료 후 · 가상의 주간보호센터", "callTime": "8:12 PM", "chan": "카카오톡",
   "chapters": ["저녁 8:12, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 원장님 화면"],
   "chapterSubs": ["3등급 아버지 · 주간보호 · 내일 상담 전화", "휠체어 차량 질문 · 자리 질문은 사람에게", "상담 예약 · 어르신 카드 · 담당 · 답변 대기"],
   "sys": {"ring": "저녁 8:12 — 전화벨이 울립니다. 상담 시간은 끝났습니다.",
           "chat": "다음 날 아침 7:48 — 같은 보호자가 카카오톡으로.",
           "morning": "오전 9:00 — 원장님 화면."},
   "customer": {"name": "최은정", "phone": "010-8164-29··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 늘봄주간보호센터입니다. 상담 시간은 끝났지만, 문의는 제가 받아 두고 내일 상담 선생님께 그대로 이어 드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "아버지 요양등급 3등급 나왔는데, 주간보호 하루 얼마나 드나요?",
     "side": [{"field": {"k": "문의", "v": "주간보호 — 아버지 · 3등급", "src": "통화에서"}}]},
    {"who": "ai", "text": "3등급이시면 주간보호 이용이 가능해요. 다만 본인부담금은 등급과 소득 구간에 따라 건강보험공단에서 정하는 거라, 저희가 임의로 계산해 드릴 수는 없어요. 바로 말씀드릴 수 있는 건 이용 시간이 아침 9시부터 오후 5시까지이고, 점심과 간식은 하루 4천원, 차량 운행이 있다는 점이에요.",
     "side": [{"field": {"k": "요양등급", "v": "3등급", "src": "본인 발화"}},
              {"field": {"k": "본인부담금", "v": "공단이 정함 — 계산하지 않음", "src": "원장님 규칙"}},
              {"field": {"k": "안내 금액", "v": "식대 · 간식 하루 4,000원", "src": "원장님 요금표"}}]},
    {"who": "user", "text": "차량은 어디까지 오나요? 저희는 상록동이에요.",
     "side": [{"field": {"k": "차량 지역", "v": "상록동", "src": "본인 발화"}}]},
    {"who": "ai", "text": "상록동은 차량 운행 지역이에요. 자세한 시간과 이용 방법은 상담 선생님이 내일 오전 중에 전화드려도 될까요?"},
    {"who": "user", "text": "네, 오전에 부탁드립니다."},
    {"who": "ai", "text": "내일 오전 10시로 전화 상담을 잡아 둘게요. 보호자분 성함과 연락처, 어르신과의 관계를 말씀해 주시겠어요?",
     "side": [{"field": {"k": "상담 예약", "v": "내일 10:00 · 전화 상담", "src": "캘린더의 빈 시간"}}]},
    {"who": "user", "text": "딸 최은정이고요, 010-8164-2907이에요.",
     "side": [{"field": {"k": "보호자", "v": "최은정 · 딸", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-8164-29··", "src": "발신번호와 일치"}}, {"crm": True}]},
    {"who": "ai", "text": "최은정 님, 내일 오전 10시에 상담 선생님이 전화드릴게요. 어르신 성함과 연세, 등급 판정일을 미리 알려 주시면 상담이 빨라져요. 본인부담금 구간은 건강보험공단에서도 확인하실 수 있어요.",
     "side": [{"work": {"icon": "✓", "k": "상담 예약 확정", "v": "내일 10:00 전화 · 캘린더에 들어감 · 확인 문자 발송"}},
              {"field": {"k": "공단 안내", "v": "안내함", "src": "원장님 규칙"}}]},
    {"who": "user", "text": "아버지는 최영호, 여든둘이시고 지난주에 판정 나왔어요. 감사합니다.",
     "side": [{"field": {"k": "어르신", "v": "최영호 · 82세 · 3등급 · 판정 지난주", "src": "본인 발화"}}]},
    {"who": "ai", "text": "네, 그대로 적어 두었어요. 내일 오전에 연락드릴게요. 편안한 밤 되세요.",
     "side": [{"work": {"icon": "@", "k": "담당·기한", "v": "상담 담당 김미라 · 내일 10:00 전화"}},
              {"work": {"icon": "#", "k": "어르신 카드", "v": "최영호 · 82세 · 3등급 · 상록동 차량 — 보호자 말 그대로"}},
              {"work": {"icon": "↻", "k": "후속 문자", "v": "상담 뒤 방문 상담 안내 문자 초안 — 발송 전 원장님 확인"}}]}
   ],
   "chat": [
    {"who": "user", "when": "7:48 AM", "text": "어제 전화드린 최은정입니다. 아버지가 걷는 게 불편하신데 휠체어로도 차량 이용이 되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "네, 휠체어 리프트가 있는 차량이 있어요. 오늘 10시 상담 전화는 그대로 진행됩니다.", "merge": True},
    {"who": "user", "when": "7:49 AM", "text": "그럼 다음 주부터 바로 다닐 수 있을까요? 자리 있나요?"},
    {"who": "ai", "when": "+2 sec", "text": "정원과 대기 상황은 매일 바뀌어서 제가 확답드릴 수 없어요. 원장님이 확인해서 10시 상담 때 바로 말씀드리도록 전달해 두었어요.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 정원과 대기 순서는 실시간으로 바뀌는 것이라 확인한 사람만 답할 수 있습니다"],
   "morning": [
    {"icon": "✓", "k": "새 상담 1건", "v": "최은정 · 오늘 10:00 전화 상담 · 캘린더에 있음"},
    {"icon": "#", "k": "어르신 카드", "v": "최영호 · 82세 · 3등급 · 상록동 차량 · 판정 지난주"},
    {"icon": "@", "k": "상담 할 일", "v": "10:00 전화 · 이용 시간과 차량 안내 · 담당 김미라"},
    {"icon": "!", "k": "답변 대기 1건", "v": "다음 주 자리 문의 · 정원 확인 필요 · 담당 원장님"}
   ],
   "person": {"when": "9:20 AM", "text": "상담 담당 김미라입니다. 최은정 님, 다음 주 자리는 원장님이 확인하셨고 한 자리 여유가 있어요. 10시 통화 때 아버님 이야기 자세히 듣고 안내드릴게요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 상담은 사람이 하고, 그 전까지의 정리는 원장님이 자는 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Willowbrook Day Center", "owner": "the owner",
   "meta": "Monday 8:12 PM · after hours · a fictional day center", "callTime": "8:12 PM", "chan": "WhatsApp",
   "chapters": ["8:12 PM, the call", "Next morning, WhatsApp", "9:00 AM, the owner’s screen"],
   "chapterSubs": ["father at level three · day care · advisor call tomorrow", "wheelchair van · the place question goes to a person", "advisor call · resident card · owner · one reply waiting"],
   "sys": {"ring": "8:12 PM — the phone rings. The office closed hours ago.",
           "chat": "Next morning, 7:48 AM — the same daughter, on WhatsApp.",
           "morning": "9:00 AM — the owner’s screen."},
   "customer": {"name": "Eunjung Choi", "phone": "555-02··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Willowbrook Day Center. Our office is closed for the evening, but I can take your questions and pass them straight to our care advisor for the morning. How can I help?"},
    {"who": "user", "text": "My father's just been assessed at care level three. What does day care cost per day?",
     "side": [{"field": {"k": "Enquiry", "v": "day care — father · level 3", "src": "from the call"}}]},
    {"who": "ai", "text": "At level three he's eligible for our day program. How much his benefits cover depends on his level and income band — the funding office sets that, so I can't work out his share. What I can tell you: the day runs nine to five, lunch and snacks are five dollars a day, and we run a pickup van.",
     "side": [{"field": {"k": "Care level", "v": "level 3", "src": "caller said it"}},
              {"field": {"k": "Co-payment", "v": "set by the funding office — not calculated", "src": "your rule"}},
              {"field": {"k": "Quote", "v": "lunch · snacks $5 a day", "src": "your price list"}}]},
    {"who": "user", "text": "How far does the van go? We're in Riverside.",
     "side": [{"field": {"k": "Van area", "v": "Riverside", "src": "caller said it"}}]},
    {"who": "ai", "text": "Riverside is on the van route. For times and how it all works, could our care advisor call you tomorrow morning?"},
    {"who": "user", "text": "Yes, please — the morning is good."},
    {"who": "ai", "text": "I'll set the call for ten tomorrow morning. Can I get your name, a number, and how you're related to him?",
     "side": [{"field": {"k": "Advisor call", "v": "tomorrow 10:00 · phone", "src": "free in your calendar"}}]},
    {"who": "user", "text": "I'm his daughter, Eunjung Choi. Five five five, zero two nine oh seven.",
     "side": [{"field": {"k": "Contact", "v": "Eunjung Choi · daughter", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-02··", "src": "matches caller ID"}}, {"crm": True}]},
    {"who": "ai", "text": "Thank you, Eunjung. Our advisor will call you at ten tomorrow. His name, age and assessment date would speed things up, and the funding office can confirm his share if you'd like to check.",
     "side": [{"work": {"icon": "✓", "k": "Call booked", "v": "tomorrow 10:00 · in your calendar · confirmation text sent"}},
              {"field": {"k": "Funding office", "v": "mentioned", "src": "your rule"}}]},
    {"who": "user", "text": "He's Youngho Choi, eighty-two, and the assessment came through last week. Thank you.",
     "side": [{"field": {"k": "Resident", "v": "Youngho Choi · 82 · level 3 · assessed last week", "src": "caller said it"}}]},
    {"who": "ai", "text": "I've noted all of that. We'll speak tomorrow morning. Have a good night.",
     "side": [{"work": {"icon": "@", "k": "Owner & due", "v": "care advisor Mira · call tomorrow 10:00"}},
              {"work": {"icon": "#", "k": "Resident card", "v": "Youngho Choi · 82 · level 3 · Riverside van — the daughter's words"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "show-round invitation drafted for after the call — you approve before it sends"}}]}
   ],
   "chat": [
    {"who": "user", "when": "7:48 AM", "text": "Hi, Eunjung Choi from last night. My father has trouble walking — can the van take a wheelchair?"},
    {"who": "ai", "when": "+2 sec", "text": "Yes — one of our vans has a wheelchair lift. Your ten o'clock call today is unchanged.", "merge": True},
    {"who": "user", "when": "7:49 AM", "text": "Then could he start next week? Do you have a place?"},
    {"who": "ai", "when": "+2 sec", "text": "Places and the waiting list change daily, so that's not something I can confirm. I've asked the owner to check, so you'll have the answer on the ten o'clock call.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: places and the waiting list change in real time — only a person who has checked can answer"],
   "morning": [
    {"icon": "✓", "k": "New enquiry", "v": "Eunjung Choi · call today 10:00 · in the calendar"},
    {"icon": "#", "k": "Resident card", "v": "Youngho Choi · 82 · level 3 · Riverside van route · assessed last week"},
    {"icon": "@", "k": "Advisor task", "v": "10:00 call · hours and van details · owner: Mira"},
    {"icon": "!", "k": "Waiting for a person", "v": "place next week · capacity to confirm · owner: the owner"}
   ],
   "person": {"when": "9:20 AM", "text": "This is Mira, the care advisor. Hi Eunjung — the owner has checked and there is one place open next week. I'll go through everything with you on our ten o'clock call."},
   "summary": "One {call} call · four messages · what a person did: one reply. The consultation stays with a person; everything before it was ready while the owner slept.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────── 학원 ─────────────────────────
 "academies": {
  "ko": {
   "biz": "한빛수학학원", "owner": "원장님",
   "meta": "월요일 10:34 PM · 수업 종료 후 · 가상의 학원", "callTime": "10:34 PM", "chan": "카카오톡",
   "chapters": ["밤 10:34, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 원장님 화면"],
   "chapterSubs": ["중2 수학 · 교습비 · 토요일 레벨테스트", "준비물 질문 · 심화반 질문은 사람에게", "테스트 예약 · 교습비 · 담당 · 답변 대기"],
   "sys": {"ring": "밤 10:34 — 전화벨이 울립니다. 수업은 끝났습니다.",
           "chat": "다음 날 아침 7:55 — 같은 학부모가 카카오톡으로.",
           "morning": "오전 9:00 — 원장님 화면."},
   "customer": {"name": "윤미래", "phone": "010-3391-74··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 한빛수학학원입니다. 지금은 수업이 끝난 시간이지만, 상담과 레벨테스트 예약은 제가 도와드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "중2 아이인데 수학 반이 어떻게 되나요? 레벨테스트는 언제 보나요?",
     "side": [{"field": {"k": "학생", "v": "중2 · 수학", "src": "통화에서"}}]},
    {"who": "ai", "text": "중등부는 학교 진도반과 심화반으로 나뉘고, 반 배정은 레벨테스트 결과로 정해요. 테스트는 평일 오후 4시와 토요일 오전 10시에 있고 30분 걸립니다. 이번 주 토요일 자리가 남아 있어요.",
     "side": [{"field": {"k": "문의한 반", "v": "진도반 · 심화반 — 배정은 테스트 후", "src": "통화에서"}},
              {"field": {"k": "테스트 시간", "v": "평일 16:00 · 토 10:00 · 30분", "src": "캘린더의 빈 시간"}}]},
    {"who": "user", "text": "토요일 10시로 부탁드려요. 수강료도 알 수 있을까요?"},
    {"who": "ai", "text": "중등 수학 주 3회는 월 34만원이에요. 교재비는 별도이고 학기마다 따로 안내드려요. 예약을 위해 학부모님 성함과 연락처, 학생 이름을 말씀해 주시겠어요?",
     "side": [{"field": {"k": "안내한 교습비", "v": "주 3회 월 340,000원 · 교재비 별도", "src": "원장님 요금표"}}]},
    {"who": "user", "text": "윤미래고요, 010-3391-7420이에요. 아이는 윤지호예요.",
     "side": [{"field": {"k": "학부모", "v": "윤미래", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-3391-74··", "src": "발신번호와 일치"}},
              {"field": {"k": "학생 이름", "v": "윤지호", "src": "본인 발화"}}, {"crm": True}]},
    {"who": "ai", "text": "윤미래 님, 지호 학생 토요일 오전 10시 레벨테스트 예약되었습니다. 확인 문자를 지금 보내 드릴게요. 혹시 함께 다닐 형제나 자매도 있으세요?",
     "side": [{"field": {"k": "테스트 예약", "v": "토 10:00", "src": "캘린더의 빈 시간"}},
              {"work": {"icon": "✓", "k": "레벨테스트 확정", "v": "토 10:00 · 캘린더에 들어감 · 확인 문자 발송"}}]},
    {"who": "user", "text": "아뇨, 지호 혼자예요. 원장님하고 통화는 언제 가능할까요?",
     "side": [{"field": {"k": "형제 · 자매", "v": "없음", "src": "본인 발화"}}]},
    {"who": "ai", "text": "원장님이 내일 중에 한 번 연락드릴 거예요. 어느 시간대가 편하세요?"},
    {"who": "user", "text": "저녁 6시 이후요.",
     "side": [{"field": {"k": "연락 가능 시간", "v": "내일 18:00 이후", "src": "본인 발화"}}]},
    {"who": "ai", "text": "내일 저녁 6시 이후로 남겨 둘게요. 토요일에 뵙겠습니다. 편안한 밤 되세요.",
     "side": [{"work": {"icon": "@", "k": "담당·기한", "v": "원장님 회신 전화 · 내일 18:00 이후"}},
              {"work": {"icon": "#", "k": "교습비 카드", "v": "주 3회 월 340,000원 · 교재비 별도 — 원장님 요금표에서"}},
              {"work": {"icon": "↻", "k": "리마인드", "v": "테스트 전날 안내 문자 초안 — 발송 전 원장님 확인"}}]}
   ],
   "chat": [
    {"who": "user", "when": "7:55 AM", "text": "어제 예약한 윤미래예요. 토요일 테스트에 아이가 준비할 게 있나요?"},
    {"who": "ai", "when": "+2 sec", "text": "필기구만 있으면 돼요. 시험지는 학원에서 준비하고, 끝나면 바로 결과 상담이 있어요. 토요일 10시 예약은 그대로예요.", "merge": True},
    {"who": "user", "when": "7:56 AM", "text": "지호가 학교 수학은 90점대인데, 심화반 들어갈 수 있을까요?"},
    {"who": "ai", "when": "+2 sec", "text": "반 배정은 테스트 결과를 보고 원장님이 정하는 부분이라 제가 미리 말씀드릴 수 없어요. 대화 내용을 원장님께 전달해 두었고, 오늘 저녁 6시 이후 통화 때 말씀드릴 거예요.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 반 배정은 테스트 결과로 원장님이 하는 판단이지 미리 말할 수 있는 사실이 아닙니다"],
   "morning": [
    {"icon": "✓", "k": "새 레벨테스트 1건", "v": "윤지호 · 중2 · 토 10:00 · 캘린더에 있음"},
    {"icon": "#", "k": "안내 교습비", "v": "주 3회 월 340,000원 · 교재비 별도 · 문자로 발송됨 · 열람 확인"},
    {"icon": "@", "k": "원장님 할 일", "v": "오늘 18:00 이후 학부모 회신 전화 · 담당 원장 강수현"},
    {"icon": "!", "k": "답변 대기 1건", "v": "심화반 가능 여부 · 대화 전체 첨부 · 담당 원장 강수현"}
   ],
   "person": {"when": "9:10 AM", "text": "원장 강수현입니다. 윤미래 님, 심화반 여부는 토요일 테스트를 보고 정확히 말씀드릴게요. 저녁 6시 넘어서 전화드리겠습니다."},
   "summary": SUMMARY_KO % "원장님",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Cedar Hill Math Academy", "owner": "the owner",
   "meta": "Monday 10:34 PM · after hours · a fictional academy", "callTime": "10:34 PM", "chan": "WhatsApp",
   "chapters": ["10:34 PM, the call", "Next morning, WhatsApp", "9:00 AM, the owner’s screen"],
   "chapterSubs": ["eighth-grade math · tuition · Saturday placement test", "what to bring · the advanced-class question goes to a person", "test booked · tuition · owner · one reply waiting"],
   "sys": {"ring": "10:34 PM — the phone rings. The last class ended hours ago.",
           "chat": "Next morning, 7:55 AM — the same parent, on WhatsApp.",
           "morning": "9:00 AM — the owner’s screen."},
   "customer": {"name": "Mirae Yoon", "phone": "555-07··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Cedar Hill Math Academy. Classes are over for the day, but I can answer questions and book a placement test. How can I help?"},
    {"who": "user", "text": "My son's in eighth grade. How are your math classes set up, and when's the placement test?",
     "side": [{"field": {"k": "Student", "v": "grade 8 · math", "src": "from the call"}}]},
    {"who": "ai", "text": "Middle school has a school-track class and an advanced class, and placement is decided by the test. Tests run weekdays at four and Saturdays at ten, and take thirty minutes. This Saturday still has room.",
     "side": [{"field": {"k": "Class asked about", "v": "school-track · advanced — placed after the test", "src": "from the call"}},
              {"field": {"k": "Test times", "v": "weekdays 4:00 · Sat 10:00 · 30 min", "src": "free in your calendar"}}]},
    {"who": "user", "text": "Saturday at ten, please. And what's the tuition?"},
    {"who": "ai", "text": "Middle school math, three sessions a week, is three hundred forty dollars a month. Books are extra and quoted each term. For the booking, can I get your name, a number, and the student's name?",
     "side": [{"field": {"k": "Tuition quoted", "v": "3 sessions a week $340 a month · books extra", "src": "your price list"}}]},
    {"who": "user", "text": "Mirae Yoon, five five five, zero seven four two. My son is Jiho.",
     "side": [{"field": {"k": "Parent", "v": "Mirae Yoon", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-07··", "src": "matches caller ID"}},
              {"field": {"k": "Student name", "v": "Jiho Yoon", "src": "caller said it"}}, {"crm": True}]},
    {"who": "ai", "text": "Thank you, Mirae. Jiho is booked for the placement test Saturday at ten — I'm texting you a confirmation now. Any siblings who might join too?",
     "side": [{"field": {"k": "Test slot", "v": "Sat 10:00", "src": "free in your calendar"}},
              {"work": {"icon": "✓", "k": "Test booked", "v": "Sat 10:00 · in your calendar · confirmation text sent"}}]},
    {"who": "user", "text": "No, just Jiho. When could I speak with the director?",
     "side": [{"field": {"k": "Siblings", "v": "none", "src": "caller said it"}}]},
    {"who": "ai", "text": "The director will call you tomorrow. What time of day suits you?"},
    {"who": "user", "text": "After six in the evening.",
     "side": [{"field": {"k": "Best time to call", "v": "tomorrow after 6:00 PM", "src": "caller said it"}}]},
    {"who": "ai", "text": "After six tomorrow — noted. We'll see Jiho on Saturday. Have a good night.",
     "side": [{"work": {"icon": "@", "k": "Owner & due", "v": "director's callback · tomorrow after 6:00 PM"}},
              {"work": {"icon": "#", "k": "Tuition card", "v": "3 sessions a week $340 a month · books extra — from your own price list"}},
              {"work": {"icon": "↻", "k": "Reminder", "v": "day-before test reminder drafted — you approve before it sends"}}]}
   ],
   "chat": [
    {"who": "user", "when": "7:55 AM", "text": "Hi, Mirae Yoon from last night. Does Jiho need to bring anything for Saturday's test?"},
    {"who": "ai", "when": "+2 sec", "text": "Just something to write with. We provide the paper, and there's a short results chat right after. Saturday at ten is unchanged.", "merge": True},
    {"who": "user", "when": "7:56 AM", "text": "Jiho gets nineties in school math — will he get into the advanced class?"},
    {"who": "ai", "when": "+2 sec", "text": "Placement is decided by the director from the test result, so I can't call that in advance. I've passed our conversation along — the director will cover it on your call after six today.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: class placement is the director's judgement from the test, not a fact that can be stated in advance"],
   "morning": [
    {"icon": "✓", "k": "New placement test", "v": "Jiho Yoon · grade 8 · Sat 10:00 · in the calendar"},
    {"icon": "#", "k": "Tuition quoted", "v": "$340 a month · books extra · sent by text · opened"},
    {"icon": "@", "k": "Director's task", "v": "call the parent after 6:00 PM today · owner: Suhyun"},
    {"icon": "!", "k": "Waiting for a person", "v": "advanced-class question · full thread attached · owner: Suhyun"}
   ],
   "person": {"when": "9:10 AM", "text": "This is Suhyun, the director. Hi Mirae — I'll give you a straight answer on the advanced class once I've seen Saturday's test. I'll call you after six."},
   "summary": SUMMARY_EN,
   "honest": HONEST_EN
  }
 },

 # ───────────────────────── 대학 입학상담 ─────────────────────────
 "universities": {
  "ko": {
   "biz": "청람대학교 입학처", "owner": "담당자님",
   "meta": "화요일 8:56 PM · 업무 종료 후 · 가상의 대학 입학처", "callTime": "8:56 PM", "chan": "카카오톡",
   "chapters": ["저녁 8:56, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 담당자님 화면"],
   "chapterSubs": ["편입 서류 · 마감일 · 내일 담당자 연락", "자기소개서 분량 · 합격 가능성은 사람에게", "문의 카드 · 서류 안내 · 담당 · 답변 대기"],
   "sys": {"ring": "저녁 8:56 — 전화벨이 울립니다. 입학처는 퇴근했습니다.",
           "chat": "다음 날 아침 8:05 — 같은 지원자가 카카오톡으로.",
           "morning": "오전 9:00 — 담당자님 화면."},
   "customer": {"name": "오지훈", "phone": "010-6642-18··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 청람대학교 입학처입니다. 업무 시간은 끝났지만, 모집요강에 있는 내용은 제가 바로 안내드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "편입 지원하려는데 제출 서류가 어떻게 되나요? 마감이 언제죠?",
     "side": [{"field": {"k": "문의", "v": "일반편입 — 서류 · 마감", "src": "통화에서"}}]},
    {"who": "ai", "text": "일반편입은 성적증명서, 졸업 또는 졸업예정 증명서, 자기소개서 세 가지가 기본이고 학과에 따라 추가 서류가 있어요. 접수 마감은 11월 14일 오후 5시이고 온라인 접수만 받습니다. 전형료는 6만원이에요. 어느 학과에 지원하세요?",
     "side": [{"field": {"k": "안내한 마감일", "v": "11월 14일 17:00 · 온라인 접수만", "src": "입학처 모집요강"}},
              {"field": {"k": "전형료", "v": "60,000원", "src": "입학처 모집요강"}}]},
    {"who": "user", "text": "컴퓨터공학과요. 전문대 졸업인데 지원 가능한가요?",
     "side": [{"field": {"k": "지원 학과", "v": "컴퓨터공학과 · 일반편입", "src": "본인 발화"}}, {"field": {"k": "학력", "v": "전문대 졸업", "src": "본인 발화"}}]},
    {"who": "ai", "text": "컴퓨터공학과는 추가 서류 없이 기본 세 가지예요. 다만 지원 자격은 학점 인정 요건이 있어서 성적표를 보고 담당자가 판단해야 하는 부분이라, 제가 된다 안 된다 말씀드릴 수는 없어요. 입학처 담당자가 내일 오전에 연락드리도록 남겨 둘까요?",
     "side": [{"field": {"k": "담당자 연결", "v": "필요 — 지원 자격 판단", "src": "입학처 규칙"}}]},
    {"who": "user", "text": "네, 부탁드려요."},
    {"who": "ai", "text": "성함과 연락 가능한 번호를 말씀해 주시겠어요? 편한 시간대도 함께요."},
    {"who": "user", "text": "오지훈이고요, 010-6642-1873이에요. 오전 10시 넘어서가 좋아요.",
     "side": [{"field": {"k": "이름", "v": "오지훈", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-6642-18··", "src": "발신번호와 일치"}},
              {"field": {"k": "연락 희망 시간", "v": "내일 10:00 이후", "src": "본인 발화"}}, {"crm": True}]},
    {"who": "ai", "text": "오지훈 님, 내일 오전 10시 이후 담당자 연락으로 남겨 두었어요. 서류 목록과 마감일은 문자로 보내 드릴게요. 성적표를 미리 준비해 두시면 확인이 빨라요.",
     "side": [{"work": {"icon": "✓", "k": "담당자 회신 예약", "v": "내일 10:00 이후 · 캘린더에 들어감 · 확인 문자 발송"}},
              {"work": {"icon": "#", "k": "서류 안내 문자", "v": "세 가지 서류 · 11월 14일 마감 — 모집요강에서"}},
              {"work": {"icon": "@", "k": "담당 배정", "v": "입학처 이정민 · 성적표 학점 인정 확인"}}]},
    {"who": "user", "text": "네, 알겠습니다. 감사합니다."},
    {"who": "ai", "text": "감사합니다. 내일 오전에 연락드릴게요.",
     "side": [{"work": {"icon": "↻", "k": "마감 리마인드", "v": "11월 12일 접수 리마인드 문자 초안 — 발송 전 담당자 확인"}}]}
   ],
   "chat": [
    {"who": "user", "when": "8:05 AM", "text": "어제 전화한 오지훈인데요, 자기소개서 분량 제한이 있나요?"},
    {"who": "ai", "when": "+2 sec", "text": "네, 모집요강 기준으로 2천자 이내예요. 양식은 입학처 홈페이지 서식 페이지에 있어요. 오늘 10시 이후 담당자 연락은 그대로 진행됩니다.", "merge": True},
    {"who": "user", "when": "8:06 AM", "text": "전문대 학점이 3.2인데 합격 가능성 있을까요?"},
    {"who": "ai", "when": "+2 sec", "text": "합격 가능성은 제가 답할 수 없는 부분이에요. 지원 자격 확인과 함께 담당자에게 전달해 두었고, 10시 이후에 연락드릴 거예요.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 지원 자격과 합격 가능성은 서류를 보고 담당자가 하는 판단이지 요강에 있는 사실이 아닙니다"],
   "morning": [
    {"icon": "✓", "k": "새 문의 1건", "v": "오지훈 · 일반편입 · 컴퓨터공학과 · 오늘 10:00 이후 회신"},
    {"icon": "#", "k": "서류 안내", "v": "세 가지 서류 · 11월 14일 마감 · 문자로 발송됨 · 열람 확인"},
    {"icon": "@", "k": "담당자 할 일", "v": "오늘 10:00 이후 회신 전화 · 성적표 학점 인정 확인 · 담당 이정민"},
    {"icon": "!", "k": "답변 대기 1건", "v": "지원 자격 · 합격 가능성 문의 · 대화 전체 첨부 · 담당 이정민"}
   ],
   "person": {"when": "10:08 AM", "text": "입학처 이정민입니다. 오지훈 님, 전문대 졸업이면 성적표로 학점 인정 요건을 확인해 드릴 수 있어요. 합격 여부는 심사 결과로만 말씀드릴 수 있고요. 지금 전화드려도 될까요?"},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 담당자님이 퇴근한 사이에 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Northgate University Admissions", "owner": "the officer",
   "meta": "Tuesday 8:56 PM · after hours · a fictional admissions office", "callTime": "8:56 PM", "chan": "WhatsApp",
   "chapters": ["8:56 PM, the call", "Next morning, WhatsApp", "9:00 AM, the officer’s screen"],
   "chapterSubs": ["transfer documents · deadline · officer call tomorrow", "statement length · the chances question goes to a person", "enquiry card · documents sent · owner · one reply waiting"],
   "sys": {"ring": "8:56 PM — the phone rings. Admissions went home hours ago.",
           "chat": "Next morning, 8:05 AM — the same applicant, on WhatsApp.",
           "morning": "9:00 AM — the officer’s screen."},
   "customer": {"name": "Jihoon Oh", "phone": "555-01··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Northgate University Admissions. The office is closed for the day, but I can answer anything that's in the published prospectus. How can I help?"},
    {"who": "user", "text": "I want to apply as a transfer student. What documents do I need, and when's the deadline?",
     "side": [{"field": {"k": "Enquiry", "v": "general transfer — documents · deadline", "src": "from the call"}}]},
    {"who": "ai", "text": "For a general transfer, the basics are your transcript, proof of graduation or expected graduation, and a personal statement, with extra documents for some departments. The deadline is November fourteenth at five PM, online only, and the application fee is sixty dollars. Which department are you applying to?",
     "side": [{"field": {"k": "Deadline quoted", "v": "Nov 14 · 5:00 PM · online only", "src": "your prospectus"}},
              {"field": {"k": "Application fee", "v": "$60", "src": "your prospectus"}}]},
    {"who": "user", "text": "Computer Science. I graduated from a community college — am I eligible?",
     "side": [{"field": {"k": "Department", "v": "Computer Science · general transfer", "src": "caller said it"}}, {"field": {"k": "Education", "v": "community college graduate", "src": "caller said it"}}]},
    {"who": "ai", "text": "Computer Science needs just the three basics. Eligibility, though, depends on credit recognition, and that's decided by an admissions officer from your transcript — so I can't tell you yes or no. Shall I have an officer call you tomorrow morning?",
     "side": [{"field": {"k": "Needs an officer", "v": "yes — eligibility judgement", "src": "your rule"}}]},
    {"who": "user", "text": "Yes, please."},
    {"who": "ai", "text": "Can I get your name, a number I can reach you on, and a time that suits?"},
    {"who": "user", "text": "Jihoon Oh, five five five, zero one eight seven. After ten in the morning is best.",
     "side": [{"field": {"k": "Name", "v": "Jihoon Oh", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-01··", "src": "matches caller ID"}},
              {"field": {"k": "Best time to call", "v": "tomorrow after 10:00", "src": "caller said it"}}, {"crm": True}]},
    {"who": "ai", "text": "Thank you, Jihoon. An officer will call you after ten tomorrow. I'm texting you the document list and the deadline now, and having your transcript ready will speed up the check.",
     "side": [{"work": {"icon": "✓", "k": "Callback booked", "v": "tomorrow after 10:00 · in your calendar · confirmation text sent"}},
              {"work": {"icon": "#", "k": "Documents text", "v": "three documents · Nov 14 deadline — from the prospectus"}},
              {"work": {"icon": "@", "k": "Owner", "v": "admissions officer Jeongmin · credit-recognition check"}}]},
    {"who": "user", "text": "Got it. Thank you."},
    {"who": "ai", "text": "Thank you. We'll call you tomorrow morning.",
     "side": [{"work": {"icon": "↻", "k": "Deadline reminder", "v": "Nov 12 reminder drafted — you approve before it sends"}}]}
   ],
   "chat": [
    {"who": "user", "when": "8:05 AM", "text": "Hi, Jihoon Oh from last night. Is there a length limit on the personal statement?"},
    {"who": "ai", "when": "+2 sec", "text": "Yes — eight hundred words, per the prospectus. The form is on the admissions site under Forms. Your officer call after ten today is unchanged.", "merge": True},
    {"who": "user", "when": "8:06 AM", "text": "My community college GPA is three point two. Do I have a chance of getting in?"},
    {"who": "ai", "when": "+2 sec", "text": "Chances of admission aren't something I can answer. I've passed it to your officer along with the eligibility check — they'll call after ten.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: eligibility and admission chances are an officer's judgement from the documents, not a fact in the prospectus"],
   "morning": [
    {"icon": "✓", "k": "New enquiry", "v": "Jihoon Oh · transfer · Computer Science · callback after 10:00 today"},
    {"icon": "#", "k": "Documents sent", "v": "three documents · Nov 14 deadline · sent by text · opened"},
    {"icon": "@", "k": "Officer task", "v": "call back after 10:00 · credit-recognition check from transcript · owner: Jeongmin"},
    {"icon": "!", "k": "Waiting for a person", "v": "eligibility and chances question · full thread attached · owner: Jeongmin"}
   ],
   "person": {"when": "10:08 AM", "text": "This is Jeongmin from Admissions. Hi Jihoon — with a community college degree I can confirm credit recognition from your transcript, and admission itself is only decided by the review. Is now a good time to call?"},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened after the office had gone home.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────── 미용실 ─────────────────────────
 "salons": {
  "ko": {
   "biz": "루미헤어", "owner": "원장님",
   "meta": "수요일 2:12 PM · 시술 중 · 가상의 미용실", "callTime": "2:12 PM", "chan": "카카오톡",
   "chapters": ["오후 2:12, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 원장님 화면"],
   "chapterSubs": ["뿌리염색과 클리닉 · 견적 · 토요일 예약", "주차 질문 · 탈색 모발 질문은 사람에게", "예약 · 안내 금액 · 담당 · 답변 대기"],
   "sys": {"ring": "오후 2:12 — 전화벨이 울립니다. 원장님은 파마 중이라 손을 뗄 수 없습니다.",
           "chat": "다음 날 아침 7:30 — 같은 손님이 카카오톡으로.",
           "morning": "오전 9:00 — 원장님 화면."},
   "customer": {"name": "강예진", "phone": "010-9047-33··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 루미헤어입니다. 지금 원장님이 시술 중이라 제가 대신 받았어요. 예약과 가격 문의는 바로 도와드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "토요일에 뿌리염색이랑 클리닉 같이 되나요? 시간 얼마나 걸려요?",
     "side": [{"field": {"k": "요청 시술", "v": "뿌리염색 + 클리닉 — 토요일", "src": "통화에서"}}]},
    {"who": "ai", "text": "네, 같이 하시면 약 2시간 잡으시면 돼요. 뿌리염색은 7만원, 클리닉은 모발 상태에 따라 8만원부터예요. 토요일은 오후 1시와 4시 30분이 비어 있어요. 어느 쪽이 좋으세요?",
     "side": [{"field": {"k": "소요 시간", "v": "약 2시간 — 넉넉히", "src": "원장님 요금표"}},
              {"field": {"k": "안내 금액", "v": "뿌리염색 70,000원 · 클리닉 80,000원부터", "src": "원장님 요금표"}}]},
    {"who": "user", "text": "1시로 할게요."},
    {"who": "ai", "text": "토요일 오후 1시로 잡을게요. 지정하실 디자이너가 있으세요?"},
    {"who": "user", "text": "아뇨, 처음 가는 거라 아무나 괜찮아요.",
     "side": [{"field": {"k": "지정 디자이너", "v": "없음 — 매장에서 배정", "src": "본인 발화"}}, {"field": {"k": "방문 구분", "v": "첫 방문", "src": "본인 발화"}}]},
    {"who": "ai", "text": "그럼 담당은 비워 두고 매장에서 정해 드릴게요. 성함과 연락처를 말씀해 주시겠어요?"},
    {"who": "user", "text": "강예진이고요, 010-9047-3318이에요.",
     "side": [{"field": {"k": "이름", "v": "강예진", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-9047-33··", "src": "발신번호와 일치"}}, {"crm": True}]},
    {"who": "ai", "text": "강예진 님, 토요일 오후 1시 예약되었습니다. 2시간으로 넉넉히 잡아 두었고, 금요일에 확인 문자 보내 드릴게요. 처음 오시니 위치 안내도 같이 넣을게요.",
     "side": [{"field": {"k": "예약", "v": "토 13:00 · 2시간", "src": "캘린더의 빈 시간"}},
              {"work": {"icon": "✓", "k": "예약 확정", "v": "토 13:00 · 2시간 · 캘린더에 들어감"}},
              {"work": {"icon": "↻", "k": "전날 확인 문자", "v": "금요일 오후 발송 예정 · 위치 안내 포함"}}]},
    {"who": "user", "text": "네, 감사합니다."},
    {"who": "ai", "text": "감사합니다. 토요일에 뵐게요.",
     "side": [{"work": {"icon": "@", "k": "담당 배정", "v": "매장에서 정함 · 첫 방문 표시"}},
              {"work": {"icon": "#", "k": "안내 금액 카드", "v": "뿌리염색 70,000원 · 클리닉 80,000원부터 — 원장님 요금표에서"}}]}
   ],
   "chat": [
    {"who": "user", "when": "7:30 AM", "text": "어제 토요일 1시로 예약한 강예진인데요, 주차 되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "네, 건물 지하 주차장 2시간 무료예요. 토요일 오후 1시 예약은 그대로예요.", "merge": True},
    {"who": "user", "when": "7:31 AM", "text": "지난달에 탈색을 했는데, 뿌리염색이랑 클리닉 같이 해도 머리 괜찮을까요?"},
    {"who": "ai", "when": "+2 sec", "text": "모발 상태는 직접 보아야 알 수 있어서 제가 판단할 수 없어요. 탈색 이력을 원장님께 전달해 두었고, 오전 중에 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 탈색한 모발에 염색이 되는지는 보고 판단할 일이지 요금표에 있는 사실이 아닙니다"],
   "morning": [
    {"icon": "✓", "k": "새 예약 1건", "v": "강예진 · 토 13:00 · 2시간 · 첫 방문 · 캘린더에 있음"},
    {"icon": "#", "k": "안내 금액", "v": "뿌리염색 70,000원 · 클리닉 80,000원부터 · 문자로 발송됨 · 열람 확인"},
    {"icon": "@", "k": "매장 할 일", "v": "담당 디자이너 배정 · 금요일 확인 문자 · 담당 원장님"},
    {"icon": "!", "k": "답변 대기 1건", "v": "탈색 후 염색 가능 여부 · 대화 전체 첨부 · 담당 원장님"}
   ],
   "person": {"when": "9:12 AM", "text": "원장 서지우입니다. 강예진 님, 탈색 이력이 있으면 토요일에 먼저 모발 상태를 보고 순서를 정할게요. 예약 시간 그대로 오시면 됩니다."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 원장님이 손을 떼지 않는 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Lumi Hair Studio", "owner": "the owner",
   "meta": "Wednesday 2:12 PM · mid-service · a fictional salon", "callTime": "2:12 PM", "chan": "WhatsApp",
   "chapters": ["2:12 PM, the call", "Next morning, WhatsApp", "9:00 AM, the owner’s screen"],
   "chapterSubs": ["roots and treatment · quote · Saturday booked", "parking · the bleached-hair question goes to a person", "booking · quote · owner · one reply waiting"],
   "sys": {"ring": "2:12 PM — the phone rings. The owner is mid-perm and can't take her hands off.",
           "chat": "Next morning, 7:30 AM — the same customer, on WhatsApp.",
           "morning": "9:00 AM — the owner’s screen."},
   "customer": {"name": "Yejin Kang", "phone": "555-03··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Lumi Hair Studio. The owner's mid-service, so I've picked up. I can handle bookings and prices right now. How can I help?"},
    {"who": "user", "text": "Can I get a root touch-up and a treatment together on Saturday? How long does that take?",
     "side": [{"field": {"k": "Request", "v": "root touch-up + treatment — Saturday", "src": "from the call"}}]},
    {"who": "ai", "text": "Yes — together, allow about two hours. A root touch-up is seventy-five dollars, and the treatment starts at eighty-five depending on your hair. On Saturday I have one PM or four thirty. Which works better?",
     "side": [{"field": {"k": "Duration", "v": "about 2 hours — generous", "src": "your service menu"}},
              {"field": {"k": "Quote", "v": "root touch-up $75 · treatment from $85", "src": "your service menu"}}]},
    {"who": "user", "text": "One o'clock, please."},
    {"who": "ai", "text": "Saturday at one it is. Do you have a stylist you'd like to request?"},
    {"who": "user", "text": "No, it's my first time there — anyone's fine.",
     "side": [{"field": {"k": "Stylist", "v": "none — salon assigns", "src": "caller said it"}}, {"field": {"k": "Visit", "v": "first visit", "src": "caller said it"}}]},
    {"who": "ai", "text": "Then I'll leave the stylist open for the salon to assign. Can I get your name and a mobile number?"},
    {"who": "user", "text": "Yejin Kang, five five five, zero three one eight.",
     "side": [{"field": {"k": "Name", "v": "Yejin Kang", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-03··", "src": "matches caller ID"}}, {"crm": True}]},
    {"who": "ai", "text": "Thank you, Yejin. You're booked for Saturday at one, with a full two hours held. I'll text you a reminder on Friday, with directions since it's your first visit.",
     "side": [{"field": {"k": "Slot", "v": "Sat 1:00 PM · 2 hours", "src": "free in your calendar"}},
              {"work": {"icon": "✓", "k": "Booked", "v": "Sat 1:00 PM · 2 hours · in your calendar"}},
              {"work": {"icon": "↻", "k": "Day-before reminder", "v": "goes out Friday afternoon · directions included"}}]},
    {"who": "user", "text": "Great, thank you."},
    {"who": "ai", "text": "Thank you. See you Saturday.",
     "side": [{"work": {"icon": "@", "k": "Stylist", "v": "left for the salon to assign · first visit flagged"}},
              {"work": {"icon": "#", "k": "Quote card", "v": "root touch-up $75 · treatment from $85 — from your own service menu"}}]}
   ],
   "chat": [
    {"who": "user", "when": "7:30 AM", "text": "Hi, Yejin Kang — I booked Saturday at one last night. Is there parking?"},
    {"who": "ai", "when": "+2 sec", "text": "Yes — two hours free in the garage under the building. Your Saturday 1:00 PM booking is unchanged.", "merge": True},
    {"who": "user", "when": "7:31 AM", "text": "I bleached my hair last month. Will it be okay to do the roots and the treatment together?"},
    {"who": "ai", "when": "+2 sec", "text": "That's a call that needs someone to see your hair, so I can't make it. I've passed the bleach history to the owner — she'll reply this morning.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: whether bleached hair can take colour is judged by looking, not a fact on the service menu"],
   "morning": [
    {"icon": "✓", "k": "New booking", "v": "Yejin Kang · Sat 1:00 PM · 2 hours · first visit · in the calendar"},
    {"icon": "#", "k": "Quote", "v": "root touch-up $75 · treatment from $85 · sent by text · opened"},
    {"icon": "@", "k": "Salon task", "v": "assign a stylist · Friday reminder · owner: the owner"},
    {"icon": "!", "k": "Waiting for a person", "v": "bleached-hair question · full thread attached · owner: the owner"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Jiwoo, the owner. Hi Yejin — with bleach in the history I'll look at your hair first on Saturday and decide the order from there. Come at one as planned."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the owner's hands were busy.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────── 헬스장 ─────────────────────────
 "fitness": {
  "ko": {
   "biz": "리지라인 피트니스", "owner": "관장님",
   "meta": "목요일 9:52 PM · 데스크 마감 후 · 가상의 헬스장", "callTime": "9:52 PM", "chan": "카카오톡",
   "chapters": ["밤 9:52, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 관장님 화면"],
   "chapterSubs": ["피티와 헬스 요금 · 무료 체험 · 내일 저녁 예약", "주차 질문 · 허리 질문은 사람에게", "체험 예약 · 안내 요금 · 담당 · 답변 대기"],
   "sys": {"ring": "밤 9:52 — 전화벨이 울립니다. 데스크는 마감했습니다.",
           "chat": "다음 날 아침 7:45 — 같은 손님이 카카오톡으로.",
           "morning": "오전 9:00 — 관장님 화면."},
   "customer": {"name": "한도윤", "phone": "010-2263-58··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 리지라인 피트니스입니다. 데스크는 마감했지만, 등록 문의와 체험 예약은 제가 도와드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "피티 몇 회부터 등록 가능한가요? 헬스만 하면 얼마예요?",
     "side": [{"field": {"k": "문의 항목", "v": "피티 · 헬스 단독", "src": "통화에서"}}]},
    {"who": "ai", "text": "피티는 10회 65만원부터이고, 20회, 30회로 갈수록 회당 단가가 내려가요. 헬스 단독은 3개월 21만원이에요. 처음이시면 무료 체험 1회가 있는데, 내일 저녁 자리가 남아 있어요.",
     "side": [{"field": {"k": "안내한 요금", "v": "피티 10회 650,000원 · 헬스 3개월 210,000원", "src": "관장님 요금표"}}]},
    {"who": "user", "text": "처음이에요. 내일 8시쯤 가능할까요?",
     "side": [{"field": {"k": "기존 회원", "v": "아님 — 첫 방문", "src": "본인 발화"}}]},
    {"who": "ai", "text": "네, 내일 저녁 8시 체험 자리 있어요. 성함과 연락처를 말씀해 주시겠어요?"},
    {"who": "user", "text": "한도윤이고요, 010-2263-5841이에요.",
     "side": [{"field": {"k": "이름", "v": "한도윤", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-2263-58··", "src": "발신번호와 일치"}}, {"crm": True}]},
    {"who": "ai", "text": "한도윤 님, 내일 저녁 8시 무료 체험 예약되었어요. 운동복과 실내화만 챙겨 오시면 되고, 락커와 수건은 준비되어 있어요. 확인 문자와 건강 문진표를 지금 보내 드릴게요.",
     "side": [{"field": {"k": "체험 예약", "v": "내일 20:00", "src": "캘린더의 빈 시간"}},
              {"work": {"icon": "✓", "k": "체험 예약 확정", "v": "내일 20:00 · 캘린더에 들어감 · 확인 문자 발송"}},
              {"work": {"icon": "#", "k": "건강 문진표", "v": "문자로 발송 — 체험 전 회수"}}]},
    {"who": "user", "text": "네. 등록하면 언제부터 다닐 수 있어요? 다음 주부터 시작하고 싶어서요.",
     "side": [{"field": {"k": "희망 시작 시기", "v": "다음 주", "src": "본인 발화"}}]},
    {"who": "ai", "text": "등록 당일부터 바로 이용하실 수 있어요. 자세한 건 체험 뒤에 트레이너가 안내드릴 거예요. 연락은 저녁 시간이 편하세요?"},
    {"who": "user", "text": "네, 저녁 7시 이후요.",
     "side": [{"field": {"k": "연락 가능 시간대", "v": "19:00 이후", "src": "본인 발화"}}]},
    {"who": "ai", "text": "저녁 7시 이후로 적어 둘게요. 내일 8시에 뵙겠습니다. 편안한 밤 되세요.",
     "side": [{"work": {"icon": "@", "k": "체험 담당", "v": "트레이너 김태오 · 내일 20:00 · 문진표 확인"}},
              {"work": {"icon": "↻", "k": "체험 후 후속", "v": "체험 다음 날 등록 안내 문자 초안 — 발송 전 관장님 확인"}}]}
   ],
   "chat": [
    {"who": "user", "when": "7:45 AM", "text": "어제 체험 예약한 한도윤인데요, 주차 되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "네, 건물 주차장 2시간 무료예요. 오늘 저녁 8시 체험은 그대로예요.", "merge": True},
    {"who": "user", "when": "7:46 AM", "text": "제가 허리 디스크가 있는데 피티 해도 괜찮을까요?"},
    {"who": "ai", "when": "+2 sec", "text": "허리 상태에 관한 건 제가 판단할 수 없는 부분이에요. 체험 담당 트레이너에게 전달해 두었고, 체험 전에 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 허리 디스크가 있는 분의 운동 가능 여부는 트레이너의 판단이지 요금표에 있는 사실이 아닙니다"],
   "morning": [
    {"icon": "✓", "k": "새 체험 예약 1건", "v": "한도윤 · 오늘 20:00 · 첫 방문 · 캘린더에 있음"},
    {"icon": "#", "k": "안내 요금", "v": "피티 10회 650,000원 · 헬스 3개월 210,000원 · 문자로 발송됨 · 열람 확인"},
    {"icon": "@", "k": "트레이너 할 일", "v": "20:00 체험 담당 · 문진표 회수 · 담당 김태오"},
    {"icon": "!", "k": "답변 대기 1건", "v": "허리 디스크 운동 가능 여부 · 대화 전체 첨부 · 담당 김태오"}
   ],
   "person": {"when": "9:12 AM", "text": "트레이너 김태오입니다. 한도윤 님, 문진표에 허리 내용을 적어 주시면 오늘 체험 때 상태를 보고 맞는 운동부터 같이 해 볼게요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 관장님이 수업하는 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Ridgeline Fitness", "owner": "the owner",
   "meta": "Thursday 9:52 PM · desk closed · a fictional gym", "callTime": "9:52 PM", "chan": "WhatsApp",
   "chapters": ["9:52 PM, the call", "Next morning, WhatsApp", "9:00 AM, the owner’s screen"],
   "chapterSubs": ["training and gym prices · free trial · tomorrow evening", "parking · the back-injury question goes to a person", "trial booked · prices quoted · owner · one reply waiting"],
   "sys": {"ring": "9:52 PM — the phone rings. The desk closed at nine.",
           "chat": "Next morning, 7:45 AM — the same caller, on WhatsApp.",
           "morning": "9:00 AM — the owner’s screen."},
   "customer": {"name": "Doyun Han", "phone": "555-05··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Ridgeline Fitness. The desk is closed for the night, but I can answer membership questions and book a trial. How can I help?"},
    {"who": "user", "text": "What's the minimum for personal training? And how much is gym-only?",
     "side": [{"field": {"k": "Enquiry", "v": "personal training · gym-only", "src": "from the call"}}]},
    {"who": "ai", "text": "Personal training starts at ten sessions for six hundred fifty dollars, and the price per session drops at twenty and thirty. Gym-only is two hundred ten for three months. If you're new, you get one free trial — there's space tomorrow evening.",
     "side": [{"field": {"k": "Prices quoted", "v": "PT 10 sessions $650 · gym 3 months $210", "src": "your price list"}}]},
    {"who": "user", "text": "I'm new. Could I come around eight tomorrow?",
     "side": [{"field": {"k": "Existing member", "v": "no — first visit", "src": "caller said it"}}]},
    {"who": "ai", "text": "Yes, eight PM tomorrow is open. Can I get your name and a mobile number?"},
    {"who": "user", "text": "Doyun Han, five five five, zero five eight four.",
     "side": [{"field": {"k": "Name", "v": "Doyun Han", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-05··", "src": "matches caller ID"}}, {"crm": True}]},
    {"who": "ai", "text": "Thank you, Doyun. Your free trial is booked for tomorrow at eight. Just bring workout clothes and indoor shoes — lockers and towels are provided. I'm texting you a confirmation and our health screening form now.",
     "side": [{"field": {"k": "Trial", "v": "tomorrow 8:00 PM", "src": "free in your calendar"}},
              {"work": {"icon": "✓", "k": "Trial booked", "v": "tomorrow 8:00 PM · in your calendar · confirmation text sent"}},
              {"work": {"icon": "#", "k": "Screening form", "v": "sent by text — collected before the trial"}}]},
    {"who": "user", "text": "Okay. If I sign up, when can I start? I'd like to begin next week.",
     "side": [{"field": {"k": "Start date wanted", "v": "next week", "src": "caller said it"}}]},
    {"who": "ai", "text": "You can use the gym from the day you sign up. The trainer will walk you through it after the trial. Are evenings the best time to reach you?"},
    {"who": "user", "text": "Yes, after seven.",
     "side": [{"field": {"k": "Best time to call", "v": "after 7:00 PM", "src": "caller said it"}}]},
    {"who": "ai", "text": "After seven — noted. See you tomorrow at eight. Have a good night.",
     "side": [{"work": {"icon": "@", "k": "Trial owner", "v": "trainer Taeo · tomorrow 8:00 PM · check the screening form"}},
              {"work": {"icon": "↻", "k": "After the trial", "v": "next-day sign-up nudge drafted — you approve before it sends"}}]}
   ],
   "chat": [
    {"who": "user", "when": "7:45 AM", "text": "Hi, Doyun Han — I booked a trial last night. Is there parking?"},
    {"who": "ai", "when": "+2 sec", "text": "Yes — two hours free in the building lot. Your trial tonight at 8:00 PM is unchanged.", "merge": True},
    {"who": "user", "when": "7:46 AM", "text": "I have a herniated disc in my lower back. Is personal training okay for me?"},
    {"who": "ai", "when": "+2 sec", "text": "That's about your back, so it's not something I can judge. I've passed it to the trainer running your trial — they'll contact you before you come in.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: whether someone with a disc injury should train is the trainer's judgement, not a fact on the price list"],
   "morning": [
    {"icon": "✓", "k": "New trial", "v": "Doyun Han · today 8:00 PM · first visit · in the calendar"},
    {"icon": "#", "k": "Prices quoted", "v": "PT 10 sessions $650 · gym 3 months $210 · sent by text · opened"},
    {"icon": "@", "k": "Trainer task", "v": "run the 8:00 PM trial · collect the screening form · owner: Taeo"},
    {"icon": "!", "k": "Waiting for a person", "v": "disc injury question · full thread attached · owner: Taeo"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Taeo, your trainer for tonight. Hi Doyun — note the back on the screening form and we'll start with what suits it when I see you at eight."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the owner was teaching.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────── 설비 · 수리 ─────────────────────────
 "home-services": {
  "ko": {
   "biz": "한결설비", "owner": "사장님",
   "meta": "화요일 8:47 PM · 기사 퇴근 후 · 가상의 설비업체", "callTime": "8:47 PM", "chan": "카카오톡",
   "chapters": ["저녁 8:47, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 사장님 화면"],
   "chapterSubs": ["보일러 에러 E9 · 안전 확인 · 오늘 밤 10시 방문", "부품 교체 일정 · 최종 금액은 사람에게", "방문 완료 · 견적서 · 담당 · 답변 대기"],
   "sys": {"ring": "저녁 8:47 — 전화벨이 울립니다. 기사님들은 모두 퇴근했습니다.",
           "chat": "다음 날 아침 7:20 — 같은 고객이 카카오톡으로.",
           "morning": "오전 9:00 — 사장님 화면."},
   "customer": {"name": "임채원", "phone": "010-7731-02··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 한결설비입니다. 기사님들은 퇴근했지만, 방문 예약은 제가 바로 잡아 드릴 수 있어요. 어디가 문제세요?"},
    {"who": "user", "text": "보일러가 안 켜지는데 오늘 와 주실 수 있나요? 에러 코드는 E9 떠 있어요.",
     "side": [{"field": {"k": "증상", "v": "보일러 안 켜짐 · 에러 코드 E9 · 8:47 PM", "src": "통화에서 · 진단 아님"}}]},
    {"who": "ai", "text": "먼저 하나만 여쭐게요. 혹시 가스 냄새가 나거나, 타는 냄새나 연기가 있나요?"},
    {"who": "user", "text": "아뇨, 그런 건 없어요. 그냥 안 켜져요.",
     "side": [{"field": {"k": "안전 문구", "v": "발동 안 함 — 가스 · 연기 없음", "src": "본인 발화"}},
              {"work": {"icon": "✓", "k": "안전 확인", "v": "가스 · 연기 없음 → 예약 진행"}}]},
    {"who": "ai", "text": "다행이에요. E9는 보일러마다 뜻이 달라서 기사님이 직접 보셔야 정확해요. 오늘은 밤 10시 이후에 가능하고, 야간 출장은 기본 출장비 5만원에 부품비가 따로 붙어요. 내일 오전 8시도 비어 있어요. 어느 쪽이 좋으세요?",
     "side": [{"field": {"k": "안내 금액", "v": "야간 기본 출장비 50,000원 · 부품비 별도", "src": "사장님 요금표"}},
              {"field": {"k": "방문 가능", "v": "오늘 22:00 이후 · 내일 08:00", "src": "캘린더의 빈 시간"}}]},
    {"who": "user", "text": "지금 집에 애기가 있어서 오늘 밤에 부탁드릴게요."},
    {"who": "ai", "text": "네, 오늘 밤 10시로 잡을게요. 성함과 연락처, 그리고 주소를 동, 호수까지 말씀해 주시겠어요?"},
    {"who": "user", "text": "임채원이고요, 010-7731-0256이에요. 주소는 은행로 24 행복아파트 103동 702호예요.",
     "side": [{"field": {"k": "이름", "v": "임채원", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-7731-02··", "src": "발신번호와 일치"}},
              {"field": {"k": "주소", "v": "은행로 24 행복아파트 103동 702호", "src": "본인 발화"}},
              {"field": {"k": "건물", "v": "아파트 · 7층", "src": "본인 발화"}}, {"crm": True}]},
    {"who": "ai", "text": "임채원 님, 오늘 밤 10시 방문 예약되었습니다. 기사님이 출발할 때 전화드릴게요. 보일러 종류나 설치한 지 얼마나 됐는지 아시면 말씀해 주세요.",
     "side": [{"field": {"k": "방문 확정", "v": "오늘 22:00", "src": "캘린더의 빈 시간"}},
              {"work": {"icon": "✓", "k": "방문 확정", "v": "오늘 22:00 · 캘린더에 들어감 · 확인 문자 발송"}},
              {"work": {"icon": "@", "k": "야간 기사 배정", "v": "박정우 기사 · 출발 전 연락"}}]},
    {"who": "user", "text": "가스보일러고요, 한 6년 됐어요.",
     "side": [{"field": {"k": "부품 확인", "v": "가스보일러 · 약 6년 — 현장 확인 필요", "src": "본인 발화 · 진단 아님"}}]},
    {"who": "ai", "text": "적어 둘게요. 기다리시는 동안 보일러를 직접 분해하거나 만지지는 마시고, 혹시 가스 냄새가 나면 바로 이 번호로 다시 전화 주세요. 밤 10시에 뵙겠습니다.",
     "side": [{"work": {"icon": "#", "k": "출장 카드", "v": "증상 원문 · 주소 · 야간 출장비 50,000원 — 사장님 요금표에서"}},
              {"work": {"icon": "↻", "k": "출발 전 연락", "v": "21:40 출발 알림 문자 초안 — 기사님 출발 시 발송"}}]},
    {"who": "user", "text": "네, 감사합니다."},
    {"who": "ai", "text": "감사합니다. 곧 뵐게요."}
   ],
   "chat": [
    {"who": "user", "when": "7:20 AM", "text": "어젯밤 기사님 다녀가신 임채원인데요, 점화 부품 교체 견적 문자 받았어요. 언제 다시 오실 수 있나요?"},
    {"who": "ai", "when": "+2 sec", "text": "견적서에는 점화 장치 교체 12만원, 어젯밤 출장비 5만원 별도로 되어 있어요. 부품은 오늘 오후에 들어오고, 내일 오전 8시가 비어 있어 임시로 잡아 두었어요. 안 맞으면 말씀해 주세요.", "merge": True},
    {"who": "user", "when": "7:22 AM", "text": "그럼 부품 갈면 총 얼마 나오나요? 그 이상은 안 나오는 거죠?"},
    {"who": "ai", "when": "+2 sec", "text": "최종 금액은 부품을 교체해 보고 확인해야 해서 제가 확정해 드릴 수 없어요. 견적 내용과 질문을 기사님께 전달해 두었고, 오전 중에 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 최종 금액은 열어 보고 정해지는 것이지 요금표에 있는 사실이 아닙니다"],
   "morning": [
    {"icon": "✓", "k": "방문 완료 1건", "v": "임채원 · 어젯밤 22:00 · 점화 장치 확인 · 내일 08:00 교체 방문 잡힘"},
    {"icon": "#", "k": "견적서 #3181", "v": "점화 장치 교체 120,000원 · 출장비 50,000원 · 문자로 발송됨 · 열람 확인"},
    {"icon": "@", "k": "기사 할 일", "v": "오늘 오후 부품 수령 · 내일 08:00 교체 방문 · 담당 박정우"},
    {"icon": "!", "k": "답변 대기 1건", "v": "최종 금액 확정 문의 · 대화 전체 첨부 · 담당 박정우"}
   ],
   "person": {"when": "9:12 AM", "text": "기사 박정우입니다. 임채원 님, 점화 장치만 교체하면 견적대로 12만원이고요, 열어 봤을 때 다른 부품이 더 필요하면 작업 전에 먼저 말씀드리고 진행할게요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 밤 10시 방문과 답장 한 줄. 나머지는 사장님 손을 거치지 않고 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Oakridge Heating and Plumbing", "owner": "the owner",
   "meta": "Tuesday 8:47 PM · crew off for the night · a fictional contractor", "callTime": "8:47 PM", "chan": "WhatsApp",
   "chapters": ["8:47 PM, the call", "Next morning, WhatsApp", "9:00 AM, the owner’s screen"],
   "chapterSubs": ["boiler error E9 · safety check · tonight at ten", "part replacement · the final-total question goes to a person", "visit done · estimate · owner · one reply waiting"],
   "sys": {"ring": "8:47 PM — the phone rings. The crew went home at six.",
           "chat": "Next morning, 7:20 AM — the same customer, on WhatsApp.",
           "morning": "9:00 AM — the owner’s screen."},
   "customer": {"name": "Chaewon Lim", "phone": "555-02··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Oakridge Heating and Plumbing. Our techs are off for the night, but I can book a visit right now. What's the problem?"},
    {"who": "user", "text": "My boiler won't turn on. Can someone come tonight? It's showing error code E nine.",
     "side": [{"field": {"k": "Symptom", "v": "boiler won't start · error code E9 · 8:47 PM", "src": "from the call · not a diagnosis"}}]},
    {"who": "ai", "text": "One thing first — do you smell gas, or anything burning, or see smoke?"},
    {"who": "user", "text": "No, nothing like that. It just won't start.",
     "side": [{"field": {"k": "Safety script", "v": "not triggered — no gas, no smoke", "src": "caller said it"}},
              {"work": {"icon": "✓", "k": "Safety check", "v": "no gas · no smoke → booking proceeds"}}]},
    {"who": "ai", "text": "Good. E nine means different things on different boilers, so a tech needs to see it to be sure. Tonight I can do after ten, and a night call-out is eighty-five dollars plus any parts. Tomorrow at eight AM is also open. Which do you prefer?",
     "side": [{"field": {"k": "Quote", "v": "night call-out $85 · parts extra", "src": "your price list"}},
              {"field": {"k": "Available", "v": "tonight after 10:00 PM · tomorrow 8:00 AM", "src": "free in your calendar"}}]},
    {"who": "user", "text": "I've got a baby at home, so tonight, please."},
    {"who": "ai", "text": "Tonight at ten it is. Can I get your name, a number, and your address with the unit number?"},
    {"who": "user", "text": "Chaewon Lim, five five five, zero two five six. It's twenty-four Bank Road, Harbor View Apartments, unit seven oh two.",
     "side": [{"field": {"k": "Name", "v": "Chaewon Lim", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-02··", "src": "matches caller ID"}},
              {"field": {"k": "Address", "v": "24 Bank Road · Harbor View Apartments · unit 702", "src": "caller said it"}},
              {"field": {"k": "Building", "v": "apartment · 7th floor", "src": "caller said it"}}, {"crm": True}]},
    {"who": "ai", "text": "Thank you, Chaewon. You're booked for ten tonight — the tech will call you when he's on his way. If you know the boiler type or how old it is, that helps.",
     "side": [{"field": {"k": "Visit", "v": "tonight 10:00 PM", "src": "free in your calendar"}},
              {"work": {"icon": "✓", "k": "Visit booked", "v": "tonight 10:00 PM · in your calendar · confirmation text sent"}},
              {"work": {"icon": "@", "k": "On-call tech", "v": "Jungwoo · calls before leaving"}}]},
    {"who": "user", "text": "It's a gas boiler, about six years old.",
     "side": [{"field": {"k": "Parts check", "v": "gas boiler · about 6 years — confirm on site", "src": "caller said it · not a diagnosis"}}]},
    {"who": "ai", "text": "Noted. While you wait, please don't open up or touch the boiler, and if you smell gas at any point, call this number again straight away. See you at ten.",
     "side": [{"work": {"icon": "#", "k": "Job card", "v": "symptom in the caller's words · address · night call-out $85 — from your own price list"}},
              {"work": {"icon": "↻", "k": "On-the-way text", "v": "9:40 PM departure text drafted — sends when the tech leaves"}}]},
    {"who": "user", "text": "Okay, thank you."},
    {"who": "ai", "text": "Thank you. See you soon."}
   ],
   "chat": [
    {"who": "user", "when": "7:20 AM", "text": "Hi, Chaewon Lim — your tech came last night. I got the estimate text for the ignition part. When can he come back?"},
    {"who": "ai", "when": "+2 sec", "text": "The estimate is one hundred sixty dollars for the ignition module, plus last night's eighty-five call-out. The part arrives this afternoon, and tomorrow at 8:00 AM was open, so I've pencilled that in — tell me if it doesn't suit.", "merge": True},
    {"who": "user", "when": "7:22 AM", "text": "So what's the total once it's replaced? It won't go above that, right?"},
    {"who": "ai", "when": "+2 sec", "text": "The final amount can only be confirmed once the part is in, so I can't guarantee it. I've passed the estimate and your question to the tech — he'll reply this morning.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: the final amount is set on the job, not a fact on the price list"],
   "morning": [
    {"icon": "✓", "k": "Visit done", "v": "Chaewon Lim · last night 10:00 PM · ignition checked · replacement pencilled for tomorrow 8:00 AM"},
    {"icon": "#", "k": "Estimate #3181", "v": "ignition module $160 · call-out $85 · sent by text · opened"},
    {"icon": "@", "k": "Tech task", "v": "collect the part this afternoon · replace tomorrow 8:00 AM · owner: Jungwoo"},
    {"icon": "!", "k": "Waiting for a person", "v": "final-total question · full thread attached · owner: Jungwoo"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Jungwoo, the tech from last night. Hi Chaewon — if it's only the ignition module, it's the one sixty on the estimate. If I find anything else once it's open, I'll tell you before I touch it."},
   "summary": "One {call} call · four messages · what people did: the ten PM visit and one reply. The rest never needed the owner's hands.",
   "honest": HONEST_EN
  }
 },

}
