# -*- coding: utf-8 -*-
"""데모 대본 B — 방역 · 건물관리 · 부동산 · 자동차 정비 · 이사 · 셀프 스토리지 · 장비 대여 · 음식점.
형식은 build/demo/validate.py 의 docstring, 본보기는 build/demo/scripts_dental.py.
각 업종의 통화는 build/ko/trades*.py 의 call 을 같은 이야기로 늘린 것이고,
2장의 마지막 질문은 그 업종의 refuse 규칙에 걸려 사람에게 넘어간다."""

HONEST_KO = "각본이 있는 시연 · 예시 데이터 · 두 목소리는 이 데모를 위해 만든 합성 음성입니다 · 금액은 예시 요금표입니다."
HONEST_EN = "Scripted simulation · sample data · both voices were synthesised for this demo · figures are an example price list."
HAND_KO = ["두 채널의 대화 전체", "받아 적은 항목 전부, 출처와 함께"]
HAND_EN = ["The whole conversation, both channels", "Every captured field, with its source"]

SCRIPTS = {

 # ───────────────────────────── 방역 · 해충방제 ─────────────────────────────
 "pest-control": {
  "ko": {
   "biz": "클린가드방역", "owner": "사장님",
   "meta": "화요일 11:16 PM · 영업 종료 후 · 가상의 방역업체", "callTime": "11:16 PM", "chan": "카카오톡",
   "chapters": ["밤 11:16, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 사장님 화면"],
   "chapterSubs": ["원룸 바퀴벌레 · 견적 · 내일 오후 2시 예약", "시공 시간 · 약제 안전 질문은 사람에게", "예약 · 견적서 · 기사 할 일 · 답변 대기"],
   "sys": {"ring": "밤 11:16 — 전화벨이 울립니다. 사무실은 닫혔습니다.",
           "chat": "다음 날 아침 7:40 — 같은 손님이 카카오톡으로.",
           "morning": "오전 9:00 — 사장님 화면."},
   "customer": {"name": "박서연", "phone": "010-7731-24··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 클린가드방역입니다. 지금은 사무실이 닫힌 시간이지만, 시공 예약과 문의는 제가 도와드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "원룸인데 바퀴가 자꾸 나와요. 얼마고 언제 오실 수 있나요?",
     "side": [{"field": {"k": "요청", "v": "바퀴벌레 — 원룸 · 빠른 시공", "src": "통화에서"}}]},
    {"who": "ai", "text": "밤에 벌레 보시면 정말 불편하시죠. 요금표 기준으로 원룸 1회 시공은 9만원부터이고, 자주 보이시면 2주 뒤 재시공을 포함한 2회 15만원을 권해 드려요. 내일 오후 2시와 5시가 비어 있어요. 어느 쪽이 편하세요?",
     "side": [{"field": {"k": "견적", "v": "1회 90,000원 · 2회 150,000원", "src": "사장님 요금표"}}]},
    {"who": "user", "text": "내일 2시요. 근데 약 냄새 심한가요? 고양이가 있어요.",
     "side": [{"field": {"k": "반려동물", "v": "고양이 1마리", "src": "본인 발화"}}]},
    {"who": "ai", "text": "반려동물이 있는 집은 약제와 시공 방법이 달라져서, 기사님이 방문 전에 확인 전화를 드릴 거예요. 성함과 연락처를 말씀해 주시겠어요?"},
    {"who": "user", "text": "박서연이고요, 010-7731-2415예요.",
     "side": [{"field": {"k": "이름", "v": "박서연", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-7731-24··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "박서연 님, 내일 오후 2시로 예약되었습니다. 확인 문자를 지금 보내 드릴게요. 벌레는 주로 어디서 보셨어요?",
     "side": [{"field": {"k": "시공", "v": "내일 오후 2:00 · 1회", "src": "캘린더의 빈 시간"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "예약 확정", "v": "내일 오후 2:00 · 캘린더에 들어감 · 확인 문자 발송"}}]},
    {"who": "user", "text": "싱크대 아래랑 화장실이요.",
     "side": [{"field": {"k": "목격 위치", "v": "싱크대 아래 · 화장실 — 종은 미확정", "src": "본인 발화 · 진단 아님"}}]},
    {"who": "ai", "text": "싱크대 아래와 화장실로 적어 두었어요. 내일까지는 음식물을 밀봉해 두시고, 기사님이 오전에 전화드릴 거예요. 내일 뵙겠습니다.",
     "side": [{"work": {"icon": "#", "k": "견적 #3108", "v": "1회 90,000원 — 사장님 요금표에서"}},
              {"work": {"icon": "@", "k": "담당·기한", "v": "기사 최민호 배정 · 방문 전 반려동물 확인 전화"}},
              {"work": {"icon": "↻", "k": "재시공 안내", "v": "2주 뒤 재시공 안내 문자 초안 — 발송 전 사장님 확인"}}]},
    {"who": "user", "text": "네, 감사합니다."},
    {"who": "ai", "text": "감사합니다. 편안한 밤 되세요."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "어제 예약한 박서연인데, 시공은 얼마나 걸리나요?"},
    {"who": "ai", "when": "+2 sec", "text": "원룸은 30분 안팎이에요. 오늘 오후 2시 예약은 그대로 유효합니다.", "merge": True},
    {"who": "user", "when": "7:41 AM", "text": "약이 고양이한테는 안전한 거 맞죠? 어디 두면 되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "약제가 반려동물에게 안전한지는 기사님이 직접 확인하고 안내해 드려야 합니다. 대화 내용을 그대로 전달해 두었고, 방문 전에 전화드리겠습니다.", "handoff": True}
   ],
   "handoff": HAND_KO + ["멈춘 이유: 약제의 안전성은 기사가 보고 판단할 일이지, 서류에 있는 사실이 아닙니다"],
   "morning": [
    {"icon": "✓", "k": "새 예약 1건", "v": "박서연 · 오늘 오후 2:00 · 캘린더에 있음"},
    {"icon": "#", "k": "견적서 #3108", "v": "90,000원 · 문자로 발송됨 · 열람 확인"},
    {"icon": "@", "k": "기사 할 일", "v": "방문 전 반려동물 확인 전화 · 담당 최민호"},
    {"icon": "!", "k": "답변 대기 1건", "v": "약제 안전 문의 · 대화 전체 첨부 · 담당 최민호"}
   ],
   "person": {"when": "9:12 AM", "text": "기사 최민호입니다. 박서연 님, 반려동물 있는 집은 분사 대신 겔 약제로 시공하고, 고양이는 시공 동안 다른 방에 두시면 돼요. 정오쯤 전화드릴게요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 사장님이 자는 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "ClearLine Pest Control", "owner": "the owner",
   "meta": "Tuesday 11:16 PM · after hours · a fictional pest company", "callTime": "11:16 PM", "chan": "WhatsApp",
   "chapters": ["11:16 PM, the call", "Next morning, WhatsApp", "9:00 AM, the owner’s screen"],
   "chapterSubs": ["roaches in a studio · quote · 2 PM tomorrow booked", "how long it takes · the pet-safety question goes to a person", "booking · estimate · technician · one reply waiting"],
   "sys": {"ring": "11:16 PM — the phone rings. The office closed hours ago.",
           "chat": "Next morning, 7:40 AM — the same customer, on WhatsApp.",
           "morning": "9:00 AM — the owner’s screen."},
   "customer": {"name": "Maya Torres", "phone": "555-02··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling ClearLine Pest Control. The office is closed for the night, but I can book treatments and answer questions. How can I help?"},
    {"who": "user", "text": "Hi — I'm in a studio apartment and I keep seeing roaches. How much is it, and how soon can someone come?",
     "side": [{"field": {"k": "Request", "v": "Roaches — studio · soon", "src": "from the call"}}]},
    {"who": "ai", "text": "That's an unpleasant thing to find at night. From our rate card, a single treatment for a studio starts at one hundred fifty dollars, and if you're seeing them often I'd suggest the two-visit package at two hundred fifty, with a follow-up in two weeks. Tomorrow I have two in the afternoon or five. Which works better?",
     "side": [{"field": {"k": "Quote", "v": "Single $150 · two-visit $250", "src": "your rate card"}}]},
    {"who": "user", "text": "Two tomorrow. Is the spray strong-smelling? I have a cat.",
     "side": [{"field": {"k": "Pets", "v": "one cat", "src": "caller said it"}}]},
    {"who": "ai", "text": "With a pet in the home, the products and the method change, so the technician will call you before the visit to go over it. Can I get your name and a mobile number?"},
    {"who": "user", "text": "Maya Torres, five five five, zero two eight one.",
     "side": [{"field": {"k": "Name", "v": "Maya Torres", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-02··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, Maya. You're booked for tomorrow at two, and I'm texting you a confirmation now. Where have you mostly seen them?",
     "side": [{"field": {"k": "Visit", "v": "Tomorrow 2:00 PM · single", "src": "free in your calendar"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "Booked", "v": "Tomorrow 2:00 PM · in your calendar · confirmation text sent"}}]},
    {"who": "user", "text": "Under the kitchen sink and in the bathroom.",
     "side": [{"field": {"k": "Seen at", "v": "under the sink · bathroom — species not identified", "src": "caller said it · not a diagnosis"}}]},
    {"who": "ai", "text": "Noted — under the sink and the bathroom. Until tomorrow, keep food sealed, and the technician will call in the morning. See you at two.",
     "side": [{"work": {"icon": "#", "k": "Estimate #3108", "v": "Single treatment $150 — from your own rate card"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "assigned to Luis · pre-visit call about the cat"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "two-week follow-up text drafted — you approve before it sends"}}]},
    {"who": "user", "text": "Okay, thank you."},
    {"who": "ai", "text": "Thank you. Have a good night."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "Hi, Maya from last night — how long does the treatment take?"},
    {"who": "ai", "when": "+2 sec", "text": "About thirty minutes for a studio. Your two o'clock today is unchanged.", "merge": True},
    {"who": "user", "when": "7:41 AM", "text": "And the spray is safe for my cat, right? Where should I keep her?"},
    {"who": "ai", "when": "+2 sec", "text": "Whether a product is safe around your cat is for the technician to say, not me. I’ve passed our conversation along — he’ll call you before the visit.", "handoff": True}
   ],
   "handoff": HAND_EN + ["Why it stopped: product safety around a pet is the technician’s judgement, not a fact on file"],
   "morning": [
    {"icon": "✓", "k": "New booking", "v": "Maya Torres · today 2:00 PM · in the calendar"},
    {"icon": "#", "k": "Estimate #3108", "v": "$150 · sent by text · opened"},
    {"icon": "@", "k": "Technician task", "v": "pre-visit call about the cat · owner: Luis"},
    {"icon": "!", "k": "Waiting for a person", "v": "pet-safety question · full thread attached · owner: Luis"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Luis, your technician. Hi Maya — in homes with pets I use gel bait instead of a spray, and your cat can stay in a closed room while I work. I’ll call you around noon."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the owner slept.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────────── 건물관리 ─────────────────────────────
 "property-management": {
  "ko": {
   "biz": "한빛타운 관리사무소", "owner": "소장님",
   "meta": "화요일 1:04 AM · 관리사무소 퇴근 후 · 가상의 아파트", "callTime": "1:04 AM", "chan": "카카오톡",
   "chapters": ["새벽 1:04, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 소장님 화면"],
   "chapterSubs": ["천장 누수 · 긴급 판정 · 당직 기사 연결", "보수 일정 · 책임 질문은 사람에게", "긴급 처리 · 신고 기록 · 담당 · 답변 대기"],
   "sys": {"ring": "새벽 1:04 — 전화벨이 울립니다. 관리사무소는 6시에 닫았습니다.",
           "chat": "다음 날 아침 7:52 — 같은 입주민이 카카오톡으로.",
           "morning": "오전 9:00 — 소장님 화면."},
   "customer": {"name": "정우진", "phone": "010-2284-77··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 한빛타운 관리사무소입니다. 지금은 사무실이 닫힌 시간이지만, 급한 신고는 바로 연결해 드리고 나머지는 접수해 둘게요. 무슨 일이세요?"},
    {"who": "user", "text": "천장에서 물이 떨어져요. 지금 누구 없나요?",
     "side": [{"field": {"k": "신고 원문", "v": "천장에서 물이 떨어져요", "src": "통화에서"}}]},
    {"who": "ai", "text": "누수는 바로 처리해야 하는 신고예요. 야간 당직 기사님께 지금 연결해 드릴게요. 몇 동 몇 호이고, 물이 어디서 떨어지나요?",
     "side": [{"field": {"k": "긴급 판정", "v": "누수 — 접수가 아니라 즉시 연결", "src": "소장님 규칙"}}]},
    {"who": "user", "text": "103동 902호, 화장실 천장이에요.",
     "side": [{"field": {"k": "위치", "v": "103동 902호 · 화장실 천장", "src": "본인 발화"}}]},
    {"who": "ai", "text": "103동 902호 화장실 천장으로 접수했어요. 물 떨어지는 곳 바로 아래에 전등이나 콘센트가 있나요?"},
    {"who": "user", "text": "환풍기 바로 옆이에요."},
    {"who": "ai", "text": "그러면 안전을 위해 화장실 차단기를 먼저 내려 주세요. 기사님께 전달할 성함과 연락처를 말씀해 주시겠어요?"},
    {"who": "user", "text": "정우진이고요, 010-2284-7762예요.",
     "side": [{"field": {"k": "이름", "v": "정우진", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-2284-77··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "정우진 님, 야간 당직 기사님께 지금 연결합니다. 10분 안에 전화드리고 필요하면 바로 올라갈 거예요. 그동안 물 받을 통 하나 받쳐 두세요.",
     "side": [{"field": {"k": "연결", "v": "야간 당직 기사 · 1:07 AM", "src": "소장님 규칙"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "긴급 접수", "v": "103동 902호 누수 · 당직 기사 연결 · 차단기 안내"}},
              {"work": {"icon": "@", "k": "담당·기한", "v": "당직 기사 출동 · 아침 9시 전 소장님께 보고"}},
              {"work": {"icon": "↻", "k": "결과 회신", "v": "처리 뒤 신고 세대 회신 문자 초안 — 발송 전 소장님 확인"}}]},
    {"who": "user", "text": "네, 빨리 부탁드려요."},
    {"who": "ai", "text": "네, 바로 연결할게요. 잠시만 기다려 주세요."}
   ],
   "chat": [
    {"who": "user", "when": "7:52 AM", "text": "902호 정우진인데, 어젯밤 기사님이 물은 잡아 주셨어요. 천장 자국 보수는 언제 되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "후속 보수로 접수되어 있어요. 오늘 오전 담당자가 일정을 잡아 연락드릴 예정입니다.", "merge": True},
    {"who": "user", "when": "7:53 AM", "text": "이거 윗집 잘못이죠? 수리비는 윗집이 내는 거죠?"},
    {"who": "ai", "when": "+2 sec", "text": "누구 책임인지와 수리비 부담은 확인 후 관리사무소가 정할 일이라 제가 답할 수 없습니다. 대화 내용을 그대로 전달해 두었고, 오전 중에 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HAND_KO + ["멈춘 이유: 책임과 수리비 부담은 확인 후의 판단이지, 서류에 있는 사실이 아닙니다"],
   "morning": [
    {"icon": "✓", "k": "긴급 신고 1건 처리", "v": "103동 902호 · 당직 기사 1:12 AM 도착 · 급수 차단"},
    {"icon": "#", "k": "신고 기록 #0917", "v": "신고 원문 · 긴급 판정 · 연결 시각 · 소장님 열람"},
    {"icon": "@", "k": "담당 할 일", "v": "천장 보수 일정 · 윗집 확인 방문 · 담당 김상훈"},
    {"icon": "!", "k": "답변 대기 1건", "v": "책임 · 수리비 문의 · 대화 전체 첨부 · 담당 김상훈"}
   ],
   "person": {"when": "9:12 AM", "text": "담당 김상훈입니다. 정우진 님, 오늘 오후 2시에 윗집 배관을 확인하러 갑니다. 세대 배관인지 공용 배관인지 보고 나서 부담 기준을 정확히 알려 드릴게요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 소장님이 자는 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Harbor Court Management Office", "owner": "the property manager",
   "meta": "Tuesday 1:04 AM · after hours · a fictional apartment complex", "callTime": "1:04 AM", "chan": "WhatsApp",
   "chapters": ["1:04 AM, the call", "Next morning, WhatsApp", "9:00 AM, the manager’s screen"],
   "chapterSubs": ["ceiling leak · urgent · on-call tech connected", "repair timing · the blame question goes to a person", "incident · log · task · one reply waiting"],
   "sys": {"ring": "1:04 AM — the phone rings. The office closed at six.",
           "chat": "Next morning, 7:52 AM — the same resident, on WhatsApp.",
           "morning": "9:00 AM — the property manager’s screen."},
   "customer": {"name": "Daniel Reyes", "phone": "555-03··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Harbor Court Management. The office is closed, but I connect urgent reports right away and log everything else for the morning. What's happening?"},
    {"who": "user", "text": "There's water coming through my ceiling. Is anyone there right now?",
     "side": [{"field": {"k": "Report", "v": "water coming through the ceiling", "src": "from the call"}}]},
    {"who": "ai", "text": "A leak is urgent, so I'm getting the on-call technician for you now. Which building and apartment, and where exactly is the water coming in?",
     "side": [{"field": {"k": "Triage", "v": "leak — connect now, not a booking", "src": "your emergency rule"}}]},
    {"who": "user", "text": "Building three, apartment 902. It's the bathroom ceiling.",
     "side": [{"field": {"k": "Location", "v": "Building 3 · apt 902 · bathroom ceiling", "src": "caller said it"}}]},
    {"who": "ai", "text": "Building three, 902, bathroom ceiling — logged. Is there a light fixture or an outlet right under where it's dripping?"},
    {"who": "user", "text": "It's right next to the exhaust fan."},
    {"who": "ai", "text": "Then please switch off the bathroom breaker first, to be safe. Can I get your name and a mobile number so the technician has it?"},
    {"who": "user", "text": "Daniel Reyes, five five five, zero three six two.",
     "side": [{"field": {"k": "Name", "v": "Daniel Reyes", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-03··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, Daniel. I'm connecting you to the on-call technician now — they'll call within ten minutes and come up if needed. Put a bucket under it in the meantime.",
     "side": [{"field": {"k": "Connected", "v": "on-call technician · 1:07 AM", "src": "your emergency rule"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "Urgent incident", "v": "Building 3, apt 902 leak · on-call tech connected · breaker advice given"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "on-call tech dispatched · report to the manager before 9:00"}},
              {"work": {"icon": "↻", "k": "Result reply", "v": "post-repair message to the resident drafted — you approve before it sends"}}]},
    {"who": "user", "text": "Okay, please hurry."},
    {"who": "ai", "text": "Connecting you now. Please hold on."}
   ],
   "chat": [
    {"who": "user", "when": "7:52 AM", "text": "Hi, Daniel from 902 — the tech stopped the water last night. When does the ceiling get repaired?"},
    {"who": "ai", "when": "+2 sec", "text": "It’s logged as a follow-up repair. Maintenance will schedule it and message you this morning.", "merge": True},
    {"who": "user", "when": "7:53 AM", "text": "It’s the upstairs unit’s fault, right? So they pay for the repair, not me?"},
    {"who": "ai", "when": "+2 sec", "text": "Who’s responsible and who pays is a decision for the office after they’ve inspected — not something I can call. I’ve passed the whole thread along; someone will reply this morning.", "handoff": True}
   ],
   "handoff": HAND_EN + ["Why it stopped: fault and repair cost are a judgement after inspection, not a fact on file"],
   "morning": [
    {"icon": "✓", "k": "Urgent incident handled", "v": "Building 3, apt 902 · on-call tech on site 1:12 AM · water shut off"},
    {"icon": "#", "k": "Incident log #0917", "v": "report in the resident’s words · triage · connect time · read by the manager"},
    {"icon": "@", "k": "Maintenance task", "v": "schedule ceiling repair · inspect the unit above · owner: Tom"},
    {"icon": "!", "k": "Waiting for a person", "v": "who-pays question · full thread attached · owner: Tom"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Tom from maintenance. Hi Daniel — we’re inspecting the unit above at two today. Once we know whether it’s their plumbing or the building’s, we’ll tell you exactly who covers the repair."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the manager slept.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────────── 부동산 ─────────────────────────────
 "real-estate": {
  "ko": {
   "biz": "한결부동산", "owner": "소장님",
   "meta": "수요일 7:24 PM · 소장님 임장 중 · 가상의 중개사무소", "callTime": "7:24 PM", "chan": "카카오톡",
   "chapters": ["저녁 7:24, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 소장님 화면"],
   "chapterSubs": ["24평 전세 · 등록 조건 · 내일 오후 3시 임장", "반려동물 · 보증금 협의는 사람에게", "임장 · 매물 카드 · 소장님 · 답변 대기"],
   "sys": {"ring": "저녁 7:24 — 전화벨이 울립니다. 소장님은 임장을 나가 있습니다.",
           "chat": "다음 날 아침 7:40 — 같은 손님이 카카오톡으로.",
           "morning": "오전 9:00 — 소장님 화면."},
   "customer": {"name": "이하늘", "phone": "010-5529-88··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 한결부동산입니다. 소장님이 지금 임장 중이라 제가 대신 받고 있어요. 매물 확인과 방문 예약을 도와드릴 수 있습니다. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "네이버에 올라온 24평 전세 아직 있나요? 주차는 몇 대예요?",
     "side": [{"field": {"k": "문의 매물", "v": "24평 전세 · 포털 유입", "src": "통화에서"}}]},
    {"who": "ai", "text": "네, 아직 있어요. 주차는 세대당 1대 배정이고 방문 주차는 별도예요. 보증금은 올려 두신 대로 3억 2천만원, 관리비는 월 12만원이에요. 내일 오전 11시나 오후 3시에 보실 수 있어요.",
     "side": [{"field": {"k": "조건", "v": "보증금 3억 2천 · 관리비 월 12만원 · 주차 1대", "src": "등록 매물 조건"}}]},
    {"who": "user", "text": "오후 3시에 볼게요. 근데 혹시 중개사님이세요?"},
    {"who": "ai", "text": "아니에요, 저는 사람이 아니라 인공지능 상담원이에요. 등록된 매물 정보와 방문 예약까지 도와드리고, 조건이나 계약 이야기는 소장님이 직접 하세요. 성함과 연락처를 말씀해 주시겠어요?",
     "side": [{"field": {"k": "구분", "v": "임차 (전세) · AI 응대임을 밝힘", "src": "소장님 규칙"}}]},
    {"who": "user", "text": "이하늘이고요, 010-5529-8834예요.",
     "side": [{"field": {"k": "이름", "v": "이하늘", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-5529-88··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "이하늘 님, 내일 오후 3시 방문으로 잡았어요. 소장님이 미리 한 번 연락드리고 현장에서 만나 뵐 거예요. 입주는 언제쯤 생각하세요?",
     "side": [{"field": {"k": "임장", "v": "내일 오후 3:00", "src": "캘린더의 빈 시간"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "임장 예약", "v": "내일 오후 3:00 · 소장님 캘린더에 들어감 · 주소 문자 발송"}}]},
    {"who": "user", "text": "다음 달 말이요.",
     "side": [{"field": {"k": "희망 입주", "v": "다음 달 말", "src": "본인 발화"}}]},
    {"who": "ai", "text": "다음 달 말로 적어 둘게요. 신분 확인은 현장에서 하고, 주소는 지금 문자로 보내 드릴게요. 내일 뵙겠습니다.",
     "side": [{"work": {"icon": "#", "k": "매물 카드 #2417", "v": "24평 전세 · 등록 조건 그대로 — 협의 없음"}},
              {"work": {"icon": "@", "k": "담당·기한", "v": "소장님 · 내일 2:30까지 사전 연락"}},
              {"work": {"icon": "↻", "k": "후속 문자", "v": "임장 뒤 D+1 안내 문자 초안 — 발송 전 소장님 확인"}}]},
    {"who": "user", "text": "네, 감사합니다."},
    {"who": "ai", "text": "감사합니다. 좋은 저녁 되세요."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "어제 예약한 이하늘인데, 그 집 강아지 키워도 되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "등록된 조건에 반려동물 가능으로 되어 있어요. 오늘 오후 3시 방문은 그대로 유효합니다.", "merge": True},
    {"who": "user", "when": "7:42 AM", "text": "보증금 3억으로 해 주시면 바로 계약할게요. 되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "보증금 협의는 소장님이 직접 하실 일이라 제가 답할 수 없습니다. 대화 내용을 그대로 전달해 두었고, 오전 중에 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HAND_KO + ["멈춘 이유: 보증금 협의는 등록된 사실이 아니라 중개사의 판단입니다"],
   "morning": [
    {"icon": "✓", "k": "새 임장 1건", "v": "이하늘 · 오늘 오후 3:00 · 캘린더에 있음"},
    {"icon": "#", "k": "매물 카드 #2417", "v": "등록 조건 · 문자로 발송됨 · 열람 확인"},
    {"icon": "@", "k": "소장님 할 일", "v": "오후 2:30까지 사전 연락 · 현장 신분 확인"},
    {"icon": "!", "k": "답변 대기 1건", "v": "보증금 협의 문의 · 대화 전체 첨부 · 담당 소장님"}
   ],
   "person": {"when": "9:12 AM", "text": "소장 박정호입니다. 이하늘 님, 보증금은 임대인 의사를 확인해야 해서 오늘 물어보고 3시 전에 말씀드릴게요. 현장에서 뵙겠습니다."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 소장님이 임장 나가 있는 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Maple Row Realty", "owner": "the broker",
   "meta": "Wednesday 7:24 PM · broker out on showings · a fictional brokerage", "callTime": "7:24 PM", "chan": "WhatsApp",
   "chapters": ["7:24 PM, the call", "Next morning, WhatsApp", "9:00 AM, the broker’s screen"],
   "chapterSubs": ["two-bedroom listing · facts from the listing · 3 PM showing", "pets · the rent offer goes to a person", "showing · listing card · broker · one reply waiting"],
   "sys": {"ring": "7:24 PM — the phone rings. The broker is out at a showing.",
           "chat": "Next morning, 7:40 AM — the same applicant, on WhatsApp.",
           "morning": "9:00 AM — the broker’s screen."},
   "customer": {"name": "Olivia Park", "phone": "555-04··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Maple Row Realty. The broker is out at a showing, so I'm answering for the office. I can confirm listings and book viewings. How can I help?"},
    {"who": "user", "text": "Is that two-bedroom on Alder Street still available? And how many parking spaces does it have?",
     "side": [{"field": {"k": "Listing", "v": "2-bed rental · Alder Street · from the portal", "src": "from the call"}}]},
    {"who": "ai", "text": "Yes, it's still available. Parking is one assigned space, and visitors park on the street. From the listing, rent is twenty-four hundred a month with a one-month deposit. I can show it tomorrow at eleven or at three.",
     "side": [{"field": {"k": "Terms", "v": "$2,400 a month · 1-month deposit · 1 space", "src": "from the listing"}}]},
    {"who": "user", "text": "Three works. Sorry — are you the agent?"},
    {"who": "ai", "text": "No, I'm an AI assistant. I can share what's in the listing and book the viewing; anything about terms or the lease is for the broker. Can I get your name and a mobile number?",
     "side": [{"field": {"k": "Type", "v": "rental applicant · told it is an AI", "src": "your rule"}}]},
    {"who": "user", "text": "Olivia Park, five five five, zero four one nine.",
     "side": [{"field": {"k": "Name", "v": "Olivia Park", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-04··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, Olivia. You're booked for tomorrow at three, and the broker will call you beforehand and meet you at the property. When are you hoping to move in?",
     "side": [{"field": {"k": "Showing", "v": "Tomorrow 3:00 PM", "src": "free in the broker’s diary"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "Showing booked", "v": "Tomorrow 3:00 PM · in the broker’s diary · address texted"}}]},
    {"who": "user", "text": "End of next month.",
     "side": [{"field": {"k": "Move-in", "v": "end of next month", "src": "caller said it"}}]},
    {"who": "ai", "text": "End of next month — noted. ID is checked at the property, and I'm texting you the address now. See you tomorrow.",
     "side": [{"work": {"icon": "#", "k": "Listing card #2417", "v": "2-bed · Alder Street · terms as listed — nothing negotiated"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "the broker · pre-showing call by 2:30"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "day-after-showing text drafted — you approve before it sends"}}]},
    {"who": "user", "text": "Great, thank you."},
    {"who": "ai", "text": "Thank you. Have a good evening."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "Hi, Olivia from yesterday — does the Alder Street unit allow dogs?"},
    {"who": "ai", "when": "+2 sec", "text": "The listing says small pets are allowed with a pet deposit. Your three o’clock today is unchanged.", "merge": True},
    {"who": "user", "when": "7:42 AM", "text": "Would they take twenty-two hundred? I’d sign today."},
    {"who": "ai", "when": "+2 sec", "text": "Negotiating the rent is for the broker, not for me. I’ve passed our conversation along — she’ll call you this morning.", "handoff": True}
   ],
   "handoff": HAND_EN + ["Why it stopped: a rent offer is a negotiation, not a fact in the listing"],
   "morning": [
    {"icon": "✓", "k": "New showing", "v": "Olivia Park · today 3:00 PM · in the diary"},
    {"icon": "#", "k": "Listing card #2417", "v": "terms as listed · sent by text · opened"},
    {"icon": "@", "k": "Broker task", "v": "pre-showing call by 2:30 · ID check on site · owner: Dana"},
    {"icon": "!", "k": "Waiting for a person", "v": "rent offer · full thread attached · owner: Dana"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Dana, the broker. Hi Olivia — I’ll put the twenty-two hundred to the owner today and let you know before we meet at three."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the broker was out showing homes.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────────── 자동차 정비 ─────────────────────────────
 "auto-repair": {
  "ko": {
   "biz": "튼튼모터스", "owner": "사장님",
   "meta": "수요일 4:47 PM · 작업 중 · 가상의 공업사", "callTime": "4:47 PM", "chan": "카카오톡",
   "chapters": ["오후 4:47, 전화", "다음 날 아침, 카카오톡", "오전 8:30, 사장님 화면"],
   "chapterSubs": ["브레이크 소음 · 요금표 범위 · 내일 9시 입고", "대차 질문 · 보험 질문은 사람에게", "입고 · 예상 견적 · 재고 확인 · 답변 대기"],
   "sys": {"ring": "오후 4:47 — 전화벨이 울립니다. 사장님은 리프트 아래에 있습니다.",
           "chat": "다음 날 아침 7:50 — 같은 손님이 카카오톡으로.",
           "morning": "오전 8:30 — 사장님 화면."},
   "customer": {"name": "최민재", "phone": "010-3347-90··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 튼튼모터스입니다. 사장님이 지금 작업 중이라 제가 대신 받고 있어요. 입고 예약과 문의를 도와드릴 수 있습니다. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "브레이크에서 쇠 갈리는 소리가 나는데 오늘 볼 수 있나요?",
     "side": [{"field": {"k": "증상 원문", "v": "브레이크에서 쇠 갈리는 소리", "src": "통화에서"}}]},
    {"who": "ai", "text": "패드가 닳았을 가능성이 있지만, 정확한 건 차를 봐야 알아요. 요금표 기준으로 패드 교체는 앞바퀴 기준 12만원부터이고, 디스크까지 손봐야 하면 달라져요. 오늘은 오후 6시 이후에 리프트가 비고, 내일은 오전 9시가 가능해요.",
     "side": [{"field": {"k": "예상 범위", "v": "패드 교체 앞바퀴 120,000원부터 — 최종은 차를 보고", "src": "사장님 요금표"}}]},
    {"who": "user", "text": "내일 9시로 할게요. 차는 아반떼예요.",
     "side": [{"field": {"k": "차종", "v": "아반떼", "src": "본인 발화"}}]},
    {"who": "ai", "text": "네, 내일 오전 9시 입고로 잡을게요. 성함과 연락처를 말씀해 주시겠어요?"},
    {"who": "user", "text": "최민재고요, 010-3347-9052예요.",
     "side": [{"field": {"k": "이름", "v": "최민재", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-3347-90··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "최민재 님, 내일 오전 9시 입고 예약되었어요. 확인 문자를 지금 보내 드릴 테니 차량번호를 답장으로 남겨 주시면 패드 재고를 미리 확인해 둘게요. 지금 제동은 잘 되세요?",
     "side": [{"field": {"k": "입고", "v": "내일 오전 9:00", "src": "캘린더의 빈 시간"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "입고 예약", "v": "내일 09:00 · 리프트 일정에 들어감 · 확인 문자 발송"}}]},
    {"who": "user", "text": "제동은 잘 돼요. 소리만 나요.",
     "side": [{"field": {"k": "안전 확인", "v": "제동 정상 — 즉시 연결 아님", "src": "본인 발화 · 진단 아님"}}]},
    {"who": "ai", "text": "그러면 내일까지는 급제동을 피하시고, 브레이크가 밀리거나 연기가 나면 바로 이 번호로 전화 주세요. 내일 아침에 뵙겠습니다.",
     "side": [{"work": {"icon": "#", "k": "예상 견적 #1583", "v": "패드 교체 120,000원부터 — 사장님 요금표에서"}},
              {"work": {"icon": "@", "k": "담당·기한", "v": "사무실 정수빈 · 차량번호 회신 후 패드 재고 확인 · 내일 8:30까지"}},
              {"work": {"icon": "↻", "k": "후속 문자", "v": "차량번호 무응답 시 저녁 안내 문자 초안 — 발송 전 사장님 확인"}}]},
    {"who": "user", "text": "네, 감사합니다."},
    {"who": "ai", "text": "감사합니다. 안전 운전하세요."}
   ],
   "chat": [
    {"who": "user", "when": "7:50 AM", "text": "어제 예약한 최민재인데, 차 맡기는 동안 대차 되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "대차는 없고, 대기실에서 기다리실 수 있어요. 패드 교체는 보통 1시간 안팎입니다. 오늘 9시 입고는 그대로 유효합니다.", "merge": True},
    {"who": "user", "when": "7:51 AM", "text": "이거 보험으로 처리되나요? 자기부담금은 얼마예요?"},
    {"who": "ai", "when": "+2 sec", "text": "보험 적용 여부와 자기부담금은 보험사가 정하는 것이라 제가 답할 수 없습니다. 대화 내용을 그대로 전달해 두었고, 입고 전에 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HAND_KO + ["멈춘 이유: 보험 처리 가능 여부는 보험사의 판단이지, 서류에 있는 사실이 아닙니다"],
   "morning": [
    {"icon": "✓", "k": "새 입고 1건", "v": "최민재 · 아반떼 · 오늘 09:00 · 리프트 일정에 있음"},
    {"icon": "#", "k": "예상 견적 #1583", "v": "120,000원부터 · 문자로 발송됨 · 열람 확인"},
    {"icon": "@", "k": "사무실 할 일", "v": "차량번호 회신 확인 · 패드 재고 확인 · 담당 정수빈"},
    {"icon": "!", "k": "답변 대기 1건", "v": "보험 처리 문의 · 대화 전체 첨부 · 담당 정수빈"}
   ],
   "person": {"when": "8:41 AM", "text": "사무실 정수빈입니다. 최민재 님, 패드 같은 소모품은 보험 적용이 안 되는 경우가 많아요. 입고하시면 보험사에 같이 확인해 드릴게요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 사장님이 리프트 아래 있는 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Ironwood Auto Repair", "owner": "the owner",
   "meta": "Wednesday 4:47 PM · owner under a lift · a fictional shop", "callTime": "4:47 PM", "chan": "WhatsApp",
   "chapters": ["4:47 PM, the call", "Next morning, WhatsApp", "8:30 AM, the owner’s screen"],
   "chapterSubs": ["grinding brakes · rate-card range · 9 AM drop-off", "loaner question · the insurance question goes to a person", "drop-off · estimate · parts check · one reply waiting"],
   "sys": {"ring": "4:47 PM — the phone rings. The owner is under a lift.",
           "chat": "Next morning, 7:50 AM — the same customer, on WhatsApp.",
           "morning": "8:30 AM — the owner’s screen."},
   "customer": {"name": "Chris Nguyen", "phone": "555-05··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Ironwood Auto Repair. The owner is under a car right now, so I'm answering for the shop. I can book drop-offs and answer questions. How can I help?"},
    {"who": "user", "text": "My brakes are making a metal grinding noise. Can you look at it today?",
     "side": [{"field": {"k": "Symptom", "v": "metal grinding noise from the brakes", "src": "from the call"}}]},
    {"who": "ai", "text": "That could be worn pads, but nobody can say for sure without seeing the car. From our rate card, front pads start at one hundred eighty dollars, more if the rotors need work. Today the lift frees up after six, or I have nine tomorrow morning.",
     "side": [{"field": {"k": "Range", "v": "front pads from $180 — final after inspection", "src": "your rate card"}}]},
    {"who": "user", "text": "Nine tomorrow. It's a twenty nineteen Civic.",
     "side": [{"field": {"k": "Vehicle", "v": "2019 Civic", "src": "caller said it"}}]},
    {"who": "ai", "text": "Nine tomorrow it is. Can I get your name and a mobile number?"},
    {"who": "user", "text": "Chris Nguyen, five five five, zero five two four.",
     "side": [{"field": {"k": "Name", "v": "Chris Nguyen", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-05··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, Chris. You're booked for a nine o'clock drop-off tomorrow. I'm texting a confirmation now — reply with your plate number and we'll check pad stock before you arrive. Is the car still stopping normally?",
     "side": [{"field": {"k": "Drop-off", "v": "Tomorrow 9:00 AM", "src": "free in your calendar"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "Booked", "v": "Tomorrow 9:00 AM · on the lift schedule · confirmation text sent"}}]},
    {"who": "user", "text": "It stops fine, it's just the noise.",
     "side": [{"field": {"k": "Safety check", "v": "brakes working — not urgent", "src": "caller said it · not a diagnosis"}}]},
    {"who": "ai", "text": "Then go easy on hard braking until tomorrow, and if the pedal goes soft or you see smoke, call this number right away. See you at nine.",
     "side": [{"work": {"icon": "#", "k": "Estimate #1583", "v": "Front pads from $180 — from your own rate card"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "assigned to Kelly at the desk · check pad stock once the plate arrives · by 8:30"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "evening nudge for the plate drafted — you approve before it sends"}}]},
    {"who": "user", "text": "Will do, thanks."},
    {"who": "ai", "text": "Thank you. Drive safe."}
   ],
   "chat": [
    {"who": "user", "when": "7:50 AM", "text": "Hi, Chris from yesterday — do you have a loaner car while mine’s in?"},
    {"who": "ai", "when": "+2 sec", "text": "No loaners, but the waiting room is open and a pad job usually takes about an hour. Your nine o’clock is unchanged.", "merge": True},
    {"who": "user", "when": "7:51 AM", "text": "Will my insurance cover this? What’s my deductible?"},
    {"who": "ai", "when": "+2 sec", "text": "Coverage and deductibles are set by your insurer — not something I can answer. I’ve passed our conversation along; someone will reply before you arrive.", "handoff": True}
   ],
   "handoff": HAND_EN + ["Why it stopped: insurance coverage is the insurer’s decision, not a fact on file"],
   "morning": [
    {"icon": "✓", "k": "New drop-off", "v": "Chris Nguyen · 2019 Civic · today 9:00 AM · on the lift schedule"},
    {"icon": "#", "k": "Estimate #1583", "v": "front pads from $180 · sent by text · opened"},
    {"icon": "@", "k": "Desk task", "v": "confirm the plate reply · check pad stock · owner: Kelly"},
    {"icon": "!", "k": "Waiting for a person", "v": "insurance question · full thread attached · owner: Kelly"}
   ],
   "person": {"when": "8:41 AM", "text": "This is Kelly at the desk. Hi Chris — wear items like pads usually aren’t covered, but bring your policy details and we’ll check with your insurer when you drop off."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the owner was under a lift.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────────── 이사 · 용달 ─────────────────────────────
 "movers": {
  "ko": {
   "biz": "든든이사", "owner": "사장님",
   "meta": "월요일 9:33 PM · 사장님 현장 중 · 가상의 이사업체", "callTime": "9:33 PM", "chan": "카카오톡",
   "chapters": ["밤 9:33, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 사장님 화면"],
   "chapterSubs": ["원룸에서 투룸 · 금액 범위 · 목요일 방문 견적", "포장 방식 · 파손 보상 질문은 사람에게", "방문 견적 · 범위 기록 · 사장님 · 답변 대기"],
   "sys": {"ring": "밤 9:33 — 전화벨이 울립니다. 사장님은 아직 다른 집 소파를 나르고 있습니다.",
           "chat": "다음 날 아침 7:40 — 같은 손님이 카카오톡으로.",
           "morning": "오전 9:00 — 사장님 화면."},
   "customer": {"name": "강도윤", "phone": "010-6612-33··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 든든이사입니다. 사장님이 지금 현장에 계셔서 제가 대신 받고 있어요. 견적 상담과 방문 견적 예약을 도와드릴 수 있습니다. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "다음 달 15일에 원룸에서 투룸으로 이사하는데 얼마나 나올까요?",
     "side": [{"field": {"k": "희망 날짜", "v": "다음 달 15일 (토)", "src": "통화에서"}}, {"field": {"k": "짐 규모", "v": "원룸 → 투룸", "src": "통화에서"}}]},
    {"who": "ai", "text": "짐 양에 따라 달라서 정확한 금액은 방문 견적 후에 나와요. 원룸에서 투룸 정도면 보통 45만원에서 70만원 사이예요. 다음 달 15일은 토요일이라 일정이 빨리 차는데, 이번 주 목요일 저녁 7시에 방문 견적이 가능해요.",
     "side": [{"field": {"k": "안내 범위", "v": "450,000원 ~ 700,000원 — 확정은 방문 견적", "src": "사장님 요금표"}}]},
    {"who": "user", "text": "목요일 7시 좋아요. 지금 사는 데는 엘리베이터 없는 3층이에요.",
     "side": [{"field": {"k": "층수 · 엘리베이터", "v": "3층 · 엘리베이터 없음 — 사다리차 확인 필요", "src": "본인 발화"}}]},
    {"who": "ai", "text": "엘리베이터 없는 3층으로 적어 둘게요. 사다리차가 필요할 수 있어서 방문 때 같이 확인할 거예요. 성함과 연락처, 지금 주소를 말씀해 주시겠어요?"},
    {"who": "user", "text": "강도윤이고요, 010-6612-3378, 마포구 성산동이에요.",
     "side": [{"field": {"k": "이름", "v": "강도윤", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-6612-33··", "src": "발신번호와 일치"}}, {"field": {"k": "출발지", "v": "마포구 성산동 · 3층", "src": "본인 발화"}}]},
    {"who": "ai", "text": "강도윤 님, 목요일 저녁 7시 방문 견적으로 잡았어요. 확인 문자를 지금 보내 드릴게요. 이사 가시는 곳 주소도 알고 계세요?",
     "side": [{"field": {"k": "방문 견적", "v": "목 저녁 7:00", "src": "캘린더의 빈 시간"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "방문 견적 예약", "v": "목 19:00 · 캘린더에 들어감 · 확인 문자 발송"}}]},
    {"who": "user", "text": "은평구 응암동이고, 거긴 엘리베이터 있어요.",
     "side": [{"field": {"k": "도착지", "v": "은평구 응암동 · 엘리베이터 있음", "src": "본인 발화"}}]},
    {"who": "ai", "text": "응암동, 엘리베이터 있음으로 적어 뒀어요. 이사 날짜는 방문 견적 뒤 계약할 때 확정되니, 15일은 우선 희망일로만 잡아 둘게요. 목요일에 뵙겠습니다.",
     "side": [{"work": {"icon": "#", "k": "안내 범위 #2266", "v": "450,000 ~ 700,000원 — 사장님 요금표에서 · 확정 아님"}},
              {"work": {"icon": "@", "k": "담당·기한", "v": "사장님 · 목 19:00 방문 견적 · 사다리차 확인"}},
              {"work": {"icon": "↻", "k": "후속 문자", "v": "견적 뒤 D+1 안내 문자 초안 — 발송 전 사장님 확인"}}]},
    {"who": "user", "text": "네, 감사합니다."},
    {"who": "ai", "text": "감사합니다. 편안한 밤 되세요."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "어제 예약한 강도윤인데, 포장이사랑 반포장 차이가 뭐예요?"},
    {"who": "ai", "when": "+2 sec", "text": "포장이사는 저희가 짐을 싸고 풀어 드리고, 반포장은 큰 짐만 옮기고 잔짐은 직접 싸시는 거예요. 목요일 방문 때 두 가지 견적을 다 받으실 수 있습니다.", "merge": True},
    {"who": "user", "when": "7:42 AM", "text": "이사 중에 TV 깨지면 새 걸로 전액 보상되는 거죠?"},
    {"who": "ai", "when": "+2 sec", "text": "파손 보상 범위는 보험과 약관에 따라 사장님이 직접 설명드려야 하는 부분이라 제가 약속할 수 없습니다. 대화 내용을 그대로 전달해 두었고, 오전 중에 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HAND_KO + ["멈춘 이유: 파손 보상 범위는 약관에 따른 약속이지, 제가 정할 사실이 아닙니다"],
   "morning": [
    {"icon": "✓", "k": "새 방문 견적 1건", "v": "강도윤 · 목 19:00 · 성산동 3층 · 캘린더에 있음"},
    {"icon": "#", "k": "안내 범위 #2266", "v": "450,000 ~ 700,000원 · 문자로 발송됨 · 열람 확인"},
    {"icon": "@", "k": "사장님 할 일", "v": "목 19:00 방문 견적 · 사다리차 · 인력 확인"},
    {"icon": "!", "k": "답변 대기 1건", "v": "파손 보상 문의 · 대화 전체 첨부 · 담당 사장님"}
   ],
   "person": {"when": "9:12 AM", "text": "사장 이재훈입니다. 강도윤 님, 보상은 가입하신 보험 조건에 따라 달라서 목요일 방문 때 약관을 보여 드리고 설명드릴게요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 사장님이 현장에 있는 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Northstar Movers", "owner": "the owner",
   "meta": "Monday 9:33 PM · crew still on a job · a fictional moving company", "callTime": "9:33 PM", "chan": "WhatsApp",
   "chapters": ["9:33 PM, the call", "Next morning, WhatsApp", "9:00 AM, the owner’s screen"],
   "chapterSubs": ["studio to two-bedroom · price range · Thursday survey", "packing options · the damage question goes to a person", "survey · range on file · owner · one reply waiting"],
   "sys": {"ring": "9:33 PM — the phone rings. The crew is still carrying someone else’s sofa.",
           "chat": "Next morning, 7:40 AM — the same customer, on WhatsApp.",
           "morning": "9:00 AM — the owner’s screen."},
   "customer": {"name": "Ethan Brooks", "phone": "555-06··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Northstar Movers. The owner is out on a job, so I'm answering for the office. I can give price ranges and book a pre-move survey. How can I help?"},
    {"who": "user", "text": "I'm moving from a studio to a two-bedroom on the fifteenth next month. Roughly what would that cost?",
     "side": [{"field": {"k": "Move date", "v": "15th next month (Saturday)", "src": "from the call"}}, {"field": {"k": "Size", "v": "studio → two-bedroom", "src": "from the call"}}]},
    {"who": "ai", "text": "It depends on how much you have, so the exact figure comes after a survey. From our rate card, a studio to two-bedroom move usually runs six hundred to a thousand dollars. The fifteenth is a Saturday and fills fast — I can do a survey this Thursday at seven in the evening.",
     "side": [{"field": {"k": "Range", "v": "$600 to $1,000 — final after the survey", "src": "your rate card"}}]},
    {"who": "user", "text": "Thursday at seven works. My current place is a third-floor walk-up, no elevator.",
     "side": [{"field": {"k": "Access", "v": "3rd floor · no elevator — extra crew to confirm", "src": "caller said it"}}]},
    {"who": "ai", "text": "Third floor, no elevator — noted. That may need extra crew, and the surveyor will confirm on Thursday. Can I get your name, a mobile number, and the address you're moving from?"},
    {"who": "user", "text": "Ethan Brooks, five five five, zero six three one. I'm at forty-two Elm Street.",
     "side": [{"field": {"k": "Name", "v": "Ethan Brooks", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-06··", "src": "matches caller ID"}}, {"field": {"k": "From", "v": "42 Elm Street · 3rd floor", "src": "caller said it"}}]},
    {"who": "ai", "text": "Thank you, Ethan. Your survey is booked for Thursday at seven, and I'm texting a confirmation now. Do you have the new address too?",
     "side": [{"field": {"k": "Survey", "v": "Thu 7:00 PM", "src": "free in your calendar"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "Survey booked", "v": "Thu 7:00 PM · in your calendar · confirmation text sent"}}]},
    {"who": "user", "text": "Yes, one ten Oakridge Avenue, and that building has an elevator.",
     "side": [{"field": {"k": "To", "v": "110 Oakridge Avenue · elevator", "src": "caller said it"}}]},
    {"who": "ai", "text": "Oakridge, with an elevator — noted. The move date is confirmed with the contract after the survey, so the fifteenth is down as your preferred date for now. See you Thursday.",
     "side": [{"work": {"icon": "#", "k": "Range on file #2266", "v": "$600 to $1,000 — from your own rate card · not a quote"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "the owner · survey Thu 7:00 PM · walk-up crew check"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "day-after-survey text drafted — you approve before it sends"}}]},
    {"who": "user", "text": "Sounds good, thanks."},
    {"who": "ai", "text": "Thank you. Have a good night."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "Hi, Ethan from last night — what’s the difference between full packing and standard?"},
    {"who": "ai", "when": "+2 sec", "text": "With full packing our crew packs and unpacks everything; standard means we move the furniture and the boxes you’ve packed yourself. You can get both prices at Thursday’s survey.", "merge": True},
    {"who": "user", "when": "7:42 AM", "text": "If the TV gets damaged in the move, you cover the full replacement, right?"},
    {"who": "ai", "when": "+2 sec", "text": "What’s covered, and for how much, is for the owner to explain from the policy — not something I can promise. I’ve passed our conversation along; he’ll reply this morning.", "handoff": True}
   ],
   "handoff": HAND_EN + ["Why it stopped: damage coverage is a promise under the policy, not a fact I can make"],
   "morning": [
    {"icon": "✓", "k": "New survey", "v": "Ethan Brooks · Thu 7:00 PM · Elm Street walk-up · in the calendar"},
    {"icon": "#", "k": "Range on file #2266", "v": "$600 to $1,000 · sent by text · opened"},
    {"icon": "@", "k": "Owner task", "v": "survey Thu 7:00 PM · extra crew check for the walk-up"},
    {"icon": "!", "k": "Waiting for a person", "v": "damage coverage question · full thread attached · owner: Mike"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Mike, the owner. Hi Ethan — coverage depends on which valuation option you pick, and I’ll walk you through both on Thursday so you can choose before the move."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the owner was still on a job.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────────── 셀프 스토리지 ─────────────────────────────
 "self-storage": {
  "ko": {
   "biz": "마이룸스토리지", "owner": "사장님",
   "meta": "목요일 10:47 PM · 무인 운영 시간 · 가상의 스토리지", "callTime": "10:47 PM", "chan": "카카오톡",
   "chapters": ["밤 10:47, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 사장님 화면"],
   "chapterSubs": ["원룸 짐 보관 · 평수와 요금 · 공실 확보", "출입 시간 · 보관 금지 물품 질문은 사람에게", "공실 확보 · 계약서 · 사장님 · 답변 대기"],
   "sys": {"ring": "밤 10:47 — 전화벨이 울립니다. 현장에는 아무도 없습니다.",
           "chat": "다음 날 아침 7:40 — 같은 손님이 카카오톡으로.",
           "morning": "오전 9:00 — 사장님 화면."},
   "customer": {"name": "윤지호", "phone": "010-8823-44··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 마이룸스토리지입니다. 지금은 무인 운영 시간이지만, 요금 안내와 공실 확인, 계약 안내는 제가 도와드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "원룸 이사하는데 짐 잠깐 맡기려고요. 얼마짜리가 맞을까요?",
     "side": [{"field": {"k": "요청", "v": "원룸 짐 임시 보관", "src": "통화에서"}}]},
    {"who": "ai", "text": "원룸 짐이면 보통 한 평이면 들어가요. 한 평은 월 12만원이고, 냉장고와 세탁기까지 넣으시면 한 평 반에 월 17만원을 권해 드려요. 지금 한 평 두 칸, 한 평 반 한 칸이 비어 있어요.",
     "side": [{"field": {"k": "요금", "v": "1평 월 120,000원 · 1.5평 월 170,000원", "src": "사장님 요금표"}}, {"field": {"k": "공실", "v": "1평 2칸 · 1.5평 1칸", "src": "재고 현황"}}]},
    {"who": "user", "text": "냉장고도 있어요. 한 평 반으로 할게요. 언제부터 쓸 수 있어요?",
     "side": [{"field": {"k": "짐 규모", "v": "원룸 · 냉장고 · 세탁기 — 다 들어간다는 보장 아님", "src": "본인 발화"}}]},
    {"who": "ai", "text": "계약하시면 바로 쓰실 수 있고, 출입 카드는 현장에서 발급돼요. 성함과 연락처를 말씀해 주시면 한 평 반 한 칸을 잡아 둘게요."},
    {"who": "user", "text": "윤지호고요, 010-8823-4419예요.",
     "side": [{"field": {"k": "이름", "v": "윤지호", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-8823-44··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "윤지호 님, 한 평 반 한 칸을 내일까지 잡아 두었어요. 계약서 링크를 문자로 지금 보내 드릴게요. 언제부터 얼마나 쓰실 계획이세요?",
     "side": [{"field": {"k": "공실 확보", "v": "1.5평 1칸 · 내일까지", "src": "재고 현황"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "공실 확보", "v": "1.5평 1칸 · 내일까지 보류 · 계약서 링크 문자 발송"}}]},
    {"who": "user", "text": "이번 주 토요일부터 두 달 정도요.",
     "side": [{"field": {"k": "시작일 · 기간", "v": "토요일부터 · 약 2개월", "src": "본인 발화"}}]},
    {"who": "ai", "text": "토요일부터 두 달로 적어 둘게요. 평수는 기준표로 안내드린 거라, 첫날 짐이 다 안 들어가면 칸을 바꾸실 수 있어요. 전화 주셔서 감사합니다.",
     "side": [{"work": {"icon": "#", "k": "계약서 #4410", "v": "1.5평 월 170,000원 — 사장님 요금표에서 · 서명 대기"}},
              {"work": {"icon": "@", "k": "담당·기한", "v": "사장님 · 계약 확인 · 토요일 출입 카드 준비"}},
              {"work": {"icon": "↻", "k": "후속 문자", "v": "미서명 시 내일 오후 안내 문자 초안 — 발송 전 사장님 확인"}}]},
    {"who": "user", "text": "네, 알겠습니다."},
    {"who": "ai", "text": "감사합니다. 편안한 밤 되세요."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "어제 전화한 윤지호인데, 출입 시간이 어떻게 돼요?"},
    {"who": "ai", "when": "+2 sec", "text": "매일 오전 6시부터 밤 10시까지 카드로 출입하실 수 있어요. 한 평 반 칸은 오늘까지 잡아 두었습니다.", "merge": True},
    {"who": "user", "when": "7:41 AM", "text": "오토바이 배터리랑 캠핑용 가스통도 넣어도 되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "보관해도 되는 물품인지는 제가 판단할 수 없습니다. 배터리와 연료는 규정이 따로 있어서, 대화 내용을 사장님께 전달해 두었고 오전 중에 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HAND_KO + ["멈춘 이유: 보관 가능 여부는 규정에 따른 판단이지, 제가 정할 사실이 아닙니다"],
   "morning": [
    {"icon": "✓", "k": "공실 확보 1건", "v": "윤지호 · 1.5평 · 오늘까지 보류"},
    {"icon": "#", "k": "계약서 #4410", "v": "월 170,000원 · 문자로 발송됨 · 열람 확인 · 서명 대기"},
    {"icon": "@", "k": "사장님 할 일", "v": "계약 확인 · 토요일 출입 카드 준비 · 담당 김유나"},
    {"icon": "!", "k": "답변 대기 1건", "v": "보관 금지 물품 문의 · 대화 전체 첨부 · 담당 김유나"}
   ],
   "person": {"when": "9:12 AM", "text": "사장 김유나입니다. 윤지호 님, 배터리는 분리해서 두시면 괜찮고, 가스통은 빈 것도 보관이 안 돼요. 나머지는 다 괜찮습니다."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 사장님이 자는 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Keystone Self Storage", "owner": "the owner",
   "meta": "Thursday 10:47 PM · unstaffed site · a fictional storage facility", "callTime": "10:47 PM", "chan": "WhatsApp",
   "chapters": ["10:47 PM, the call", "Next morning, WhatsApp", "9:00 AM, the owner’s screen"],
   "chapterSubs": ["studio move · size and price · unit held", "gate hours · the prohibited-items question goes to a person", "hold · e-sign link · manager · one reply waiting"],
   "sys": {"ring": "10:47 PM — the phone rings. Nobody is on site.",
           "chat": "Next morning, 7:40 AM — the same customer, on WhatsApp.",
           "morning": "9:00 AM — the owner’s screen."},
   "customer": {"name": "Sophie Adams", "phone": "555-07··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Keystone Self Storage. The site is unstaffed right now, but I can quote prices, check what's available, and start a rental. How can I help?"},
    {"who": "user", "text": "I'm moving out of a studio and need to store my stuff for a bit. What size would I need?",
     "side": [{"field": {"k": "Request", "v": "temporary storage · studio contents", "src": "from the call"}}]},
    {"who": "ai", "text": "A studio usually fits in a five by five unit, which is seventy-nine dollars a month. If you're storing a fridge and a washer too, I'd suggest a five by ten at one hundred twenty-nine. Right now I have two five by fives and one five by ten open.",
     "side": [{"field": {"k": "Price", "v": "5x5 $79 a month · 5x10 $129 a month", "src": "your rate card"}}, {"field": {"k": "Availability", "v": "two 5x5 · one 5x10", "src": "live inventory"}}]},
    {"who": "user", "text": "I do have a fridge. Let's do the five by ten. When could I start?",
     "side": [{"field": {"k": "Contents", "v": "studio · fridge · washer — fit not guaranteed", "src": "caller said it"}}]},
    {"who": "ai", "text": "As soon as the rental agreement is signed, and your gate code and access card are issued on site. Can I get your name and a mobile number so I can hold the unit for you?"},
    {"who": "user", "text": "Sophie Adams, five five five, zero seven four six.",
     "side": [{"field": {"k": "Name", "v": "Sophie Adams", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-07··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, Sophie. I've held the five by ten for you until tomorrow, and I'm texting the e-sign link now. When would you move in, and for about how long?",
     "side": [{"field": {"k": "Hold", "v": "5x10 · until tomorrow", "src": "live inventory"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "Unit held", "v": "5x10 · held until tomorrow · e-sign link texted"}}]},
    {"who": "user", "text": "This Saturday, for about two months.",
     "side": [{"field": {"k": "Start and term", "v": "Saturday · about 2 months", "src": "caller said it"}}]},
    {"who": "ai", "text": "Saturday, about two months — noted. The size is a guide from our chart, so if it doesn't all fit on the day, you can switch units. Thanks for calling.",
     "side": [{"work": {"icon": "#", "k": "Agreement #4410", "v": "5x10 at $129 a month — from your own rate card · awaiting signature"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "site manager · confirm the hold · access card ready for Saturday"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "unsigned-by-tomorrow nudge drafted — you approve before it sends"}}]},
    {"who": "user", "text": "Perfect, thanks."},
    {"who": "ai", "text": "Thank you. Have a good night."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "Hi, Sophie from last night — what are the gate hours?"},
    {"who": "ai", "when": "+2 sec", "text": "Gate access is six in the morning to ten at night, every day, with your code. Your five by ten is still held until tonight.", "merge": True},
    {"who": "user", "when": "7:41 AM", "text": "Can I store a motorcycle battery and a couple of camping propane tanks in there?"},
    {"who": "ai", "when": "+2 sec", "text": "Whether those are allowed is a call for the manager, not for me — the rules on batteries and fuel are specific. I’ve passed our conversation along; she’ll reply this morning.", "handoff": True}
   ],
   "handoff": HAND_EN + ["Why it stopped: what may be stored is a judgement under the rules, not a fact I can decide"],
   "morning": [
    {"icon": "✓", "k": "Unit held", "v": "Sophie Adams · 5x10 · held until tonight"},
    {"icon": "#", "k": "Agreement #4410", "v": "$129 a month · e-sign sent · opened · awaiting signature"},
    {"icon": "@", "k": "Manager task", "v": "confirm the hold · access card ready for Saturday · owner: Anna"},
    {"icon": "!", "k": "Waiting for a person", "v": "prohibited-items question · full thread attached · owner: Anna"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Anna, the site manager. Hi Sophie — the battery is fine if it’s disconnected; propane tanks aren’t allowed on site, even empty. Everything else on your list is okay."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the owner slept.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────────── 장비 대여 ─────────────────────────────
 "equipment-rental": {
  "ko": {
   "biz": "대성장비", "owner": "사장님",
   "meta": "월요일 8:19 PM · 사무실 마감 후 · 가상의 장비 대여업체", "callTime": "8:19 PM", "chan": "카카오톡",
   "chapters": ["저녁 8:19, 전화", "새벽 6:05, 카카오톡", "오전 6:30, 사장님 화면"],
   "chapterSubs": ["3톤 지게차 · 요금표 · 내일 7시 인도 예약", "세금계산서 · 적재 하중 질문은 사람에게", "예약 · 견적 · 배차 · 답변 대기"],
   "sys": {"ring": "저녁 8:19 — 전화벨이 울립니다. 사무실은 5시에 닫았습니다.",
           "chat": "다음 날 새벽 6:05 — 같은 현장 소장님이 카카오톡으로.",
           "morning": "오전 6:30 — 사장님 화면."},
   "customer": {"name": "오세훈", "phone": "010-9145-22··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 대성장비입니다. 사무실은 닫혔지만 장비 재고 확인과 예약은 제가 바로 도와드릴 수 있어요. 무엇이 필요하세요?"},
    {"who": "user", "text": "내일 아침에 3톤 지게차 하루 쓸 수 있나요?",
     "side": [{"field": {"k": "장비", "v": "3톤 지게차 · 내일 · 1일", "src": "통화에서"}}]},
    {"who": "ai", "text": "3톤 지게차는 내일 한 대 가능해요. 일 대여는 18만원이고 운반비는 거리에 따라 별도예요. 기사 포함이면 32만원입니다. 현장 주소가 어디세요?",
     "side": [{"field": {"k": "재고", "v": "3톤 지게차 1대 가능", "src": "재고 현황"}}, {"field": {"k": "요금", "v": "일 180,000원 · 기사 포함 320,000원", "src": "사장님 요금표"}}]},
    {"who": "user", "text": "용인 기흥이고, 기사 포함으로 부탁드려요.",
     "side": [{"field": {"k": "현장 · 기사", "v": "용인 기흥 · 기사 포함", "src": "본인 발화"}}]},
    {"who": "ai", "text": "용인 기흥, 기사 포함으로 적었어요. 운반비는 주소 기준으로 담당자가 확인해서 아침에 알려 드릴게요. 성함과 연락처를 말씀해 주시겠어요?",
     "side": [{"field": {"k": "운반비", "v": "거리 확인 후 안내", "src": "요금표에 없음 · 확인 후 안내"}}]},
    {"who": "user", "text": "현장 소장 오세훈이고, 010-9145-2260입니다.",
     "side": [{"field": {"k": "이름", "v": "오세훈 · 현장 소장", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-9145-22··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "오세훈 소장님, 3톤 지게차 기사 포함으로 내일 예약되었어요. 장비가 한 대뿐이라 지금 바로 잡아 뒀습니다. 몇 시까지 도착하면 될까요?",
     "side": [{"crm": True}, {"work": {"icon": "✓", "k": "재고 확보 · 예약", "v": "3톤 지게차 1대 · 기사 포함 · 내일 · 재고에서 빠짐"}}]},
    {"who": "user", "text": "7시까지 와 주세요. 현장 담당은 저예요.",
     "side": [{"field": {"k": "인도 시각 · 담당", "v": "내일 07:00 · 오세훈", "src": "본인 발화"}}]},
    {"who": "ai", "text": "내일 오전 7시 도착, 현장 담당 오세훈 소장님으로 적었어요. 확인 문자를 보내 드리고, 운반비는 아침에 담당자가 연락드릴게요. 감사합니다.",
     "side": [{"work": {"icon": "#", "k": "견적 #0932", "v": "기사 포함 320,000원 — 사장님 요금표에서 · 운반비 확인 중"}},
              {"work": {"icon": "@", "k": "담당·기한", "v": "배차 김태우 · 기사 배정 · 운반비 확정 · 06:30까지"}},
              {"work": {"icon": "↻", "k": "후속 문자", "v": "회수 전날 안내 문자 초안 — 발송 전 사장님 확인"}}]},
    {"who": "user", "text": "네, 부탁드립니다."},
    {"who": "ai", "text": "감사합니다. 내일 아침에 뵙겠습니다."}
   ],
   "chat": [
    {"who": "user", "when": "6:05 AM", "text": "어제 예약한 오세훈인데, 카드 말고 세금계산서로 해 주실 수 있나요?"},
    {"who": "ai", "when": "+2 sec", "text": "네, 사업자 정보를 보내 주시면 세금계산서로 발행돼요. 3톤 지게차 기사 포함, 오늘 7시 기흥 도착은 그대로 유효합니다.", "merge": True},
    {"who": "user", "when": "6:07 AM", "text": "3톤인데 3.5톤 살짝 넘는 팔레트도 들 수 있죠? 조금만 넘는데요."},
    {"who": "ai", "when": "+2 sec", "text": "장비가 얼마까지 안전하게 드는지는 제가 답하면 안 되는 부분입니다. 대화 내용을 담당자께 그대로 전달해 두었고, 인도 전에 전화드리겠습니다.", "handoff": True}
   ],
   "handoff": HAND_KO + ["멈춘 이유: 장비가 안전하게 들 수 있는 무게는 안전 판단이지, 제가 정할 사실이 아닙니다"],
   "morning": [
    {"icon": "✓", "k": "새 예약 1건", "v": "오세훈 · 3톤 지게차 기사 포함 · 오늘 07:00 · 용인 기흥"},
    {"icon": "#", "k": "견적서 #0932", "v": "320,000원 · 운반비 주소 확인 중 · 문자로 발송됨"},
    {"icon": "@", "k": "배차 할 일", "v": "기사 배정 · 운반비 확정 · 담당 김태우"},
    {"icon": "!", "k": "답변 대기 1건", "v": "적재 하중 문의 · 대화 전체 첨부 · 담당 김태우"}
   ],
   "person": {"when": "6:42 AM", "text": "배차 담당 김태우입니다. 오세훈 소장님, 3톤 장비는 3톤까지만 들어야 해서 그 팔레트가 더 무거우면 7시 전에 5톤으로 바꿔 드릴 수 있어요. 지금 전화드릴게요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 사장님이 자는 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Ridgeline Equipment Rentals", "owner": "the owner",
   "meta": "Monday 8:19 PM · depot closed · a fictional rental yard", "callTime": "8:19 PM", "chan": "WhatsApp",
   "chapters": ["8:19 PM, the call", "6:05 AM, WhatsApp", "6:30 AM, the owner’s screen"],
   "chapterSubs": ["three-ton forklift · rate card · reserved for 7 AM", "invoicing · the load-limit question goes to a person", "reservation · quote · dispatch · one reply waiting"],
   "sys": {"ring": "8:19 PM — the phone rings. The depot closed at five.",
           "chat": "Next morning, 6:05 AM — the same foreman, on WhatsApp.",
           "morning": "6:30 AM — the owner’s screen."},
   "customer": {"name": "Marcus Hill", "phone": "555-08··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Ridgeline Equipment Rentals. The depot is closed, but I can check stock and reserve equipment right now. What do you need?"},
    {"who": "user", "text": "Can I get a three-ton forklift for tomorrow morning, just for the day?",
     "side": [{"field": {"k": "Equipment", "v": "3-ton forklift · tomorrow · 1 day", "src": "from the call"}}]},
    {"who": "ai", "text": "Yes — I have one three-ton forklift free tomorrow. The daily rate is two hundred eighty dollars, and delivery is charged separately by distance. With an operator it's five hundred twenty. Where's the site?",
     "side": [{"field": {"k": "Stock", "v": "3-ton forklift · 1 available", "src": "live inventory"}}, {"field": {"k": "Rate", "v": "$280 a day · $520 with operator", "src": "your rate card"}}]},
    {"who": "user", "text": "It's the Riverside job on Mill Road, and I'll need the operator.",
     "side": [{"field": {"k": "Site · operator", "v": "Riverside job, Mill Road · with operator", "src": "caller said it"}}]},
    {"who": "ai", "text": "Riverside on Mill Road, with an operator — noted. Delivery gets confirmed from the address by the hire desk first thing in the morning. Can I get your name and a mobile number?",
     "side": [{"field": {"k": "Delivery", "v": "quoted after the address check", "src": "not on the rate card · confirm first"}}]},
    {"who": "user", "text": "Marcus Hill, I'm the site foreman. Five five five, zero eight one seven.",
     "side": [{"field": {"k": "Name", "v": "Marcus Hill · site foreman", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-08··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, Marcus. The three-ton forklift with an operator is reserved for you tomorrow — it's the only one, so I've locked it in now. What time do you need it on site?",
     "side": [{"crm": True}, {"work": {"icon": "✓", "k": "Reserved", "v": "3-ton forklift · with operator · tomorrow · taken out of stock"}}]},
    {"who": "user", "text": "Seven, and I'm the site contact.",
     "side": [{"field": {"k": "Delivery time · contact", "v": "tomorrow 7:00 AM · Marcus Hill", "src": "caller said it"}}]},
    {"who": "ai", "text": "Seven tomorrow morning, site contact Marcus Hill — all noted. I'm texting a confirmation, and the hire desk will call you about delivery in the morning. Thank you.",
     "side": [{"work": {"icon": "#", "k": "Quote #0932", "v": "$520 with operator — from your own rate card · delivery pending"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "dispatch, Ray · assign operator · confirm delivery charge · by 6:30"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "day-before-pickup reminder drafted — you approve before it sends"}}]},
    {"who": "user", "text": "Great, thanks."},
    {"who": "ai", "text": "Thank you. See you tomorrow morning."}
   ],
   "chat": [
    {"who": "user", "when": "6:05 AM", "text": "Hi, Marcus from last night — can you invoice the company instead of charging a card?"},
    {"who": "ai", "when": "+2 sec", "text": "Yes — send the company details and we’ll invoice on account. Your forklift with operator is still set for seven at Riverside.", "merge": True},
    {"who": "user", "when": "6:07 AM", "text": "It’s a three-ton, but can it lift a pallet that’s just over three and a half? Only slightly over."},
    {"who": "ai", "when": "+2 sec", "text": "Load limits and what’s safe to lift are for the operator and the hire desk to answer, not me. I’ve passed our conversation along — someone will call you before delivery.", "handoff": True}
   ],
   "handoff": HAND_EN + ["Why it stopped: what a machine can safely lift is a safety judgement, not a fact I can give"],
   "morning": [
    {"icon": "✓", "k": "New reservation", "v": "Marcus Hill · 3-ton forklift with operator · today 7:00 AM · Riverside"},
    {"icon": "#", "k": "Quote #0932", "v": "$520 with operator · delivery pending address check · sent by text"},
    {"icon": "@", "k": "Dispatch task", "v": "assign operator · confirm delivery charge · owner: Ray"},
    {"icon": "!", "k": "Waiting for a person", "v": "load-limit question · full thread attached · owner: Ray"}
   ],
   "person": {"when": "6:42 AM", "text": "This is Ray at the hire desk. Hi Marcus — a three-ton machine stays under three tons, no exceptions. If that pallet’s heavier, I can swap you to a five-ton before seven. Calling you now."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the owner slept.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────────── 음식점 ─────────────────────────────
 "restaurants": {
  "ko": {
   "biz": "온기식당", "owner": "사장님",
   "meta": "수요일 12:38 PM · 점심 피크 · 가상의 음식점", "callTime": "12:38 PM", "chan": "카카오톡",
   "chapters": ["낮 12:38, 전화", "그날 오후, 카카오톡", "다음 날 오전 10:00, 사장님 화면"],
   "chapterSubs": ["20명 회식 · 코스 단가 · 금요일 6시 예약", "세금계산서 · 알레르기 질문은 주방에", "예약 · 확인 문자 · 주방 할 일 · 답변 대기"],
   "sys": {"ring": "낮 12:38 — 전화벨이 울립니다. 홀도 주방도 손이 비지 않습니다.",
           "chat": "그날 오후 3:15 — 같은 손님이 카카오톡으로.",
           "morning": "다음 날 오전 10:00 — 사장님 화면."},
   "customer": {"name": "한소희", "phone": "010-4471-66··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 온기식당입니다. 지금 점심시간이라 홀이 바빠서 제가 대신 받고 있어요. 예약과 문의를 도와드릴 수 있습니다. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "금요일 저녁에 20명 예약 되나요? 룸 있어요?",
     "side": [{"field": {"k": "요청", "v": "금요일 저녁 · 20명 · 룸", "src": "통화에서"}}]},
    {"who": "ai", "text": "금요일 저녁은 6시와 8시 두 타임이 남아 있고, 20명이면 2층 룸이 맞아요. 단체는 1인 2만 5천원 코스로 나가고, 주류는 별도예요. 어느 시간으로 잡아 드릴까요?",
     "side": [{"field": {"k": "룸 · 시간", "v": "2층 룸 · 6시 또는 8시", "src": "캘린더의 빈 시간"}}, {"field": {"k": "코스 단가", "v": "1인 25,000원 · 주류 별도", "src": "사장님 요금표"}}]},
    {"who": "user", "text": "6시로 해 주세요. 채식하시는 분이 한 분 계세요.",
     "side": [{"field": {"k": "요청 사항", "v": "채식 1인 — 말 그대로 기록", "src": "본인 발화"}}]},
    {"who": "ai", "text": "금요일 저녁 6시, 20명, 2층 룸으로 잡을게요. 채식 한 분은 말씀하신 그대로 사장님께 전달해 둘게요. 예약자 성함과 연락처를 말씀해 주시겠어요?"},
    {"who": "user", "text": "한소희고요, 010-4471-6690이에요.",
     "side": [{"field": {"k": "이름", "v": "한소희", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-4471-66··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "한소희 님, 금요일 저녁 6시 20명 예약되었어요. 확인 문자를 지금 보내 드릴게요. 회사 회식이면 예약자명에 회사명도 같이 적어 둘까요?",
     "side": [{"field": {"k": "예약", "v": "금 18:00 · 20명 · 2층 룸", "src": "캘린더의 빈 시간"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "예약 확정", "v": "금 18:00 · 2층 룸 · 좌석 현황에 들어감 · 확인 문자 발송"}}]},
    {"who": "user", "text": "네, 한빛건설로 해 주세요.",
     "side": [{"field": {"k": "예약자", "v": "한소희 · 한빛건설", "src": "본인 발화"}}]},
    {"who": "ai", "text": "한빛건설, 한소희 님으로 적어 두었어요. 목요일 오후에 확인 문자를 한 번 더 드릴게요. 금요일에 뵙겠습니다.",
     "side": [{"work": {"icon": "#", "k": "예약 확인서 #5127", "v": "1인 25,000원 코스 · 20명 — 사장님 요금표에서"}},
              {"work": {"icon": "@", "k": "담당·기한", "v": "사장님 · 채식 1인분 구성 확인 · 목요일까지"}},
              {"work": {"icon": "↻", "k": "전날 확인", "v": "목요일 오후 확인 문자 초안 — 발송 전 사장님 확인"}}]},
    {"who": "user", "text": "네, 감사합니다."},
    {"who": "ai", "text": "감사합니다. 맛있게 준비해 둘게요."}
   ],
   "chat": [
    {"who": "user", "when": "3:15 PM", "text": "아까 예약한 한소희인데, 당일 카드 말고 세금계산서 발행되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "네, 사업자 정보를 보내 주시면 세금계산서로 발행돼요. 금요일 6시 20명 2층 룸 예약은 그대로 유효합니다.", "merge": True},
    {"who": "user", "when": "3:16 PM", "text": "코스에 새우 들어가나요? 갑각류 알레르기 있는 분이 계세요."},
    {"who": "ai", "when": "+2 sec", "text": "재료와 알레르기는 주방에서 확인해야 해서 제가 답할 수 없습니다. 말씀하신 그대로 적어 사장님께 전달해 두었고, 내일 오전에 답변드리겠습니다.", "handoff": True}
   ],
   "handoff": HAND_KO + ["멈춘 이유: 어떤 재료가 들어가는지는 주방이 확인할 일이지, 제가 정할 사실이 아닙니다"],
   "morning": [
    {"icon": "✓", "k": "새 예약 1건", "v": "한빛건설 · 금 18:00 · 20명 · 2층 룸 · 좌석 현황에 있음"},
    {"icon": "#", "k": "예약 확인서 #5127", "v": "1인 25,000원 · 문자로 발송됨 · 열람 확인"},
    {"icon": "@", "k": "주방 할 일", "v": "채식 1인분 구성 · 목요일까지 · 담당 사장님"},
    {"icon": "!", "k": "답변 대기 1건", "v": "갑각류 알레르기 문의 · 대화 전체 첨부 · 담당 사장님"}
   ],
   "person": {"when": "10:25 AM", "text": "사장 박은정입니다. 한소희 님, 주방에 확인하니 두 번째 코스에 새우가 들어가요. 그분 것은 갑각류를 빼고 따로 준비할게요. 당일에 자리만 알려 주세요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 사장님이 주방에 있는 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Harvest Table", "owner": "the owner",
   "meta": "Wednesday 12:38 PM · lunch rush · a fictional restaurant", "callTime": "12:38 PM", "chan": "WhatsApp",
   "chapters": ["12:38 PM, the call", "That afternoon, WhatsApp", "Next day 10:00 AM, the owner’s screen"],
   "chapterSubs": ["party of twenty · set menu · Friday 6 PM booked", "invoicing · the allergy question goes to the kitchen", "booking · confirmation · kitchen task · one reply waiting"],
   "sys": {"ring": "12:38 PM — the phone rings. The floor and the kitchen are both slammed.",
           "chat": "That afternoon, 3:15 PM — the same organiser, on WhatsApp.",
           "morning": "Next day, 10:00 AM — the owner’s screen."},
   "customer": {"name": "Rachel Moore", "phone": "555-09··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Harvest Table. It's the lunch rush, so I'm answering for the floor. I can take reservations and answer questions. How can I help?"},
    {"who": "user", "text": "Can you take twenty people on Friday evening? Do you have a private room?",
     "side": [{"field": {"k": "Request", "v": "Friday evening · 20 guests · private room", "src": "from the call"}}]},
    {"who": "ai", "text": "Friday evening I have six or eight o'clock left, and for twenty the upstairs private room is the right fit. Groups are on the set menu at forty-five dollars a head, drinks separate. Which time would you like?",
     "side": [{"field": {"k": "Room · time", "v": "upstairs room · 6 or 8 PM", "src": "free in your bookings"}}, {"field": {"k": "Set menu", "v": "$45 a head · drinks separate", "src": "your function sheet"}}]},
    {"who": "user", "text": "Six, please. One of our guests is vegetarian.",
     "side": [{"field": {"k": "Requests", "v": "1 vegetarian — written word for word", "src": "caller said it"}}]},
    {"who": "ai", "text": "Friday at six, twenty guests, upstairs room — booking that now. I'll pass the vegetarian guest on to the owner exactly as you said it. Can I get your name and a mobile number?"},
    {"who": "user", "text": "Rachel Moore, five five five, zero nine two five.",
     "side": [{"field": {"k": "Name", "v": "Rachel Moore", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-09··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, Rachel. You're booked for Friday at six, and I'm texting a confirmation now. Is this a company dinner? I can put the company name on the booking too.",
     "side": [{"field": {"k": "Booking", "v": "Fri 6:00 PM · 20 · upstairs room", "src": "free in your bookings"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "Booked", "v": "Fri 6:00 PM · upstairs room · in the bookings · confirmation text sent"}}]},
    {"who": "user", "text": "Yes — Brightwater Consulting.",
     "side": [{"field": {"k": "Booked under", "v": "Rachel Moore · Brightwater Consulting", "src": "caller said it"}}]},
    {"who": "ai", "text": "Brightwater Consulting, Rachel Moore — noted. I'll send one more confirmation on Thursday afternoon. See you Friday.",
     "side": [{"work": {"icon": "#", "k": "Confirmation #5127", "v": "$45 set menu · 20 guests — from your own function sheet"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "the owner · vegetarian course for one · by Thursday"}},
              {"work": {"icon": "↻", "k": "Day-before check", "v": "Thursday afternoon reminder drafted — you approve before it sends"}}]},
    {"who": "user", "text": "Great, thank you."},
    {"who": "ai", "text": "Thank you. We'll have the room ready."}
   ],
   "chat": [
    {"who": "user", "when": "3:15 PM", "text": "Hi, Rachel from earlier — can you invoice the company instead of a card on the night?"},
    {"who": "ai", "when": "+2 sec", "text": "Yes — send the billing details and we’ll invoice. Friday at six, twenty guests, upstairs room is unchanged.", "merge": True},
    {"who": "user", "when": "3:16 PM", "text": "Does the set menu have any shrimp? One guest has a shellfish allergy."},
    {"who": "ai", "when": "+2 sec", "text": "Anything about allergens has to come from the kitchen, not from me. I’ve written it down word for word and passed it to the owner — you’ll have an answer tomorrow morning.", "handoff": True}
   ],
   "handoff": HAND_EN + ["Why it stopped: what is in a dish is for the kitchen to confirm, not a fact I can give"],
   "morning": [
    {"icon": "✓", "k": "New booking", "v": "Brightwater Consulting · Fri 6:00 PM · 20 guests · upstairs room"},
    {"icon": "#", "k": "Confirmation #5127", "v": "$45 set menu · sent by text · opened"},
    {"icon": "@", "k": "Kitchen task", "v": "vegetarian course for one · by Thursday · owner: Nina"},
    {"icon": "!", "k": "Waiting for a person", "v": "shellfish allergy question · full thread attached · owner: Nina"}
   ],
   "person": {"when": "10:25 AM", "text": "This is Nina, the owner. Hi Rachel — I checked with the chef: the second course has shrimp, so we’ll plate a shellfish-free version for that guest. Just tell us which seat on the night."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the owner was in the kitchen.",
   "honest": HONEST_EN
  }
 }
}
