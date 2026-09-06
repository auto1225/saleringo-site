# -*- coding: utf-8 -*-
"""다섯 개 업종 추가 — 여섯 번째 묶음.

홈시큐리티 · 태양광, 컴퓨터 수리 · 퀵서비스, 인쇄 · 간판.
각 항목의 'en' 은 영문 사이트용이며 번역이 아니라 그 나라의 통화로 다시 쓴 것이다.
'group' 은 build/ko/p_trades.py 의 GROUPS 인덱스, 'en.room' 은 en/industries.html 의 방 id.
"""

PH = 'https://images.pexels.com/photos/%s/pexels-photo-%s.jpeg'


def ph(i):
    return PH % (i, i)


TRADES6 = [
{
 'slug': 'home-security', 'owner': '사장님', 'name': '홈시큐리티 · CCTV 설치', 'photo': ph('PENDING'),
 'when': {'eyebrow': '옆집에 도둑이 든 저녁의 통화', 'h2': '무서워서 거는 밤에<br>이렇게 흘러갑니다.', 'tt': '저녁 8시 41분', 'badge': '설치 기사 퇴근 후'},
 'kicker': '홈시큐리티 &middot; CCTV &middot; 출입 통제',
 'h1': '옆집에 도둑이 든 날 저녁,<br>그 골목의 전화가 옵니다.',
 'sub': 'CCTV 문의는 무슨 일이 있고 난 뒤의 저녁에 옵니다. 설치 기사는 퇴근했고, '
        '무서워서 건 전화가 부재중으로 남으면 그 집은 다음 검색 결과에 겁니다.',
 'cost': '설치 한 건은 80만원에서 130만원이고, 한 번 단 집은 카메라를 늘리고 이웃을 소개합니다. '
         '그 전화는 기사가 사다리를 내려놓은 뒤에 옵니다. 부재중을 만난 집은 그 밤에 다른 업체와 실사를 잡고, '
         '골목의 나머지 집도 그쪽으로 갑니다. 놓친 통화 하나가 놓친 골목 하나가 됩니다.',
 'call': [('고객', '8:41 PM', '어젯밤에 옆집에 도둑이 들었대요. 저희 집도 CCTV 달고 싶은데 얼마나 하고, 언제 올 수 있어요?'),
          ('Saleringo', '+11초', '많이 놀라셨겠어요. 먼저 현장 실사를 나가는데 <b>3만원</b>이고 설치하시면 그 금액은 빠집니다. '
                                 '단독주택 기준 <b>4채널 패키지 78만원</b>(실외 2대, 실내 2대, 1TB 녹화기, 스마트폰 알림), '
                                 '<b>8채널 129만원</b>입니다. 실사는 <b>내일 오후 2시</b>와 <b>모레 오전 10시</b>가 비어 있습니다.'),
          ('고객', '8:43 PM', '이거 달면 도둑은 확실히 못 들어오는 거죠?'),
          ('Saleringo', '+8초', '카메라는 기록하고 알려 주는 장비라, 침입을 막아 준다고 약속드리지는 않습니다. '
                                '어디를 비추면 사각이 없어지는지는 사장님이 실사에서 직접 봐 드립니다. 내일 2시로 잡아 드릴까요?'),
          ('고객', '8:44 PM', '네, 2시에 와 주세요.'),
          ('Saleringo', '+7초', '내일 오후 2시 실사로 접수했습니다. 주소와 성함, 연락처를 남겨 주시면 확인 문자를 보내 드리고, '
                                '기사님 이름도 함께 알려 드리겠습니다.')],
 'refuse': [('침입을 막아 준다고 약속하지 않습니다.',
             '카메라는 기록하고 알리는 장비입니다. 달면 도둑이 못 들어온다는 말은 하지 않고, '
             '사각지대를 실사에서 봐 드린다는 데까지만 말합니다.'),
            ('지금 벌어지는 일에는 조언하지 않습니다.',
             '누가 집에 들어온 것 같다는 전화에는 먼저 112에 신고하시라고 안내하고, 곧바로 담당자에게 연결합니다. '
             '문을 잠그라거나 나가서 확인해 보라는 말은 AI가 할 말이 아닙니다.'),
            ('요금표에 없는 구성을 만들지 않습니다.',
             '사장님이 넣어 둔 채널 수별 패키지와 실사비만 말합니다. 기존 카메라 재활용이나 표에 없는 조합은 '
             '&ldquo;실사 후 견적&rdquo;으로 남깁니다.'),
            ('남의 집을 비추는 설치를 약속하지 않습니다.',
             '옆집 대문이나 공용 복도, 도로를 비추는 각도는 개인정보보호법에 걸릴 수 있습니다. '
             '되는지 안 되는지는 사장님이 현장에서 판단합니다.')],
 'fields': ['설치 장소(단독 · 빌라 · 상가)와 층수', '희망 채널 수와 실외 · 실내 구분', '문의 계기(침입 · 택배 분실 · 반려동물)',
            '요금표에서 안내한 패키지와 실사비', '실사 방문 일시와 배정 기사', '확인 문자 발송 기록'],
 'stages': ['문의 접수', '실사 예약', '현장 실사 · 견적', '설치', '앱 연동 · 사후 점검'],
 'lead': '옆집에 도둑이 든 저녁에 겁니다. 실사비와 패키지만 안내하고, 도둑을 막아 준다는 말은 하지 않습니다.',
 'group': 2,
 'en': {
  'name': 'Home security & CCTV installers', 'owner': 'the installer',
  'kicker': 'Home security &middot; CCTV &middot; access control',
  'h1': 'The call comes the evening<br>after the house next door was hit.',
  'sub': 'Nobody prices cameras on a calm afternoon. The inquiry arrives the night after a break-in on the street, '
         'the installer is off the ladder, and a frightened caller who reaches voicemail phones the next result.',
  'cost': 'An install is a $1,300 to $2,200 ticket, and the house that gets one adds cameras later and sends the neighbours. '
          'The call lands after the van is parked for the night. The household that hits voicemail books a survey with '
          'somebody else before bed, and the rest of the street follows them. A missed call is a missed street.',
  'call': [('Customer', '8:41 PM', 'Our neighbours were burgled last night. We want cameras on our house &mdash; what does it cost, and how soon can someone come?'),
           ('Saleringo', '+11 s', 'That is a horrible thing to have next door. The first step is a site survey at <b>$49</b>, credited back if you go ahead. '
                                  'For a detached house the <b>four-camera package is $1,290</b> (two outdoor, two indoor, a 1 TB recorder and phone alerts) and '
                                  'the <b>eight-camera package is $2,190</b>. I can survey <b>tomorrow at 2:00 PM</b> or <b>Thursday at 10:00 AM</b>.'),
           ('Customer', '8:43 PM', 'And once it is in, nobody is getting in, right?'),
           ('Saleringo', '+8 s', 'Cameras record and alert &mdash; I will not promise you they stop a burglar. What the installer can do at the survey is '
                                 'show you where to point them so there is no blind side. Shall I hold tomorrow at two?'),
           ('Customer', '8:44 PM', 'Yes, two o&rsquo;clock.'),
           ('Saleringo', '+7 s', 'Survey held for tomorrow at 2:00 PM. If you give me the address, your name and a mobile number, I will text '
                                 'the confirmation with the installer&rsquo;s name.')],
  'refuse': [('It never promises a system will stop a burglary.',
              'A camera records and alerts; it does not keep anyone out. The AI says what the kit does and leaves the blind spots to the survey.'),
             ('It never advises during a break-in.',
              'A caller who thinks someone is in the house is told to call the police first, then put straight through to a person. '
              'Lock the door, go and look, stay quiet &mdash; none of that is the AI&rsquo;s to say.'),
             ('It never assembles a package that is not on the sheet.',
              'It quotes the per-channel packages and the survey fee the installer loaded. Reusing old cameras or any other combination is logged as &ldquo;quote after survey&rdquo;.'),
             ('It never promises a camera pointed at someone else&rsquo;s property.',
              'A lens on the neighbour&rsquo;s door, a shared hallway or the street can break privacy law. Whether it can be done is decided by the installer on site.')],
  'fields': ['Property type (house, flat, shop) and floors', 'Channels wanted, indoor and outdoor', 'What prompted the call (break-in, parcel theft, pets)',
             'Package and survey fee quoted from the sheet', 'Survey date and installer assigned', 'Confirmation text sent'],
  'stages': ['Inquiry', 'Survey booked', 'Site survey and quote', 'Installed', 'App set up and follow-up check'],
  'when': {'eyebrow': 'A call the evening after a break-in next door', 'h2': 'While the street is frightened,<br>this is how it goes.', 'tt': '8:41 PM', 'badge': 'installer off the ladder'},
  'lead': 'The call comes the evening after the house next door was hit. It quotes the survey and the packages on your sheet, and never promises a camera stops a burglar.',
  'room': 'home-property',
  'room_d': 'The 8:41 PM call after the neighbours&rsquo; break-in: packages quoted from your own sheet and a survey held for two &mdash; with no promise that a camera keeps anyone out.',
  'room_no': ('0', 'burglaries promised prevented over the phone'),
 },
},
{
 'slug': 'solar', 'owner': '대표님', 'name': '태양광 · 에너지 설비', 'photo': ph('PENDING'),
 'when': {'eyebrow': '고지서를 받은 주말 아침의 통화', 'h2': '시공팀이 지붕 위에 있는 토요일에<br>이렇게 흘러갑니다.', 'tt': '토요일 9시 23분', 'badge': '시공팀 현장 출근'},
 'kicker': '태양광 &middot; ESS &middot; 에너지 설비',
 'h1': '전기요금 고지서가 온 토요일 아침에<br>태양광을 검색합니다.',
 'sub': '32만원짜리 고지서를 받은 사람은 그 주말 아침에 전화를 겁니다. 시공팀은 다른 집 지붕에 올라가 있고, '
        '사무실 전화는 월요일까지 울리기만 합니다.',
 'cost': '주택 태양광 한 건은 400만원에서 600만원이고, 상가와 공장은 그 열 배입니다. 문의는 고지서가 도착한 주말에 몰리고, '
         '그때 시공팀은 지붕 위에 있습니다. 월요일에 콜백을 받은 손님은 이미 토요일에 다른 업체와 실사를 잡았습니다. '
         '지붕은 한 번 올리면 이십 년을 갑니다. 그 손님은 이십 년 동안 다시 오지 않습니다.',
 'call': [('고객', '9:23 AM', '이번 달 전기요금이 32만원 나왔어요. 태양광 달면 얼마나 줄고, 설치비는 얼마예요?'),
          ('Saleringo', '+14초', '얼마나 줄어드는지는 지붕 방향과 그늘, 계약 종별에 따라 집마다 달라서 전화로는 말씀드리지 않습니다. '
                                 '요금표 기준으로 <b>주택용 3kW 기본 시공이 480만원</b>이고, 먼저 현장 실사를 나가는데 <b>5만원</b>이며 '
                                 '계약하시면 빠집니다. 실사는 <b>화요일 오전 10시</b>와 <b>수요일 오후 2시</b>가 비어 있습니다.'),
          ('고객', '9:25 AM', '정부 보조금 받으면 반값이라던데, 저희 집도 되나요?'),
          ('Saleringo', '+9초', '보조금은 지자체 공고와 건물 조건에 따라 대상이 갈려서 제가 된다 안 된다 말씀드릴 수 없습니다. '
                                '대표님이 실사 때 건축물대장을 보고 어느 공고에 해당하는지 안내드립니다. 화요일 10시로 잡아 드릴까요?'),
          ('고객', '9:26 AM', '네, 화요일 오전이요.'),
          ('Saleringo', '+7초', '화요일 오전 10시 실사로 접수했습니다. 주소와 성함, 연락처를 남겨 주시면 확인 문자를 보내 드리고, '
                                '최근 고지서를 준비해 두시면 실사가 빠릅니다.')],
 'refuse': [('회수 기간과 절감액을 말하지 않습니다.',
             '몇 년이면 본전이라는 말은 지붕과 그늘, 계약 종별을 보기 전에는 누구도 할 수 없습니다. '
             '요금표의 시공 금액과 실사비만 말하고 실사를 잡습니다.'),
            ('보조금 대상 여부를 단정하지 않습니다.',
             '지자체 공고는 해마다 바뀌고 건물마다 조건이 다릅니다. 어느 공고에 해당하는지는 대표님이 서류를 보고 안내합니다.'),
            ('지붕 안전은 전화로 답하지 않습니다.',
             '슬레이트 지붕에 올려도 되는지, 하중을 견디는지, 누수가 생기지 않는지는 현장을 본 사람의 판단입니다. '
             '그 질문은 바로 사람에게 넘깁니다.'),
            ('한전 계약과 상계 처리를 대신 판단하지 않습니다.',
             '상계거래 신청과 계약 종별 변경은 한전 규정과 계량기 상태로 정해집니다. AI는 문의 사실만 적고 실사 항목으로 넘깁니다.')],
 'fields': ['건물 유형(단독 · 빌라 · 상가 · 공장)과 지붕 형태', '최근 월 전기요금과 계약 종별', '희망 용량과 설치 목적(자가 소비 · 판매)',
            '요금표에서 안내한 기본 시공 금액과 실사비', '실사 방문 일시', '보조금 · 상계 · 지붕 문의 여부'],
 'stages': ['문의 접수', '실사 예약', '현장 실사 · 견적', '계약 · 인허가', '시공 · 계통 연결'],
 'lead': '전기요금 고지서를 받은 토요일 아침에 겁니다. 절감액과 회수 기간은 말하지 않고, 실사비만 안내하고 실사를 잡습니다.',
 'group': 2,
 'en': {
  'name': 'Solar & energy installers', 'owner': 'the installer',
  'kicker': 'Solar &middot; battery storage &middot; energy systems',
  'h1': 'A $340 electricity bill<br>makes a Saturday-morning phone call.',
  'sub': 'The household that opens a big bill on Friday night searches for solar on Saturday morning. '
         'The crew is on somebody else&rsquo;s roof, and the office line rings until Monday.',
  'cost': 'A residential system is a fifteen-to-twenty-thousand-dollar job, and a commercial roof is ten times that. Inquiries cluster on the '
          'weekend the bills land, which is exactly when the crew is up a ladder. The caller who gets a Monday callback booked a survey with '
          'another installer on Saturday. A roof is done once in twenty years; that customer does not come back for twenty years.',
  'call': [('Customer', '9:23 AM', 'Our electricity bill just came in at three hundred and forty dollars. How much would solar cut it, and what does a system cost?'),
           ('Saleringo', '+14 s', 'How much it cuts depends on your roof direction, shading and your tariff, so I do not give a savings figure over the phone. '
                                  'From the price sheet, a <b>six-kilowatt residential system starts at $16,800</b>, and the first step is a site survey at <b>$150</b>, '
                                  'credited back if you sign. I can survey <b>Tuesday at 10:00 AM</b> or <b>Wednesday at 2:00 PM</b>.'),
           ('Customer', '9:25 AM', 'I heard the rebate covers half of it. Do we qualify?'),
           ('Saleringo', '+9 s', 'Rebate eligibility depends on the current programme rules and on the building, so I cannot tell you yes or no. '
                                 'The installer checks the paperwork at the survey and tells you which programme you fall under. Shall I hold Tuesday at ten?'),
           ('Customer', '9:26 AM', 'Tuesday morning, yes.'),
           ('Saleringo', '+7 s', 'Survey held for Tuesday at 10:00 AM. Give me the address, your name and a mobile number and I will text the confirmation. '
                                 'Having the last bill to hand makes the survey quicker.')],
  'refuse': [('It never states a payback period or a savings figure.',
              'How many years until it pays for itself is a number nobody can give before seeing the roof, the shade and the tariff. It quotes the system price and the survey fee and books the survey.'),
             ('It never rules on rebate eligibility.',
              'Programmes change every year and the conditions differ by building. Which one applies is the installer&rsquo;s call, with the paperwork in front of them.'),
             ('It never answers a roof-safety question.',
              'Whether an old tile roof takes the load, whether panels can go on a slate roof, whether it will leak &mdash; those go straight to a person.'),
             ('It never decides the grid-connection paperwork for you.',
              'Net-metering applications and tariff changes are set by the utility&rsquo;s rules and the meter on the wall. The AI records the question and leaves it for the survey.')],
  'fields': ['Building type (house, flat, shop, factory) and roof', 'Latest monthly bill and tariff', 'System size wanted and purpose (self-use or export)',
             'System price and survey fee quoted from the sheet', 'Survey date', 'Rebate, metering and roof questions raised'],
  'stages': ['Inquiry', 'Survey scheduled', 'Roof survey and quote', 'Contract and permits', 'Installed and connected'],
  'when': {'eyebrow': 'A Saturday-morning call with the bill in hand', 'h2': 'While the crew is on another roof,<br>this is how it goes.', 'tt': 'Saturday 9:23 AM', 'badge': 'crew up the ladder'},
  'lead': 'The bill arrives Friday, the call comes Saturday. It quotes the system price and the survey fee, books the survey, and never gives a payback period or a rebate answer.',
  'room': 'home-property',
  'room_d': 'The Saturday-morning call with a $340 bill: system price and survey fee from your sheet, a survey held for Tuesday &mdash; and no savings figure, no payback period, no rebate verdict.',
  'room_no': ('0', 'payback periods or rebate verdicts given on the phone'),
 },
},
{
 'slug': 'it-repair', 'owner': '사장님', 'name': '컴퓨터 · 휴대폰 수리', 'photo': ph('PENDING'),
 'when': {'eyebrow': '마감 전날 밤의 통화', 'h2': '노트북이 안 켜지는 밤 아홉 시에<br>이렇게 흘러갑니다.', 'tt': '밤 9시 04분', 'badge': '매장 마감 후'},
 'kicker': '컴퓨터 &middot; 노트북 &middot; 휴대폰 수리',
 'h1': '노트북은 발표 전날 밤에<br>안 켜집니다.',
 'sub': '수리 전화는 급한 사람이 겁니다. 내일 아침까지 내야 할 파일이 그 안에 있고, '
        '매장은 일곱 시에 닫았습니다. 안 받으면 그 손님은 밤새 다른 매장을 검색합니다.',
 'cost': '수리 한 건은 5만원에서 30만원이고, 한 번 살려 준 손님은 집안 기기를 다 들고 옵니다. 그 전화는 마감 뒤에, '
         '마감이 있는 사람에게서 옵니다. 부재중을 만난 손님은 아침 아홉 시에 다른 매장 앞에 서 있고, '
         '급한 손님일수록 다시 걸지 않습니다.',
 'call': [('고객', '9:04 PM', '노트북이 갑자기 안 켜져요. 내일 아침까지 발표 자료를 내야 하는데, 고칠 수 있나요? 얼마나 해요?'),
          ('Saleringo', '+12초', '급하시겠어요. 안 켜지는 원인은 열어 봐야 알아서 수리비는 진단 뒤에 정해집니다. '
                                 '<b>진단비 2만원</b>이고 수리하시면 빠지며, 노트북 전원 계통 수리는 요금표 기준 <b>5만원에서 18만원 사이</b>입니다. '
                                 '내일 <b>오전 9시</b> 오픈과 동시에 첫 순번으로 봐 드릴 수 있습니다.'),
          ('고객', '9:06 PM', '자료는 살릴 수 있는 거죠? 백업을 안 해 놨어요.'),
          ('Saleringo', '+8초', '저장장치 상태를 봐야 하는 일이라 살릴 수 있다고 약속드리지는 않습니다. 사장님이 진단하면서 '
                                '자료가 어떤 상태인지 먼저 확인하고 바로 알려 드립니다. 내일 9시 첫 순번으로 잡아 드릴까요?'),
          ('고객', '9:07 PM', '네, 9시에 바로 갈게요.'),
          ('Saleringo', '+7초', '내일 오전 9시 첫 순번으로 접수했습니다. 모델명과 성함, 연락처를 남겨 주시면 확인 문자를 보내 드리고, '
                                '충전기도 같이 가져오시면 진단이 빠릅니다.')],
 'refuse': [('데이터 복구를 보장하지 않습니다.',
             '저장장치가 어떤 상태인지는 열어 봐야 압니다. 살릴 수 있다는 말도, 못 살린다는 말도 하지 않고, '
             '진단 뒤 사장님이 먼저 확인해 알려 드린다고만 말합니다.'),
            ('진단 전에 수리비를 확정하지 않습니다.',
             '안 켜지는 노트북의 원인은 어댑터일 수도, 메인보드일 수도 있습니다. 요금표의 진단비와 수리비 범위만 말합니다.'),
            ('&ldquo;자료 날아간 거예요?&rdquo;에 답하지 않습니다.',
             '켜졌다 꺼졌다 한다, 이상한 소리가 난다는 말을 듣고 파일이 남아 있는지 판단하는 것은 사람의 일입니다. '
             '증상은 원문대로 적고 사장님에게 넘깁니다.'),
            ('잠금 해제와 계정 우회는 접수하지 않습니다.',
             '비밀번호를 모르는 휴대폰, 남의 계정이 묶인 기기는 소유 확인 없이 받지 않습니다. 사장님이 매장에서 신분과 구매 기록을 확인합니다.')],
 'fields': ['기기 종류 · 모델명 · 구입 시기', '증상 원문(안 켜짐 · 액정 · 침수 · 느림)', '백업 여부와 데이터 복구 요청',
            '요금표의 진단비와 수리비 범위', '입고 예약 시간과 손님의 마감 기한', '확인 문자 발송 기록'],
 'stages': ['문의 접수', '입고 예약', '진단 · 견적 안내', '수리', '출고 · 데이터 확인'],
 'lead': '마감 전날 밤 아홉 시에 노트북이 안 켜집니다. 진단비와 범위만 말하고, 자료가 살아 있는지는 사장님에게 남깁니다.',
 'group': 3,
 'en': {
  'name': 'Computer & phone repair', 'owner': 'the shop owner',
  'kicker': 'Computer &middot; laptop &middot; phone repair',
  'h1': 'Laptops die the night<br>before the deadline.',
  'sub': 'Repair calls come from people in a hurry. The file due at nine is on the drive, the shop shut at seven, '
         'and a caller who gets voicemail spends the night searching for another shop.',
  'cost': 'A repair is a $60 to $400 ticket, and the customer whose files you saved brings every device in the house from then on. '
          'The call comes after closing, from someone with a deadline. The one who reaches voicemail is standing outside a competitor '
          'at nine the next morning, and the more urgent the customer, the less likely they call back.',
  'call': [('Customer', '9:04 PM', 'My laptop will not turn on and my presentation is due at nine tomorrow. Can you fix it, and what will it cost?'),
           ('Saleringo', '+12 s', 'That is a bad night to have. Why it will not start is something we only know once it is open, so the repair price comes after the diagnosis. '
                                  'The <b>diagnostic is $35</b>, credited back if you repair, and laptop power faults run <b>$80 to $260</b> on the price list. '
                                  'I can put you first in the queue when the shop opens at <b>9:00 AM</b> tomorrow.'),
           ('Customer', '9:06 PM', 'And my files will be fine, right? I never backed it up.'),
           ('Saleringo', '+8 s', 'That depends on the state of the drive, so I will not promise you the files are safe. The owner checks the drive first thing during '
                                 'the diagnosis and tells you straight away. Shall I hold the first slot at nine?'),
           ('Customer', '9:07 PM', 'Yes, I will be there at nine.'),
           ('Saleringo', '+7 s', 'First slot at 9:00 AM tomorrow, held. Give me the model, your name and a mobile number and I will text the confirmation. '
                                 'Bring the charger too &mdash; it makes the diagnosis quicker.')],
  'refuse': [('It never guarantees data recovery.',
              'What state a drive is in is known only once the machine is open. It neither promises the files are safe nor says they are lost; it says the owner checks first.'),
             ('It never quotes a repair price before the diagnosis.',
              'A laptop that will not start might need a charger or a motherboard. It gives the diagnostic fee and the price-list range, nothing narrower.'),
             ('It never answers &ldquo;is my data gone?&rdquo;',
              'Deciding from a clicking noise or a flickering screen whether the files survived is a person&rsquo;s job. The symptom is written down verbatim and handed to the owner.'),
             ('It never takes an unlock or an account bypass.',
              'A phone with an unknown passcode or a device tied to someone else&rsquo;s account is not booked without proof of ownership. The owner checks ID and the receipt at the counter.')],
  'fields': ['Device, model and age', 'Symptom in the caller&rsquo;s words (dead, screen, water, slow)', 'Backed up or not, and any recovery request',
             'Diagnostic fee and repair range from the price list', 'Drop-off slot and the customer&rsquo;s deadline', 'Confirmation text logged'],
  'stages': ['Inquiry', 'Drop-off booked', 'Diagnosed and quoted', 'Repaired', 'Collected and data checked'],
  'when': {'eyebrow': 'A call the night before a deadline', 'h2': 'While the shop is dark and the file is due,<br>this is how it goes.', 'tt': '9:04 PM', 'badge': 'shutters down'},
  'lead': 'The laptop dies at nine the night before the deadline. It quotes the diagnostic fee and the range, books the first slot, and leaves whether the files survived to the owner.',
  'room': 'vehicle-plant-storage',
  'room_d': 'The 9:04 PM dead laptop the night before a deadline: diagnostic fee and range quoted, first slot at nine held &mdash; and no promise that the files are still there.',
  'room_no': ('0', 'data recoveries guaranteed before the drive is opened'),
 },
},
{
 'slug': 'courier', 'owner': '사장님', 'name': '택배 · 퀵서비스 · 용달', 'photo': ph('PENDING'),
 'when': {'eyebrow': '가게 문 열기 전의 통화', 'h2': '기사가 전부 도로 위에 있는 아침에<br>이렇게 흘러갑니다.', 'tt': '오전 7시 30분', 'badge': '배차 담당 운전 중'},
 'kicker': '퀵서비스 &middot; 당일 배송 &middot; 용달',
 'h1': '오늘 안에 보내야 하는 박스는<br>일곱 시 반에 전화합니다.',
 'sub': '당일 배송 문의는 가게가 문을 열기 전에 옵니다. 그 시간에 배차 담당은 운전 중이고, '
        '벨이 울리다 끊기면 그 가게는 앱을 켭니다.',
 'cost': '퀵 한 건은 2만원에서 6만원이지만, 매일 보내는 가게 하나는 한 달에 백만원입니다. 그 가게가 처음 거는 전화는 급한 아침에 오고, '
         '한 번 받아 준 곳에 계속 겁니다. 부재중을 만난 가게는 플랫폼 앱으로 넘어가고, 그 뒤로 수수료를 떼인 채로도 돌아오지 않습니다.',
 'call': [('고객', '7:30 AM', '성수동 케이크 가게인데요, 오늘 오전 중에 판교로 박스 세 개 보내야 해요. 되나요? 얼마예요?'),
          ('Saleringo', '+13초', '네, 몇 가지만 여쭙겠습니다. 픽업 주소와 도착 주소, 박스 크기와 무게, 그리고 몇 시까지 도착해야 하는지요.'),
          ('고객', '7:31 AM', '성수동 연무장길에서 판교 테크노밸리요. 40센티 박스 세 개, 하나에 3킬로쯤이고, 11시까지 가야 해요.'),
          ('Saleringo', '+11초', '성수에서 판교는 요금표 기준 <b>다마스 4만 5천원</b>입니다. 40센티 박스 세 개는 오토바이에 실리지 않아 '
                                 '다마스로 잡아야 합니다. 11시 도착은 배차와 도로 사정에 달려 있어서 제가 약속드릴 수는 없고, '
                                 '사장님이 배차를 확인하고 <b>8시 전에</b> 연락드립니다.'),
          ('고객', '7:32 AM', '네, 그럼 그렇게 해 주세요. 달콤제과 김민서예요.'),
          ('Saleringo', '+7초', '달콤제과 김민서 님, 성수 픽업, 판교 도착, 40센티 박스 세 개, 11시 마감으로 접수했습니다. '
                                '연락처 남겨 주시면 접수 문자를 보내고, 배차가 되는 대로 기사 번호를 보내 드리겠습니다.')],
 'refuse': [('확인되지 않은 도착 시간을 약속하지 않습니다.',
             '몇 시까지 간다는 말은 기사가 배차되고 사장님이 확인한 뒤에만 합니다. 그 전에는 마감 시간을 적고 &ldquo;배차 확인 후 연락&rdquo;으로 남깁니다.'),
            ('위험물과 살아 있는 것은 접수하지 않습니다.',
             '드라이아이스, 리튬 배터리 묶음, 부탄가스, 강아지 한 마리. 이런 말이 나오면 접수를 멈추고 사장님에게 넘깁니다.'),
            ('요금표 구역 밖의 금액을 만들지 않습니다.',
             '사장님이 넣어 둔 구역별 · 차종별 요금만 말합니다. 표에 없는 지역이나 1톤 이상은 &ldquo;확인 후 안내&rdquo;로 남깁니다.'),
            ('파손과 분실의 보상을 전화로 정하지 않습니다.',
             '깨진 케이크를 물어 주는지, 얼마를 물어 주는지는 약관과 사진으로 사장님이 정합니다. AI는 신고 내용만 그대로 적습니다.')],
 'fields': ['픽업 주소와 도착 주소', '물품 종류 · 박스 수 · 크기 · 무게', '요금표의 구역 요금과 차종(오토바이 · 다마스 · 1톤)',
            '픽업 희망 시간과 도착 마감', '위험물 · 생물 · 파손 주의 여부', '배차 확인 연락 기록'],
 'stages': ['접수', '배차 확인', '픽업', '배송 중', '도착 · 정산'],
 'lead': '가게 문 열기 전 일곱 시 반에 겁니다. 주소와 크기를 받아 구역 요금을 말하고, 도착 시간은 사장님이 확인한 뒤에만 답합니다.',
 'group': 3,
 'en': {
  'name': 'Couriers & same-day delivery', 'owner': 'the owner',
  'kicker': 'Couriers &middot; same-day delivery &middot; van hire',
  'h1': 'The box that has to go today<br>calls at half past seven.',
  'sub': 'Same-day jobs come in before the shop that needs them has opened. The dispatcher is driving, '
         'and a shop that hears the phone ring out opens an app instead.',
  'cost': 'One job is $30 to $90, but a shop that sends every day is worth a thousand a month. Its first call comes on a frantic morning, '
          'and it keeps calling whoever answered. The shop that reaches voicemail moves to a platform app and does not come back, '
          'even once the platform&rsquo;s cut starts to hurt.',
  'call': [('Customer', '7:30 AM', 'This is the cake shop on Mercer Street. I need three boxes in the business park across the river by late morning. Can you do it, and what does it cost?'),
           ('Saleringo', '+13 s', 'Yes &mdash; a few things first. The pickup address and the delivery address, the size and weight of the boxes, and the time they have to be there.'),
           ('Customer', '7:31 AM', 'Pickup at 40 Mercer Street, delivery to Riverside Business Park. Three sixteen-inch boxes, about seven pounds each, and they need to be there by eleven.'),
           ('Saleringo', '+11 s', 'Mercer Street to Riverside is <b>$65 by cargo van</b> on the rate card. Three sixteen-inch boxes will not go on a bike, so it has to be the van. '
                                  'Whether they land by eleven depends on the driver and the traffic, so I will not promise it &mdash; the owner checks the dispatch board '
                                  'and calls you <b>before eight</b>.'),
           ('Customer', '7:32 AM', 'Fine, do that. It is Sweetly Bakery, Mina Kim.'),
           ('Saleringo', '+7 s', 'Sweetly Bakery, Mina Kim: pickup Mercer Street, drop Riverside, three sixteen-inch boxes, eleven o&rsquo;clock deadline &mdash; logged. '
                                 'Give me a mobile number and I will text the job number, then the driver&rsquo;s number once dispatch confirms.')],
  'refuse': [('It never promises an arrival time the owner has not confirmed.',
              'A delivery time is said only after a driver is assigned and the owner has checked. Until then the deadline is written down and the job is marked &ldquo;confirm dispatch&rdquo;.'),
             ('It never takes hazardous or living cargo.',
              'Dry ice, a crate of lithium batteries, gas canisters, a puppy. The moment one of these comes up the AI stops booking and passes the call to a person.'),
             ('It never prices a run that is not on the rate card.',
              'It quotes the zone and vehicle rates the owner loaded. A postcode outside the zones or anything over a van is logged as &ldquo;price to confirm&rdquo;.'),
             ('It never settles a damage or loss claim on the phone.',
              'Whether a crushed cake is paid for, and how much, is decided by the owner from the terms and the photos. The AI records the report word for word.')],
  'fields': ['Pickup and delivery addresses', 'What it is, how many boxes, size and weight', 'Zone rate and vehicle from the rate card (bike, van, truck)',
             'Pickup window and delivery deadline', 'Hazardous, live or fragile flags', 'Dispatch confirmation call logged'],
  'stages': ['Job logged', 'Dispatch confirmed', 'Collected', 'On the road', 'Delivered and invoiced'],
  'when': {'eyebrow': 'A call before the shop has opened', 'h2': 'While every driver is on the road,<br>this is how it goes.', 'tt': '7:30 AM', 'badge': 'dispatcher driving'},
  'lead': 'The call comes at half past seven from a shop with three boxes to move. It takes the addresses, the size and the deadline, quotes the zone rate, and leaves the arrival time to the owner.',
  'room': 'vehicle-plant-storage',
  'room_d': 'The 7:30 AM call from a shop with three boxes to move: addresses, size and deadline taken, the zone rate quoted &mdash; and no arrival time promised until dispatch confirms.',
  'room_no': ('0', 'arrival times promised before a driver is assigned'),
 },
},
{
 'slug': 'print-signage', 'owner': '실장님', 'name': '인쇄 · 간판 · 현수막', 'photo': ph('PENDING'),
 'when': {'eyebrow': '오픈 전날 오후 다섯 시의 통화', 'h2': '출력기가 돌아가는 오후에<br>이렇게 흘러갑니다.', 'tt': '오후 5시 02분', 'badge': '실장님 재단 중'},
 'kicker': '인쇄 &middot; 간판 &middot; 현수막 &middot; 시트',
 'h1': '현수막은 오픈 전날<br>오후 다섯 시에 주문됩니다.',
 'sub': '급한 인쇄는 마감이 있는 사람이 마감 직전에 겁니다. 그 시간에 실장님은 출력기 앞이나 사다리 위에 있고, '
        '안 받으면 그 가게는 온라인 인쇄소에 파일을 올립니다.',
 'cost': '명함 한 통은 2만원이지만 그 가게의 오픈 현수막, 메뉴판, 간판, 시트지가 그 뒤에 붙어 있습니다. 첫 전화는 급할 때 오고, '
         '급할 때 받아 준 인쇄소가 그 가게의 인쇄소가 됩니다. 부재중을 만난 가게는 그날 밤 온라인 인쇄소에 올리고, 간판은 다른 데 맡깁니다.',
 'call': [('고객', '5:02 PM', '내일 오픈인데 현수막 하나랑 명함 200장 급하게 되나요?'),
          ('Saleringo', '+12초', '네, 규격과 파일부터 확인하겠습니다. 현수막은 어느 크기이고, 명함은 단면인지 양면인지, '
                                 '그리고 인쇄할 파일은 완성돼 있으신가요?'),
          ('고객', '5:03 PM', '현수막은 5미터짜리 가로로 걸 거고요, 명함은 단면이요. 파일은 디자이너가 준 게 있어요.'),
          ('Saleringo', '+11초', '요금표 기준 <b>현수막 5m&times;90cm 3만 5천원</b>, <b>명함 단면 200장 1만 8천원</b>입니다. '
                                 '파일을 <b>오늘 6시까지</b> 보내 주시면 실장님이 확인하고 내일 오전에 되는지 바로 연락드립니다. '
                                 '파일을 열어 보기 전에는 내일 된다고 약속드리지 않습니다.'),
          ('고객', '5:04 PM', '알겠어요. 근데 가게 앞에 간판도 새로 달고 싶은데, 그건 허가 받아야 해요?'),
          ('Saleringo', '+8초', '옥외 간판 허가는 위치와 크기, 구청 기준에 따라 달라서 제가 답할 수 있는 것이 아닙니다. '
                                '실장님이 파일 확인하실 때 함께 안내드리겠습니다. 상호와 연락처를 남겨 주시면 파일 받을 번호를 문자로 보내 드립니다.')],
 'refuse': [('파일을 확인하기 전에 납품일을 약속하지 않습니다.',
             '해상도가 낮거나 여백이 없거나 폰트가 깨진 파일은 내일 나올 수 없습니다. 파일을 연 실장님이 확인한 뒤에만 날짜를 말합니다.'),
            ('옥외 간판의 허가 여부를 판단하지 않습니다.',
             '옥외광고물법상 신고와 허가는 위치, 크기, 건물 층수에 따라 갈립니다. 그 질문은 실장님에게 넘기고 AI는 문의 사실만 적습니다.'),
            ('요금표에 없는 특수 인쇄 금액을 만들지 않습니다.',
             '박, 형압, 특수 지류, 대형 실사 출력처럼 표에 없는 것은 &ldquo;확인 후 견적&rdquo;으로 남깁니다. 정가만 말합니다.'),
            ('모니터의 색이 그대로 나온다고 약속하지 않습니다.',
             '화면 색과 인쇄 색은 다르고, 저해상도 파일은 확대하면 깨집니다. 색 재현과 품질은 시안 확인 뒤에 실장님이 답합니다.')],
 'fields': ['품목(현수막 · 명함 · 전단 · 간판)과 규격', '수량과 단면 · 양면 · 재질', '파일 상태(완성 파일 · 수정 필요 · 디자인 의뢰)',
            '요금표에서 안내한 정가', '희망 납품일과 실장님 확인 여부', '옥외 간판 허가 문의 여부'],
 'stages': ['문의 접수', '파일 접수 · 확인', '시안 확인 · 결제', '인쇄 · 제작', '납품 · 시공'],
 'lead': '오픈 전날 오후 다섯 시에 겁니다. 규격과 수량으로 정가를 말하고, 납품일은 파일을 확인한 뒤에만 답합니다.',
 'group': 5,
 'en': {
  'name': 'Print shops & signage', 'owner': 'the shop owner',
  'kicker': 'Print &middot; signage &middot; banners &middot; vinyl',
  'h1': 'The opening banner is ordered<br>at five the day before.',
  'sub': 'Rush print jobs come from people with a deadline, just before the deadline. The owner is at the printer or up a ladder, '
         'and a shop that gets no answer uploads the file to an online printer instead.',
  'cost': 'A box of business cards is $45, but behind it are the opening banner, the menu boards, the shop sign and the window vinyl. The first call comes when '
          'it is urgent, and the print shop that answered becomes the shop&rsquo;s print shop. The one that reached voicemail uploads online that night '
          'and gives the sign to someone else.',
  'call': [('Customer', '5:02 PM', 'We open tomorrow. Can you do a banner and two hundred and fifty business cards in a rush?'),
           ('Saleringo', '+12 s', 'Yes &mdash; size and artwork first. What size is the banner, are the cards single- or double-sided, and is the artwork finished?'),
           ('Customer', '5:03 PM', 'A ten-foot banner to hang across the front, cards single-sided. Our designer sent us the files.'),
           ('Saleringo', '+11 s', 'From the price list, a <b>10 ft &times; 3 ft vinyl banner is $89</b> and <b>250 single-sided cards are $45</b>. '
                                  'Send the files by <b>6:00 PM today</b> and the owner checks them and calls you back on whether tomorrow morning works. '
                                  'I will not promise tomorrow until the files have been opened.'),
           ('Customer', '5:04 PM', 'OK. We also want a new sign over the door &mdash; do we need a permit for that?'),
           ('Saleringo', '+8 s', 'Sign permits depend on the location, the size and the local rules, so that is not mine to answer. The owner will cover it when '
                                 'they call about the files. Give me the shop name and a mobile number and I will text you where to send the artwork.')],
  'refuse': [('It never promises a delivery date before the file is checked.',
              'Low resolution, no bleed, a missing font &mdash; any of them means tomorrow is not happening. The date is given only after the owner has opened the file.'),
             ('It never rules on whether an outdoor sign needs a permit.',
              'Signage law turns on location, size and the building. The question goes to the owner; the AI records that it was asked.'),
             ('It never prices a special finish that is not on the list.',
              'Foil, embossing, unusual stock, large-format photo prints &mdash; anything off the list is logged as &ldquo;quote to follow&rdquo;. It quotes list prices only.'),
             ('It never promises the print will match the screen.',
              'Screen colour and ink are different things, and a small file blown up to banner size falls apart. Colour and quality are the owner&rsquo;s answer, after the proof.')],
  'fields': ['Item (banner, cards, flyers, sign) and size', 'Quantity, sides and stock', 'Artwork status (print-ready, needs fixing, design wanted)',
             'List price quoted', 'Date wanted and whether the owner has confirmed it', 'Sign-permit question raised'],
  'stages': ['Inquiry', 'Artwork received and checked', 'Proof approved and paid', 'Printed and made', 'Delivered or installed'],
  'when': {'eyebrow': 'A call at five the day before an opening', 'h2': 'While the printer is running,<br>this is how it goes.', 'tt': '5:02 PM', 'badge': 'owner at the cutter'},
  'lead': 'The banner is ordered at five the day before the opening. It quotes list prices from the size and quantity, and never promises a date until the file has been checked.',
  'room': 'professional-public',
  'room_d': 'The 5:02 PM call the day before an opening: size, quantity and artwork status taken, list prices quoted &mdash; and no delivery date promised until the file has been opened.',
  'room_no': ('0', 'delivery dates promised before the artwork is opened'),
 },
},
]
