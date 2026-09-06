# -*- coding: utf-8 -*-
"""English page data for 12 original trades — used by p_trades/p_packs to generate en/industries/<slug>.html and -pack.html."""
EN1 = {
 'dental': {
  'name': 'Dental', 'owner': 'the dentist',
  'kicker': 'Dental &middot; family dentistry &middot; cosmetic',
  'h1': 'The call at eleven at night<br>is almost always a new patient.',
  'sub': 'Someone with a tooth that hurts searches, finds you and dials. If nobody answers, they dial the next practice. '
         'Existing patients ring back; new ones do not.',
  'cost': 'A new patient is not one visit. A cleaning leads to a crown and a crown to an implant, so the missed call is worth '
          'more than the one procedure asked about. That loss is never written down anywhere &mdash; the calls that rang out '
          'over lunch and after closing sit in the phone log and nowhere in the month-end numbers.',
  'call': [('Patient', '11:42 PM', 'Hi &mdash; I chipped a front tooth. How much is a crown, and can anyone see me this week?'),
           ('Saleringo', '+12 s', 'I&rsquo;m sorry, that&rsquo;s never fun. From our fee schedule a crown runs <b>$1,100 to $1,600</b> '
                                  'depending on the material, and the exam with X-rays is <b>$95</b>. This week I have '
                                  '<b>Thursday at 10:30 AM</b> or <b>Friday at 8:00 AM</b>. Which works better?'),
           ('Patient', '11:43 PM', 'Thursday, please. It&rsquo;s Jane Kim, 555-0147.'),
           ('Saleringo', '+6 s', 'Thank you, Jane. You&rsquo;re booked for Thursday at 10:30 AM, and I&rsquo;m texting a confirmation now '
                                 'with directions and parking since it&rsquo;s your first visit. Is the tooth painful right now, or just sensitive?'),
           ('Patient', '11:44 PM', 'A little sensitive, that&rsquo;s all.'),
           ('Saleringo', '+5 s', 'Then avoid very cold food until Thursday, and if the pain gets worse call this number again &mdash; '
                                 'I answer at night too. We&rsquo;ll see you Thursday.')],
  'refuse': [('It never names a diagnosis from a description.',
              'Whether a chipped tooth needs a crown, a veneer or root canal work is decided in the chair, and saying it on the '
              'phone is practising dentistry without looking. The AI stops at &ldquo;that needs to be seen&rdquo; and books the visit.'),
             ('It never invents a fee.',
              'It quotes only the items on the fee schedule the dentist loaded. Anything not on it is logged as &ldquo;confirm at the visit&rdquo;.'),
             ('It never rules on insurance coverage.',
              'What a plan pays for a crown depends on the plan and the code. The AI asks the patient to bring the card and hands the question to the desk.'),
             ('It never books severe pain into next week.',
              'A patient in pain they cannot bear at night gets the emergency script and the on-call number, not a Thursday slot.')],
  'fields': ['New or existing patient and how they found you', 'Procedure asked about and the tooth',
             'Estimated range from the fee schedule', 'Time asked for and the slot booked',
             'Insurance or out-of-pocket question raised', 'Confirmation text sent'],
  'stages': ['Inquiry', 'Appointment booked', 'Visit', 'Treatment plan consult', 'Treatment and rebooking'],
  'when': {'eyebrow': 'Tuesday 11:42 PM, the call', 'h2': 'How it goes<br>hours after the practice locks up.', 'tt': 'chipped tooth, late night', 'badge': 'after hours'},
  'lead': 'The new patient calls at 11:42 PM. It quotes the crown off your own fee schedule, books Thursday, and leaves the insurance question for the desk.',
  'room': 'health-care',
  'room_d': 'The 11:42 PM chipped-tooth call quoted from your own fee schedule and booked for Thursday at 10:30 &mdash; with the insurance question passed to the desk, not answered.',
  'room_no': ('0', 'diagnoses or coverage promises made over the phone'),
 },
 'clinics': {
  'name': 'Clinics & med-spa', 'owner': 'the doctor',
  'kicker': 'Dermatology &middot; med-spa &middot; aesthetic clinics',
  'h1': 'The price question is the call<br>you get most and must answer most carefully.',
  'sub': 'Treatment prices are not on the website, so people phone to ask. Answer that call badly and it is no longer '
         'a booking question but an advertising-rules problem.',
  'cost': 'Almost every aesthetic inquiry opens with a price, and the one that goes unanswered becomes a consultation at the '
          'clinic down the street. The same call is where the risk lives: a promised result, a comparison with a competitor '
          'or a misquoted promotion is a compliance complaint waiting to happen. The line a trained receptionist keeps, the machine has to keep too.',
  'call': [('Customer', '9:18 PM', 'How much is Botox? It&rsquo;s my first time &mdash; does it hurt?'),
           ('Saleringo', '+14 s', 'From our price list, the forehead and frown lines are <b>$190 per area</b>, and the jawline starts at '
                                  '<b>$390</b>. Pain and results vary from person to person, so I can&rsquo;t speak to those &mdash; the doctor '
                                  'goes through them with you at the consultation. Which area are you thinking of?'),
           ('Customer', '9:19 PM', 'Forehead and frown lines. When could I come in?'),
           ('Saleringo', '+7 s', 'I have a consultation slot this <b>Thursday at 3:00 PM</b>. Shall I book that for you?'),
           ('Customer', '9:20 PM', 'Yes, let&rsquo;s do that. Seoyeon Lee, 555-0314.'),
           ('Saleringo', '+6 s', 'Thank you, Seoyeon. You&rsquo;re booked for Thursday at 3:00 PM. Since it&rsquo;s your first visit, '
                                 'just bring a photo ID &mdash; I&rsquo;ll text the confirmation now.')],
  'refuse': [('It never promises a result or rules out side effects.',
              'Whether Botox works on one person&rsquo;s skin and what it does after is a clinical judgement. '
              'The AI says results vary and passes the question to the doctor.'),
             ('It never compares you with another clinic.',
              'Saying you are better than the place across town is an advertising-rules breach. It states only your prices and your calendar.'),
             ('It never diagnoses.',
              'It does not listen to a description of someone&rsquo;s skin and say what the problem is. That takes eyes on the patient.'),
             ('It never writes its own marketing line.',
              'Every sentence it can say about a treatment was loaded by the clinic in advance. It does not improvise a claim.')],
  'fields': ['Treatment asked about and the area', 'First consultation or returning patient',
             'Price quoted from the price list', 'Consultation time booked',
             'How they found you (search, channel, referral)', 'Contact method they agreed to'],
  'stages': ['Inquiry', 'Consultation booked', 'Consultation', 'Treatment decided', 'Treatment and aftercare'],
  'when': {'eyebrow': 'Wednesday 9:18 PM, the call', 'h2': 'How it goes<br>after the clinic has closed for the night.', 'tt': 'first-time price call', 'badge': 'after hours'},
  'lead': 'The Botox price call comes at 9:18 PM. It quotes your loaded price list, books Thursday&rsquo;s consultation, and leaves results and side effects to the doctor.',
  'room': 'health-care',
  'room_d': 'The 9:18 PM Botox inquiry answered from your own price list and a consultation held for Thursday at 3:00 PM &mdash; with results and side effects left to the doctor.',
  'room_no': ('0', 'results promised or clinics compared'),
 },
 'veterinary': {
  'name': 'Veterinary', 'owner': 'the vet',
  'kicker': 'Veterinary &middot; animal hospitals &middot; emergency',
  'h1': 'The urgent call and the routine call<br>must never be mixed up.',
  'sub': 'Night calls to a vet come in two kinds: the animal that has to be seen now, and the one that can wait for '
         'tomorrow&rsquo;s appointment. Treat them the same and you lose both.',
  'cost': 'The night call is made by a frightened owner. Miss it and they drive to the 24-hour hospital, which becomes their '
          'vet from then on. The same line also carries vaccination and neutering questions that can wait until morning. '
          'Send the emergency straight to a person and turn the rest into appointments, and most of the night is handled.',
  'call': [('Client', '10:51 PM', 'I think my dog ate some chocolate. What should I do?'),
           ('Saleringo', '+5 s', 'Chocolate can be an emergency, so I won&rsquo;t book an appointment &mdash; I&rsquo;m connecting you to our '
                                 'on-call vet right now. Try to remember <b>how much he ate, when, and his weight</b>, and please don&rsquo;t make him vomit.'),
           ('Client', '10:52 PM', 'Okay, please. About half a bar, an hour ago. He&rsquo;s around 11 pounds. It&rsquo;s Haneul Jung, 555-0712 '
                                  '&mdash; the dog&rsquo;s name is Bean.'),
           ('Saleringo', '+4 s', 'Thank you, Haneul. I&rsquo;ve noted all of this on Bean&rsquo;s record and passed it to the on-call vet '
                                 'word for word. Connecting you now &mdash; one moment.')],
  'refuse': [('It never diagnoses.',
              'It does not hear a symptom and name a condition or a treatment. That is the vet&rsquo;s job.'),
             ('It routes an emergency signal to a person at once.',
              'Poisoning, breathing trouble, seizures, bleeding or a birth in progress mean no appointment &mdash; the on-call vet is connected on the spot.'),
             ('It never advises on medicine or doses.',
              'Whether a human tablet in the cupboard can be given to a dog is a question it does not answer. It goes to the vet before the visit.'),
             ('It never says an animal is fit for surgery.',
              'Age and weight over the phone are not an assessment. That is decided after the exam.')],
  'fields': ['Owner and pet (species, age, weight)', 'Symptom and when it started',
             'Emergency verdict and the reason for it', 'On-call vet connected, and when',
             'Appointment time, when it is not urgent', 'Vaccination or procedure history asked about'],
  'stages': ['Inquiry', 'Triage', 'Booked or connected', 'Visit', 'Recheck and vaccination reminders'],
  'when': {'eyebrow': 'Friday 10:51 PM, the call', 'h2': 'How it goes<br>when the practice is dark and the dog ate chocolate.', 'tt': 'suspected poisoning', 'badge': 'after hours'},
  'lead': 'The chocolate call comes at 10:51 PM. It recognises the poisoning keyword, skips the booking and connects the on-call vet with the owner&rsquo;s words attached.',
  'room': 'health-care',
  'room_d': 'The 10:51 PM chocolate call triaged as an emergency and put through to the on-call vet at once &mdash; amount, time and weight on the record, and no medication advice given.',
  'room_no': ('0', 'medicines or doses suggested to an owner'),
 },
 'senior-care': {
  'name': 'Senior care', 'owner': 'the owner',
  'kicker': 'Senior care &middot; day programs &middot; home care',
  'h1': 'The hardest call is made<br>by someone who is already exhausted.',
  'sub': 'It is the call to find care for a parent. The person dialling is worn out and does not know what to ask first. '
         'This is the one call a person should take &mdash; so the whole job is handing it to a person well.',
  'cost': 'Care is chosen after a consultation, a visit and a family discussion. Miss the first call and that long process '
          'starts at another provider. On top of that, care levels, covered services and the family&rsquo;s share are set by '
          'the funding office, so the provider cannot answer freely. The AI does one thing: it gathers the facts and passes them on.',
  'call': [('Customer', '8:12 PM', 'My father&rsquo;s just been assessed at care level three. What does day care cost per day?'),
           ('Saleringo', '+16 s', 'At level three he&rsquo;s eligible for our day program. How much his benefits cover depends on his level '
                                  'and income band &mdash; the funding office sets that, so I can&rsquo;t work out his share. What I can tell you: '
                                  'the day runs <b>9:00 to 5:00</b>, lunch and snacks are <b>$5 a day</b>, and we run a pickup van.'),
           ('Customer', '8:13 PM', 'How far does the van go? We&rsquo;re in Riverside.'),
           ('Saleringo', '+6 s', 'Riverside is on the van route. For times and how it all works, could our care advisor call you '
                                 '<b>tomorrow at 10:00 AM</b>? I&rsquo;d just need your name, a number and how you&rsquo;re related to him.'),
           ('Customer', '8:14 PM', 'Yes, please. I&rsquo;m his daughter, Eunjung Choi, 555-0297. He&rsquo;s Youngho Choi, 82, and the '
                                   'assessment came through last week.'),
           ('Saleringo', '+7 s', 'Thank you, Eunjung. I&rsquo;ve noted all of that, and our advisor will call you at ten tomorrow. '
                                 'The funding office can confirm his share if you&rsquo;d like to check before then.')],
  'refuse': [('It never calculates the family&rsquo;s share.',
              'The co-payment is set by the funding office from the care level and the income band. It is not a number a provider can quote in advance.'),
             ('It never predicts a care-level assessment.',
              'It does not say &ldquo;he sounds like a level three&rdquo;. The assessment is someone else&rsquo;s decision.'),
             ('It never judges a parent&rsquo;s condition.',
              'It does not hear symptoms and decide which service fits. That is settled at the visit.'),
             ('It never confirms a place.',
              'Capacity and the waiting list change by the day. It says the owner will check, and the family hears on the advisor call.')],
  'fields': ['Age and care level', 'Service wanted (residential, day program, home visits)',
             'Relationship to the caller and contact number', 'Area the van would need to cover',
             'Advisor call time', 'Funding office mentioned'],
  'stages': ['Inquiry', 'Advisor call booked', 'Phone consultation', 'Visit and show-round', 'Agreement and first day'],
  'when': {'eyebrow': 'Monday 8:12 PM, the call', 'h2': 'How it goes<br>after the office has gone home for the evening.', 'tt': 'daughter calling about her father', 'badge': 'after hours'},
  'lead': 'The daughter calls at 8:12 PM. It gives the hours, the $5 lunch and the van route, books the advisor for ten tomorrow, and leaves the co-payment and the place to people.',
  'room': 'health-care',
  'room_d': 'The 8:12 PM day-care inquiry answered with hours, meals and the van route, an advisor call set for tomorrow at 10:00 &mdash; and no co-payment figure or place confirmed.',
  'room_no': ('0', 'co-payments calculated or places promised'),
 },
 'home-services': {
  'name': 'Home services', 'owner': 'the owner',
  'kicker': 'Plumbing &middot; heating &middot; repairs',
  'h1': 'A house with water on the floor<br>is already dialling the second company.',
  'sub': 'When the boiler dies or a pipe bursts, nobody waits. They search, call from the top of the list down, '
         'and whoever answers first goes out that night.',
  'cost': 'Repair calls arrive as a mix of urgent and not, and the urgent ones are the high-ticket jobs because someone has '
          'to go today. While the owner is on a job, both kinds ring out. Eight missed calls in the evening do not tell you '
          'which one should have been today&rsquo;s visit.',
  'call': [('Customer', '8:47 PM', 'My boiler won&rsquo;t turn on. Can someone come tonight? It&rsquo;s showing error code E9.'),
           ('Saleringo', '+5 s', 'One thing first &mdash; do you smell gas, or anything burning, or see smoke?'),
           ('Customer', '8:48 PM', 'No, nothing like that. It just won&rsquo;t start.'),
           ('Saleringo', '+9 s', 'Good. E9 means different things on different boilers, so a tech needs to see it to be sure. Tonight I can do '
                                 '<b>after 10:00 PM</b>, and a night call-out is <b>$85</b> plus any parts. <b>Tomorrow at 8:00 AM</b> is also open. '
                                 'Which do you prefer?'),
           ('Customer', '8:49 PM', 'I&rsquo;ve got a baby at home, so tonight, please. Chaewon Lim, 555-0256 &mdash; 24 Bank Road, '
                                   'Harbor View Apartments, unit 702.'),
           ('Saleringo', '+7 s', 'Thank you, Chaewon. You&rsquo;re booked for ten tonight, and the tech will call you when he&rsquo;s on his way. '
                                 'Please don&rsquo;t open up the boiler while you wait, and if you smell gas at any point call this number again straight away.')],
  'refuse': [('It never diagnoses the fault on the phone.',
              'An error code or a noise is not a verdict on what is broken. It goes as far as &ldquo;could be&rdquo; and leaves the rest to the visit.'),
             ('It never fixes the final total.',
              'It states the call-out and the basic labour. Parts are priced once the unit is open, so the customer asking '
              '&ldquo;it won&rsquo;t go above that, right?&rdquo; hears from the tech, not the AI.'),
             ('It never books a job where someone smells gas.',
              'Gas, shocks, sparks or smoke trigger the safety script and an immediate transfer to a person, not a time slot.'),
             ('It never tells anyone to have a go themselves.',
              'No &ldquo;try taking the cover off&rdquo;. An accident after that advice lands on the company.')],
  'fields': ['Fault described and when it began', 'Building type and floor',
             'Preferred visit time and the time booked', 'Service area and full address',
             'Safety script triggered or not', 'Parts check needed before the visit'],
  'stages': ['Inquiry', 'Visit booked', 'On-site check', 'Estimate approved', 'Work done and paid'],
  'when': {'eyebrow': 'Tuesday 8:47 PM, the call', 'h2': 'How it goes<br>after the crew has gone home for the night.', 'tt': 'boiler down, baby at home', 'badge': 'crew off'},
  'lead': 'The boiler call comes at 8:47 PM. It runs the gas check first, quotes the $85 night call-out, books ten tonight, and leaves the final total to the tech.',
  'room': 'home-property',
  'room_d': 'The 8:47 PM boiler call screened for gas and smoke first, quoted the $85 night call-out and booked for ten tonight &mdash; with the final total left to the tech who opens it up.',
  'room_no': ('0', 'final totals guaranteed before the boiler is open'),
 },
 'pest-control': {
  'name': 'Pest control', 'owner': 'the owner',
  'kicker': 'Pest control &middot; extermination &middot; recurring plans',
  'h1': 'Someone who has just seen a roach<br>is calling right now.',
  'sub': 'Nobody waits until morning. They search where they stand, and the company that picks up gets the job.',
  'cost': 'Pest calls pile up after the office closes, because the person who saw something on the way to bed dials on the spot. '
          'And the job rarely ends at one visit: a treatment turns into a recurring plan, and a restaurant or an office turns '
          'into an annual contract. The call that rang out at night may have been a year&rsquo;s work.',
  'call': [('Customer', '11:16 PM', 'Hi &mdash; I&rsquo;m in a studio apartment and I keep seeing roaches. How much is it, and how soon can someone come?'),
           ('Saleringo', '+13 s', 'That&rsquo;s an unpleasant thing to find at night. From our rate card, a single treatment for a studio starts at '
                                  '<b>$150</b>, and if you&rsquo;re seeing them often I&rsquo;d suggest the two-visit package at <b>$250</b>, with a '
                                  'follow-up in two weeks. Tomorrow I have <b>2:00 PM</b> or <b>5:00 PM</b>. Which works better?'),
           ('Customer', '11:17 PM', 'Two tomorrow. Is the spray strong-smelling? I have a cat.'),
           ('Saleringo', '+8 s', 'With a pet in the home, the products and the method change, so the technician will call you before the visit '
                                 'to go over it. Can I get your name and a mobile number?'),
           ('Customer', '11:18 PM', 'Maya Torres, 555-0281. They&rsquo;re mostly under the kitchen sink and in the bathroom.'),
           ('Saleringo', '+6 s', 'Thank you, Maya. You&rsquo;re booked for tomorrow at 2:00 PM and I&rsquo;m texting the confirmation now. '
                                 'Under the sink and the bathroom &mdash; noted. Keep food sealed until then, and the technician will call in the morning.')],
  'refuse': [('It never names the species from a description.',
              'What is under the sink is identified on site, not from &ldquo;small and brown&rdquo; on the phone.'),
             ('It never promises total eradication.',
              'It does not say &ldquo;one visit and they&rsquo;re gone&rdquo;. It is not true, and it is where disputes start.'),
             ('It never rules on product safety around a pet or a child.',
              'Which product, and where the cat should be during the visit, is the technician&rsquo;s call. '
              'The AI books the pre-visit call and passes the question along.'),
             ('It never describes what is inside a wall or a pipe.',
              'How far an infestation reaches behind the tiles is known only after it has been opened up.')],
  'fields': ['Pest and where it was seen', 'Building type and size', 'Pets or infants in the home',
             'Preferred time and the time booked', 'Single treatment or recurring plan', 'Follow-up visit date'],
  'stages': ['Inquiry', 'Treatment booked', 'Treatment', 'Follow-up visit', 'Recurring plan'],
  'when': {'eyebrow': 'Tuesday 11:16 PM, the call', 'h2': 'How it goes<br>when the office closed hours ago and the roach did not.', 'tt': 'roaches in a studio', 'badge': 'after hours'},
  'lead': 'The roach call comes at 11:16 PM. It quotes $150 single or $250 for two visits off your rate card, books 2:00 PM tomorrow, and sends the cat question to the technician.',
  'room': 'home-property',
  'room_d': 'The 11:16 PM roach call quoted from your own rate card and booked for 2:00 PM tomorrow &mdash; with the question of what is safe around the cat handed to the technician.',
  'room_no': ('0', 'products declared pet-safe before the technician has looked'),
 },
 'property-management': {
  'name': 'Property management', 'owner': 'the property manager',
  'kicker': 'Property management &middot; apartments &middot; facilities',
  'h1': 'The management office phone<br>rings after the office has gone home.',
  'sub': 'Leaks, outages and parking rows do not keep office hours. Miss that call and tomorrow&rsquo;s complaints double.',
  'cost': 'A missed call here comes back as a complaint, not as lost revenue. Miss a leak report at night and by morning the '
          'unit below is wet too, and a repair bill has become a liability claim. There is no night porter, and forwarding '
          'the line puts the manager on call around the clock. What is needed is a front door that sorts urgent from not, at night as well.',
  'call': [('Resident', '1:04 AM', 'There&rsquo;s water coming through my ceiling. Is anyone there right now?'),
           ('Saleringo', '+4 s', 'A leak is urgent, so I&rsquo;m getting the on-call technician for you now. Which building and apartment, '
                                 'and where exactly is the water coming in?'),
           ('Resident', '1:05 AM', 'Building 3, apartment 902. It&rsquo;s the bathroom ceiling, right next to the exhaust fan.'),
           ('Saleringo', '+6 s', 'Building 3, 902, bathroom ceiling &mdash; logged. Since it&rsquo;s next to the fan, please switch off the '
                                 'bathroom breaker first, to be safe. Can I get your name and a mobile number so the technician has it?'),
           ('Resident', '1:06 AM', 'Daniel Reyes, 555-0362. Please hurry.'),
           ('Saleringo', '+5 s', 'Thank you, Daniel. I&rsquo;m connecting you to the on-call technician now &mdash; they&rsquo;ll call within '
                                 'ten minutes and come up if needed. Put a bucket under it in the meantime.')],
  'refuse': [('It never decides whose fault it is.',
              'Whether the water came from the unit above or from the building&rsquo;s own plumbing is settled after inspection. '
              'The AI logs the report and passes it up.'),
             ('It never says who pays for the repair.',
              'Whether it is covered by the building or charged to a resident depends on the rules and the cause. '
              'The &ldquo;they pay, not me, right?&rdquo; question goes to the office.'),
             ('It never gives out another resident&rsquo;s details.',
              'Who lives upstairs and how to reach them is not something it tells a caller.'),
             ('It never turns an emergency into a booking.',
              'A leak, a power failure, someone stuck in a lift or a smell of gas is connected immediately, not scheduled.')],
  'fields': ['Building, unit and where the problem is', 'Report in the resident&rsquo;s own words', 'Urgency verdict',
             'Who was connected and at what time', 'Scheduled follow-up repair', 'Repeat report from the same unit'],
  'stages': ['Report received', 'Triage', 'Assigned', 'On site', 'Resident updated'],
  'when': {'eyebrow': 'Tuesday 1:04 AM, the call', 'h2': 'How it goes<br>at one in the morning with water through the ceiling.', 'tt': 'ceiling leak, 1 AM', 'badge': 'office closed'},
  'lead': 'The leak call comes at 1:04 AM. It logs the unit and the location, says to switch off the breaker, connects the on-call technician, and leaves who pays to the office.',
  'room': 'home-property',
  'room_d': 'The 1:04 AM ceiling leak logged with building and unit, the breaker advice given and the on-call technician connected by 1:07 &mdash; and no ruling on whose fault it was.',
  'room_no': ('0', 'fault or repair costs decided on the phone'),
 },
 'real-estate': {
  'name': 'Real estate', 'owner': 'the broker',
  'kicker': 'Real estate &middot; rentals &middot; brokerages',
  'h1': 'The listing inquiry arrives<br>while the broker is out showing homes.',
  'sub': 'The hours spent at viewings are exactly the hours people call. That one call is either your next contract '
         'or the brokerage down the street&rsquo;s.',
  'cost': 'Several offices carry the same listing, so whoever answers first books the showing, and whoever books the showing '
          'writes the contract. The broker cannot pick up precisely when out at a showing &mdash; which means the busier the '
          'office gets, the more calls it drops.',
  'call': [('Customer', '7:24 PM', 'Is that two-bedroom on Alder Street still available? And how many parking spaces does it have?'),
           ('Saleringo', '+11 s', 'Yes, it&rsquo;s still available. Parking is one assigned space, and visitors park on the street. From the '
                                  'listing, rent is <b>$2,400 a month</b> with a one-month deposit. I can show it <b>tomorrow at 11:00 AM</b> '
                                  'or at <b>3:00 PM</b>.'),
           ('Customer', '7:25 PM', 'Three works. Sorry &mdash; are you the agent?'),
           ('Saleringo', '+6 s', 'No, I&rsquo;m an AI assistant. I can share what&rsquo;s in the listing and book the viewing; anything about '
                                 'terms or the lease is for the broker. May I take your name and a mobile number?'),
           ('Customer', '7:26 PM', 'Olivia Park, 555-0419. I&rsquo;m hoping to move in at the end of next month.'),
           ('Saleringo', '+7 s', 'Thank you, Olivia. You&rsquo;re booked for tomorrow at 3:00 PM, and the broker will call you beforehand '
                                 'and meet you at the property. ID is checked there, and I&rsquo;m texting you the address now.')],
  'refuse': [('It never passes itself off as the agent.',
              'Asked, it says it is an AI. Nothing that needs a licence is said by something without one.'),
             ('It never negotiates.',
              'It does not knock anything off the rent or the deposit. It reads the terms as listed, books the showing, '
              'and a &ldquo;would they take $2,200?&rdquo; goes to the broker.'),
             ('It never explains title or liens.',
              'Mortgages, prior claims and who holds what are read off the record and explained by the broker.'),
             ('It never gives an investment opinion.',
              'Whether the area will go up, or whether to buy at all, is not a question it answers.')],
  'fields': ['Listing number and property type', 'What they want (budget, move-in date, floor, parking)',
             'Showing time booked', 'Buying or renting',
             'How they found the listing (portal, sign, referral)', 'Contact consent'],
  'stages': ['Inquiry', 'Showing booked', 'Showing', 'Terms negotiated', 'Contract'],
  'when': {'eyebrow': 'Wednesday 7:24 PM, the call', 'h2': 'How it goes<br>while the broker is out on showings.', 'tt': 'listing call, mid-showing', 'badge': 'broker out'},
  'lead': 'The Alder Street call comes at 7:24 PM. It reads the listing as written, says it is an AI when asked, books tomorrow at three, and sends the rent offer to the broker.',
  'room': 'home-property',
  'room_d': 'The 7:24 PM Alder Street inquiry answered from the listing as written and a showing booked for 3:00 PM tomorrow &mdash; the $2,200 offer passed to the broker, not answered.',
  'room_no': ('0', 'rents negotiated or agents impersonated'),
 },
 'auto-repair': {
  'name': 'Auto repair', 'owner': 'the owner',
  'kicker': 'Auto repair &middot; brakes &middot; service',
  'h1': 'Nobody answers the phone<br>from under a lift.',
  'sub': 'You cannot wipe your hands and climb out every time it rings. The estimate call that comes in meanwhile '
         'goes straight to the shop next door.',
  'cost': 'Most repair calls are &ldquo;it&rsquo;s making this noise &mdash; what will it cost?&rdquo; Both sides know the exact figure '
          'cannot be given on the phone. What the caller wants is a rough range and whether you can take the car today. '
          'Answer those two and the drop-off gets booked &mdash; but the one person who can answer is under a car.',
  'call': [('Customer', '4:47 PM', 'My brakes are making a metal grinding noise. Can you look at it today?'),
           ('Saleringo', '+10 s', 'That could be worn pads, but nobody can say for sure without seeing the car. From our rate card, front pads '
                                  'start at <b>$180</b>, more if the rotors need work. Today the lift frees up <b>after 6:00 PM</b>, or I have '
                                  '<b>9:00 AM tomorrow</b>.'),
           ('Customer', '4:48 PM', 'Nine tomorrow. It&rsquo;s a 2019 Civic. Chris Nguyen, 555-0524.'),
           ('Saleringo', '+7 s', 'Thank you, Chris. You&rsquo;re booked for a 9:00 AM drop-off tomorrow. I&rsquo;m texting a confirmation now '
                                 '&mdash; reply with your plate number and we&rsquo;ll check pad stock before you arrive. Is the car still stopping normally?'),
           ('Customer', '4:49 PM', 'It stops fine, it&rsquo;s just the noise.'),
           ('Saleringo', '+5 s', 'Then go easy on hard braking until tomorrow, and if the pedal goes soft or you see smoke, call this number '
                                 'right away. See you at nine.')],
  'refuse': [('It never names the cause from a noise.',
              'It does not end with &ldquo;just needs pads&rdquo;. It goes as far as &ldquo;could be&rdquo; and leaves the verdict to the inspection.'),
             ('It never fixes the final price.',
              'It gives the rate-card labour and the parts range. The estimate is written with the car on the lift.'),
             ('It routes a safety symptom straight to a person.',
              'No braking, smoke, or a wheel pulling hard are not a booking &mdash; they are advice and a transfer.'),
             ('It never rules on insurance.',
              'Whether a job is covered and what the deductible is are the insurer&rsquo;s decisions. The AI states the facts and hands the question to the desk.')],
  'fields': ['Vehicle, year and mileage', 'Symptom in the customer&rsquo;s words', 'Range from the rate card',
             'Preferred drop-off and the time booked', 'Parts stock to check before arrival', 'Insurance or self-pay'],
  'stages': ['Inquiry', 'Drop-off booked', 'Check-in and inspection', 'Estimate approved', 'Work and collection'],
  'when': {'eyebrow': 'Wednesday 4:47 PM, the call', 'h2': 'How it goes<br>while the owner is under a lift.', 'tt': 'grinding brakes, mid-job', 'badge': 'hands full'},
  'lead': 'The brake call comes at 4:47 PM with the owner under a car. It gives the rate-card range from $180, books nine tomorrow, and leaves the insurance question for the desk.',
  'room': 'vehicle-plant-storage',
  'room_d': 'The 4:47 PM grinding-brakes call given the rate-card range from $180 and a 9:00 AM drop-off booked &mdash; with the deductible question handed to the desk, not guessed.',
  'room_no': ('0', 'causes named or coverage promised from a noise on the phone'),
 },
 'movers': {
  'name': 'Movers', 'owner': 'the owner',
  'kicker': 'Movers &middot; removals &middot; packing',
  'h1': 'The estimate call comes<br>while the crew is carrying someone else&rsquo;s sofa.',
  'sub': 'A moving inquiry goes to three companies at once. The first to answer books the survey, and the one that '
         'books the survey signs the job.',
  'cost': 'Moving inquiries cluster around weekends and month-end, exactly when the owner is on a truck. The hours spent '
          'lifting are the hours next month&rsquo;s work is decided. And a price named without seeing the load, when it differs '
          'from the bill on the day, becomes an argument on the doorstep.',
  'call': [('Customer', '9:33 PM', 'I&rsquo;m moving from a studio to a two-bedroom on the 15th next month. Roughly what would that cost?'),
           ('Saleringo', '+13 s', 'It depends on how much you have, so the exact figure comes after a survey. From our rate card, a '
                                  'studio-to-two-bedroom move usually runs <b>$600 to $1,000</b>. The 15th is a Saturday and fills fast &mdash; '
                                  'I can do a survey this <b>Thursday at 7:00 PM</b>.'),
           ('Customer', '9:34 PM', 'Thursday at seven works. My current place is a third-floor walk-up, no elevator. Ethan Brooks, 555-0631, '
                                   'at 42 Elm Street.'),
           ('Saleringo', '+8 s', 'Third floor, no elevator &mdash; noted. That may need extra crew, and the surveyor will confirm on Thursday. '
                                 'Do you have the new address too?'),
           ('Customer', '9:35 PM', 'Yes, 110 Oakridge Avenue, and that building has an elevator.'),
           ('Saleringo', '+6 s', 'Oakridge, with an elevator &mdash; noted. Your survey is booked for Thursday at 7:00 PM and I&rsquo;m texting '
                                 'the confirmation. The move date is confirmed with the contract after the survey, so the 15th is down as your preferred date for now.')],
  'refuse': [('It never fixes a price without seeing the load.',
              'It gives the range and books the survey. Most disputes in this trade start with a number given blind.'),
             ('It never skips the stairs question.',
              'Elevator or not, and which floor, are always asked and written down as said. Extra crew or a hoist are never quietly dropped from the job.'),
             ('It never pencils in the move date as booked.',
              'The survey is the booking. The move date is fixed by the contract, not by the phone call.'),
             ('It never promises what damage is covered.',
              'Whether a broken TV is replaced in full depends on the valuation option chosen. The owner explains it from the policy; '
              'the AI passes the question on.')],
  'fields': ['From and to addresses, with floors', 'Elevator, or extra crew and hoist needed', 'Preferred move date',
             'Size of the load (studio, two-bedroom, house)', 'Survey time booked', 'Range quoted'],
  'stages': ['Inquiry', 'Survey booked', 'Survey', 'Contract', 'Move and settlement'],
  'when': {'eyebrow': 'Monday 9:33 PM, the call', 'h2': 'How it goes<br>while the crew is still on a job.', 'tt': 'studio to two-bed', 'badge': 'crew out'},
  'lead': 'The estimate call comes at 9:33 PM with the crew still out. It gives the $600 to $1,000 range, books Thursday&rsquo;s survey, and leaves damage coverage to the owner.',
  'room': 'vehicle-plant-storage',
  'room_d': 'The 9:33 PM studio-to-two-bedroom call given the rate-card range and a survey booked for Thursday at 7:00 PM &mdash; with the damage-coverage question sent to the owner, not promised.',
  'room_no': ('0', 'prices fixed or damage coverage promised before the survey'),
 },
 'self-storage': {
  'name': 'Self storage', 'owner': 'the owner',
  'kicker': 'Self storage &middot; units &middot; unstaffed sites',
  'h1': 'The more unstaffed the site,<br>the fewer people there are to answer.',
  'sub': 'Running without staff on site is the whole point of the business. But the inquiries still come to a person.',
  'cost': 'Almost every inquiry is one of three: how much, which size, and is there one free. All three can be answered from '
          'what is already on file, and yet with nobody on site they ring out. A rental, once started, runs for months or '
          'years &mdash; a $129 unit over two years is more than $3,000 walking to the facility down the road.',
  'call': [('Customer', '10:47 PM', 'I&rsquo;m moving out of a studio and need to store my stuff for a bit. What size would I need?'),
           ('Saleringo', '+12 s', 'A studio usually fits in a 5x5 unit, which is <b>$79 a month</b>. If you&rsquo;re storing a fridge and a '
                                  'washer too, I&rsquo;d suggest a 5x10 at <b>$129</b>. Right now I have <b>two 5x5s and one 5x10</b> open.'),
           ('Customer', '10:48 PM', 'I do have a fridge. Let&rsquo;s do the 5x10. When could I start?'),
           ('Saleringo', '+7 s', 'As soon as the rental agreement is signed, and your gate code and access card are issued on site. '
                                 'Can I get your name and a mobile number so I can hold the unit for you?'),
           ('Customer', '10:49 PM', 'Sophie Adams, 555-0746. This Saturday, for about two months.'),
           ('Saleringo', '+6 s', 'Thank you, Sophie. I&rsquo;ve held the 5x10 for you until tomorrow and I&rsquo;m texting the e-sign link now. '
                                 'Saturday, about two months &mdash; noted. The size is a guide from our chart, so if it doesn&rsquo;t all fit on the day you can switch units.')],
  'refuse': [('It never decides what may be stored.',
              'A motorcycle battery or a camping propane tank is a question for the manager under the site rules. The AI passes it on rather than guessing.'),
             ('It never lets a unit that is not free.',
              'It holds only what the live inventory shows open.'),
             ('It never guarantees everything will fit.',
              'It advises a size from the chart. Whether the fridge goes in is known on the day.'),
             ('It never stretches the insurance or liability terms.',
              'What is covered and for how much is stated as the agreement has it, no wider.')],
  'fields': ['What is being stored and how much', 'Start date and expected term', 'Size and price advised',
             'Unit held or not', 'Access instructions given', 'Agreement sent'],
  'stages': ['Inquiry', 'Size advised', 'Unit held', 'Agreement signed', 'Move-in and use'],
  'when': {'eyebrow': 'Thursday 10:47 PM, the call', 'h2': 'How it goes<br>at a site with nobody on it.', 'tt': 'studio contents, two months', 'badge': 'unstaffed'},
  'lead': 'The storage call comes at 10:47 PM to an empty site. It sizes the unit off your chart, quotes $129, holds the 5x10 until tomorrow, and leaves the propane question to the manager.',
  'room': 'vehicle-plant-storage',
  'room_d': 'The 10:47 PM studio-move call sized from your chart, the 5x10 held at $129 a month with the e-sign link sent &mdash; and the battery-and-propane question left to the manager.',
  'room_no': ('0', 'prohibited-items rulings made without the manager'),
 },
 'equipment-rental': {
  'name': 'Equipment rental', 'owner': 'the owner',
  'kicker': 'Equipment rental &middot; plant hire &middot; tools',
  'h1': 'The site starts moving<br>at seven in the morning.',
  'sub': 'Tomorrow&rsquo;s machine is looked for tonight. Whoever answers at that hour gets the job.',
  'cost': 'A foreman sorting out tomorrow&rsquo;s work in the evening discovers the machine he needs is not on site. Miss that call '
          'and another yard&rsquo;s forklift is unloaded there at seven. A hire account, once opened, runs until the project ends '
          '&mdash; so the evening call that rang out may have been months of hire.',
  'call': [('Customer', '8:19 PM', 'Can I get a 3-ton forklift for tomorrow morning, just for the day?'),
           ('Saleringo', '+9 s', 'Yes &mdash; I have one 3-ton forklift free tomorrow. The daily rate is <b>$280</b>, and delivery is charged '
                                 'separately by distance. With an operator it&rsquo;s <b>$520</b>. Where&rsquo;s the site?'),
           ('Customer', '8:20 PM', 'It&rsquo;s the Riverside job on Mill Road, and I&rsquo;ll need the operator. Marcus Hill, I&rsquo;m the site '
                                   'foreman &mdash; 555-0817.'),
           ('Saleringo', '+8 s', 'Riverside on Mill Road, with an operator &mdash; noted. Delivery gets confirmed from the address by the hire desk '
                                 'first thing in the morning. The forklift is the only one, so I&rsquo;ve reserved it for you now. What time do you need it on site?'),
           ('Customer', '8:21 PM', 'Seven, and I&rsquo;m the site contact.'),
           ('Saleringo', '+6 s', 'Seven tomorrow morning, site contact Marcus Hill &mdash; all noted. I&rsquo;m texting a confirmation, and the hire '
                                 'desk will call you about delivery in the morning.')],
  'refuse': [('It never reserves a machine that is not in stock.',
              'It books only what the inventory shows free. A machine that is not there at seven stops the whole site.'),
             ('It never guesses the delivery charge.',
              'Delivery depends on distance, so it takes the address and the hire desk confirms the figure in the morning.'),
             ('It never explains how to operate a machine or what it can safely lift.',
              'A 3-ton forklift and a pallet that is &ldquo;only slightly over&rdquo; is a safety judgement for the operator and the hire desk. '
              'Controls and safety rules are explained at handover by a person.'),
             ('It never says a licence is not needed.',
              'Equipment that requires a ticket is described as requiring one, plainly.')],
  'fields': ['Equipment type and specification', 'Hire period and delivery time', 'Site address and site contact',
             'Operator included or not', 'Rate and delivery charge quoted', 'Stock reserved'],
  'stages': ['Inquiry', 'Stock check', 'Reservation confirmed', 'Delivery and use', 'Return and invoice'],
  'when': {'eyebrow': 'Monday 8:19 PM, the call', 'h2': 'How it goes<br>after the depot has locked the gate.', 'tt': 'forklift for 7 AM', 'badge': 'depot closed'},
  'lead': 'The forklift call comes at 8:19 PM after the depot closes. It checks stock, quotes $280 or $520 with an operator, reserves the machine, and leaves the load-limit question to the hire desk.',
  'room': 'vehicle-plant-storage',
  'room_d': 'The 8:19 PM forklift call checked against live stock, quoted at $520 with an operator and reserved for 7:00 AM &mdash; the load-limit question handed to the hire desk, not answered.',
  'room_no': ('0', 'load limits or delivery charges guessed at'),
 },
}
