# -*- coding: utf-8 -*-
"""세 번째 묶음, 열 개 업종.

앞의 스물다섯 곳과 형식은 같고 문장은 하나도 겹치지 않는다. 이번 열 곳은 대부분
밤이 아니라 낮에 전화를 놓친다. 약사님은 조제대에, 치료사는 환자에게, 선생님은
현관에, 강사는 매트 위에 있어서다. 그래서 `when` 이 거의 다 낮이다.

  · 약국은 약사법 - 복약 지도는 약사만 한다. 용량과 병용 여부는 기계가 답하지 않는다.
  · 병원 대표번호는 검사 결과를 절대 읽지 않는다. 증상으로 진료과를 고르지도 않는다.
  · 물리치료·한의원·안경원은 "몇 번이면 낫나", "왜 침침한가"에 답하지 않는다.
  · 심리상담은 자해·자살 표현이 나오는 순간 예약을 멈추고 사람을 붙인다.
  · 어린이집과 음악학원은 하원 인계자와 차량 하차 장소를 전화로 바꾸지 않는다.

각 항목의 `en` 은 영어 사이트용이다. 번역이 아니라 그 나라 말투로 다시 썼고,
금액은 달러 기준 예시 요금표다.
"""

PH = 'https://images.pexels.com/photos/%s/pexels-photo-%s.jpeg'


def ph(i):
    return PH % (i, i)


TRADES3 = [
{
 'slug': 'pharmacy', 'owner': '약사님', 'name': '약국', 'photo': ph('PENDING'),
 'kicker': '약국 &middot; 조제 &middot; 일반의약품',
 'h1': '조제대에 손이 있는 동안<br>픽업 전화가 옵니다.',
 'sub': '처방전을 들고 나온 사람은 퇴근길에 찾을 수 있는지부터 묻습니다. '
        '못 받으면 길 건너 다른 약국에 걸고, 그 병원 앞 약국이 단골이 됩니다.',
 'cost': '약국 전화는 대부분 세 가지입니다. 몇 시까지 하는지, 이 약 있는지, 미리 조제해 둘 수 있는지. '
         '전부 30초면 답할 수 있는데, 그 30초가 조제 중에는 나지 않습니다. 놓친 전화는 한 번의 처방으로 '
         '끝나지 않습니다. 만성질환 처방은 두 달마다 돌아오고, 한 번 옮긴 단골은 그 병원 앞 약국에 남습니다.',
 'call': [('손님', '1:12 PM', '지금 병원에서 처방전 받았는데, 미리 조제해 두시면 퇴근길에 찾아갈 수 있을까요? 8시까지 하시나요?'),
          ('Saleringo', '+14초', '평일은 <b>저녁 8시 30분</b>까지입니다. 처방전을 사진으로 보내 주시면 접수해 두고, '
                                 '조제는 약사님이 원본을 확인한 뒤에 합니다. 오늘 <b>7시 이후</b> 찾으러 오시는 것으로 남겨 두겠습니다.'),
          ('손님', '1:14 PM', '그리고 혈압약이랑 같이 먹어도 되는 감기약 있으면 같이 챙겨 주세요.'),
          ('Saleringo', '+7초', '같이 드셔도 되는지는 약사님이 복용 중인 약을 보고 직접 안내드려야 해서, '
                                '그 질문은 그대로 전달해 두겠습니다. 오실 때 드시는 약 이름을 알려 주시면 됩니다.')],
 'refuse': [('용량과 복용 시간을 바꾸지 않습니다.',
             '&ldquo;반 알만 드세요&rdquo;, &ldquo;하루 두 번으로 줄이세요&rdquo; 같은 말은 복약 지도이고, 약사법상 약사만 합니다.'),
            ('두 약을 같이 먹어도 되는지 답하지 않습니다.',
             '복용 중인 약을 보고 약사님이 확인할 일입니다. 질문은 원문 그대로 약사님 화면에 남깁니다.'),
            ('증상을 듣고 약을 골라 주지 않습니다.',
             '&ldquo;머리가 아픈데 뭐 먹을까요&rdquo;에는 재고와 가격만 답하고, 어느 약이 맞는지는 약사님에게 넘깁니다.'),
            ('과다 복용이나 알레르기 반응이 나오면 예약을 멈춥니다.',
             '약을 잘못 먹었다, 숨이 막힌다, 두드러기가 번진다는 말이 나오면 응급 안내를 읽고 약사님을 바로 연결합니다.')],
 'fields': ['처방전 접수 여부와 받은 시각', '문의한 품목과 재고 상태', '약속한 픽업 시간',
            '일반의약품 가격표 기준 안내 금액', '병용 · 용량 질문 약사님 전달 표시', '확인 문자 발송 기록'],
 'stages': ['문의 접수', '처방전 접수', '약사님 조제', '픽업', '재처방 안내'],
 'when': {'eyebrow': '조제 중의 통화', 'h2': '약사님 손이 조제대에 있는 동안<br>이렇게 흘러갑니다.',
          'tt': '조제 중', 'badge': '조제대를 떠날 수 없는 시간'},
 'lead': '조제 중에 오는 픽업 전화. 처방전을 접수해 두되, 용량과 병용 여부는 약사님에게 그대로 넘깁니다.',
 'group': 0,
 'en': {
  'name': 'Pharmacy', 'owner': 'the pharmacist',
  'kicker': 'Pharmacy &middot; prescriptions &middot; over the counter',
  'h1': 'The pickup call comes<br>while the pills are being counted.',
  'sub': 'Someone leaving the doctor wants to know if it can be ready after work. '
         'Unanswered, they drive to the chain across the road, and the refill every two months goes with them.',
  'cost': 'Almost every pharmacy call is one of three: what time do you close, do you have this, can you fill it before I get there. '
          'Each takes thirty seconds to answer, and none of those seconds exist while a prescription is being filled. '
          'A missed call is not one prescription. Chronic scripts come back every two months, and a customer who moved once stays moved.',
  'call': [('Customer', '1:12 PM', 'I just left the doctor with a prescription. Can you have it ready if I come by after work? Are you open until eight?'),
           ('Saleringo', '+14 s', 'We are open until <b>8:30 PM</b> on weekdays. Send a photo of the prescription and I will log it for pickup after <b>7 PM</b>; '
                                  'the pharmacist fills it once she has the original in hand.'),
           ('Customer', '1:14 PM', 'And could you add a cold medicine that is safe with my blood-pressure pills?'),
           ('Saleringo', '+7 s', 'Whether two medicines can be taken together is for the pharmacist to check against what you already take, '
                                 'so I have passed that question to her exactly as you said it. Bring the names of your current medicines when you come.')],
  'refuse': [('Never changes a dose or a schedule.',
              '"Take half" or "drop to twice a day" is counselling, and by law only the pharmacist gives it.'),
             ('Never says two medicines are safe together.',
              'That is checked against what the patient already takes. The question is left on the pharmacist\'s screen, word for word.'),
             ('Never picks a medicine for a symptom.',
              '"What should I take for a headache" gets stock and price from the list, and the choice goes to the pharmacist.'),
             ('An overdose or an allergic reaction ends the booking.',
              'Took the wrong pills, cannot breathe, a rash that is spreading: the AI reads the emergency instruction and puts the pharmacist on the line.')],
  'fields': ['Prescription received, and when', 'Item asked for and stock status', 'Pickup time promised',
             'Price quoted from the over-the-counter list', 'Dose or interaction question flagged to the pharmacist', 'Confirmation text sent'],
  'stages': ['Enquiry', 'Prescription logged', 'Filled by the pharmacist', 'Pickup', 'Refill reminder'],
  'when': {'eyebrow': 'A call mid-fill', 'h2': 'While both hands are on<br>a prescription, this is how it goes.',
           'tt': 'Mid-fill', 'badge': 'Cannot leave the bench'},
  'lead': 'The pickup call lands mid-fill. The AI logs the prescription and the time; doses and interactions stay with the pharmacist.',
  'room': 'health-care',
  'room_d': 'Refill pickups and stock checks answered while the pharmacist is counting. Every dose and interaction question reaches her as written, never answered.',
  'room_no': ('0', 'dosage changes the AI may suggest'),
 },
},
{
 'slug': 'hospital-outpatient', 'owner': '원장님', 'name': '병원 외래 · 대표번호', 'photo': ph('PENDING'),
 'kicker': '병원 외래 &middot; 대표번호 &middot; 원무과',
 'h1': '아침 아홉 시에는<br>모든 회선이 통화 중입니다.',
 'sub': '외래 예약, 진료의뢰서 질문, &ldquo;김 교수님 무슨 요일에 계세요&rdquo;가 개원 직후 대표번호로 한꺼번에 몰립니다. '
        '통화 중 신호를 세 번 들은 환자는 다른 병원에 겁니다.',
 'cost': '대표번호의 문제는 밤이 아니라 아침입니다. 9시부터 10시 사이에 하루 통화의 3분의 1이 들어오고, '
         '원무과 인원은 그 시간에도 창구 앞 줄을 받고 있습니다. 통화 중 신호로 끊긴 외래 예약은 어디에도 남지 않아서 '
         '몇 명을 놓쳤는지 병원도 모릅니다. 대부분은 &ldquo;몇 시가 비어 있나요&rdquo; 한 문장이라 사람이 아니어도 답할 수 있습니다.',
 'call': [('환자', '9:04 AM', '정형외과 김 교수님 외래 이번 주에 예약할 수 있나요? 다른 병원에서 찍은 엑스레이 CD 가져가면 되나요?'),
          ('Saleringo', '+19초', '김 교수님 외래는 <b>화 · 목 오전</b>이고, 이번 주 <b>목요일 10시 40분</b>이 비어 있습니다. '
                                 '다른 병원 영상 CD와 진료의뢰서를 가져오시면 접수 때 등록됩니다. 초진이시면 20분 전에 오시면 됩니다.'),
          ('환자', '9:06 AM', '목요일로 할게요. 무릎이 자꾸 붓는데 수술해야 할까요?'),
          ('Saleringo', '+6초', '그건 교수님이 영상을 보고 판단하실 부분이라 제가 말씀드릴 수 없습니다. 목요일 10시 40분으로 예약해 두었고, '
                                '성함과 생년월일을 남겨 주시면 확인 문자를 보내 드리겠습니다.')],
 'refuse': [('검사 결과를 전화로 읽지 않습니다.',
             '피검사 수치든 영상 소견이든, 본인 확인을 거쳐 의사가 설명할 일입니다. 결과 문의는 담당 과에 전달만 합니다.'),
            ('증상을 듣고 진료과를 정해 주지 않습니다.',
             '환자가 말한 과로 잡고, 어느 과인지 모르겠다고 하면 원무과 상담으로 넘깁니다. 과를 고르는 것도 판단입니다.'),
            ('입원 병상, 수술 날짜, 최종 진료비를 확답하지 않습니다.',
             '고시된 비급여 요금표의 금액까지만 말합니다. 병실과 수술 일정은 담당 과가 정하고, 급여 적용은 진료 뒤에 갈립니다.'),
            ('가슴 통증이나 호흡 곤란이 나오면 예약을 멈춥니다.',
             '응급 안내 문구를 읽고 119와 응급실을 안내한 뒤, 지정된 간호사에게 바로 연결합니다.')],
 'fields': ['진료과와 지정 교수', '초진 · 재진 구분', '진료의뢰서와 외부 영상 지참 여부',
            '예약 시각과 접수 시각', '검사 결과 · 서류 문의 담당 과 전달 표시', '비급여 요금표 기준 안내 금액'],
 'stages': ['문의 접수', '외래 예약', '접수', '진료', '재진 · 검사 예약'],
 'when': {'eyebrow': '아침 아홉 시의 통화', 'h2': '대표번호가 통화 중인 동안<br>이렇게 흘러갑니다.',
          'tt': '오전 피크', 'badge': '회선이 모두 찬 시간'},
 'lead': '아침 아홉 시 대표번호가 통화 중일 때. 외래 일정표에서만 잡고, 검사 결과는 읽지 않습니다.',
 'group': 0,
 'en': {
  'name': 'Hospitals & outpatient', 'owner': 'the director',
  'kicker': 'Hospitals &middot; outpatient &middot; the main number',
  'h1': 'At nine in the morning<br>every line is busy.',
  'sub': 'Outpatient bookings, referral questions and "which day is Dr Kim in" all hit the main number at opening. '
         'A patient who hears the busy tone three times tries the hospital across town.',
  'cost': 'The main number\'s problem is not the night; it is the first hour. A third of the day\'s calls arrive between nine and ten, '
          'and the same admissions staff are serving the queue at the counter. A booking lost to a busy tone leaves no record, '
          'so the hospital never learns how many it lost. Most of them were one sentence: which slot is free.',
  'call': [('Patient', '9:04 AM', 'Can I book Dr Kim in orthopaedics this week? I have X-rays on a CD from another clinic.'),
           ('Saleringo', '+19 s', 'Dr Kim sees outpatients on <b>Tuesday and Thursday mornings</b>, and <b>Thursday at 10:40</b> is open. '
                                  'Bring the CD and your referral letter and they will be registered at check-in. New patients should arrive twenty minutes early.'),
           ('Patient', '9:06 AM', 'Thursday then. My knee keeps swelling. Will I need surgery?'),
           ('Saleringo', '+6 s', 'That is for Dr Kim to decide after looking at the images, so I cannot say. You are booked for Thursday at 10:40; '
                                 'give me your name and date of birth and I will text a confirmation.')],
  'refuse': [('Never reads a test result over the phone.',
              'A blood value or an imaging report is explained by a doctor after identity is verified. The AI only passes the request to the ward.'),
             ('Never picks a department from symptoms.',
              'It books the department the patient names. If they do not know which, admissions decides; choosing one is a judgement too.'),
             ('Never promises a bed, a surgery date or a final bill.',
              'It quotes the published self-pay list and stops. Beds and theatre dates belong to the department; what insurance covers is settled after the visit.'),
             ('Chest pain or trouble breathing ends the booking.',
              'The AI reads the emergency instruction, tells the caller to call the emergency number or come to the ER, and connects the duty nurse.')],
  'fields': ['Department and named doctor', 'New or returning patient', 'Referral letter and outside images on hand',
             'Booked slot and check-in time', 'Result or records request passed to the ward', 'Self-pay price quoted from the published list'],
  'stages': ['Enquiry', 'Outpatient booked', 'Check-in', 'Consultation', 'Follow-up or tests'],
  'when': {'eyebrow': 'The nine o\'clock call', 'h2': 'While the main number is busy,<br>this is how it goes.',
           'tt': 'Morning peak', 'badge': 'Every line taken'},
  'lead': 'Nine in the morning and the main number is busy. The AI books only from the outpatient timetable and never reads a result.',
  'room': 'health-care',
  'room_d': 'The overflow from the main number at opening: outpatient slots booked from the timetable, referrals logged, and every result request passed to the ward unread.',
  'room_no': ('0', 'test results the AI reads out'),
 },
},
{
 'slug': 'physio-rehab', 'owner': '원장님', 'name': '물리치료 · 재활', 'photo': ph('PENDING'),
 'kicker': '물리치료 &middot; 도수치료 &middot; 재활의학과',
 'h1': '치료사의 손은<br>다른 환자의 허리에 있습니다.',
 'sub': '40분짜리 도수치료는 전화 때문에 멈출 수 없습니다. 그래서 &ldquo;도수 얼마예요, 실비 되나요&rdquo;라는 '
        '첫 문의가 음성사서함으로 갑니다.',
 'cost': '도수치료 환자는 한 번 오고 끝나지 않습니다. 평가 뒤에 10회, 20회 계획이 잡히고, 그 환자가 가족을 데려옵니다. '
         '그런데 첫 문의는 치료 시간표가 꽉 찬 오후에 오고, 치료사는 손을 뗄 수 없습니다. '
         '놓친 첫 문의 한 통은 한 회가 아니라 한 계획입니다.',
 'call': [('환자', '3:22 PM', '허리 디스크로 도수치료 받아 보려는데, 처음 가면 얼마예요? 실비 되나요?'),
          ('Saleringo', '+21초', '첫 방문은 원장님 진료와 평가가 먼저이고, 도수치료는 <b>30분 7만원</b>입니다. '
                                 '실손보험은 진료 뒤 청구 서류를 드리고, 보장 여부는 가입하신 약관에 따라 다릅니다. '
                                 '내일 <b>오전 11시</b>와 <b>오후 5시 30분</b>이 비어 있습니다.'),
          ('환자', '3:24 PM', '5시 30분이요. 몇 번 받으면 나을까요?'),
          ('Saleringo', '+7초', '회복 속도는 사람마다 달라서 제가 횟수를 말씀드릴 수 없고, 원장님이 평가하고 계획을 세워 드립니다. '
                                '내일 5시 30분으로 잡아 두었으니, 있으시면 MRI나 진단서를 가져오세요.')],
 'refuse': [('몇 회면 낫는지 약속하지 않습니다.',
             '&ldquo;열 번이면 좋아집니다&rdquo;는 치료 계획이고, 평가 없이 나올 수 없는 말입니다. 횟수는 원장님이 정합니다.'),
            ('운동이나 스트레칭을 처방하지 않습니다.',
             '&ldquo;집에서 뭐 하면 되나요&rdquo;에 답하지 않습니다. 상태에 맞지 않는 운동은 더 다치게 합니다.'),
            ('실손보험 보장 여부를 단정하지 않습니다.',
             '청구 서류를 드린다는 사실까지만 말합니다. 보장은 가입 약관과 보험사가 정합니다.'),
            ('두 다리에 감각이 없거나 대소변 조절이 안 된다고 하면 예약을 멈춥니다.',
             '척추의 위험 신호입니다. 응급 진료를 안내하고 원장님에게 바로 연결합니다.')],
 'fields': ['증상 설명 원문', '진단서 · MRI · 의뢰서 지참 여부', '평가 예약 시각',
            '요금표 기준 안내 금액', '실손 문의 데스크 확인 표시', '위험 신호 확인 결과'],
 'stages': ['문의 접수', '평가 예약', '진료 · 평가', '치료 계획', '치료 · 재평가'],
 'when': {'eyebrow': '치료 중의 통화', 'h2': '치료사 손이 환자에게 있는 동안<br>이렇게 흘러갑니다.',
          'tt': '치료 중', 'badge': '환자를 두고 나올 수 없는 시간'},
 'lead': '치료사 손이 환자에게 있을 때 오는 첫 문의. 몇 회면 낫는지 약속하지 않고 평가 예약을 잡습니다.',
 'group': 0,
 'en': {
  'name': 'Physio & rehab', 'owner': 'the owner',
  'kicker': 'Physiotherapy &middot; manual therapy &middot; rehab',
  'h1': 'The physio\'s hands are<br>on someone else\'s back.',
  'sub': 'A forty-minute session cannot stop for the phone. So the first enquiry, "how much is manual therapy and will insurance pay", '
         'rings through to voicemail.',
  'cost': 'A physio patient is not one visit. After the assessment comes a plan of ten or twenty sessions, and that patient brings the family. '
          'But the first enquiry arrives in the afternoon when the timetable is full and no hand is free. '
          'One missed first call is a plan, not a session.',
  'call': [('Patient', '3:22 PM', 'I have a herniated disc and want to try manual therapy. What does a first visit cost, and will my insurance cover it?'),
           ('Saleringo', '+21 s', 'A first visit is an assessment at <b>$120</b>, and manual therapy after that is <b>$95 per thirty minutes</b>. '
                                  'We give you the paperwork to claim; whether your plan pays depends on its terms. Tomorrow I have <b>11 AM</b> or <b>5:30 PM</b>.'),
           ('Patient', '3:24 PM', '5:30. How many sessions until it\'s better?'),
           ('Saleringo', '+7 s', 'Recovery differs from person to person, so I cannot promise a number; the physio sets a plan after the assessment. '
                                 'You are booked for 5:30 tomorrow. Bring any MRI or doctor\'s note you have.')],
  'refuse': [('Never promises how many sessions.',
              '"Ten and you will be fine" is a treatment plan, and there is none before an assessment. The physio sets the number.'),
             ('Never prescribes an exercise or a stretch.',
              '"What should I do at home" goes unanswered. The wrong exercise for the wrong back makes it worse.'),
             ('Never says what insurance will pay.',
              'It says the clinic provides claim paperwork, and stops. Coverage is the insurer\'s decision under the policy.'),
             ('Numbness in both legs or loss of bladder control ends the booking.',
              'Those are spinal red flags. The AI directs the caller to emergency care and connects the physio at once.')],
  'fields': ['Complaint in the patient\'s own words', 'Referral, MRI or doctor\'s note on hand', 'Assessment slot booked',
             'Fee quoted from the clinic schedule', 'Insurance question flagged to the desk', 'Red-flag check result'],
  'stages': ['Enquiry', 'Assessment booked', 'Assessment', 'Treatment plan', 'Sessions & review'],
  'when': {'eyebrow': 'A call mid-session', 'h2': 'While the physio\'s hands are on a patient,<br>this is how it goes.',
           'tt': 'Mid-session', 'badge': 'Cannot leave the table'},
  'lead': 'The first enquiry arrives mid-session. The AI books the assessment and refuses to say how many sessions it will take.',
  'room': 'health-care',
  'room_d': 'First enquiries about manual therapy answered while the physio is with a patient: fee read from the schedule, assessment booked, and no promise about recovery.',
  'room_no': ('0', 'recovery promises the AI makes'),
 },
},
{
 'slug': 'korean-medicine', 'owner': '원장님', 'name': '한의원', 'photo': ph('PENDING'),
 'kicker': '한의원 &middot; 침 &middot; 추나 &middot; 한약',
 'h1': '점심시간에 걸려 오는<br>교통사고 환자 전화.',
 'sub': '어제 추돌 뒤 목이 뻐근한 사람, 밤새 허리가 더 굳은 사람. '
        '그 전화는 문을 잠근 한 시간 동안 옵니다.',
 'cost': '한의원 신환의 절반은 자동차보험 환자이고, 사고 다음 날 낮에 겁니다. 그 시간이 점심시간이면 '
         '전화는 옆 한의원으로 갑니다. 자보 환자는 열 번 넘게 통원하고, 그 뒤에 한약과 가족 진료로 이어집니다. '
         '점심 한 시간에 놓친 전화 한 통이 한 달치 통원입니다.',
 'call': [('환자', '12:52 PM', '어제 교통사고 나서 목이 뻐근한데, 자동차보험으로 침 치료 되나요? 오늘 갈 수 있을까요?'),
          ('Saleringo', '+18초', '보험사에 접수된 사고번호가 있으면 자동차보험 진료가 됩니다. 오늘 <b>오후 3시 20분</b>과 <b>6시</b>가 비어 있고, '
                                 '첫 방문은 진료와 침 치료로 40분 정도 걸립니다.'),
          ('환자', '12:54 PM', '3시 20분이요. 한약도 같이 먹어야 하나요?'),
          ('Saleringo', '+7초', '한약이 필요한지는 원장님이 진료하고 정하실 일이라 제가 답할 수 없습니다. 3시 20분으로 잡아 두었고, '
                                '사고번호와 보험사 담당자 연락처를 가져오시면 접수가 빨라집니다.')],
 'refuse': [('체질이나 병증을 말하지 않습니다.',
             '&ldquo;소음인 같으시네요&rdquo;, &ldquo;담이 결린 겁니다&rdquo;는 진료입니다. 한쪽 팔다리에 힘이 빠진다는 말이 나오면 예약을 멈추고 응급 안내를 읽습니다.'),
            ('한약의 효과와 치료 기간을 약속하지 않습니다.',
             '&ldquo;한 제 드시면 좋아집니다&rdquo;, &ldquo;몇 주면 낫습니다&rdquo;를 말하지 않습니다. 요금표의 한약 가격까지만 안내하고 처방과 기간은 원장님이 정합니다.'),
            ('드시던 양약을 끊으라고 하지 않습니다.',
             '한약과 양약을 같이 먹어도 되는지, 무엇을 끊을지는 원장님이 처방을 보고 판단합니다.'),
            ('자동차보험이나 실손 적용을 확답하지 않습니다.',
             '사고 접수 여부는 보험사가 정합니다. 사고번호가 있으면 된다는 사실까지만 말합니다.')],
 'fields': ['증상과 시작 시점', '자보 · 실손 · 일반 구분과 사고번호', '첫 방문 예약 시각',
            '요금표 기준 안내 금액', '한약 문의 원장님 전달 표시', '확인 문자 발송 기록'],
 'stages': ['문의 접수', '예약 확정', '진료 · 침 치료', '치료 계획', '통원 · 재진'],
 'when': {'eyebrow': '점심시간의 통화', 'h2': '문을 잠근 한 시간 동안<br>이렇게 흘러갑니다.',
          'tt': '점심시간', 'badge': '데스크가 비는 시간'},
 'lead': '점심시간에 오는 교통사고 환자 전화. 한약이 필요한지 정하지 않고, 오늘 자리에 예약을 잡습니다.',
 'group': 0,
 'en': {
  'name': 'Acupuncture & traditional medicine', 'owner': 'the practitioner',
  'kicker': 'Acupuncture &middot; herbal medicine &middot; traditional clinics',
  'h1': 'The lunch-hour call<br>from a car accident.',
  'sub': 'Whiplash after a rear-end collision, a back that seized overnight. '
         'Those calls come during the one hour the door is locked.',
  'cost': 'Half of a clinic\'s new patients are injury claims, and they call the day after the accident, in daylight. '
          'If that is the lunch hour, the call goes to the clinic next door. A claim patient comes back ten times or more, '
          'then for a herbal course, then with the family. One call lost at lunch is a month of visits.',
  'call': [('Patient', '12:52 PM', 'I was rear-ended yesterday and my neck is stiff. Do you treat auto-injury claims, and can I come in today?'),
           ('Saleringo', '+18 s', 'Yes. With the claim number from the insurer, the visit is billed to the claim. Today I have <b>3:20 PM</b> and <b>6 PM</b>; '
                                  'a first visit with acupuncture takes about forty minutes.'),
           ('Patient', '12:54 PM', '3:20. Should I take herbal medicine as well?'),
           ('Saleringo', '+7 s', 'Whether you need a herbal formula is the practitioner\'s call after examining you, so I will leave it to him. '
                                 'You are booked for 3:20; bring the claim number and the adjuster\'s contact and check-in will be quick.')],
  'refuse': [('Never names a constitution or a condition.',
              '"You sound like a cold type" or "that is a pulled muscle" is a consultation. Weakness on one side of the body ends the booking and the AI reads the emergency instruction.'),
             ('Never promises what a herbal formula will do, or how long treatment takes.',
              'It quotes the price of a course from the schedule and stops. Whether to prescribe one, and how many weeks of visits follow, is the practitioner\'s decision.'),
             ('Never tells anyone to stop a prescribed medicine.',
              'Whether herbs and a prescription can be taken together, or what to pause, is decided by the practitioner with the prescription in front of him.'),
             ('Never confirms that a claim or a plan will pay.',
              'The insurer decides whether a claim is open. The AI says only that a claim number is what the clinic needs.')],
  'fields': ['Complaint and when it started', 'Auto claim, insurance or self-pay, and claim number', 'First-visit slot booked',
             'Fee quoted from the practitioner\'s schedule', 'Herbal-formula question passed to the practitioner', 'Confirmation text with claim checklist sent'],
  'stages': ['Enquiry', 'Visit booked', 'Consultation & acupuncture', 'Course planned', 'Course of visits'],
  'when': {'eyebrow': 'The lunch-hour call', 'h2': 'While the door is locked for an hour,<br>this is how it goes.',
           'tt': 'Lunch hour', 'badge': 'Desk empty'},
  'lead': 'The injury-claim call at lunch. The AI books today\'s slot and leaves the herbal question to the practitioner.',
  'room': 'health-care',
  'room_d': 'Injury-claim and first-visit calls answered through the locked lunch hour: slot booked, claim number captured, and no opinion on herbs, constitutions or what to stop taking.',
  'room_no': ('0', 'herbal formulas the AI recommends'),
 },
},
{
 'slug': 'optician', 'owner': '대표님', 'name': '안경원', 'photo': ph('PENDING'),
 'kicker': '안경원 &middot; 콘택트렌즈',
 'h1': '검안은 전화 때문에<br>멈출 수 없습니다.',
 'sub': '렌즈만 바꾸면 얼마인지, 주문한 안경이 왔는지, 오늘 가면 바로 되는지. '
        '대표님이 검안실에서 다른 손님의 시력을 재는 동안 묻는 질문들입니다.',
 'cost': '안경원 전화는 짧습니다. 가격 하나, 시간 하나. 그런데 그 짧은 전화가 검안실에서는 받을 수 없고, '
         '못 받은 손님은 지하철역 앞 체인점에 걸어 들어갑니다. 안경은 2년마다 바꾸고 렌즈는 매달 삽니다. '
         '한 번 옮긴 손님은 그 체인점의 회원이 됩니다.',
 'call': [('손님', '5:48 PM', '안경 렌즈만 바꾸려는데 얼마예요? 두께 얇은 걸로요. 오늘 가면 바로 되나요?'),
          ('Saleringo', '+20초', '압축 렌즈는 <b>1.60 한 쌍 6만원</b>, <b>1.67은 9만원</b>입니다. 도수와 테 모양에 따라 맞는 압축률이 달라서 검안을 먼저 합니다. '
                                 '재고가 있는 도수면 당일에 되고, 오늘 <b>저녁 7시 30분</b>에 자리가 있습니다.'),
          ('손님', '5:49 PM', '7시 30분이요. 요즘 눈이 침침한데 노안 온 걸까요?'),
          ('Saleringo', '+6초', '그건 검안하면서 대표님이 봐 드려야 하는 부분이라 제가 판단하지 않습니다. 7시 30분으로 잡아 두었고, '
                                '지금 쓰시는 안경을 가져오시면 도수 비교가 됩니다.')],
 'refuse': [('시력이 왜 나빠졌는지 말하지 않습니다.',
             '침침함, 두통, 눈부심의 원인은 검안과 안과 진료가 정합니다. 증상은 원문으로 적고 판단은 남기지 않습니다.'),
            ('콘택트렌즈 도수를 전화로 정해 주지 않습니다.',
             '&ldquo;안경 도수 그대로 렌즈 주세요&rdquo;에 도수를 환산해 답하지 않습니다. 렌즈는 착용 검사 뒤에 나갑니다.'),
            ('확인하지 않은 재고를 약속하지 않습니다.',
             '등록된 재고 현황에 있는 도수와 테만 당일 가능하다고 말합니다. 없으면 주문 기간을 안내합니다.'),
            ('갑자기 안 보인다거나 눈이 아프다고 하면 예약을 멈춥니다.',
             '안과 응급 진료를 안내하고 대표님에게 바로 연결합니다.')],
 'fields': ['요청 항목(렌즈 · 테 · 콘택트렌즈)', '현재 도수 · 처방전 지참 여부', '검안 예약 시각',
            '렌즈 가격표 기준 안내 금액', '재고 확인 필요 여부', '시력 변화 질문 판단 보류 표시'],
 'stages': ['문의 접수', '검안 예약', '검안 · 피팅', '당일 제작 또는 주문', '수령 · 재검 안내'],
 'when': {'eyebrow': '검안 중의 통화', 'h2': '다른 손님의 시력을 재는 동안<br>이렇게 흘러갑니다.',
          'tt': '검안 중', 'badge': '검안실을 비울 수 없는 시간'},
 'lead': '검안 중에 오는 렌즈 문의. 침침한 이유를 말하지 않고, 렌즈 가격표와 오늘 시간만 답합니다.',
 'group': 0,
 'en': {
  'name': 'Opticians', 'owner': 'the owner',
  'kicker': 'Opticians &middot; contact lenses',
  'h1': 'The eye test cannot pause<br>for the phone.',
  'sub': 'Lens-only replacements, "has my order come in", "can you do it today". '
         'Asked while the optician is in the exam room with somebody else.',
  'cost': 'Optician calls are short: one price, one time. But the short call cannot be taken in the exam room, and the customer who was not answered '
          'walks into the chain by the station. Glasses are replaced every two years and contacts are bought every month; '
          'a customer who moved once becomes that chain\'s member.',
  'call': [('Customer', '5:48 PM', 'I just want new lenses in my frames, the thin kind. How much, and can it be done today?'),
           ('Saleringo', '+20 s', 'Thin lenses are <b>$120 a pair at 1.60</b> and <b>$180 at 1.67</b>. The right index depends on your prescription and the frame, '
                                  'so we start with an eye test. If your prescription is in stock it is same-day, and <b>7:30 tonight</b> is open.'),
           ('Customer', '5:49 PM', '7:30 then. My eyes have been blurry lately. Is it presbyopia?'),
           ('Saleringo', '+6 s', 'That is something the optician checks during the test, not something I judge. You are booked for 7:30; '
                                 'bring the glasses you wear now so we can compare prescriptions.')],
  'refuse': [('Never explains why vision changed.',
              'Blur, headaches and glare are for the eye test and, if needed, an ophthalmologist. The symptom is written down as said, without a verdict.'),
             ('Never sets a contact-lens prescription over the phone.',
              '"Just give me contacts in my glasses prescription" is not converted. Contacts leave the shop after a fitting.'),
             ('Never promises stock it has not checked.',
              'Same-day means the prescription and frame are on the stock list. Otherwise it quotes the order lead time.'),
             ('Sudden vision loss or eye pain ends the booking.',
              'The AI directs the caller to an eye emergency service now and connects the owner.')],
  'fields': ['Request: lenses, frames or contacts', 'Current prescription on hand', 'Eye-test slot booked',
             'Price quoted from the lens list', 'Stock check needed', 'Vision-change question flagged as not assessed'],
  'stages': ['Enquiry', 'Eye test booked', 'Test & fitting', 'Same-day or ordered', 'Collection & recall'],
  'when': {'eyebrow': 'A call mid-test', 'h2': 'While another customer is in the chair,<br>this is how it goes.',
           'tt': 'Mid-test', 'badge': 'Cannot leave the exam room'},
  'lead': 'The lens call lands mid-test. The AI quotes the lens list and tonight\'s slot, and leaves the blur to the optician.',
  'room': 'health-care',
  'room_d': 'Lens, frame and contact questions answered while the optician is testing someone else: price from the list, slot tonight, and no opinion on why the caller\'s eyes changed.',
  'room_no': ('0', 'eye conditions the AI explains'),
 },
},
{
 'slug': 'counseling', 'owner': '원장님', 'name': '심리상담센터', 'photo': ph('PENDING'),
 'kicker': '심리상담 &middot; 부부 · 가족 상담 &middot; 청소년 상담',
 'h1': '첫 전화에는 용기가 필요합니다.<br>음성사서함으로 가면 안 됩니다.',
 'sub': '일주일을 망설이다 밤 아홉 시에 거는 전화입니다. '
        '아무도 받지 않으면, 그 사람은 다시 걸지 않습니다.',
 'cost': '상담센터의 첫 문의는 상담 시간이 끝난 저녁에 옵니다. 낮에는 걸 용기가 나지 않아서입니다. '
         '못 받은 첫 전화는 다른 센터로 가지 않고 그냥 사라집니다. 그 전화가 이어졌다면 열 회기, 스무 회기의 상담이었고, '
         '무엇보다 한 사람이 도움을 받는 첫날이었습니다.',
 'call': [('문의', '9:14 PM', '성인 개인 상담을 처음 받아 보려는데요, 비용이 어떻게 되나요? 평일 저녁도 되나요?'),
          ('Saleringo', '+23초', '개인 상담은 <b>50분 8만원</b>이고, 첫 회기는 초기 면담으로 진행됩니다. 평일 저녁은 <b>화 · 목 7시</b>에 있고, '
                                 '이번 주 <b>목요일 7시</b>가 비어 있습니다. 어느 상담사와 하실지는 첫 면담 뒤에 정합니다.'),
          ('문의', '9:16 PM', '목요일로 할게요. 제가 우울증인 건가요?'),
          ('Saleringo', '+6초', '그건 상담사가 직접 만나 뵙고 함께 살펴볼 부분이라 제가 말씀드릴 수 없습니다. 목요일 7시로 잡아 두었고, '
                                '성함과 연락처만 남겨 주시면 됩니다.')],
 'refuse': [('진단명을 말하지 않습니다.',
             '&ldquo;우울증인가요&rdquo;, &ldquo;공황장애 같은데요&rdquo;에 답하지 않습니다. 상담사가 만나서 함께 볼 일입니다.'),
            ('상담의 결과를 약속하지 않습니다.',
             '몇 회기면 좋아진다, 부부 관계가 회복된다는 말을 하지 않습니다. 회기 수와 방향은 초기 면담 뒤에 정해집니다.'),
            ('누가 상담을 받는지 말하지 않습니다.',
             '배우자나 자녀가 다니는지 물어도 답하지 않습니다. 내담 사실 자체가 비밀입니다.'),
            ('자해나 죽고 싶다는 표현이 나오면 예약을 멈춥니다.',
             '위기 상담 전화 109를 안내하고, 통화를 끊지 않은 채 당직 상담사에게 즉시 연결합니다.')],
 'fields': ['개인 · 부부 · 가족 · 청소년 구분', '첫 문의 · 재방문 구분', '초기 면담 예약 시각',
            '요금표 기준 안내 금액', '희망 상담사 유무', '위기 대응 발동 여부'],
 'stages': ['문의 접수', '초기 면담 예약', '초기 면담', '상담사 배정', '정기 상담'],
 'when': {'eyebrow': '밤 아홉 시의 통화', 'h2': '상담실 불이 꺼진 뒤<br>이렇게 흘러갑니다.',
          'tt': '상담 종료 후', 'badge': '용기가 필요한 시간'},
 'lead': '용기 내서 거는 첫 전화입니다. 진단하지 않고 초기 면담을 잡되, 위기 표현이 나오면 즉시 사람에게 넘깁니다.',
 'group': 0,
 'en': {
  'name': 'Counseling & therapy', 'owner': 'the director',
  'kicker': 'Counselling &middot; couples &amp; family &middot; adolescents',
  'h1': 'The first call takes courage.<br>It must not reach voicemail.',
  'sub': 'People ring a counselling centre at nine at night, after a week of rehearsing. '
         'If nobody answers, most never ring again.',
  'cost': 'A centre\'s first enquiries come in the evening, after the last session, because daytime takes a courage many callers do not have yet. '
          'A missed first call does not go to another centre; it simply disappears. Had it connected, it was ten or twenty sessions, '
          'and above all the first day somebody got help.',
  'call': [('Caller', '9:14 PM', 'I\'ve never done this before. I\'d like to try individual counselling. What does it cost, and do you have weekday evenings?'),
           ('Saleringo', '+23 s', 'An individual session is <b>$130 for fifty minutes</b>, and the first one is an intake. Weekday evenings are <b>Tuesday and Thursday at 7</b>; '
                                  '<b>this Thursday at 7</b> is open. Which counsellor you see is decided after the intake.'),
           ('Caller', '9:16 PM', 'Thursday, please. Do you think I have depression?'),
           ('Saleringo', '+6 s', 'That is something a counsellor looks at with you in person, and not something I can say. You are booked for Thursday at 7. '
                                 'Just leave me a name and a number.')],
  'refuse': [('Never names a diagnosis.',
              '"Is it depression" or "it sounds like panic attacks" goes unanswered. A counsellor looks at that with the client, in the room.'),
             ('Never promises a result.',
              'No "you will feel better in six sessions", no "the marriage can be saved". Length and direction are set after the intake.'),
             ('Never says whether anyone is a client.',
              'A spouse or a parent asking if someone attends gets no answer. Attendance itself is confidential.'),
             ('Any mention of self-harm ends the booking.',
              'The AI reads the crisis line, stays on the call and connects the on-call counsellor immediately.')],
  'fields': ['Individual, couple, family or adolescent', 'First contact or returning', 'Intake slot booked',
             'Session fee quoted from the schedule', 'Preferred counsellor, or none', 'Crisis protocol triggered or not'],
  'stages': ['Enquiry', 'Intake booked', 'Intake', 'Counsellor matched', 'Ongoing sessions'],
  'when': {'eyebrow': 'The call at nine at night', 'h2': 'After the last session ends,<br>this is how it goes.',
           'tt': 'After hours', 'badge': 'The call that took courage'},
  'lead': 'The first call, made with courage. The AI books the intake without a diagnosis and hands any crisis to a person at once.',
  'room': 'health-care',
  'room_d': 'The first, hesitant call at nine at night answered: fee read as published, intake booked, and no diagnosis. A single mention of self-harm puts a counsellor on the line.',
  'room_no': ('0', 'diagnoses the AI offers'),
 },
},
{
 'slug': 'childcare', 'owner': '원장님', 'name': '어린이집 · 유치원', 'photo': ph('PENDING'),
 'kicker': '어린이집 &middot; 유치원 &middot; 놀이학교',
 'h1': '등원 시간에<br>전화가 울립니다.',
 'sub': '8시 40분, 선생님은 전부 현관에 나가 있습니다. 대기 문의, 견학 요청, '
        '&ldquo;열이 있는데 보내도 되나요&rdquo;가 그 시간에 한꺼번에 옵니다.',
 'cost': '어린이집 문의는 한 아이가 아니라 3년입니다. 만 3세에 들어온 아이는 졸업까지 다니고, 동생이 따라 들어옵니다. '
         '그런데 그 문의는 아이들이 들어오는 아침과 낮잠 시간에 오고, 선생님은 아이 곁을 떠날 수 없습니다. '
         '못 받은 견학 문의는 다음 주에 다른 원을 보고 있습니다.',
 'call': [('학부모', '8:41 AM', '내년 3월에 만 3세 반 들어갈 수 있을까요? 견학도 해 보고 싶어요.'),
          ('Saleringo', '+22초', '만 3세 반은 <b>정원 15명</b>이고, 입소 순서는 임신육아종합포털의 대기 순번으로 정해져서 제가 자리를 확정해 드릴 수는 없습니다. '
                                 '견학은 <b>매주 수요일 오전 10시 30분</b>에 하고, 다음 주 수요일 자리가 있습니다. 특별활동비는 <b>월 6만원</b>입니다.'),
          ('학부모', '8:43 AM', '다음 주 수요일로 할게요. 아이가 아직 기저귀를 못 뗐는데 괜찮을까요?'),
          ('Saleringo', '+7초', '기저귀나 적응 문제는 원장님과 담임 선생님이 견학 때 직접 상담해 드립니다. 다음 주 수요일 10시 30분으로 잡아 두었고, '
                                '아이 이름과 생년월일을 남겨 주시면 대기 순번 확인도 같이 준비해 두겠습니다.')],
 'refuse': [('입소를 확답하지 않습니다.',
             '자리는 포털의 대기 순번과 원장님이 정합니다. 정원과 견학 일정까지만 말합니다.'),
            ('아이의 발달을 판단하지 않습니다.',
             '&ldquo;말이 늦은 것 같은데 괜찮나요&rdquo;에 답하지 않습니다. 담임과 원장님이 아이를 보고 상담할 일입니다.'),
            ('하원 인계자를 전화로 바꾸지 않습니다.',
             '&ldquo;오늘은 이모가 데리러 갑니다&rdquo;는 접수만 하고 원장님에게 넘깁니다. 원장님이 학부모 본인에게 확인한 뒤에만 바뀝니다.'),
            ('아픈 아이와 다친 아이는 예약이 아니라 사람의 일입니다.',
             '열이 있는데 보내도 되는지는 원의 규정을 읽어 드리고 판단은 담임에게 넘깁니다. 아이가 다쳤다는 전화는 원장님에게 즉시 연결합니다.')],
 'fields': ['아이 연령과 희망 반', '대기 순번 확인 필요 여부', '견학 예약 시각',
            '공개된 요금표 기준 안내 금액', '형제 · 자매 재원 여부', '하원 · 건강 관련 요청 원장님 전달 표시'],
 'stages': ['문의 접수', '견학 예약', '견학 · 상담', '입소 안내', '입소 · 적응'],
 'when': {'eyebrow': '등원 시간의 통화', 'h2': '선생님들이 현관에 나가 있는 동안<br>이렇게 흘러갑니다.',
          'tt': '등원 시간', 'badge': '아이 곁을 떠날 수 없는 시간'},
 'lead': '등원 시간에 오는 대기 문의. 입소를 확답하지 않고 견학을 잡으며, 하원 인계자는 전화로 바꾸지 않습니다.',
 'group': 1,
 'en': {
  'name': 'Daycare & preschool', 'owner': 'the director',
  'kicker': 'Daycare &middot; preschool &middot; nursery',
  'h1': 'Drop-off is when<br>the phone rings.',
  'sub': 'At 8:40 every teacher is at the gate. That is when the waitlist call, the tour request '
         'and "she has a fever, can she still come" all land at once.',
  'cost': 'A daycare enquiry is not one child; it is three years. A three-year-old stays until preschool ends and the younger sibling follows. '
          'But the enquiry comes at drop-off and nap time, when no teacher can leave the room. '
          'The tour request nobody answered is touring another centre next week.',
  'call': [('Parent', '8:41 AM', 'Is there a place in the three-year-old room next spring? I\'d like to see the centre.'),
           ('Saleringo', '+22 s', 'The three-year-old room holds <b>15 children</b>, and places are offered in waitlist order, so I cannot confirm one myself. '
                                  'Tours run <b>Wednesdays at 10:30</b> and next Wednesday is open. Full-day tuition is <b>$1,250 a month</b>, with enrichment at <b>$60</b>.'),
           ('Parent', '8:43 AM', 'Next Wednesday, please. She isn\'t potty-trained yet. Is that a problem?'),
           ('Saleringo', '+7 s', 'Toilet training and settling in are things the director and her teacher talk through with you on the tour. '
                                 'You are booked for next Wednesday at 10:30; give me her name and date of birth and I will have the waitlist position ready.')],
  'refuse': [('Never confirms a place.',
              'Places follow the waitlist and the director. The AI gives room sizes and tour dates and stops there.'),
             ('Never judges a child\'s development.',
              '"She is not talking much yet, is that normal" goes unanswered. Her teacher and the director look at the child, not at a phone call.'),
             ('Never changes who picks a child up.',
              '"Her aunt is collecting her today" is logged and passed to the director, and changed only after the director verifies the parent herself.'),
             ('A sick or hurt child is a person\'s call, not a booking.',
              'For a fever it reads the centre\'s policy as written and leaves the decision to the teacher. A call about an injury reaches the director at once.')],
  'fields': ['Child\'s age and requested room', 'Waitlist position to check', 'Tour slot booked',
             'Fees quoted from the published list', 'Sibling already enrolled', 'Pickup or health request passed to the director'],
  'stages': ['Enquiry', 'Tour booked', 'Tour & talk', 'Place offered', 'Enrolment & settling in'],
  'when': {'eyebrow': 'The drop-off call', 'h2': 'While every teacher is at the gate,<br>this is how it goes.',
           'tt': 'Drop-off', 'badge': 'Cannot leave the children'},
  'lead': 'The waitlist call at drop-off. The AI books the tour, confirms no place, and never changes a pickup by phone.',
  'room': 'booked-by-appointment',
  'room_d': 'Waitlist and tour calls answered while every teacher is at the gate: tour booked, fees read as published, and any pickup change or sick-child question handed to the director.',
  'room_no': ('0', 'pickup changes the AI makes on its own'),
 },
},
{
 'slug': 'driving-school', 'owner': '원장님', 'name': '운전학원', 'photo': ph('PENDING'),
 'kicker': '운전학원 &middot; 자동차운전전문학원',
 'h1': '토요일 아침, 접수 창구에<br>줄이 서고 전화가 울립니다.',
 'sub': '&ldquo;총 얼마예요, 얼마나 걸려요, 주말에도 되나요.&rdquo; 첫 면허 문의는 사무실이 가장 바쁠 때 옵니다. '
        '그 전화를 받은 학원이 그 수강생을 등록합니다.',
 'cost': '운전학원 문의는 비교 전화입니다. 세 곳에 걸어서 먼저 답한 곳에 갑니다. 방학과 연초에 몰리고, '
         '그 시간에 창구는 줄이 서 있습니다. 한 명이 70만원 안팎이고, 친구가 따라 옵니다. '
         '통화 중 신호로 놓친 전화는 옆 학원의 등록입니다.',
 'call': [('문의', '10:07 AM', '2종 자동 처음 따려는데 총 얼마예요? 주말에도 교육 되나요?'),
          ('Saleringo', '+24초', '2종 자동 정규 과정은 <b>학과 · 장내 · 도로주행 포함 72만원</b>이고, 검정료는 별도입니다. 주말 교육은 <b>토 · 일 오전</b>에 있고, '
                                 '학과교육 첫 시간은 <b>이번 주 토요일 9시</b>가 비어 있습니다. 신분증과 6개월 이내 사진 3장이 필요합니다.'),
          ('문의', '10:09 AM', '토요일 9시로 할게요. 한 달 안에 딸 수 있죠?'),
          ('Saleringo', '+7초', '합격 시기는 교육 진도와 시험 일정에 따라 달라서 제가 약속드릴 수 없습니다. 토요일 9시 학과교육으로 접수해 두었고, '
                                '성함과 연락처를 남겨 주시면 준비물 안내를 문자로 보내 드리겠습니다.')],
 'refuse': [('합격을 약속하지 않습니다.',
             '&ldquo;한 달이면 됩니다&rdquo;, &ldquo;한 번에 붙습니다&rdquo;를 말하지 않습니다. 시험은 학원이 아니라 시험장에서 봅니다.'),
            ('면허를 딸 수 있는 몸인지 판단하지 않습니다.',
             '시력, 복용 중인 약, 지병으로 되는지 묻는 질문은 적성검사가 정합니다. 학원이 미리 답할 일이 아닙니다.'),
            ('신고된 수강료를 깎지 않습니다.',
             '등록된 과정 요금과 원장님이 넣어 둔 할인만 말합니다. 흥정하지 않습니다.'),
            ('교육 중 사고 전화는 사람에게 바로 갑니다.',
             '도로주행 중 접촉이 났다, 수강생이 다쳤다는 말이 나오면 접수가 아니라 원장님 즉시 연결입니다.')],
 'fields': ['면허 종별과 변속기', '평일 · 주말 희망 시간대', '첫 교육 예약 시각',
            '신고된 요금표 기준 안내 금액', '남은 준비 서류', '기존 면허 · 운전 경험 여부'],
 'stages': ['문의 접수', '등록', '학과교육', '장내 · 도로주행', '시험 접수'],
 'when': {'eyebrow': '토요일 아침의 통화', 'h2': '접수 창구에 줄이 선 동안<br>이렇게 흘러갑니다.',
          'tt': '주말 접수 피크', 'badge': '창구가 밀리는 시간'},
 'lead': '토요일 접수 창구가 밀릴 때 오는 전화. 합격을 약속하지 않고, 신고된 수강료로 첫 교육을 접수합니다.',
 'group': 1,
 'en': {
  'name': 'Driving schools', 'owner': 'the owner',
  'kicker': 'Driving schools &middot; driver education',
  'h1': 'Saturday morning, a queue<br>at the counter and the phone.',
  'sub': '"How much in total, how long, can I do weekends." The first-licence call comes when the office is busiest. '
         'Whichever school answers it enrols the student.',
  'cost': 'A driving-school enquiry is a comparison call: three schools dialled, the first to answer wins. They bunch up in school holidays and in January, '
          'exactly when the counter has a queue. One student is around seven hundred dollars and brings a friend. '
          'A call lost to the busy tone is the school next door\'s enrolment.',
  'call': [('Enquirer', '10:07 AM', 'I want to get my first licence, automatic. What\'s the total, and can I do lessons on weekends?'),
           ('Saleringo', '+24 s', 'The beginner package, classroom, range and road lessons, is <b>$720</b>; test fees are separate. Weekend lessons run <b>Saturday and Sunday mornings</b>, '
                                  'and the first classroom session has a seat <b>this Saturday at 9</b>. Bring photo ID and three passport photos.'),
           ('Enquirer', '10:09 AM', 'Saturday at 9, then. I can pass within a month, right?'),
           ('Saleringo', '+7 s', 'When you pass depends on how the lessons go and on test dates, so I cannot promise that. You are enrolled for Saturday at 9; '
                                 'leave a name and number and I will text you what to bring.')],
  'refuse': [('Never promises a pass.',
              'No "a month is enough", no "first time, easily". The test is taken at the licensing centre, not at the school.'),
             ('Never judges whether someone may hold a licence.',
              'Eyesight, medication and medical conditions are screened by the licensing authority. The school does not pre-decide it on the phone.'),
             ('Never discounts the published fee.',
              'It quotes the registered course price and only the discounts the owner entered. It does not haggle.'),
             ('A crash during a lesson goes to a person at once.',
              'A scrape on a road lesson or an injured student is not an enquiry; it connects the owner immediately.')],
  'fields': ['Licence class and transmission', 'Weekday or weekend preference', 'First session booked',
             'Package price quoted from the published list', 'Documents still needed', 'Previous licence or driving experience'],
  'stages': ['Enquiry', 'Enrolled', 'Classroom', 'Range & road lessons', 'Test booked'],
  'when': {'eyebrow': 'The Saturday-morning call', 'h2': 'While the counter has a queue,<br>this is how it goes.',
           'tt': 'Weekend peak', 'badge': 'Counter backed up'},
  'lead': 'The Saturday call while the counter is queued. The AI enrols the first session at the published fee and promises no pass.',
  'room': 'booked-by-appointment',
  'room_d': 'First-licence calls answered through the Saturday rush: package priced from the published list, first session enrolled, and no promise about passing.',
  'room_no': ('0', 'passes the AI promises'),
 },
},
{
 'slug': 'music-art-academy', 'owner': '원장님', 'name': '음악 · 미술 학원', 'photo': ph('PENDING'),
 'kicker': '피아노 &middot; 바이올린 &middot; 미술 학원',
 'h1': '레슨은 일대일입니다.<br>전화도 그렇습니다.',
 'sub': '일곱 살 아이가 음계를 치는 중에 선생님이 자리를 뜰 수는 없습니다. '
        '체험 문의는 매일 오후 네 시, 딱 그 시간에 옵니다.',
 'cost': '예체능 학원 원생은 한 번 오면 몇 년을 다닙니다. 바이엘에서 체르니로, 스케치에서 수채화로. '
         '그런데 첫 문의는 학교가 끝난 오후에 오고, 그 시간 원장님은 레슨실에 있습니다. '
         '놓친 체험 문의는 같은 건물 다른 층의 학원에 등록합니다.',
 'call': [('학부모', '4:36 PM', '7살 아이 피아노 처음 시작하려는데 주 2회 얼마예요? 체험 수업 있나요?'),
          ('Saleringo', '+19초', '초등 전 피아노 주 2회는 <b>월 16만원</b>이고, 교재비는 별도입니다. 체험은 <b>30분 무료 1회</b>로, '
                                 '이번 주 <b>금요일 오후 4시</b>와 <b>토요일 11시</b>가 비어 있습니다.'),
          ('학부모', '4:38 PM', '금요일 4시요. 우리 애가 절대음감인 것 같은데 콩쿠르 나갈 수 있을까요?'),
          ('Saleringo', '+7초', '아이의 재능이나 콩쿠르 준비 여부는 원장님이 체험 수업에서 직접 보고 말씀드릴 부분입니다. '
                                '금요일 4시 체험으로 잡아 두었고, 아이 이름과 나이만 남겨 주시면 됩니다.')],
 'refuse': [('아이의 재능을 판단하지 않습니다.',
             '&ldquo;절대음감이면 전공 가능하겠네요&rdquo; 같은 말을 하지 않습니다. 원장님이 체험에서 보고 정합니다.'),
            ('콩쿠르 입상이나 입시 결과를 약속하지 않습니다.',
             '&ldquo;저희 다니면 예중 갑니다&rdquo;를 말하지 않습니다. 학원법상 문제이고, 아이마다 다릅니다.'),
            ('없는 교습비와 할인을 만들지 않습니다.',
             '신고된 교습비와 원장님이 넣어 둔 형제 할인만 안내합니다.'),
            ('차량 하차 장소를 전화로 바꾸지 않습니다.',
             '&ldquo;오늘만 할머니 집에 내려 주세요&rdquo;는 접수만 하고 원장님에게 넘깁니다. 차가 출발하기 전에 원장님이 학부모 본인에게 확인합니다.')],
 'fields': ['아이 나이와 악기 · 과목', '체험 예약 시각', '신고된 교습비 기준 안내 금액',
            '가능한 요일과 시간대', '집에 악기 보유 여부', '차량 · 하원 요청 원장님 전달 표시'],
 'stages': ['문의 접수', '체험 예약', '체험 수업', '반 배정', '등록 · 발표회'],
 'when': {'eyebrow': '레슨 중의 통화', 'h2': '피아노 앞에 앉아 있는 동안<br>이렇게 흘러갑니다.',
          'tt': '레슨 중', 'badge': '레슨실을 비울 수 없는 시간'},
 'lead': '레슨 중에 오는 체험 문의. 아이의 재능을 판단하지 않고, 무료 체험 시간을 잡습니다.',
 'group': 1,
 'en': {
  'name': 'Music & art schools', 'owner': 'the director',
  'kicker': 'Piano &middot; violin &middot; art schools',
  'h1': 'The lesson is one to one.<br>So is the phone.',
  'sub': 'A piano teacher cannot leave a seven-year-old mid-scale to take a trial-lesson call. '
         'That call comes at four in the afternoon, every day.',
  'cost': 'A music or art student stays for years: from first scales to sonatinas, from sketching to watercolour. '
          'But the first enquiry comes after school lets out, when the director is in the lesson room. '
          'The trial request nobody answered enrols at the school two floors down.',
  'call': [('Parent', '4:36 PM', 'My seven-year-old wants to start piano. How much is twice a week, and is there a trial lesson?'),
           ('Saleringo', '+19 s', 'Piano twice a week for beginners under eight is <b>$160 a month</b>, books separate. The trial is a free thirty minutes, '
                                  'and <b>Friday at 4 PM</b> or <b>Saturday at 11</b> are open this week.'),
           ('Parent', '4:38 PM', 'Friday at 4. I think she has perfect pitch. Could she enter competitions?'),
           ('Saleringo', '+7 s', 'How gifted she is, and whether to prepare for competitions, is something the director judges in the trial lesson itself. '
                                 'Friday at 4 is booked; just leave her name and age.')],
  'refuse': [('Never judges a child\'s talent.',
              'No "perfect pitch, she could go professional". The director hears the child in the trial and decides.'),
             ('Never promises a prize or an audition result.',
              'No "our students get into the conservatory". It differs by child, and it is not the school\'s promise to make.'),
             ('Never invents a fee or a discount.',
              'It quotes the registered tuition and only the sibling discount the director entered.'),
             ('Never changes a van drop-off by phone.',
              '"Just today, drop her at grandma\'s" is logged and passed to the director, who confirms it with the parent herself before the van leaves.')],
  'fields': ['Child\'s age and instrument or medium', 'Trial slot booked', 'Fee quoted from the registered tuition',
             'Days and times that suit the family', 'Instrument at home', 'Van or pickup request passed to the director'],
  'stages': ['Enquiry', 'Trial booked', 'Trial lesson', 'Class placed', 'Enrolled & recital'],
  'when': {'eyebrow': 'A call mid-lesson', 'h2': 'While the teacher is at the piano,<br>this is how it goes.',
           'tt': 'Mid-lesson', 'badge': 'Cannot leave the lesson room'},
  'lead': 'The trial-lesson call lands mid-lesson. The AI books the free trial and leaves the child\'s talent to the director.',
  'room': 'booked-by-appointment',
  'room_d': 'Trial-lesson calls answered while the teacher is at the piano: tuition read as registered, trial booked, and no verdict on talent or competitions.',
  'room_no': ('0', 'talent verdicts the AI gives'),
 },
},
{
 'slug': 'yoga-pilates', 'owner': '원장님', 'name': '요가 · 필라테스', 'photo': ph('PENDING'),
 'kicker': '요가 &middot; 필라테스 &middot; 기구 스튜디오',
 'h1': '저녁 수업은 꽉 찼고<br>음성사서함도 꽉 찼습니다.',
 'sub': '여섯 시부터 아홉 시까지 강사는 매트 위에 있고 데스크는 비어 있습니다. '
        '내일의 회원이 첫 수업을 묻는 시간이 바로 그때입니다.',
 'cost': '스튜디오 문의는 퇴근길에 옵니다. 저녁 수업이 돌아가는 세 시간 동안 하루 문의의 대부분이 들어오고, '
         '강사는 회원 앞에서 전화를 받을 수 없습니다. 놓친 문의는 앱으로 옆 스튜디오를 예약합니다. '
         '회원 한 명은 석 달이 아니라, 재등록을 거듭하는 몇 년입니다.',
 'call': [('문의', '7:08 PM', '필라테스 처음인데, 기구 개인 레슨이랑 그룹 가격이 어떻게 되나요? 임신 중인데 해도 되나요?'),
          ('Saleringo', '+21초', '기구 그룹은 <b>주 2회 월 22만원</b>, 개인 레슨은 <b>10회 75만원</b>입니다. 임신 중 운동은 담당 의사의 확인이 먼저고, '
                                 '가능 여부는 강사가 직접 상담해 드려야 해서 제가 판단하지 않습니다. 상담 겸 체험은 <b>내일 오전 11시</b>가 비어 있습니다.'),
          ('문의', '7:10 PM', '내일 11시로 할게요.'),
          ('Saleringo', '+6초', '내일 오전 11시 상담으로 잡아 두었습니다. 편한 운동복만 입고 오시면 되고, 미끄럼 방지 양말은 준비되어 있습니다. '
                                '성함과 연락처만 남겨 주세요.')],
 'refuse': [('운동해도 되는 몸인지 판단하지 않습니다.',
             '임신, 디스크, 수술 뒤에 해도 되는지는 의사 확인과 강사 상담이 정합니다. 말한 그대로 적고 판단은 남기지 않습니다.'),
            ('몸의 변화를 약속하지 않습니다.',
             '&ldquo;석 달이면 자세가 잡힙니다&rdquo;, &ldquo;체중이 빠집니다&rdquo;를 말하지 않습니다.'),
            ('회원권 양도와 기간 연장을 전화로 정해 주지 않습니다.',
             '원장님이 넣어 둔 규정 그대로 읽습니다. 규정에 없는 요청은 원장님 확인 항목으로 남깁니다.'),
            ('수업 중 통증이나 어지러움 신고는 강사에게 바로 갑니다.',
             '수업 중에 다쳤다, 어지럽다는 전화는 예약이 아니라 즉시 연결입니다.')],
 'fields': ['그룹 · 개인 구분과 경험 수준', '건강 관련 언급 원문 · 판단 없음', '상담 · 체험 예약 시각',
            '요금표 기준 안내 금액', '희망 수업 시간대', '회원권 규정 문의 원장님 확인 표시'],
 'stages': ['문의 접수', '체험 예약', '체험 · 상담', '등록', '재등록'],
 'when': {'eyebrow': '저녁 수업 중의 통화', 'h2': '강사가 매트 위에 있는 동안<br>이렇게 흘러갑니다.',
          'tt': '저녁 수업', 'badge': '회원 앞을 떠날 수 없는 시간'},
 'lead': '저녁 수업 중에 오는 첫 문의. 운동해도 되는지 판단하지 않고, 상담 겸 체험을 잡습니다.',
 'group': 1,
 'en': {
  'name': 'Yoga & pilates studios', 'owner': 'the owner',
  'kicker': 'Yoga &middot; pilates &middot; reformer studios',
  'h1': 'The evening class is full.<br>So is the voicemail.',
  'sub': 'From six to nine the instructor is on the mat and the desk is empty. '
         'That is exactly when tomorrow\'s members call to ask about a first session.',
  'cost': 'Studio enquiries come on the way home from work. Most of the day\'s calls land during the three evening classes, '
          'and an instructor cannot answer in front of a room of members. The caller who was not answered books the studio next door in an app. '
          'A member is not three months; it is years of renewals.',
  'call': [('Enquirer', '7:08 PM', 'I\'m new to pilates. What do reformer group and private sessions cost? And I\'m pregnant. Is it okay?'),
           ('Saleringo', '+21 s', 'Reformer group twice a week is <b>$220 a month</b>, and a private ten-pack is <b>$750</b>. Exercise in pregnancy needs your doctor\'s okay first, '
                                  'and the instructor will talk it through with you; I cannot judge that. A consultation with a trial is open <b>tomorrow at 11 AM</b>.'),
           ('Enquirer', '7:10 PM', 'Tomorrow at 11, then.'),
           ('Saleringo', '+6 s', 'Booked for tomorrow at 11. Come in comfortable clothes; grip socks are here. Just leave a name and a number.')],
  'refuse': [('Never decides whether someone may exercise.',
              'Pregnancy, a disc, recent surgery: that is a doctor\'s clearance and an instructor\'s conversation. The AI writes down what was said and adds no verdict.'),
             ('Never promises a body.',
              'No "three months and your posture is fixed", no "you will lose the weight".'),
             ('Never rewrites the membership terms.',
              'Transfers, freezes and extensions follow the owner\'s rules as written. Anything not in them waits for her.'),
             ('Pain or dizziness in a class goes to the instructor at once.',
              'A member calling about an injury or feeling faint mid-class is not an enquiry; it connects a person immediately.')],
  'fields': ['Group or private, and experience', 'Health note in the caller\'s own words, not assessed', 'Consultation or trial slot booked',
             'Membership price quoted from the list', 'Preferred class times', 'Membership question flagged to the owner'],
  'stages': ['Enquiry', 'Trial booked', 'Trial & consultation', 'Membership', 'Renewal'],
  'when': {'eyebrow': 'A call mid-class', 'h2': 'While the instructor is on the mat,<br>this is how it goes.',
           'tt': 'Evening class', 'badge': 'Cannot leave the room'},
  'lead': 'The first enquiry during the evening class. The AI books the consultation and refuses to say whether the caller may exercise.',
  'room': 'booked-by-appointment',
  'room_d': 'First-session calls answered while the instructor is on the mat: prices read from the list, consultation booked, and every health question left to a doctor and the instructor.',
  'room_no': ('0', 'health clearances the AI gives'),
 },
},
]
