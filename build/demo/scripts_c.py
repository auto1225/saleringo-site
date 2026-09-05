# -*- coding: utf-8 -*-
"""데모 대본 C — venues · stays · golf · legal · public-sector · funeral-homes · ecommerce · franchise.
형식은 build/demo/validate.py 의 docstring 을 따른다. 상호와 인물은 전부 가상이다."""

HONEST_KO = "각본이 있는 시연 · 예시 데이터 · 두 목소리는 이 데모를 위해 만든 합성 음성입니다 · 금액은 예시 요금표입니다."
HONEST_EN = "Scripted simulation · sample data · both voices were synthesised for this demo · figures are an example price list."
HANDOFF_KO = ["두 채널의 대화 전체", "받아 적은 항목 전부, 출처와 함께"]
HANDOFF_EN = ["The whole conversation, both channels", "Every captured field, with its source"]

SCRIPTS = {

 # ───────────────────────── 웨딩홀 · 행사장 ─────────────────────────
 "venues": {
  "ko": {
   "biz": "라온웨딩홀", "owner": "담당자님",
   "meta": "토요일 9:41 PM · 저녁 예식 진행 중 · 가상의 웨딩홀", "callTime": "9:41 PM", "chan": "카카오톡",
   "chapters": ["밤 9:41, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 담당자 화면"],
   "chapterSubs": ["내년 5월 17일 · 하객 200명 · 일요일 상담 예약", "주차 질문 · 날짜 선점은 사람에게", "상담 예약 · 안내 기록 · 담당 · 답변 대기"],
   "sys": {"ring": "밤 9:41 — 전화벨이 울립니다. 사무실은 비었고, 홀에서는 저녁 예식이 진행 중입니다.",
           "chat": "다음 날 아침 7:40 — 같은 손님이 카카오톡으로.",
           "morning": "오전 9:00 — 담당자 화면."},
   "customer": {"name": "박서연", "phone": "010-7731-28··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 라온웨딩홀입니다. 지금은 사무실 근무가 끝난 시간이지만, 날짜 확인과 상담 예약은 제가 도와드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "내년 5월 17일 토요일 오후에 예식 가능한가요? 하객은 200명 정도예요.",
     "side": [{"field": {"k": "희망 날짜", "v": "내년 5월 17일 토 · 오후", "src": "통화에서"}},
              {"field": {"k": "행사 · 하객", "v": "예식 · 약 200명", "src": "통화에서"}}]},
    {"who": "ai", "text": "네, 5월 17일은 오후 1시와 오후 4시 두 타임이 남아 있어요. 200명이면 그랜드홀이 맞고, 식대는 1인 7만 5천원부터입니다. 보증 인원과 대관료는 타임마다 달라서 상담에서 정확히 안내드려요.",
     "side": [{"field": {"k": "남은 타임", "v": "5/17 오후 1시 · 오후 4시", "src": "캘린더의 빈 시간"}},
              {"field": {"k": "홀 · 식대", "v": "그랜드홀 · 식대 1인 75,000원부터", "src": "사장님 요금표"}}]},
    {"who": "user", "text": "주말에 상담 받을 수 있을까요?"},
    {"who": "ai", "text": "이번 주 일요일 오전 11시에 자리가 있어요. 두 분 오시면 홀도 같이 보실 수 있습니다. 잡아 드릴까요?"},
    {"who": "user", "text": "네, 잡아 주세요. 박서연이고요, 010-7731-2846이에요.",
     "side": [{"field": {"k": "이름", "v": "박서연", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-7731-28··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "박서연 님, 일요일 오전 11시 상담 예약되었습니다. 확인 문자와 오시는 길을 지금 보내 드릴게요. 낮에 연락드리기 편한 시간이 있으세요?",
     "side": [{"field": {"k": "상담 예약", "v": "일 11:00 · 홀 투어 포함", "src": "캘린더의 빈 시간"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "상담 예약 확정", "v": "일 11:00 · 캘린더에 들어감 · 확인 문자 발송"}}]},
    {"who": "user", "text": "평일 저녁 6시 이후가 좋아요.",
     "side": [{"field": {"k": "연락 가능 시간", "v": "평일 18시 이후", "src": "본인 발화"}}]},
    {"who": "ai", "text": "알겠습니다. 5월 17일 두 타임은 일요일 상담 전까지 담당자가 현황을 확인해 둘게요. 일요일에 뵙겠습니다.",
     "side": [{"work": {"icon": "#", "k": "안내 기록 #3104", "v": "5/17 오후 1시 · 4시 · 식대 75,000원부터 — 요금표에서"}},
              {"work": {"icon": "@", "k": "담당 · 기한", "v": "담당 김하늘 배정 · 일 10:30까지 홀 투어 준비"}},
              {"work": {"icon": "↻", "k": "후속 문자", "v": "상담 전날 리마인드 초안 — 발송 전 담당자 확인"}}]},
    {"who": "user", "text": "감사합니다."},
    {"who": "ai", "text": "감사합니다. 편안한 밤 되세요."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "어제 상담 예약한 박서연이에요. 일요일에 주차 되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "네 — 지하 주차장 2시간 무료입니다. 일요일 11시 상담 예약은 그대로예요.", "merge": True},
    {"who": "user", "when": "7:42 AM", "text": "계약 전인데, 5월 17일 4시 타임을 저희 이름으로 먼저 잡아 둘 수 있을까요?"},
    {"who": "ai", "when": "+2 sec", "text": "날짜를 잡아 두는 건 계약으로만 가능해서 제가 정할 수 없어요. 대화 내용을 담당자에게 그대로 전달했고, 오전 중에 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 날짜 선점은 계약 사항이라 담당자만 결정할 수 있습니다"],
   "morning": [
    {"icon": "✓", "k": "새 상담 예약 1건", "v": "박서연 · 일 11:00 · 하객 200명 · 그랜드홀"},
    {"icon": "#", "k": "안내 기록 #3104", "v": "5/17 오후 1시 · 4시 · 식대 1인 75,000원부터 · 문자로 발송됨"},
    {"icon": "@", "k": "담당 할 일", "v": "일 10:30까지 홀 투어 준비 · 담당 김하늘"},
    {"icon": "!", "k": "답변 대기 1건", "v": "계약 전 날짜 선점 문의 · 대화 전체 첨부 · 담당 김하늘"}
   ],
   "person": {"when": "9:12 AM", "text": "담당자 김하늘입니다. 박서연 님, 날짜는 계약금과 함께 확정되지만 일요일 상담 전까지 4시 타임 현황을 제가 직접 확인해 두고, 그 자리에서 바로 진행하실 수 있게 준비할게요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 예식이 진행되는 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Laon Hall", "owner": "the venue manager",
   "meta": "Saturday 9:41 PM · an evening reception in progress · a fictional venue", "callTime": "9:41 PM", "chan": "WhatsApp",
   "chapters": ["9:41 PM, the call", "Next morning, WhatsApp", "9:00 AM, the venue manager's screen"],
   "chapterSubs": ["May 17 next year · 200 guests · Sunday consultation booked", "parking · the date hold goes to a person", "consultation · quote record · owner · one reply waiting"],
   "sys": {"ring": "9:41 PM — the phone rings. The office is empty; a reception is under way in the hall.",
           "chat": "Next morning, 7:40 AM — the same customer, on WhatsApp.",
           "morning": "9:00 AM — the venue manager's screen."},
   "customer": {"name": "Emma Park", "phone": "555-02··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Laon Hall. The office is closed for the evening, but I can check dates and book a consultation. How can I help?"},
    {"who": "user", "text": "Hi — is Saturday, May seventeenth next year open for a wedding in the afternoon? About two hundred guests.",
     "side": [{"field": {"k": "Date wanted", "v": "Sat May 17 next year · afternoon", "src": "from the call"}},
              {"field": {"k": "Event · guests", "v": "wedding · about 200", "src": "from the call"}}]},
    {"who": "ai", "text": "It is. May seventeenth still has two afternoon slots, one o'clock and four o'clock. For two hundred guests the Grand Hall is the right fit, and catering starts at sixty-five dollars a head. The minimum guest count and the room fee depend on the slot, so the team will walk you through the exact numbers at the consultation.",
     "side": [{"field": {"k": "Open slots", "v": "May 17 · 1 PM · 4 PM", "src": "free in your calendar"}},
              {"field": {"k": "Hall · catering", "v": "Grand Hall · from $65 a head", "src": "your price list"}}]},
    {"who": "user", "text": "Could we come in on a weekend?"},
    {"who": "ai", "text": "This Sunday at eleven in the morning is open. Both of you can come, and you'll see the hall as well. Shall I book that?"},
    {"who": "user", "text": "Yes, please. It's Emma Park, five five five, zero two eight four.",
     "side": [{"field": {"k": "Name", "v": "Emma Park", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-02··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, Emma. You're booked for Sunday at eleven. I'm texting you the confirmation and directions now. Is there a time of day that's best to reach you?",
     "side": [{"field": {"k": "Consultation", "v": "Sun 11:00 · hall tour included", "src": "free in your calendar"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "Consultation booked", "v": "Sun 11:00 · in your calendar · confirmation text sent"}}]},
    {"who": "user", "text": "Weekday evenings, after six.",
     "side": [{"field": {"k": "Best time to reach", "v": "weekdays after 6 PM", "src": "caller said it"}}]},
    {"who": "ai", "text": "Noted. Before Sunday the team will check the status of both May seventeenth slots so you have the latest picture. We'll see you Sunday.",
     "side": [{"work": {"icon": "#", "k": "Quote record #3104", "v": "May 17 · 1 PM · 4 PM · catering from $65 a head — from your price list"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "assigned to Hana · hall tour ready by Sun 10:30"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "day-before reminder drafted — the team approves before it sends"}}]},
    {"who": "user", "text": "Thank you so much."},
    {"who": "ai", "text": "Thank you. Have a lovely evening."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "Hi, Emma Park — I booked a consultation for Sunday. Is there parking?"},
    {"who": "ai", "when": "+2 sec", "text": "Yes — the underground garage is free for two hours. Your Sunday eleven o'clock consultation is unchanged.", "merge": True},
    {"who": "user", "when": "7:42 AM", "text": "We haven't signed anything yet, but could you hold the four o'clock slot on May seventeenth under our name?"},
    {"who": "ai", "when": "+2 sec", "text": "Holding a date is something only a signed contract can do, so it isn't my call. I've passed our conversation to the venue manager — someone will reply this morning.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: holding a date is a contract decision, not a fact on file"],
   "morning": [
    {"icon": "✓", "k": "New consultation", "v": "Emma Park · Sun 11:00 · 200 guests · Grand Hall"},
    {"icon": "#", "k": "Quote record #3104", "v": "May 17 · 1 PM · 4 PM · catering from $65 a head · sent by text"},
    {"icon": "@", "k": "Team task", "v": "hall tour ready by Sun 10:30 · owner: Hana"},
    {"icon": "!", "k": "Waiting for a person", "v": "pre-contract date hold · full thread attached · owner: Hana"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Hana from the events team. Hi Emma — a date is confirmed with the deposit, but I'll check the four o'clock slot myself before Sunday so you can decide on the spot."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the hall was hosting a reception.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────── 펜션 · 숙박 ─────────────────────────
 "stays": {
  "ko": {
   "biz": "바다숲펜션", "owner": "사장님",
   "meta": "수요일 10:22 PM · 청소 마치고 취침 · 가상의 펜션", "callTime": "10:22 PM", "chan": "카카오톡",
   "chapters": ["밤 10:22, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 사장님 화면"],
   "chapterSubs": ["토요일 독채 · 바비큐 · 반려견 · 직접 예약", "짐 보관 질문 · 우천 환불은 사람에게", "예약 · 입금 안내 · 할 일 · 답변 대기"],
   "sys": {"ring": "밤 10:22 — 전화벨이 울립니다. 사장님은 객실 청소를 마치고 잠든 뒤입니다.",
           "chat": "다음 날 아침 7:40 — 같은 손님이 카카오톡으로.",
           "morning": "오전 9:00 — 사장님 화면."},
   "customer": {"name": "이준호", "phone": "010-2094-66··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 바다숲펜션입니다. 늦은 시간이라 사장님은 쉬고 계시지만, 객실 확인과 예약은 제가 도와드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "이번 주 토요일에 4인 독채 남아 있나요? 바비큐도 되나요?",
     "side": [{"field": {"k": "요청", "v": "토요일 1박 · 4인 독채 · 바비큐", "src": "통화에서"}}]},
    {"who": "ai", "text": "토요일은 C동 독채가 하나 남아 있어요. 4인 기준 주말 요금으로 25만원이고요. 바비큐는 1인 1만원에 숯과 그릴이 나가고, 고기는 준비해 오시면 됩니다. 직접 예약이시면 플랫폼보다 2만원 저렴해요.",
     "side": [{"field": {"k": "객실", "v": "C동 독채 · 마지막 1실", "src": "재고 현황"}},
              {"field": {"k": "요금", "v": "주말 250,000원 · 바비큐 1인 10,000원 · 직접 예약 20,000원 할인", "src": "사장님 요금표"}}]},
    {"who": "user", "text": "그럼 직접 예약할게요. 강아지 한 마리 데려가도 되나요?"},
    {"who": "ai", "text": "C동은 반려견 동반이 가능하고, 마리당 2만원이 추가돼요. 토요일 C동으로 잡아 두겠습니다. 성함과 연락처를 말씀해 주시겠어요?",
     "side": [{"field": {"k": "반려동물", "v": "반려견 1마리 · 20,000원 추가", "src": "사장님 요금표"}}]},
    {"who": "user", "text": "이준호고요, 010-2094-6631이에요.",
     "side": [{"field": {"k": "이름", "v": "이준호", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-2094-66··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "이준호 님, 토요일 C동 독채 4인, 바비큐, 반려견 한 마리로 잡아 두었어요. 입금 계좌를 문자로 보내 드릴게요. 입금이 확인되면 예약이 확정됩니다.",
     "side": [{"field": {"k": "예약", "v": "토 C동 · 입금 대기", "src": "캘린더의 빈 시간"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "객실 확보", "v": "토 C동 독채 · 예약 현황에 잡힘 · 입금 안내 문자 발송"}}]},
    {"who": "user", "text": "체크인은 몇 시예요?"},
    {"who": "ai", "text": "체크인은 오후 3시, 체크아웃은 오전 11시예요. 바비큐 숯은 저녁 6시에 준비해 드리고요. 문자 보내 드렸으니 편하실 때 입금해 주세요. 토요일에 뵐게요.",
     "side": [{"work": {"icon": "#", "k": "입금 안내 #1187", "v": "250,000원 + 바비큐 40,000원 + 반려견 20,000원 — 요금표에서"}},
              {"work": {"icon": "@", "k": "담당 · 기한", "v": "토 15:00 전 C동 준비 · 18:00 바비큐 숯 · 담당 사장님"}},
              {"work": {"icon": "↻", "k": "후속 문자", "v": "미입금 시 D+1 안내 초안 — 발송 전 사장님 확인"}}]},
    {"who": "user", "text": "네, 감사합니다."},
    {"who": "ai", "text": "감사합니다. 편안한 밤 되세요."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "어제 예약한 이준호예요. 일찍 도착하면 짐만 먼저 둘 수 있나요?"},
    {"who": "ai", "when": "+2 sec", "text": "네 — 오후 1시부터 C동 앞 보관함에 두시면 돼요. 토요일 C동 예약은 그대로 유효합니다.", "merge": True},
    {"who": "user", "when": "7:41 AM", "text": "토요일에 비 오면 취소해도 전액 환불되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "환불 규정은 등록된 대로 안내드릴 수 있지만, 날씨를 이유로 예외를 둘지는 사장님이 정하실 일이에요. 대화 내용을 그대로 전달했고, 오전 중에 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 날씨 예외 환불은 규정이 아니라 사장님의 판단입니다"],
   "morning": [
    {"icon": "✓", "k": "새 예약 1건", "v": "이준호 · 토 C동 독채 · 4인 · 반려견 1 · 입금 대기"},
    {"icon": "#", "k": "입금 안내 #1187", "v": "310,000원 · 문자로 발송됨 · 열람 확인"},
    {"icon": "@", "k": "할 일", "v": "토 15:00 전 C동 준비 · 18:00 바비큐 숯 · 담당 사장님"},
    {"icon": "!", "k": "답변 대기 1건", "v": "우천 시 환불 문의 · 대화 전체 첨부 · 담당 사장님"}
   ],
   "person": {"when": "9:12 AM", "text": "바다숲펜션 박민준입니다. 이준호 님, 비 예보만으로는 환불이 어렵지만 기상특보로 못 오시게 되면 날짜 변경은 무료로 해 드릴게요. 토요일에 뵙겠습니다."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 사장님이 자는 동안 끝났고, 수수료는 0원입니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Seaforest Cabins", "owner": "the owner",
   "meta": "Wednesday 10:22 PM · owner asleep after turnover · a fictional guesthouse", "callTime": "10:22 PM", "chan": "WhatsApp",
   "chapters": ["10:22 PM, the call", "Next morning, WhatsApp", "9:00 AM, the owner's screen"],
   "chapterSubs": ["Saturday cabin · barbecue · one dog · booked direct", "early bags · the rain refund goes to a person", "booking · payment request · tasks · one reply waiting"],
   "sys": {"ring": "10:22 PM — the phone rings. The owner finished cleaning the cabins and went to bed.",
           "chat": "Next morning, 7:40 AM — the same guest, on WhatsApp.",
           "morning": "9:00 AM — the owner's screen."},
   "customer": {"name": "Daniel Lee", "phone": "555-03··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Seaforest Cabins. It's late and the owner has turned in, but I can check rooms and take a booking. How can I help?"},
    {"who": "user", "text": "Is the four-person cabin free this Saturday? And can we barbecue?",
     "side": [{"field": {"k": "Request", "v": "Sat 1 night · 4-person cabin · barbecue", "src": "from the call"}}]},
    {"who": "ai", "text": "Cabin C is the last one open on Saturday. It's two hundred and twenty dollars for four at the weekend rate. The barbecue is ten dollars a person and includes charcoal and the grill — you bring the food. Booking direct is twenty dollars less than the app.",
     "side": [{"field": {"k": "Room", "v": "Cabin C · last one", "src": "live availability"}},
              {"field": {"k": "Rate", "v": "weekend $220 · barbecue $10 a person · $20 off direct", "src": "your rate sheet"}}]},
    {"who": "user", "text": "Then I'll book direct. Can we bring our dog?"},
    {"who": "ai", "text": "Cabin C is dog-friendly, with a twenty dollar pet fee. I'll hold Cabin C for Saturday. Can I get your name and a mobile number?",
     "side": [{"field": {"k": "Pet", "v": "1 dog · $20 fee", "src": "your rate sheet"}}]},
    {"who": "user", "text": "Daniel Lee, five five five, zero three six one.",
     "side": [{"field": {"k": "Name", "v": "Daniel Lee", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-03··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, Daniel. Cabin C is held for Saturday, four guests, barbecue and one dog. I'm texting you the payment details now, and the booking is confirmed once the deposit lands.",
     "side": [{"field": {"k": "Booking", "v": "Sat Cabin C · deposit pending", "src": "free in your calendar"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "Room held", "v": "Sat Cabin C · on the availability board · payment text sent"}}]},
    {"who": "user", "text": "What time is check-in?"},
    {"who": "ai", "text": "Check-in is three in the afternoon, check-out is eleven. The charcoal will be ready at six. The text is on its way, so pay whenever it suits you. See you Saturday.",
     "side": [{"work": {"icon": "#", "k": "Payment request #1187", "v": "$220 + barbecue $40 + pet $20 — from your rate sheet"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "Cabin C ready by Sat 3:00 · charcoal at 6:00 · owner"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "D+1 nudge drafted if unpaid — you approve before it sends"}}]},
    {"who": "user", "text": "Great, thank you."},
    {"who": "ai", "text": "Thank you. Have a good night."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "Hi, Daniel Lee from last night — if we arrive early, can we drop our bags?"},
    {"who": "ai", "when": "+2 sec", "text": "Yes — from one o'clock, at the locker outside Cabin C. Your Saturday booking is unchanged.", "merge": True},
    {"who": "user", "when": "7:41 AM", "text": "If it rains on Saturday, can we cancel for a full refund?"},
    {"who": "ai", "when": "+2 sec", "text": "I can read you the cancellation policy as written, but making an exception for the weather is the owner's decision, not mine. I've passed our conversation along — the owner will reply this morning.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: a weather exception to the refund policy is a judgement, not a rule on file"],
   "morning": [
    {"icon": "✓", "k": "New booking", "v": "Daniel Lee · Sat Cabin C · 4 guests · 1 dog · deposit pending"},
    {"icon": "#", "k": "Payment request #1187", "v": "$280 · sent by text · opened"},
    {"icon": "@", "k": "Owner task", "v": "Cabin C ready by Sat 3:00 · charcoal at 6:00"},
    {"icon": "!", "k": "Waiting for a person", "v": "rain refund question · full thread attached · owner"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Minjun, the owner. Hi Daniel — a forecast alone isn't refundable, but if a weather warning stops you travelling, I'll move your date for free. See you Saturday."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the owner slept — and no platform took a cut.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────── 골프장 · 연습장 ─────────────────────────
 "golf": {
  "ko": {
   "biz": "청솔컨트리클럽", "owner": "사장님",
   "meta": "목요일 6:12 AM · 첫 티오프 전 · 가상의 골프장", "callTime": "6:12 AM", "chan": "카카오톡",
   "chapters": ["새벽 6:12, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 사장님 화면"],
   "chapterSubs": ["일요일 오전 4인 · 그린피 · 7시 40분 부킹", "카트 · 캐디 질문 · 우천 취소는 사람에게", "부킹 · 안내 기록 · 프로샵 · 답변 대기"],
   "sys": {"ring": "새벽 6:12 — 전화벨이 울립니다. 첫 티오프 전이라 프로샵은 아직 열지 않았습니다.",
           "chat": "다음 날 아침 7:40 — 같은 손님이 카카오톡으로.",
           "morning": "오전 9:00 — 사장님 화면."},
   "customer": {"name": "최민석", "phone": "010-5518-90··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 청솔컨트리클럽입니다. 프로샵은 아직 열기 전이지만, 티타임 확인과 부킹은 제가 도와드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "이번 주 일요일 오전에 4인 부킹 가능한가요?",
     "side": [{"field": {"k": "요청", "v": "일요일 오전 · 4인", "src": "통화에서"}}]},
    {"who": "ai", "text": "일요일 오전은 7시 40분 한 팀이 남아 있어요. 주말 그린피는 1인 22만원이고, 카트비와 캐디피는 별도입니다. 이 시간으로 잡아 드릴까요?",
     "side": [{"field": {"k": "티타임", "v": "일 07:40 · 마지막 1팀", "src": "캘린더의 빈 시간"}},
              {"field": {"k": "그린피", "v": "주말 1인 220,000원 · 카트 · 캐디 별도", "src": "사장님 요금표"}}]},
    {"who": "user", "text": "네, 잡아 주세요. 저희는 비회원이에요.",
     "side": [{"field": {"k": "구분", "v": "비회원", "src": "본인 발화"}}]},
    {"who": "ai", "text": "네, 비회원 요금으로 안내드린 금액이 맞아요. 대표자 성함과 연락처를 말씀해 주시겠어요?"},
    {"who": "user", "text": "최민석이고요, 010-5518-9027이에요.",
     "side": [{"field": {"k": "대표자", "v": "최민석", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-5518-90··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "최민석 님, 일요일 오전 7시 40분, 4인으로 예약되었습니다. 확인 문자를 지금 보내 드릴게요. 혹시 더 이른 시간이 나면 연락드릴까요?",
     "side": [{"crm": True},
              {"work": {"icon": "✓", "k": "티타임 확보", "v": "일 07:40 · 4인 · 예약 시스템에 들어감 · 확인 문자 발송"}}]},
    {"who": "user", "text": "네, 7시 이전이면 좋겠어요.",
     "side": [{"field": {"k": "대기 등록", "v": "일 07:00 이전 취소분 대기", "src": "통화에서"}}]},
    {"who": "ai", "text": "대기 명단에 올려 두었어요. 취소로 자리가 나면 문자로 먼저 알려 드릴게요. 일요일 7시 40분 팀은 그대로 유지됩니다. 즐거운 라운드 되세요.",
     "side": [{"work": {"icon": "#", "k": "안내 기록 #2210", "v": "주말 그린피 220,000원 · 카트 · 캐디 별도 — 요금표에서"}},
              {"work": {"icon": "@", "k": "담당 · 기한", "v": "프로샵 정재훈 배정 · 일 06:30 대기 취소분 확인"}},
              {"work": {"icon": "↻", "k": "대기 알림", "v": "07:00 이전 취소 발생 시 최민석 님에게 문자 — 사장님 규칙"}}]},
    {"who": "user", "text": "감사합니다."},
    {"who": "ai", "text": "감사합니다. 좋은 하루 되세요."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "어제 부킹한 최민석입니다. 카트비랑 캐디피는 얼마예요?"},
    {"who": "ai", "when": "+2 sec", "text": "카트비는 팀당 10만원, 캐디피는 팀당 15만원이에요. 일요일 7시 40분 예약은 그대로예요.", "merge": True},
    {"who": "user", "when": "7:42 AM", "text": "일요일에 비 예보가 있던데, 비 오면 취소해도 위약금 없나요?"},
    {"who": "ai", "when": "+2 sec", "text": "우천 취소는 당일 코스 상태를 보고 사장님이 정하시는 부분이라 제가 미리 확정해 드릴 수 없어요. 대화 내용을 전달했고, 오전 중에 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 우천 취소는 규정과 당일 코스 상태를 보고 사람이 정합니다"],
   "morning": [
    {"icon": "✓", "k": "새 부킹 1건", "v": "최민석 · 일 07:40 · 4인 · 비회원 · 07:00 이전 대기"},
    {"icon": "#", "k": "안내 기록 #2210", "v": "그린피 220,000원 · 카트 100,000원 · 캐디 150,000원 · 문자로 발송됨"},
    {"icon": "@", "k": "프로샵 할 일", "v": "일 06:30 대기 취소분 확인 · 담당 정재훈"},
    {"icon": "!", "k": "답변 대기 1건", "v": "우천 취소 위약금 문의 · 대화 전체 첨부 · 담당 정재훈"}
   ],
   "person": {"when": "9:12 AM", "text": "프로샵 정재훈입니다. 최민석 님, 당일 아침 코스 상태를 보고 라운드가 어려우면 위약금 없이 취소해 드리고, 예보만으로는 전날 오후 6시까지 무료로 변경하실 수 있어요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 사장님이 코스에 나가 있는 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Pine Ridge Golf Club", "owner": "the owner",
   "meta": "Thursday 6:12 AM · before the first tee · a fictional club", "callTime": "6:12 AM", "chan": "WhatsApp",
   "chapters": ["6:12 AM, the call", "Next morning, WhatsApp", "9:00 AM, the owner's screen"],
   "chapterSubs": ["Sunday four-ball · green fee · 7:40 booked", "cart and caddie · the rain cancellation goes to a person", "booking · quote record · pro shop · one reply waiting"],
   "sys": {"ring": "6:12 AM — the phone rings. It's before the first tee and the pro shop isn't open yet.",
           "chat": "Next morning, 7:40 AM — the same golfer, on WhatsApp.",
           "morning": "9:00 AM — the owner's screen."},
   "customer": {"name": "Michael Choi", "phone": "555-04··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Pine Ridge Golf Club. The pro shop isn't open yet, but I can check tee times and take a booking. How can I help?"},
    {"who": "user", "text": "Can I get a four-ball on Sunday morning?",
     "side": [{"field": {"k": "Request", "v": "Sunday morning · 4 players", "src": "from the call"}}]},
    {"who": "ai", "text": "Sunday morning has one slot left, seven forty. The weekend green fee is one hundred and sixty dollars a player, and carts and caddies are extra. Shall I hold seven forty for you?",
     "side": [{"field": {"k": "Tee time", "v": "Sun 7:40 · last slot", "src": "free in your tee sheet"}},
              {"field": {"k": "Green fee", "v": "weekend $160 a player · cart and caddie extra", "src": "your fee sheet"}}]},
    {"who": "user", "text": "Yes, please. We're not members.",
     "side": [{"field": {"k": "Status", "v": "visitors", "src": "caller said it"}}]},
    {"who": "ai", "text": "That's the visitor rate I quoted, so you're all set. Can I get the lead player's name and a mobile number?"},
    {"who": "user", "text": "Michael Choi, five five five, zero four two seven.",
     "side": [{"field": {"k": "Lead player", "v": "Michael Choi", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-04··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, Michael. You're booked for Sunday at seven forty, four players. I'm texting the confirmation now. Would you like me to let you know if an earlier time opens up?",
     "side": [{"crm": True},
              {"work": {"icon": "✓", "k": "Tee time held", "v": "Sun 7:40 · 4 players · on the tee sheet · confirmation text sent"}}]},
    {"who": "user", "text": "Yes — anything before seven would be great.",
     "side": [{"field": {"k": "Waitlist", "v": "any cancellation before Sun 7:00", "src": "from the call"}}]},
    {"who": "ai", "text": "You're on the waiting list. If a cancellation comes up I'll text you first, and your seven forty slot stays as it is. Enjoy the round.",
     "side": [{"work": {"icon": "#", "k": "Quote record #2210", "v": "weekend green fee $160 · cart and caddie extra — from your fee sheet"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "assigned to Jay in the pro shop · check waitlist against cancellations by Sun 6:30"}},
              {"work": {"icon": "↻", "k": "Waitlist alert", "v": "text Michael if a slot before 7:00 opens — your rule"}}]},
    {"who": "user", "text": "Thanks a lot."},
    {"who": "ai", "text": "Thank you. Have a great day."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "Hi, Michael Choi from yesterday — how much are the cart and the caddie?"},
    {"who": "ai", "when": "+2 sec", "text": "The cart is eighty dollars per group and the caddie is one hundred and twenty. Your Sunday seven forty booking is unchanged.", "merge": True},
    {"who": "user", "when": "7:42 AM", "text": "There's rain in the forecast for Sunday. If it rains, can we cancel without a penalty?"},
    {"who": "ai", "when": "+2 sec", "text": "A rain cancellation is decided on the day, by the club, from the course conditions — I can't confirm it in advance. I've passed our conversation along and someone will reply this morning.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: a weather cancellation is a judgement on the day, not a rule I can promise"],
   "morning": [
    {"icon": "✓", "k": "New booking", "v": "Michael Choi · Sun 7:40 · 4 players · visitors · waitlist before 7:00"},
    {"icon": "#", "k": "Quote record #2210", "v": "green fee $160 · cart $80 · caddie $120 · sent by text"},
    {"icon": "@", "k": "Pro shop task", "v": "check waitlist against cancellations by Sun 6:30 · owner: Jay"},
    {"icon": "!", "k": "Waiting for a person", "v": "rain cancellation question · full thread attached · owner: Jay"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Jay from the pro shop. Hi Michael — if the course is unplayable on the morning, we cancel with no penalty. On a forecast alone, you can move the time for free until six the evening before."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the owner was out on the course.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────── 법률사무소 ─────────────────────────
 "legal": {
  "ko": {
   "biz": "법률사무소 온정", "owner": "변호사님",
   "meta": "월요일 7:41 PM · 재판 준비 중 · 가상의 법률사무소", "callTime": "7:41 PM", "chan": "카카오톡",
   "chapters": ["저녁 7:41, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 변호사님 화면"],
   "chapterSubs": ["내용증명 · 상담료 · 내일 4시 예약", "주차 질문 · 사건 전망은 사람에게", "상담 예약 · 안내 기록 · 사무장 · 답변 대기"],
   "sys": {"ring": "저녁 7:41 — 전화벨이 울립니다. 변호사님은 내일 재판 준비 중입니다.",
           "chat": "다음 날 아침 7:40 — 같은 의뢰인이 카카오톡으로.",
           "morning": "오전 9:00 — 변호사님 화면."},
   "customer": {"name": "정우진", "phone": "010-3362-47··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 법률사무소 온정입니다. 지금은 상담 시간이 끝났지만, 상담 예약과 안내는 제가 도와드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "내용증명을 받았는데요, 상담 받을 수 있나요? 비용은 얼마인가요?",
     "side": [{"field": {"k": "문의", "v": "내용증명 수령 · 상담 요청", "src": "통화에서"}}]},
    {"who": "ai", "text": "네, 상담은 30분에 5만원이고, 사건을 맡기시면 상담료는 수임료에서 차감돼요. 내용증명은 답변 기한이 있는 경우가 많아서, 받으신 날짜를 확인해 두시면 좋습니다. 내일 오후 4시에 상담이 가능해요.",
     "side": [{"field": {"k": "상담료", "v": "30분 50,000원 · 수임 시 차감", "src": "변호사님 요금표"}},
              {"field": {"k": "기한 서류", "v": "내용증명 · 수령일 확인 요청", "src": "통화에서"}}]},
    {"who": "user", "text": "내일 4시로 부탁드려요. 상대는 전에 거래하던 업체예요.",
     "side": [{"field": {"k": "사건 유형", "v": "민사 · 상대방 있음 · 거래 업체", "src": "본인 발화"}}]},
    {"who": "ai", "text": "알겠습니다. 성함과 연락처를 말씀해 주시겠어요?"},
    {"who": "user", "text": "정우진이고요, 010-3362-4715예요.",
     "side": [{"field": {"k": "이름", "v": "정우진", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-3362-47··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "정우진 님, 내일 오후 4시 상담 예약되었습니다. 확인 문자를 지금 보내 드릴게요. 오실 때 받으신 내용증명 원본과, 그 업체와 주고받은 계약서나 문자가 있으면 함께 가져오시면 상담이 훨씬 빨라져요.",
     "side": [{"field": {"k": "상담 예약", "v": "화 16:00", "src": "캘린더의 빈 시간"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "상담 예약 확정", "v": "화 16:00 · 캘린더에 들어감 · 확인 문자와 지참 서류 안내 발송"}}]},
    {"who": "user", "text": "받은 지 며칠 됐는데, 언제까지 답을 해야 하나요?"},
    {"who": "ai", "text": "기한은 제가 단정해 드릴 수 없어요. 받으신 날짜만 확인해 두시면, 내일 변호사님이 서류를 보고 바로 말씀드릴 거예요. 내일 뵙겠습니다.",
     "side": [{"work": {"icon": "#", "k": "접수 기록 #0917", "v": "상담료 50,000원 · 지참 서류 안내 — 요금표에서"}},
              {"work": {"icon": "@", "k": "담당 · 기한", "v": "사무장 조은영 배정 · 화 15:30까지 상담 카드 준비"}},
              {"work": {"icon": "↻", "k": "후속 문자", "v": "당일 오전 리마인드 초안 — 발송 전 사무장 확인"}}]},
    {"who": "user", "text": "네, 감사합니다."},
    {"who": "ai", "text": "감사합니다. 편안한 밤 되세요."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "어제 예약한 정우진입니다. 사무실에 주차 되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "네 — 건물 지하 주차장 1시간 무료예요. 오늘 오후 4시 상담은 그대로입니다.", "merge": True},
    {"who": "user", "when": "7:42 AM", "text": "솔직히, 이거 이길 수 있는 사건인가요?"},
    {"who": "ai", "when": "+2 sec", "text": "사건의 전망은 변호사님이 서류를 보고 말씀드릴 부분이라 제가 답할 수 없어요. 대화 내용을 그대로 전달했고, 오전 중에 사무실에서 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 사건의 전망은 법률 판단이라 변호사만 말할 수 있습니다"],
   "morning": [
    {"icon": "✓", "k": "새 상담 예약 1건", "v": "정우진 · 화 16:00 · 민사 · 내용증명"},
    {"icon": "#", "k": "접수 기록 #0917", "v": "상담료 50,000원 · 지참 서류 안내 문자 발송 · 열람 확인"},
    {"icon": "@", "k": "사무장 할 일", "v": "화 15:30까지 상담 카드 준비 · 담당 조은영"},
    {"icon": "!", "k": "답변 대기 1건", "v": "사건 전망 질문 · 대화 전체 첨부 · 변호사님 확인"}
   ],
   "person": {"when": "9:12 AM", "text": "사무장 조은영입니다. 정우진 님, 전망은 변호사님이 서류를 직접 보신 뒤 오늘 상담에서 말씀드릴게요. 내용증명 원본을 꼭 가져오세요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 변호사님이 재판을 준비하는 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Onjung Law Office", "owner": "the attorney",
   "meta": "Monday 7:41 PM · preparing for court · a fictional law office", "callTime": "7:41 PM", "chan": "WhatsApp",
   "chapters": ["7:41 PM, the call", "Next morning, WhatsApp", "9:00 AM, the attorney's screen"],
   "chapterSubs": ["demand letter · consultation fee · tomorrow at 4 booked", "parking · the case outlook goes to a person", "consultation · intake record · paralegal · one reply waiting"],
   "sys": {"ring": "7:41 PM — the phone rings. The attorney is preparing for tomorrow's hearing.",
           "chat": "Next morning, 7:40 AM — the same client, on WhatsApp.",
           "morning": "9:00 AM — the attorney's screen."},
   "customer": {"name": "James Jung", "phone": "555-05··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Onjung Law Office. Consultations are finished for the day, but I can book one and answer general questions. How can I help?"},
    {"who": "user", "text": "I've received a formal demand letter. Can I get a consultation, and what does it cost?",
     "side": [{"field": {"k": "Enquiry", "v": "demand letter received · consultation", "src": "from the call"}}]},
    {"who": "ai", "text": "You can. An initial consultation is one hundred and fifty dollars for thirty minutes, and if you retain the firm that amount comes off the fee. Demand letters often carry a response deadline, so please note the date you received it. Tomorrow at four in the afternoon is open.",
     "side": [{"field": {"k": "Consultation fee", "v": "$150 for 30 min · credited if retained", "src": "your fee schedule"}},
              {"field": {"k": "Deadline document", "v": "demand letter · date received to confirm", "src": "from the call"}}]},
    {"who": "user", "text": "Four tomorrow works. The other side is a company I used to do business with.",
     "side": [{"field": {"k": "Matter type", "v": "civil · opposing party · former business partner", "src": "caller said it"}}]},
    {"who": "ai", "text": "Understood. Can I get your name and a mobile number?"},
    {"who": "user", "text": "James Jung, five five five, zero five one five.",
     "side": [{"field": {"k": "Name", "v": "James Jung", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-05··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, James. You're booked for tomorrow at four. I'm texting the confirmation now. Please bring the original letter, and any contract or messages between you and that company — it makes the consultation much faster.",
     "side": [{"field": {"k": "Consultation", "v": "Tue 4:00 PM", "src": "free in your calendar"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "Consultation booked", "v": "Tue 4:00 · in your calendar · confirmation and document checklist sent"}}]},
    {"who": "user", "text": "It's been a few days already. How long do I have to respond?"},
    {"who": "ai", "text": "That's not something I can determine for you. Just note the date you received it, and the attorney will tell you exactly where you stand tomorrow. We'll see you at four.",
     "side": [{"work": {"icon": "#", "k": "Intake record #0917", "v": "consultation $150 · document checklist — from your fee schedule"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "assigned to Eunyoung · intake file ready by Tue 3:30"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "same-day reminder drafted — the paralegal approves before it sends"}}]},
    {"who": "user", "text": "Okay, thank you."},
    {"who": "ai", "text": "Thank you. Have a good evening."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "Hi, James Jung from last night — is there parking at the office?"},
    {"who": "ai", "when": "+2 sec", "text": "Yes — one hour free in the building's garage. Your consultation today at four is unchanged.", "merge": True},
    {"who": "user", "when": "7:42 AM", "text": "Honestly — is this a case I can win?"},
    {"who": "ai", "when": "+2 sec", "text": "Only the attorney can speak to that, and only after reading the documents. I've passed our conversation along — the office will reply this morning.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: the outlook of a case is legal judgement, and only the attorney gives it"],
   "morning": [
    {"icon": "✓", "k": "New consultation", "v": "James Jung · Tue 4:00 · civil · demand letter"},
    {"icon": "#", "k": "Intake record #0917", "v": "consultation $150 · document checklist sent by text · opened"},
    {"icon": "@", "k": "Paralegal task", "v": "intake file ready by Tue 3:30 · owner: Eunyoung"},
    {"icon": "!", "k": "Waiting for a person", "v": "case outlook question · full thread attached · for the attorney"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Eunyoung, the paralegal. Hi James — the attorney will read your letter first and give you a straight answer at four today. Please bring the original."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the attorney was preparing for court.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────── 공공기관 ─────────────────────────
 "public-sector": {
  "ko": {
   "biz": "하늘동 주민센터", "owner": "담당 과장님",
   "meta": "화요일 12:24 PM · 점심시간, 창구 부재 · 가상의 주민센터", "callTime": "12:24 PM", "chan": "카카오톡",
   "chapters": ["낮 12:24, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 담당 과장 화면"],
   "chapterSubs": ["전입신고 서류 · 대리 신고 · 오후 1시 회신 접수", "위임장 양식 · 지원 대상 판단은 사람에게", "접수 · 접수 번호 · 민원팀 · 답변 대기"],
   "sys": {"ring": "낮 12:24 — 전화벨이 울립니다. 점심시간이라 창구가 비었습니다.",
           "chat": "다음 날 아침 8:50 — 같은 민원인이 카카오톡으로. 업무 시작 전입니다.",
           "morning": "오전 9:00 — 담당 과장 화면."},
   "customer": {"name": "한지민", "phone": "010-8827-13··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 하늘동 주민센터입니다. 지금은 점심시간이라 창구 직원이 자리에 없지만, 서류 안내와 담당 부서 연결은 제가 도와드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "전입신고를 하려는데 필요한 서류가 뭔가요? 어머니 대신 제가 가도 되나요?",
     "side": [{"field": {"k": "민원 유형", "v": "전입신고 · 대리 신고", "src": "통화에서"}}]},
    {"who": "ai", "text": "네, 본인이 오시면 신분증만 있으면 돼요. 대리인이 오시면 위임장, 위임하시는 분의 신분증 사본, 그리고 오시는 분의 신분증이 필요합니다. 정부24에서 온라인으로도 신청하실 수 있어요.",
     "side": [{"field": {"k": "구비 서류", "v": "위임장 · 위임인 신분증 사본 · 대리인 신분증", "src": "등록된 안내 기준"}}]},
    {"who": "user", "text": "온라인으로 하면 언제 처리되나요?"},
    {"who": "ai", "text": "처리 시점은 신청 내용에 따라 달라서 담당 부서에서 확인해 드려야 해요. 점심시간이 끝나는 오후 1시 이후에 민원팀에서 전화드릴 수 있는데, 대기 접수해 드릴까요?",
     "side": [{"field": {"k": "담당 부서", "v": "민원팀 · 13시 이후 회신", "src": "등록된 안내 기준"}}]},
    {"who": "user", "text": "네, 부탁드려요. 한지민이고요, 010-8827-1349예요.",
     "side": [{"field": {"k": "이름", "v": "한지민", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-8827-13··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "한지민 님, 오후 1시 이후 민원팀 회신으로 접수했습니다. 접수 번호는 문자로 보내 드릴게요. 연락 받기 편한 시간이 따로 있으세요?",
     "side": [{"crm": True},
              {"work": {"icon": "✓", "k": "대기 접수", "v": "민원팀 회신 대기 · 13:00 이후 · 접수 번호 문자 발송"}}]},
    {"who": "user", "text": "1시 반 이후면 좋겠어요.",
     "side": [{"field": {"k": "회신 희망", "v": "13:30 이후", "src": "본인 발화"}}]},
    {"who": "ai", "text": "1시 반 이후로 남겨 두었어요. 담당자가 순서대로 전화드릴 거예요. 다른 문의는 이 번호로 언제든 다시 연락 주세요.",
     "side": [{"work": {"icon": "#", "k": "접수 번호 #5521", "v": "전입신고 대리 · 구비 서류 안내 — 안내 기준에서"}},
              {"work": {"icon": "@", "k": "담당 · 기한", "v": "민원팀 김현우 주무관 배정 · 오늘 13:30 이후 회신"}},
              {"work": {"icon": "↻", "k": "회신 확인", "v": "회신 완료 여부 17:00 자동 확인 — 미회신 시 과장 알림"}}]},
    {"who": "user", "text": "감사합니다."},
    {"who": "ai", "text": "감사합니다. 좋은 하루 되세요."}
   ],
   "chat": [
    {"who": "user", "when": "8:50 AM", "text": "어제 전화한 한지민입니다. 위임장 양식은 어디서 받나요?"},
    {"who": "ai", "when": "+2 sec", "text": "주민센터 홈페이지 서식 자료실에서 내려받으실 수 있고, 창구에도 비치되어 있어요. 어제 접수 건은 민원팀에서 회신 완료로 되어 있습니다.", "merge": True},
    {"who": "user", "when": "8:52 AM", "text": "전입하면 어머니가 전입 지원금 대상이 되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "지원 대상 여부는 담당 부서에서 요건을 확인하고 판단할 부분이라 제가 답할 수 없어요. 문의 내용을 그대로 전달했고, 9시에 업무가 시작되면 담당자가 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 지원 대상 판단은 안내가 아니라 담당 부서의 결정입니다"],
   "morning": [
    {"icon": "✓", "k": "민원 접수 1건", "v": "한지민 · 전입신고 대리 · 어제 13:40 회신 완료"},
    {"icon": "#", "k": "접수 번호 #5521", "v": "구비 서류 안내 · 문자로 발송됨 · 열람 확인"},
    {"icon": "@", "k": "민원팀 할 일", "v": "전입 지원금 요건 확인 · 담당 김현우 주무관"},
    {"icon": "!", "k": "답변 대기 1건", "v": "전입 지원금 대상 문의 · 대화 전체 첨부 · 담당 김현우 주무관"}
   ],
   "person": {"when": "9:12 AM", "text": "민원팀 김현우 주무관입니다. 한지민 님, 전입 지원금은 전입일과 세대 구성에 따라 달라서 신고 접수하실 때 창구에서 요건을 바로 확인해 드릴게요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 창구가 빈 동안 끝났습니다.",
   "honest": "각본이 있는 시연 · 예시 데이터 · 두 목소리는 이 데모를 위해 만든 합성 음성입니다 · 안내 내용과 금액은 예시 요금표입니다."
  },
  "en": {
   "biz": "Riverside District Office", "owner": "the office manager",
   "meta": "Tuesday 12:24 PM · lunch hour, counter unattended · a fictional district office", "callTime": "12:24 PM", "chan": "WhatsApp",
   "chapters": ["12:24 PM, the call", "Next morning, WhatsApp", "9:00 AM, the office manager's screen"],
   "chapterSubs": ["address change · by proxy · callback logged for after 1", "the form · the eligibility ruling goes to a person", "enquiry · reference · residents' team · one reply waiting"],
   "sys": {"ring": "12:24 PM — the phone rings. It's the lunch hour and the counter is unattended.",
           "chat": "Next morning, 8:50 AM — the same resident, on WhatsApp, before the office opens.",
           "morning": "9:00 AM — the office manager's screen."},
   "customer": {"name": "Mina Han", "phone": "555-06··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Riverside District Office. It's the lunch hour and the counter is unattended, but I can tell you what documents you need and route you to the right team. How can I help?"},
    {"who": "user", "text": "I need to register a change of address. What do I bring? And can I do it for my mother, on her behalf?",
     "side": [{"field": {"k": "Enquiry type", "v": "address registration · by proxy", "src": "from the call"}}]},
    {"who": "ai", "text": "If she comes in herself, just her photo ID. If you come on her behalf, you'll need a signed authorisation letter, a copy of her ID, and your own ID. It can also be filed online through the government portal.",
     "side": [{"field": {"k": "Documents", "v": "authorisation letter · copy of her ID · your ID", "src": "your approved guidance"}}]},
    {"who": "user", "text": "If I file online, when does it get processed?"},
    {"who": "ai", "text": "That depends on what's in the application, so the residents' team has to confirm it. They're back from lunch at one. Shall I log a callback so they ring you?",
     "side": [{"field": {"k": "Responsible team", "v": "residents' team · callback after 1 PM", "src": "your approved guidance"}}]},
    {"who": "user", "text": "Yes, please. Mina Han, five five five, zero six four nine.",
     "side": [{"field": {"k": "Name", "v": "Mina Han", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-06··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, Mina. Your callback is logged with the residents' team for after one o'clock, and I'm texting you a reference number now. Is there a time that suits you best?",
     "side": [{"crm": True},
              {"work": {"icon": "✓", "k": "Callback logged", "v": "residents' team · after 1:00 PM · reference number sent by text"}}]},
    {"who": "user", "text": "After one thirty would be better.",
     "side": [{"field": {"k": "Preferred time", "v": "after 1:30 PM", "src": "caller said it"}}]},
    {"who": "ai", "text": "Noted, after one thirty. They'll call in order. If anything else comes up, this number is answered any time.",
     "side": [{"work": {"icon": "#", "k": "Reference #5521", "v": "address change by proxy · document checklist — from your guidance"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "assigned to Officer Kim · callback after 1:30 today"}},
              {"work": {"icon": "↻", "k": "Callback check", "v": "auto-check at 5:00 PM — the manager is alerted if no one called"}}]},
    {"who": "user", "text": "Thank you."},
    {"who": "ai", "text": "Thank you. Have a good day."}
   ],
   "chat": [
    {"who": "user", "when": "8:50 AM", "text": "Hi, Mina Han from yesterday — where do I get the authorisation letter form?"},
    {"who": "ai", "when": "+2 sec", "text": "It's under Forms on the district office website, and printed copies are at the counter. Yesterday's callback is marked as completed by the residents' team.", "merge": True},
    {"who": "user", "when": "8:52 AM", "text": "Once she moves in, would my mother qualify for the relocation allowance?"},
    {"who": "ai", "when": "+2 sec", "text": "Eligibility is a ruling for the residents' team after they check the requirements — not something I can decide. I've passed your question along, and someone will call once the office opens at nine.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: eligibility is a ruling by the responsible team, not information on file"],
   "morning": [
    {"icon": "✓", "k": "Enquiry logged", "v": "Mina Han · address change by proxy · callback completed 1:40 PM yesterday"},
    {"icon": "#", "k": "Reference #5521", "v": "document checklist · sent by text · opened"},
    {"icon": "@", "k": "Team task", "v": "check relocation allowance requirements · owner: Officer Kim"},
    {"icon": "!", "k": "Waiting for a person", "v": "eligibility question · full thread attached · owner: Officer Kim"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Officer Kim from the residents' team. Hi Mina — the allowance depends on the move-in date and the household, so we'll check the requirements at the counter when you file."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while the counter was empty.",
   "honest": "Scripted simulation · sample data · both voices were synthesised for this demo · procedures are illustrative and figures are an example price list."
  }
 },

 # ───────────────────────── 장례식장 ─────────────────────────
 "funeral-homes": {
  "ko": {
   "biz": "평안장례식장", "owner": "담당자님",
   "meta": "일요일 3:12 AM · 당직 담당자 이송 중 · 가상의 장례식장", "callTime": "3:12 AM", "chan": "카카오톡",
   "chapters": ["새벽 3:12, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 담당자 화면"],
   "chapterSubs": ["부친상 · 병원 접수 · 담당자 연결", "주차 질문 · 빈소 규모는 사람에게", "접수 · 접수 번호 · 담당 · 답변 대기"],
   "sys": {"ring": "새벽 3:12 — 전화벨이 울립니다. 당직 담당자는 이송 차량에 있습니다.",
           "chat": "다음 날 아침 7:40 — 같은 유족이 카카오톡으로.",
           "morning": "오전 9:00 — 담당자 화면."},
   "customer": {"name": "윤태호", "phone": "010-6604-35··"},
   "lines": [
    {"who": "ai", "text": "평안장례식장입니다. 밤늦은 시간이지만 제가 듣고 있어요. 천천히 말씀해 주세요."},
    {"who": "user", "text": "아버지가 방금 돌아가셨는데… 어떻게 해야 하나요.",
     "side": [{"field": {"k": "접수", "v": "부친상 · 새벽 3:12", "src": "통화에서"}}]},
    {"who": "ai", "text": "먼저 깊은 위로의 말씀 드립니다. 지금 담당자에게 바로 연결해 드릴게요. 연결되는 동안, 지금 계신 병원 이름만 알려 주시겠어요? 이송 준비를 먼저 시작할 수 있어요."},
    {"who": "user", "text": "한솔대학교병원 응급실이에요.",
     "side": [{"field": {"k": "현재 장소", "v": "한솔대학교병원 응급실", "src": "본인 발화"}},
              {"work": {"icon": "@", "k": "이송 준비", "v": "한솔대학교병원 응급실 · 당직 김성호 부장에게 전달 · 이송 필요"}}]},
    {"who": "ai", "text": "한솔대학교병원 응급실로 접수했습니다. 전화 주신 분은 고인과 어떤 관계이신지, 성함과 연락처를 말씀해 주시겠어요? 담당자가 바로 이 번호로 연락드릴 수 있게요."},
    {"who": "user", "text": "아들 윤태호고요, 010-6604-3518이에요.",
     "side": [{"field": {"k": "연락 주신 분", "v": "아들 · 윤태호", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-6604-35··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "윤태호 님, 감사합니다. 당직 담당자 김성호 부장에게 지금 연결하고 있어요. 연결이 끊기더라도 3분 안에 이 번호로 다시 전화드릴 거예요. 그때까지 아버님 곁에 계셔 주세요.",
     "side": [{"field": {"k": "담당자 연결", "v": "당직 김성호 부장 · 3:14", "src": "당직 담당표"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "담당자 연결", "v": "당직 김성호 부장 · 3:14 통화 연결 · 미연결 시 3분 내 회신"}}]},
    {"who": "user", "text": "네… 감사합니다."},
    {"who": "ai", "text": "지금 연결합니다. 잠시만 기다려 주세요.",
     "side": [{"work": {"icon": "#", "k": "접수 번호 #0312", "v": "부친상 · 한솔대학교병원 · 3:12 접수 · 유족 연락처"}},
              {"work": {"icon": "↻", "k": "후속 연락", "v": "담당자 통화 후 카드 갱신 · 유족에게는 담당자가 직접 연락"}}]}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "어젯밤 통화한 윤태호입니다. 빈소 오시는 분들 주차는 어디로 안내하면 되나요?"},
    {"who": "ai", "when": "+2 sec", "text": "장례식장 지하 주차장을 이용하시면 되고, 조문객은 3시간 무료예요. 어젯밤 접수 건은 김성호 부장님이 맡고 계십니다.", "merge": True},
    {"who": "user", "when": "7:43 AM", "text": "빈소는 어느 정도 크기로 해야 할까요? 저희가 잘 몰라서요."},
    {"who": "ai", "when": "+2 sec", "text": "그건 제가 권해 드릴 일이 아니에요. 가족분들과 담당자가 만나서 정하시는 게 맞아요. 김성호 부장님께 지금 바로 전달했고, 곧 직접 연락드릴 거예요.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 빈소 규모와 장례 형식은 기계가 권하지 않습니다. 사람이 만나서 정할 일입니다"],
   "morning": [
    {"icon": "✓", "k": "접수 1건", "v": "윤태호 님 · 부친상 · 한솔대학교병원 · 3:12 접수"},
    {"icon": "#", "k": "접수 번호 #0312", "v": "이송 기록 · 유족 연락처 · 후속 연락은 담당자 직접"},
    {"icon": "@", "k": "담당", "v": "당직 김성호 부장 · 3:14 연결 · 4:05 이송 완료"},
    {"icon": "!", "k": "답변 대기 1건", "v": "빈소 규모 문의 · 대화 전체 첨부 · 담당 김성호 부장"}
   ],
   "person": {"when": "8:05 AM", "text": "담당 김성호입니다. 윤태호 님, 빈소는 조문 오실 분들 규모를 여쭤 보고 함께 정하면 됩니다. 9시 반에 제가 직접 찾아뵙고 천천히 안내드리겠습니다."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 3분 안에 받은 전화 한 통과 답장 한 줄. 기계는 그 사이를 지켰을 뿐입니다.",
   "honest": "각본이 있는 시연 · 예시 데이터 · 두 목소리는 이 데모를 위해 만든 합성 음성입니다 · 금액은 예시 요금표이며 이 통화에서는 말하지 않습니다."
  },
  "en": {
   "biz": "Evergreen Funeral Home", "owner": "the director",
   "meta": "Sunday 3:12 AM · the director on call is out on a transfer · a fictional funeral home", "callTime": "3:12 AM", "chan": "WhatsApp",
   "chapters": ["3:12 AM, the call", "Next morning, WhatsApp", "9:00 AM, the director's screen"],
   "chapterSubs": ["a father's death · the hospital · the director connected", "parking · the room question goes to a person", "case · case file · director · one reply waiting"],
   "sys": {"ring": "3:12 AM — the phone rings. The director on call is in the transfer vehicle.",
           "chat": "Next morning, 7:40 AM — the same family member, on WhatsApp.",
           "morning": "9:00 AM — the director's screen."},
   "customer": {"name": "Thomas Yoon", "phone": "555-07··"},
   "lines": [
    {"who": "ai", "text": "Evergreen Funeral Home. It's late, and I'm here. Take your time."},
    {"who": "user", "text": "My father just passed away… I don't know what to do.",
     "side": [{"field": {"k": "Case", "v": "father's death · 3:12 AM", "src": "from the call"}}]},
    {"who": "ai", "text": "I'm so sorry for your loss. I'm going to put you through to our director right now. While I connect you, could you tell me just the name of the hospital you're at? That lets us start arranging the transfer."},
    {"who": "user", "text": "Hansol University Hospital, the emergency department.",
     "side": [{"field": {"k": "Place", "v": "Hansol University Hospital · emergency dept", "src": "caller said it"}},
              {"work": {"icon": "@", "k": "Transfer prep", "v": "Hansol University Hospital ED · passed to Sungho Kim on call · transfer needed"}}]},
    {"who": "ai", "text": "Hansol University Hospital, emergency department — noted. May I ask how you're related to your father, and your name and a number the director can reach you on?"},
    {"who": "user", "text": "I'm his son, Thomas Yoon. Five five five, zero seven one eight.",
     "side": [{"field": {"k": "Caller", "v": "son · Thomas Yoon", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-07··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, Thomas. I'm connecting you to Sungho Kim, our director on call. If the line drops, he will ring you back on this number within three minutes. Until then, stay with your father.",
     "side": [{"field": {"k": "Director connected", "v": "Sungho Kim on call · 3:14", "src": "on-call roster"}}, {"crm": True},
              {"work": {"icon": "✓", "k": "Director connected", "v": "Sungho Kim · line joined 3:14 · callback within 3 min if dropped"}}]},
    {"who": "user", "text": "Okay… thank you."},
    {"who": "ai", "text": "Connecting you now. Please hold for a moment.",
     "side": [{"work": {"icon": "#", "k": "Case file #0312", "v": "father's death · Hansol University Hospital · logged 3:12 · family contact"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "card updated after the director's call · the director contacts the family himself"}}]}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "Hi, Thomas Yoon from last night. Where should I tell people to park for the visitation?"},
    {"who": "ai", "when": "+2 sec", "text": "The funeral home's underground car park — three hours free for visitors. Sungho Kim is handling everything from last night.", "merge": True},
    {"who": "user", "when": "7:43 AM", "text": "What size room should we take for the visitation? We really don't know."},
    {"who": "ai", "when": "+2 sec", "text": "That's not something I should recommend. It's a decision for your family to make together with the director. I've passed it to Sungho just now, and he'll call you himself shortly.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: the room and the form of the service are never suggested by a machine — that's for a person, in the room"],
   "morning": [
    {"icon": "✓", "k": "Case opened", "v": "Thomas Yoon · father · Hansol University Hospital · logged 3:12 AM"},
    {"icon": "#", "k": "Case file #0312", "v": "transfer record · family contact · follow-up by the director"},
    {"icon": "@", "k": "Director", "v": "Sungho Kim on call · connected 3:14 · transfer completed 4:05"},
    {"icon": "!", "k": "Waiting for a person", "v": "visitation room question · full thread attached · owner: Sungho"}
   ],
   "person": {"when": "8:05 AM", "text": "This is Sungho. Thomas, we'll choose the room together once we know roughly how many people will come. I'll come and see you at nine thirty and walk you through everything, slowly."},
   "summary": "One {call} call · four messages · what a person did: one call answered within three minutes, one reply. The machine only held the line in between.",
   "honest": "Scripted simulation · sample data · both voices were synthesised for this demo · figures are an example price list, and none are quoted in this call."
  }
 },

 # ───────────────────────── 온라인 쇼핑몰 ─────────────────────────
 "ecommerce": {
  "ko": {
   "biz": "모드앤데이", "owner": "대표님",
   "meta": "목요일 11:31 PM · 고객센터 퇴근 후 · 가상의 쇼핑몰", "callTime": "11:31 PM", "chan": "카카오톡",
   "chapters": ["밤 11:31, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 대표님 화면"],
   "chapterSubs": ["원피스 사이즈 · 내일 출고 · 교환 규정", "출고 질문 · 도착 보장은 사람에게", "주문 · 안내 기록 · CS · 답변 대기"],
   "sys": {"ring": "밤 11:31 — 전화벨이 울립니다. 고객센터는 오후 6시에 퇴근했습니다.",
           "chat": "다음 날 아침 7:40 — 같은 손님이 카카오톡으로.",
           "morning": "오전 9:00 — 대표님 화면."},
   "customer": {"name": "오수아", "phone": "010-4190-72··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 모드앤데이입니다. 고객센터 운영 시간은 끝났지만, 상품과 배송 문의는 제가 도와드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "린넨 셔츠 원피스 베이지요, 55 사이즈면 넉넉한가요? 모레까지 받아야 하는데 가능해요?",
     "side": [{"field": {"k": "문의 상품", "v": "린넨 셔츠 원피스 · 베이지 · 55", "src": "통화에서"}},
              {"field": {"k": "문의 유형", "v": "사이즈 · 배송", "src": "통화에서"}}]},
    {"who": "ai", "text": "이 제품은 정사이즈로 나와서 평소 55 입으시면 맞아요. 어깨가 좁게 나온 편이라 어깨가 넓으시면 66을 권해 드려요. 베이지 55는 재고가 있고, 지금 주문하시면 내일 출고돼요. 도착일은 택배사가 정해서 제가 확정해 드릴 수는 없고, 보통 출고 다음 날 받으세요.",
     "side": [{"field": {"k": "재고 · 출고", "v": "베이지 55 재고 있음 · 내일 출고", "src": "재고 현황"}}]},
    {"who": "user", "text": "어깨는 보통이에요. 안 맞으면 교환 되나요?"},
    {"who": "ai", "text": "받으신 날부터 7일 안에 교환 가능하고, 단순 변심이면 왕복 배송비 5천원이 부담돼요. 착용 흔적이 없어야 하고요.",
     "side": [{"field": {"k": "교환 규정", "v": "7일 이내 · 왕복 5,000원 · 미착용", "src": "등록된 약관"}}]},
    {"who": "user", "text": "알겠어요. 주문하면 송장을 문자로 받을 수 있나요?"},
    {"who": "ai", "text": "네, 성함과 연락처를 말씀해 주시면 출고될 때 송장 번호를 바로 문자 드릴게요."},
    {"who": "user", "text": "오수아고요, 010-4190-7263이에요.",
     "side": [{"field": {"k": "이름", "v": "오수아", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-4190-72··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "오수아 님, 이 번호로 송장 문자 보내 드릴게요. 주문은 앱이나 사이트에서 결제해 주시면 되고, 오늘 문의하신 사이즈 내용은 주문에 메모로 붙여 둘게요.",
     "side": [{"crm": True},
              {"work": {"icon": "✓", "k": "문의 메모", "v": "사이즈 · 배송 · 교환 안내 내역 — 주문에 자동 첨부 · 송장 문자 예약"}}]},
    {"who": "user", "text": "지금 바로 결제할게요."},
    {"who": "ai", "text": "감사합니다. 결제가 확인되면 내일 출고 순서에 올라가요. 편안한 밤 되세요.",
     "side": [{"work": {"icon": "#", "k": "안내 기록 #48213", "v": "교환 7일 · 왕복 5,000원 · 내일 출고 — 약관과 재고에서"}},
              {"work": {"icon": "@", "k": "담당 · 기한", "v": "CS 임채원 배정 · 오전 출고 1순위"}},
              {"work": {"icon": "↻", "k": "후속 문자", "v": "출고 시 송장 자동 발송 · 미결제 시 D+1 안내 초안 — 발송 전 대표님 확인"}}]}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "어제 전화한 오수아예요. 주문번호 48213인데 출고됐나요?"},
    {"who": "ai", "when": "+2 sec", "text": "네 — 오늘 아침 출고 순서에 올라가 있어요. 송장이 나오면 이 번호로 바로 문자 드립니다.", "merge": True},
    {"who": "user", "when": "7:42 AM", "text": "모레 오전에 꼭 입어야 하는데, 모레 오전까지 도착 확실한가요?"},
    {"who": "ai", "when": "+2 sec", "text": "도착 시각은 택배사가 정하는 거라 제가 확실하다고 말씀드릴 수 없어요. 담당자에게 상황을 그대로 전달했고, 출고 전에 확인해서 연락드릴게요.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 도착일 보장은 재고나 약관에 있는 사실이 아니라 약속입니다"],
   "morning": [
    {"icon": "✓", "k": "새 주문 1건", "v": "오수아 · #48213 · 린넨 셔츠 원피스 베이지 55 · 결제 완료 23:52"},
    {"icon": "#", "k": "안내 기록 #48213", "v": "교환 7일 · 왕복 5,000원 · 문자로 발송됨 · 열람 확인"},
    {"icon": "@", "k": "CS 할 일", "v": "오전 출고 1순위 · 담당 임채원"},
    {"icon": "!", "k": "답변 대기 1건", "v": "모레 오전 도착 보장 문의 · 대화 전체 첨부 · 담당 임채원"}
   ],
   "person": {"when": "9:12 AM", "text": "CS 임채원입니다. 오수아 님, 오늘 첫 집하로 보내 드리고 택배사에 익일 배송으로 확인 요청해 두었어요. 택배사 스캔이 뜨면 바로 문자 드릴게요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 장바구니는 대표님이 자는 동안 결제로 바뀌었습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Mode and Day", "owner": "the owner",
   "meta": "Thursday 11:31 PM · customer service gone home · a fictional online store", "callTime": "11:31 PM", "chan": "WhatsApp",
   "chapters": ["11:31 PM, the call", "Next morning, WhatsApp", "9:00 AM, the owner's screen"],
   "chapterSubs": ["dress size · ships tomorrow · exchange policy", "shipping question · the delivery guarantee goes to a person", "order · policy note · CS · one reply waiting"],
   "sys": {"ring": "11:31 PM — the phone rings. Customer service went home at six.",
           "chat": "Next morning, 7:40 AM — the same customer, on WhatsApp.",
           "morning": "9:00 AM — the owner's screen."},
   "customer": {"name": "Sua Oh", "phone": "555-08··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Mode and Day. Customer service is closed for the night, but I can help with products and shipping. What can I do for you?"},
    {"who": "user", "text": "The linen shirt dress in beige — does a size small run roomy? I need it by the day after tomorrow. Is that possible?",
     "side": [{"field": {"k": "Product", "v": "linen shirt dress · beige · S", "src": "from the call"}},
              {"field": {"k": "Enquiry type", "v": "sizing · shipping", "src": "from the call"}}]},
    {"who": "ai", "text": "It's true to size, so if you usually wear a small, a small will fit. The shoulders run a little narrow, so if you have broader shoulders I'd suggest a medium. Beige in small is in stock, and if you order tonight it ships tomorrow. The delivery date is set by the carrier, so I can't confirm it, but it usually arrives the day after shipping.",
     "side": [{"field": {"k": "Stock · ships", "v": "beige S in stock · ships tomorrow", "src": "live inventory"}}]},
    {"who": "user", "text": "My shoulders are average. Can I exchange it if it doesn't fit?"},
    {"who": "ai", "text": "Yes — within seven days of delivery. If it's a change of mind, return shipping both ways is eight dollars, and the item needs to be unworn.",
     "side": [{"field": {"k": "Exchange policy", "v": "within 7 days · $8 return shipping · unworn", "src": "your published terms"}}]},
    {"who": "user", "text": "Okay. If I order, can I get the tracking number by text?"},
    {"who": "ai", "text": "Of course. Give me your name and mobile number and I'll text the tracking number the moment it ships."},
    {"who": "user", "text": "Sua Oh, five five five, zero eight six three.",
     "side": [{"field": {"k": "Name", "v": "Sua Oh", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-08··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, Sua. I'll text tracking to this number. Place the order in the app or on the site, and I'll attach tonight's sizing notes to it so the team has them.",
     "side": [{"crm": True},
              {"work": {"icon": "✓", "k": "Enquiry note", "v": "sizing · shipping · exchange advice — attached to the order · tracking text scheduled"}}]},
    {"who": "user", "text": "I'll pay right now."},
    {"who": "ai", "text": "Thank you. Once payment clears you're in tomorrow's shipping queue. Have a good night.",
     "side": [{"work": {"icon": "#", "k": "Policy note #48213", "v": "exchange within 7 days · $8 return shipping · ships tomorrow — from your terms and inventory"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "assigned to Chaewon in CS · first in the morning dispatch"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "tracking text on dispatch · D+1 nudge drafted if unpaid — you approve before it sends"}}]}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "Hi, Sua Oh from last night — order forty-eight two thirteen. Has it shipped?"},
    {"who": "ai", "when": "+2 sec", "text": "It's in this morning's shipping queue. I'll text the tracking number to this phone as soon as the label prints.", "merge": True},
    {"who": "user", "when": "7:42 AM", "text": "I have to wear it the morning after tomorrow. Can you guarantee it arrives by then?"},
    {"who": "ai", "when": "+2 sec", "text": "The arrival time is set by the carrier, so I can't promise it. I've passed this to the team as it stands — they'll check before it ships and get back to you.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: a guaranteed delivery date is a promise, not a fact in stock or in the policy"],
   "morning": [
    {"icon": "✓", "k": "New order", "v": "Sua Oh · #48213 · linen shirt dress beige S · paid 11:52 PM"},
    {"icon": "#", "k": "Policy note #48213", "v": "exchange within 7 days · $8 return shipping · sent by text · opened"},
    {"icon": "@", "k": "CS task", "v": "first in the morning dispatch · owner: Chaewon"},
    {"icon": "!", "k": "Waiting for a person", "v": "delivery guarantee question · full thread attached · owner: Chaewon"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Chaewon from customer service. Hi Sua — it's going out on today's first pickup and I've asked the carrier for next-day delivery. I'll text you the moment their scan confirms it."},
   "summary": "One {call} call · four messages · what a person did: one reply. The cart became an order while the owner slept.",
   "honest": HONEST_EN
  }
 },

 # ───────────────────────── 프랜차이즈 본부 ─────────────────────────
 "franchise": {
  "ko": {
   "biz": "달빛치킨 본사", "owner": "대표님",
   "meta": "수요일 9:07 PM · 본사 퇴근 후 · 가상의 프랜차이즈 본부", "callTime": "9:07 PM", "chan": "카카오톡",
   "chapters": ["밤 9:07, 전화", "다음 날 아침, 카카오톡", "오전 9:00, 대표님 화면"],
   "chapterSubs": ["가맹 문의 · 창업 비용 · 담당자 배정", "상담 장소 질문 · 예상 매출은 사람에게", "가맹 문의 · 정보공개서 · 담당 · 답변 대기"],
   "sys": {"ring": "밤 9:07 — 대표번호가 울립니다. 본사는 오후 6시에 퇴근했습니다.",
           "chat": "다음 날 아침 7:40 — 같은 예비 점주가 카카오톡으로.",
           "morning": "오전 9:00 — 대표님 화면."},
   "customer": {"name": "강도현", "phone": "010-9245-58··"},
   "lines": [
    {"who": "ai", "text": "안녕하세요, 달빛치킨 본사입니다. 본사 업무 시간은 끝났지만, 가맹 문의와 매장 관련 접수는 제가 도와드릴 수 있어요. 무엇을 도와드릴까요?"},
    {"who": "user", "text": "가맹 문의인데요. 창업 비용이 총 얼마나 드나요?",
     "side": [{"field": {"k": "문의 구분", "v": "가맹 문의", "src": "통화에서"}}]},
    {"who": "ai", "text": "가맹 문의 감사합니다. 10평 기준으로 가맹비 1천만원, 교육비 3백만원, 인테리어는 평당 250만원이 기본이고, 주방 설비와 초도 물품은 별도예요. 정확한 금액은 상권과 점포 상태에 따라 달라져서, 정보공개서를 보내 드리고 상담을 잡아 드릴게요.",
     "side": [{"field": {"k": "기본 비용", "v": "가맹비 10,000,000원 · 교육비 3,000,000원 · 인테리어 평당 2,500,000원", "src": "대표님 요금표"}}]},
    {"who": "user", "text": "네, 보내 주세요. 지역은 대전이고, 예산은 1억 정도 생각하고 있어요.",
     "side": [{"field": {"k": "희망 지역 · 예산", "v": "대전 · 약 1억원", "src": "본인 발화"}}]},
    {"who": "ai", "text": "대전 지역 담당자에게 배정해 드릴게요. 성함과 연락처, 그리고 정보공개서 받으실 이메일 주소를 말씀해 주시겠어요?"},
    {"who": "user", "text": "강도현이고요, 010-9245-5817이에요. 이메일은 문자로 보내 드릴게요.",
     "side": [{"field": {"k": "이름", "v": "강도현", "src": "본인 발화"}}, {"field": {"k": "전화", "v": "010-9245-58··", "src": "발신번호와 일치"}}]},
    {"who": "ai", "text": "강도현 님, 대전 담당 서지훈 매니저에게 배정되었습니다. 이메일 주소가 오면 정보공개서를 오늘 중으로 보내 드리고, 담당자가 내일 오전에 연락드릴 거예요. 연락 받기 편한 시간이 있으세요?",
     "side": [{"crm": True},
              {"work": {"icon": "✓", "k": "담당자 배정", "v": "대전 담당 서지훈 · 가맹 파이프라인에 등록 · 확인 문자 발송"}}]},
    {"who": "user", "text": "오전 10시 이후가 좋아요.",
     "side": [{"field": {"k": "연락 희망", "v": "내일 10시 이후", "src": "본인 발화"}}]},
    {"who": "ai", "text": "네, 내일 오전 10시 이후로 남겨 두었어요. 정보공개서는 꼭 천천히 읽어 보시고, 궁금한 점은 상담 때 담당자에게 물어보시면 됩니다.",
     "side": [{"work": {"icon": "#", "k": "정보공개서 #0421", "v": "이메일 도착 즉시 발송 예약 — 대표님 규칙"}},
              {"work": {"icon": "@", "k": "담당 · 기한", "v": "서지훈 매니저 · 내일 10:00 이후 전화 · 상담 일정 제안"}},
              {"work": {"icon": "↻", "k": "후속 문자", "v": "정보공개서 미열람 시 D+2 안내 초안 — 발송 전 담당자 확인"}}]},
    {"who": "user", "text": "감사합니다."},
    {"who": "ai", "text": "감사합니다. 편안한 밤 되세요."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "어제 통화한 강도현입니다. 정보공개서 잘 받았어요. 상담은 본사에서 하나요?"},
    {"who": "ai", "when": "+2 sec", "text": "네 — 본사 상담실에서 진행하고, 화상 상담도 가능해요. 서지훈 매니저가 오늘 10시 이후에 연락드릴 예정입니다.", "merge": True},
    {"who": "user", "when": "7:42 AM", "text": "대전 둔산동이면 월 매출 어느 정도 나오나요?"},
    {"who": "ai", "when": "+2 sec", "text": "예상 매출은 가맹사업법상 제가 말씀드릴 수 없는 내용이에요. 정보공개서에 있는 자료를 기준으로 담당자가 설명드릴 수 있도록 대화 내용을 그대로 전달했고, 오전에 연락드리겠습니다.", "handoff": True}
   ],
   "handoff": HANDOFF_KO + ["멈춘 이유: 예상 매출은 근거 없이 제시할 수 없는 법적 사항이라 담당자가 정보공개서로 답합니다"],
   "morning": [
    {"icon": "✓", "k": "새 가맹 문의 1건", "v": "강도현 · 대전 · 10평 · 예산 약 1억원"},
    {"icon": "#", "k": "정보공개서 #0421", "v": "어제 21:40 이메일 발송 · 열람 확인"},
    {"icon": "@", "k": "담당", "v": "서지훈 매니저 · 오늘 10:00 이후 전화 · 상담 일정 제안"},
    {"icon": "!", "k": "답변 대기 1건", "v": "예상 매출 문의 · 대화 전체 첨부 · 담당 서지훈"}
   ],
   "person": {"when": "9:12 AM", "text": "대전 담당 서지훈입니다. 강도현 님, 매출은 정보공개서에 있는 지역별 평균 자료 범위 안에서만 설명드릴 수 있어요. 10시 반에 전화드려서 둔산동 상권 조사 절차부터 안내드릴게요."},
   "summary": "통화 {call} · 카카오톡 4건 · 사람이 한 일: 답장 한 줄. 나머지는 본사가 퇴근한 동안 끝났습니다.",
   "honest": HONEST_KO
  },
  "en": {
   "biz": "Moonlight Chicken head office", "owner": "head office",
   "meta": "Wednesday 9:07 PM · head office closed · a fictional franchisor", "callTime": "9:07 PM", "chan": "WhatsApp",
   "chapters": ["9:07 PM, the call", "Next morning, WhatsApp", "9:00 AM, the head office screen"],
   "chapterSubs": ["franchise enquiry · opening cost · manager assigned", "where the consultation is · expected revenue goes to a person", "lead · disclosure document · manager · one reply waiting"],
   "sys": {"ring": "9:07 PM — the main line rings. Head office closed at six.",
           "chat": "Next morning, 7:40 AM — the same candidate, on WhatsApp.",
           "morning": "9:00 AM — the head office screen."},
   "customer": {"name": "David Kang", "phone": "555-09··"},
   "lines": [
    {"who": "ai", "text": "Thanks for calling Moonlight Chicken head office. The office is closed for the day, but I can take franchise enquiries and store matters. How can I help?"},
    {"who": "user", "text": "I'm interested in a franchise. What does it cost in total to open one?",
     "side": [{"field": {"k": "Enquiry type", "v": "franchise candidate", "src": "from the call"}}]},
    {"who": "ai", "text": "Thank you for your interest. For a standard three hundred and fifty square foot store, the base figures are a thirty thousand dollar franchise fee, nine thousand for training, and fit-out at about seventy-five dollars a square foot, with kitchen equipment and opening stock on top. The exact total depends on the site, so I'll send you the disclosure document and set up a consultation.",
     "side": [{"field": {"k": "Base costs", "v": "franchise fee $30,000 · training $9,000 · fit-out ~$75 per sq ft", "src": "your published schedule"}}]},
    {"who": "user", "text": "Yes, please send it. I'm looking at Daejeon, with a budget of around three hundred thousand.",
     "side": [{"field": {"k": "Region · budget", "v": "Daejeon · about $300,000", "src": "caller said it"}}]},
    {"who": "ai", "text": "I'll assign you to the Daejeon regional manager. Can I get your name, a mobile number, and an email address for the disclosure document?"},
    {"who": "user", "text": "David Kang, five five five, zero nine one seven. I'll text you the email address.",
     "side": [{"field": {"k": "Name", "v": "David Kang", "src": "caller said it"}}, {"field": {"k": "Phone", "v": "555-09··", "src": "matches caller ID"}}]},
    {"who": "ai", "text": "Thank you, David. You're assigned to Jihoon Seo, our Daejeon manager. Once your email comes in, the disclosure document goes out tonight, and Jihoon will call you tomorrow morning. Is there a time that suits you?",
     "side": [{"crm": True},
              {"work": {"icon": "✓", "k": "Manager assigned", "v": "Jihoon Seo, Daejeon · added to the franchise pipeline · confirmation text sent"}}]},
    {"who": "user", "text": "After ten in the morning.",
     "side": [{"field": {"k": "Preferred time", "v": "tomorrow after 10 AM", "src": "caller said it"}}]},
    {"who": "ai", "text": "Noted, after ten tomorrow. Take your time with the disclosure document, and bring any questions to the consultation.",
     "side": [{"work": {"icon": "#", "k": "Disclosure document #0421", "v": "scheduled to send the moment the email arrives — your rule"}},
              {"work": {"icon": "@", "k": "Owner & due", "v": "Jihoon Seo · call after 10:00 tomorrow · propose a consultation"}},
              {"work": {"icon": "↻", "k": "Follow-up", "v": "D+2 nudge drafted if the document goes unopened — the manager approves before it sends"}}]},
    {"who": "user", "text": "Thanks."},
    {"who": "ai", "text": "Thank you. Have a good evening."}
   ],
   "chat": [
    {"who": "user", "when": "7:40 AM", "text": "Hi, David Kang from last night — got the disclosure document, thanks. Is the consultation at head office?"},
    {"who": "ai", "when": "+2 sec", "text": "Yes — in the consultation room at head office, or by video call if you prefer. Jihoon will call you after ten today.", "merge": True},
    {"who": "user", "when": "7:42 AM", "text": "If I open in Dunsan-dong in Daejeon, what monthly revenue could I expect?"},
    {"who": "ai", "when": "+2 sec", "text": "Expected revenue is something franchise law doesn't allow me to state. I've passed your question to Jihoon so he can walk you through the figures in the disclosure document — he'll call this morning.", "handoff": True}
   ],
   "handoff": HANDOFF_EN + ["Why it stopped: expected revenue is a legal line, not a fact I hold — the manager answers from the disclosure document"],
   "morning": [
    {"icon": "✓", "k": "New franchise lead", "v": "David Kang · Daejeon · 350 sq ft · budget about $300,000"},
    {"icon": "#", "k": "Disclosure document #0421", "v": "emailed 9:40 PM last night · opened"},
    {"icon": "@", "k": "Regional manager", "v": "Jihoon Seo · call after 10:00 today · propose a consultation"},
    {"icon": "!", "k": "Waiting for a person", "v": "expected revenue question · full thread attached · owner: Jihoon"}
   ],
   "person": {"when": "9:12 AM", "text": "This is Jihoon, Daejeon regional manager. Hi David — I can only discuss revenue within the regional averages in the disclosure document. I'll call at ten thirty and start with how a site survey for Dunsan-dong works."},
   "summary": "One {call} call · four messages · what a person did: one reply. The rest happened while head office was closed.",
   "honest": HONEST_EN
  }
 }
}
