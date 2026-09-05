# -*- coding: utf-8 -*-
"""열 개 업종 추가 — 예약으로 도는 곳 넷, 집과 건물 여섯.

앞의 스물다섯과 형식은 같고 문장은 하나도 겹치지 않는다. 각 항목의 'en' 에는
영어 페이지와 영어 업종 벽(room)에 쓰는 같은 이야기가 미국 기준으로 다시 쓰여 있다.
사진은 아직 고르지 않았다 — ph('PENDING').

  · 도장은 승급을, 네일은 손발톱 상태를, 반려동물 미용은 아이의 건강을 말하지 않는다.
  · 청소·인테리어·조경·가전 수리는 보지 않은 일에 최종 금액을 말하지 않는다.
  · 열쇠는 본인 확인을 전화로 끝내지 않고, 안에 사람이 갇혀 있으면 119 다음에 사람이다.
  · 세탁소는 얼룩이 빠진다고 약속하지 않는다.
"""

PH = 'https://images.pexels.com/photos/%s/pexels-photo-%s.jpeg'


def ph(i):
    return PH % (i, i)


TRADES4 = [
{
 'slug': 'martial-arts', 'owner': '관장님', 'name': '태권도·무술 도장', 'photo': ph('PENDING'),
 'when': {'eyebrow': '저녁 수업 중의 통화', 'h2': '매트 위에 서 있는 동안<br>이렇게 흘러갑니다.', 'tt': '저녁 수업 중', 'badge': '매트에서 내려올 수 없는 시간'},
 'kicker': '태권도 &middot; 합기도 &middot; 주짓수 도장',
 'h1': '학부모 전화는<br>수업 중에 옵니다.',
 'sub': '저녁 일곱 시 반, 관장님은 아이 스무 명 앞에 서 있습니다. '
        '그 시간에 다른 아이의 부모가 처음으로 전화를 겁니다.',
 'cost': '도장 문의는 새 학기와 여름방학 앞에 몰리고, 대부분 &ldquo;일곱 살인데 언제 갈 수 있나요&rdquo;로 시작합니다. '
         '체험 한 번이 등록이 되고, 등록 한 명이 형제와 친구로 이어집니다. '
         '그런데 그 전화가 오는 시간은 정확히 관장님이 구령을 붙이고 있는 시간이고, 수업이 끝나 콜백할 때면 '
         '옆 도장 체험이 이미 잡혀 있습니다.',
 'call': [('학부모', '7:52 PM', '일곱 살 아이인데 처음 시작하려고요. 몇 시 반이 있고 관비는 얼마인가요?'),
          ('Saleringo', '+23초', '일곱 살이면 <b>유치·초등 저학년반</b>이고, 평일 <b>오후 4시</b>와 <b>5시</b>에 있습니다. '
                                 '관비는 <b>월 13만원</b>, 도복은 <b>4만원</b>이고 첫 체험은 무료입니다. '
                                 '이번 주 목요일 5시 체험 자리가 있습니다.'),
          ('학부모', '7:54 PM', '목요일 5시로 할게요. 차량은 오나요?'),
          ('Saleringo', '+9초', '목요일 5시 체험으로 잡았습니다. 차량은 등록 후 노선을 확인해 안내드리고, '
                                '체험 날은 편한 옷으로 오시면 됩니다. 아이 이름과 연락처만 남겨 주세요.')],
 'refuse': [('승급이나 심사 결과를 약속하지 않습니다.',
             '&ldquo;6개월이면 노란띠&rdquo; 같은 말을 하지 않습니다. 심사는 관장님이 아이를 보고 정합니다.'),
            ('아이가 맞는지 판단하지 않습니다.',
             '산만한 아이도 되는지, 몸이 약한데 괜찮은지는 체험 수업에서 관장님이 보고 답할 일입니다.'),
            ('다친 아이 이야기는 바로 사람에게 넘깁니다.',
             '수업 중 다쳤다는 전화가 오면 안내 대신 즉시 관장님 번호로 연결합니다.'),
            ('관비를 깎거나 다른 원생 이야기를 하지 않습니다.',
             '등록된 관비와 형제 할인만 말하고, 같은 반에 누가 다니는지는 답하지 않습니다.')],
 'fields': ['아이 나이와 학년', '희망 반과 요일', '체험 수업 예약 시간',
            '안내한 관비와 도복비', '차량 운행 필요 여부', '학부모 연락 가능 시간'],
 'stages': ['문의 접수', '체험 예약', '체험 수업', '등록', '승급 심사 안내'],
 'lead': '관장님이 구령을 붙이는 시간에 오는 학부모 전화. 승급을 약속하지 않고, 체험 수업만 잡습니다.',
 'group': 1,
 'en': {
  'name': 'Martial arts dojos', 'owner': 'the head instructor',
  'kicker': 'Taekwondo &middot; karate &middot; BJJ academies',
  'h1': 'Parents call<br>while class is running.',
  'sub': 'At 7:30 PM the head instructor is on the mat in front of twenty kids. '
         'That is exactly when another child’s parent calls for the first time.',
  'cost': 'Dojo inquiries cluster before the school year and before summer break, and almost every one opens with '
          '&ldquo;he’s seven — when can he start?&rdquo; One trial class becomes an enrolment, and one enrolment brings '
          'a sibling and a friend. But the call lands while you are counting kicks, and by the time class ends and you '
          'call back, the trial is already booked at the academy across the road.',
  'call': [('Parent', '7:52 PM', 'My son is seven and has never done this. What times do you have, and what does it cost?'),
           ('Saleringo', '+23 s', 'At seven he’d be in our <b>Little Tigers</b> class, weekdays at <b>4:00</b> and <b>5:00 PM</b>. '
                                  'Tuition is <b>$129 a month</b>, the uniform is <b>$45</b>, and the first trial class is free. '
                                  'Thursday at five has a trial spot open.'),
           ('Parent', '7:54 PM', 'Thursday at five works. Do you do school pick-up?'),
           ('Saleringo', '+9 s', 'You’re set for Thursday at five. Pick-up routes are confirmed after enrolment, so I’ll '
                                 'note the question for the instructor. Comfortable clothes are fine for the trial — may I '
                                 'have your child’s name and a number for you?')],
  'refuse': [('It never promises a belt or a test result.',
              'No &ldquo;yellow belt in six months.&rdquo; Promotion is the instructor’s call, made on the mat.'),
             ('It never decides whether a child is a fit.',
              'Whether an easily distracted or physically slight child will do well is answered at the trial, by a person who has watched them.'),
             ('An injured child goes to a person at once.',
              'A call about a child hurt in class gets no script — it rings the head instructor directly.'),
             ('It never discounts tuition or discusses other students.',
              'Only the published tuition and sibling rate are quoted, and who else is in the class is never answered.')],
  'fields': ['Child’s age and grade', 'Class and days asked about', 'Trial class booked',
             'Tuition and uniform quoted', 'School pick-up needed', 'Best time to reach the parent'],
  'stages': ['Inquiry', 'Trial booked', 'Trial class', 'Enrolled', 'Belt test scheduled'],
  'when': {'eyebrow': 'The call during evening class', 'h2': 'While you are on the mat,<br>this is how it goes.', 'tt': 'evening class', 'badge': 'Cannot step off the mat'},
  'lead': 'The parent who calls while you are counting kicks. No belt promised — just a trial class on the calendar.',
  'room': 'booked-by-appointment',
  'room_d': 'The 7:52 PM parent call answered mid-class: age, class time and tuition from your own sheet, a trial booked — and no belt or test result ever promised.',
  'room_no': ('0', 'belts or test results the AI is allowed to promise'),
 },
},
{
 'slug': 'nail-spa', 'owner': '원장님', 'name': '네일·스파', 'photo': ph('PENDING'),
 'when': {'eyebrow': '젤 굳히는 동안의 통화', 'h2': '두 손이 손님 손 위에 있는 동안<br>이렇게 흘러갑니다.', 'tt': '토요일 오후', 'badge': '손을 놓을 수 없는 시간'},
 'kicker': '네일 &middot; 페디 &middot; 스파',
 'h1': '두 손이 손님 손 위에 있을 때<br>전화가 웁니다.',
 'sub': '젤을 올리는 중에는 전화기를 잡을 수 없습니다. '
        '토요일 오후에 오는 예약 문의는 그래서 대부분 부재중이 됩니다.',
 'cost': '네일 손님은 3주마다 돌아오는 손님입니다. 첫 예약 한 통을 놓치면 그 3주짜리 주기가 통째로 옆 샵에 갑니다. '
         '문의는 &ldquo;오늘 저녁 되나요, 타샵 제거도 되나요&rdquo; 두 문장이면 끝나는데, '
         '그 두 문장에 답할 사람이 램프 앞에서 손님 손을 잡고 있습니다.',
 'call': [('손님', '1:05 PM', '오늘 저녁에 젤 제거하고 새로 하고 싶은데요. 다른 샵에서 한 거예요. 얼마 나와요?'),
          ('Saleringo', '+21초', '젤 네일은 <b>5만 5천원</b>이고, 타샵 제거는 <b>1만 5천원</b>이 추가됩니다. '
                                 '제거까지 하면 <b>1시간 반</b> 정도 잡으시면 되고, 오늘은 <b>저녁 6시 30분</b>이 비어 있습니다.'),
          ('손님', '1:06 PM', '6시 반으로 해 주세요. 페디도 같이 될까요?'),
          ('Saleringo', '+10초', '페디큐어는 <b>6만원</b>이고 함께 하시면 2시간 반으로 잡겠습니다. '
                                 '6시 30분에 두 자리로 예약했습니다. 성함과 연락처 남겨 주시면 확인 문자 보내 드릴게요.')],
 'refuse': [('손발톱 상태를 진단하지 않습니다.',
             '변색이나 통증, 들뜸이 무엇 때문인지 말하지 않습니다. 감염이 의심되는 설명이면 시술 대신 병원부터 안내하고 원장님에게 남깁니다.'),
            ('사진만 보고 디자인을 확정하지 않습니다.',
             '원하는 아트가 가능한지, 얼마가 나올지는 손톱 길이와 상태를 보고 원장님이 정합니다.'),
            ('시술 시간을 줄여 잡지 않습니다.',
             '제거와 아트가 붙으면 넉넉하게 잡습니다. 다음 손님을 기다리게 하는 것이 가장 비싼 실수입니다.'),
            ('메뉴에 없는 금액을 만들지 않습니다.',
             '등록된 메뉴판만 읽습니다. 없는 시술은 확인 후 연락드린다고 남깁니다.')],
 'fields': ['요청 시술과 예상 소요 시간', '타샵 제거 여부', '예약 시간과 담당',
            '메뉴판 기준 안내 금액', '첫 방문 · 재방문 구분', '확인 문자 발송 기록'],
 'stages': ['문의 접수', '예약 확정', '전날 확인', '방문 · 시술', '3주 뒤 리터치 안내'],
 'lead': '램프 앞에서 손님 손을 잡고 있을 때 오는 전화. 손발톱 상태는 말하지 않고, 제거 시간까지 넣어 예약을 잡습니다.',
 'group': 1,
 'en': {
  'name': 'Nail & spa', 'owner': 'the owner',
  'kicker': 'Nail salons &middot; pedicure &middot; day spa',
  'h1': 'The phone rings<br>while both hands are on a client.',
  'sub': 'Mid-gel, nobody can pick up a phone. '
         'Saturday-afternoon booking calls go to voicemail for exactly that reason.',
  'cost': 'A nail client comes back every three weeks. Miss her first call and that whole three-week cycle walks to '
          'the salon next door. The inquiry is two sentences — &ldquo;anything tonight, and can you remove another '
          'salon’s gel?&rdquo; — and the only person who can answer is under the lamp holding someone’s hand.',
  'call': [('Customer', '1:05 PM', 'Can I get a gel removal and a new set this evening? Another place did it. What would that run?'),
           ('Saleringo', '+21 s', 'A gel manicure is <b>$55</b>, and removal of another salon’s gel adds <b>$12</b>. '
                                  'With the soak-off, plan on about <b>an hour and a half</b>. Tonight I have <b>6:30 PM</b> open.'),
           ('Customer', '1:06 PM', 'Six thirty, please. Could I add a pedicure?'),
           ('Saleringo', '+10 s', 'A pedicure is <b>$65</b>, and together I’ll block two and a half hours. You’re booked '
                                  'at 6:30 for both. May I have your name and a mobile number for the confirmation text?')],
  'refuse': [('It never diagnoses a nail or skin condition.',
              'Why a nail is discoloured, sore or lifting is not answered. A description that sounds like infection gets a doctor suggested, not a booking, and the owner is told.'),
             ('It never confirms a design from a photo.',
              'Whether the art is possible and what it costs is settled by the owner, looking at the actual nail length and condition.'),
             ('It never books a shorter slot than the work needs.',
              'Removal plus art gets the long block. Making the next client wait is the most expensive mistake in the room.'),
             ('It never invents a price that is not on the menu.',
              'Only your service menu is read. Anything else is logged as &ldquo;we’ll confirm and call back.&rdquo;')],
  'fields': ['Service requested and time needed', 'Removal of another salon’s gel', 'Slot and technician',
             'Price quoted from your menu', 'First visit or returning', 'Confirmation text sent'],
  'stages': ['Inquiry', 'Booked', 'Day-before reminder', 'Visit', 'Three-week refill reminder'],
  'when': {'eyebrow': 'The call while the gel cures', 'h2': 'While both hands are on a client,<br>this is how it goes.', 'tt': 'Saturday afternoon', 'badge': 'Cannot let go of the hand'},
  'lead': 'The call that comes while you are under the lamp. No nail condition assessed — soak-off time added, the slot booked.',
  'room': 'booked-by-appointment',
  'room_d': 'The Saturday 1:05 PM call for a soak-off and a new set: the menu price quoted, the long slot held for tonight — and a sore or discoloured nail sent to a doctor, never assessed.',
  'room_no': ('0', 'nail or skin conditions the AI is allowed to diagnose'),
 },
},
{
 'slug': 'barbershop', 'owner': '사장님', 'name': '이발소·바버샵', 'photo': ph('PENDING'),
 'when': {'eyebrow': '퇴근 시간 피크의 통화', 'h2': '가위를 든 동안<br>이렇게 흘러갑니다.', 'tt': '저녁 피크', 'badge': '의자가 비지 않는 시간'},
 'kicker': '바버샵 &middot; 이발소 &middot; 남성 전문',
 'h1': '가위를 든 손으로는<br>전화를 받지 못합니다.',
 'sub': '저녁 여섯 시부터 여덟 시, 의자는 비지 않고 대기 의자에도 두 명이 앉아 있습니다. '
        '내일 아침 출근 전에 자르고 싶은 사람이 지금 전화를 겁니다.',
 'cost': '바버샵 손님은 4주에 한 번 옵니다. 한 번 잡은 단골이 1년이면 열두 번이고, 그 열두 번이 첫 통화 한 번에 달려 있습니다. '
         '문의는 &ldquo;내일 아침 몇 시에 되나요&rdquo;가 전부인데, 그 시간에 사장님 손에는 가위가, 손님 머리에는 클리퍼가 있습니다. '
         '워크인만 받는 곳도 마찬가지입니다 &mdash; 대기가 얼마인지 답할 사람이 없으면 손님은 옆 골목으로 갑니다.',
 'call': [('손님', '6:40 PM', '내일 아침 출근 전에 커트랑 수염 정리 되나요? 얼마예요?'),
          ('Saleringo', '+18초', '커트는 <b>2만 5천원</b>, 커트와 면도를 같이 하시면 <b>4만원</b>입니다. '
                                 '내일 아침은 <b>8시</b>와 <b>8시 40분</b>이 비어 있고, 둘 다 하시면 40분 잡습니다.'),
          ('손님', '6:41 PM', '8시로요. 지난번에 해 주신 분으로 가능할까요?'),
          ('Saleringo', '+8초', '지정 요청으로 남겨 두겠습니다. 어느 분이었는지는 사장님이 예약 명단을 보고 확인해 배정합니다. '
                                '내일 8시로 잡았고, 성함과 연락처를 남겨 주시면 아침에 알림을 보내 드리겠습니다.')],
 'refuse': [('두피나 탈모를 판단하지 않습니다.',
             '머리가 빠진다, 두피가 가렵다는 말에 원인이나 제품을 말하지 않습니다. 피부과와 사장님 상담으로 넘깁니다.'),
            ('이발사를 임의로 배정하지 않습니다.',
             '&ldquo;지난번 그분&rdquo;이 누구인지 기계는 추측하지 않습니다. 요청으로 남기고 사장님이 정합니다.'),
            ('워크인 대기 시간을 단정하지 않습니다.',
             '&ldquo;10분이면 됩니다&rdquo;라고 말하지 않습니다. 예약을 잡거나, 현재 대기가 몇 명인지 등록된 현황만 읽습니다.'),
            ('요금표에 없는 서비스 금액을 만들지 않습니다.',
             '펌이나 염색처럼 등록되지 않은 항목은 확인 후 연락드린다고 남깁니다.')],
 'fields': ['요청 서비스와 소요 시간', '지정 이발사 요청', '예약 시간',
            '요금표 기준 안내 금액', '워크인 · 예약 구분', '당일 알림 발송 기록'],
 'stages': ['문의 접수', '예약 확정', '당일 알림', '방문 · 커트', '4주 뒤 재방문 안내'],
 'lead': '가위를 들고 있는 저녁에 오는 내일 아침 예약. 대기 시간을 지어내지 않고, 빈 시간에 그대로 잡습니다.',
 'group': 1,
 'en': {
  'name': 'Barbershops', 'owner': 'the owner',
  'kicker': 'Barbershops &middot; men’s grooming',
  'h1': 'You cannot answer a phone<br>with shears in your hand.',
  'sub': 'Six to eight in the evening, no chair is empty and two people are waiting. '
         'The man who wants a cut before work tomorrow is calling right now.',
  'cost': 'A barbershop client comes every four weeks. Win him once and that is twelve visits a year, all riding on '
          'the first call. The question is only &ldquo;what have you got tomorrow morning?&rdquo; — and at that moment '
          'you have shears in one hand and clippers on somebody’s neck. Walk-in shops lose the same way: if nobody can '
          'say how long the wait is, he walks to the next block.',
  'call': [('Customer', '6:40 PM', 'Can I get a cut and a beard trim before work tomorrow? What do you charge?'),
           ('Saleringo', '+18 s', 'A haircut is <b>$35</b>, and a cut with a beard trim is <b>$55</b>. '
                                  'Tomorrow morning I have <b>8:00</b> and <b>8:40</b>, and I’d block forty minutes for both.'),
           ('Customer', '6:41 PM', 'Eight, please. Could I get the same barber as last time?'),
           ('Saleringo', '+8 s', 'I’ll note that as a request. The owner checks the booking list to see who cut you last '
                                 'and assigns the chair. You’re down for eight tomorrow — your name and a mobile number, and I’ll text a reminder in the morning.')],
  'refuse': [('It never judges scalp problems or hair loss.',
              '&ldquo;My hair is thinning&rdquo; or &ldquo;my scalp itches&rdquo; gets no cause and no product — it gets a dermatologist and a note for the owner.'),
             ('It never guesses which barber someone means.',
              '&ldquo;The guy from last time&rdquo; is logged as a request, not resolved by a machine. The owner assigns the chair.'),
             ('It never states a walk-in wait time it cannot see.',
              'No &ldquo;ten minutes, tops.&rdquo; It books a slot, or reads the live wait count you keep — nothing else.'),
             ('It never prices a service that is not on your list.',
              'Perms, colour or anything unlisted is logged as &ldquo;we’ll confirm and call back.&rdquo;')],
  'fields': ['Service and time needed', 'Barber requested', 'Slot booked',
             'Price quoted from your list', 'Walk-in or appointment', 'Same-day reminder sent'],
  'stages': ['Inquiry', 'Booked', 'Same-day reminder', 'In the chair', 'Four-week rebook'],
  'when': {'eyebrow': 'The call at the evening rush', 'h2': 'While the shears are in your hand,<br>this is how it goes.', 'tt': 'evening rush', 'badge': 'No chair is empty'},
  'lead': 'Tomorrow-morning bookings that call during tonight’s rush. No wait time invented — the open slot booked as it is.',
  'room': 'booked-by-appointment',
  'room_d': 'The 6:40 PM call for a cut before work: your price quoted, the 8:00 chair booked, the barber request logged for you — and no wait time stated that the AI cannot see.',
  'room_no': ('0', 'walk-in wait times the AI is allowed to guess'),
 },
},
{
 'slug': 'pet-grooming', 'owner': '사장님', 'name': '반려동물 미용·호텔', 'photo': ph('PENDING'),
 'when': {'eyebrow': '드라이 중의 통화', 'h2': '젖은 아이를 안고 있는 동안<br>이렇게 흘러갑니다.', 'tt': '미용 중', 'badge': '드라이기를 끌 수 없는 시간'},
 'kicker': '반려동물 미용 &middot; 호텔 &middot; 유치원',
 'h1': '젖은 강아지를 안고 있으면<br>전화를 받을 수 없습니다.',
 'sub': '드라이기 소리 속에서 전화벨은 들리지도 않습니다. '
        '연휴 앞 호텔 문의는 정확히 그 시간에 옵니다.',
 'cost': '미용은 6주마다, 호텔은 연휴마다 돌아오는 손님입니다. 명절 앞 열흘 동안 놓친 전화 한 통은 '
         '그 연휴의 호텔 예약 하나가 아니라, 그 집 강아지가 앞으로 다닐 곳이 정해지는 일입니다. '
         '그런데 미용사 손에는 가위와 드라이기가 있고, 그 손을 놓는 순간 테이블 위의 아이가 위험합니다.',
 'call': [('보호자', '3:10 PM', '다음 주 연휴에 2박 호텔 되나요? 들어가기 전에 미용도 같이 하고 싶어요. 5킬로 말티즈예요.'),
          ('Saleringo', '+24초', '연휴에 <b>소형견 자리 2개</b>가 남아 있습니다. 호텔은 <b>1박 3만 5천원</b>, '
                                 '목욕과 위생미용은 <b>5만원</b>, 전체미용은 털 상태에 따라 <b>7만원부터</b>입니다. '
                                 '호텔 입실에는 <b>종합백신과 켄넬코프 접종 증명</b>이 필요합니다.'),
          ('보호자', '3:12 PM', '접종은 다 했어요. 그럼 그날 아침에 맡길게요.'),
          ('Saleringo', '+9초', '연휴 첫날 오전 입실, 2박, 입실 전 목욕과 위생미용으로 잡아 두었습니다. '
                                '접종 증명 사진을 문자로 보내 주시면 확정되고, 사료와 평소 먹는 약이 있으면 함께 챙겨 주세요. '
                                '보호자 성함과 아이 이름을 남겨 주시겠어요?')],
 'refuse': [('아이의 건강에 관해 답하지 않습니다.',
             '피부가 빨갛다, 설사를 한다, 다리를 전다는 말에 원인이나 처치를 말하지 않습니다. 동물병원을 안내하고 사장님에게 남깁니다.'),
            ('접종 증명 없이 호텔을 확정하지 않습니다.',
             '&ldquo;다 맞았어요&rdquo;는 접수만 됩니다. 증명이 도착해야 확정으로 바뀝니다. 다른 아이들을 지키는 규칙입니다.'),
            ('사진만 보고 미용 결과를 약속하지 않습니다.',
             '엉킴이 심하면 원하는 스타일이 안 나올 수 있습니다. 털 상태는 보고 미용사가 정합니다.'),
            ('아이가 위험한 상황이면 즉시 사람에게 넘깁니다.',
             '호흡이 이상하다, 축 늘어졌다는 말이 나오면 예약이 아니라 24시 동물병원 안내와 사장님 연결입니다.')],
 'fields': ['반려동물 종 · 체중 · 나이', '요청 미용과 호텔 날짜', '접종 증명 확인 여부',
            '요금표 기준 안내 금액', '특이사항(엉킴 · 공격성 · 복용 약)', '확정 문자 발송 기록'],
 'stages': ['문의 접수', '접종 확인', '예약 확정', '입실 · 미용', '재방문 안내'],
 'lead': '드라이기 소리 속에서 놓치는 연휴 호텔 문의. 아이 건강은 말하지 않고, 접종 증명이 와야 확정합니다.',
 'group': 1,
 'en': {
  'name': 'Pet grooming & boarding', 'owner': 'the owner',
  'kicker': 'Groomers &middot; boarding &middot; daycare',
  'h1': 'You cannot take a call<br>holding a wet dog.',
  'sub': 'Over a dryer you do not even hear the phone ring. '
         'Holiday boarding inquiries arrive at exactly that moment.',
  'cost': 'Grooming comes back every six weeks and boarding every holiday. One missed call in the ten days before '
          'Thanksgiving is not one lost booking — it decides where that dog goes for years. But the groomer has shears '
          'in one hand and a dryer in the other, and the moment she lets go, the dog on the table is at risk.',
  'call': [('Customer', '3:10 PM', 'Do you have boarding over the holiday weekend, two nights? I’d like a groom before she goes in. She’s an eleven-pound Maltese.'),
           ('Saleringo', '+24 s', 'I have <b>two small-dog spots</b> left that weekend. Boarding is <b>$45 a night</b>, a bath '
                                  'with a tidy is <b>$65</b>, and a full groom starts at <b>$90</b> depending on coat condition. '
                                  'Boarding requires <b>proof of rabies, DHPP and Bordetella</b> vaccination.'),
           ('Customer', '3:12 PM', 'She’s up to date on all of it. I’ll drop her off that morning.'),
           ('Saleringo', '+9 s', 'I’ve held Friday morning check-in, two nights, with a bath and tidy before she goes in. '
                                 'Text me a photo of the vaccination record and the hold becomes a confirmed booking. Please pack her food and any '
                                 'medication she takes. May I have your name and hers?')],
  'refuse': [('It never answers a question about the animal’s health.',
              'Red skin, diarrhoea, a limp — no cause and no remedy. It points to a vet and leaves a note for the owner.'),
             ('It never confirms boarding without vaccination proof.',
              '&ldquo;She’s had everything&rdquo; creates a hold, not a booking. The record has to arrive first. That rule protects every other dog in the building.'),
             ('It never promises a groom result from a photo.',
              'A matted coat may not take the style the client wants. The groomer decides with the dog on the table.'),
             ('An animal in distress goes straight to a person.',
              'Laboured breathing or a collapsed dog gets the 24-hour emergency vet and the owner’s phone, not a booking.')],
  'fields': ['Breed, weight and age', 'Groom requested and boarding dates', 'Vaccination proof received',
             'Price quoted from your list', 'Notes (matting · temperament · medication)', 'Confirmation text sent'],
  'stages': ['Inquiry', 'Vaccines verified', 'Booked', 'Check-in & groom', 'Rebook reminder'],
  'when': {'eyebrow': 'The call over the dryer', 'h2': 'While you are holding a wet dog,<br>this is how it goes.', 'tt': 'mid-groom', 'badge': 'Cannot switch the dryer off'},
  'lead': 'Holiday boarding inquiries lost under the dryer. No health advice given — and nothing confirmed until the vaccination record arrives.',
  'room': 'booked-by-appointment',
  'room_d': 'The 3:10 PM holiday-boarding call answered over the dryer: rates from your own list, the spot held — confirmed only when the vaccination record arrives, and never a word of advice about the animal’s health.',
  'room_no': ('0', 'boardings confirmed without vaccination proof'),
 },
},
{
 'slug': 'cleaning-services', 'owner': '대표님', 'name': '청소 서비스', 'photo': ph('PENDING'),
 'when': {'eyebrow': '현장에 나가 있는 동안의 통화', 'h2': '팀이 남의 집에 들어가 있는 동안<br>이렇게 흘러갑니다.', 'tt': '현장 작업 중', 'badge': '사무실이 비는 시간'},
 'kicker': '입주청소 &middot; 이사청소 &middot; 정기 가사',
 'h1': '견적 전화는<br>팀이 현장에 들어가 있을 때 옵니다.',
 'sub': '오전 아홉 시부터 오후 다섯 시까지 대표님은 장갑을 끼고 있습니다. '
        '입주 날짜가 잡힌 사람이 그 시간에 세 군데에 전화를 돌립니다.',
 'cost': '입주청소 문의는 잔금일이 정해진 사람이 겁니다. 날짜가 급하니 답이 오는 순서대로 계약하고, '
         '한 집을 놓치면 그 집이 소개할 아파트 단지의 이웃도 함께 놓칩니다. '
         '그런데 &ldquo;32평 얼마예요&rdquo;에 답할 사람은 지금 다른 집 화장실 타일 줄눈을 닦고 있고, '
         '저녁에 콜백하면 이미 다른 업체의 입금이 끝나 있습니다.',
 'call': [('손님', '11:20 AM', '다음 주 토요일에 32평 입주청소 되나요? 얼마 정도 나와요?'),
          ('Saleringo', '+25초', '32평 입주청소는 빈집 기준 <b>45만원에서 52만원</b> 사이이고, 정확한 금액은 '
                                 '짐 유무와 오염 상태를 사진이나 방문으로 확인한 뒤 확정됩니다. '
                                 '다음 주 토요일은 <b>오전 팀</b>이 비어 있고, 32평이면 <b>3명이 5시간</b> 정도 봅니다.'),
          ('손님', '11:22 AM', '토요일 오전으로 잡아 주세요. 새 아파트라 짐은 없어요.'),
          ('Saleringo', '+9초', '토요일 오전, 빈집 32평으로 잡아 두었습니다. 주소와 출입 방법을 문자로 보내 주시면 '
                                '대표님이 확인하고 확정 금액을 오늘 중에 알려 드립니다. 성함과 연락처를 남겨 주시겠어요?')],
 'refuse': [('보지 않은 집의 금액을 확정하지 않습니다.',
             '평수만 듣고 최종 금액을 말하지 않습니다. 범위까지만 말하고, 확정은 사진이나 방문 후 대표님이 합니다.'),
            ('곰팡이와 찌든 때가 다 지워진다고 말하지 않습니다.',
             '실리콘 곰팡이, 오래된 기름때는 청소로 안 지워지는 경우가 있습니다. 보고 판단할 일이라고 답합니다.'),
            ('끝나는 시각을 약속하지 않습니다.',
             '오염 상태에 따라 한두 시간이 늘어납니다. &ldquo;3시까지 끝납니다&rdquo;는 대표님만 말할 수 있습니다.'),
            ('가스 냄새나 누수 이야기는 바로 사람에게 넘깁니다.',
             '청소 중이든 문의 중이든 가스 냄새, 물이 새는 소리가 나오면 안내 문구를 읽고 즉시 연결합니다.')],
 'fields': ['주소와 평수 · 구조', '청소 종류(입주 · 이사 · 정기)', '희망 일자와 시간대',
            '요금표 기준 안내 범위', '짐 유무 · 주차 · 출입 방법', '확정 금액 안내 기록'],
 'stages': ['문의 접수', '견적 확정', '일정 확정', '작업', '정기 이용 제안'],
 'lead': '잔금일이 정해진 사람이 낮에 거는 전화. 보지 않은 집의 금액을 확정하지 않고, 범위와 팀 일정만 잡습니다.',
 'group': 2,
 'en': {
  'name': 'Cleaning services', 'owner': 'the owner',
  'kicker': 'Move-out cleans &middot; deep cleans &middot; recurring',
  'h1': 'Quote calls come<br>while the crew is inside a house.',
  'sub': 'From nine to five the owner is wearing gloves. '
         'Someone with a closing date is calling three companies in that window.',
  'cost': 'Move-out inquiries come from people with a date already fixed. They hire in the order the answers arrive, '
          'and losing one house loses the neighbours it would have referred. But the person who can price a '
          'three-bedroom is scrubbing grout in somebody else’s bathroom, and by the evening call-back another company '
          'has the deposit.',
  'call': [('Customer', '11:20 AM', 'Can you do a move-out clean next Saturday? It’s a three-bedroom, about eleven hundred square feet. Roughly what would it cost?'),
           ('Saleringo', '+25 s', 'An empty three-bedroom move-out runs <b>$380 to $480</b>, and the exact figure is confirmed once we’ve '
                                  'seen photos or the place itself — furniture and condition change it. Next Saturday the <b>morning crew</b> '
                                  'is open, and that size usually takes <b>three people about five hours</b>.'),
           ('Customer', '11:22 AM', 'Saturday morning, please. It’s a new build, completely empty.'),
           ('Saleringo', '+9 s', 'I’ve held Saturday morning for an empty three-bedroom. Text me the address and how the crew gets in, '
                                 'and the owner will confirm the final price today. May I have your name and a mobile number?')],
  'refuse': [('It never fixes a price on a house nobody has seen.',
              'Square footage alone gets a range, not a number. The final figure is the owner’s, after photos or a visit.'),
             ('It never promises that mould or grime will come out.',
              'Silicone mould and old grease sometimes do not clean off. That is answered by someone looking at it.'),
             ('It never promises a finish time.',
              'Condition adds an hour or two. &ldquo;Done by three&rdquo; is something only the owner can say.'),
             ('A gas smell or a leak goes to a person immediately.',
              'Whether it comes up during a job or during a call, the safety line is read and a human is connected.')],
  'fields': ['Address, size and layout', 'Type of clean (move-out · deep · recurring)', 'Date and time window wanted',
             'Range quoted from your price list', 'Furniture · parking · access', 'Final price confirmed'],
  'stages': ['Inquiry', 'Quote confirmed', 'Scheduled', 'Job done', 'Recurring offer'],
  'when': {'eyebrow': 'The call while the crew is out', 'h2': 'While your team is inside someone’s home,<br>this is how it goes.', 'tt': 'crew on site', 'badge': 'Nobody in the office'},
  'lead': 'The daytime call from someone with a closing date. No price fixed on a house nobody has seen — a range and a crew slot instead.',
  'room': 'home-property',
  'room_d': 'The 11:20 AM move-out call: a range from your own list, the Saturday crew held, the address requested for a real quote — and no final price on a house nobody has seen.',
  'room_no': ('0', 'prices fixed on a home nobody has seen'),
 },
},
{
 'slug': 'interior-renovation', 'owner': '대표님', 'name': '인테리어·리모델링', 'photo': ph('PENDING'),
 'when': {'eyebrow': '현장 소음 속의 통화', 'h2': '타일 자르는 소리 옆에서<br>이렇게 흘러갑니다.', 'tt': '시공 현장', 'badge': '전화 소리가 들리지 않는 시간'},
 'kicker': '인테리어 &middot; 리모델링 &middot; 욕실 · 주방 시공',
 'h1': '그라인더 소리 옆에서는<br>전화가 울려도 모릅니다.',
 'sub': '시공 중인 현장에서 대표님은 하루를 보냅니다. '
        '그 사이 걸려 온 &ldquo;욕실 하나 얼마예요&rdquo;는 부재중 목록에 번호로만 남습니다.',
 'cost': '리모델링 문의 한 통은 수백만 원에서 수천만 원짜리 공사입니다. 그런데 문의하는 사람은 세 군데에 동시에 걸고, '
         '먼저 실측 날짜를 잡아 주는 곳과 계약합니다. 대표님이 현장에 있는 낮 시간이 정확히 그 전화가 오는 시간이고, '
         '저녁에 콜백하면 이미 다른 업체가 다녀간 뒤입니다.',
 'call': [('손님', '2:35 PM', '욕실 하나 전체 리모델링하면 얼마 정도 들어요? 기간은요?'),
          ('Saleringo', '+27초', '욕실 전체 리모델링은 자재 등급과 크기에 따라 <b>350만원에서 600만원</b> 사이이고, '
                                 '정확한 금액은 실측을 해야 나옵니다. 공사는 보통 <b>4일에서 6일</b>인데, 배관 위치를 옮기면 더 걸립니다. '
                                 '실측은 무료이고 <b>목요일 오후 2시</b>나 <b>토요일 오전 10시</b>에 가능합니다.'),
          ('손님', '2:37 PM', '토요일 10시에 와 주세요. 아파트고 지금 살고 있는 집이에요.'),
          ('Saleringo', '+10초', '토요일 오전 10시 실측으로 잡았습니다. 거주 중이시면 공사 기간 동안 욕실 사용 계획도 그날 같이 상의하시면 됩니다. '
                                 '주소와 아파트 평형, 참고하실 사진이 있으면 문자로 보내 주세요. 성함과 연락처도 함께 부탁드립니다.')],
 'refuse': [('실측 없이 견적을 확정하지 않습니다.',
             '평형과 사진만으로 최종 금액을 말하지 않습니다. 범위까지만 말하고, 견적은 실측 후 대표님이 냅니다.'),
            ('준공일을 약속하지 않습니다.',
             '자재 수급과 관리사무소 승인, 철거 후 드러나는 상태에 따라 달라집니다. 기간은 &ldquo;보통&rdquo;까지만 말합니다.'),
            ('벽을 헐어도 되는지 판단하지 않습니다.',
             '내력벽인지, 배관을 옮길 수 있는지는 도면과 현장을 보고 정할 일입니다. 전화로 답하지 않습니다.'),
            ('이웃 동의와 관리사무소 신고를 대신 장담하지 않습니다.',
             '공사 가능 시간과 신고 절차는 단지마다 다릅니다. 확인해야 할 항목으로 남기고 실측 때 상의합니다.')],
 'fields': ['주소 · 평형 · 공사 범위', '희망 공사 시기와 거주 여부', '요금표 기준 안내 범위',
            '실측 예약 시간', '관리사무소 신고 · 동의 확인 필요 여부', '참고 사진 수신 기록'],
 'stages': ['문의 접수', '실측 예약', '실측 · 견적', '계약', '시공 · 준공'],
 'lead': '그라인더 소리에 묻히는 리모델링 문의. 실측 없이 견적을 내지 않고, 범위와 실측 날짜만 잡습니다.',
 'group': 2,
 'en': {
  'name': 'Renovation contractors', 'owner': 'the owner',
  'kicker': 'Remodelers &middot; kitchen &amp; bath &middot; general contractors',
  'h1': 'Next to a tile saw<br>you never hear the phone.',
  'sub': 'The owner spends the day on a job site. '
         'Meanwhile &ldquo;what would one bathroom cost?&rdquo; becomes a number in the missed-call list.',
  'cost': 'One remodel inquiry is a five-figure job. But the homeowner calls three contractors at once and signs with '
          'whoever books the site visit first. The daytime hours when the owner is on site are exactly when that call '
          'comes, and by the evening call-back another contractor has already walked the house.',
  'call': [('Customer', '2:35 PM', 'What would a full bathroom remodel run, roughly? And how long does it take?'),
           ('Saleringo', '+27 s', 'A full bathroom remodel runs <b>$9,000 to $18,000</b> depending on size and finishes, and the real number '
                                  'needs a site visit. Most take <b>four to six working days</b>; moving plumbing adds time. '
                                  'The site visit is free — I have <b>Thursday at 2 PM</b> or <b>Saturday at 10 AM</b>.'),
           ('Customer', '2:37 PM', 'Saturday at ten. It’s a condo, and we’re living in it.'),
           ('Saleringo', '+10 s', 'Saturday at 10 AM is booked. Since you’re living there, the owner will go over how you’ll manage without the bathroom during the work. '
                                  'Text me the address, the unit size and any photos you like, and may I have your name and a mobile number?')],
  'refuse': [('It never fixes a quote without a site visit.',
              'Square footage and photos get a range, never a final figure. The estimate is the owner’s, after measuring.'),
             ('It never promises a completion date.',
              'Material lead times, HOA approval and what the demo uncovers all move it. It says &ldquo;most take,&rdquo; nothing firmer.'),
             ('It never says whether a wall can come out.',
              'Load-bearing walls and plumbing relocation are decided from the plans and the site, not over the phone.'),
             ('It never guarantees HOA or neighbour sign-off.',
              'Working hours and permit rules differ by building. They are logged as items to confirm at the visit.')],
  'fields': ['Address, unit size and scope', 'Timing wanted and whether occupied', 'Range quoted from your price list',
             'Site visit booked', 'HOA permit or approval to check', 'Reference photos received'],
  'stages': ['Inquiry', 'Site visit booked', 'Measured & estimated', 'Contract', 'Build & handover'],
  'when': {'eyebrow': 'The call over the job-site noise', 'h2': 'Next to the tile saw,<br>this is how it goes.', 'tt': 'on site', 'badge': 'Cannot hear the phone'},
  'lead': 'The remodel inquiry drowned out by a grinder. No estimate without measuring — a range and a site-visit date instead.',
  'room': 'home-property',
  'room_d': 'The 2:35 PM bathroom-remodel call answered over the tile saw: a range from your own sheet, a free site visit booked for Saturday — and no estimate or completion date fixed before anyone has measured.',
  'room_no': ('0', 'estimates confirmed before a site visit'),
 },
},
{
 'slug': 'landscaping', 'owner': '사장님', 'name': '조경·정원 관리', 'photo': ph('PENDING'),
 'when': {'eyebrow': '예초기 소리 속의 통화', 'h2': '잔디 깎는 동안<br>이렇게 흘러갑니다.', 'tt': '작업 중', 'badge': '엔진을 끌 수 없는 시간'},
 'kicker': '조경 &middot; 정원 관리 &middot; 잔디 · 수목',
 'h1': '예초기를 멘 채로는<br>전화를 받을 수 없습니다.',
 'sub': '봄부터 가을까지 사장님은 남의 집 마당에 있습니다. '
        '주말에 손님이 올 사람이 금요일 오전에 &ldquo;오늘 잔디 되나요&rdquo;라고 전화를 겁니다.',
 'cost': '조경 문의는 날씨와 계절에 묶여 있습니다. 4월과 5월에 놓친 전화는 그해 정기 관리 계약이고, '
         '정기 관리 한 집은 한 시즌에 여덟 번에서 열 번 방문입니다. 그런데 그 전화가 오는 시간은 정확히 예초기 엔진이 돌아가는 시간이고, '
         '점심에 부재중을 보고 걸어도 그 집은 이미 다른 팀과 날짜를 잡았습니다.',
 'call': [('손님', '10:30 AM', '전원주택인데 마당 잔디 깎고 나무 몇 그루 가지치기하려고요. 얼마나 나와요?'),
          ('Saleringo', '+26초', '잔디 깎기는 <b>100평 기준 12만원부터</b>이고, 가지치기는 나무 높이와 그루 수에 따라 달라서 '
                                 '사장님이 보고 견적을 냅니다. 방문 견적은 무료이고, 이번 주는 <b>목요일 오후 3시</b>가 비어 있습니다. '
                                 '장비 차량이 들어갈 수 있는지도 그때 같이 봅니다.'),
          ('손님', '10:32 AM', '목요일 3시에 와 주세요. 소나무가 5미터쯤 되는데 그것도 되나요?'),
          ('Saleringo', '+9초', '5미터 소나무는 사다리나 장비가 필요할 수 있어서 현장에서 확인해 드리겠습니다. '
                                '목요일 오후 3시 방문 견적으로 잡았습니다. 주소와 마당 대략 면적을 남겨 주시고, 성함과 연락처도 부탁드립니다.')],
 'refuse': [('보지 않은 마당의 금액을 확정하지 않습니다.',
             '면적만 듣고 가지치기나 조경 금액을 말하지 않습니다. 경사, 수목 높이, 장비 진입 여부에 따라 달라집니다.'),
            ('작업 날짜를 못 박지 않습니다.',
             '비가 오면 밀립니다. &ldquo;토요일에 꼭 끝냅니다&rdquo;는 사장님이 날씨를 보고 말할 일입니다.'),
            ('나무의 병을 진단하지 않습니다.',
             '잎이 마른다, 벌레가 있다는 말에 병명이나 약을 말하지 않습니다. 보고 판단할 항목으로 남깁니다.'),
            ('큰 나무를 베어 준다고 약속하지 않습니다.',
             '보호수나 허가가 필요한 벌목이 있습니다. 가능 여부는 확인 후 답하고, 전화로 확답하지 않습니다.')],
 'fields': ['주소와 마당 면적', '요청 작업(잔디 · 전지 · 제초 · 정기 관리)', '희망 시기',
            '요금표 기준 안내 범위', '방문 견적 시간', '장비 차량 진입 · 주차 여부'],
 'stages': ['문의 접수', '방문 견적', '견적 승인', '작업', '정기 관리 제안'],
 'lead': '예초기 엔진이 도는 동안 오는 전화. 보지 않은 마당에 금액을 확정하지 않고, 방문 견적만 잡습니다.',
 'group': 2,
 'en': {
  'name': 'Landscaping & lawn care', 'owner': 'the owner',
  'kicker': 'Landscaping &middot; lawn care &middot; tree work',
  'h1': 'You cannot answer a phone<br>on a mower.',
  'sub': 'From spring to fall the owner is in somebody else’s yard. '
         'A homeowner with weekend guests calls on Friday morning asking &ldquo;can you mow today?&rdquo;',
  'cost': 'Landscaping inquiries are tied to weather and season. A call missed in April or May is that year’s maintenance '
          'contract, and one contract is eight to ten visits a season. But the call comes precisely while the mower is '
          'running, and when you see the missed call at lunch, that house has already booked another crew.',
  'call': [('Customer', '10:30 AM', 'I need the lawn mowed and a few trees trimmed at my place. What would you charge?'),
           ('Saleringo', '+26 s', 'Mowing starts at <b>$60 a visit</b> for up to a quarter acre. Trimming depends on the height and number of trees, '
                                  'so the owner prices it after seeing them. The estimate visit is free, and <b>Thursday at 3 PM</b> is open this week. '
                                  'He’ll also check whether the truck can get in.'),
           ('Customer', '10:32 AM', 'Thursday at three works. One of the pines is about sixteen feet — can you do that too?'),
           ('Saleringo', '+9 s', 'A sixteen-foot pine may need a ladder or a lift, so he’ll confirm that on site. You’re booked for Thursday at 3 PM. '
                                 'Please leave the address and roughly how big the yard is, plus your name and a mobile number.')],
  'refuse': [('It never fixes a price on a yard nobody has seen.',
              'Acreage alone gets no trimming or landscaping figure. Slope, tree height and truck access all change it.'),
             ('It never nails down a work date.',
              'Rain pushes everything. &ldquo;Definitely done Saturday&rdquo; is something the owner says after checking the forecast.'),
             ('It never diagnoses a sick tree.',
              'Browning leaves or bugs get no disease name and no spray recommendation — just a note for the visit.'),
             ('It never promises to take down a large tree.',
              'Some removals need a permit or are protected. It says &ldquo;we’ll confirm,&rdquo; never yes, on the phone.')],
  'fields': ['Address and yard size', 'Work requested (mow · trim · cleanup · maintenance)', 'Timing wanted',
             'Range quoted from your price list', 'Estimate visit booked', 'Truck access and parking'],
  'stages': ['Inquiry', 'Estimate visit', 'Quote approved', 'Job done', 'Maintenance plan offered'],
  'when': {'eyebrow': 'The call over the mower', 'h2': 'While the mower is running,<br>this is how it goes.', 'tt': 'on the mower', 'badge': 'Cannot cut the engine'},
  'lead': 'The call that comes while the mower is running. No price on a yard nobody has seen — an estimate visit booked instead.',
  'room': 'home-property',
  'room_d': 'The 10:30 AM call taken while you are on the mower: the mowing rate from your own list, the free estimate visit booked for Thursday — and no tree-work price or work date fixed before anyone has seen the yard.',
  'room_no': ('0', 'quotes given before seeing the job'),
 },
},
{
 'slug': 'locksmith', 'owner': '사장님', 'name': '열쇠·도어락', 'photo': ph('PENDING'),
 'when': {'eyebrow': '밤 열한 시의 통화', 'h2': '현관 앞에 서 있는 사람에게<br>이렇게 흘러갑니다.', 'tt': '밤 11시', 'badge': '다른 현장으로 출동 중'},
 'kicker': '열쇠 &middot; 도어락 &middot; 출장 개방',
 'h1': '문 앞에 서 있는 사람은<br>두 번째 번호로 넘어갑니다.',
 'sub': '밤 열한 시, 도어락 배터리가 나가서 집에 못 들어가는 사람이 검색 결과를 위에서부터 겁니다. '
        '첫 번째가 안 받으면 두 번째, 두 번째가 안 받으면 세 번째입니다.',
 'cost': '열쇠 문의는 지금 당장의 일입니다. 잠긴 사람은 콜백을 기다리지 않고, 먼저 받는 곳이 그 출동을 가져갑니다. '
         '그런데 사장님이 다른 현장에서 문을 열고 있는 동안에는 전화를 받을 수 없고, '
         '그 십 분 사이에 손님은 이미 다른 업체와 통화를 끝냈습니다. 야간 출동은 단가가 가장 높은 일이기도 합니다.',
 'call': [('손님', '11:05 PM', '도어락 배터리가 나갔는지 문이 안 열려요. 지금 와 주실 수 있나요? 얼마예요?'),
          ('Saleringo', '+14초', '지금 사장님이 다른 현장에 계셔서 <b>40분 안에</b> 도착 가능합니다. 야간 개방 출장은 '
                                 '<b>6만원에서 8만원</b> 사이이고, 도어락 종류에 따라 현장에서 확정됩니다. '
                                 '집 안에 아이나 어르신이 혼자 계신가요?'),
          ('손님', '11:06 PM', '아니요, 저 혼자예요. 40분 기다릴게요.'),
          ('Saleringo', '+8초', '출동으로 잡았습니다. 현장에서 <b>신분증으로 거주 확인</b>을 하니 준비해 주시고, '
                                '주소와 도어락 브랜드를 알려 주시면 사장님께 바로 전달하겠습니다. 도착 전에 한 번 전화드립니다.')],
 'refuse': [('전화로 본인 확인을 끝내지 않습니다.',
             '&ldquo;제 집 맞아요&rdquo;로 문을 열지 않습니다. 신분증과 거주 확인은 현장에서 사장님이 합니다. 열쇠 업종이 지켜야 할 첫 번째 선입니다.'),
            ('문을 여는 방법을 알려 주지 않습니다.',
             '어떻게 하면 열리는지 묻는 질문에는 답하지 않습니다. 출동만 잡습니다.'),
            ('안에 사람이 갇혀 있으면 119 다음에 사람입니다.',
             '아이가 안에 있다, 가스 냄새가 난다는 말이 나오면 119 안내를 먼저 읽고 즉시 사장님 번호로 연결합니다.'),
            ('최종 금액을 문 앞에서 정합니다.',
             '출장비 범위까지만 말합니다. 파손 개방인지, 교체가 필요한지는 문을 보고 정합니다.')],
 'fields': ['주소와 문 종류(현관 · 도어락 · 차량 · 금고)', '상황(잠김 · 고장 · 분실 · 교체)', '출동 요청 시각과 예상 도착',
            '요금표 기준 출장비 범위', '본인 확인 안내 여부', '안에 사람이 있는지 확인한 기록'],
 'stages': ['문의 접수', '출동 배정', '현장 확인', '작업 · 정산', '사후 안내'],
 'lead': '밤 열한 시, 문 앞에 서 있는 사람의 전화. 본인 확인을 전화로 끝내지 않고, 출장비 범위와 도착 시간만 말합니다.',
 'group': 2,
 'en': {
  'name': 'Locksmiths', 'owner': 'the owner',
  'kicker': 'Locksmiths &middot; smart locks &middot; lockouts',
  'h1': 'The person at the door<br>dials the next number.',
  'sub': 'At 11 PM someone whose smart lock died is calling search results from the top. '
         'If the first does not answer, the second; if the second does not, the third.',
  'cost': 'A locksmith inquiry is a right-now problem. A locked-out caller does not wait for a call-back — whoever picks up '
          'gets the job. But while the owner is opening a door across town he cannot answer, and in those ten minutes the '
          'caller has already finished with another company. Night lockouts are also the highest-rate work you do.',
  'call': [('Customer', '11:05 PM', 'I think my smart lock’s battery died and I can’t get in. Can someone come now? What does it cost?'),
           ('Saleringo', '+14 s', 'The owner is finishing another job and can be there <b>within forty minutes</b>. An after-hours '
                                  'lockout is <b>$95 to $150</b>, confirmed at the door depending on the lock. '
                                  'Is there a child or an elderly person alone inside?'),
           ('Customer', '11:06 PM', 'No, it’s just me. Forty minutes is fine.'),
           ('Saleringo', '+8 s', 'You’re on the dispatch list. He’ll <b>check photo ID against the address</b> at the door, so have it ready. '
                                 'Tell me the address and the lock brand and I’ll pass it straight to him. He’ll call before he arrives.')],
  'refuse': [('It never completes identity verification over the phone.',
              '&ldquo;It’s my house&rdquo; opens nothing. ID and proof of residence are checked at the door by the owner — the first line a locksmith holds.'),
             ('It never explains how to open a lock.',
              'A question about how to get a door open is not answered. A dispatch is booked instead.'),
             ('Someone locked inside means 911 first, then a person.',
              'A child inside, a gas smell, a medical worry — the emergency line is read first and the owner’s phone rings immediately.'),
             ('The final price is set at the door.',
              'Only the call-out range is quoted. Whether it is a pick, a drill-out or a replacement is decided looking at the lock.')],
  'fields': ['Address and lock type (door · smart lock · car · safe)', 'Situation (lockout · failure · lost key · rekey)', 'Time requested and ETA',
             'Call-out range from your price list', 'ID check explained', 'Anyone inside confirmed'],
  'stages': ['Inquiry', 'Dispatched', 'On site', 'Job & payment', 'Follow-up'],
  'when': {'eyebrow': 'The call at eleven at night', 'h2': 'For the person standing at the door,<br>this is how it goes.', 'tt': '11 PM', 'badge': 'Out on another job'},
  'lead': 'The 11 PM call from someone standing at their own front door. ID is never verified by phone — only the call-out range and the ETA.',
  'room': 'home-property',
  'room_d': 'The 11:05 PM lockout: the ETA and the after-hours range from your own list, a dispatch booked, the ID check at the door explained — and anyone locked inside sent to 911 before anything else.',
  'room_no': ('0', 'identities verified over the phone'),
 },
},
{
 'slug': 'appliance-repair', 'owner': '사장님', 'name': '가전 수리', 'photo': ph('PENDING'),
 'when': {'eyebrow': '이동 중의 통화', 'h2': '다음 집으로 운전하는 동안<br>이렇게 흘러갑니다.', 'tt': '출장 이동 중', 'badge': '핸들을 잡고 있는 시간'},
 'kicker': '가전 수리 &middot; 세탁기 · 냉장고 · 에어컨',
 'h1': '핸들을 잡고 있는 동안<br>다음 손님이 전화합니다.',
 'sub': '하루에 여섯 집을 돌면 그 사이 운전 시간이 두 시간입니다. '
        '세탁기가 멈춘 집은 그 두 시간 안에 다른 기사와 통화를 끝냅니다.',
 'cost': '가전 수리 문의는 &ldquo;오늘 올 수 있나요&rdquo;로 시작합니다. 냉장고가 안 시원한 집은 하루를 기다리지 않습니다. '
         '그런데 사장님이 남의 집 세탁기 뒤에 있거나 다음 집으로 운전하는 동안에는 받을 수 없고, '
         '저녁에 콜백하면 그 집은 이미 고쳐졌거나 새 제품을 주문했습니다. 여름 에어컨 성수기에는 그런 전화가 하루 열 통입니다.',
 'call': [('손님', '4:15 PM', '세탁기가 탈수가 안 되고 물이 안 빠져요. 오늘 오실 수 있나요? 얼마 정도 들어요?'),
          ('Saleringo', '+22초', '배수 문제는 배수펌프나 호스 막힘일 수 있는데, 원인은 기사님이 보셔야 정확합니다. '
                                 '출장 점검비는 <b>3만원</b>이고 수리하시면 공임에 포함됩니다. 배수펌프 교체면 부품 포함 '
                                 '<b>8만원에서 12만원</b> 사이입니다. 오늘은 <b>저녁 6시 30분 이후</b>, 내일은 <b>오전 10시</b>가 가능합니다.'),
          ('손님', '4:17 PM', '오늘 6시 반으로요. 삼성 드럼이고 5년쯤 됐어요.'),
          ('Saleringo', '+9초', '오늘 저녁 6시 30분 방문으로 잡았습니다. 모델명은 세탁기 문 안쪽 라벨에 있으니 사진으로 보내 주시면 '
                                '부품을 미리 챙겨 가겠습니다. 주소와 주차 가능 여부, 성함과 연락처를 남겨 주세요.')],
 'refuse': [('증상만 듣고 원인을 단정하지 않습니다.',
             '&ldquo;펌프입니다&rdquo;로 끝내지 않습니다. 가능성까지만 말하고, 진단은 기사님이 열어 보고 합니다.'),
            ('최종 수리비를 확정하지 않습니다.',
             '점검비와 흔한 수리의 범위까지만 말합니다. 모델과 부품 재고에 따라 달라지고, 견적은 점검 후에 나옵니다.'),
            ('당일 수리 완료를 약속하지 않습니다.',
             '부품이 없으면 주문 후 재방문입니다. &ldquo;오늘 다 고쳐 드립니다&rdquo;는 말하지 않습니다.'),
            ('타는 냄새와 스파크는 안내 문구 다음에 사람입니다.',
             '연기, 타는 냄새, 가스 냄새가 나오면 플러그를 뽑고 가스 밸브를 잠그라는 문구를 읽고 즉시 연결합니다. 직접 고치는 방법은 알려 주지 않습니다.')],
 'fields': ['제품 종류 · 브랜드 · 모델 · 연식', '증상 설명 원문', '방문 희망 시각과 확정 시각',
            '요금표 기준 점검비와 예상 범위', '부품 확인 필요 여부', '주소 · 주차 · 엘리베이터'],
 'stages': ['문의 접수', '방문 예약', '점검 · 견적', '수리', '사후 확인'],
 'lead': '다음 집으로 운전하는 동안 오는 전화. 증상만 듣고 원인을 단정하지 않고, 점검비와 범위만 말하고 방문을 잡습니다.',
 'group': 2,
 'en': {
  'name': 'Appliance repair', 'owner': 'the owner',
  'kicker': 'Appliance repair &middot; washers · fridges · HVAC',
  'h1': 'The next customer calls<br>while your hands are on the wheel.',
  'sub': 'Six houses a day means two hours of driving in between. '
         'The house with the dead washer finishes its call with another tech inside those two hours.',
  'cost': 'Appliance calls open with &ldquo;can you come today?&rdquo; A warm refrigerator does not wait a day. But while '
          'the owner is behind somebody’s washer or driving to the next house he cannot answer, and by the evening '
          'call-back that house is fixed or has ordered a new unit. In air-conditioning season that is ten calls a day.',
  'call': [('Customer', '4:15 PM', 'My washer won’t drain or spin. Can you come today? Any idea what it might cost?'),
           ('Saleringo', '+22 s', 'No drain can be the pump or a blocked hose, and the tech has to see it to be sure. '
                                  'The diagnostic visit is <b>$79</b> and it’s waived if you go ahead with the repair. A drain-pump replacement runs '
                                  '<b>$150 to $220</b> with parts. Today I have <b>after 6:30 PM</b>, or tomorrow at <b>10 AM</b>.'),
           ('Customer', '4:17 PM', 'Tonight at six thirty. It’s a Samsung front-loader, about five years old.'),
           ('Saleringo', '+9 s', 'Booked for 6:30 this evening. The model number is on the label inside the door — text me a photo and he’ll bring the likely part. '
                                 'Please leave the address, whether there’s parking, and your name and mobile number.')],
  'refuse': [('It never names the cause from a description.',
              'It does not end with &ldquo;it’s the pump.&rdquo; It gives the possibilities and leaves the diagnosis to the tech with the panel off.'),
             ('It never fixes the final repair bill.',
              'The diagnostic fee and the range for a common repair are all it quotes. Model and parts stock change the rest, and the estimate follows the inspection.'),
             ('It never promises a same-day fix.',
              'If the part is not on the truck, it is a second visit. &ldquo;We’ll have it done tonight&rdquo; is never said.'),
             ('A burning smell or sparks gets the safety line, then a person.',
              'Smoke, burning or gas means unplug it and shut the valve — read from your script — and an immediate transfer. It never explains how to fix it yourself.')],
  'fields': ['Appliance, brand, model and age', 'Symptom in the customer’s words', 'Time wanted and time booked',
             'Diagnostic fee and range from your price list', 'Part to check before the visit', 'Address · parking · elevator'],
  'stages': ['Inquiry', 'Visit booked', 'Diagnosed & quoted', 'Repaired', 'Follow-up check'],
  'when': {'eyebrow': 'The call between jobs', 'h2': 'While you are driving to the next house,<br>this is how it goes.', 'tt': 'between jobs', 'badge': 'Hands on the wheel'},
  'lead': 'The call that comes while you drive to the next house. No cause named from a description — the diagnostic fee, a range, and a visit booked.',
  'room': 'home-property',
  'room_d': 'The 4:15 PM dead-washer call answered between jobs: the diagnostic fee and a repair range from your own list, tonight’s slot booked, the model photo requested — and no cause or final bill named before the panel comes off.',
  'room_no': ('0', 'faults diagnosed from a description'),
 },
},
{
 'slug': 'laundry', 'owner': '사장님', 'name': '세탁·드라이클리닝', 'photo': ph('PENDING'),
 'when': {'eyebrow': '개점 전의 통화', 'h2': '다림질대 앞에 서 있는 동안<br>이렇게 흘러갑니다.', 'tt': '개점 전', 'badge': '스팀을 끌 수 없는 시간'},
 'kicker': '세탁소 &middot; 드라이클리닝 &middot; 수거 · 배달',
 'h1': '금요일에 입을 정장은<br>화요일 아침에 맡겨집니다.',
 'sub': '개점 전 여덟 시, 사장님은 이미 다림질대 앞에 있습니다. '
        '출근길 손님이 그 시간에 &ldquo;금요일까지 되나요&rdquo;라고 전화를 겁니다.',
 'cost': '세탁소 손님은 동네 손님입니다. 한 번 맡긴 사람은 계속 맡기고, 한 번 못 맡긴 사람은 옆 동네 수거 서비스 앱으로 갑니다. '
         '문의는 &ldquo;언제 되나요, 얼마예요, 수거 오나요&rdquo; 셋뿐인데 그 셋에 답할 사람은 스팀 다리미를 쥐고 있고, '
         '벨 소리는 프레스 소리에 묻힙니다.',
 'call': [('손님', '8:10 AM', '정장 한 벌 드라이 맡기려는데 금요일까지 되나요? 와인 얼룩이 좀 있어요. 수거도 되나요?'),
          ('Saleringo', '+20초', '정장 상하 드라이는 <b>1만 2천원</b>이고, 오늘 맡기시면 <b>목요일 오후</b>에 나옵니다. '
                                 '와인 얼룩은 종류와 시간이 지난 정도에 따라 안 빠질 수도 있어서, 사장님이 보시고 미리 말씀드립니다. '
                                 '수거는 <b>3만원 이상</b>이면 무료이고, 그 아래는 <b>3천원</b>입니다.'),
          ('손님', '8:11 AM', '그럼 코트도 같이 맡길게요. 오늘 오후에 수거 가능해요?'),
          ('Saleringo', '+8초', '코트는 <b>1만 5천원</b>이고, 합쳐서 2만 7천원이라 수거비 3천원이 붙습니다. 오늘 <b>오후 2시에서 4시 사이</b> 수거로 잡았습니다. '
                                '주소와 성함, 연락처를 남겨 주시면 기사님이 출발 전에 연락드립니다.')],
 'refuse': [('얼룩이 빠진다고 약속하지 않습니다.',
             '와인, 기름, 잉크는 종류와 지난 시간에 따라 다릅니다. &ldquo;보시고 미리 말씀드립니다&rdquo;에서 멈춥니다.'),
            ('물량을 보지 않고 완료 시각을 당기지 않습니다.',
             '기본 소요일만 말합니다. 급행이 되는지는 그날 물량을 아는 사장님이 정합니다.'),
            ('손상 보상을 판단하지 않습니다.',
             '옷이 줄었다, 색이 빠졌다는 이야기는 소비자분쟁해결기준과 사장님이 정할 일입니다. 사실만 받아 적고 넘깁니다.'),
            ('명품과 가죽을 전화로 받지 않습니다.',
             '소재 표시를 보고 사장님이 세탁 가능 여부를 정합니다. 접수 전 확인 항목으로 남깁니다.')],
 'fields': ['의류 종류와 수량', '얼룩 종류와 지난 시간(본인 설명)', '희망 완료일과 안내한 완료일',
            '요금표 기준 안내 금액', '수거 · 배달 주소와 시간대', '기사 출발 연락 기록'],
 'stages': ['문의 접수', '수거 · 접수', '세탁', '완료 알림', '배달 · 수령'],
 'lead': '프레스 소리에 묻히는 개점 전 전화. 얼룩이 빠진다고 말하지 않고, 요금과 수거 시간만 잡습니다.',
 'group': 2,
 'en': {
  'name': 'Dry cleaning & laundry', 'owner': 'the owner',
  'kicker': 'Dry cleaners &middot; laundry &middot; pickup &amp; delivery',
  'h1': 'Friday’s suit<br>gets dropped off on Tuesday morning.',
  'sub': 'At eight, before opening, the owner is already at the press. '
         'A commuter calls at that moment asking &ldquo;can you have it by Friday?&rdquo;',
  'cost': 'A dry-cleaning customer is a neighbourhood customer. Whoever drops off once keeps dropping off, and whoever '
          'could not reach you once switches to the pickup app from two towns over. The questions are only three — when, '
          'how much, do you pick up — and the person who can answer is holding a steam iron while the press drowns the ring.',
  'call': [('Customer', '8:10 AM', 'I need a suit dry-cleaned by Friday. It has a bit of a wine stain. And do you pick up?'),
           ('Saleringo', '+20 s', 'A two-piece suit is <b>$18</b>, and dropped off today it’s ready <b>Thursday afternoon</b>. '
                                  'Wine depends on the fabric and how long it’s set, so the owner will look at it and tell you upfront if it may not come out. '
                                  'Pickup is free on orders over <b>$45</b>; under that it’s <b>$5</b>.'),
           ('Customer', '8:11 AM', 'Then add a coat too. Can you pick up this afternoon?'),
           ('Saleringo', '+8 s', 'With the coat at <b>$22</b> that’s forty dollars, so there’s a <b>$5</b> pickup fee. I’ve set it for <b>between 2 and 4 PM</b> today. '
                                 'Leave the address, your name and a mobile number, and the driver will text before heading over.')],
  'refuse': [('It never guarantees a stain will come out.',
              'Wine, oil and ink depend on fabric and time. It stops at &ldquo;the owner will look and tell you upfront.&rdquo;'),
             ('It never promises a rush without seeing the day’s load.',
              'Only the standard turnaround is quoted. Whether a rush is possible is decided by the owner who knows what is on the rail.'),
             ('It never rules on a damage claim.',
              'A shrunk sweater or faded shirt is a matter for the owner and the shop’s policy. The facts are written down and passed on.'),
             ('It never accepts designer or leather pieces by phone.',
              'The owner reads the care label and decides whether it can be cleaned. It is logged as an item to check at intake.')],
  'fields': ['Garments and count', 'Stain type and how long ago (customer’s words)', 'Date wanted and date quoted',
             'Price quoted from your list', 'Pickup / delivery address and window', 'Driver text sent'],
  'stages': ['Inquiry', 'Picked up', 'Cleaning', 'Ready notice', 'Delivered'],
  'when': {'eyebrow': 'The call before opening', 'h2': 'While you are at the press,<br>this is how it goes.', 'tt': 'before opening', 'badge': 'Cannot shut the steam off'},
  'lead': 'The pre-opening call lost under the press. No stain promised to come out — the price and the pickup window booked.',
  'room': 'home-property',
  'room_d': 'The 8:10 AM call at the press: the suit priced from your own list, Thursday’s turnaround and a free pickup booked — and the wine stain never promised to come out.',
  'room_no': ('0', 'stains the AI is allowed to guarantee'),
 },
},
]
