# -*- coding: utf-8 -*-
"""English page data for 13 original trades — used by p_trades/p_packs to generate en/industries/<slug>.html and -pack.html."""
EN2 = {
  'academies': {
  'name': 'Academies & tutoring', 'owner': 'the owner',
  'kicker': 'Academies &middot; tutoring &middot; test prep',
  'h1': 'Parents call<br>after the children are asleep.',
  'sub': 'Half past ten on a Monday night: the academy is dark and the owner went home hours ago. '
         'That is the only hour a working parent has free to call.',
  'cost': 'Academy inquiries bunch up before term starts, right after exams and just before the holidays. '
          'A call missed in those few weeks is a whole term of tuition &mdash; $340 a month, three sessions a week &mdash; '
          'and the student who enrols across the road does not come back that term. Yet most of those calls are '
          '&ldquo;when is the placement test&rdquo;, a question that never needed a person.',
  'call': [('Parent', '10:34 PM', 'My son&rsquo;s in eighth grade. How are your math classes set up, and when&rsquo;s the placement test?'),
           ('Saleringo', '+24 s', 'Middle school has a school-track class and an advanced class, and placement is decided by the test. '
                                  'Tests run <b>weekdays at 4:00 PM</b> and <b>Saturdays at 10:00 AM</b> and take thirty minutes. This Saturday still has room.'),
           ('Parent', '10:36 PM', 'Saturday at ten, please. And what&rsquo;s the tuition?'),
           ('Saleringo', '+11 s', 'Middle school math, three sessions a week, is <b>$340 a month</b>. Books are extra and quoted each term. '
                                  'For the booking, may I have your name, a number, and the student&rsquo;s name?'),
           ('Parent', '10:37 PM', 'Mirae Yoon, 555-0742. My son is Jiho. Could the director call me tomorrow, after six?'),
           ('Saleringo', '+9 s', 'Thank you, Mirae. Jiho is booked for the placement test <b>Saturday at 10:00 AM</b> &mdash; I&rsquo;m texting the confirmation now. '
                                 'The director will call you tomorrow after six.')],
  'refuse': [('It never judges a child&rsquo;s level over the phone.',
              'A parent who says &ldquo;he gets nineties&rdquo; hears no verdict on the advanced class. Placement is the director&rsquo;s call '
              'from the test result, so the AI books the test and stops there.'),
             ('It never promises a grade will rise.',
              'No &ldquo;two grades in one term&rdquo;. A result cannot be guaranteed, and advertising one breaks the rules an academy answers to.'),
             ('It never adjusts the tuition.',
              'It quotes the published fee &mdash; $340 a month, books extra &mdash; and the only discounts it mentions are the ones the owner has entered.'),
             ('It never talks about other students.',
              'Who is in a class, how many there are, and how they are doing is nobody else&rsquo;s business, and the AI does not answer it.')],
  'fields': ['Student&rsquo;s grade and subject', 'Class asked about and preferred days', 'Placement test slot',
             'Tuition quoted', 'Siblings who might enrol', 'When the parent can take a call'],
  'stages': ['Inquiry', 'Placement test booked', 'Test and consultation', 'Class placement', 'Enrolled'],
  'when': {'eyebrow': 'Monday 10:34 PM, the call', 'h2': 'How it goes<br>hours after the last class let out.', 'tt': 'after the last class', 'badge': 'after hours'},
  'lead': 'The parent calls at half past ten, once the child is asleep. It explains the classes and the test times, quotes the published tuition, '
          'books Saturday at ten &mdash; and leaves the advanced-class question to the director.',
  'room': 'booked-by-appointment',
  'room_d': 'The Monday 10:34 PM parent with an eighth-grader: test times and tuition from your own sheet, a placement test held for Saturday at ten '
            '&mdash; and no word on whether he makes the advanced class.',
  'room_no': ('0', 'children placed in a class before they have sat the test'),
  },
  'salons': {
  'name': 'Hair & beauty salons', 'owner': 'the owner',
  'kicker': 'Hair salons &middot; barbers &middot; nails',
  'h1': 'The phone rings<br>when your hands are wet.',
  'sub': 'Nobody answers mid-colour. Yet that is exactly when booking calls come, and the busier the Saturday, the more of them are lost.',
  'cost': 'Most booking calls are one sentence long: &ldquo;can you do Saturday afternoon?&rdquo; It takes thirty seconds to answer, and on a Saturday '
          'with a perm and a colour running at once those thirty seconds do not exist. The customer does not wait. She books somewhere else online '
          'or pushes it to next week, and a customer who does that twice never becomes a regular.',
  'call': [('Customer', '2:12 PM', 'Can I get a root touch-up and a treatment together on Saturday? How long does that take?'),
           ('Saleringo', '+19 s', 'Together, allow about <b>two hours</b>. A root touch-up is <b>$75</b>, and the treatment starts at <b>$85</b> depending on your hair. '
                                  'On Saturday I have <b>1:00 PM</b> or <b>4:30 PM</b> &mdash; which works better?'),
           ('Customer', '2:13 PM', 'One o&rsquo;clock, please. It&rsquo;s my first time there &mdash; any stylist is fine.'),
           ('Saleringo', '+7 s', 'Saturday at 1:00 PM it is, with the full two hours held and the stylist left open for the salon to assign. Whose name should I put it under, and which mobile number?'),
           ('Customer', '2:14 PM', 'Yejin Kang, 555-0318.'),
           ('Saleringo', '+6 s', 'Thank you, Yejin. You&rsquo;re booked for Saturday at one. I&rsquo;ll text a reminder on Friday, with directions since it&rsquo;s your first visit.')],
  'refuse': [('It never diagnoses hair.',
              'Whether bleached hair can take colour, or how damaged it is, cannot be judged from a message or a photo. '
              'The bleach history goes to the owner and the verdict waits for the chair.'),
             ('It never assigns a stylist on its own.',
              'A requested stylist is booked as requested. With no request, the slot is left open and the salon decides.'),
             ('It never shortens the service time to fit.',
              'Under-quoting the time is the most common reason a salon runs late. It quotes the generous figure and blocks exactly that in the calendar.'),
             ('It never invents a service that is not on the menu.',
              'Ask for something the menu does not list and it says the salon will check and get back to you, and leaves the note.')],
  'fields': ['Services requested and time allowed', 'Requested stylist, or none', 'Slot and chair',
             'Quote from the service menu', 'First visit or returning', 'Friday reminder with directions'],
  'stages': ['Inquiry received', 'Booked', 'Day-before reminder', 'In the chair', 'Rebooked'],
  'when': {'eyebrow': 'Wednesday 2:12 PM, the call', 'h2': 'How it goes<br>while the owner is mid-perm.', 'tt': 'mid-perm, hands full', 'badge': 'hands busy'},
  'lead': 'The owner is mid-perm and cannot take her hands off. It quotes the roots and the treatment from your menu, holds two hours on Saturday, '
          'and leaves the bleached-hair question to someone who can see the hair.',
  'room': 'booked-by-appointment',
  'room_d': 'The Wednesday 2:12 PM call while the owner is mid-perm: roots and treatment quoted from your menu, two hours held for Saturday at one '
            '&mdash; and no ruling on whether bleached hair can take colour.',
  'room_no': ('0', 'hair diagnosed from a photo before it reaches the chair'),
  },
  'fitness': {
  'name': 'Gyms & fitness', 'owner': 'the owner',
  'kicker': 'Gyms &middot; personal training &middot; pilates',
  'h1': 'People sign up<br>the night they decide.',
  'sub': 'The call comes from someone who just thought &ldquo;I start tomorrow&rdquo; and searched. Miss it, and the resolve cools with the phone.',
  'cost': 'A gym inquiry is close to an impulse. Someone decides at night, checks the price on the spot, and joins wherever answers. '
          'Give it a day and the decision is gone. The heaviest hour for inquiries is six to nine in the evening &mdash; exactly when every class '
          'is running and the desk has closed at nine.',
  'call': [('Customer', '9:52 PM', 'What&rsquo;s the minimum for personal training? And how much is gym-only?'),
           ('Saleringo', '+20 s', 'Personal training starts at <b>ten sessions for $650</b>, and the price per session drops at twenty and thirty. '
                                  'Gym-only is <b>$210 for three months</b>. If you&rsquo;re new, you get one free trial, and there&rsquo;s space tomorrow evening.'),
           ('Customer', '9:54 PM', 'I&rsquo;m new. Could I come around eight tomorrow?'),
           ('Saleringo', '+8 s', '<b>8:00 PM tomorrow</b> is open. Can I have your name and a mobile number for the trial?'),
           ('Customer', '9:55 PM', 'Doyun Han, 555-0584.'),
           ('Saleringo', '+7 s', 'Thank you, Doyun. Your free trial is booked for tomorrow at eight. Just bring workout clothes and indoor shoes &mdash; '
                                 'lockers and towels are provided. I&rsquo;m texting a confirmation and our health screening form now.')],
  'refuse': [('It never prescribes exercise.',
              'Which exercises to do, or how to lose ten pounds, is not a question it answers. That is what the trainer at the trial is for.'),
             ('It never judges a health condition.',
              'A herniated disc, a bad knee, a heart condition &mdash; whether training is safe is the trainer&rsquo;s judgement, so the question '
              'goes to the trainer running the trial before the caller comes in.'),
             ('It never haggles a membership.',
              'It quotes the registered prices and the promotions the owner has entered, and does not bargain.'),
             ('It never restates the refund terms.',
              'Cooling-off rights and the club&rsquo;s own terms are read as written, not softened to close a sale.')],
  'fields': ['What was asked about (gym, PT, classes)', 'When they want to start', 'Trial slot',
             'Prices and session counts quoted', 'Existing member or new', 'Best time to call back'],
  'stages': ['Inquiry', 'Trial booked', 'Trial and consultation', 'Signed up', 'Renewal'],
  'when': {'eyebrow': 'Thursday 9:52 PM, the call', 'h2': 'How it goes<br>after the desk has closed for the night.', 'tt': 'desk closed at nine', 'badge': 'desk dark'},
  'lead': 'The desk closed at nine and the call comes at 9:52. It quotes PT and gym-only from your sheet, books a free trial for tomorrow at eight, '
          'and sends the disc-injury question to the trainer.',
  'room': 'booked-by-appointment',
  'room_d': 'The Thursday 9:52 PM caller who decided tonight: PT and gym-only quoted from your sheet, a free trial held for tomorrow at eight '
            '&mdash; and no opinion on training with a herniated disc.',
  'room_no': ('0', 'injuries cleared for training over the phone'),
  },
  'golf': {
  'name': 'Golf clubs', 'owner': 'the owner',
  'kicker': 'Golf clubs &middot; driving ranges &middot; simulators',
  'h1': 'Tee-time calls come<br>before the pro shop opens.',
  'sub': 'A weekend tee time goes to whichever club answers first. Miss the 6:12 AM call and that four-ball plays somewhere else on Sunday.',
  'cost': 'Several clubs get the same call for the same Sunday morning, and the one that says &ldquo;yes, seven forty&rdquo; first gets the group. '
          'A cancellation is filled by whoever reaches the waiting list first, and if nobody does, the slot simply goes out empty. '
          'At the range, membership and lesson calls pile up in the evening, when every pro is on the mat with a pupil.',
  'call': [('Customer', '6:12 AM', 'Can I get a four-ball on Sunday morning?'),
           ('Saleringo', '+19 s', 'Sunday morning has one slot left, <b>7:40 AM</b>. The weekend green fee is <b>$160 a player</b>, and carts and caddies are extra. '
                                  'Shall I hold 7:40 for you?'),
           ('Customer', '6:14 AM', 'Yes, please. We&rsquo;re not members. Michael Choi, 555-0427.'),
           ('Saleringo', '+7 s', 'That&rsquo;s the visitor rate I quoted, so you&rsquo;re set. Thank you, Michael &mdash; Sunday at 7:40, four players, and the '
                                 'confirmation is on its way by text. Would you like to hear if an earlier time opens up?'),
           ('Customer', '6:15 AM', 'Anything before seven would be great.'),
           ('Saleringo', '+6 s', 'You&rsquo;re on the waiting list for anything before <b>7:00</b>. If a cancellation comes up I&rsquo;ll text you first, and your 7:40 stays as it is.')],
  'refuse': [('It never invents a tee time.',
              'It books only the slots the tee sheet shows open. A full sheet gets the waiting list, not a squeezed-in group.'),
             ('It never adjusts the green fee.',
              'Weekday, weekend, member, visitor &mdash; it quotes the rate registered for that day and hour and nothing else.'),
             ('It never confirms a rain cancellation in advance.',
              'Whether Sunday is called off is decided on the day, by the club, from the course. It reads the policy as written and passes the question to the pro shop.'),
             ('It never discloses another group&rsquo;s booking.',
              'Who is on the tee at seven forty is not something a caller is told.')],
  'fields': ['Date and tee time wanted', 'Players and lead name', 'Member or visitor',
             'Green fee quoted and extras', 'Waiting-list request', 'Confirmation text to the lead player'],
  'stages': ['Inquiry', 'Tee time held', 'Confirmed and paid', 'Round played', 'Rebooked or waitlisted'],
  'when': {'eyebrow': 'Thursday 6:12 AM, the call', 'h2': 'How it goes<br>before the first tee, with the pro shop still dark.', 'tt': 'before the first tee', 'badge': 'pro shop closed'},
  'lead': 'The call comes at 6:12, before the pro shop opens. It holds the last Sunday slot, quotes the weekend green fee from your sheet, '
          'puts the group on the waiting list &mdash; and leaves the rain question to the club.',
  'room': 'booked-by-appointment',
  'room_d': 'The Thursday 6:12 AM four-ball before the pro shop opens: the last Sunday slot held, the green fee quoted from your sheet, the group waitlisted '
            '&mdash; and no promise about canceling if it rains.',
  'room_no': ('0', 'rain cancellations promised before the morning arrives'),
  },
  'restaurants': {
  'name': 'Restaurants', 'owner': 'the owner',
  'kicker': 'Restaurants &middot; group bookings &middot; catering',
  'h1': 'Nobody answers a party of twenty<br>during the lunch rush.',
  'sub': 'The delivery apps run themselves. The problem is the floor phone: a twenty-person company dinner rings at 12:38 PM.',
  'cost': 'Most calls to a restaurant are group bookings. One call is twenty covers, and twenty covers at $45 a head is half of that Friday&rsquo;s takings. '
          'It rings at the lunch peak, when neither the kitchen nor the floor has a free hand. The dinner goes next door, and next time the company '
          'calls next door first. Because groups come back, the cost of one missed call is never one call.',
  'call': [('Customer', '12:38 PM', 'Can you take twenty people on Friday evening? Do you have a private room?'),
           ('Saleringo', '+18 s', 'Friday evening I have <b>6:00</b> or <b>8:00 PM</b> left, and for twenty the upstairs private room is the right fit. '
                                  'Groups are on the set menu at <b>$45 a head</b>, drinks separate. Which time would you like?'),
           ('Customer', '12:40 PM', 'Six, please. One of our guests is vegetarian.'),
           ('Saleringo', '+8 s', 'Friday at six, twenty guests, upstairs room &mdash; booking that now. I&rsquo;ll pass the vegetarian guest on to the owner '
                                 'exactly as you said it. Could you give me your name and a mobile number?'),
           ('Customer', '12:41 PM', 'Rachel Moore, 555-0925. It&rsquo;s a company dinner &mdash; Brightwater Consulting.'),
           ('Saleringo', '+7 s', 'Brightwater Consulting, Rachel Moore &mdash; noted. You&rsquo;re booked for Friday at six, the confirmation is going out by text, '
                                 'and I&rsquo;ll send one more on Thursday afternoon.')],
  'refuse': [('It never answers for the kitchen on allergens or origin.',
              'Whether the set menu has shrimp in it, or nuts, is for the kitchen to confirm. The question is written down word for word and the owner answers it.'),
             ('It never creates a table that is not there.',
              'It books from the registered tables and rooms only. A double-booked room means turning twenty people away at the door.'),
             ('It never promises a menu change.',
              'Swapping a course or an ingredient is the owner&rsquo;s decision. The request is logged, not granted.'),
             ('It never makes up a discount.',
              'The only group rates it mentions are the ones on the function sheet.')],
  'fields': ['Party size, date and time', 'Room or main floor', 'Set menu and price per head',
             'Dietary requests, word for word', 'Name, company and mobile', 'Confirmation and Thursday reminder'],
  'stages': ['Inquiry', 'Booked', 'Day-before check', 'Seated', 'Next booking'],
  'when': {'eyebrow': 'Wednesday 12:38 PM, the call', 'h2': 'How it goes<br>while the floor and the kitchen are slammed.', 'tt': 'lunch rush', 'badge': 'no free hands'},
  'lead': 'The party of twenty rings at the lunch peak. It offers the two Friday slots, quotes the set menu from your function sheet, books the upstairs room, '
          'and hands the shellfish question to the kitchen.',
  'room': 'places-hospitality',
  'room_d': 'The Wednesday 12:38 PM party of twenty in the lunch rush: the upstairs room booked for Friday at six, the set menu quoted from your function sheet '
            '&mdash; and the shellfish question left for the kitchen.',
  'room_no': ('0', 'allergens answered without asking the kitchen'),
  },
  'venues': {
  'name': 'Wedding & event venues', 'owner': 'the venue manager',
  'kicker': 'Wedding venues &middot; event halls &middot; banquets',
  'h1': 'The first question is always<br>whether the date is free.',
  'sub': 'Every inquiry opens the same way: &ldquo;is May seventeenth next year open?&rdquo; Take a day to answer and the wedding is held in another hall.',
  'cost': 'Couples ask three or four venues about the same Saturday at once, and go to see the one that said &ldquo;yes&rdquo; first. '
          'The inquiries arrive on weekend evenings, when a reception is under way in the hall and the office is empty. '
          'A web form answered on Monday morning is already too late.',
  'call': [('Customer', '9:41 PM', 'Is Saturday, May 17th next year open for a wedding in the afternoon? About two hundred guests.'),
           ('Saleringo', '+25 s', 'It is. May 17th still has two afternoon slots, <b>1:00 PM</b> and <b>4:00 PM</b>. For two hundred guests the Grand Hall is the right fit, '
                                  'and catering starts at <b>$65 a head</b>. The minimum guest count and the room fee depend on the slot, so the team will walk you '
                                  'through the exact numbers at a consultation.'),
           ('Customer', '9:43 PM', 'Could we come in on a weekend?'),
           ('Saleringo', '+8 s', '<b>This Sunday at 11:00 AM</b> is open. Both of you can come, and you&rsquo;ll see the hall as well. Shall I book that?'),
           ('Customer', '9:44 PM', 'Yes, please. It&rsquo;s Emma Park, 555-0284.'),
           ('Saleringo', '+7 s', 'Thank you, Emma. You&rsquo;re booked for Sunday at eleven, and the confirmation and directions are going out by text now. '
                                 'Before Sunday the team will check the status of both May 17th slots so you have the latest picture.')],
  'refuse': [('It never holds a date.',
              'It confirms availability and books the consultation. A date is held only by a signed contract, so &ldquo;could you keep the four o&rsquo;clock '
              'under our name&rdquo; goes to the venue manager.'),
             ('It never fixes a quote.',
              'It gives the starting figures for catering and the room. The minimum guest count and the options are settled at the consultation.'),
             ('It never promises a discount.',
              'The only promotions it mentions are the ones registered. It does not invent terms.'),
             ('It never discusses other bookings.',
              'Who has booked the day, or how many couples have toured, is not disclosed.')],
  'fields': ['Date and time of day wanted', 'Expected guest count', 'Event type (wedding, birthday, corporate)',
             'Hall and catering rate quoted', 'Consultation slot', 'Best time to reach the couple'],
  'stages': ['Inquiry', 'Consultation booked', 'Consultation and hall tour', 'Quote finalised', 'Contract signed'],
  'when': {'eyebrow': 'Saturday 9:41 PM, the call', 'h2': 'How it goes<br>while a reception fills the hall.', 'tt': 'reception in progress', 'badge': 'office empty'},
  'lead': 'The call comes at 9:41 on a Saturday, with a reception in the hall and nobody in the office. It gives the two open May slots, quotes catering from your sheet, '
          'books Sunday&rsquo;s tour &mdash; and never holds a date without a contract.',
  'room': 'places-hospitality',
  'room_d': 'The Saturday 9:41 PM couple asking about May 17th: both open slots named, catering quoted from your sheet, a Sunday tour booked '
            '&mdash; and no date held before a contract is signed.',
  'room_no': ('0', 'dates held on a phone call'),
  },
  'stays': {
  'name': 'Boutique stays', 'owner': 'the owner',
  'kicker': 'Guesthouses &middot; cabins &middot; boutique stays',
  'h1': 'Every booking through the app<br>costs you ten to twenty percent.',
  'sub': 'A guest who calls you directly is a guest with no commission attached. Miss the call and the same guest books the same cabin through the app.',
  'cost': 'The maths on a missed call is simple. A direct booking pays no commission; the platform takes ten to twenty percent. Same guest, same cabin, '
          'and one unanswered phone changes what lands in the account. Weekend plans get made on weeknights, and at 10:22 PM the owner is either '
          'still cleaning the cabins or already asleep.',
  'call': [('Customer', '10:22 PM', 'Is the four-person cabin free this Saturday? And can we barbecue?'),
           ('Saleringo', '+21 s', 'Cabin C is the last one open on Saturday. It&rsquo;s <b>$220</b> for four at the weekend rate. The barbecue is <b>$10 a person</b> '
                                  'and includes charcoal and the grill &mdash; you bring the food. Booking direct is <b>$20 less</b> than the app.'),
           ('Customer', '10:24 PM', 'Then I&rsquo;ll book direct. Can we bring our dog?'),
           ('Saleringo', '+9 s', 'Cabin C is dog-friendly, with a <b>$20</b> pet fee. I&rsquo;ll hold Cabin C for Saturday &mdash; what name and mobile number should it go under?'),
           ('Customer', '10:25 PM', 'Daniel Lee, 555-0361. What time is check-in?'),
           ('Saleringo', '+7 s', 'Thank you, Daniel. Check-in is <b>3:00 PM</b>, check-out is eleven, and the charcoal will be ready at six. Cabin C is held for Saturday, '
                                 'four guests, barbecue and one dog; the payment details are on their way by text, and the booking is confirmed once the deposit lands.')],
  'refuse': [('It never sells a cabin that is not free.',
              'It books only from the live availability board. A double booking means a guest turned away at the door.'),
             ('It never bends the refund policy.',
              'It reads the cancellation terms as written. A weather exception &mdash; &ldquo;full refund if it rains&rdquo; &mdash; is the owner&rsquo;s decision, '
              'and the question goes to the owner.'),
             ('It never invents what is nearby.',
              'Asked what is around the cabins, it says only what the owner has confirmed.'),
             ('It never chases the deposit.',
              'It sends the payment details and waits. It does not take a payment itself.')],
  'fields': ['Dates and number of nights', 'Guests and cabin', 'Pets',
             'Extras (barbecue, breakfast)', 'Rate quoted and the direct-booking saving', 'Payment request sent'],
  'stages': ['Inquiry', 'Cabin held', 'Deposit received', 'Stayed', 'Return visit'],
  'when': {'eyebrow': 'Wednesday 10:22 PM, the call', 'h2': 'How it goes<br>while the owner sleeps after turnover.', 'tt': 'after the last turnover', 'badge': 'owner asleep'},
  'lead': 'The owner finished the turnover and went to bed; the call comes at 10:22. It offers the last cabin, quotes the weekend rate and the extras from your sheet, '
          'books it direct &mdash; and leaves the rain refund to the owner.',
  'room': 'places-hospitality',
  'room_d': 'The Wednesday 10:22 PM guest while the owner sleeps: the last cabin held at your weekend rate, barbecue and one dog added, paid direct '
            '&mdash; and no exception to the refund policy promised for rain.',
  'room_no': ('0', 'refund exceptions granted at night for a forecast'),
  },
  'universities': {
  'name': 'Universities', 'owner': 'the admissions officer',
  'kicker': 'Universities &middot; admissions &middot; continuing education',
  'h1': 'In application season<br>the phone rings ten times as much.',
  'sub': 'The same question comes in hundreds of times a day. Answering it with people is a waste; failing to answer it is a loss.',
  'cost': 'In transfer and admission season the office takes ten times the usual calls, and most of them ask for the document list and the deadline '
          'that are already in the prospectus. The problem is the real consultations mixed in with them. An applicant whose eligibility is unclear '
          'needs an officer, and the line is engaged.',
  'call': [('Applicant', '8:56 PM', 'I want to apply as a transfer student. What documents do I need, and when&rsquo;s the deadline?'),
           ('Saleringo', '+20 s', 'For a general transfer the basics are your <b>transcript</b>, <b>proof of graduation</b> or expected graduation, and a '
                                  '<b>personal statement</b>, with extra documents for some departments. The deadline is <b>November 14th at 5:00 PM</b>, online only, '
                                  'and the application fee is <b>$60</b>. Which department are you applying to?'),
           ('Applicant', '8:58 PM', 'Computer Science. I graduated from a community college &mdash; am I eligible?'),
           ('Saleringo', '+10 s', 'Computer Science needs just the three basics. Eligibility, though, depends on credit recognition, and an admissions officer '
                                  'decides that from your transcript &mdash; so I can&rsquo;t tell you yes or no. Shall I have an officer call you tomorrow morning?'),
           ('Applicant', '8:59 PM', 'Yes, please. Jihoon Oh, 555-0187. After ten is best.'),
           ('Saleringo', '+8 s', 'Thank you, Jihoon. An officer will call you after ten tomorrow. I&rsquo;m texting the document list and the deadline now, '
                                 'and having your transcript ready will speed up the check.')],
  'refuse': [('It never rates the chances of admission.',
              'A GPA of 3.2 gets no &ldquo;you should be fine&rdquo;. Admission is decided by the review, and the AI says so.'),
             ('It never rules on eligibility.',
              'Credit recognition and entry requirements are judged by an officer from the documents. The AI books the officer&rsquo;s call.'),
             ('It never adds to the prospectus.',
              'It says what is published and makes no exceptions.'),
             ('It never talks about other applicants.',
              'Live application numbers and who has applied are not answered.')],
  'fields': ['Programme and department', 'Education and eligibility notes', 'Inquiry text as spoken',
             'Officer needed or answered from the prospectus', 'Best time for the callback', 'Deadline quoted'],
  'stages': ['Inquiry', 'Answered from the prospectus', 'Passed to an officer', 'Officer consultation', 'Application filed'],
  'when': {'eyebrow': 'Tuesday 8:56 PM, the call', 'h2': 'How it goes<br>after admissions has gone home.', 'tt': 'admissions gone home', 'badge': 'office dark'},
  'lead': 'Admissions went home hours before the 8:56 PM call. It reads the document list and the deadline from the prospectus, books an officer&rsquo;s callback '
          'for after ten &mdash; and gives no verdict on eligibility or chances.',
  'room': 'professional-public',
  'room_d': 'The Tuesday 8:56 PM transfer applicant: documents and the November deadline read from your prospectus, an officer&rsquo;s callback booked for after ten '
            '&mdash; and no verdict on eligibility or on chances.',
  'room_no': ('0', 'admission chances rated over the phone'),
  },
  'legal': {
  'name': 'Law firms', 'owner': 'the attorney',
  'kicker': 'Law firms &middot; attorneys &middot; paralegals',
  'h1': 'The calls come in,<br>and court is where you are.',
  'sub': 'The hours an attorney spends in a hearing are the hours new matters call. And in this trade, a wrong answer on the phone is a professional-conduct problem.',
  'cost': 'A legal inquiry is urgent. The caller has just been served or has a demand letter in hand, and if nobody answers they do not call back &mdash; '
          'they call the next firm. Most of an attorney&rsquo;s day is in court or in consultations, and a receptionist cannot judge a matter. '
          'What the firm needs is a front desk that takes the facts down exactly and books the consultation.',
  'call': [('Client', '7:41 PM', 'I&rsquo;ve received a formal demand letter. Can I get a consultation, and what does it cost?'),
           ('Saleringo', '+23 s', 'You can. An initial consultation is <b>$150 for thirty minutes</b>, and if you retain the firm that amount comes off the fee. '
                                  'Demand letters often carry a response deadline, so please note the date you received it. <b>Tomorrow at 4:00 PM</b> is open.'),
           ('Client', '7:43 PM', 'Four tomorrow works. James Jung, 555-0515. The other side is a company I used to do business with.'),
           ('Saleringo', '+9 s', 'Thank you, James. You&rsquo;re booked for tomorrow at four and the confirmation is on its way. Please bring the original letter, '
                                 'and any contract or messages between you and that company &mdash; it makes the consultation much faster.'),
           ('Client', '7:44 PM', 'It&rsquo;s been a few days already. How long do I have to respond?'),
           ('Saleringo', '+8 s', 'That&rsquo;s not something I can determine for you. Note the date you received it, and the attorney will tell you exactly where you stand tomorrow at four.')],
  'refuse': [('It never gives the outlook of a case.',
              '&ldquo;Is this a case I can win&rdquo; is legal judgement, and only the attorney gives it, after reading the documents.'),
             ('It never gives legal advice.',
              'It does not tell a caller how to respond. It books the consultation and stops.'),
             ('It never fixes the retainer.',
              'It quotes the consultation fee only. The fee for the matter is set by the attorney once the matter is seen.'),
             ('It never calculates a deadline.',
              'How long the caller has to respond is not stated. It says to note the date the letter arrived and leaves the rest to the attorney.')],
  'fields': ['Matter type (civil, criminal, family, employment)', 'Opposing party', 'Documents with a deadline',
             'Consultation slot', 'Consultation fee quoted', 'Document checklist sent'],
  'stages': ['Inquiry', 'Consultation booked', 'Consultation', 'Retained or declined', 'Matter in progress'],
  'when': {'eyebrow': 'Monday 7:41 PM, the call', 'h2': 'How it goes<br>while the attorney prepares for tomorrow&rsquo;s hearing.', 'tt': 'preparing for court', 'badge': 'hearing tomorrow'},
  'lead': 'The demand letter rings at 7:41 while the attorney is preparing for court. It quotes the consultation fee from your schedule, books four o&rsquo;clock tomorrow, '
          'lists what to bring &mdash; and gives no opinion on whether the case can be won.',
  'room': 'professional-public',
  'room_d': 'The Monday 7:41 PM demand letter while the attorney prepares for court: the consultation fee quoted from your schedule, four o&rsquo;clock tomorrow booked, '
            'the documents listed &mdash; and no word on whether the case can be won.',
  'room_no': ('0', 'case outlooks given before the attorney has read a page'),
  },
  'public-sector': {
  'name': 'Public sector', 'owner': 'the office manager',
  'kicker': 'District offices &middot; agencies &middot; public services',
  'h1': 'A resident calls<br>already annoyed.',
  'sub': 'They have been transferred twice and this is the third call. Send them the wrong way again and the inquiry becomes a complaint.',
  'cost': 'The cost of a missed call here is trust, not revenue. Two unanswered calls and the resident writes to the mayor or the ombudsman, and clearing '
          'that takes many times the original work. Yet most calls end the moment the right team is named. Sorting them &mdash; at lunch, at night &mdash; '
          'is all the AI is asked to do.',
  'call': [('Resident', '12:24 PM', 'I need to register a change of address. What do I bring? And can I do it for my mother, on her behalf?'),
           ('Saleringo', '+19 s', 'If she comes in herself, just her <b>photo ID</b>. If you come on her behalf, you&rsquo;ll need a <b>signed authorisation letter</b>, '
                                  'a <b>copy of her ID</b>, and your own ID. It can also be filed online through the government portal.'),
           ('Resident', '12:26 PM', 'If I file online, when does it get processed?'),
           ('Saleringo', '+8 s', 'That depends on what&rsquo;s in the application, so the residents&rsquo; team has to confirm it. They&rsquo;re back from lunch at <b>1:00 PM</b>. '
                                 'Shall I log a callback so they ring you?'),
           ('Resident', '12:27 PM', 'Yes, please. Mina Han, 555-0649. After one thirty would be better.'),
           ('Saleringo', '+7 s', 'Thank you, Mina. Your callback is logged with the residents&rsquo; team for after <b>1:30 PM</b>, and a reference number is on its way by text. '
                                 'They&rsquo;ll call in order.')],
  'refuse': [('It never predicts a ruling.',
              'Whether a permit is granted or an allowance is paid is decided by the responsible team after checking the requirements. '
              'The relocation-allowance question goes to the residents&rsquo; team.'),
             ('It never interprets the regulations.',
              'How a rule applies to a resident&rsquo;s case is the department&rsquo;s judgement, not the AI&rsquo;s.'),
             ('It never looks up personal records.',
              'Anything that requires identity verification is not done on a phone call.'),
             ('It never answers for another department.',
              'If it does not know, it says so and routes the call. Sending a resident the wrong way is worse than not answering.')],
  'fields': ['Inquiry type and responsible team', 'The question, word for word', 'In person or by proxy',
             'Documents listed', 'Transferred or callback logged', 'Preferred callback time'],
  'stages': ['Logged', 'Classified', 'Answered from guidance', 'Routed to the team', 'Outcome reported'],
  'when': {'eyebrow': 'Tuesday 12:24 PM, the call', 'h2': 'How it goes<br>while the counter is empty for lunch.', 'tt': 'lunch hour', 'badge': 'counter unattended'},
  'lead': 'The counter is empty for lunch when the 12:24 call comes. It lists the documents from your approved guidance, logs a callback with the residents&rsquo; team '
          'for after 1:30 &mdash; and never rules on who qualifies for an allowance.',
  'room': 'professional-public',
  'room_d': 'The Tuesday 12:24 PM address change during the lunch hour: documents listed from your approved guidance, a callback logged with the residents&rsquo; team '
            '&mdash; and no ruling on whether the mother qualifies for the allowance.',
  'room_no': ('0', 'eligibility rulings handed out at the switchboard'),
  },
  'funeral-homes': {
  'name': 'Funeral homes', 'owner': 'the director',
  'kicker': 'Funeral homes &middot; funeral directors &middot; pre-need',
  'h1': 'This is the one call<br>that must never wait.',
  'sub': 'The caller lost a parent minutes ago. They are standing in a hospital corridor at 3:12 AM, not knowing what to ask.',
  'cost': 'A funeral call comes at three in the morning, and the person calling is in an emergency department. If it rings three times and stops, '
          'the family dials the next number. The point of answering here is not to sell: it is to say the one thing to do now and to hand over to a person '
          'as fast as possible. This is a trade where a machine must never run the conversation.',
  'call': [('Family', '3:12 AM', 'My father just passed away&hellip; I don&rsquo;t know what to do.'),
           ('Saleringo', '+4 s', 'I&rsquo;m so sorry for your loss. I&rsquo;m going to put you through to our director right now. While I connect you, could you tell me '
                                 'just the name of the hospital you&rsquo;re at? That lets us start arranging the transfer.'),
           ('Family', '3:13 AM', 'Hansol University Hospital, the emergency department. I&rsquo;m his son, Thomas Yoon &mdash; 555-0718.'),
           ('Saleringo', '+3 s', 'Thank you, Thomas. Hansol University Hospital, emergency department &mdash; noted. I&rsquo;m connecting you to <b>Sungho Kim</b>, our director on call. '
                                 'If the line drops, he will ring you back on this number within <b>three minutes</b>. Until then, stay with your father.')],
  'refuse': [('It never suggests a product.',
              'The size of the visitation room and the form of the service are not proposed by a machine. That is decided by the family with the director, in the room.'),
             ('It never raises money first.',
              'No cost is mentioned in this call unless the family asks, and then only a range.'),
             ('It never explains the procedure at length.',
              'One thing to do now, then the connection. The explaining is the director&rsquo;s.'),
             ('It never delays the handover.',
              'In this trade, the less time the AI holds the line, the better. The director was on the call within two minutes.')],
  'fields': ['Caller and relationship to the deceased', 'Hospital or place', 'Transfer needed',
             'Director connected, and when', 'Time the call was logged', 'How the family will be contacted'],
  'stages': ['Call logged', 'Director connected', 'Transfer and room', 'Service', 'Aftercare'],
  'when': {'eyebrow': 'Sunday 3:12 AM, the call', 'h2': 'How it goes<br>while the director on call is out on a transfer.', 'tt': 'director on a transfer', 'badge': 'small hours'},
  'lead': 'At 3:12 AM the director on call is in the transfer vehicle. It takes the hospital name, connects the son to the director within two minutes '
          '&mdash; and suggests nothing about the room or the service.',
  'room': 'professional-public',
  'room_d': 'The Sunday 3:12 AM call from an emergency department: the hospital taken down, the son connected to the director on call within two minutes '
            '&mdash; and no room or service suggested by a machine.',
  'room_no': ('0', 'rooms or services recommended to a grieving family'),
  },
  'ecommerce': {
  'name': 'Online stores', 'owner': 'the owner',
  'kicker': 'Online stores &middot; brand shops &middot; D2C',
  'h1': 'Questions come at night.<br>Customer service answers by day.',
  'sub': 'Someone with a dress in the cart does not wait for an answer. Reply at ten the next morning and the cart is already empty.',
  'cost': 'Half of all questions arrive a click before checkout: will the small fit, will it arrive by Saturday, can I exchange it. Answered, they pay; '
          'unanswered, they close the tab. The questions cluster between ten and midnight, and the customer service reply goes out at ten the next morning. '
          'Those twelve hours are your abandonment rate.',
  'call': [('Customer', '11:31 PM', 'The linen shirt dress in beige &mdash; does a size small run roomy? I need it by the day after tomorrow. Is that possible?'),
           ('Saleringo', '+17 s', 'It&rsquo;s true to size, so if you usually wear a small, a small will fit. The shoulders run a little narrow, so with broader shoulders '
                                  'I&rsquo;d suggest a medium. Beige in small is in stock, and if you order tonight it <b>ships tomorrow</b>. The delivery date is set by '
                                  'the carrier, so I can&rsquo;t confirm it, but it usually arrives the day after shipping.'),
           ('Customer', '11:33 PM', 'My shoulders are average. Can I exchange it if it doesn&rsquo;t fit?'),
           ('Saleringo', '+7 s', 'Yes &mdash; within <b>seven days</b> of delivery. If it&rsquo;s a change of mind, return shipping both ways is <b>$8</b>, and the item needs to be unworn.'),
           ('Customer', '11:34 PM', 'Okay. If I order, can I get the tracking number by text? Sua Oh, 555-0863.'),
           ('Saleringo', '+6 s', 'Thank you, Sua &mdash; I&rsquo;ll text the tracking to this number the moment it ships. Place the order in the app or on the site, '
                                 'and I&rsquo;ll attach tonight&rsquo;s sizing notes so the team has them.')],
  'refuse': [('It never invents stock.',
              'It answers from the live inventory only. Selling what is not there means canceling the order the next morning.'),
             ('It never promises a delivery date.',
              'It commits to the ship date. Arrival is set by the carrier, so &ldquo;can you guarantee it by Saturday morning&rdquo; goes to the team.'),
             ('It never claims an effect or an ingredient.',
              'Cosmetics and supplements have labelling rules. It uses the registered product copy and nothing more.'),
             ('It never sweetens the return policy.',
              'Consumer law and the published terms are read as they stand.')],
  'fields': ['Product and option asked about', 'Question type (sizing, shipping, exchange, stock)', 'Order number',
             'Ship date quoted', 'Exchange or refund terms given', 'Converted to an order or not'],
  'stages': ['Inquiry', 'Answered on the spot', 'Ordered and paid', 'Shipped', 'Exchange or refund handled'],
  'when': {'eyebrow': 'Thursday 11:31 PM, the call', 'h2': 'How it goes<br>after customer service has gone home.', 'tt': 'CS gone home', 'badge': 'after six'},
  'lead': 'Customer service went home at six; the sizing question comes at 11:31. It answers from the live inventory and the published terms, names the ship date '
          '&mdash; and never guarantees the day the parcel arrives.',
  'room': 'online-multi-site',
  'room_d': 'The Thursday 11:31 PM shopper with a dress in the cart: sizing answered from your product notes, the ship date and the exchange terms from your published policy '
            '&mdash; and no delivery day guaranteed.',
  'room_no': ('0', 'delivery days guaranteed on behalf of the carrier'),
  },
  'franchise': {
  'name': 'Franchises', 'owner': 'head office',
  'kicker': 'Franchisors &middot; head office &middot; multi-site',
  'h1': 'Franchise leads and store complaints<br>ring the same number.',
  'sub': 'The head-office line takes candidates asking what a store costs and customers angry at a branch. Two entirely different calls, one person answering.',
  'cost': 'The main line carries two kinds of call. A franchise inquiry is a contract worth hundreds of thousands of dollars; a complaint, handled badly, '
          'can unsettle a whole franchisee. Opposite in nature, and they share one desk. The more stores you open, the more complaints come in, '
          'so the better you do, the more candidates you miss.',
  'call': [('Candidate', '9:07 PM', 'I&rsquo;m interested in a franchise. What does it cost in total to open one?'),
           ('Saleringo', '+24 s', 'Thank you for your interest. For a standard 350-square-foot store, the base figures are a <b>$30,000</b> franchise fee, <b>$9,000</b> for training, '
                                  'and fit-out at about <b>$75 a square foot</b>, with kitchen equipment and opening stock on top. The exact total depends on the site, '
                                  'so I&rsquo;ll send you the disclosure document and set up a consultation.'),
           ('Candidate', '9:09 PM', 'Yes, please send it. I&rsquo;m looking at Daejeon, with a budget of around $300,000.'),
           ('Saleringo', '+9 s', 'I&rsquo;ll assign you to the Daejeon regional manager. Can I get your name, a mobile number, and an email address for the disclosure document?'),
           ('Candidate', '9:10 PM', 'David Kang, 555-0917. I&rsquo;ll text you the email. After ten tomorrow is best for a call.'),
           ('Saleringo', '+7 s', 'Thank you, David. You&rsquo;re assigned to <b>Jihoon Seo</b>, our Daejeon manager. Once your email comes in the disclosure document goes out tonight, '
                                 'and Jihoon will call you tomorrow after ten.')],
  'refuse': [('It never states expected revenue.',
              'Franchise law bars a revenue projection without a basis. &ldquo;What would a store in Dunsan-dong make&rdquo; goes to the regional manager, '
              'who answers from the disclosure document.'),
             ('It never rates a location.',
              'Whether a neighbourhood will work is not answered. The site survey is done by a person.'),
             ('It never discounts the franchise terms.',
              'It quotes the published schedule and nothing off it.'),
             ('It never admits fault for a franchisee.',
              'A complaint is logged as facts and routed to the right department. No apology binds a store.')],
  'fields': ['Call type (franchise, complaint, other)', 'Region and budget', 'Disclosure document sent',
             'Store and date of the incident', 'Regional manager assigned', 'When the candidate wants the call'],
  'stages': ['Lead received', 'Sorted: lead or complaint', 'Manager assigned', 'Consultation or resolution', 'Signed or closed'],
  'when': {'eyebrow': 'Wednesday 9:07 PM, the call', 'h2': 'How it goes<br>after head office has closed for the day.', 'tt': 'head office closed', 'badge': 'main line after six'},
  'lead': 'Head office closed at six and the franchise inquiry comes at 9:07. It quotes the opening costs from your published schedule, sends the disclosure document, '
          'assigns the regional manager &mdash; and never projects revenue.',
  'room': 'online-multi-site',
  'room_d': 'The Wednesday 9:07 PM franchise candidate after head office closed: opening costs quoted from your published schedule, the disclosure document sent, '
            'a regional manager assigned &mdash; and no revenue projection.',
  'room_no': ('0', 'revenue projections given to a candidate'),
  },
}
