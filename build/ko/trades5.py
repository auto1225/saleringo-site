# -*- coding: utf-8 -*-
"""열 개 업종 추가 — 다섯 번째 묶음.

세차 · 자동차 딜러 · 견인, 카페 · 케이터링 · 여행사, 사진관 · 꽃집, 세무 · 보험.
각 항목의 'en' 은 영문 사이트용이며 번역이 아니라 그 나라의 통화로 다시 쓴 것이다.
'group' 은 build/ko/p_trades.py 의 GROUPS 인덱스, 'en.room' 은 en/industries.html 의 방 id.
"""

PH = 'https://images.pexels.com/photos/%s/pexels-photo-%s.jpeg'


def ph(i):
    return PH % (i, i)


TRADES5 = [
{
 'slug': 'car-wash', 'owner': '사장님', 'name': '세차 · 디테일링', 'photo': ph('PENDING'),
 'when': {'eyebrow': '폴리셔를 든 동안의 통화', 'h2': '베이 안에 있는 동안<br>이렇게 흘러갑니다.', 'tt': '디테일링 중', 'badge': '장갑 벗을 수 없는 시간'},
 'kicker': '세차 &middot; 디테일링 &middot; 코팅',
 'h1': '폴리셔 소리에<br>전화벨은 묻힙니다.',
 'sub': '디테일링 문의는 토요일 오전에 오고, 토요일 오전은 베이가 다 찬 시간입니다. '
        '한 대에 네 시간이 걸리는 일을 하면서 벨 소리를 듣는 사람은 없습니다.',
 'cost': '디테일링 한 건은 30만원 안팎이고, 한 번 맡긴 손님은 계절마다 세차를 하러 옵니다. '
         '그 전화는 베이가 가장 시끄럽고 장갑이 가장 더러운 시간에 옵니다. 부재중으로 남은 손님은 '
         '길 건너 세차장에 예약하고, 그 뒤로도 거기로 갑니다. 들어오지 않은 30만원은 매출표 어디에도 없습니다.',
 'call': [('고객', '10:12 AM', '중형 SUV인데 실내 클리닝이랑 광택 같이 하면 얼마예요? 오늘 오후에 가능한가요?'),
          ('Saleringo', '+19초', 'SUV 기준 실내 클리닝은 <b>12만원</b>, 외부 광택은 <b>18만원</b>이고 둘을 같이 하시면 '
                                 '<b>27만원</b>입니다. 오늘은 <b>오후 3시</b>에 베이가 하나 비어 있고, 두 가지 모두 하면 '
                                 '<b>4시간</b> 걸립니다.'),
          ('고객', '10:13 AM', '시트에 커피 자국이 있는데 완전히 지워지나요?'),
          ('Saleringo', '+8초', '얼룩은 소재와 묵은 정도에 따라 달라서 보고 말씀드려야 정확합니다. 입고하시면 사장님이 '
                                '시트를 먼저 확인하고 어느 정도 될지 안내드립니다. 오후 3시로 잡아 드릴까요?'),
          ('고객', '10:14 AM', '네, 그렇게 해 주세요. 차는 흰색 쏘렌토예요.'),
          ('Saleringo', '+7초', '오늘 오후 3시, 흰색 쏘렌토, 실내 클리닝과 광택으로 접수했습니다. '
                                '성함과 연락처 남겨 주시면 확인 문자 드리겠습니다.')],
 'refuse': [('얼룩과 흠집의 결과를 약속하지 않습니다.',
             '커피 자국이 다 지워지는지, 기스가 광택으로 없어지는지는 소재와 깊이를 봐야 압니다. '
             '입고 후 사장님이 확인하고 안내하는 것으로 남깁니다.'),
            ('없는 패키지 가격을 만들지 않습니다.',
             '사장님이 넣어 둔 차종별 요금표의 조합만 말합니다. 표에 없는 조합은 &ldquo;입고 후 견적&rdquo;으로 넘깁니다.'),
            ('베이가 찬 시간에 접수하지 않습니다.',
             '차 한 대가 네 시간을 차지하는 일입니다. 캘린더에 빈 베이가 있을 때만 잡고, 겹치면 다음 빈 시간을 제시합니다.'),
            ('도장 손상의 책임을 전화로 가리지 않습니다.',
             '기존 흠집과 작업 중 생긴 것을 구분하는 일은 입고 사진과 사장님의 확인으로만 합니다. '
             '보상을 약속하지도, 부인하지도 않습니다.')],
 'fields': ['차종 · 색상 · 번호판 뒷자리', '문의한 서비스와 요금표 조합', '얼룩 · 흠집 등 확인 요청 사항',
            '입고 시간과 예상 소요 시간', '대기 · 픽업 · 탁송 여부', '확인 문자 발송 기록'],
 'stages': ['문의 접수', '입고 예약', '입고 · 상태 확인', '작업', '출고 · 재방문 안내'],
 'lead': '폴리셔를 들고 있으면 전화를 못 받습니다. 요금표의 조합만 말하고, 얼룩이 지워질지는 보고 답하도록 남깁니다.',
 'group': 3,
 'en': {
  'name': 'Car wash & detailing', 'owner': 'the owner',
  'kicker': 'Car wash &middot; detailing &middot; ceramic coating',
  'h1': 'The phone rings while<br>both hands are on the polisher.',
  'sub': 'Detailing customers call on Saturday morning, and Saturday morning is when every bay is full. '
         'A detail takes four hours; a missed call takes four seconds.',
  'cost': 'A detail is a four-hundred-dollar ticket, and the customer who books one comes back every season '
          'for a wash. The call lands when the bay is loudest and the gloves are dirtiest, and the customer '
          'who gets voicemail books the shop across the road. Nothing in the till shows the ticket that never arrived.',
  'call': [('Customer', '10:12 AM', 'Mid-size SUV &mdash; how much for an interior detail plus an exterior polish, and can you do it this afternoon?'),
           ('Saleringo', '+19 s', 'For an SUV the interior detail is <b>$180</b>, the exterior polish is <b>$260</b>, and together '
                                  'they are <b>$400</b>. This afternoon I have a bay free at <b>3:00 PM</b>, and both together take about <b>four hours</b>.'),
           ('Customer', '10:13 AM', 'There&rsquo;s a coffee stain on the passenger seat. Will it come out completely?'),
           ('Saleringo', '+8 s', 'That depends on the fabric and how long it has set, so it needs to be seen. When the car comes in, '
                                 'the owner checks the seat first and tells you what to expect. Shall I hold 3:00 PM?'),
           ('Customer', '10:14 AM', 'Yes, please. It&rsquo;s a white Sorento.'),
           ('Saleringo', '+7 s', 'Booked: today at 3:00 PM, white Sorento, interior detail and polish. '
                                 'If you give me your name and mobile number I will text the confirmation.')],
  'refuse': [('It never promises a stain or a scratch will disappear.',
              'Whether coffee comes out of a seat or a swirl polishes away depends on the material and the depth. '
              'The AI books the car in and leaves the verdict to the owner&rsquo;s inspection.'),
             ('It never invents a package price.',
              'It quotes only the combinations on the owner&rsquo;s per-vehicle price list. Anything not on the list is '
              'written up as &ldquo;quote on arrival&rdquo;.'),
             ('It never books into a bay that is already taken.',
              'One car occupies a bay for four hours. It books only where the calendar shows a free bay and offers the next open slot otherwise.'),
             ('It never rules on paint damage.',
              'Telling an old chip from a new one is done with the check-in photos and the owner, not on the phone. '
              'The AI neither promises compensation nor denies it.')],
  'fields': ['Vehicle, colour and last digits of the plate', 'Service asked for and the price-list combination',
             'Stains, scratches and anything to inspect', 'Drop-off time and estimated duration',
             'Wait, pick-up or collection', 'Confirmation text sent'],
  'stages': ['Enquiry', 'Drop-off booked', 'Check-in and inspection', 'In the bay', 'Collected and rebooked'],
  'when': {'eyebrow': 'A call from inside the bay', 'h2': 'While the polisher is running,<br>this is how it goes.', 'tt': 'mid-detail', 'badge': 'gloves on'},
  'lead': 'Nobody hears the phone over the polisher. It quotes the combinations on your price list and leaves whether the stain comes out to your inspection.',
  'room': 'vehicle-plant-storage',
  'room_d': 'The Saturday-morning SUV quoted off your own per-vehicle list and a bay held for 3:00 PM &mdash; and never a promise that the coffee stain will come out.',
  'room_no': ('0', 'stains promised gone before the owner has seen the seat'),
 },
},
{
 'slug': 'car-dealers', 'owner': '대표님', 'name': '자동차 딜러', 'photo': ph('PENDING'),
 'when': {'eyebrow': '전시장 문 닫은 뒤의 통화', 'h2': '매물을 밤에 보는 동안<br>이렇게 흘러갑니다.', 'tt': '전시장 마감 후', 'badge': '딜러 퇴근 후'},
 'kicker': '자동차 딜러 &middot; 중고차 &middot; 전시장',
 'h1': '매물은 전시장이 닫힌 뒤에<br>검색됩니다.',
 'sub': '밤 열 시에 매물 페이지를 보다가 바로 전화를 겁니다. '
        '아홉 시부터 여섯 시까지만 받는 전시장은 손님의 절반을 부재중으로 만납니다.',
 'cost': '중고차 문의 한 통은 차 한 대의 마진에 할부와 보상 판매까지 붙은 금액이고, 사람들이 매물을 볼 시간이 나는 '
         '퇴근 뒤에 옵니다. 부재중을 만난 손님은 다음 매물을 누릅니다. 잡지 못한 방문 약속을 세는 전시장은 없습니다.',
 'call': [('고객', '9:47 PM', '홈페이지에 있는 2022년식 그랜저 아직 있나요? 할부로 하면 월 얼마 정도예요?'),
          ('Saleringo', '+22초', '2022년식 그랜저 흰색, <b>3만 8천 km</b>, 표시 가격 <b>2,890만원</b>은 오늘 기준 아직 판매 중입니다. '
                                 '할부 조건은 신용과 기간에 따라 달라서 제가 월 납입액을 말씀드릴 수 없고, '
                                 '담당 딜러가 상담에서 직접 계산해 드립니다.'),
          ('고객', '9:49 PM', '지금 타는 차 팔면 얼마 받을 수 있어요? 2018년 아반떼예요.'),
          ('Saleringo', '+9초', '보상 판매 금액은 차를 직접 보고 정하는 것이라 전화로는 말씀드리지 않습니다. 방문하실 때 아반떼를 '
                                '같이 가져오시면 그 자리에서 평가해 드립니다. <b>내일 오후 2시</b>와 <b>모레 오전 11시</b>가 비어 있습니다.'),
          ('고객', '9:50 PM', '내일 2시요.'),
          ('Saleringo', '+7초', '내일 오후 2시, 그랜저 시승과 아반떼 평가로 잡아 두었습니다. 성함과 연락처 남겨 주시면 '
                                '확인 문자를 보내고, 담당 딜러가 아침에 한 번 연락드립니다.')],
 'refuse': [('할부 조건과 월 납입액을 말하지 않습니다.',
             '금리와 기간, 심사 결과에 따라 달라지는 것을 전화로 계산해 주면 그 숫자가 약속이 됩니다. '
             '담당 딜러가 상담에서 직접 계산합니다.'),
            ('보상 판매 금액을 부르지 않습니다.',
             '타던 차의 값은 실차를 보고 정합니다. 방문 때 함께 가져오시라고 안내하고, 평가는 사람이 합니다.'),
            ('가격 협상을 하지 않습니다.',
             '표시 가격과 등록된 프로모션만 말합니다. 깎아 드리겠다는 말은 딜러의 권한이고 AI의 권한이 아닙니다.'),
            ('팔린 차를 팔지 않습니다.',
             '재고 목록에 판매 중으로 남아 있는 매물만 안내합니다. 목록에 없으면 &ldquo;확인 후 연락&rdquo;으로 남깁니다.')],
 'fields': ['문의 매물(연식 · 모델 · 재고 번호)', '신차 · 중고 · 보상 판매 구분', '타던 차 정보(연식 · 모델)',
            '할부 · 리스 문의 여부', '시승 · 방문 예약 시간', '담당 딜러 배정'],
 'stages': ['문의 접수', '방문 · 시승 예약', '시승 · 차량 평가', '견적 · 상담', '계약 · 출고'],
 'lead': '매물은 밤에 봅니다. 재고에 있는 차만 안내하고, 할부 조건과 보상 판매 금액은 말하지 않고 방문을 잡습니다.',
 'group': 3,
 'en': {
  'name': 'Car dealerships', 'owner': 'the dealer principal',
  'kicker': 'Car dealerships &middot; used cars &middot; showrooms',
  'h1': 'Buyers browse the lot online<br>after the showroom locks up.',
  'sub': 'The listing is read at ten at night and the call is made straight away. '
         'A dealership that only answers between nine and six meets half its buyers on voicemail.',
  'cost': 'A used-car enquiry is worth the gross on the car plus the finance and the part-exchange behind it, and it '
          'arrives after hours because that is when people have time to look. The buyer who reaches voicemail clicks '
          'the next listing. No dealership counts the appointments it never took.',
  'call': [('Customer', '9:47 PM', 'Is the 2022 Camry on your site still available? And roughly what would it be a month on finance?'),
           ('Saleringo', '+22 s', 'The 2022 Camry in white, <b>24,000 miles</b>, listed at <b>$26,900</b>, is still for sale as of today. '
                                  'Finance depends on your credit and the term, so I cannot give you a monthly figure &mdash; '
                                  'the sales consultant works it out with you at the appointment.'),
           ('Customer', '9:49 PM', 'What would you give me for my 2018 Elantra as a trade-in?'),
           ('Saleringo', '+9 s', 'A trade-in value is set by looking at the car, so I do not give one over the phone. Bring the Elantra '
                                 'with you and it is appraised on the spot. I have <b>tomorrow at 2:00 PM</b> or <b>Thursday at 11:00 AM</b>.'),
           ('Customer', '9:50 PM', 'Tomorrow at two.'),
           ('Saleringo', '+7 s', 'Tomorrow at 2:00 PM, test drive of the Camry and appraisal of the Elantra &mdash; held. Give me your name '
                                 'and mobile number and I will text the confirmation; the consultant calls you in the morning.')],
  'refuse': [('It never states finance terms or a monthly payment.',
              'Rate, term and approval change the number, and a figure given on the phone becomes a promise. '
              'The sales consultant runs it at the desk.'),
             ('It never names a trade-in value.',
              'What the old car is worth is decided by the appraiser with the car in front of them. The AI asks the buyer to bring it along.'),
             ('It never negotiates.',
              'It states the listed price and the promotions the principal has loaded. Discounting is the consultant&rsquo;s authority, not the AI&rsquo;s.'),
             ('It never sells a car that has already gone.',
              'It offers only vehicles still marked available in the inventory feed. Anything else is logged as &ldquo;check and call back&rdquo;.')],
  'fields': ['Vehicle enquired about (year, model, stock number)', 'New, used or trade-in', 'Current car (year and model)',
             'Finance or lease interest', 'Test-drive appointment', 'Consultant assigned'],
  'stages': ['Enquiry', 'Appointment booked', 'Test drive and appraisal', 'Quote and consultation', 'Contract and delivery'],
  'when': {'eyebrow': 'A call after the showroom closes', 'h2': 'While the lot is browsed from a sofa,<br>this is how it goes.', 'tt': 'after closing', 'badge': 'sales floor dark'},
  'lead': 'Listings are read at night. It offers only cars still in stock and books the visit without a finance figure or a trade-in value.',
  'room': 'vehicle-plant-storage',
  'room_d': 'The 9:47 PM listing enquiry checked against live stock and a test drive booked for two &mdash; with no monthly payment and no trade-in figure given.',
  'room_no': ('0', 'finance terms or trade-in values quoted on the phone'),
 },
},
{
 'slug': 'towing', 'owner': '사장님', 'name': '견인 · 긴급출동', 'photo': ph('PENDING'),
 'when': {'eyebrow': '새벽 갓길의 통화', 'h2': '기사가 다른 현장에 있는 동안<br>이렇게 흘러갑니다.', 'tt': '새벽 2시', 'badge': '전원 출동 중'},
 'kicker': '견인 &middot; 긴급출동 &middot; 로드서비스',
 'h1': '고속도로에서 터진 타이어는<br>영업시간을 기다리지 않습니다.',
 'sub': '견인 전화는 거는 사람에게 전부 응급입니다. 배차 담당은 다른 현장에 있고, '
        '벨이 울리다 끊기면 갓길의 운전자는 목록의 다음 업체에 겁니다.',
 'cost': '로드서비스는 먼저 받는 곳이 가져갑니다. 다음 업체로 넘어간 견인 한 건은 10만원이 넘고, 통화 연결이 안 된 '
         '기록이 쌓이면 보험사 협력 순번에서 빠집니다. 더 나쁜 것은, 주행 차로에 선 차의 전화가 끊기는 일은 '
         '매출 문제 이전에 안전 문제라는 점입니다.',
 'call': [('고객', '2:13 AM', '고속도로에서 타이어가 터졌어요. 차가 갓길에 서 있는데 견인 되나요?'),
          ('Saleringo', '+6초', '먼저 안전부터 확인하겠습니다. 다치신 분은 없으신가요? 차가 주행 차로 밖으로 완전히 나와 있고, '
                                '지금 차 밖 가드레일 뒤에 계신가요?'),
          ('고객', '2:13 AM', '다친 사람은 없고요, 차는 갓길에 다 붙였어요. 저는 밖에 나와 있어요. '
                              '경부고속도로 서울 방향 안성휴게소 지나서예요.'),
          ('Saleringo', '+9초', '경부선 서울 방향 안성휴게소 지난 지점, 갓길 정차, 부상 없음으로 접수했습니다. 당직 기사가 지금 출발해서 '
                                '<b>35분 안</b>에 도착합니다. 야간 고속도로 견인은 <b>기본 9만원</b>에 10km 초과분 <b>km당 2천원</b>이고, '
                                '정비소까지 거리는 기사가 현장에서 확인해 정산합니다.'),
          ('고객', '2:15 AM', '스페어 타이어로 갈아 주면 안 되나요? 얼마예요?'),
          ('Saleringo', '+8초', '스페어로 교체가 되는지는 기사가 현장에서 타이어와 휠을 보고 판단합니다. 전화로 수리 여부나 금액을 '
                                '정하지 않습니다. 성함과 연락처 남겨 주시면 기사 번호와 도착 예정 문자를 지금 보내 드리겠습니다.')],
 'refuse': [('위치와 안전을 묻기 전에는 아무것도 하지 않습니다.',
             '부상 여부, 차가 주행 차로에 걸쳐 있는지, 사람이 차 밖에 있는지를 먼저 묻습니다. 주행 차로에 서 있거나 '
             '다친 사람이 있으면 112와 당직 기사에게 동시에 연결합니다.'),
            ('현장을 보지 않고 수리를 말하지 않습니다.',
             '스페어 교체가 되는지, 점프로 시동이 걸릴지는 기사가 봐야 압니다. 전화로 수리 여부와 금액을 정하지 않습니다.'),
            ('출동 순번을 임의로 바꾸지 않습니다.',
             '당직표에 있는 기사에게 순서대로 배차합니다. 특정 기사를 지목하거나 다른 현장에서 빼 오지 않습니다.'),
            ('보험 처리 여부를 단정하지 않습니다.',
             '고객 보험의 긴급출동 특약에 해당하는지는 보험사가 정합니다. 접수 번호와 현장 사진만 남깁니다.')],
 'fields': ['현장 위치(도로 · 방향 · 기준점)', '부상 여부와 차량 위치(갓길 · 주행 차로)', '차종과 고장 유형',
            '배차된 기사와 출발 · 도착 예정 시간', '기본 요금과 거리 요율', '보험 긴급출동 접수 번호'],
 'stages': ['접수 · 안전 확인', '배차', '현장 도착', '견인 · 인도', '정산'],
 'lead': '새벽 두 시 갓길의 전화입니다. 부상과 위치를 먼저 묻고 당직표에서 배차하며, 수리 여부는 현장의 기사에게 맡깁니다.',
 'group': 3,
 'en': {
  'name': 'Towing & roadside', 'owner': 'the owner',
  'kicker': 'Towing &middot; roadside assistance &middot; recovery',
  'h1': 'A blown tyre on the interstate<br>does not wait for office hours.',
  'sub': 'Every recovery call is urgent to the person making it. The dispatcher is on another job, the phone rings out, '
         'and the driver on the shoulder calls the next name on the list.',
  'cost': 'Roadside work is won by whoever answers first. A tow that goes to the next operator is a hundred and fifty dollars '
          'gone, and the motor club that logs your unanswered calls drops you from the rota. Worse, a call that rings out '
          'from a live lane is a safety problem before it is a revenue one.',
  'call': [('Customer', '2:13 AM', 'I blew a tyre on the interstate. The car is on the shoulder &mdash; can you tow it?'),
           ('Saleringo', '+6 s', 'Safety first. Is anyone hurt? Is the car fully off the travel lane, and are you out of the vehicle and behind the barrier?'),
           ('Customer', '2:13 AM', 'Nobody is hurt, the car is right over on the shoulder and I am out behind the rail. I-95 northbound, just past exit 42.'),
           ('Saleringo', '+9 s', 'Logged: I-95 northbound past exit 42, on the shoulder, no injuries. The duty driver is leaving now and will be '
                                 'with you in <b>under 35 minutes</b>. A night interstate tow is <b>$95 hook-up</b> plus <b>$4 a mile</b> after '
                                 'the first ten, and the driver confirms the distance to the shop on site.'),
           ('Customer', '2:15 AM', 'Could he just put the spare on instead? What does that cost?'),
           ('Saleringo', '+8 s', 'Whether the spare can go on is the driver&rsquo;s call once he has seen the tyre and the wheel &mdash; I do not '
                                 'decide repairs or quote them by phone. Give me your name and mobile number and I will text you the driver&rsquo;s number and his ETA now.')],
  'refuse': [('It does nothing before it has the location and the safety picture.',
              'Injuries, whether the car is in a live lane and whether the people are out of it come first. A live-lane stop or '
              'an injury is put through to 911 and the duty driver at the same moment.'),
             ('It never diagnoses a repair from the phone.',
              'Whether a spare will fit or a jump will take is decided by the driver at the scene. No repair is agreed or priced by the AI.'),
             ('It never reorders the rota.',
              'Jobs go to the duty driver in the order the rota says. It does not pick favourites or pull a driver off another scene.'),
             ('It never says the insurer will pay.',
              'Whether the call falls under a motor club or a policy is the insurer&rsquo;s decision. The AI records the claim reference and the scene photos.')],
  'fields': ['Location (road, direction, landmark)', 'Injuries and vehicle position (shoulder or live lane)', 'Vehicle and fault type',
             'Driver dispatched, departure and ETA', 'Hook-up fee and mileage rate', 'Insurer or motor-club reference'],
  'stages': ['Logged and safety-checked', 'Dispatched', 'On scene', 'Towed and delivered', 'Settled'],
  'when': {'eyebrow': 'A call from the hard shoulder', 'h2': 'While every truck is out,<br>this is how it goes.', 'tt': '2:13 AM', 'badge': 'all drivers on scene'},
  'lead': 'Two in the morning on the shoulder. It asks about injuries and position first, dispatches off the rota, and leaves the repair verdict to the driver on scene.',
  'room': 'vehicle-plant-storage',
  'room_d': 'The 2:13 AM shoulder call: injuries and lane position asked before anything else, the duty driver dispatched off the rota with an ETA &mdash; and no repair diagnosed by phone.',
  'room_no': ('0', 'repairs diagnosed or priced before a driver reaches the scene'),
 },
},
{
 'slug': 'cafes-bakeries', 'owner': '사장님', 'name': '카페 · 베이커리', 'photo': ph('PENDING'),
 'when': {'eyebrow': '오픈 러시의 통화', 'h2': '에스프레소 머신 앞에 있는 동안<br>이렇게 흘러갑니다.', 'tt': '오전 8시', 'badge': '줄이 문밖까지'},
 'kicker': '카페 &middot; 베이커리 &middot; 주문 케이크',
 'h1': '케이크 주문은 여덟 시,<br>커피 줄 한가운데서 옵니다.',
 'sub': '돌 케이크는 출근길에 주문되고, 출근길은 가게가 가장 바쁜 한 시간입니다. '
        '바리스타는 전화를 들 수 없고, 주문 케이크는 문자 두 줄로 끝나는 주문이 아닙니다.',
 'cost': '주문 케이크 하나는 5만원에서 10만원이고, 그 뒤에 돌잔치 답례품과 회사 납품, 단골이 따라옵니다. 주문 전화는 '
         '줄이 문밖까지 섰고 전화기가 우유 피처 밑에 깔린 시간에 옵니다. 답을 못 들은 손님은 두 집 건너 빵집에 '
         '주문하고, 내년에도 거기에 합니다.',
 'call': [('고객', '8:04 AM', '토요일에 돌잔치 케이크 주문하려고요. 2호 사이즈 되나요?'),
          ('Saleringo', '+16초', '토요일 주문 가능합니다. 2호 생크림 케이크는 <b>4만 8천원</b>, 레터링은 <b>5천원</b> 추가이고, '
                                 '픽업은 오전 10시부터입니다. 문구와 색상만 정해 주시면 됩니다.'),
          ('고객', '8:05 AM', '문구는 &ldquo;서준아 첫 생일 축하해&rdquo;로 하고, 파스텔 블루로요. 손님 중에 견과류 알레르기가 있는데 괜찮나요?'),
          ('Saleringo', '+9초', '문구와 색상은 그대로 적어 두었습니다. 견과류가 들어가는지는 주방에서 확인해 답해 드려야 해서, '
                                '그 부분만 사장님이 오늘 중에 연락드리겠습니다. 픽업은 토요일 몇 시로 할까요?'),
          ('고객', '8:06 AM', '11시요. 이름은 김민지예요.'),
          ('Saleringo', '+7초', '토요일 오전 11시 픽업, 2호 파스텔 블루 레터링 케이크, 김민지 님으로 접수했습니다. '
                                '확인 문자를 보내 드리고, 알레르기 답변은 따로 연락드리겠습니다.')],
 'refuse': [('알레르기와 원재료를 대신 답하지 않습니다.',
             '견과류, 우유, 밀이 들어가는지는 그날 주방이 확인할 일입니다. 질문은 그대로 적어 두고 사장님이 답합니다.'),
            ('주문이 꽉 찬 날짜를 받지 않습니다.',
             '케이크는 하루에 만들 수 있는 개수가 정해져 있습니다. 등록된 주문 한도 안에서만 받고, 넘치면 다음 날을 제시합니다.'),
            ('메뉴에 없는 케이크를 만들어 주겠다고 하지 않습니다.',
             '주문 가능한 사이즈와 맛, 옵션은 사장님이 넣어 둔 목록뿐입니다. 특별 주문은 요청으로 남깁니다.'),
            ('단체 · 납품 단가를 조정하지 않습니다.',
             '회사 납품이나 대량 주문 할인은 사장님이 정합니다. 수량과 날짜만 받아 적습니다.')],
 'fields': ['주문 품목 · 사이즈 · 옵션', '레터링 문구와 색상', '픽업 날짜와 시간',
            '알레르기 · 원재료 문의 여부', '주문자 성함과 연락처', '선결제 · 현장 결제 구분'],
 'stages': ['문의 접수', '주문 확정', '전날 준비', '픽업', '재주문 안내'],
 'lead': '케이크 주문은 오픈 러시에 옵니다. 주문 한도 안에서만 받고, 알레르기 질문은 그대로 적어 주방으로 넘깁니다.',
 'group': 4,
 'en': {
  'name': 'Cafés & bakeries', 'owner': 'the owner',
  'kicker': 'Caf&eacute;s &middot; bakeries &middot; custom cakes',
  'h1': 'Cake orders arrive at eight,<br>in the middle of the coffee line.',
  'sub': 'The birthday cake is ordered on the way to work, and the way to work is your busiest hour. '
         'The barista cannot pick up, and a custom order is not a two-word text.',
  'cost': 'A custom cake is fifty to a hundred dollars and it brings the party, the corporate order and the regular back. '
          'The order call lands when the line is out the door and the phone is under the milk jugs. The customer who gets '
          'no answer orders from the bakery two doors down, and next year she orders there again.',
  'call': [('Customer', '8:04 AM', 'I would like to order a first-birthday cake for Saturday. Do you do an eight-inch?'),
           ('Saleringo', '+16 s', 'Saturday is available. An eight-inch cream cake is <b>$58</b>, hand lettering is <b>$6</b> extra, '
                                  'and pick-up starts at 10:00 AM. I just need the wording and the colour.'),
           ('Customer', '8:05 AM', 'The wording is &ldquo;Happy first birthday, Leo&rdquo;, in pastel blue. One guest has a nut allergy &mdash; is that okay?'),
           ('Saleringo', '+9 s', 'Wording and colour are written down exactly as you said them. Whether nuts are present is something the kitchen '
                                 'has to confirm, so the owner will call you about that today. What time on Saturday would you like to collect?'),
           ('Customer', '8:06 AM', 'Eleven. The name is Emma Park.'),
           ('Saleringo', '+7 s', 'Saturday 11:00 AM pick-up, eight-inch pastel-blue lettered cake, under Emma Park. '
                                 'I will text the confirmation now, and the allergy answer comes separately from the owner.')],
  'refuse': [('It never answers an allergen question itself.',
              'Whether nuts, dairy or gluten are in a cake is for the kitchen to confirm on the day. The question is recorded word for word and the owner answers it.'),
             ('It never takes an order for a day that is full.',
              'There is a limit to how many cakes a kitchen can make. It books within the order cap the owner set and offers the next day otherwise.'),
             ('It never promises a cake that is not on the menu.',
              'Sizes, flavours and options are the ones the owner loaded. A special request is logged as a request, not a confirmation.'),
             ('It never adjusts a wholesale or bulk price.',
              'Corporate and volume discounts are the owner&rsquo;s decision. The AI records the quantity and the date.')],
  'fields': ['Item, size and options', 'Lettering and colour', 'Pick-up date and time',
             'Allergen or ingredient question raised', 'Customer name and mobile', 'Prepaid or pay on collection'],
  'stages': ['Enquiry', 'Order confirmed', 'Prepped the day before', 'Collected', 'Reorder prompt'],
  'when': {'eyebrow': 'A call during the morning rush', 'h2': 'While the line is out the door,<br>this is how it goes.', 'tt': '8:04 AM', 'badge': 'espresso machine running'},
  'lead': 'Cake orders come at the height of the coffee rush. It books within the daily cap and passes the allergy question to the kitchen, unanswered.',
  'room': 'places-hospitality',
  'room_d': 'The 8:04 AM birthday-cake order taken to the letter and the colour, priced off your own menu, the Saturday slot held &mdash; and the nut question written down for the kitchen, never answered.',
  'room_no': ('0', 'allergen questions answered by anyone but the kitchen'),
 },
},
{
 'slug': 'catering', 'owner': '대표님', 'name': '케이터링 · 출장뷔페', 'photo': ph('PENDING'),
 'when': {'eyebrow': '행사장에서 배식 중의 통화', 'h2': '뷔페 라인을 지키는 동안<br>이렇게 흘러갑니다.', 'tt': '배식 중', 'badge': '전 직원 현장'},
 'kicker': '케이터링 &middot; 출장뷔페 &middot; 기업 행사',
 'h1': '다음 행사의 전화는<br>이번 행사를 차리는 중에 옵니다.',
 'sub': '케이터링 문의는 총무팀의 근무 시간과 가족의 토요일 저녁에 옵니다. '
        '둘 다 팀 전체가 다른 행사장의 뷔페 라인에 서 있는 시간입니다.',
 'cost': '80명 기업 오찬은 300만원짜리 행사이고, 한 번 맡긴 회사는 연말 행사도 맡깁니다. 문의는 모든 손이 '
         '보온 용기를 들고 있을 때 오고, 부재중을 만난 담당자는 같은 요청서를 다른 세 곳에 보냅니다. '
         '날짜와 단가를 먼저 답한 곳이 시식 기회를 가져갑니다.',
 'call': [('고객', '6:32 PM', '다음 달 15일에 회사 창립 기념 행사가 있는데 80명 출장뷔페 되나요?'),
          ('Saleringo', '+21초', '15일은 아직 접수 가능한 날짜로 나옵니다. 80명 기준 <b>스탠다드 코스 1인 3만 5천원</b>, '
                                 '<b>프리미엄 1인 5만 2천원</b>이고 배식 인력과 집기가 포함됩니다. 장소가 어디이고 몇 시에 식사 시작인가요?'),
          ('고객', '6:34 PM', '판교 사무실 5층 라운지고 점심 12시요. 채식하는 분이 여섯 명쯤 되고, 가격은 좀 조정이 될까요?'),
          ('Saleringo', '+9초', '판교 사무실 5층, 12시 식사, 80명 중 채식 6명으로 적어 두었습니다. 견적 조정은 대표님이 현장 조건을 '
                                '보고 정하시는 것이라 제가 답할 수 없고, 답사 뒤에 정식 견적서로 보내 드립니다. '
                                '답사는 <b>이번 주 목요일 오후</b>가 가능합니다.'),
          ('고객', '6:35 PM', '목요일 3시로 해 주세요. 총무팀 박서연입니다.'),
          ('Saleringo', '+7초', '목요일 오후 3시 현장 답사, 박서연 님으로 잡았습니다. 15일은 답사와 견적 확정 전까지 가접수 상태로 두고, '
                                '확인 문자를 지금 보내 드리겠습니다.')],
 'refuse': [('찬 날짜를 받지 않습니다.',
             '같은 날 두 현장은 한 팀으로 못 갑니다. 등록된 행사 캘린더에서 비어 있는 날만 가접수하고, 확정은 답사와 계약으로만 합니다.'),
            ('견적을 깎아 주지 않습니다.',
             '1인 단가는 대표님이 넣어 둔 코스표대로만 말합니다. 조정은 답사 뒤 대표님이 정식 견적서로 답합니다.'),
            ('식단과 알레르기 대응을 확정하지 않습니다.',
             '채식, 할랄, 알레르기 요청은 인원과 함께 그대로 적어 두고 주방이 답합니다.'),
            ('현장 조건을 가정하지 않습니다.',
             '주차, 엘리베이터, 전기와 급수는 답사에서 확인할 일입니다. 전화로 &ldquo;될 겁니다&rdquo;라고 하지 않습니다.')],
 'fields': ['행사 날짜 · 장소 · 식사 시간', '인원과 코스(1인 단가)', '채식 · 알레르기 등 식단 요청',
            '현장 답사 예약 시간', '담당자 성함 · 소속 · 연락처', '가접수 · 확정 상태'],
 'stages': ['문의 접수', '가접수 · 답사 예약', '답사 · 견적서', '계약 · 확정', '행사 · 정산'],
 'lead': '행사 문의는 다른 행사장에서 배식 중일 때 옵니다. 빈 날짜만 가접수하고, 단가 조정은 답사 뒤 대표님의 견적서로 넘깁니다.',
 'group': 4,
 'en': {
  'name': 'Catering', 'owner': 'the owner',
  'kicker': 'Catering &middot; event food &middot; corporate lunches',
  'h1': 'The next booking calls<br>while you are serving this one.',
  'sub': 'Catering enquiries come from office managers during their working day and from families on Saturday evening. '
         'Both are the hours your whole team is on a buffet line somewhere else.',
  'cost': 'An eighty-head corporate lunch is a three-thousand-dollar job, and the company that books once books the holiday '
          'party too. The enquiry lands when every hand is carrying a chafing dish, and the organiser who gets voicemail sends '
          'the same brief to three other caterers. Whoever replies first with a date and a price gets the tasting.',
  'call': [('Client', '6:32 PM', 'We have a company anniversary on the 15th of next month &mdash; can you cater a buffet for eighty?'),
           ('Saleringo', '+21 s', 'The 15th is still showing as open. For eighty, the <b>standard buffet is $32 a head</b> and the '
                                  '<b>premium is $48</b>, with service staff and equipment included. Where is the venue and what time does lunch start?'),
           ('Client', '6:34 PM', 'Our office in Palo Alto, fifth-floor lounge, lunch at noon. About six vegetarians. Is there any movement on the price?'),
           ('Saleringo', '+9 s', 'Palo Alto office, fifth floor, noon service, eighty guests with six vegetarian &mdash; noted. Pricing adjustments '
                                 'are the owner&rsquo;s decision after seeing the site, so I cannot answer that; a formal quote follows the site visit. '
                                 'The owner can visit <b>this Thursday afternoon</b>.'),
           ('Client', '6:35 PM', 'Thursday at three. Sarah Park, office management.'),
           ('Saleringo', '+7 s', 'Thursday 3:00 PM site visit, under Sarah Park &mdash; booked. The 15th stays on a provisional hold until the visit '
                                 'and the quote are confirmed, and I am texting the confirmation now.')],
  'refuse': [('It never takes a date the calendar already has.',
              'One team cannot serve two sites on the same day. It holds only dates the event calendar shows open, and a hold becomes '
              'a booking only through the site visit and a contract.'),
             ('It never moves the price.',
              'Per-head rates are read from the course sheet the owner loaded. Any adjustment comes after the site visit, in the owner&rsquo;s written quote.'),
             ('It never confirms dietary or allergen handling.',
              'Vegetarian, halal and allergy requests are recorded with the headcount and answered by the kitchen.'),
             ('It never assumes the site will work.',
              'Parking, lifts, power and water are checked on the visit. It does not say &ldquo;that should be fine&rdquo; down the phone.')],
  'fields': ['Event date, venue and service time', 'Headcount and menu tier (per-head rate)', 'Dietary and allergen requests',
             'Site-visit appointment', 'Organiser name, company and mobile', 'Provisional or confirmed'],
  'stages': ['Enquiry', 'Provisional hold and site visit', 'Visit and written quote', 'Contract and confirmation', 'Event and invoice'],
  'when': {'eyebrow': 'A call from behind the buffet line', 'h2': 'While the chafing dishes are out,<br>this is how it goes.', 'tt': 'mid-service', 'badge': 'whole team on site'},
  'lead': 'Event enquiries arrive while the team is serving another event. It holds only open dates and leaves the price movement to the owner&rsquo;s quote after the site visit.',
  'room': 'places-hospitality',
  'room_d': 'The eighty-head anniversary lunch priced per head off your own course sheet, the date put on a provisional hold, the site visit booked &mdash; and the discount question left for the owner.',
  'room_no': ('0', 'dates confirmed before the site visit and the contract'),
 },
},
{
 'slug': 'travel-agency', 'owner': '대표님', 'name': '여행사', 'photo': ph('PENDING'),
 'when': {'eyebrow': '저녁 식탁 뒤의 통화', 'h2': '예약 시스템이 닫힌 동안<br>이렇게 흘러갑니다.', 'tt': '저녁 9시', 'badge': '담당자 퇴근 후'},
 'kicker': '여행사 &middot; 패키지 &middot; 항공 · 호텔',
 'h1': '여행은 저녁 식탁에서 정해지고,<br>전화는 그 자리에서 걸립니다.',
 'sub': '가족은 화요일 밤에 여행지를 정하고, 신혼부부는 열두 시간 시차 너머에서 메시지를 보냅니다. '
        '책상에서만 받는 여행사는 문의의 절반만 받습니다.',
 'cost': '4인 패키지 한 건은 400만원 안팎의 예약이고, 한 번 함께 다녀온 가족은 다음 여행도 같은 곳에 맡깁니다. '
         '문의는 밤 아홉 시에 오고, 사람과 연결되지 않은 손님은 같은 상품을 온라인에서 결제합니다. '
         '거기서는 아무도 여권 만료를 잡아 주지 않습니다.',
 'call': [('고객', '9:26 PM', '12월 말에 부모님 모시고 다낭 4박 5일 패키지 가려고요. 자리 있나요?'),
          ('Saleringo', '+20초', '12월 출발 다낭 4박 5일 상품은 <b>12월 26일</b>과 <b>28일</b> 출발이 있고, 성인 1인 <b>89만원</b>부터입니다. '
                                 '좌석은 담당자가 항공사 시스템에서 확인해야 정확해서, 지금 &ldquo;있다&rdquo;고는 말씀드리지 않겠습니다. '
                                 '몇 분이시고 어느 날짜를 원하세요?'),
          ('고객', '9:28 PM', '어른 넷이고 26일이요. 아버지 여권이 내년 3월에 만료되는데 괜찮나요?'),
          ('Saleringo', '+9초', '성인 4명, 26일 출발로 적어 두었습니다. 여권 잔여 기간과 입국 요건은 나라마다 기준이 달라서 제가 판단하지 않고, '
                                '담당자가 확인해서 좌석과 함께 안내드립니다. 내일 오전에 연락드려도 될까요?'),
          ('고객', '9:29 PM', '네, 오전 10시 이후로요. 이름은 정하윤입니다.'),
          ('Saleringo', '+7초', '정하윤 님, 내일 오전 10시 이후 담당자 연락으로 잡았습니다. 문의 내용과 확인할 항목을 정리해서 문자로 보내 드리겠습니다.')],
 'refuse': [('확인하지 않은 좌석을 있다고 하지 않습니다.',
             '항공 좌석과 호텔 객실은 담당자가 예약 시스템에서 조회해야 압니다. 상품과 출발일까지만 말하고 확인은 사람이 합니다.'),
            ('비자와 입국 요건을 판단하지 않습니다.',
             '여권 잔여 기간, 비자 필요 여부, 입국 조건은 국가와 국적에 따라 다르고 예고 없이 바뀝니다. 질문을 적어 두고 담당자가 확인해 답합니다.'),
            ('없는 요금과 프로모션을 만들지 않습니다.',
             '등록된 상품 가격표의 출발일별 금액만 말합니다. 유류할증료와 세금이 별도인지도 표에 적힌 대로 말합니다.'),
            ('취소 수수료를 대신 정하지 않습니다.',
             '취소 · 변경 규정은 상품과 항공권마다 다릅니다. 약관 확인 항목으로 남깁니다.')],
 'fields': ['목적지 · 상품명 · 출발일', '인원(성인 · 아동 · 유아)', '안내한 1인 요금과 포함 사항',
            '여권 · 비자 등 확인 요청 사항', '희망 연락 시간과 담당자', '가예약 · 확정 상태'],
 'stages': ['문의 접수', '담당자 확인', '가예약 · 견적', '계약 · 결제', '출발 안내'],
 'lead': '여행 계획은 저녁 식탁에서 세워집니다. 상품과 출발일까지만 말하고, 좌석 확인과 비자 판단은 담당자에게 넘깁니다.',
 'group': 4,
 'en': {
  'name': 'Travel agencies', 'owner': 'the owner',
  'kicker': 'Travel agencies &middot; tour operators &middot; package holidays',
  'h1': 'Holidays are planned after dinner,<br>in a different time zone from your desk.',
  'sub': 'The family decides on the trip on Tuesday night and the honeymooners message from twelve hours away. '
         'A travel agent who answers only at the desk answers half the enquiries.',
  'cost': 'A four-person package is a four-thousand-dollar booking, and the family that travels with you once comes back '
          'for the next trip. The enquiry lands at nine at night, and the customer who cannot reach a person books the same '
          'trip online, where nobody would have caught the passport problem.',
  'call': [('Customer', '9:26 PM', 'We want to take my parents to Canc&uacute;n for five nights at the end of December &mdash; is there space on a package?'),
           ('Saleringo', '+20 s', 'For December there are Canc&uacute;n five-night departures on the <b>26th</b> and the <b>28th</b>, from '
                                  '<b>$1,290 per adult</b>. Seats have to be checked in the airline system by an agent, so I will not tell you '
                                  'there is space until they have. How many travellers and which date?'),
           ('Customer', '9:28 PM', 'Four adults, the 26th. My father&rsquo;s passport expires next March &mdash; is that a problem?'),
           ('Saleringo', '+9 s', 'Four adults on the 26th &mdash; noted. Passport validity and entry requirements differ by country, so I do not '
                                 'rule on that; an agent checks it and tells you together with the availability. May they call you tomorrow morning?'),
           ('Customer', '9:29 PM', 'Yes, after ten. It&rsquo;s Hannah Chung.'),
           ('Saleringo', '+7 s', 'Hannah, an agent will call you tomorrow after 10:00 AM. I am texting you a summary of the enquiry and the items they will check.')],
  'refuse': [('It never says there is availability it has not checked.',
              'Airline seats and hotel rooms exist only in the booking system an agent can see. It names the product and the departure date, and a person confirms the space.'),
             ('It never gives a visa or entry ruling.',
              'Passport validity, visa requirements and entry rules vary by country and nationality and change without notice. The question is logged and an agent answers it.'),
             ('It never invents a fare or a promotion.',
              'It quotes only the per-departure prices on the loaded product sheet, and says whether taxes and fuel surcharges are extra exactly as the sheet says.'),
             ('It never decides a cancellation fee.',
              'Cancellation and change terms differ by product and by ticket. They are left as a terms-check item for the agent.')],
  'fields': ['Destination, product and departure date', 'Travellers (adults, children, infants)', 'Per-person price quoted and inclusions',
             'Passport, visa and entry questions raised', 'Preferred callback time and agent', 'Held or confirmed'],
  'stages': ['Enquiry', 'Agent check', 'Provisional booking and quote', 'Contract and payment', 'Pre-departure briefing'],
  'when': {'eyebrow': 'A call after the dinner plates', 'h2': 'While the booking system is logged off,<br>this is how it goes.', 'tt': '9:26 PM', 'badge': 'agents off duty'},
  'lead': 'Trips are planned at the dinner table. It names the product and the departure date, and leaves the seat check and the visa question to an agent.',
  'room': 'places-hospitality',
  'room_d': 'The 9:26 PM family package enquiry priced off your own product sheet and handed to an agent for the morning &mdash; with no seat promised unchecked and no passport ruling given.',
  'room_no': ('0', 'seats confirmed unchecked, and no entry rulings given'),
 },
},
{
 'slug': 'photo-studio', 'owner': '실장님', 'name': '사진관 · 스튜디오', 'photo': ph('PENDING'),
 'when': {'eyebrow': '촬영 중의 통화', 'h2': '셔터를 누르는 동안<br>이렇게 흘러갑니다.', 'tt': '촬영 중', 'badge': '조명 켜진 시간'},
 'kicker': '사진관 &middot; 스튜디오 &middot; 돌 · 가족 · 프로필',
 'h1': '전화는 셔터와<br>다음 포즈 사이에 울립니다.',
 'sub': '스튜디오 예약은 평일 오후에 잡히고, 평일 오후는 조명이 켜지고 작가가 카메라 뒤에 있는 시간입니다. '
        '촬영을 끊고 전화를 받는 사람은 없습니다.',
 'cost': '가족 촬영 한 건은 30만원 안팎의 예약이고, 액자와 다음 기념일, 동서의 소개로 이어집니다. 문의는 촬영 중에 오고, '
         '부재중을 만난 손님은 온라인 캘린더가 있는 스튜디오에 예약합니다. 찍지 못한 촬영이 몇 건인지 아는 스튜디오는 없습니다.',
 'call': [('고객', '3:18 PM', '돌 스냅 촬영 얼마예요? 다음 달 둘째 주 토요일 오전에 되나요?'),
          ('Saleringo', '+18초', '돌 스냅은 <b>1시간 촬영에 22만원</b>이고 원본 전체와 보정본 20장이 포함됩니다. 다음 달 둘째 주 토요일은 '
                                 '<b>오전 10시</b>가 비어 있습니다. 의상은 두 벌까지 대여가 포함입니다.'),
          ('고객', '3:19 PM', '가족사진도 같이 찍으면 추가로 얼마예요? 아이 얼굴 보정도 자연스럽게 되나요?'),
          ('Saleringo', '+9초', '가족 컷 추가는 <b>5만원</b>입니다. 보정 정도는 실장님이 촬영 뒤 샘플을 보여 드리고 상의하는 것이라, '
                                '결과를 전화로 약속드리지는 않겠습니다. 토요일 10시로 잡아 드릴까요?'),
          ('고객', '3:20 PM', '네, 잡아 주세요. 이서윤이에요.'),
          ('Saleringo', '+7초', '이서윤 님, 다음 달 둘째 주 토요일 오전 10시, 돌 스냅과 가족 컷으로 예약했습니다. 예약금 안내와 준비물을 문자로 보내 드리겠습니다.')],
 'refuse': [('결과물을 약속하지 않습니다.',
             '&ldquo;잘 나온다&rdquo;, &ldquo;자연스럽게 된다&rdquo;는 말을 하지 않습니다. 보정의 정도와 촬영 결과는 실장님이 샘플로 보여 드리고 상의합니다.'),
            ('예약된 시간에 다른 촬영을 넣지 않습니다.',
             '스튜디오도 작가도 하나입니다. 캘린더에 비어 있는 시간에만 잡고, 세팅 시간을 포함해 겹치지 않게 둡니다.'),
            ('가격표 밖의 구성을 만들지 않습니다.',
             '촬영 종류별 시간, 포함 컷 수, 추가 옵션은 실장님이 넣어 둔 표대로만 말합니다.'),
            ('납품 일정을 앞당겨 약속하지 않습니다.',
             '보정본 전달 기간은 등록된 기준대로만 말합니다. 급행이 되는지는 실장님이 정합니다.')],
 'fields': ['촬영 종류(돌 · 가족 · 프로필 · 증명)', '촬영 날짜 · 시간과 소요 시간', '인원과 의상 대여 여부',
            '안내한 금액과 추가 옵션', '예약금 안내 · 입금 여부', '보정본 납품 예정일'],
 'stages': ['문의 접수', '예약 · 예약금', '촬영', '셀렉 · 보정', '납품 · 재촬영 안내'],
 'lead': '셔터를 누르는 동안 전화를 받을 수 없습니다. 가격표의 구성으로 빈 시간에 예약하고, 사진이 어떻게 나올지는 약속하지 않습니다.',
 'group': 1,
 'en': {
  'name': 'Photo studios', 'owner': 'the studio owner',
  'kicker': 'Photo studios &middot; portraits &middot; family sessions',
  'h1': 'The phone rings<br>between the shutter and the next pose.',
  'sub': 'Studio bookings are made on weekday afternoons, and weekday afternoons are when the lights are on and the '
         'photographer is behind the camera. Nobody breaks a session to answer.',
  'cost': 'A family session is a three-hundred-dollar booking that turns into prints, the next milestone and the referral to '
          'the sister-in-law. The enquiry arrives mid-shoot, and the caller who reaches voicemail books the studio with the '
          'online calendar. The studio never learns which sessions it did not shoot.',
  'call': [('Customer', '3:18 PM', 'How much is a first-birthday session, and do you have a Saturday morning in the second week of next month?'),
           ('Saleringo', '+18 s', 'The first-birthday session is <b>$280 for one hour</b>, with all originals and twenty retouched images included. '
                                  'The second Saturday next month has <b>10:00 AM</b> open. Two outfits from the studio wardrobe are included.'),
           ('Customer', '3:19 PM', 'What is the extra for family shots as well? And will the retouching on the baby look natural?'),
           ('Saleringo', '+9 s', 'Adding family shots is <b>$60</b>. How far the retouching goes is something the studio owner shows you on samples '
                                 'after the shoot and agrees with you, so I will not promise a result over the phone. Shall I hold Saturday at ten?'),
           ('Customer', '3:20 PM', 'Please do. It&rsquo;s Olivia Lee.'),
           ('Saleringo', '+7 s', 'Olivia, you are booked for the second Saturday next month at 10:00 AM, first-birthday session plus family shots. '
                                 'I am texting the deposit details and what to bring.')],
  'refuse': [('It never promises how the pictures will come out.',
              'No &ldquo;they will look great&rdquo; and no &ldquo;the retouching will be natural&rdquo;. Retouching and results are shown on samples by the studio owner and agreed in person.'),
             ('It never double-books the studio.',
              'There is one room and one photographer. It books only into open calendar time and keeps set-up time clear between sessions.'),
             ('It never builds a package that is not on the price sheet.',
              'Session lengths, included images and add-ons are quoted exactly as the owner loaded them.'),
             ('It never promises a faster delivery.',
              'Turnaround for retouched images is stated from the loaded standard. Whether a rush is possible is the owner&rsquo;s decision.')],
  'fields': ['Session type (milestone, family, headshot, passport)', 'Date, time and session length', 'Headcount and wardrobe hire',
             'Price quoted and add-ons', 'Deposit requested and received', 'Delivery date for retouched images'],
  'stages': ['Enquiry', 'Booked and deposit', 'Session', 'Selection and retouching', 'Delivered and next milestone'],
  'when': {'eyebrow': 'A call mid-session', 'h2': 'While the lights are on,<br>this is how it goes.', 'tt': 'mid-shoot', 'badge': 'camera in hand'},
  'lead': 'Nobody answers between the shutter and the next pose. It books open studio time off the price sheet and never promises how the pictures will look.',
  'room': 'booked-by-appointment',
  'room_d': 'The mid-session milestone enquiry priced off your own sheet, the open Saturday held with a deposit request sent &mdash; and no promise of how the retouching will look.',
  'room_no': ('0', 'results the AI promises before the owner has shown a sample'),
 },
},
{
 'slug': 'florist', 'owner': '사장님', 'name': '꽃집', 'photo': ph('PENDING'),
 'when': {'eyebrow': '꽃 시장 다녀온 뒤의 통화', 'h2': '줄기를 다듬는 동안<br>이렇게 흘러갑니다.', 'tt': '오전 7시 40분', 'badge': '배송 나가기 전'},
 'kicker': '꽃집 &middot; 당일 배송 &middot; 행사 꽃',
 'h1': '주문은 줄기를<br>자르는 중에 들어옵니다.',
 'sub': '당일 주문은 시장에서 돌아온 뒤 첫 배송 전까지, 손이 젖어 있고 차에 반쯤 실은 시간에 옵니다. '
        '부재중이 된 주문은 꽃배달 중개 앱으로 갑니다.',
 'cost': '병문안 꽃바구니 하나는 5만원이고, 그것을 보낸 손님은 기념일 꽃다발과 근조 화환도 보냅니다. 주문은 아침 러시에 오고, '
         '중개 앱은 30%를 떼고 기꺼이 그 주문을 받습니다. 이미 찬 날에 받아 버린 예식 주문은 놓친 주문보다 나쁩니다.',
 'call': [('고객', '7:41 AM', '오늘 오후에 병원으로 꽃바구니 배달되나요? 5만원 정도로요.'),
          ('Saleringo', '+15초', '오늘 오후 배달 가능합니다. <b>5만원 꽃바구니</b>는 계절 꽃으로 구성되고, 시내 병원 배송비는 <b>5천원</b>입니다. '
                                 '병원 이름과 병실 번호, 받으시는 분 성함을 알려 주시겠어요?'),
          ('고객', '7:42 AM', '한빛병원 702호 김영희 님이요. 향이 강한 꽃은 빼 주시고, 카드에 &ldquo;빠른 쾌유를 빕니다&rdquo;라고 써 주세요.'),
          ('Saleringo', '+9초', '한빛병원 702호 김영희 님, 향 강한 꽃 제외, 카드 문구까지 그대로 적었습니다. 병원마다 생화 반입 규정이 달라서 '
                                '배송 전에 사장님이 확인하고, 문제가 있으면 먼저 연락드립니다.'),
          ('고객', '7:43 AM', '네, 그리고 다음 주 토요일 결혼식 부케도 될까요?'),
          ('Saleringo', '+8초', '다음 주 토요일은 이미 예식 주문이 한도까지 차 있어서 부케는 제가 받지 않겠습니다. 사장님이 오늘 중에 '
                                '가능 여부를 확인해서 연락드리도록 남겨 두겠습니다. 오늘 배달 건은 결제 링크를 문자로 보내 드립니다.')],
 'refuse': [('예식 주문이 찬 날에는 부케를 받지 않습니다.',
             '예식과 행사 꽃은 하루에 할 수 있는 양이 정해져 있습니다. 등록된 주문 한도를 넘는 날은 &ldquo;확인 후 연락&rdquo;으로 남깁니다.'),
            ('없는 꽃을 약속하지 않습니다.',
             '그날 시장에서 들어온 꽃으로 만듭니다. 특정 품종을 반드시 넣겠다고 하지 않고, 요청으로만 적어 둡니다.'),
            ('가격대 밖의 구성을 만들지 않습니다.',
             '금액대별 구성과 배송비는 사장님이 넣어 둔 표대로만 말합니다.'),
            ('병원 · 장례식장 반입 규정을 단정하지 않습니다.',
             '생화 반입이 되는지는 그 시설의 규정입니다. 배송 전에 사장님이 확인하고, 안 되면 먼저 연락드립니다.')],
 'fields': ['용도(축하 · 쾌유 · 근조 · 예식)', '금액대와 구성 요청', '배송 주소 · 받는 분 · 희망 시간',
            '카드 문구', '주문자 성함과 연락처', '결제 링크 발송 · 결제 여부'],
 'stages': ['문의 접수', '주문 확정 · 결제', '제작', '배송 · 사진 전송', '재주문 안내'],
 'lead': '꽃 주문은 시장에서 돌아온 아침에 옵니다. 금액대별 구성으로 오늘 배달을 받고, 찬 날짜의 예식 주문은 받지 않습니다.',
 'group': 4,
 'en': {
  'name': 'Florists', 'owner': 'the owner',
  'kicker': 'Florists &middot; same-day delivery &middot; event flowers',
  'h1': 'The order comes in<br>while the stems are still being cut.',
  'sub': 'Same-day orders arrive between the market run and the first delivery, with wet hands and the van half loaded. '
         'The order that goes to voicemail goes to the online aggregator instead.',
  'cost': 'A hospital basket is sixty dollars, and the customer who sends one sends the anniversary bouquet and the funeral spray. '
          'Orders land in the morning rush, and the aggregators are happy to take them for a thirty-per-cent cut. A wedding taken '
          'on a day that is already full is worse than a missed one.',
  'call': [('Customer', '7:41 AM', 'Can you deliver a get-well basket to the hospital this afternoon? Around sixty dollars.'),
           ('Saleringo', '+15 s', 'This afternoon works. The <b>$60 basket</b> is made with seasonal flowers, and delivery to hospitals in town is <b>$8</b>. '
                                  'Which hospital, which room, and who is it for?'),
           ('Customer', '7:42 AM', 'St. Mary&rsquo;s, room 702, Margaret Kim. Nothing too fragrant, and the card should say &ldquo;Wishing you a speedy recovery&rdquo;.'),
           ('Saleringo', '+9 s', 'St. Mary&rsquo;s, room 702, Margaret Kim, nothing strongly scented, card wording as you said it &mdash; written down. '
                                 'Hospitals differ on fresh flowers on the wards, so the owner checks before dispatch and calls you first if there is a problem.'),
           ('Customer', '7:43 AM', 'Great. Could you also do a bridal bouquet for next Saturday?'),
           ('Saleringo', '+8 s', 'Next Saturday already has wedding orders to the limit, so I will not take the bouquet myself. I am leaving it for the '
                                 'owner to confirm today whether it is possible. For today&rsquo;s delivery I am texting you a payment link now.')],
  'refuse': [('It never books a wedding on a day the sheet shows full.',
              'Wedding and event work has a daily limit. A date past the loaded cap is logged as &ldquo;owner to confirm&rdquo;, not as an order.'),
             ('It never promises a flower it does not have.',
              'Arrangements are built from what came in from the market that morning. A specific variety is written down as a request, not guaranteed.'),
             ('It never composes a price that is not on the sheet.',
              'Price bands, what each band contains and delivery charges are quoted as the owner loaded them.'),
             ('It never assumes a hospital or funeral home will accept flowers.',
              'Ward and chapel rules belong to that building. The owner checks before dispatch and calls first if flowers cannot go in.')],
  'fields': ['Occasion (celebration, get-well, sympathy, wedding)', 'Price band and composition requests', 'Delivery address, recipient and time window',
             'Card message', 'Sender name and mobile', 'Payment link sent and paid'],
  'stages': ['Enquiry', 'Order confirmed and paid', 'Made up', 'Delivered with photo', 'Next-occasion reminder'],
  'when': {'eyebrow': 'A call after the market run', 'h2': 'While the stems are being conditioned,<br>this is how it goes.', 'tt': '7:41 AM', 'badge': 'van half loaded'},
  'lead': 'Orders arrive in the hour after the market. It takes today&rsquo;s delivery off the price bands and refuses the wedding on a day that is already full.',
  'room': 'booked-by-appointment',
  'room_d': 'The 7:41 AM get-well basket taken with the card wording and the ward number, priced off your own bands &mdash; and next Saturday&rsquo;s bouquet refused because the day is already full.',
  'room_no': ('0', 'orders taken on a day the sheet already shows full'),
 },
},
{
 'slug': 'accounting-tax', 'owner': '세무사님', 'name': '세무 · 회계 사무소', 'photo': ph('PENDING'),
 'when': {'eyebrow': '신고 마감 전날 저녁의 통화', 'h2': '마감 서류를 붙드는 동안<br>이렇게 흘러갑니다.', 'tt': '신고 마감 전날', 'badge': '전 직원 야근'},
 'kicker': '세무사 &middot; 회계사 &middot; 기장 대행',
 'h1': '마감은 내일이고,<br>신규 의뢰인은 오늘 밤에 겁니다.',
 'sub': '신고 기간은 전화가 가장 많이 오는 때이자 사무실의 누구도 받을 수 없는 때입니다. '
        '첫 신고를 앞둔 사장님은 마감 전날 저녁 여덟 시에 겁니다.',
 'cost': '신규 개인사업자 한 명은 이번 신고에 몇 년치 기장이 붙는 의뢰인이고, 모든 책상이 서류에 묻힌 두 주 사이에 옵니다. '
         '부재중을 만난 사람은 홈택스에서 혼자 하거나 옆 건물 사무소에 맡깁니다. 더 위험한 쪽은 누군가 받아서 '
         '&ldquo;이번엔 안 하셔도 될 거예요&rdquo;라고 말하는 경우이고, 그 한마디가 가산세가 됩니다.',
 'call': [('의뢰인', '7:52 PM', '작년에 개업했는데 부가세 신고를 처음 해 봐요. 간이과세인지 일반인지도 모르겠고, 이번에 꼭 해야 하나요?'),
          ('Saleringo', '+20초', '처음이시면 막막하실 만합니다. 간이인지 일반인지, 이번 기한에 신고 의무가 있는지는 사업자 등록 내용을 세무사님이 '
                                 '보고 판단하실 부분이라 제가 답하지 않겠습니다. 대신 상담을 잡고, 그때 가져오실 서류를 정리해 드리겠습니다.'),
          ('의뢰인', '7:54 PM', '그럼 뭘 가져가면 되나요? 수수료는요?'),
          ('Saleringo', '+10초', '사업자등록증, 홈택스 아이디, 매출 · 매입 자료와 카드 매출 내역이 필요합니다. 부가세 신고 대행은 '
                                 '<b>기장 없이 건당 15만원</b>부터이고, 정확한 금액은 자료를 본 뒤 안내드립니다. '
                                 '<b>내일 오전 9시 30분</b> 상담 자리가 비어 있습니다.'),
          ('의뢰인', '7:55 PM', '9시 반으로 부탁드립니다. 최준호입니다.'),
          ('Saleringo', '+7초', '최준호 님, 내일 오전 9시 30분 상담으로 잡았습니다. 준비 서류 목록을 문자로 보내 드리고, 세무사님께 개업 첫 신고 건으로 표시해 두겠습니다.')],
 'refuse': [('세법 판단을 하지 않습니다.',
             '간이인지 일반인지, 공제가 되는지, 이 지출이 경비인지는 세무사님이 자료를 보고 판단할 일입니다. 질문을 그대로 적고 상담으로 넘깁니다.'),
            ('신고 기한과 의무를 단정하지 않습니다.',
             '&ldquo;이번에는 안 하셔도 됩니다&rdquo; 한마디가 가산세가 됩니다. 기한 관련 질문은 확인 항목으로 남겨 세무사님이 답합니다.'),
            ('수임료를 조정하지 않습니다.',
             '세무사님이 넣어 둔 기본 수임료 표만 말합니다. 업종과 규모에 따른 조정은 자료를 본 뒤 정합니다.'),
            ('다른 의뢰인의 정보를 말하지 않습니다.',
             '누가 어디에 신고했는지, 얼마를 냈는지는 어떤 경우에도 답하지 않습니다.')],
 'fields': ['의뢰인 구분(개인 · 개인사업자 · 법인)', '문의 유형(부가세 · 종소세 · 기장 · 법인세)', '업종과 개업 시점',
            '안내한 기본 수임료', '상담 예약 시간과 준비 서류', '기한 관련 확인 요청 여부'],
 'stages': ['문의 접수', '상담 예약', '자료 수령', '수임 · 신고', '기장 · 재계약'],
 'lead': '신고 마감 전날 저녁에 첫 신고 전화가 옵니다. 세법 판단과 기한 판단은 하지 않고, 준비 서류를 정리해 상담을 잡습니다.',
 'group': 5,
 'en': {
  'name': 'Accountants & tax', 'owner': 'the accountant',
  'kicker': 'Accountants &middot; tax preparers &middot; bookkeeping',
  'h1': 'The deadline is tomorrow,<br>and the new client is calling tonight.',
  'sub': 'Filing season is when the phone rings most and when nobody in the office can pick it up. '
         'The first-time filer calls at eight in the evening, the night before the deadline.',
  'cost': 'A new small-business client is worth the return plus years of bookkeeping, and they arrive in the fortnight when every '
          'desk is buried. The caller who reaches voicemail files with software or with the firm down the street. The dangerous '
          'version is worse: someone picks up and says &ldquo;you probably don&rsquo;t need to file this quarter&rdquo;, and that sentence becomes the penalty.',
  'call': [('Client', '7:52 PM', 'I started my business last year and I have never filed sales tax. I do not even know if I am supposed to file this quarter &mdash; do I have to?'),
           ('Saleringo', '+20 s', 'That is a fair thing to be unsure about. Whether you are required to file this quarter depends on your registration '
                                  'and your receipts, and that is the accountant&rsquo;s judgement to make, not mine. What I can do is book a consultation '
                                  'and tell you exactly what to bring.'),
           ('Client', '7:54 PM', 'Okay &mdash; what do I bring, and what does it cost?'),
           ('Saleringo', '+10 s', 'Your business registration, your sales records and card-processing statements, and any prior returns. A quarterly '
                                  'sales-tax return without bookkeeping starts at <b>$250</b>, and the exact fee is confirmed once the accountant has seen '
                                  'your records. There is a consultation open <b>tomorrow at 9:30 AM</b>.'),
           ('Client', '7:55 PM', 'Nine thirty, please. It&rsquo;s Daniel Choi.'),
           ('Saleringo', '+7 s', 'Daniel, tomorrow at 9:30 AM is booked. I am texting you the document list and flagging the file to the accountant as a first-time filer.')],
  'refuse': [('It never takes a tax position.',
              'Whether an expense is deductible, whether you qualify for a scheme, whether you owe &mdash; these are the accountant&rsquo;s calls after seeing the records. The question is recorded and passed on.'),
             ('It never rules on a filing deadline or an obligation.',
              '&ldquo;You probably don&rsquo;t need to file this time&rdquo; is the sentence that becomes a penalty. Deadline questions are left as a check item for the accountant to answer.'),
             ('It never adjusts the fee.',
              'It quotes the base fee schedule the accountant loaded. Adjustments for industry and volume are set after the records have been seen.'),
             ('It never discloses another client.',
              'Who files with the firm, what they earned and what they paid are never answered, to anyone.')],
  'fields': ['Client type (individual, sole trader, company)', 'Enquiry type (sales tax, income tax, bookkeeping, corporate)', 'Industry and trading start date',
             'Base fee quoted', 'Consultation time and document list', 'Deadline question flagged for the accountant'],
  'stages': ['Enquiry', 'Consultation booked', 'Records received', 'Engaged and filed', 'Bookkeeping and renewal'],
  'when': {'eyebrow': 'A call the night before the deadline', 'h2': 'While every desk is buried in filings,<br>this is how it goes.', 'tt': 'deadline eve', 'badge': 'whole office working late'},
  'lead': 'The first-time filer calls the night before the deadline. It takes no tax position and no view on the deadline; it lists the documents and books the consultation.',
  'room': 'professional-public',
  'room_d': 'The 7:52 PM first-time-filer call the night before the deadline: documents listed, base fee quoted off your own schedule, the consultation booked &mdash; and no view on whether they must file.',
  'room_no': ('0', 'tax positions or deadline rulings the AI will give'),
 },
},
{
 'slug': 'insurance-agency', 'owner': '대표님', 'name': '보험 대리점', 'photo': ph('PENDING'),
 'when': {'eyebrow': '토요일 저녁 접촉 사고 뒤의 통화', 'h2': '대리점이 닫힌 동안<br>이렇게 흘러갑니다.', 'tt': '토요일 저녁', 'badge': '설계사 휴무'},
 'kicker': '보험 대리점 &middot; 설계사 &middot; 사고 접수',
 'h1': '사고는 토요일 밤에 나고,<br>대리점은 월요일에 엽니다.',
 'sub': '계약자는 보험사 콜센터가 아니라 아는 설계사에게 걸고, 사고가 난 그 순간에 겁니다. '
        '근무 시간에만 받는 대리점은 첫 사고 전화를 이틀 늦게 받습니다.',
 'cost': '한 가구를 지키는 일은 계약 하나에 그 뒤의 갱신과 소개가 전부 걸린 일이고, 사고 처리가 꼬인 한 주에 잃습니다. '
         '전화는 긁힌 지 몇 분 안에 길가에서 옵니다. 부재중보다 나쁜 것은 잘못된 답입니다. 설계사가 아닌 누군가의 '
         '&ldquo;그건 처리돼요&rdquo;는 대리점이 책임져야 할 약속이 됩니다.',
 'call': [('고객', '8:17 PM', '방금 주차장에서 뒤차가 제 차를 긁었어요. 제 보험으로 처리되나요? 자차 들어 있는 것 같은데요.'),
          ('Saleringo', '+8초', '먼저 다치신 분은 없으신지요? 없으시면, 처리가 되는지는 약관과 사고 내용을 담당 설계사가 확인해야 답할 수 있어서 '
                                '제가 &ldquo;됩니다&rdquo;라고 말씀드리지 않겠습니다. 대신 지금 필요한 것을 정리해 드리겠습니다.'),
          ('고객', '8:18 PM', '다친 사람은 없어요. 상대방이 그냥 가려고 해서 번호판만 찍었어요.'),
          ('Saleringo', '+10초', '상대 차량 번호판 사진, 파손 부위 사진, 주차장 이름과 시간을 지금 문자로 보내 주시면 그대로 담당 설계사에게 '
                                 '전달하겠습니다. 보험사 24시간 사고 접수 번호로 오늘 밤에 접수 번호를 받으실 수 있으니, 그 번호도 함께 보내 드릴게요.'),
          ('고객', '8:19 PM', '네. 자기부담금은 얼마 나와요?'),
          ('Saleringo', '+8초', '자기부담금은 가입하신 특약에 따라 달라서 설계사가 증권을 보고 안내드립니다. 성함과 연락처를 남겨 주시면 '
                                '<b>월요일 오전 9시</b> 설계사가 먼저 연락드리도록 잡아 두겠습니다.')],
 'refuse': [('보상 여부를 말하지 않습니다.',
             '&ldquo;처리됩니다&rdquo; 한마디가 약속이 됩니다. 사고 내용과 사진을 받아 적고, 약관 확인은 담당 설계사가 합니다.'),
            ('자기부담금과 보험료 인상을 계산하지 않습니다.',
             '특약과 할증 기준은 증권마다 다릅니다. 증권을 본 설계사가 답합니다.'),
            ('상품을 권하거나 비교하지 않습니다.',
             '어느 보험이 더 낫다, 갈아타시라 같은 말은 모집 규정에 걸립니다. 문의 내용만 남기고 설계사가 상담합니다.'),
            ('부상이 있으면 접수보다 먼저 사람을 부릅니다.',
             '다친 사람이 있다고 하면 119 안내와 함께 당직 설계사에게 바로 연결합니다.')],
 'fields': ['문의 유형(사고 접수 · 보장 문의 · 갱신 · 신규)', '사고 일시 · 장소 · 부상 여부', '가입 상품과 증권 번호(확인 요청)',
            '받은 사진과 서류', '담당 설계사와 연락 예정 시간', '보험사 접수 번호'],
 'stages': ['문의 접수', '설계사 배정', '증권 · 약관 확인', '보험사 접수 · 처리', '갱신 · 추가 상담'],
 'lead': '사고는 대리점이 닫힌 토요일 저녁에 납니다. 보상 여부를 말하지 않고, 사진과 사실을 받아 설계사에게 넘깁니다.',
 'group': 5,
 'en': {
  'name': 'Insurance agencies', 'owner': 'the agency principal',
  'kicker': 'Insurance agencies &middot; brokers &middot; claims intake',
  'h1': 'Accidents happen on Saturday night.<br>The agency opens on Monday.',
  'sub': 'The policyholder calls the agent they know, not the carrier&rsquo;s hotline, and they call at the moment it happens. '
         'An agency that answers only in office hours takes its first claims call two days late.',
  'cost': 'A retained household is a policy plus every renewal and referral after it, and it is lost in the week a claim goes badly. '
          'The call comes from the kerb, minutes after the scrape. Worse than voicemail is the wrong answer: &ldquo;you&rsquo;re covered '
          'for that&rdquo; from anyone but the agent is a promise the agency has to keep.',
  'call': [('Customer', '8:17 PM', 'Someone just scraped my car in a parking lot. Is that covered on my policy? I think I have collision.'),
           ('Saleringo', '+8 s', 'First &mdash; is anyone hurt? If not, whether this is covered depends on your policy wording and the details, and that '
                                 'is for your agent to confirm, so I will not tell you it is. What I can do is get everything ready for them now.'),
           ('Customer', '8:18 PM', 'Nobody is hurt. The other driver tried to leave, so I only got a photo of the plate.'),
           ('Saleringo', '+10 s', 'Text me the plate photo, photos of the damage, and the name of the lot and the time, and I will pass them to your agent '
                                  'exactly as sent. The carrier&rsquo;s 24-hour claims line can open a claim number tonight &mdash; I will text you that number too.'),
           ('Customer', '8:19 PM', 'Okay. What will my deductible be?'),
           ('Saleringo', '+8 s', 'The deductible depends on the coverage you selected, and your agent reads it off your policy. Give me your name and '
                                 'mobile number and I will book the agent to call you first thing <b>Monday at 9:00 AM</b>.')],
  'refuse': [('It never says a claim is covered.',
              '&ldquo;You&rsquo;re covered&rdquo; is a promise the moment it is said. The AI records the facts and the photos; the policy wording is read by the agent.'),
             ('It never calculates a deductible or a premium change.',
              'Deductibles and surcharge rules differ by policy. The agent answers with the policy open.'),
             ('It never recommends or compares products.',
              'Telling someone one policy is better or that they should switch is regulated advice. The enquiry is logged and the licensed agent advises.'),
             ('An injury goes to a person before it goes to a form.',
              'If anyone is hurt, the caller is told to call 911 and the duty agent is connected at once.')],
  'fields': ['Enquiry type (claim, coverage question, renewal, new policy)', 'Incident date, place and injuries', 'Product held and policy number (to verify)',
             'Photos and documents received', 'Agent assigned and callback time', 'Carrier claim number'],
  'stages': ['Enquiry', 'Agent assigned', 'Policy and wording checked', 'Claim filed with the carrier', 'Renewal and follow-up'],
  'when': {'eyebrow': 'A call after a Saturday-night scrape', 'h2': 'While the agency is dark,<br>this is how it goes.', 'tt': 'Saturday evening', 'badge': 'closed for the weekend'},
  'lead': 'The scrape happens on Saturday night with the agency shut. It never says the claim is covered; it collects the photos and the facts and routes them to the agent.',
  'room': 'professional-public',
  'room_d': 'The 8:17 PM parking-lot scrape: injuries asked first, the plate and damage photos collected, the carrier&rsquo;s claims line given and the agent booked for Monday &mdash; with no word on whether it is covered.',
  'room_no': ('0', 'claims the AI says are covered'),
 },
},
]
