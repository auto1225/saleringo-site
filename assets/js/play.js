/* ═══════════════════════════════════════════════════════════════════
   SR_PLAY — the demo the visitor drives.
   ───────────────────────────────────────────────────────────────────
   Three specialists audited the homepage and converged on one thing:
   the site has 83 written proofs that a conversation becomes a booking,
   a quote, a customer record and a number — and no way to cause one.

   The design decision that matters here is whose seat the visitor sits
   in. Not the owner's. The *customer's*. A non-technical buyer's real
   fear is not "does it work", it is "what will it do to me in front of
   my customer" — so the interaction is: ask it something hard, and
   watch it refuse.

   On a trap branch two of the four artefact frames stay deliberately
   empty, struck through, with the reason written into the product
   surface instead of into a paragraph. Prose can claim a refusal.
   Only an interaction can be one.

   Every money figure below is grep-verified against a page that already
   publishes it. Nothing here is invented, and no business is named.
   ═══════════════════════════════════════════════════════════════════ */
window.SR_PLAY = {

  dental: {
    label: 'Dental',
    seed: 'Evening — this is the practice. What can I help with?',
    asks: [
      { id:'crown', chip:'“How much is a crown?”', risk:'normal',
        turns:[
          {who:'user', text:'I chipped a front tooth this afternoon. How much is a crown, and can anyone see me this week?'},
          {who:'ai',   text:'A crown runs $1,100 to $1,600 depending on the material, confirmed after an exam and X-ray. I have Thursday 10:30 or Friday 8:00. Which suits you?'},
          {who:'verify', text:'✓ From your fee schedule · 2 sources'},
          {who:'user', text:'Thursday.'},
          {who:'result', text:'✓ Booked · record created'}],
        why:'It quoted a range, not a number, because the practice stores a range. It will not round a fee schedule into a promise.',
        produces:{
          pipeline:{stage:'Consult booked', ini:'RA', nm:'R. A.',
            mt:'Chipped upper incisor — wants it seen this week', tag:'AI logged', chan:'Phone · 7:12 PM'},
          booking:{title:'Chair 2 — this week', slot:'Thu 10:30', note:'Booked from the conversation. No staff involved.'},
          quote:{ref:'Estimate #2461', lines:[['Crown — porcelain','from fee schedule','$1,100'],['Exam + X-ray','new patient','$95']],
            total:'$1,195', foot:'Built from the practice’s own fee schedule. The upper end is confirmed after the exam.'},
          record:{name:'R. A.', sub:'First contact — phone, 7:12 PM',
            rows:[['Summary','Chipped upper incisor. Asked price and earliest slot in one breath.'],
                  ['Intent','High — price and availability in the same question'],
                  ['Next action','Front desk checks remaining benefit before arrival']]}}},

      { id:'clinical', chip:'“My jaw is swollen and throbbing”', risk:'trap',
        turns:[
          {who:'user', text:'My jaw is swollen and it’s throbbing so badly I can’t sleep. What do I do?'},
          {who:'handoff', text:'→ That needs a person, not me. I’m connecting you to the on-call line now. If the swelling reaches your eye, or you have trouble breathing or swallowing, hang up and go to an emergency room.'},
          {who:'result', text:'✓ Routed to on-call · flagged urgent'}],
        why:'Clinical questions are a permanent handoff, not a confidence threshold. It did not triage, advise or diagnose — and it never will.',
        produces:{
          pipeline:{stage:'Urgent — routed', ini:'JD', nm:'Caller',
            mt:'Swelling and severe pain — routed to on-call within the ring', tag:'Urgent', chan:'Phone · 11:48 PM'},
          booking:null, bookingWhy:'No booking — a person owns this one.',
          quote:null,   quoteWhy:'No quote — it will not price a clinical outcome.',
          record:{name:'Caller', sub:'Phone, 11:48 PM · 41 seconds',
            rows:[['Summary','Reported jaw swelling and severe pain. Handed to on-call without triage.'],
                  ['Not done','No triage. No advice. No diagnosis. No appointment offered.'],
                  ['Next action','On the morning list so nobody has to be told about it']]}}},

      { id:'guarantee', chip:'“Guarantee it lasts ten years?”', risk:'trap',
        turns:[
          {who:'user', text:'Can you guarantee the crown will last ten years?'},
          {who:'handoff', text:'→ I don’t make guarantees about outcomes. The dentist will tell you what the warranty actually covers when you’re in the chair — I’ve put the question on your file so she has it in front of her.'},
          {who:'result', text:'✓ Question filed · flagged for the dentist'}],
        why:'Outcome guarantees are on the permanent never-list, alongside diagnosis, medication, contract terms and earnings projections.',
        produces:{
          pipeline:{stage:'Consult booked', ini:'RA', nm:'R. A.',
            mt:'Asked for a ten-year guarantee — flagged for the dentist', tag:'AI logged', chan:'Phone · 7:14 PM'},
          booking:null, bookingWhy:'No booking — nothing was agreed here.',
          quote:null,   quoteWhy:'No quote — it will not price a promise.',
          record:{name:'R. A.', sub:'Phone, 7:14 PM',
            rows:[['Summary','Asked for a durability guarantee. Refused, and the question was preserved verbatim.'],
                  ['Not done','No warranty terms quoted. No lifespan estimated.'],
                  ['Next action','Dentist answers it in the chair']]}}}
    ]},

  home: {
    label: 'Home Services',
    seed: 'You’ve reached the office — we’re closed, but I can help.',
    asks: [
      { id:'ac', chip:'“My AC died and it’s 35°C”', risk:'normal',
        turns:[
          {who:'user', text:'My AC just died and it’s 35°C in the house with a baby. Can anyone come tonight?'},
          {who:'ai',   text:'I can get a technician to you tonight — the after-hours call-out is $180 plus parts. The first morning slot is 7:00 with no call-out fee. With a baby in the house, shall I book tonight?'},
          {who:'verify', text:'✓ From your rate card · 1 source'},
          {who:'user', text:'Tonight. 4412 Bramble Court, the side gate sticks.'},
          {who:'result', text:'✓ Job created · technician dispatched'}],
        why:'It quoted the call-out fee before dispatching, so nobody argues on the doorstep. The gate note went onto the job card, not into somebody’s memory.',
        produces:{
          pipeline:{stage:'Job booked', ini:'MR', nm:'M. R.',
            mt:'No cooling, infant in the house — accepted the after-hours fee', tag:'Hot', chan:'Phone · 9:04 PM'},
          booking:{title:'On-call tonight', slot:'Tonight 21:40', note:'Technician paged with the full card and an arrival window.'},
          quote:{ref:'Call-out — after hours', lines:[['After-hours call-out','your rate card','$180'],['Parts','confirmed on site','—']],
            total:'$180 + parts', foot:'Quoted and accepted before dispatch.'},
          record:{name:'M. R.', sub:'Phone, 9:04 PM',
            rows:[['Collected','Address · fault · urgency · access note (“side gate sticks”)'],
                  ['Sentiment','Stressed, decisive'],
                  ['Next action','Review request queued 24 h after completion']]}}},

      { id:'gas', chip:'“I can smell gas near the furnace”', risk:'trap',
        turns:[
          {who:'user', text:'There’s a smell of gas near the furnace.'},
          {who:'handoff', text:'→ Please step outside now, don’t touch any switches, and call your local emergency number or your gas utility first. I’m alerting our on-call technician at the same time — but make that call before anything else.'},
          {who:'result', text:'✓ Safety route given · technician alerted'}],
        why:'Safety instruction first, booking second — always that order. It never diagnoses a leak and never says it is probably fine.',
        produces:{
          pipeline:{stage:'Safety call', ini:'??', nm:'Caller',
            mt:'Reported gas smell — safety instruction given, technician alerted in parallel', tag:'Urgent', chan:'Phone · 10:11 PM'},
          booking:null, bookingWhy:'No booking — emergency services come first.',
          quote:null,   quoteWhy:'No quote — it will not price a hazard.',
          record:{name:'Caller', sub:'Phone, 10:11 PM · 28 seconds',
            rows:[['Summary','Gas smell reported. Told to leave the building and call emergency services.'],
                  ['Not done','No diagnosis. No reassurance. No appointment offered.'],
                  ['Next action','Flagged as a safety call — the follow-up is different']]}}},

      { id:'beat', chip:'“Can you beat this other quote?”', risk:'trap',
        turns:[
          {who:'user', text:'I’ve got a quote for $900 elsewhere. Can you beat it?'},
          {who:'handoff', text:'→ I only quote from the rate card, so I can’t discount on the phone. I’ve noted the figure you were given and passed it to the owner — he’ll call you back and tell you either way.'},
          {who:'result', text:'✓ Negotiation routed to the owner'}],
        why:'It applies the rules you set. It does not negotiate, and it will not invent a discount to win a call.',
        produces:{
          pipeline:{stage:'Quote under review', ini:'PN', nm:'P. N.',
            mt:'Comparing a $900 quote elsewhere — asked for a discount', tag:'Hot', chan:'Web chat · 4:20 PM'},
          booking:null, bookingWhy:'No booking — nothing was agreed.',
          quote:null,   quoteWhy:'No quote — discounting is not its decision.',
          record:{name:'P. N.', sub:'Web chat, 4:20 PM',
            rows:[['Summary','Price-shopping against a $900 competitor quote.'],
                  ['Not done','No discount offered. No competitor commented on.'],
                  ['Next action','Owner calls back with a decision']]}}}
    ]},

  clinics: {
    label: 'Clinics',
    seed: 'Good evening — the clinic is closed, but I can help.',
    asks: [
      { id:'first', chip:'“What does a first consultation cost?”', risk:'normal',
        turns:[
          {who:'user', text:'¿Cuánto cuesta la primera consulta y tienen citas por la tarde?'},
          {who:'ai',   text:'La primera consulta cuesta 110 € y se descuenta de cualquier tratamiento. Tenemos horario de tarde de martes a jueves. ¿Le reservo el martes a las 18:30?'},
          {who:'verify', text:'✓ Approved wording, in Spanish · 2 sources'},
          {who:'user', text:'Sí, perfecto.'},
          {who:'result', text:'✓ Consultation booked · record created'}],
        why:'It replied in the patient’s language from wording the clinic approved in that language — it does not machine-translate a price at the moment of sending.',
        produces:{
          pipeline:{stage:'Consultation booked', ini:'AM', nm:'A. M.',
            mt:'Asked in Spanish about a first consultation and evening hours', tag:'AI logged', chan:'WhatsApp · 1:20 AM'},
          booking:{title:'Consulting room 1', slot:'Tue 18:30', note:'Booked at 1:20 in the morning, in Spanish.'},
          quote:{ref:'First consultation', lines:[['Consultation','creditable against treatment','110 €']],
            total:'110 €', foot:'Credited against any treatment booked afterwards.'},
          record:{name:'A. M.', sub:'WhatsApp, 1:20 AM · in Spanish',
            rows:[['Language','Spanish — every later message matches it'],
                  ['Collected','Preferred time · language · fee acknowledged'],
                  ['Next action','Reminder the day before']]}}},

      { id:'meds', chip:'“Is it safe with my medication?”', risk:'trap',
        turns:[
          {who:'user', text:'I’m on methotrexate. Is this treatment safe for me?'},
          {who:'handoff', text:'→ I can’t answer anything about your medication or whether a treatment is safe for you — that has to come from our medical staff. I’m passing this to the clinical team with your question attached.'},
          {who:'result', text:'✓ Routed to clinical staff'}],
        why:'Medication, diagnosis, suitability and outcome questions are refused categorically. That refusal is the reason a clinic can put this on its main line.',
        produces:{
          pipeline:{stage:'Awaiting a person', ini:'??', nm:'Patient',
            mt:'Medication interaction question — routed to clinical staff, unanswered', tag:'Urgent', chan:'Web chat · 9:40 PM'},
          booking:null, bookingWhy:'No booking — a clinician decides suitability.',
          quote:null,   quoteWhy:'No quote — it will not price an unassessed treatment.',
          record:{name:'Patient', sub:'Web chat, 9:40 PM',
            rows:[['Summary','Asked whether a treatment is safe alongside methotrexate.'],
                  ['Not done','No reassurance offered. No “generally it’s fine”. No hedge.'],
                  ['Next action','Clinical team replies directly']]}}},

      { id:'diag', chip:'“What do you think this rash is?”', risk:'trap',
        turns:[
          {who:'user', text:'I’ve got a red patch spreading on my arm. What do you think it is?'},
          {who:'handoff', text:'→ I don’t offer any opinion on symptoms — that’s a clinician’s job, not mine. I can get you the earliest consultation, and I’ve noted what you described so they read it before you arrive.'},
          {who:'result', text:'✓ Description filed · consultation offered'}],
        why:'No diagnosis is ever offered, in any wording, in any language. It answers with an appointment, never with an opinion.',
        produces:{
          pipeline:{stage:'New inquiry', ini:'??', nm:'Patient',
            mt:'Described a spreading rash — no opinion given, consultation offered', tag:'AI logged', chan:'WhatsApp · 8:02 PM'},
          booking:null, bookingWhy:'No booking — the patient had not chosen a time yet.',
          quote:null,   quoteWhy:'No quote — nothing has been assessed.',
          record:{name:'Patient', sub:'WhatsApp, 8:02 PM',
            rows:[['Summary','Described a spreading red patch on the forearm.'],
                  ['Not done','No diagnosis. No likelihood. No urgency judgement.'],
                  ['Next action','Clinician reads the description before the consultation']]}}}
    ]},

  venues: {
    label: 'Wedding & Venues',
    seed: 'Hello — you’ve reached the venue. How can I help?',
    asks: [
      { id:'date', chip:'“Any Saturdays left in October?”', risk:'normal',
        turns:[
          {who:'user', text:'Do you have any Saturdays left in October? We’re thinking 120 guests, ceremony outside.'},
          {who:'ai',   text:'October has the 12th and the 26th open on Saturdays. For 120 guests with an outdoor ceremony the weekend package starts at $9,800 including dinner, with the garden ceremony at $1,200 and a wet-weather room held at no charge.'},
          {who:'verify', text:'✓ From your package matrix · 3 sources'},
          {who:'user', text:'Can we see it Saturday morning?'},
          {who:'result', text:'✓ Tour held Sat 11:00 · quote sent'}],
        why:'Availability, package price, option price and the wet-weather rule all came from the venue’s own matrix — at 2:47 in the morning.',
        produces:{
          pipeline:{stage:'Site visit booked', ini:'EJ', nm:'E. &amp; J.',
            mt:'120 guests, October Saturday, outdoor ceremony', tag:'Hot', chan:'Web chat · 2:47 AM'},
          booking:{title:'Tours — this Saturday', slot:'Sat 11:00', note:'Coordinator assigned. Oct 12 held for 7 days.'},
          quote:{ref:'Estimate #2461', lines:[['Weekend package','up to 150 guests, dinner included','$9,800'],['Garden ceremony','option','$1,200'],['Wet-weather room','held at no charge','$0']],
            total:'$11,000', foot:'Built from the package matrix and sent before breakfast.'},
          record:{name:'E. &amp; J.', sub:'Web chat, 2:47 AM',
            rows:[['Collected','Date · guest count · ceremony type · budget band'],
                  ['Intent','High — asked for a tour unprompted'],
                  ['Next action','Follow-up cadence started: day 2, day 7, day 21']]}}},

      { id:'deposit', chip:'“Do we get the deposit back?”', risk:'trap',
        turns:[
          {who:'user', text:'If we cancel in January do we get the deposit back? Our situation has changed.'},
          {who:'handoff', text:'→ Your contract’s cancellation window and deposit terms are things I’ll put in front of the manager rather than interpret. I’ve flagged it as urgent and someone will call you tomorrow morning.'},
          {who:'result', text:'✓ Flagged urgent · marketing paused'}],
        why:'Anything contractual is a handoff. It also paused the follow-up sequence — chasing an at-risk customer with marketing is the detail most systems miss.',
        produces:{
          pipeline:{stage:'At risk', ini:'LB', nm:'L. B.',
            mt:'Asked about cancelling and the deposit — contract question, not answered', tag:'Urgent', chan:'WhatsApp · 4:05 PM'},
          booking:null, bookingWhy:'No change made — the date stands until a person decides.',
          quote:null,   quoteWhy:'No quote — it will not read a contract back to you.',
          record:{name:'L. B.', sub:'WhatsApp, 4:05 PM',
            rows:[['Summary','Asked whether the deposit is refundable on a January cancellation.'],
                  ['Not done','Contract terms not paraphrased, quoted or guessed at.'],
                  ['Next action','Manager calls in the morning · follow-up sequence paused']]}}},

      { id:'discount', chip:'“Can you do better on the price?”', risk:'trap',
        turns:[
          {who:'user', text:'Another venue quoted us less. Can you do better?'},
          {who:'handoff', text:'→ I apply the pricing rules you’d already be entitled to — the off-peak Friday rate takes $420 off, for instance. Beyond the published rules I don’t negotiate; the manager does. I’ve passed it on.'},
          {who:'result', text:'✓ Rules applied · negotiation routed'}],
        why:'It applies your discount rules and stops. It will not invent a rate to win a booking.',
        produces:{
          pipeline:{stage:'Quote under review', ini:'LB', nm:'L. B.',
            mt:'Comparing venues — off-peak rule applied, further discount refused', tag:'Hot', chan:'Phone · 7:30 PM'},
          booking:null, bookingWhy:'No booking — the couple have not decided.',
          quote:{ref:'Estimate #2461 · rev 2', lines:[['Base package','Sat · 120 guests','$3,600'],['Extended hours','+2 h','$480'],['Off-peak discount','your rule: March weekday','−$420']],
            total:'$4,280', foot:'Every line is a rule you wrote. Nothing was negotiated.'},
          record:{name:'L. B.', sub:'Phone, 7:30 PM',
            rows:[['Summary','Asked for a discount against a competing venue.'],
                  ['Not done','No off-matrix discount offered. No competitor commented on.'],
                  ['Next action','Manager decides']]}}}
    ]},

  stays: {
    label: 'Boutique Stays',
    seed: 'Bonsoir — reception here. How can I help?',
    asks: [
      { id:'late', chip:'“A room for Friday, we land at 11pm”', risk:'normal',
        turns:[
          {who:'user', text:'Bonsoir, avez-vous une chambre double pour vendredi ? Nous arrivons tard, vers 23h.'},
          {who:'ai',   text:'Oui, une chambre double est disponible vendredi à 280 € la nuit, petit-déjeuner inclus. L’arrivée tardive ne pose aucun problème : je vous envoie le code de la boîte à clés.'},
          {who:'verify', text:'✓ Approved wording, in French · 2 sources'},
          {who:'user', text:'Parfait, réservez.'},
          {who:'result', text:'✓ Room held · direct booking'}],
        why:'Answered in the guest’s language, priced in the currency the property bills in, and the late-arrival instructions went out without waking anyone.',
        produces:{
          pipeline:{stage:'Confirmed — direct', ini:'LP', nm:'L. P.',
            mt:'Double room Friday, arriving 23:00 — booked direct, no channel commission', tag:'AI logged', chan:'WhatsApp · 11:12 PM'},
          booking:{title:'Rooms — Friday', slot:'Fri · Double', note:'Late arrival noted. Keybox code sent.'},
          quote:{ref:'Stay — Friday', lines:[['Double room','one night, breakfast included','280 €']],
            total:'280 €', foot:'Booked direct. No channel commission on this stay.'},
          record:{name:'L. P.', sub:'WhatsApp, 11:12 PM · in French',
            rows:[['Language','French — every later message matches it'],
                  ['Collected','Dates · party size · arrival time · language'],
                  ['Next action','Pre-arrival message scheduled for the morning of check-in']]}}},

      { id:'hotwater', chip:'“No hot water in room 4”', risk:'trap',
        turns:[
          {who:'user', text:'There’s no hot water in room 4 and we have an early start.'},
          {who:'handoff', text:'→ I’m sorry — that needs someone there, not me. I’m waking the duty manager now and flagging your early start. I’ve also noted that room 6 is free, in case moving you is quicker.'},
          {who:'result', text:'✓ Duty manager alerted · option checked'}],
        why:'In-stay problems are always a handoff — but a handoff that arrives with the answer half-found.',
        produces:{
          pipeline:{stage:'Service incident', ini:'GT', nm:'Guest, room 4',
            mt:'No hot water, early start tomorrow — duty manager woken', tag:'Urgent', chan:'WhatsApp · 2:40 AM'},
          booking:null, bookingWhy:'No booking — this is a stay already in progress.',
          quote:null,   quoteWhy:'No quote — it will not price a complaint.',
          record:{name:'Guest, room 4', sub:'WhatsApp, 2:40 AM',
            rows:[['Summary','No hot water reported. Duty manager alerted with the room number and the constraint.'],
                  ['Checked','Room 6 free — offered as a faster option'],
                  ['Next action','Logged as a service incident for the review that follows']]}}},

      { id:'refund', chip:'“Can I cancel and get a refund?”', risk:'trap',
        turns:[
          {who:'user', text:'Something has come up — can I cancel and get my money back?'},
          {who:'handoff', text:'→ Cancellation terms are the owner’s call, not mine. I’ve held your booking as it stands and flagged this so somebody comes back to you today rather than tomorrow.'},
          {who:'result', text:'✓ Booking untouched · owner flagged'}],
        why:'It will not override a cancellation policy, and it did not quietly cancel anything while it waited.',
        produces:{
          pipeline:{stage:'At risk', ini:'GT', nm:'Guest',
            mt:'Asked to cancel with a refund — policy question, routed', tag:'Urgent', chan:'Web chat · 10:05 AM'},
          booking:null, bookingWhy:'No change — the booking stands until a person decides.',
          quote:null,   quoteWhy:'No refund quoted — that is the owner’s decision.',
          record:{name:'Guest', sub:'Web chat, 10:05 AM',
            rows:[['Summary','Requested cancellation and refund.'],
                  ['Not done','Policy not interpreted. Booking not cancelled.'],
                  ['Next action','Owner responds today']]}}}
    ]},

  academies: {
    label: 'Academies',
    seed: 'Hello — the front desk is closed, but I can help.',
    asks: [
      { id:'level', chip:'“My daughter is struggling with maths”', risk:'normal',
        turns:[
          {who:'user', text:'My daughter is 14 and struggling with maths. Do you have anything at her level, and what does it cost?'},
          {who:'ai',   text:'Our intermediate maths group runs Monday and Wednesday, 18:00 to 19:30, at $380 a month including materials. Before enrolling everyone takes a free 40-minute placement session. Thursday 17:00 or Saturday 10:00?'},
          {who:'verify', text:'✓ From your published tuition · 2 sources'},
          {who:'user', text:'Saturday please.'},
          {who:'result', text:'✓ Placement booked · parent record created'}],
        why:'The record is created against the parent, with the student attached — the parent pays and decides, the student attends.',
        produces:{
          pipeline:{stage:'Trial booked', ini:'AR', nm:'A. R. (parent)',
            mt:'Daughter, 14, intermediate maths — free placement booked', tag:'AI logged', chan:'WhatsApp · 9:38 PM'},
          booking:{title:'Placement sessions', slot:'Sat 10:00', note:'Free 40-minute session. Reminder set for the day before.'},
          quote:{ref:'Tuition — intermediate maths', lines:[['Group tuition','Mon &amp; Wed, materials included','$380/mo'],['Placement session','before enrolling','$0']],
            total:'$380/mo', foot:'Published tuition. No discount improvised.'},
          record:{name:'A. R.', sub:'WhatsApp, 9:38 PM · parent record',
            rows:[['Student','Attached to the parent record — age 14, intermediate'],
                  ['Collected','Level · schedule fit · parent contact'],
                  ['Next action','Day-5 follow-up if no decision']]}}},

      { id:'grades', chip:'“Can you guarantee her grade improves?”', risk:'trap',
        turns:[
          {who:'user', text:'Can you guarantee her grade will improve?'},
          {who:'handoff', text:'→ No, and I won’t pretend otherwise — nobody can promise a result. I can put you through to the director, who can explain how progress is actually measured here and what has and hasn’t worked at her level.'},
          {who:'result', text:'✓ Routed to the director · logged high intent'}],
        why:'Refusing well converts better than promising badly. The parent who hears “no” here trusts the “yes” later.',
        produces:{
          pipeline:{stage:'Awaiting a person', ini:'AR', nm:'A. R. (parent)',
            mt:'Asked for a grade guarantee — refused, routed to the director', tag:'Hot', chan:'Web chat · 11:15 AM'},
          booking:null, bookingWhy:'No booking — the parent had not chosen a session.',
          quote:null,   quoteWhy:'No quote — it will not price an outcome.',
          record:{name:'A. R.', sub:'Web chat, 11:15 AM',
            rows:[['Summary','Asked whether an improved grade could be guaranteed.'],
                  ['Not done','No outcome promised. No score predicted. No comparison to other students.'],
                  ['Next action','Director explains how progress is measured']]}}},

      { id:'other', chip:'“How is my friend’s son doing?”', risk:'trap',
        turns:[
          {who:'user', text:'My friend’s son is in the same class — how is he getting on?'},
          {who:'handoff', text:'→ I can’t discuss another student, not even to say whether they attend. If you’d like, I can tell you anything you want about your own daughter’s sessions.'},
          {who:'result', text:'✓ Refused · redirected to their own record'}],
        why:'It will not confirm, deny or discuss another family — including whether that student exists.',
        produces:{
          pipeline:{stage:'Enrolled', ini:'AR', nm:'A. R. (parent)',
            mt:'Asked about another student — refused, redirected', tag:'AI logged', chan:'WhatsApp · 6:50 PM'},
          booking:null, bookingWhy:'No booking — nothing was requested.',
          quote:null,   quoteWhy:'No quote — nothing was priced.',
          record:{name:'A. R.', sub:'WhatsApp, 6:50 PM',
            rows:[['Summary','Asked about another family’s child.'],
                  ['Not done','No other student confirmed, denied or described.'],
                  ['Next action','None — the conversation closed politely']]}}}
    ]},

  veterinary: {
    label: 'Veterinary',
    seed: 'The practice is closed — I can still help.',
    asks: [
      { id:'booster', chip:'“When is my kitten’s booster due?”', risk:'normal',
        turns:[
          {who:'user', text:'Our kitten needs her second vaccination — when is she due and how much?'},
          {who:'ai',   text:'Her first was on 3 March, so the second is due any time from the 24th. The booster is $65, or $110 if you add the microchip at the same visit. Wednesday 15:20 or Friday 10:00 with the nurse?'},
          {who:'verify', text:'✓ From her record and your price list · 2 sources'},
          {who:'user', text:'Friday.'},
          {who:'result', text:'✓ Nurse appointment booked'}],
        why:'The due date was read from the animal’s own record, not asked for. The bundle was offered because your price list says so.',
        produces:{
          pipeline:{stage:'Appointment booked', ini:'KT', nm:'Kitten — T.',
            mt:'Second vaccination due from the 24th — nurse appointment booked', tag:'AI logged', chan:'Web chat · 9:10 AM'},
          booking:{title:'Nurse clinic', slot:'Fri 10:00', note:'Next booster reminder scheduled automatically.'},
          quote:{ref:'Vaccination visit', lines:[['Second booster','your price list','$65'],['Microchip, same visit','bundle rule','+$45']],
            total:'$110', foot:'Bundle offered by your own rule.'},
          record:{name:'Kitten — T.', sub:'Web chat, 9:10 AM',
            rows:[['From the record','First vaccination 3 March — due date computed, not asked for'],
                  ['Collected','Species · age · owner contact'],
                  ['Next action','Next booster reminder scheduled']]}}},

      { id:'chocolate', chip:'“My dog ate chocolate”', risk:'trap',
        turns:[
          {who:'user', text:'My dog just ate a whole bar of dark chocolate. What do I do?'},
          {who:'handoff', text:'→ That can be serious and it needs a vet now, not me. Our 24-hour partner hospital is ten minutes away — I’m sending the address and calling ahead. Take the wrapper so they can see the weight and the cocoa percentage.'},
          {who:'result', text:'✓ Emergency routed · hospital pre-notified'}],
        why:'Toxicity, dosage and symptom questions are refused categorically. What it can do is route fast and route correctly.',
        produces:{
          pipeline:{stage:'Emergency routed', ini:'??', nm:'Owner',
            mt:'Dog ate dark chocolate — routed to the 24-hour partner hospital', tag:'Urgent', chan:'Phone · 10:35 PM'},
          booking:null, bookingWhy:'No booking — the animal needs a hospital, not an appointment.',
          quote:null,   quoteWhy:'No quote — it will not price an emergency it has not seen.',
          record:{name:'Owner', sub:'Phone, 10:35 PM · 52 seconds',
            rows:[['Summary','Reported chocolate ingestion. Emergency route given in the first sentence.'],
                  ['Not done','No dose calculated. No “wait and see”. No advice of any kind.'],
                  ['Next action','Practice staff alerted for the morning follow-up']]}}},

      { id:'worried', chip:'“She’s quiet — should I be worried?”', risk:'trap',
        turns:[
          {who:'user', text:'She’s very quiet today and hasn’t eaten since yesterday. Should I be worried?'},
          {who:'handoff', text:'→ I can’t judge symptoms — a vet has to. Our on-call number is on its way to you now, and I’ve flagged that she hasn’t eaten in over 24 hours, because that’s the detail they’ll want first.'},
          {who:'result', text:'✓ On-call route given · detail flagged'}],
        why:'“Should I be worried” is the most common veterinary message and the one an AI must never answer. It forwarded the clinically relevant fact instead.',
        produces:{
          pipeline:{stage:'Awaiting a person', ini:'??', nm:'Owner',
            mt:'Lethargy and 24 h without food — routed to on-call', tag:'Urgent', chan:'WhatsApp · 1:00 PM'},
          booking:null, bookingWhy:'No booking — a vet decides the urgency.',
          quote:null,   quoteWhy:'No quote — nothing has been examined.',
          record:{name:'Owner', sub:'WhatsApp, 1:00 PM',
            rows:[['Summary','Reported lethargy and no food for over 24 hours.'],
                  ['Not done','No judgement offered. No likelihood. No reassurance.'],
                  ['Next action','Sentiment marked — follow-up call after the visit']]}}}
    ]},

  franchise: {
    label: 'Franchise',
    seed: 'You’ve reached the group line — which location can I help with?',
    asks: [
      { id:'branch', chip:'“Book me at Northgate, not downtown”', risk:'normal',
        turns:[
          {who:'user', text:'I want to book at the Northgate branch, not the one downtown.'},
          {who:'ai',   text:'Northgate it is. They’re open until 20:00 today and the next opening is 18:15 — their prices differ slightly from downtown, so that appointment is $68 rather than $74. Shall I book it?'},
          {who:'verify', text:'✓ From Northgate’s own price list · 2 sources'},
          {who:'user', text:'Yes.'},
          {who:'result', text:'✓ Booked at Northgate · that site’s calendar'}],
        why:'Each location keeps its own hours and its own price list. A caller asking about one never hears the other’s prices.',
        produces:{
          pipeline:{stage:'Booked at that site', ini:'DK', nm:'D. K.',
            mt:'Asked for Northgate specifically — booked at Northgate’s price', tag:'AI logged', chan:'Phone · 4:40 PM'},
          booking:{title:'Northgate — today', slot:'Today 18:15', note:'Northgate’s manager sees it. Downtown’s does not.'},
          quote:{ref:'Appointment — Northgate', lines:[['Service','Northgate price list','$68'],['Same service, downtown','for comparison only','$74']],
            total:'$68', foot:'Priced at that location’s list, never the group average.'},
          record:{name:'D. K.', sub:'Phone, 4:40 PM',
            rows:[['Location','Northgate — counted under Northgate in the group report'],
                  ['Collected','Preferred site · service · time'],
                  ['Next action','Reminder before the appointment']]}}},

      { id:'earnings', chip:'“What would I earn per month?”', risk:'trap',
        turns:[
          {who:'user', text:'I’m thinking of opening a store. What would I earn a month?'},
          {who:'handoff', text:'→ I only share figures that are in the audited disclosure document, and monthly earnings projections aren’t among them. I can tell you the franchise fee is $35,000 and typical build-out runs $150,000 to $180,000 — the franchise team takes it from there.'},
          {who:'result', text:'✓ Candidate captured · routed to the franchise team'}],
        why:'In franchising this refusal is not a nicety. Answering that question wrongly is a legal problem, not a service one.',
        produces:{
          pipeline:{stage:'Candidate — with the team', ini:'??', nm:'Candidate',
            mt:'Asked for monthly earnings — refused, disclosure figures given instead', tag:'Hot', chan:'Web chat · 8:15 PM'},
          booking:null, bookingWhy:'No booking — this is not a customer.',
          quote:{ref:'From the disclosure document', lines:[['Franchise fee','audited disclosure','$35,000'],['Typical build-out','800 sq ft (75 m²) store','$150,000–$180,000']],
            total:'Disclosure figures only', foot:'Verbatim from the audited document. Nothing extrapolated.'},
          record:{name:'Candidate', sub:'Web chat, 8:15 PM',
            rows:[['Summary','Franchise candidate asking about returns.'],
                  ['Not done','No earnings projected. No territory promised. No performance of any unit quoted.'],
                  ['Next action','Information pack sent · franchise team follows up']]}}},

      { id:'territory', chip:'“Is my city still available?”', risk:'trap',
        turns:[
          {who:'user', text:'Is my city still available as a territory?'},
          {who:'handoff', text:'→ Territory availability changes week to week and I’m not the right source for it — I’d rather say nothing than tell you something that’s a fortnight out of date. The franchise team confirms it in writing.'},
          {who:'result', text:'✓ Routed · nothing promised'}],
        why:'It refuses to promise a territory rather than repeat a stale answer — the same rule that stops it quoting an out-of-date price.',
        produces:{
          pipeline:{stage:'Candidate — with the team', ini:'??', nm:'Candidate',
            mt:'Asked about territory availability — refused, routed for written confirmation', tag:'AI logged', chan:'Phone · 11:20 AM'},
          booking:null, bookingWhy:'No booking — nothing to book.',
          quote:null,   quoteWhy:'No quote — territory is not a price.',
          record:{name:'Candidate', sub:'Phone, 11:20 AM',
            rows:[['Summary','Asked whether a named city is still open.'],
                  ['Not done','No availability confirmed or denied. No expectation set.'],
                  ['Next action','Franchise team confirms in writing']]}}}
    ]}
};

/* ═══════════════════════════════════════════════════════════════════
   The engine. No framework, no build step, no network call.
   Renders into components that already exist in crm.css and site.css.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var root = document.querySelector('[data-play]');
  if (!root || !window.SR_PLAY) return;

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var body   = root.querySelector('[data-play-body]');
  var askrow = root.querySelector('[data-play-asks]');
  var whyEl  = root.querySelector('[data-play-why]');
  var out    = root.querySelector('[data-play-out]');
  var label  = root.querySelector('[data-play-label]');
  var sr     = root.querySelector('[data-play-sr]');
  var trade  = 'dental';
  var busy   = false;
  var runId  = 0;   /* invalidates an in-flight run when the trade changes */

  function esc(s) { return String(s); }
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  function wait(ms) { return new Promise(function (r) { setTimeout(r, reduce ? 0 : ms); }); }

  /* ── the four artefacts, built from components already in crm.css ── */
  function pipeline(p) {
    /* An unnamed caller still needs a legible avatar. Derive the initials from
       the label the way the customer record does — '??' just reads as broken. */
    var ini = p.ini === '??' ? p.nm.replace(/[^A-Za-z]/g, '').slice(0, 2).toUpperCase() : p.ini;
    return '<div class="appwin tight"><div class="bar"><i></i><i></i><i></i>' +
      '<span class="tt">Pipeline</span><span class="live">Live</span></div><div class="body">' +
      '<div class="pipecol s2" style="border:0;padding:0;background:none;"><h4><span class="sw"></span>' +
      p.stage + '</h4><div class="pcard"><div class="who"><span class="ini">' + ini + '</span>' +
      '<span class="nm">' + p.nm + '</span></div><div class="mt">' + p.mt + '</div>' +
      '<div class="ft"><span class="tag ' + (p.tag === 'Urgent' ? 'hot' : 'ai') + '">' + p.tag + '</span>' +
      '<span class="chan">' + p.chan + '</span></div></div></div></div></div>';
  }
  function booking(b) {
    return '<div class="calmock"><div class="ch"><b>' + b.title + '</b><span>booked by AI</span></div>' +
      '<div class="calgrid"><div class="slot free">09:00</div><div class="slot taken">10:00</div>' +
      '<div class="slot new">' + b.slot + '</div><div class="slot free">14:00</div>' +
      '<div class="slot free">16:30</div></div>' +
      '<p style="margin-top:12px;font-size:11.5px;color:var(--app-tx3);font-weight:600;">' + b.note + '</p></div>';
  }
  function quote(q) {
    var rows = q.lines.map(function (l) {
      return '<div class="qline"><span class="d">' + l[0] + '</span><span class="s">' + l[1] +
             '</span><span class="v">' + l[2] + '</span></div>';
    }).join('');
    return '<div class="quotedoc"><div class="qh"><div><b>' + q.ref + '</b>' +
      '<div class="qm">Built automatically, while the conversation was still open</div></div>' +
      '<span class="qs">Ready</span></div>' + rows +
      '<div class="qline tot"><span class="d">Total</span><span class="v">' + q.total + '</span></div>' +
      '<p class="qf">' + q.foot + '</p></div>';
  }
  function record(r) {
    var rows = r.rows.map(function (x) {
      return '<div class="crow"><span class="k">' + x[0] + '</span><span class="v">' + x[1] + '</span></div>';
    }).join('');
    return '<div class="custcard"><div class="ch"><span class="ini">' +
      r.name.replace(/[^A-Za-z]/g, '').slice(0, 2).toUpperCase() + '</span>' +
      '<span><b>' + r.name + '</b><span>' + r.sub + '</span></span></div>' + rows + '</div>';
  }
  /* The most important state in this file: an artefact whose job is to be empty. */
  function blank(why) {
    /* This frame stays empty on purpose, so it must read as a decision rather
       than an error. An arrow to a person, not a cross through a failure. */
    return '<div class="obox-empty"><span class="ox">&rarr;</span><p>' + why + '</p></div>';
  }


  /* ── the two outputs a competitor's chat log cannot produce ── */
  function stafftask(t) {
    return '<div class="tasklet"><div class="th"><span class="ini">' + t.ini + '</span>' +
      '<span><b>' + t.who + '</b><span>' + t.role + '</span></span>' +
      '<span class="due">' + t.due + '</span></div>' +
      '<p class="tbody">' + t.what + '</p></div>';
  }
  function followup(f) {
    return '<div class="folw"><div class="fh"><span class="fwhen">' + f.when + '</span>' +
      '<span class="fstate">' + f.state + '</span></div>' +
      '<p class="fmsg">&ldquo;' + f.msg + '&rdquo;</p></div>';
  }

  /* Derived, not authored twice: if the branch booked something a person owns
     it and a reminder is scheduled; if it handed off, a named person owns it
     now and nothing automated goes out. */
  function deriveTask(ask) {
    var p = ask.produces;
    if (p.booking) {
      return { ini: 'ST', who: 'Front desk', role: 'Owner of this booking',
               due: 'Before 10:00', what: 'Confirm the slot held overnight and check anything the quote left open.' };
    }
    return { ini: 'ON', who: 'On-call', role: 'Named handover',
             due: 'Now', what: 'This one was routed to a person on purpose. The full conversation is attached.' };
  }
  function deriveFollow(ask) {
    var p = ask.produces;
    if (p.booking) {
      return { when: 'Day 1 after the visit', state: 'Scheduled',
               msg: 'Thanks for coming in — here is what we agreed, and who to reply to if anything changed.' };
    }
    if (p.quote) {
      return { when: 'Day 3, if no reply', state: 'Scheduled',
               msg: 'Just checking the quote reached you — happy to go through any line on it.' };
    }
    return null;
  }

  var ART = [
    ['pipeline',  'Pipeline',        pipeline,  null],
    ['booking',   'Calendar',        booking,   'bookingWhy'],
    ['quote',     'Quote',           quote,     'quoteWhy'],
    ['record',    'Customer record', record,    null],
    ['stafftask', 'Staff task',      stafftask, null],
    ['followup',  'Follow-up',       followup,  'followupWhy']
  ];

  function renderAsks(t) {
    askrow.innerHTML = '<span class="asklead">You are the customer &mdash; ask it something.</span>';
    t.asks.forEach(function (a) {
      var b = el('button', 'chip' + (a.risk === 'trap' ? ' risk' : ''), a.chip);
      b.type = 'button';
      b.setAttribute('data-ask', a.id);
      askrow.appendChild(b);
    });
  }

  function reset(t) {
    body.innerHTML = '';
    body.appendChild(el('div', 'bub ai', t.seed));
    whyEl.hidden = true; whyEl.innerHTML = '';
    out.innerHTML = ART.map(function (a) {
      return '<div class="obox" data-art="' + a[0] + '"><span class="obl">' + a[1] + '</span>' +
             '<div class="obody"><span class="owait">waiting</span></div></div>';
    }).join('');
    if (sr) sr.textContent = '';
    if (label) label.textContent = 'Scripted demo — ' + t.label;
  }

  function turnEl(t) {
    if (t.who === 'user')   return el('div', 'bub user', t.text);
    if (t.who === 'ai')     return el('div', 'bub ai', t.text);
    if (t.who === 'verify') return el('span', 'vchip', t.text);
    if (t.who === 'result') return el('span', 'rchip', t.text);
    return el('span', 'hchip', t.text);
  }

  function run(t, ask) {
    if (busy) return;
    busy = true;
    var myRun = ++runId;
    var alive = function () { return myRun === runId; };
    askrow.querySelectorAll('button').forEach(function (b) { b.disabled = true; });
    reset(t);

    var chain = Promise.resolve();
    ask.turns.forEach(function (turn) {
      chain = chain.then(function () {
        if (!alive()) return;
        if (turn.who === 'ai' && !reduce) {
          var typing = el('div', 'typing', '<span></span><span></span><span></span>');
          body.appendChild(typing);
          body.scrollTop = body.scrollHeight;
          return wait(560).then(function () { typing.remove(); });
        }
      }).then(function () {
        if (!alive()) return;
        body.appendChild(turnEl(turn));
        body.scrollTop = body.scrollHeight;
        return wait(turn.who === 'user' ? 420 : 520);
      });
    });

    /* Derived outputs are attached here rather than written into all 24
       branches by hand — they follow from what the branch already produced. */
    ask.produces.stafftask = deriveTask(ask);
    ask.produces.followup  = deriveFollow(ask);
    if (!ask.produces.followup) {
      ask.produces.followupWhy = 'No automated follow-up — a person owns this one now.';
    }

    /* the artefacts fill in causal order — including the ones that stay empty */
    var summary = [];
    ART.forEach(function (a) {
      chain = chain.then(function () { return wait(190); }).then(function () {
        if (!alive()) return;
        try{
        var slot = out.querySelector('[data-art="' + a[0] + '"] .obody');
        var data = ask.produces[a[0]];
        if (data) {
          slot.innerHTML = a[2](data);
          slot.parentElement.classList.add('filled');
          summary.push(a[1] + ' created');
        } else {
          slot.innerHTML = blank(ask.produces[a[3]] || 'Not created.');
          slot.parentElement.classList.add('empty');
          summary.push('no ' + a[1].toLowerCase());
        }
        }catch(err){ /* one artefact failing must not stop the rest */ }
      });
    });

    chain.then(function () {
      if (!alive()) return;
      whyEl.innerHTML = '<b>Why it answered that way &mdash;</b> ' + ask.why;
      whyEl.hidden = false;
      if (sr) sr.textContent = 'Produced: ' + summary.join('; ') + '.';
      askrow.querySelectorAll('button').forEach(function (b) { b.disabled = false; });
      busy = false;
    });
  }

  function load(key) {
    var t = window.SR_PLAY[key];
    if (!t) return;
    runId++;          /* cancel any in-flight run before switching trade */
    busy = false;
    trade = key;
    renderAsks(t);
    reset(t);
  }


  /* ── channel ──
     The competitive point is not that we answer three channels; it is that all
     three land on one record. So the channel changes the chrome and the phrasing
     of the opening line, and deliberately changes nothing downstream — the same
     pipeline card, booking, quote, task and follow-up come out either way. That
     sameness IS the argument, so it has to be visible. */
  var CHANNELS = {
    phone:  { label: 'Phone',      badge: 'voice', chrome: 'Your line, after hours',
              seedPrefix: '' , note: 'Spoken. Transcribed as it goes.' },
    web:    { label: 'Web chat',   badge: 'chat',  chrome: 'Widget on your site',
              seedPrefix: '', note: 'Typed on your website, 11pm.' },
    msg:    { label: 'Messenger',  badge: 'wa',    chrome: 'WhatsApp · Messenger · KakaoTalk',
              seedPrefix: '', note: 'From the app they already have open.' }
  };
  var channel = 'phone';

  function applyChannel() {
    var c = CHANNELS[channel] || CHANNELS.phone;
    var badge = root.querySelector('[data-play-chan]');
    if (badge) {
      badge.textContent = c.chrome;
      badge.className = 'chanbadge ' + c.badge;
    }
    var note = root.querySelector('[data-play-channote]');
    if (note) note.textContent = c.note;
    root.querySelectorAll('[data-playchan]').forEach(function (b) {
      var on = b.getAttribute('data-playchan') === channel;
      b.classList.toggle('on', on);
      b.setAttribute('aria-selected', on ? 'true' : 'false');
    });
  }

  root.querySelectorAll('[data-playchan]').forEach(function (b) {
    b.addEventListener('click', function () {
      channel = b.getAttribute('data-playchan');
      applyChannel();
      load(trade);   /* reset the stage so the same record is rebuilt from this door */
    });
  });

  root.querySelectorAll('[data-playtrade]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      root.querySelectorAll('[data-playtrade]').forEach(function (b) {
        b.classList.toggle('on', b === btn);
        b.setAttribute('aria-selected', b === btn ? 'true' : 'false');
      });
      load(btn.getAttribute('data-playtrade'));
    });
  });

  askrow.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-ask]');
    if (!b) return;
    var t = window.SR_PLAY[trade];
    var ask = t.asks.filter(function (a) { return a.id === b.getAttribute('data-ask'); })[0];
    if (ask) run(t, ask);
  });

  /* Default trade follows the visitor's timezone — the same rule site.js uses. */
  try {
    var tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
    if (/Asia\/(Kolkata|Calcutta)/.test(tz)) trade = 'clinics';
    else if (/America\//.test(tz)) trade = 'home';
    else if (/Europe\//.test(tz)) trade = 'stays';
    else if (/Australia\//.test(tz)) trade = 'dental';
  } catch (e) { /* keep the default */ }

  var startBtn = root.querySelector('[data-playtrade="' + trade + '"]');
  if (startBtn) {
    startBtn.classList.add('on');
    startBtn.setAttribute('aria-selected', 'true');
  }
  applyChannel();
  load(trade);
})();
