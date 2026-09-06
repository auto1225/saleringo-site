# -*- coding: utf-8 -*-
"""다섯 개 업종 추가 — 일곱 번째 묶음.

공유오피스 · 투어 · 사립/국제학교 · 인력파견 · 영상의학/검진센터.
각 항목의 'en' 은 영문 사이트용이며 번역이 아니라 그 나라의 통화로 다시 쓴 것이다.
'group' 은 build/ko/p_trades.py 의 GROUPS 인덱스, 'en.room' 은 en/industries.html 의 방 id.
"""

PH = 'https://images.pexels.com/photos/%s/pexels-photo-%s.jpeg'


def ph(i):
    return PH % (i, i)


TRADES7 = [
{
 'slug': 'coworking', 'owner': '대표님', 'name': '공유오피스 · 코워킹', 'photo': ph('PENDING'),
 'when': {'eyebrow': '점심시간의 통화', 'h2': '다른 손님과 투어를 도는 동안<br>이렇게 흘러갑니다.', 'tt': '점심시간', 'badge': '투어 안내 중'},
 'kicker': '공유오피스 &middot; 코워킹 &middot; 소호 사무실',
 'h1': '사무실을 보러 다니는 사람은<br>점심시간에 겁니다.',
 'sub': '근처 건물 두세 곳을 돌다가 길에서 바로 전화합니다. 매니저는 다른 손님과 투어 중이고, '
        '벨이 울리다 끊긴 전화는 길 건너 건물에 계약을 줍니다.',
 'cost': '4인 사무실 하나는 월 165만원짜리 계약이고, 한 번 들어온 회사는 몇 년을 머뭅니다. '
         '그 문의는 매니저가 투어를 돌고 있어 받을 수 없는 시간에 오고, 부재중을 만난 사람은 다음 건물에서 '
         '계약합니다. 공실로 남은 달의 월세는 누구의 실적에도 잡히지 않습니다.',
 'call': [('고객', '12:38 PM', '근처 사무실 몇 군데 보고 있는데요, 4인 사무실 월 얼마예요? 오늘 오후에 볼 수 있나요?'),
          ('Saleringo', '+14초', '4인 사무실은 월 <b>165만원</b>(부가세 별도)이고 관리비와 인터넷이 포함입니다. 지정석은 '
                                 '<b>35만원</b>, 자유석은 <b>22만원</b>입니다. 투어는 오늘 <b>오후 4시</b>와 내일 <b>오전 11시</b>가 가능합니다.'),
          ('고객', '12:39 PM', '4인실 지금 비어 있어요? 다음 주부터 바로 들어가고 싶은데요.'),
          ('Saleringo', '+9초', '지금 비어 있는 호실이 있는지는 매니저가 확인해야 정확해서 제가 특정 호실을 약속드리지 않습니다. '
                                '오후 4시 투어에서 비어 있는 호실을 직접 보시고 입주 가능일까지 안내받으실 수 있습니다. 잡아 드릴까요?'),
          ('고객', '12:40 PM', '네, 4시로요.'),
          ('Saleringo', '+7초', '오늘 오후 4시, 4인 사무실 투어로 잡았습니다. 성함과 연락처 남겨 주시면 '
                                '확인 문자에 오시는 길과 주차 안내를 넣어 보내 드리겠습니다.')],
 'refuse': [('확인하지 않은 호실을 비어 있다고 말하지 않습니다.',
             '공실은 매니저가 그날 확인해야 아는 것입니다. AI는 투어를 잡고, 비어 있는 호실은 그 자리에서 보여 드리는 것으로 남깁니다.'),
            ('요금표 밖의 할인을 만들지 않습니다.',
             '장기 계약 할인과 보증금 조정은 매니저의 권한입니다. 요금표에 적힌 금액과 조건만 말하고, 깎아 달라는 요청은 사람에게 넘깁니다.'),
            ('계약 조건을 전화로 확정하지 않습니다.',
             '입주일, 계약 기간, 보증금은 계약서로 정합니다. AI는 희망 조건을 받아 적을 뿐 어느 것도 약속하지 않습니다.'),
            ('다른 입주사의 정보를 말하지 않습니다.',
             '어느 회사가 어느 호실을 쓰는지, 몇 명이 있는지는 입주사의 정보입니다. 물어도 답하지 않고 투어 예약으로 돌아갑니다.')],
 'fields': ['희망 좌석 유형(자유석 · 지정석 · 사무실)과 인원', '희망 입주일과 계약 기간', '요금표에서 안내한 월 이용료',
            '투어 예약 시간', '회의실 · 주차 · 24시간 출입 등 문의 사항', '확인 문자 발송 기록'],
 'stages': ['문의 접수', '투어 예약', '투어 · 공실 확인', '계약', '입주'],
 'lead': '점심시간에 근처 사무실을 돌다가 겁니다. 요금표의 금액만 말하고, 호실이 비었는지는 확인 뒤에 답하도록 투어를 잡습니다.',
 'group': 4,
 'en': {
  'name': 'Coworking spaces', 'owner': 'the community manager',
  'kicker': 'Coworking &middot; flexible offices &middot; hot desks',
  'h1': 'The inquiry lands at lunch,<br>from someone touring three buildings.',
  'sub': 'Office hunters spend the lunch hour walking between buildings and call from the pavement. '
         'The community manager is mid-tour with somebody else, and the call that rings out signs across the street.',
  'cost': 'A four-person office is a two-thousand-dollar-a-month contract, and the company that moves in stays for years. '
          'The inquiry arrives while the manager is walking a tour and cannot pick up, and the caller who gets voicemail '
          'signs in the next building. The month an office sits empty appears on nobody&rsquo;s numbers.',
  'call': [('Customer', '12:38 PM', 'I&rsquo;m looking at a few spaces nearby. What&rsquo;s a four-person office a month, and can I see it this afternoon?'),
           ('Saleringo', '+14 s', 'A four-person private office is <b>$2,200 a month</b>, with utilities and internet included. A dedicated desk '
                                  'is <b>$450</b> and a hot desk is <b>$275</b>. I can show you the space today at <b>4:00 PM</b> or tomorrow at <b>11:00 AM</b>.'),
           ('Customer', '12:39 PM', 'Is a four-person office free right now? I&rsquo;d want to move in next week.'),
           ('Saleringo', '+9 s', 'Whether a specific office is free is something the community manager confirms, so I don&rsquo;t promise one on the phone. '
                                 'On the 4:00 PM tour you&rsquo;ll see what is actually open and get a move-in date. Shall I book it?'),
           ('Customer', '12:40 PM', 'Four o&rsquo;clock works.'),
           ('Saleringo', '+7 s', 'Booked: today at 4:00 PM, a tour for a four-person office. Give me your name and mobile number and '
                                 'I&rsquo;ll text the confirmation with directions and parking.')],
  'refuse': [('It never calls an office available before it has been checked.',
              'Vacancy is something the manager confirms on the day. The AI books the tour and leaves the empty office to be shown in person.'),
             ('It never invents a discount.',
              'Long-term discounts and deposit adjustments are the manager&rsquo;s authority. It quotes the rate card and passes any haggling to a person.'),
             ('It never settles contract terms on the phone.',
              'Move-in date, term and deposit are decided in the agreement. The AI records what the caller wants and promises none of it.'),
             ('It never talks about other members.',
              'Which company sits in which office, and how many of them there are, belongs to those members. Asked, it declines and returns to the booking.')],
  'fields': ['Seat type wanted (hot desk, dedicated desk, office) and headcount', 'Move-in date and term wanted',
             'Monthly rate quoted from the rate card', 'Tour booked',
             'Meeting rooms, parking and 24-hour access asked about', 'Confirmation text sent'],
  'stages': ['Inquiry', 'Tour booked', 'Tour and availability check', 'Agreement', 'Move-in'],
  'when': {'eyebrow': 'A call in the middle of a tour', 'h2': 'While another tour is walking the floor,<br>this is how it goes.', 'tt': 'lunch hour', 'badge': 'mid-tour'},
  'lead': 'Office hunters call at lunch from the pavement. It quotes the rate card, books the tour, and leaves whether a specific office is free to the manager.',
  'room': 'places-hospitality',
  'room_d': 'The lunchtime caller between three buildings quoted the rate card and booked onto the 4:00 PM tour &mdash; without a promise that any particular office is free until the manager has checked.',
  'room_no': ('0', 'offices promised free before anyone has checked'),
 },
},
{
 'slug': 'tours-activities', 'owner': '대표님', 'name': '투어 · 액티비티 · 체험', 'photo': ph('PENDING'),
 'when': {'eyebrow': '출발 전날 밤의 통화', 'h2': '가이드가 잠든 밤에<br>이렇게 흘러갑니다.', 'tt': '밤 10시', 'badge': '가이드 취침 중'},
 'kicker': '투어 &middot; 액티비티 &middot; 체험',
 'h1': '내일 일정은<br>밤 열 시에 정해집니다.',
 'sub': '여행자는 저녁을 먹고 숙소에 돌아와 내일을 정합니다. 가이드는 새벽 출발을 앞두고 잠들어 있고, '
        '받지 않은 전화는 온라인 예약이 되는 다른 업체로 갑니다.',
 'cost': '카약 투어 두 자리는 13만원이고 네 식구면 그 두 배입니다. 그 전화는 여행자가 일정을 짜는 밤 열 시에 오고, '
         '안 받으면 검색 결과의 다음 업체가 가져갑니다. 빈 자리로 나간 배는 그날 매출에서 사라지고, '
         '성수기의 빈 자리는 다시 채워지지 않습니다.',
 'call': [('손님', '10:04 PM', '내일 오전 카약 투어 어른 두 명 되나요? 가격도 알려 주세요.'),
          ('Saleringo', '+12초', '내일 <b>오전 9시 30분</b> 출발 회차에 <b>두 자리</b>가 남아 있습니다. 성인은 <b>1인 6만 5천원</b>이고 '
                                 '구명조끼와 방수 가방이 포함됩니다. 두 시간 반 코스이고, 출발 20분 전에 해안공원 매표소 앞에서 모입니다.'),
          ('손님', '10:05 PM', '내일 비 온다던데, 그래도 나가나요?'),
          ('Saleringo', '+8초', '날씨에 따른 출발 여부는 당일 아침에 대표님이 바다 상황을 보고 정하기 때문에 제가 오늘 밤에 확정해 드리지 않습니다. '
                                '취소되면 전액 환불입니다. 두 자리는 가예약으로 잡아 두고 <b>아침 7시</b>까지 문자로 알려 드리겠습니다.'),
          ('손님', '10:06 PM', '그럼 일단 두 명 잡아 주세요.'),
          ('Saleringo', '+7초', '내일 9시 30분 카약 투어 성인 2명, 가예약으로 잡았습니다. 성함과 연락처 남겨 주시면 집결 장소와 준비물 안내를 '
                                '문자로 보내 드리고, 출발 여부는 아침에 다시 문자 드립니다.')],
 'refuse': [('날씨가 걸린 출발을 미리 확정하지 않습니다.',
             '바람과 파도에 따라 나갈지 말지는 당일 아침 대표님이 정합니다. AI는 가예약과 환불 규정까지만 말하고, 확정은 사람의 문자로 남깁니다.'),
            ('몸 상태로 참여해도 되는지 판단하지 않습니다.',
             '임신 중이거나 심장 질환, 허리 수술 이력이 있는 분이 타도 되는지는 안전의 문제입니다. 그 질문은 바로 대표님에게 넘깁니다.'),
            ('요금표에 없는 단체 할인을 만들지 않습니다.',
             '정가와 등록된 단체 조건만 말합니다. 열 명이면 얼마냐는 질문에 표에 없는 숫자를 만들지 않습니다.'),
            ('정원을 넘겨 받지 않습니다.',
             '회차별로 남은 자리에서만 잡습니다. 자리가 없으면 대기로 적어 두고, 취소가 나면 순서대로 연락합니다.')],
 'fields': ['투어 이름과 출발 회차', '인원(성인 · 어린이)과 나이', '요금표에서 계산한 금액',
            '가예약 · 확정 상태', '건강 · 수영 가능 여부 등 확인 요청 사항', '집결 안내 · 출발 여부 문자 기록'],
 'stages': ['문의 접수', '가예약', '출발 확정 · 결제', '투어 진행', '후기 · 재예약 안내'],
 'lead': '내일 일정은 밤 열 시에 정해집니다. 정가와 남은 자리만 말하고, 비가 와도 나가는지는 아침에 사람이 정하도록 남깁니다.',
 'group': 4,
 'en': {
  'name': 'Tours & activities', 'owner': 'the tour operator',
  'kicker': 'Tours &middot; activities &middot; experiences',
  'h1': 'Tomorrow&rsquo;s trip is booked<br>from a hotel bed at ten at night.',
  'sub': 'Travellers plan the next day after dinner, back at the hotel with the weather app open. '
         'The guide is asleep before an early launch, and the call nobody answers goes to the operator with the online form.',
  'cost': 'Two seats on a sea-kayak tour are a hundred-and-seventy-dollar booking, and a family of four is twice that. '
          'The call comes at ten because that is when travellers plan, and the operator who does not answer hands the seats '
          'to the next search result. A boat that launches with empty seats loses them for good in high season.',
  'call': [('Customer', '10:04 PM', 'Do you have room for two adults on the kayak tour tomorrow morning, and what does it cost?'),
           ('Saleringo', '+12 s', 'Tomorrow&rsquo;s <b>9:30 AM</b> departure has <b>two seats</b> left. Adults are <b>$85 each</b>, with life jackets and a dry bag '
                                  'included. It&rsquo;s a two-and-a-half-hour paddle, and you meet at the beach hut twenty minutes before.'),
           ('Customer', '10:05 PM', 'The forecast says rain. Does it still go out?'),
           ('Saleringo', '+8 s', 'Whether a departure goes ahead is decided by the operator on the morning, from the sea state, so I can&rsquo;t confirm that tonight. '
                                 'If it is cancelled you are refunded in full. I can hold your two seats provisionally and text you by <b>7:00 AM</b> either way.'),
           ('Customer', '10:06 PM', 'Hold them, then.'),
           ('Saleringo', '+7 s', 'Two adults on tomorrow&rsquo;s 9:30 AM kayak tour, held provisionally. Give me your name and mobile number and I&rsquo;ll text '
                                 'the meeting point and what to bring, and the go or no-go in the morning.')],
  'refuse': [('It never confirms a weather-dependent departure.',
              'Wind and swell decide whether the boat goes out, and the operator reads them at first light. The AI holds the seat, states the refund rule and leaves the confirmation to a person.'),
             ('It never decides whether someone is fit to take part.',
              'Pregnancy, a heart condition or a back operation is a safety question, not a booking question. It goes straight to the operator.'),
             ('It never invents a group discount.',
              'It quotes list prices and the group terms on the sheet. Asked what ten people would cost, it does not make up a number that is not there.'),
             ('It never sells past the seat count.',
              'It books only from the seats left on each departure. When a departure is full it takes a waitlist entry and calls back in order if a seat opens.')],
  'fields': ['Tour and departure time', 'Headcount (adults, children) and ages', 'Price from the rate card',
             'Provisional or confirmed', 'Health, swimming ability and anything to check', 'Meeting-point and go/no-go texts sent'],
  'stages': ['Inquiry', 'Provisional hold', 'Confirmed and paid', 'On the water', 'Review and rebooking'],
  'when': {'eyebrow': 'A call the night before the launch', 'h2': 'While tomorrow is planned from a hotel bed,<br>this is how it goes.', 'tt': '10 PM', 'badge': 'guide asleep'},
  'lead': 'Tomorrow is planned at ten at night. It quotes list prices and holds a seat, and leaves whether the boat goes out in the rain to a person in the morning.',
  'room': 'places-hospitality',
  'room_d': 'The ten-o&rsquo;clock traveller quoted the list price and two seats held for the morning departure &mdash; with the rain question left to the operator at first light, not answered on the phone.',
  'room_no': ('0', 'departures confirmed in weather nobody has seen yet'),
 },
},
{
 'slug': 'schools', 'owner': '교장선생님', 'name': '사립 · 국제학교 · 교육기관', 'photo': ph('PENDING'),
 'when': {'eyebrow': '등교 시간의 통화', 'h2': '교문에서 등교 지도를 하는 동안<br>이렇게 흘러갑니다.', 'tt': '오전 8시', 'badge': '입학처 자리 비움'},
 'kicker': '사립학교 &middot; 국제학교 &middot; 입학처',
 'h1': '학부모는 아침 여덟 시,<br>등교 차량 줄에서 겁니다.',
 'sub': '입학 문의는 아이를 뒷자리에 태우고 교문 앞에 줄 서 있는 아침에 옵니다. '
        '입학처 선생님이 교문에 나가 있어 가장 받기 어려운 시간이기도 합니다.',
 'cost': '입학 한 건은 해마다 내는 수천만원의 학비가 아이가 다니는 동안 이어지는 금액이고, 동생이 따라오는 일도 흔합니다. '
         '학부모는 세 학교를 보고 답이 온 곳을 고릅니다. 받지 못한 아침 전화는 부재중 목록에만 남고, '
         '그 아이는 다른 학교의 명단에 오릅니다.',
 'call': [('학부모', '8:03 AM', '내년 봄에 초등 3학년 편입 문의드려요. 학비가 얼마고 원서는 언제까지예요?'),
          ('Saleringo', '+15초', '초등 3학년 기준 연간 학비는 <b>2,400만원</b>이고, 입학금 <b>150만원</b>과 통학버스 · 급식비는 별도입니다. '
                                 '봄학기 편입 원서는 <b>11월 30일</b>까지이고, 서류 심사 뒤 <b>12월 둘째 주</b>에 가족 면접이 있습니다.'),
          ('학부모', '8:04 AM', '저희 애가 영어를 잘하는 편인데, 3학년 편입은 어렵지 않겠죠?'),
          ('Saleringo', '+9초', '입학 여부와 배정 학년은 심사 뒤에 입학처에서 정하는 것이라 제가 말씀드릴 수 없습니다. 학교 투어에서 입학처 선생님이 '
                                '절차를 직접 설명드립니다. <b>이번 주 목요일 오전 10시</b>와 <b>다음 주 화요일 오전 10시</b>에 투어가 있습니다.'),
          ('학부모', '8:05 AM', '목요일로 할게요.'),
          ('Saleringo', '+7초', '목요일 오전 10시 학교 투어로 잡았습니다. 학부모님 성함과 연락처, 자녀의 현재 학년을 남겨 주시면 '
                                '확인 문자와 편입 준비 서류 안내를 보내 드리겠습니다.')],
 'refuse': [('입학 가능성을 말하지 않습니다.',
             '합격할지, 편입이 될지는 서류와 면접을 본 뒤 입학처가 정합니다. AI는 전형 절차와 일정만 말하고 &ldquo;어렵지 않겠죠&rdquo;에 답하지 않습니다.'),
            ('배정 학년과 반편성을 말하지 않습니다.',
             '몇 학년으로 들어가는지, 어느 레벨의 반인지는 평가 뒤 교사가 정합니다. 학부모의 설명을 듣고도 학년을 짐작해 말하지 않습니다.'),
            ('학생 안전에 관한 이야기는 바로 사람에게 넘깁니다.',
             '괴롭힘, 학대가 의심된다는 말, 아이가 다쳤다는 전화는 예약할 일이 아닙니다. 담당 선생님과 교감에게 즉시 연결하고 대화 전체를 남깁니다.'),
            ('재학생의 정보를 말하지 않습니다.',
             '특정 학생의 출결, 성적, 어느 반인지는 신원을 확인하지 않은 전화에 말하지 않습니다. 학교로 직접 오시라고 안내합니다.')],
 'fields': ['자녀 학년(현재 · 희망)과 편입 시기', '요금표에서 안내한 학비 · 입학금', '원서 마감과 전형 일정',
            '학교 투어 예약 시간', '통학버스 · 급식 · 방과후 문의 사항', '확인 문자 · 서류 안내 발송 기록'],
 'stages': ['문의 접수', '학교 투어 예약', '투어 · 원서 접수', '심사 · 면접', '입학 확정'],
 'lead': '등교 차량 줄에 서서 학부모가 겁니다. 학비와 원서 일정만 답하고, 합격 가능성은 말하지 않고 투어를 잡습니다.',
 'group': 1,
 'en': {
  'name': 'Schools & international schools', 'owner': 'the admissions office',
  'kicker': 'Private schools &middot; international schools &middot; admissions',
  'h1': 'Parents call at eight,<br>from the drop-off queue.',
  'sub': 'Admissions inquiries come at eight in the morning, from a parent in the car line with the child in the back seat. '
         'It is the moment the office is out at the gate and least able to pick up.',
  'cost': 'One enrolment is a five-figure fee every year for as long as the child stays, and a younger sibling often follows. '
          'Parents visit three schools and choose the one that answered. The eight-o&rsquo;clock call that rings out sits in '
          'the missed-call list, and the child ends up on another school&rsquo;s roll.',
  'call': [('Parent', '8:03 AM', 'I&rsquo;m asking about a mid-year transfer into Grade 3 next spring. What are the fees, and when do applications close?'),
           ('Saleringo', '+15 s', 'Grade 3 tuition is <b>$24,000 a year</b>, with a one-time enrolment fee of <b>$1,500</b>; bus and lunch are extra. '
                                  'Applications for the spring intake close on <b>November 30</b>, and after the file review there is a family interview in the <b>second week of December</b>.'),
           ('Parent', '8:04 AM', 'My daughter&rsquo;s English is strong. Grade 3 shouldn&rsquo;t be a problem for her, right?'),
           ('Saleringo', '+9 s', 'Admission and grade placement are decided by the admissions office after the assessment, so that isn&rsquo;t something I can speak to. '
                                 'On a school tour the admissions officer walks you through the process. There&rsquo;s a tour <b>this Thursday at 10:00 AM</b> and another <b>next Tuesday at 10:00 AM</b>.'),
           ('Parent', '8:05 AM', 'Thursday, please.'),
           ('Saleringo', '+7 s', 'Thursday at 10:00 AM, school tour &mdash; booked. Give me your name, a mobile number and your daughter&rsquo;s current grade, '
                                 'and I&rsquo;ll text the confirmation with the transfer document checklist.')],
  'refuse': [('It never says a child will get in.',
              'Whether a pupil is admitted is decided after the file review and the interview. The AI explains the process and the dates, and does not answer &ldquo;shouldn&rsquo;t be a problem, right?&rdquo;'),
             ('It never comments on placement.',
              'Which grade a child enters and which level of class is decided by teachers after the assessment. A parent&rsquo;s description of the child does not become a placement on the phone.'),
             ('It hands any safeguarding matter to a person at once.',
              'Bullying, a suspicion of abuse, or a child who has been hurt is not a booking. The AI connects the caller to the designated safeguarding lead immediately and keeps the whole conversation.'),
             ('It never gives out a pupil&rsquo;s information.',
              'Attendance, marks and which class a named child is in are not shared with an unverified caller. It asks them to come to the school in person.')],
  'fields': ['Child&rsquo;s current grade, grade applied for and intake', 'Tuition and fees quoted from the fee sheet',
             'Application deadline and assessment dates', 'School tour booked',
             'Bus, lunch and after-school questions', 'Confirmation and document checklist sent'],
  'stages': ['Inquiry', 'Tour booked', 'Tour and application', 'Assessment and interview', 'Enrolled'],
  'when': {'eyebrow': 'A call from the drop-off queue', 'h2': 'While the car line is moving,<br>this is how it goes.', 'tt': '8 AM', 'badge': 'office at the gate'},
  'lead': 'Parents call at eight from the car line. It gives the fees and the admissions calendar, books the tour, and never says whether a child will be admitted.',
  'room': 'not-a-trade',
  'room_d': 'The eight-o&rsquo;clock parent given tuition and the application deadline from your own sheet and booked onto Thursday&rsquo;s tour &mdash; with nothing said about whether the child will be admitted, and any safeguarding call handed to a person at once.',
  'room_no': ('0', 'admission odds or placement levels given on the phone'),
 },
},
{
 'slug': 'staffing', 'owner': '대표님', 'name': '인력파견 · 채용대행', 'photo': ph('PENDING'),
 'when': {'eyebrow': '퇴근 시간의 통화', 'h2': '담당자가 퇴근길에 있는 동안<br>이렇게 흘러갑니다.', 'tt': '오후 6시', 'badge': '사무실 마감 후'},
 'kicker': '인력파견 &middot; 채용대행 &middot; 아웃소싱',
 'h1': '내일 조가 비었다는 전화는<br>사무실이 닫힌 뒤에 옵니다.',
 'sub': '공장 관리자는 퇴근 전에 인원을 세다가 내일 라인에서 세 명이 빠진 것을 압니다. '
        '전화는 여섯 시에 오고, 영업 담당은 퇴근길이며, 먼저 받은 업체가 그 요청을 가져갑니다.',
 'cost': '세 명짜리 요청 하나가 일주일이면 수백만원의 청구이고, 한 번 채워 준 거래처는 라인이 빌 때마다 같은 곳에 겁니다. '
         '그 전화가 오는 시간은 담당자가 사무실을 나선 뒤이고, 받지 못한 요청은 다음 업체의 매출이 됩니다. '
         '놓친 요청은 어느 장부에도 적히지 않습니다.',
 'call': [('의뢰인', '6:12 PM', '내일 주간조 포장 라인에 세 명이 빠졌는데, 내일 아침까지 채워 줄 수 있어요?'),
          ('Saleringo', '+14초', '접수하겠습니다. 포장 · 단순조립 직종은 등록된 요율대로 <b>시급 1만 1천원에서 1만 2천 5백원</b> 사이이고, '
                                 '주간조 8시간 기준 한 분에 <b>일 9만 5천원 안팎</b>입니다. 근무지와 출근 시간을 알려 주시겠어요?'),
          ('의뢰인', '6:13 PM', '화성 공장이고 아침 8시요. 내일 세 명 확실히 오는 거죠?'),
          ('Saleringo', '+9초', '세 분을 다 채울 수 있을지는 담당자가 오늘 저녁 대기 인력을 확인하고 정하기 때문에 제가 충원을 약속드리지 않습니다. '
                                '화성 공장, 내일 8시, 포장 3명으로 접수했고, 담당자가 <b>오늘 8시 전</b>에 몇 명이 배정되는지 연락드립니다.'),
          ('의뢰인', '6:14 PM', '네, 빨리 부탁드려요.'),
          ('Saleringo', '+7초', '성함과 연락처, 현장 담당자 번호를 남겨 주시면 접수 확인 문자를 보내고 '
                                '담당자에게 지금 바로 넘기겠습니다.')],
 'refuse': [('충원을 약속하지 않습니다.',
             '내일 세 명이 나온다는 말은 대기 인력을 확인한 담당자만 할 수 있습니다. AI는 요청을 접수하고 요율대를 말할 뿐, 몇 명이 갈지는 사람의 회신으로 남깁니다.'),
            ('특정 근로자의 급여를 말하지 않습니다.',
             '누가 얼마를 받는지는 근로자와 회사 사이의 계약입니다. 의뢰처가 물어도 공개된 청구 요율대만 말합니다.'),
            ('근로자와 의뢰처의 분쟁을 판단하지 않습니다.',
             '무단결근, 현장 사고, 임금 문제로 오는 전화는 접수할 일이 아니라 즉시 담당자에게 넘길 일입니다. 어느 쪽 편도 들지 않습니다.'),
            ('파견이 되는 업무인지 법적으로 판단하지 않습니다.',
             '파견법상 허용 업무인지, 도급으로 가야 하는지는 담당자가 계약 단계에서 확인합니다. AI는 직종과 업무 내용을 받아 적기만 합니다.')],
 'fields': ['직종 · 필요 인원 · 근무 형태(주간 · 야간)', '근무지와 출근 일시', '요율표에서 안내한 시급 · 일당 범위',
            '안전화 · 자격 등 요구 조건', '담당자 배정과 배정 확정 인원', '접수 확인 문자 기록'],
 'stages': ['요청 접수', '인력 확인', '배정 확정', '출근 · 근태 관리', '정산'],
 'lead': '내일 조가 비면 오후 여섯 시에 겁니다. 직종과 인원, 날짜를 받아 적고 요율대만 말하며, 채울 수 있는지는 담당자가 답합니다.',
 'group': 5,
 'en': {
  'name': 'Staffing & recruitment agencies', 'owner': 'the branch manager',
  'kicker': 'Staffing &middot; temp labour &middot; recruitment',
  'h1': 'The shift is short at six,<br>and the branch closed at five.',
  'sub': 'A plant manager counts heads at the end of the day and finds three missing from tomorrow&rsquo;s line. '
         'The call comes at six, the recruiters have gone home, and the agency that answers gets the order.',
  'cost': 'A three-head order for a week is a few thousand dollars of billings, and the client who gets filled once calls the same '
          'agency every time the line is short. The call comes after the recruiters have left the building, and the order nobody '
          'answered becomes the next agency&rsquo;s revenue. No branch counts the orders it never took.',
  'call': [('Client', '6:12 PM', 'Three people dropped off my packing line for tomorrow&rsquo;s day shift. Can you fill it by morning?'),
           ('Saleringo', '+14 s', 'I&rsquo;ll take the order. Packing and light assembly bill in the published band of <b>$21 to $24 an hour</b>, '
                                  'so a full day shift is around <b>$180 per worker</b>. Where is the site and what time do they start?'),
           ('Client', '6:13 PM', 'The Riverside plant, eight AM. I&rsquo;ll definitely have three tomorrow, right?'),
           ('Saleringo', '+9 s', 'Whether all three can be filled is decided by the branch manager tonight, from who is on the bench, so I don&rsquo;t guarantee a fill. '
                                 'I&rsquo;ve logged Riverside, 8:00 AM tomorrow, three packers, and the manager calls you <b>before 8:00 PM</b> with how many are assigned.'),
           ('Client', '6:14 PM', 'Fine, but please be quick.'),
           ('Saleringo', '+7 s', 'Give me your name, a mobile number and the on-site supervisor&rsquo;s number, and I&rsquo;ll text the order confirmation '
                                 'and put this in front of the manager right now.')],
  'refuse': [('It never guarantees a fill.',
              'Only a recruiter who has looked at the bench can say three people will turn up tomorrow. The AI logs the order and quotes the band, and leaves the headcount to a person&rsquo;s reply.'),
             ('It never discusses what a worker is paid.',
              'A worker&rsquo;s wage is between the worker and the agency. Asked by a client, it states only the published bill-rate band.'),
             ('It never rules on a dispute.',
              'A no-show, an injury on site or a wage complaint is not an order to log; it goes to a person at once. The AI takes no side.'),
             ('It never decides the contract form.',
              'Whether a role can be filled as temp, contract-to-hire or direct placement, and what co-employment obligations follow, is confirmed by the branch manager at contract stage. The AI records the role and the duties.')],
  'fields': ['Role, headcount and shift', 'Site and start time', 'Bill-rate band quoted from the rate card',
             'Safety boots, certifications and other requirements', 'Recruiter assigned and heads confirmed', 'Order confirmation text sent'],
  'stages': ['Order taken', 'Bench checked', 'Heads confirmed', 'On shift and timekeeping', 'Invoiced'],
  'when': {'eyebrow': 'A call at six, an hour after the branch closed', 'h2': 'While the recruiters are on the motorway home,<br>this is how it goes.', 'tt': '6 PM', 'badge': 'branch closed'},
  'lead': 'A short line is discovered at six. It takes the role, headcount and date, quotes the published band, and leaves whether it can be filled to the manager.',
  'room': 'professional-public',
  'room_d': 'The six-o&rsquo;clock plant manager&rsquo;s three-packer order logged with the published bill band and put in front of the branch manager &mdash; with no fill guaranteed and no worker&rsquo;s pay discussed.',
  'room_no': ('0', 'fills guaranteed before anyone has checked the bench'),
 },
},
{
 'slug': 'imaging', 'owner': '원장님', 'name': '영상의학 · 건강검진센터', 'photo': ph('PENDING'),
 'when': {'eyebrow': '의뢰서를 든 아침의 통화', 'h2': '첫 검사가 돌아가는 동안<br>이렇게 흘러갑니다.', 'tt': '오전 8시 30분', 'badge': '접수처 대기 줄'},
 'kicker': '영상의학과 &middot; MRI &middot; CT &middot; 건강검진',
 'h1': '의뢰서를 받은 환자는<br>아침 여덟 시 반에 겁니다.',
 'sub': '진료실을 나오며 의뢰서 한 장과 걱정 하나를 들고 바로 전화합니다. '
        '첫 검사가 이미 돌아가고 있고, 접수처에는 줄이 서 있는 시간입니다.',
 'cost': 'MRI 한 건은 비급여 45만원이고, 비어 있는 장비 시간은 건물 안에서 가장 비싼 시간입니다. '
         '부재중을 만난 환자는 의뢰서에 적힌 다음 센터에 걸고, 그 병원의 의뢰는 다음부터 거기로 갑니다. '
         '빈 슬롯은 어느 장부에도 손실로 적히지 않습니다.',
 'call': [('환자', '8:31 AM', '정형외과에서 허리 MRI 찍으라고 의뢰서를 받았는데요, 오늘 오후에 되나요? 비용은요?'),
          ('Saleringo', '+16초', '요추 MRI는 오늘 <b>오후 2시 40분</b>과 <b>4시 20분</b>에 자리가 있습니다. 비급여로 하시면 <b>45만원</b>이고, '
                                 '의뢰서에 급여 사유가 적혀 있으면 접수 때 건강보험 적용 여부를 확인해 드립니다. 검사는 <b>30분</b> 정도 걸리고 금식은 필요 없습니다.'),
          ('환자', '8:32 AM', '다른 데서 찍은 엑스레이도 있는데, 그거 보고 어떤지 좀 알려 주실 수 있어요? MRI를 꼭 찍어야 하나요?'),
          ('Saleringo', '+9초', '영상을 읽거나 검사가 필요한지 말씀드리는 것은 의사만 할 수 있어서 제가 답하지 않습니다. 의뢰서와 이전 영상 CD를 '
                                '가져오시면 판독 때 함께 봅니다. 2시 40분으로 잡아 드릴까요?'),
          ('환자', '8:33 AM', '네, 2시 40분요.'),
          ('Saleringo', '+7초', '오늘 오후 2시 40분 요추 MRI로 접수했습니다. 성함과 생년월일, 연락처를 남겨 주시면 확인 문자와 준비 안내를 보내 드립니다. '
                                '몸 안에 금속이나 심장 박동기가 있으시면 접수 때 꼭 말씀해 주세요.')],
 'refuse': [('결과를 읽지 않습니다.',
             '판독이 나왔는지, 뭐라고 쓰여 있는지는 의사가 설명합니다. 전화로 결과를 말하는 것은 의료법 위반이고, AI는 &ldquo;의뢰하신 병원에서 설명드립니다&rdquo;로 멈춥니다.'),
            ('검사가 필요한지 말하지 않습니다.',
             '의뢰서에 적힌 검사만 접수합니다. MRI 대신 CT가 낫다거나 안 찍어도 된다는 말은 임상의의 판단이지 접수의 판단이 아닙니다.'),
            ('준비 안내는 원장님이 적어 둔 문장 그대로만 읽습니다.',
             '금식 시간, 조영제, 체내 금속 여부는 시트의 문장으로만 말합니다. 조영제 부작용 이력, 신장 질환, 임신 가능성이 나오면 예약을 멈추고 사람에게 넘깁니다.'),
            ('급여인지 비급여인지 전화로 가르지 않습니다.',
             '건강보험 적용은 의뢰서의 사유와 조건에 따라 갈립니다. 비급여 정가만 말하고, 적용 여부는 접수 때 확인하는 것으로 남깁니다.')],
 'fields': ['의뢰서의 검사 항목과 부위', '의뢰 병원 · 진료과', '요금표에서 안내한 비급여 금액과 급여 확인 여부',
            '검사 예약 시간과 소요 시간', '금식 · 조영제 · 체내 금속 등 확인 사항', '확인 문자 · 준비 안내 발송 기록'],
 'stages': ['문의 접수', '검사 예약', '접수 · 검사', '판독', '결과 전달 · 의뢰 병원 회신'],
 'lead': '의뢰서를 들고 아침 여덟 시 반에 겁니다. 시간표에서 검사만 잡고, 결과를 읽거나 검사가 필요한지는 한마디도 하지 않습니다.',
 'group': 0,
 'en': {
  'name': 'Imaging & health-screening centers', 'owner': 'the centre manager',
  'kicker': 'Imaging &middot; MRI and CT &middot; health screening',
  'h1': 'The patient calls at 8:30,<br>holding a referral.',
  'sub': 'Referral calls come first thing, from a patient who left the surgery with a form and a worry. '
         'The scanner is already running and the front desk has a queue.',
  'cost': 'An MRI is a four-hundred-and-fifty-dollar self-pay ticket, and a scanner sitting idle is the most expensive minute in the building. '
          'The patient who reaches voicemail calls the next centre on the referral, and that practice&rsquo;s referrals follow. '
          'An empty slot is never written down as a loss.',
  'call': [('Patient', '8:31 AM', 'My orthopaedist gave me a referral for a lumbar MRI. Can you do it this afternoon, and what does it cost?'),
           ('Saleringo', '+16 s', 'For a lumbar MRI I have <b>2:40 PM</b> and <b>4:20 PM</b> today. If you&rsquo;re paying yourself the scan is <b>$450</b>; if it&rsquo;s going '
                                  'through insurance, the desk confirms the authorisation at check-in. It takes about <b>thirty minutes</b>, and you don&rsquo;t need to fast.'),
           ('Patient', '8:32 AM', 'I&rsquo;ve got an X-ray from another clinic. Can you tell me what it shows? And do I really need the MRI?'),
           ('Saleringo', '+9 s', 'Reading an image or saying whether a scan is needed is for a doctor, so I won&rsquo;t answer that. Bring the referral and the X-ray disc '
                                 'and the radiologist reads them together. Shall I book 2:40 PM?'),
           ('Patient', '8:33 AM', 'Yes, 2:40.'),
           ('Saleringo', '+7 s', 'Today at 2:40 PM, lumbar MRI &mdash; booked. Give me your name, date of birth and mobile number and I&rsquo;ll text the confirmation '
                                 'and the preparation notes. If you have any metal implants or a pacemaker, please tell the desk at check-in.')],
  'refuse': [('It never reads a result.',
              'Whether the report is out and what it says is for a doctor to explain. The AI stops at &ldquo;your referring doctor will take you through it&rdquo;.'),
             ('It never says whether a scan is necessary.',
              'It books what is written on the referral. Suggesting a CT instead, or that the scan can be skipped, is a clinician&rsquo;s judgement, not the desk&rsquo;s.'),
             ('It reads preparation instructions only as written.',
              'Fasting, contrast and metal implants are explained in the sentences on the sheet and no further. A contrast reaction in the past, kidney disease or a possible pregnancy stops the booking and goes to a person.'),
             ('It never rules on coverage.',
              'Whether insurance pays depends on the referral and the plan. It quotes the self-pay price and leaves authorisation to the desk at check-in.')],
  'fields': ['Scan and body part on the referral', 'Referring practice and clinician', 'Self-pay price quoted and insurance status',
             'Appointment time and scan duration', 'Fasting, contrast, implants and anything flagged', 'Confirmation and preparation notes sent'],
  'stages': ['Inquiry', 'Scan booked', 'Check-in and scan', 'Reported', 'Results to the referrer'],
  'when': {'eyebrow': 'A call while the first scan is running', 'h2': 'While the front desk has a queue,<br>this is how it goes.', 'tt': '8:30 AM', 'badge': 'scanner running'},
  'lead': 'Patients call at 8:30 with a referral in hand. It books from the timetable and quotes the self-pay price, and says nothing about what a scan shows or whether one is needed.',
  'room': 'health-care',
  'room_d': 'The 8:30 AM referral booked into the afternoon MRI slot at the self-pay list price &mdash; with the old X-ray and the &ldquo;do I really need this&rdquo; question left to the radiologist.',
  'room_no': ('0', 'scan results read out by phone'),
 },
},
]
