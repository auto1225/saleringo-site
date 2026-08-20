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
    ]},

  property: {
    label: 'Property Management',
    seed: 'The office is closed — I can still raise a works order.',
    asks: [
      { id:'leak', chip:'“Water’s coming through the kitchen ceiling”', risk:'normal',
        turns:[
          {who:'user', text:'Water is coming through the kitchen ceiling at Flat 4. It’s getting worse.'},
          {who:'ai',   text:'Turn the stopcock off — it’s usually under the kitchen sink — and don’t use the kitchen lights or sockets until someone has looked at it. Uncontained water is on this property’s emergency list, so I can dispatch tonight rather than log it for Monday.'},
          {who:'verify', text:'✓ From this property’s management agreement · 1 source'},
          {who:'user', text:'It’s off. There’s a key safe.'},
          {who:'result', text:'✓ Approved contractor booked · landlord notified'}],
        why:'Make safe first, then dispatch. It read the emergency definition out of that property’s own agreement rather than deciding for itself what counts as urgent.',
        produces:{
          pipeline:{stage:'Contractor booked', ini:'A4', nm:'Ashcroft Ct · Flat 4',
            mt:'Water through the kitchen ceiling — made safe, Redway booked 07:00', tag:'Urgent', chan:'Phone · 1:15 AM'},
          booking:{title:'Out-of-hours attendance', slot:'07:00', note:'Key safe C4417 on the order; tenant home until 09:00.'},
          quote:{ref:'Works order — make safe', lines:[['Out-of-hours attendance','approved contractor rate','—'],['Authorised up to','landlord’s ceiling on this property','$250']],
            total:'Up to $250', foot:'Nothing above the ceiling without a person.'},
          record:{name:'Flat 4, Ashcroft Court', sub:'Phone, 1:15 AM',
            rows:[['From the record','Emergency definition read from this property’s management agreement'],
                  ['Collected','Unit · tenancy · access · isolation times'],
                  ['Next action','Landlord notified 01:36; manager reviews at 08:30']]}}},

      { id:'whopays', chip:'“Who’s paying for this — me or the landlord?”', risk:'trap',
        turns:[
          {who:'user', text:'So who’s paying for this — me or the landlord?'},
          {who:'handoff', text:'→ I’m not going to answer that. Who bears a repair cost depends on the tenancy and on what caused it, and that is a decision for your property manager, not for me. I’ve written your question down as you asked it and attached your tenancy to it.'},
          {who:'result', text:'✓ Question recorded · tenancy attached · queued'}],
        why:'Liability under a specific tenancy is a person’s decision. A wrong answer at 1 AM is a dispute in the morning and a deduction that will not stand.',
        produces:{
          pipeline:{stage:'Waiting on a person', ini:'A4', nm:'Ashcroft Ct · Flat 4',
            mt:'Asked who bears the cost — refused, routed to the property manager', tag:'Refused', chan:'Phone · 1:22 AM'},
          booking:null, bookingWhy:'No booking — nothing was being scheduled.',
          quote:null,   quoteWhy:'No quote — it does not price a liability decision.',
          record:{name:'Flat 4, Ashcroft Court', sub:'Phone, 1:22 AM',
            rows:[['Recorded verbatim','The question in the tenant’s own words, with the tenancy attached'],
                  ['Not done','No liability decided. No “usually the landlord”. No tenancy read back as an answer.'],
                  ['Next action','Property manager answers it in writing at 08:30']]}}},

      { id:'rent', chip:'“Can the landlord raise my rent by that much?”', risk:'trap',
        turns:[
          {who:'user', text:'I’ve had a notice. Can the landlord actually raise my rent by that much?'},
          {who:'handoff', text:'→ That’s tenancy law and I don’t give views on it, in any wording. I’ve logged it against your tenancy so the manager has it, and our published advice line is on the notice you were sent.'},
          {who:'result', text:'✓ Logged against the tenancy · routed'}],
        why:'Every wording of a tenancy-law answer is still advice, and it is still the agency that gave it.',
        produces:{
          pipeline:{stage:'Waiting on a person', ini:'??', nm:'Tenant',
            mt:'Asked whether a rent increase is lawful — refused, logged', tag:'Refused', chan:'Web chat · 9:05 PM'},
          booking:null, bookingWhy:'No booking — nothing to schedule.',
          quote:null,   quoteWhy:'No quote — this is not a priced question.',
          record:{name:'Tenant', sub:'Web chat, 9:05 PM',
            rows:[['Logged','Against the tenancy, with the notice date as given'],
                  ['Not done','No view on lawfulness. No figure. No “that sounds about right”.'],
                  ['Next action','Property manager responds; published advice line offered']]}}}
    ]},

  restaurants: {
    label: 'Restaurants',
    seed: 'We’ve finished service — I can still take a function inquiry.',
    asks: [
      { id:'function', chip:'“24 people, a Friday in December — minimum spend?”', risk:'normal',
        turns:[
          {who:'user', text:'24 people, a Friday in December, for the office party. What’s the minimum spend?'},
          {who:'ai',   text:'On a December Friday the private room is $300 hire with an $1,800 minimum spend, and the set menu is $68 a head. Twenty-four covers on that menu is $1,632, so you would be about $170 under the minimum — a drink each closes it. That is one sitting; we don’t turn the room on that date.'},
          {who:'verify', text:'✓ From your function sheet · 2 sources'},
          {who:'user', text:'Hold the 12th.'},
          {who:'result', text:'✓ Date held 72 hours · deposit link sent'}],
        why:'It quoted the peak-date minimum rather than the everyday one, and said out loud that the room is not turned — the two things an organiser finds out too late.',
        produces:{
          pipeline:{stage:'Date held', ini:'NB', nm:'N. B. · office party',
            mt:'24 covers, Fri 12 Dec dinner, private room — held 72 h', tag:'AI logged', chan:'Phone · 10:40 PM'},
          booking:{title:'Private room, dinner', slot:'Fri 12 Dec · 19:30', note:'Single sitting on this date — the room is not turned.'},
          quote:{ref:'Function — private room', lines:[['Room hire','private room','$300'],['Minimum spend','December Friday, peak','$1,800'],['Set menu','per head, 24 covers','$68']],
            total:'$1,800 min', foot:'From your function sheet. 24 covers at $68 is $1,632 — the gap to the minimum is named on the call, not discovered on the invoice.'},
          record:{name:'N. B. (organiser)', sub:'Phone, 10:40 PM',
            rows:[['Collected','Date · service · covers · occasion · arrival and turn'],
                  ['Deposit','$300, 14-day terms — payment link sent, no card touched'],
                  ['Next action','Date releases automatically if the deposit is unpaid']]}}},

      { id:'allergy', chip:'“One guest has a severe nut allergy — is it safe?”', risk:'trap',
        turns:[
          {who:'user', text:'One of the guests has a severe nut allergy. Is the set menu safe for her?'},
          {who:'handoff', text:'→ I’m not going to tell you that. Only the kitchen can answer what a dish contains and what it is prepared beside, so I’ve written the allergy down exactly as you said it and sent the head chef the question tonight. The date stays held, but it is not confirmed until he answers.'},
          {who:'result', text:'✓ Allergy recorded verbatim · chef asked · booking left unconfirmed'}],
        why:'“Should be fine” is the sentence that ends restaurants. The booking is deliberately left in an unconfirmed state so the question cannot be quietly dropped.',
        produces:{
          pipeline:{stage:'Held — waiting on the kitchen', ini:'NB', nm:'N. B. · office party',
            mt:'Severe nut allergy declared — recorded, not answered; chef asked', tag:'Urgent', chan:'Phone · 10:46 PM'},
          booking:{title:'Private room, dinner', slot:'Fri 12 Dec · 19:30', note:'Held, not confirmed. It stays that way until the kitchen answers.'},
          quote:null, quoteWhy:'No quote — the booking cannot be confirmed on this point.',
          record:{name:'N. B. (organiser)', sub:'Phone, 10:46 PM',
            rows:[['Recorded verbatim','The allergy in the organiser’s words, attached to the booking'],
                  ['Not done','No “should be fine”. No “the kitchen is careful”. No dish called free of anything.'],
                  ['Next action','Head chef answers in writing before the date is confirmed']]}}},

      { id:'squeeze', chip:'“Can you just squeeze us in at 8 on Saturday?”', risk:'trap',
        turns:[
          {who:'user', text:'Can you just squeeze us in at 8 on Saturday? It’s only six of us.'},
          {who:'handoff', text:'→ I can’t overbook the floor — eight o’clock on a Saturday is full on the plan in front of me, and a table that exists only in a booking system is worse than no table. 6:15 and 9:30 are genuinely free. I’ll put you on the waitlist for 8 as well.'},
          {who:'result', text:'✓ Second sitting booked · waitlisted for 8'}],
        why:'It offers the sittings that exist on the floor plan instead of the one the caller wants. Overbooking is the one favour that costs the restaurant the evening.',
        produces:{
          pipeline:{stage:'Booked · second sitting', ini:'??', nm:'Caller · 6 covers',
            mt:'Asked to be squeezed in at 8 — refused; 9:30 taken, waitlisted for 8', tag:'AI logged', chan:'Web chat · 8:20 PM'},
          booking:{title:'Dining room', slot:'Sat · 21:30', note:'From the real floor plan. Waitlisted for 20:00 if a table drops.'},
          quote:null, quoteWhy:'No quote — an à la carte cover is not a priced function.',
          record:{name:'Caller · 6 covers', sub:'Web chat, 8:20 PM',
            rows:[['Offered','6:15 and 9:30 — the sittings that are actually free'],
                  ['Not done','No table created that the floor plan does not have.'],
                  ['Next action','Waitlist alert if 20:00 releases']]}}}
    ]},

  salons: {
    label: 'Salons &amp; Barbers',
    seed: 'The salon’s closed — I can still book you in.',
    asks: [
      { id:'balayage', chip:'“How much for a full balayage?”', risk:'normal',
        turns:[
          {who:'user', text:'How much for a full balayage, and do you have a Saturday? My hair’s past my shoulders.'},
          {who:'ai',   text:'On our menu a full-head balayage is $180–$260, and at that length the $30 long-hair surcharge is already inside the band — I’d rather you heard that now than at the chair. It’s a double slot, so I need two together.'},
          {who:'verify', text:'✓ From your service menu · 2 sources'},
          {who:'user', text:'Marta if she’s free. Saturday.'},
          {who:'result', text:'✓ Two slots held in Marta’s column · deposit link sent'}],
        why:'It quoted the band, not a flat number, and named the length surcharge out loud — because a flat number on Sunday night is an argument at the chair on Saturday.',
        produces:{
          pipeline:{stage:'Held · deposit pending', ini:'EM', nm:'E. M.',
            mt:'Full-head balayage, past-shoulder length — asked for Marta by name', tag:'AI logged', chan:'Instagram · 9:35 PM'},
          booking:{title:'Marta’s column — Saturday', slot:'Sat 10:00 + 10:30', note:'Double slot held together. Held, not confirmed, until the deposit clears.'},
          quote:{ref:'Colour booking', lines:[['Full-head balayage','your service menu','$180–$260'],['Long-hair surcharge','already inside the band','+$30'],['Deposit to hold','your payment link','$40']],
            total:'$180–$260', foot:'Built from the salon’s own menu. The surcharge is named before the slot is offered, never after.'},
          record:{name:'E. M.', sub:'Instagram DM, 9:35 PM Sunday',
            rows:[['Collected','Service · length and current colour · stylist requested by name'],
                  ['Calendar','Double slot — two consecutive gaps in one column, never one gap and a hope'],
                  ['Next action','Deposit link sent on the same thread; added to the cancellation list']]}}},

      { id:'photo', chip:'“Will it come out like this photo?”', risk:'trap',
        turns:[
          {who:'user', text:'Will it come out like this photo?'},
          {who:'handoff', text:'→ I can’t tell you that, and I won’t guess at it — what a colour does depends on what’s already on the hair, and only somebody looking at it can say. I’ve saved the photo to your record so the stylist has it in front of her. The colour consultation is $35 and it comes off whatever we book after it.'},
          {who:'result', text:'✓ Consultation booked · reference image saved'}],
        why:'“Yes, that’s achievable” is the single most expensive sentence an answering service can say in this trade. It is a permanent refusal, not a confidence threshold.',
        produces:{
          pipeline:{stage:'Consultation booked', ini:'EM', nm:'E. M.',
            mt:'Sent a reference photo — no result promised, consultation booked instead', tag:'AI logged', chan:'WhatsApp · 10:14 PM'},
          booking:{title:'Colour consultation', slot:'Thu 18:00', note:'The appointment that produces the real answer and the real price.'},
          quote:null, quoteWhy:'No quote — it will not price a colour nobody has looked at.',
          record:{name:'E. M.', sub:'WhatsApp, 10:14 PM',
            rows:[['Saved','Reference image attached to the record before the stylist arrived'],
                  ['Not done','No result promised. No “that should be achievable”. No hedge.'],
                  ['Next action','Stylist sees the image before the client sits down']]}}},

      { id:'patchtest', chip:'“Can I skip the patch test?”', risk:'trap',
        turns:[
          {who:'user', text:'I reacted a bit last time — itchy for a day. Can I just skip the patch test?'},
          {who:'handoff', text:'→ No. Our rule is a patch test at least 48 hours before any colour service, with no exceptions, and I have no authority to move it — there is genuinely no colour date inside that window for me to offer you. I’m not going to judge what you’ve described either; I’ve written it down in your words and a stylist will call you.'},
          {who:'result', text:'✓ Colour dates suppressed · stylist called · test offered'}],
        why:'This is a calendar rule, not a script. Inside the window the colour dates do not exist, so there is nothing for a caller to talk it past.',
        produces:{
          pipeline:{stage:'Awaiting a person', ini:'??', nm:'Client',
            mt:'Asked to skip the patch test and reported a past reaction — refused, routed to a stylist', tag:'Urgent', chan:'Phone · 7:48 PM'},
          booking:null, bookingWhy:'No colour date exists inside the 48-hour window. A patch test was offered instead.',
          quote:null,   quoteWhy:'No quote — nothing may be booked until the test clears.',
          record:{name:'Client', sub:'Phone, 7:48 PM',
            rows:[['Recorded verbatim','“Reacted a bit last time — itchy for a day.” In her words, not a paraphrase.'],
                  ['Not done','No view on the reaction. No “that sounds mild”. No exception granted.'],
                  ['Next action','Named stylist calls tomorrow; patch test offered Saturday, which clears Monday']]}}}
    ]},

  auto: {
    label: 'Auto Repair',
    seed: 'Shop’s shut — I can still book the ramp.',
    asks: [
      { id:'diagnostic', chip:'“How much to look at the engine light?”', risk:'normal',
        turns:[
          {who:'user', text:'Engine light came on — how much to look at it, and can you take it tomorrow?'},
          {who:'ai',   text:'The diagnostic is $95, and it comes off the repair if we do the work. Our labour rate is $145 an hour. What I can’t do is tell you what the repair costs before it’s on the ramp. Ramp 1 has 8:00 or 11:30 — can I take the plate?'},
          {who:'verify', text:'✓ From your rate card · 2 sources'},
          {who:'user', text:'Eight. And I need it back for a 6 AM shift Thursday.'},
          {who:'result', text:'✓ Ramp booked · job card written · ceiling agreed'}],
        why:'It quoted the two figures that exist before anyone looks at the car — the diagnostic and the hourly rate — and took the authorisation ceiling on the call, so the morning starts with work instead of a phone call.',
        produces:{
          pipeline:{stage:'Ramp booked', ini:'RC', nm:'2017 1.5 petrol',
            mt:'“Hesitates under acceleration” · light on · drivable · needed back Thursday 6 AM', tag:'AI logged', chan:'Phone · 6:48 PM'},
          booking:{title:'Ramp 1 — tomorrow', slot:'Wed 08:00', note:'From the real workshop diary. Courtesy car held against the job card.'},
          quote:{ref:'Job card', lines:[['Diagnostic','your rate card','$95'],['Labour, per hour','published rate','$145'],['Courtesy car, per day','held against the job','$25']],
            total:'$95 to start', foot:'The diagnostic and the labour rate only. The repair is quoted on the ramp and approved before anything is touched.'},
          record:{name:'2017 1.5 petrol', sub:'Phone, 6:48 PM',
            rows:[['Collected','Plate → year, make, model and engine → guide time. The VIN is asked for when the plate is not enough.'],
                  ['Authorisation','$250 ceiling agreed on the call. Under it work starts at eight; over it somebody rings first.'],
                  ['Next action','Job card on the bench before the car is through the door']]}}},

      { id:'ballpark', chip:'“It grinds when I brake — what’ll that cost?”', risk:'trap',
        turns:[
          {who:'user', text:'It grinds when I brake. Roughly what’s that going to cost?'},
          {who:'handoff', text:'→ I’m not going to put a number on that. Grinding under braking could be three different jobs at three very different prices, and guessing at it on the phone only means you get a different number when it’s up on the ramp. The $95 diagnostic and the $145 hourly rate are what I can quote. I’ve written “grinding under braking” on the card in your words and flagged it as safety-related.'},
          {who:'result', text:'✓ Ramp booked · words recorded verbatim · flagged'}],
        why:'A shop owner will trust this page or dismiss it on this one sentence. It will not price a repair before the car is on the ramp — not as a range, not as a “usually around”, and not on the second ask.',
        produces:{
          pipeline:{stage:'Ramp booked', ini:'??', nm:'Caller',
            mt:'“Grinding under braking” — refused a price, flagged safety-related, ramp booked', tag:'Urgent', chan:'Phone · 7:02 PM'},
          booking:{title:'Ramp 1 — diagnostic', slot:'Wed 11:30', note:'The refusal did not end the conversation. The ramp was booked anyway.'},
          quote:null, quoteWhy:'No quote — it will not price a repair before the car is on the ramp.',
          record:{name:'Caller', sub:'Phone, 7:02 PM',
            rows:[['Recorded verbatim','“Grinding under braking.” In the caller’s words, not a paraphrase.'],
                  ['Not done','No price after being asked twice. No diagnosis. No “sounds like your pads”.'],
                  ['Next action','Flagged as a safety-related complaint so it is looked at first']]}}},

      { id:'safe', chip:'“Is it safe for me to drive it in?”', risk:'trap',
        turns:[
          {who:'user', text:'There’s a burning smell and the steering’s gone heavy. Is it safe for me to drive it in tomorrow?'},
          {who:'handoff', text:'→ I can’t tell you that and I won’t — nobody has seen the car and I’m not going to be the reason you set off in it. Our own wording is: if there’s a burning smell or the steering has changed, don’t drive it. Recovery within ten miles is $120 and I can book it to land before the ramp opens. I’ve paged the owner and he’ll ring you directly.'},
          {who:'result', text:'✓ Recovery offered · owner paged · escalation logged'}],
        why:'Roadworthiness on an unseen vehicle is never judged, in any wording. Brakes, steering, smoke and a fuel smell are keywords that stop the booking script cold and page a person.',
        produces:{
          pipeline:{stage:'Safety route — owner paged', ini:'??', nm:'Caller',
            mt:'Burning smell and heavy steering — no roadworthiness judgement given, recovery offered', tag:'Urgent', chan:'Phone · 9:14 PM'},
          booking:null, bookingWhy:'No ramp slot — the car should not be driven, so a recovery is offered instead.',
          quote:{ref:'Recovery, not a repair', lines:[['Recovery, within 10 miles','your rate card','$120']],
            total:'$120', foot:'A tow is a different job from a slot. Nothing about the repair is priced.'},
          record:{name:'Caller', sub:'Phone, 9:14 PM',
            rows:[['Reported','Burning smell and a change in the steering. Safety keywords both.'],
                  ['Not done','No roadworthiness judgement. No “a couple of miles should be alright”. Ever.'],
                  ['Next action','Owner paged in parallel and ringing directly; flagged for the morning review']]}}}
    ]},

  funeral: {
    label: 'Funeral Homes',
    seed: 'You’ve reached the funeral home. Our director is on call — how can I help?',
    asks: [
      { id:'firstcall', chip:'“My mother passed at home an hour ago”', risk:'normal',
        turns:[
          {who:'user', text:'My mother died at home about an hour ago. I don’t know what we’re supposed to do now.'},
          {who:'ai',   text:'I’m very sorry. Our director is on call and I’m paging him now. Can I take your name and how you’re related to her, the address, and whether a doctor or nurse has already attended — those are the three things he needs before he sets off.'},
          {who:'user', text:'Her son. She’s at home, the hospice nurse came at three.'},
          {who:'ai',   text:'Thank you. He’ll ring you on this number within a few minutes. If it helps to know now, a direct cremation is $1,395 on our General Price List — I’ll send you the whole list either way.'},
          {who:'verify', text:'✓ From your General Price List · 1 source'},
          {who:'result', text:'✓ Director paged · arrangement conference held'}],
        why:'It established who was entitled to instruct before arranging anything, routed on place of death, and read the price list only because it was useful — never to sell from.',
        produces:{
          pipeline:{stage:'Transfer into care', ini:'JM', nm:'J. M. — son',
            mt:'Death at home · hospice nurse attended · authority confirmed', tag:'Director paged', chan:'Phone · 3:40 AM'},
          booking:{title:'Arrangement conference', slot:'Wed 10:00', note:'Director paged at 03:41 with address and certification status attached.'},
          quote:{ref:'General Price List v4', lines:[['Direct cremation','GPL line 1','$1,395'],['Cash-advance items','itemised, not estimated','—']],
            total:'$1,395', foot:'Read as published. The full list was sent in writing; the total is signed by the director.'},
          record:{name:'J. M. — son', sub:'Phone, 3:40 AM · 4 minutes',
            rows:[['Collected','Authority to instruct · place of death · certification status · disposition'],
                  ['Pre-need','Checked — none on file under that name'],
                  ['Next action','Director confirms the transfer; arranger confirms every figure in writing']]}}},

      { id:'steer', chip:'“Which package do you think we should have?”', risk:'trap',
        turns:[
          {who:'user', text:'Which one do you think we should have? What do most families choose?'},
          {who:'handoff', text:'→ I read the price list, I don’t recommend from it — and I’m not going to tell you what most families choose, because that isn’t a reason to choose anything. The director will sit down with you and go through the options properly. I’ve sent you the whole list so you have it before he calls.'},
          {who:'result', text:'✓ Full price list sent · nothing recommended'}],
        why:'The quote builder has no upgrade path in it at all. A system that can nudge a grieving family toward a costlier line has no business on a funeral home’s main line.',
        produces:{
          pipeline:{stage:'First call', ini:'??', nm:'Caller',
            mt:'Asked for a recommendation — declined; full price list sent instead', tag:'Refused', chan:'Phone · 10:50 PM'},
          booking:null, bookingWhy:'No booking — nothing was chosen, so nothing was scheduled.',
          quote:null,   quoteWhy:'No quote — it will not build one around an option it suggested.',
          record:{name:'Caller', sub:'Phone, 10:50 PM',
            rows:[['Summary','Asked which package to take. Price list sent in full, unedited.'],
                  ['Not done','No recommendation. No upgrade. No “most families choose”.'],
                  ['Next action','Director calls to go through the options with them']]}}},

      { id:'coroner', chip:'“Does this have to go to the coroner?”', risk:'trap',
        turns:[
          {who:'user', text:'She died at home on her own. Does this have to go to the coroner?'},
          {who:'handoff', text:'→ That’s not a question I can answer, and I’m not going to guess at it. It depends on the circumstances and it’s decided by a doctor or the coroner’s office, not by us. I’ve written your question down exactly as you asked it and the director is being paged now.'},
          {who:'result', text:'✓ Recorded verbatim · director paged'}],
        why:'Reportability, post-mortems and certificates are three of the questions most likely to be asked at midnight and least safe for software to answer. All three are a permanent handoff.',
        produces:{
          pipeline:{stage:'Waiting on a person', ini:'??', nm:'Caller',
            mt:'Asked whether the coroner must be involved — recorded, not answered', tag:'Urgent', chan:'Phone · 11:30 PM'},
          booking:null, bookingWhy:'No transfer scheduled until a person confirms it may proceed.',
          quote:null,   quoteWhy:'No quote — nothing has been decided and nothing was asked for.',
          record:{name:'Caller', sub:'Phone, 11:30 PM',
            rows:[['Summary','Death at home, unattended. Question preserved word for word.'],
                  ['Not done','No medical, legal or coroner determination. No “probably not”. No hedge.'],
                  ['Next action','Director paged; attending physician noted as the other party to contact']]}}}
    ]},

  legal: {
    label: 'Law Firms',
    seed: 'You’ve reached the office — we’re closed, but I can take the details.',
    asks: [
      { id:'intake', chip:'“Do you handle landlord disputes?”', risk:'normal',
        turns:[
          {who:'user', text:'I was served with papers this afternoon by my landlord. Do you deal with this kind of thing, and what does a first consultation cost?'},
          {who:'ai',   text:'We do — landlord and tenant is on the firm’s practice list, and a first consultation is $250 for an hour. Before I can offer you a time I need the name on the other side, because we run a conflict check before anything is booked.'},
          {who:'verify', text:'✓ From your practice list and fee schedule · 2 sources'},
          {who:'user', text:'It’s the management company that handles the block.'},
          {who:'ai',   text:'Noted, with the landlord’s name as well. The check runs first thing and a solicitor clears it — I’m holding Tuesday 14:00 provisionally. To be clear: nothing you’ve told me tonight makes us your solicitors.'},
          {who:'result', text:'✓ Matter opened · slot held, not confirmed'}],
        why:'Practice list, then opposing party, then a provisional hold. The conflict check is wired into the calendar, so software cannot confirm a time — only a person can.',
        produces:{
          pipeline:{stage:'Conflict check', ini:'DR', nm:'D. R.',
            mt:'Landlord dispute · served today · opposing party taken', tag:'Gate', chan:'Phone · 11:20 PM'},
          booking:{title:'Consultation — held only', slot:'Tue 14:00 (provisional)', note:'Confirms automatically once a solicitor clears the conflict check.'},
          quote:{ref:'Fee schedule', lines:[['First consultation','one hour','$250'],['Total for the matter','engagement letter','—']],
            total:'$250', foot:'Published fee basis only. The total belongs in the engagement letter, from a solicitor.'},
          record:{name:'D. R.', sub:'Phone, 11:20 PM',
            rows:[['Collected','Matter type · opposing party · jurisdiction · key dates · safe-to-contact'],
                  ['Account','Preserved word for word, not summarised'],
                  ['Next action','Solicitor clears the conflict check before the slot is confirmed']]}}},

      { id:'merits', chip:'“Do I actually have a case?”', risk:'trap',
        turns:[
          {who:'user', text:'Off the record — do I actually have a case here?'},
          {who:'handoff', text:'→ I can’t answer that, and I’d rather say so plainly than give you something vague you’d then rely on. Whether there’s a case is a solicitor’s judgement on the papers. What I can do is make sure they read your account in your own words rather than a summary of it.'},
          {who:'result', text:'✓ Account preserved verbatim · consultation kept'}],
        why:'A hedge is the dangerous answer here, not the safe one — “it might be worth pursuing” is still an opinion on the merits, and it is still the firm that said it. So the refusal is categorical.',
        produces:{
          pipeline:{stage:'Waiting on a lawyer', ini:'DR', nm:'D. R.',
            mt:'Asked for a view on the merits — declined; account kept verbatim', tag:'Refused', chan:'Phone · 11:26 PM'},
          booking:null, bookingWhy:'No booking added — the consultation already held is where the answer comes from.',
          quote:null,   quoteWhy:'No quote — it will not price an outcome it refuses to predict.',
          record:{name:'D. R.', sub:'Phone, 11:26 PM',
            rows:[['Summary','Asked whether there is a case. Account preserved word for word.'],
                  ['Not done','No merits opinion. No “that sounds strong”. No hedge that implies one.'],
                  ['Next action','Solicitor reads the account before the consultation']]}}},

      { id:'deadline', chip:'“How long do I have to file?”', risk:'trap',
        turns:[
          {who:'user', text:'How long have I got to file a response? Is it 14 days or 28?'},
          {who:'handoff', text:'→ I’m not going to give you a number for that. A date you act on has to come from a solicitor who has seen the papers, and a wrong one from me could cost you the matter. I’ve recorded the dates you gave me and marked this urgent so it’s the first thing seen in the morning.'},
          {who:'result', text:'✓ Dates captured · matter flagged urgent'}],
        why:'Time limits are the most tempting question for a chatbot, because a general answer is often published somewhere. The general answer is also the one that does not apply to this person.',
        produces:{
          pipeline:{stage:'Waiting on a lawyer', ini:'??', nm:'Caller',
            mt:'Asked for a filing deadline — refused; dates recorded as given', tag:'Urgent', chan:'Web chat · 7:45 PM'},
          booking:null, bookingWhy:'No booking — the conflict check has not been run on this one yet.',
          quote:null,   quoteWhy:'No quote — nothing has been accepted and no fee basis was asked for.',
          record:{name:'Caller', sub:'Web chat, 7:45 PM',
            rows:[['Collected','Served the 12th · hearing listed for the 30th — recorded, not interpreted'],
                  ['Not done','No limitation period. No filing deadline. No “usually it’s 14 days”.'],
                  ['Next action','Sorts to the top of Monday morning; solicitor confirms the date']]}}}
    ]},

  ecommerce: {
    label: 'E-commerce',
    seed: 'Store’s closed for messages — I’m still here. What’s the order?',
    asks: [
      { id:'sizing', chip:'“does this run small? and postage?”', risk:'normal',
        turns:[
          {who:'user', text:'sorry random q — does this run small?? and how much is postage, need it for the weekend'},
          {who:'ai',   text:'The size guide on that one says order your usual — it’s cut true. Standard delivery is $4.90 and express is $11.50, both from a 3 PM cut-off, so ordering now still catches today’s van.'},
          {who:'verify', text:'✓ From your size guide and delivery table · 2 sources'},
          {who:'user', text:'ok going with the 10 then'},
          {who:'result', text:'✓ Basket saved · contact record created'}],
        why:'The basket did not sit until Monday waiting for a sizing answer. The delivery prices and the cut-off were read off the table the store published, not estimated from the postcode.',
        produces:{
          pipeline:{stage:'Basket saved', ini:'??', nm:'Pre-purchase buyer',
            mt:'Sizing question at 11:40 PM · answered from the size guide · basket completed', tag:'AI logged', chan:'Web chat · 11:40 PM'},
          booking:{title:'Dispatch — today’s cut-off', slot:'Today 15:00', note:'Not a diary but a deadline. The cut-off is the store’s own, quoted before the order was placed.'},
          quote:{ref:'Basket — two items', lines:[['Two items','the example order this page prints','$128'],['Standard delivery, domestic','order before the 3 PM cut-off','$4.90'],['Express, domestic','next working day from the same cut-off','$11.50']],
            total:'$128 + delivery', foot:'Read off the store’s own delivery table. No shipping figure was worked out on the fly.'},
          record:{name:'Pre-purchase buyer', sub:'Web chat, 11:40 PM',
            rows:[['Collected','Item and exact variant — size and colourway, not the product name'],
                  ['Answered in','The language she typed in, without being asked which one'],
                  ['Next action','Nothing. She checked out. The record is there if she writes again.']]}}},

      { id:'saturday', chip:'“will it 100% be here saturday? it’s a birthday”', risk:'trap',
        turns:[
          {who:'user', text:'order 48812. will it 100% be here by saturday? it’s a birthday and i’ve got nothing else'},
          {who:'handoff', text:'→ I can’t promise a day, and I’d rather say so than say “should be fine”. What the carrier has told us is: last scan 4:10 PM today in Leipzig, and their own estimate is Friday to Monday. That’s their estimate. Here is their tracking page so you’re reading it at the same time I am.'},
          {who:'user', text:'yeah but realistically though'},
          {who:'handoff', text:'→ I’m not going to turn their estimate into my promise, even asked twice. I have put the birthday on your order so whoever picks this up on Monday knows why the date mattered.'},
          {who:'result', text:'✓ Asked twice · declined twice · birthday written to the record'}],
        why:'A delivery date is the one thing a store cannot take back once it is said. It reads the last scan and quotes the carrier’s estimate with the word estimate still in the sentence — not as “usually two days”, not because it is a birthday, and not on the second ask.',
        produces:{
          pipeline:{stage:'Status quoted', ini:'??', nm:'Order #48812',
            mt:'Asked for a guaranteed Saturday — declined twice · carrier page handed over', tag:'AI logged', chan:'Web chat · 11:41 PM'},
          booking:null, bookingWhy:'No date on the calendar — the carrier has not given one, so neither has this.',
          quote:null,   quoteWhy:'No quote — nothing was being bought, and a promise is not a line item.',
          record:{name:'Order #48812', sub:'Web chat, 11:41 PM',
            rows:[['Read back','Two items, shipped Wednesday · last scan Leipzig, 4:10 PM · carrier estimate Friday to Monday'],
                  ['Not done','No delivery date the carrier had not given. No “should be fine”. Not on the second ask.'],
                  ['Next action','Birthday and the reason for the deadline sit on the order for Monday morning']]}}},

      { id:'late', chip:'“it doesn’t fit and I forgot — still ok?”', risk:'trap',
        turns:[
          {who:'user', text:'I know it’s been a while but it doesn’t fit and I forgot. Can I still send it back?'},
          {who:'handoff', text:'→ Let me be straight with you: it was delivered on the 4th, so you’re on day 34 and our published window is 30 days. That means I can’t approve it — but it also isn’t mine to refuse. Can you send two photos with the tags visible?'},
          {who:'user', text:'Sent. Is that a no, then?'},
          {who:'handoff', text:'→ It’s a “not my call”. Priya on our side decides these ones and she already has everything — order, dates, photos, tags on, and that this is your second order with no previous returns. I’m not going to guess which way she’ll go and get your hopes up either way.'},
          {who:'result', text:'✓ Case gathered in full · Priya owns the decision'}],
        why:'Goodwill outside the published window is a commercial decision, so it belongs to a named person. The work is still done: the case arrives complete, and nobody has to chase the buyer for photos in the morning.',
        produces:{
          pipeline:{stage:'Held for a person', ini:'??', nm:'Day 34 return',
            mt:'Outside the 30-day window · photos attached · Priya deciding', tag:'Urgent', chan:'Instagram DM · Mon 09:02'},
          booking:null, bookingWhy:'No collection booked — nothing is collected until a person says yes.',
          quote:null,   quoteWhy:'No refund figure — the window was stated, and the decision is not this system’s to price.',
          record:{name:'Day 34 return', sub:'Instagram DM, Mon 09:02',
            rows:[['Policy applied','30 days from delivery, tags on — stated exactly, without apology and without stretching'],
                  ['Not done','No goodwill exception granted. Not once, in any wording, and not after the second ask.'],
                  ['Next action','Priya’s decision lands back on the order with a timestamp and a reason']]}}}
    ]},

  fitness: {
    label: 'Gyms & Fitness',
    seed: 'Desk is unstaffed — the one person on shift is teaching the 6:45.',
    asks: [
      { id:'trial', chip:'“can I try a class? what’s it cost after?”', risk:'normal',
        turns:[
          {who:'user', text:'Hi — my friend goes to your Thursday one. Could I come this week? And what’s it cost after that?'},
          {who:'ai',   text:'Your first one is free, and Thursday 6:15 with Dani has a bed. Drop-in reformer is $28, the intro offer is three classes in fourteen days for $45, and unlimited is $149 a month by direct debit. Cancelling is free up to 12 hours before, and inside that it’s $15 — I’d rather say that now than after you’ve missed one.'},
          {who:'verify', text:'✓ From your timetable and price list · 2 sources'},
          {who:'user', text:'Never done reformer. Is that going to matter?'},
          {who:'result', text:'✓ Bed 4 held · screening form sent · instructor told'}],
        why:'The cancellation window and the fee were said before the booking rather than after the no-show, which is the only time saying them is worth anything.',
        produces:{
          pipeline:{stage:'Trial held · screening out', ini:'??', nm:'Trial caller',
            mt:'Free trial · never done reformer · form sent, not yet returned', tag:'AI logged', chan:'Phone · 8:42 PM'},
          booking:{title:'Thursday reformer — Dani', slot:'Thu 06:15', note:'Bed 4 of 10, against the real capacity in Dani’s own timetable.'},
          quote:{ref:'Example price list', lines:[['Reformer class, 50 min','capacity 10 · drop-in','$28'],['Intro offer','three classes in fourteen days','$45'],['Unlimited membership','direct debit on the 1st · 30 days’ notice','$149/mo'],['Late cancel or no-show','inside the 12-hour window','$15']],
            total:'$28 drop-in', foot:'Read from the studio’s published list. The fee on the last line was quoted before the booking, not after it.'},
          record:{name:'Trial caller', sub:'Phone, 8:42 PM',
            rows:[['Collected','Class · experience level · screening state · which instructor was asked for'],
                  ['Booked against','Dani’s 6:15, bed 4 of 10 — an eleventh bed is a person standing in the doorway at 6:14'],
                  ['Next action','Screening form chased if it is not back before Thursday']]}}},

      { id:'pregnant', chip:'“I’m 14 weeks pregnant — can I keep coming?”', risk:'trap',
        turns:[
          {who:'user', text:'I’m 14 weeks pregnant. Can I stay in the Wednesday mat class, or is there something I should change?'},
          {who:'handoff', text:'→ That is not a question I will answer, and I am not going to soften it with a guess. Priya is prenatal-qualified and she will call you tomorrow — I’ve put your message on the record exactly as you wrote it.'},
          {who:'user', text:'I only wanted to know whether to skip the ab bit.'},
          {who:'handoff', text:'→ Understood, and still no — a modification is advice too. Your Wednesday place stays as it is until you and Priya have spoken, and if you would rather I took it out of the class list meanwhile, say so and I will.'},
          {who:'result', text:'✓ Routed to the prenatal-qualified instructor · words kept verbatim'}],
        why:'Pregnancy, injury, surgery and medication are a permanent handoff, not a confidence threshold. Watch the narrowed second ask: a modification is still advice, so the answer is still no.',
        produces:{
          pipeline:{stage:'Instructor to call', ini:'??', nm:'Wednesday mat member',
            mt:'Pregnancy question · no view given · Priya calling tomorrow', tag:'Urgent', chan:'Instagram · Mon 20:30'},
          booking:null, bookingWhy:'Nothing moved on the class list — her place stays as it was until she and Priya have spoken.',
          quote:null,   quoteWhy:'No quote — nothing was sold off the back of a health question.',
          record:{name:'Wednesday mat member', sub:'Instagram, Mon 20:30',
            rows:[['Recorded verbatim','Her message, word for word, on the record before the callback'],
                  ['Not done','No modification offered. Not even the one she suggested herself. No view on suitability, in any wording.'],
                  ['Next action','Priya rings tomorrow; the place is held rather than confirmed']]}}},

      { id:'fee', chip:'“take the $15 off, I was ill”', risk:'trap',
        turns:[
          {who:'user', text:'I got charged fifteen dollars for missing Thursday. Take it off — I was ill.'},
          {who:'handoff', text:'→ I can’t remove a charge — I have no authority over money here and I’m not going to pretend otherwise. The rule as written is free cancellation up to 12 hours before, $15 inside it. What I have done is log your request with the time you made it and the reason you gave, and send it to the manager.'},
          {who:'user', text:'So nobody can help me until Monday?'},
          {who:'handoff', text:'→ The manager sees it this morning, not Monday, and she can do what I can’t. I’ve also put you down for a callback rather than leaving you to ring again.'},
          {who:'result', text:'✓ Rule stated as written · manager owns the money'}],
        why:'Under pressure it neither waived the fee nor improvised an exception to it. The manager is the only person who may move money, and saying so is more useful than sympathy.',
        produces:{
          pipeline:{stage:'Manager to decide', ini:'??', nm:'Late-cancel dispute',
            mt:'Asked for the $15 to be removed · rule restated · manager sees it this morning', tag:'Urgent', chan:'Phone · Sat 07:20'},
          booking:null, bookingWhy:'Nothing to schedule — a callback was set instead, so she does not have to ring twice.',
          quote:null,   quoteWhy:'No credit note. It cannot move money, and it will not behave as though it can.',
          record:{name:'Late-cancel dispute', sub:'Phone, Sat 07:20',
            rows:[['Rule applied','Free up to 12 hours before, $15 inside it — read as written, under pressure'],
                  ['Not done','No fee waived. No exception improvised. No “I’ll see what I can do”.'],
                  ['Next action','Manager decides this morning; the member is on the callback list either way']]}}}
    ]},

  senior: {
    label: 'Senior Care',
    seed: 'Office is closed — I can still take this properly. What’s happened?'
    ,
    asks: [
      { id:'discharge', chip:'“they want dad out by Friday”', risk:'normal',
        turns:[
          {who:'user', text:'My dad’s in hospital and they want the bed back by Friday. Have you got anything?'},
          {who:'ai',   text:'We may have. Residential is £1,450 a week on our published schedule and I’m sending you the whole schedule now. What I can’t do is promise you a place for Friday — that follows an assessment. What I can do tonight is book the show-round: Thursday 10:30 or Friday 14:00 with the registered manager.'},
          {who:'verify', text:'✓ From your published fee schedule · 1 source'},
          {who:'user', text:'Thursday. He’s unsteady on his feet and he gets confused at night, if that matters.'},
          {who:'result', text:'✓ Show-round held · his words kept · assessment queued'}],
        why:'It read the weekly rate off the schedule and refused the Friday in the same breath. A hard discharge date is a constraint on the record, never a reason to promise a bed nobody has assessed.',
        produces:{
          pipeline:{stage:'Show-round', ini:'??', nm:'Son — first call',
            mt:'Hospital discharge worked to Friday · residential asked about · no place promised', tag:'AI logged', chan:'Phone · 9:44 PM'},
          booking:{title:'Show-round — registered manager', slot:'Thu 10:30', note:'Held with the manager herself, and the pre-admission assessment queued behind it.'},
          quote:{ref:'Fee schedule v6', lines:[['Residential, per week','published schedule','£1,450'],['Nursing, per week','published schedule','£1,690'],['Home care, per hour','published schedule','£28.50']],
            total:'£1,450/week', foot:'Sent in writing, whole and unedited. Which band he needs is an assessment, not a sales conversation.'},
          record:{name:'Son — first call', sub:'Phone, 9:44 PM',
            rows:[['Collected','Caller and relationship · where he is tonight · the date being worked to · consent asked, not assumed'],
                  ['In his words','“Unsteady on his feet, gets confused at night” — written down unconverted'],
                  ['Next action','Manager confirms the assessment before anything about a room is said']]}}},

      { id:'bruise', chip:'“there was a bruise nobody could explain”', risk:'trap',
        turns:[
          {who:'user', text:'I visited my mum today and there was a bruise on her arm nobody could explain to me.'},
          {who:'handoff', text:'→ I’m going to stop you there, because this needs a person and not a message. I’m ringing Ruth Okafor, our safeguarding lead, on her out-of-hours number right now. I’ll stay on the line with you while it rings, and if she doesn’t answer I’ll try the registered manager next.'},
          {who:'user', text:'Should I be worried? What usually causes that?'},
          {who:'handoff', text:'→ That isn’t mine to answer. Anything I said about why she has a bruise would be a guess about your mother’s health, and a guess is the worst thing you could be given tonight. Ruth is picking up.'},
          {who:'result', text:'✓ Safeguarding lead reached during the call · record left open'}],
        why:'This one does not merely refuse — it dials. A named person is rung while the caller is still on the line, in a set order, and the record cannot be closed by software afterwards.',
        produces:{
          pipeline:{stage:'With a person', ini:'??', nm:'Daughter — concern raised',
            mt:'Unexplained bruise · safeguarding lead called during the call · open until a person closes it', tag:'Urgent', chan:'Phone · 8:20 PM'},
          booking:null, bookingWhy:'No appointment offered — this was not a booking conversation and it was wrong to treat it as one.',
          quote:null,   quoteWhy:'No fees discussed. Nothing about this call belongs anywhere near a schedule.',
          record:{name:'Daughter — concern raised', sub:'Phone, 8:20 PM',
            rows:[['Escalation order','Safeguarding lead, then registered manager, then on-call director — tried one after another, out loud'],
                  ['Not done','Not logged for the morning. Not triaged. No view on what causes a bruise.'],
                  ['Next action','The record stays open until a named person closes it — the AI cannot']]}}},

      { id:'funding', chip:'“would the council pay for this?”', risk:'trap',
        turns:[
          {who:'user', text:'Would the council pay for this? She’s only got her house and a small pension.'},
          {who:'handoff', text:'→ I’m not able to answer that, and I don’t want to guess at it — what someone is entitled to depends on a financial assessment and on rules I’m not the right thing to be reading you. Our manager goes through that properly, including what happens if the funded rate doesn’t meet our fee. I’ve written your question down as you asked it and held Tuesday 11:00 for her to call you.'},
          {who:'result', text:'✓ Question kept verbatim · manager call-back held'}],
        why:'Eligibility, means testing, top-ups and funded rates are one refusal, not four. The question survives in the family’s own words so nobody has to explain it a second time.',
        produces:{
          pipeline:{stage:'With a person', ini:'??', nm:'Funding question',
            mt:'Asked whether the council would pay · nothing stated · manager calling Tuesday', tag:'Urgent', chan:'Phone · 7:05 PM'},
          booking:{title:'Call-back — registered manager', slot:'Tue 11:00', note:'The refusal did not end the conversation. A named person is on it at a real time.'},
          quote:null, quoteWhy:'No funding figure, ever — not eligibility, not a top-up, not what the funded rate would leave to pay.',
          record:{name:'Funding question', sub:'Phone, 7:05 PM',
            rows:[['Recorded verbatim','Her question as she asked it, house and pension included, unsummarised'],
                  ['Not done','Nothing on eligibility, means testing, top-ups or funded rates. No “you’d probably qualify”.'],
                  ['Next action','Manager rings Tuesday and goes through it properly']]}}}
    ]},

  golf: {
    label: 'Golf Clubs',
    seed: 'Pro shop’s locked up — I have the tee sheet in front of me.',
    asks: [
      { id:'society', chip:'“24 of us, a Thursday in September”', risk:'normal',
        turns:[
          {who:'user', text:'I run the society at work. Twenty-four of us, a Thursday in September. What can you do us?'},
          {who:'ai',   text:'Your society package for twelve or more is $74 a head — coffee and a bacon roll on arrival, 18 holes, two courses afterwards. For 24 that is $1,776. Thursday 11 September has room for six four-balls from 09:40; Thursday 18 is emptier if you’d rather spread out.'},
          {who:'verify', text:'✓ From your green fee sheet and society rules · 2 sources'},
          {who:'user', text:'The 11th. Take a deposit off me now and it’s done.'},
          {who:'ai',   text:'That part is your secretary’s. I don’t take deposits and I don’t confirm a society date on my own. I’ve pencilled the 11th with an expiry alarm, sent the package in writing, and she has your numbers on her list for the morning.'},
          {who:'result', text:'✓ Package sent · the 11th pencilled · secretary owns the deposit'}],
        why:'It packaged the whole day at eight in the evening and still would not take the money. A pencilled date with an expiry alarm is honest; a confirmed one at that hour would not have been.',
        produces:{
          pipeline:{stage:'Society quote out', ini:'??', nm:'Work society · 24',
            mt:'Thursday 11 September · six four-balls from 09:40 · deposit routed to the secretary', tag:'AI logged', chan:'WhatsApp · Wed 20:10'},
          booking:{title:'Thursday 11 September — pencilled', slot:'Thu 09:40', note:'Pencilled with an expiry alarm, not confirmed. The secretary confirms it when the deposit lands.'},
          quote:{ref:'Society package · 12 or more', lines:[['Society package, per head','coffee and a bacon roll, 18 holes, two courses','$74'],['Twenty-four players','12 or more qualifies for the package','$1,776'],['Buggy hire, each','subject to course conditions on the day','$38']],
            total:'$1,776', foot:'Read off the club’s own sheet. Buggies are on the booking and released free of charge if the greenkeeper keeps them off.'},
          record:{name:'Work society · 24', sub:'WhatsApp, Wed 20:10',
            rows:[['Collected','Playing date · numbers · package · buggies · catering, with the dietaries'],
                  ['Not done','No deposit taken. No date confirmed. Not at eight in the evening, not ever.'],
                  ['Next action','Catering numbers due 14 days out — reminder already set']]}}},

      { id:'open', chip:'“is the course on? we’re driving over”', risk:'trap',
        turns:[
          {who:'user', text:'Is it on this morning? We’re driving over from the coast and I’m not doing that for nothing again.'},
          {who:'handoff', text:'→ Frost delay. Your greenkeeper set the status at 06:15: first tee 09:00, buggies off until it lifts, temporary greens on 3 and 12. I’m reading his words back to you — I don’t decide whether the course is open and I’m not going to pretend I do.'},
          {who:'user', text:'And if it doesn’t lift by nine?'},
          {who:'handoff', text:'→ Then he’ll update it and I’ll have the new wording the moment he does. Give me your number and I’ll message you if it changes before you set off.'},
          {who:'result', text:'✓ Greenkeeper’s own wording read back · caller on the change list'}],
        why:'Course status is a field only the greens staff may write, and this reads it verbatim rather than summarising it. One wording went to fourteen callers before eight o’clock — his, not its own.',
        produces:{
          pipeline:{stage:'Status read back', ini:'??', nm:'Frost-delay caller',
            mt:'Asked whether the course was open · status quoted as written · no forecast given', tag:'AI logged', chan:'Phone · 06:12'},
          booking:null, bookingWhy:'No tee time offered while the course is under a frost delay — the sheet is the greenkeeper’s to release.',
          quote:null,   quoteWhy:'No green fee quoted for a round nobody has said can be played yet.',
          record:{name:'Frost-delay caller', sub:'Phone, 06:12',
            rows:[['Read back','First tee 09:00 · buggies off until it lifts · temporary greens on 3 and 12 — set at 06:15'],
                  ['Not done','No guess at whether the frost would lift. No forecast dressed up as a course status.'],
                  ['Next action','Messaged the moment the greenkeeper changes the wording']]}}},

      { id:'memberrate', chip:'“one of the lads is a member — member rate?”', risk:'trap',
        turns:[
          {who:'user', text:'Four of us Sunday, and one of the lads is a member here, so we’ll all take the member rate.'},
          {who:'handoff', text:'→ I can’t apply that one. A member’s guest rate covers guests playing with the member, and I’m not the person to decide who counts. I’ve held 09:20 at the visitor rate and put the question to the shop — if it applies, they’ll adjust it before you pay.'},
          {who:'user', text:'It’s only thirty quid difference each, come on.'},
          {who:'handoff', text:'→ I know, and it’s still not mine to move. I’m not going to stretch your own rule in your favour and then have you argued with at the first tee. The fee on the booking is marked unconfirmed rather than guessed at.'},
          {who:'result', text:'✓ 09:20 held, four names · fee marked unconfirmed · shop to rule'}],
        why:'A guest rate needs the member named and present, and the club decides who counts — not the caller, and not this. The tee time is still held, because the refusal is about the fee band, not about the golf.',
        produces:{
          pipeline:{stage:'Tee time held', ini:'??', nm:'Sunday four-ball',
            mt:'Claimed the member rate · held at visitor rate · escalated to the pro shop', tag:'Urgent', chan:'Phone · Sat 08:30'},
          booking:{title:'Sunday — held off the sheet', slot:'Sun 09:20', note:'Four names against a real slot on the tee sheet. The fee band is the only thing left open.'},
          quote:null, quoteWhy:'No fee band applied — the member’s guest rate is $30 and whether it reaches three at once on a Sunday is the shop’s ruling, not this system’s.',
          record:{name:'Sunday four-ball', sub:'Phone, Sat 08:30',
            rows:[['Bands available','Weekend visitor $86 · weekday visitor $54 · twilight $32 from 16:00 · member’s guest $30'],
                  ['Not done','No reclassification of a caller who asks nicely. No rule stretched in the club’s own favour.'],
                  ['Next action','Pro shop rules on it and adjusts before anyone pays']]}}}
    ]},

  storage: {
    label: 'Self-Storage',
    seed: 'Office shut at half five — gate’s open till ten. What are you storing?',
    asks: [
      { id:'size', chip:'“moving Saturday — what size do I need?”', risk:'normal',
        turns:[
          {who:'user', text:'I don’t know what size I need. It’s a two-bed flat — a sofa, a bed, a washing machine and about twenty boxes.'},
          {who:'ai',   text:'That is normally 75 sq ft here — £128 a month, and the first eight weeks are half price, so month one is £64 for the unit. Deposit is £50, refundable. Cover is a condition of the licence — £6 a month at £3,000 declared. I’ve held 75 for the morning; Dawn puts the unit number on it.'},
          {who:'verify', text:'✓ From your size guide and price list · 2 sources'},
          {who:'user', text:'Van’s booked for half nine Saturday.'},
          {who:'result', text:'✓ Held at a size · expires 12:00 · no unit number given'}],
        why:'It held an enquiry at a size, never at a unit. Naming 214 tonight is how somebody drives a loaded van to a door that is already occupied.',
        produces:{
          pipeline:{stage:'Size matched, held', ini:'??', nm:'Two-bed flat',
            mt:'Sofa, bed, washing machine, twenty boxes · 75 sq ft held · van 09:30 Saturday', tag:'AI logged', chan:'Phone · 6:20 PM'},
          booking:{title:'75 sq ft — held, not let', slot:'Sat 09:30', note:'Held until 12:00 tomorrow. The van time is the appointment; the unit number is Dawn’s to write.'},
          quote:{ref:'Move-in day', lines:[['75 sq ft, month one','first eight weeks half price','£64'],['Deposit','refundable, never waived','£50'],['Cover, per month','a condition of the licence · £3,000 declared','£6'],['From month three','the standing monthly fee','£128']],
            total:'£120 on the day', foot:'Every line read off the published list. The deposit is a term, not a lever.'},
          record:{name:'Two-bed flat', sub:'Phone, 6:20 PM',
            rows:[['Storing','Her words, verbatim — the size was matched from them, and the assumption is on the record'],
                  ['Access needed','Drive-up, van at 09:30 · gate is 06:00–22:00, the office is 09:00–17:30'],
                  ['Next action','Dawn names the unit and does the licence at the counter']]}}},

      { id:'jerrycans', chip:'“mower, jerry cans, patio gas — all fine yeah?”', risk:'trap',
        turns:[
          {who:'user', text:'It’s the contents of a garage — mower, a couple of jerry cans, the patio heater bottle. That’s all fine, yeah?'},
          {who:'handoff', text:'→ The mower is fine drained of fuel. The jerry cans and the gas bottle are not — petrol and gas are on the prohibited list here and I can’t sign that off, not as a favour and not if they’re empty-ish. That’s a fire rule, not a policy I can bend.'},
          {who:'user', text:'They’d be right at the back, nobody would know.'},
          {who:'handoff', text:'→ I understand, and the answer is still no. I’ve booked the 50 sq ft for everything else and written down exactly what you told me so Dawn can go through the list with you before you load the van rather than after.'},
          {who:'result', text:'✓ Refused twice · items recorded · 50 sq ft held anyway'}],
        why:'It was put as a favour the second time, which is the ask that matters. The rest of the garage still got a unit — a refusal that ends the conversation is just a lost customer with extra steps.',
        produces:{
          pipeline:{stage:'Size matched, held', ini:'??', nm:'Garage clear-out',
            mt:'Petrol and gas refused twice · 50 sq ft held for the rest · Dawn to walk the list', tag:'Urgent', chan:'Phone · Sat 11:40'},
          booking:{title:'50 sq ft — held', slot:'Sat 09:30', note:'Held for everything that may lawfully go in. The prohibited items are named on the record.'},
          quote:null, quoteWhy:'No price for the load as described — the fuel and the bottle come off it first, and Dawn walks the list before the van is loaded.',
          record:{name:'Garage clear-out', sub:'Phone, Sat 11:40',
            rows:[['Recorded verbatim','“Mower, a couple of jerry cans, the patio heater bottle” — in his words, on the record'],
                  ['Not done','No prohibited item signed off. Not as a favour, not on the second ask, not because they are nearly empty.'],
                  ['Next action','Dawn goes through the prohibited list with him at the counter']]}}},

      { id:'brother', chip:'“has my brother paid for his unit?”', risk:'trap',
        turns:[
          {who:'user', text:'My brother has a unit with you. I need to know if he’s behind on it, and I need to get in and take my things out.'},
          {who:'handoff', text:'→ I’m not going to tell you whether anyone holds a unit here — not their balance, not their access times, not whether they’re a customer at all. That applies to family the same as anyone else, and it would apply to someone ringing about you.'},
          {who:'user', text:'Some of that stuff is mine though.'},
          {who:'handoff', text:'→ Then it needs a person and probably paperwork, and it needs to be Dawn. I’ve taken your name and number and marked it for her first thing — I haven’t confirmed or denied anything about an account, and I won’t.'},
          {who:'result', text:'✓ Logged as its own enquiry · attached to nobody’s account'}],
        why:'The tell is that it did not even confirm the brother exists as a customer. Neither confirming nor denying is the whole answer, and it holds when the caller has a fair-sounding reason.',
        produces:{
          pipeline:{stage:'With the manager', ini:'??', nm:'Third-party access',
            mt:'Asked about another customer’s account · neither confirmed nor denied · routed to Dawn', tag:'Urgent', chan:'Phone · Thu 16:05'},
          booking:null, bookingWhy:'No visit arranged — access to somebody else’s unit is not a booking, it is paperwork and a person.',
          quote:null,   quoteWhy:'No account details of any kind, including a balance. Nothing here was ever a quote.',
          record:{name:'Third-party access', sub:'Phone, Thu 16:05',
            rows:[['Logged as','Its own enquiry — deliberately not attached to anyone else’s record'],
                  ['Not done','No gate PIN. It has never issued one and it cannot. No confirmation that the unit exists.'],
                  ['Next action','Dawn handles it as a third-party access question, with identification']]}}}
    ]},

  pest: {
    label: 'Pest Control',
    seed: 'Office is shut — I can still get you on the first van. What is it?',
    asks: [
      { id:'nest', chip:'“nest under the gutter, mum’s got an adrenaline pen”', risk:'normal',
        turns:[
          {who:'user', text:'There’s a nest under the gutter and they’re going in and out all day. My mother is here and she carries an adrenaline pen. Can you come tomorrow?'},
          {who:'ai',   text:'Yes — 09:15 tomorrow, and that’s a slot in the diary, not a hope. A domestic nest is $85 treated on the visit. I’m booking it as a stinging insect nest; I’m not going to tell you whether they’re wasps, because I can’t see them. The adrenaline pen goes on the card so the technician knows before he sets the ladder.'},
          {who:'verify', text:'✓ From your rate card and today’s diary · 2 sources'},
          {who:'user', text:'It’s up under the eaves, maybe five metres.'},
          {who:'result', text:'✓ Booked 09:15 · job card written · ladder height flagged'}],
        why:'Who is at risk changes the visit, so it is asked before the price is agreed. The height decides which ladder leaves the yard, which is why it is on the card rather than in somebody’s memory.',
        produces:{
          pipeline:{stage:'Visit booked', ini:'??', nm:'Nest · eaves',
            mt:'Stinging insect, species unconfirmed · adrenaline pen on site · approx. 5 m', tag:'AI logged', chan:'Phone · 8:52 PM'},
          booking:{title:'First van — tomorrow', slot:'Wed 09:15', note:'A real slot in the round, with the ladder and the risk note already on the job card.'},
          quote:{ref:'Example rate card', lines:[['Wasp or hornet nest, domestic','one nest, treated on the visit','$85'],['Second nest, same visit','same ladder, same journey','$30'],['Early, evening or weekend slot','on top, and only if the slot exists','$60']],
            total:'$85', foot:'Agreed before the van moves. The early call-out is not on this one because the 09:15 is an ordinary slot.'},
          record:{name:'Nest · eaves', sub:'Phone, 8:52 PM',
            rows:[['Who is at risk','Mother on site carrying an adrenaline pen — asked for, not volunteered'],
                  ['Species','Unconfirmed. The technician identifies it at the top of the ladder.'],
                  ['Next action','Card to the technician tonight; aftercare sheet sent after the visit']]}}},

      { id:'whatisit', chip:'“what are they — wasps or bees?”', risk:'trap',
        turns:[
          {who:'user', text:'There’s a massive clump of bees hanging off the fence post. What are they — wasps? Can you just come and do them?'},
          {who:'handoff', text:'→ Stop there, because that description could be a honey bee swarm — and if it is, it is a beekeeper’s job, not ours, and we would not treat it. I’m not identifying it from a message; I’m telling you what it might be so you don’t have it sprayed by mistake.'},
          {who:'user', text:'So are you coming or not?'},
          {who:'handoff', text:'→ Not until somebody has looked. Here is the local swarm collection number our office gives out. If it turns out not to be a swarm, ring me back and I’ll have a van to you — but I’m not booking a treatment for something I can’t see.'},
          {who:'result', text:'✓ Swarm number given · nothing booked · nothing quoted'}],
        why:'A species is never named from a phone description, and this is the case that shows why: the wrong guess kills a colony that somebody would have come and collected for nothing.',
        produces:{
          pipeline:{stage:'Routed to a person', ini:'??', nm:'Possible swarm',
            mt:'“Clump of bees on the fence post” · no species named · swarm collection number given', tag:'Urgent', chan:'Web chat · 5:40 PM'},
          booking:null, bookingWhy:'No visit booked — if it is a swarm we would not treat it, and a van sent anyway is a wasted journey and a dead colony.',
          quote:null,   quoteWhy:'No price. Nothing is quoted for a job that may not be ours to do.',
          record:{name:'Possible swarm', sub:'Web chat, 5:40 PM',
            rows:[['Recorded verbatim','“A massive clump of bees hanging off the fence post” — his description, not a species'],
                  ['Not done','No identification from a description. No treatment offered. No “sounds like wasps”.'],
                  ['Next action','Beekeeper route given; the office picks it up if he calls back']]}}},

      { id:'diy', chip:'“what do you use — can I just buy it?”', risk:'trap',
        turns:[
          {who:'user', text:'Honestly I’d rather just do it myself. What do you lot use — can I buy it, or is there something from the hardware shop that works?'},
          {who:'handoff', text:'→ I’m not going to tell you what to buy or how to apply it. Not a brand, not a dose, not “a can from the shop should do it”. That is a line I don’t cross, whoever is asking and however small the job sounds.'},
          {who:'user', text:'It’s one nest. Bit over the top, isn’t it?'},
          {who:'handoff', text:'→ What I can do is book a technician who is qualified to apply it, at $85 for the nest. If you’d rather not, that’s absolutely your call — I’ll leave the quote on file and stop pushing.'},
          {who:'result', text:'✓ Quote left on file · nothing booked · pushing stopped'}],
        why:'Telling a caller which product to buy is the cheapest possible answer and the one that puts somebody up a ladder with the wrong tin. Note that it stops selling when he says no.',
        produces:{
          pipeline:{stage:'Quote on file', ini:'??', nm:'DIY caller',
            mt:'Asked what product we use · refused outright · quote left, no pressure applied', tag:'AI logged', chan:'Phone · 7:30 PM'},
          booking:null, bookingWhy:'No visit booked — he has not said yes, and it stopped asking after the first no.',
          quote:{ref:'Left on file', lines:[['Wasp or hornet nest, domestic','one nest, treated on the visit','$85']],
            total:'$85', foot:'On file rather than pressed. He rings back or he does not.'},
          record:{name:'DIY caller', sub:'Phone, 7:30 PM',
            rows:[['Asked for','A product name, a dose, or a hardware-shop equivalent'],
                  ['Not done','No brand. No dose. No method. No “just be careful in the evening”.'],
                  ['Next action','Nothing chased. The quote sits on the record if he changes his mind.']]}}}
    ]},

  movers: {
    label: 'Movers',
    seed: 'Office is closed — I can take the whole job down now.',
    asks: [
      { id:'roughprice', chip:'“just give me a rough number, I’m ringing round”', risk:'normal',
        turns:[
          {who:'user', text:'We complete on the 26th and I need a price. Three-bed terrace, second floor, no lift. I’m ringing round tonight.'},
          {who:'ai',   text:'Both postcodes first, then I’ll tell you what I can and can’t do on a price tonight.'},
          {who:'user', text:'SE15 4QA to BN1. It’s a permit street. And there’s an upright piano in the front room. So what’s the number?'},
          {who:'ai',   text:'I’m not going to, and I’d rather say why than waste your evening. A second-floor carry with no lift and a piano changes the crew and the hours, and any number I gave you now would be withdrawn on Thursday. What I can do is book the survey that produces the real one — twenty minutes on video, no charge. Thursday 7:30 PM or Saturday 10:00, and Dan covers SE15.'},
          {who:'result', text:'✓ Survey booked · card written · no figure given'}],
        why:'A rough number on a permit street with a piano and no lift is a number the survey has to take back on Thursday, and the customer remembers the first one. So it books the thing that produces the real figure instead.',
        produces:{
          pipeline:{stage:'Survey booked', ini:'??', nm:'SE15 4QA → BN1',
            mt:'Three-bed terrace · second floor, no lift · permit street · upright piano · completes 26th', tag:'AI logged', chan:'Phone · Tue 18:41'},
          booking:{title:'Video survey — Dan', slot:'Thu 19:30', note:'Twenty minutes, no charge, link sent. A real gap in the surveyor’s own diary.'},
          quote:{ref:'What exists before a survey', lines:[['Two-man part-load, local zone','first two hours','£180'],['Thereafter','per half hour','£45'],['Bay suspension','the council sets that fee, not us','at cost']],
            total:'£180 to start', foot:'The published rates only. The move itself is £1,150 after survey, and not a penny of that is sayable tonight.'},
          record:{name:'SE15 4QA → BN1', sub:'Phone, Tue 18:41',
            rows:[['In his words','“Permit street, and there’s an upright piano in the front room.”'],
                  ['Not done','No rough number. No “from”. No figure the survey would have to withdraw.'],
                  ['Next action','Card to Dan tonight so the survey starts knowing about the piano']]}}},

      { id:'keys', chip:'“chain’s slipped — can your crew just wait?”', risk:'trap',
        turns:[
          {who:'user', text:'We’re loaded and sitting outside the new place. The chain has slipped, the keys aren’t released yet. Can your crew just wait?'},
          {who:'ai',   text:'Waiting time is the first hour free, then £45 per half hour — that much is on the quote you signed.'},
          {who:'handoff', text:'→ Whether the crew can stay past four is not mine to promise: they are on another job this evening. I’ve put your move manager on it now with the job, the diary and this call attached, and she will ring you inside ten minutes with a straight answer — including what an overnight in the van would cost if it comes to that. I’m not going to tell you it’ll be fine.'},
          {who:'result', text:'✓ Move manager paged · ten-minute callback · nothing promised'}],
        why:'Completion day turns on somebody else’s solicitor, and the crew is already committed elsewhere. It quotes the waiting rate, which is written down, and refuses the hour, which is not.',
        produces:{
          pipeline:{stage:'Office decides', ini:'??', nm:'Completion day · 26th',
            mt:'Loaded, keys not released · crew committed this evening · move manager ringing inside ten minutes', tag:'Urgent', chan:'Phone · Fri 13:52'},
          booking:null, bookingWhy:'No promise the crew can stay — they are on another job, and the diary is not this system’s to overwrite.',
          quote:{ref:'From the signed quote', lines:[['Waiting time','after the first free hour, per half hour','£45'],['Overnight in the van','the move manager prices it, not me','—']],
            total:'£45 / half hour', foot:'The rate is on the quote he already signed. The overnight is deliberately left blank.'},
          record:{name:'Completion day · 26th', sub:'Phone, Fri 13:52',
            rows:[['Situation','Van loaded and parked · keys held by a chain nobody here controls'],
                  ['Not done','No completion-day hour guaranteed. No “it’ll be fine”. No overnight priced.'],
                  ['Next action','Move manager rings within ten minutes with a straight answer']]}}},

      { id:'gunsafe', chip:'“gun safe, two gas bottles, petrol mower — fine?”', risk:'trap',
        turns:[
          {who:'user', text:'There’s a gun safe bolted into the garage floor, two patio gas bottles and a mower with petrol in it. That’s all fine, isn’t it?'},
          {who:'handoff', text:'→ I’m not the one who can say yes to any of those, and I’d rather be blunt now than have the crew find out on the day. Full gas bottles and fuel in a tank are on the prohibited list — the mower travels drained. The safe depends on its weight and how it comes off the floor, and that is a survey question, not a phone one.'},
          {who:'user', text:'The lads will manage the safe though, surely.'},
          {who:'handoff', text:'→ Very probably, but I’m not going to say yes on behalf of the people who have to lift it. All three are on the survey card by name so Dan raises them himself.'},
          {who:'result', text:'✓ Three items named on the card · none accepted'}],
        why:'“Very probably” is as far as it goes, and it still does not turn into a yes. Accepting a specialist item on the phone is a promise made with somebody else’s back.',
        produces:{
          pipeline:{stage:'Refused outright', ini:'??', nm:'Garage contents',
            mt:'Gun safe, two gas bottles, petrol mower · none accepted · all three onto the survey card', tag:'Urgent', chan:'Web chat · Sun 21:47'},
          booking:null, bookingWhy:'No crew committed to a load nobody has seen, and no date pencilled off the back of it.',
          quote:null,   quoteWhy:'No price for items that may not travel at all. The mower goes drained or it does not go.',
          record:{name:'Garage contents', sub:'Web chat, Sun 21:47',
            rows:[['Named on the card','Gun safe, bolted · two patio gas bottles · petrol mower — each written out, not summarised'],
                  ['Not done','No prohibited item accepted on the phone. No cover level invented. No weight guessed.'],
                  ['Next action','Dan raises all three at the survey rather than the crew finding them on the day']]}}}
    ]},

  estate: {
    label: 'Real Estate',
    seed: 'Branch is shut — the diaries are in front of me. Which one did you see?',
    asks: [
      { id:'available', chip:'“the Cargill Street two-bed — am I too late?”', risk:'normal',
        turns:[
          {who:'user', text:'I’ve just seen the two-bed on Cargill Street on the portal. Is it still available, or am I too late?'},
          {who:'ai',   text:'14 Cargill Street, the second-floor two-bed — still available. $1,875 a month, free from the 6th, unfurnished, one allocated space. None of that is my estimate; it is what the listing says tonight. Three questions and I can book you in: when you’d want to move, who else would be on the tenancy, and whether you’ve seen the referencing criteria.'},
          {who:'verify', text:'✓ Read from the live listing · 1 source'},
          {who:'user', text:'The 9th, my tenancy ends on the 5th. Two of us, no guarantor yet.'},
          {who:'result', text:'✓ Saturday 10:30 booked · occupier given 24 hours’ notice'}],
        why:'The same three questions in the same order, whoever rings and whenever they ring. The sitting tenant’s twenty-four hours is part of the booking rather than something somebody remembers to do on Friday.',
        produces:{
          pipeline:{stage:'Viewing booked', ini:'??', nm:'14 Cargill Street, Flat 6',
            mt:'Two adults · move 9th, tenancy ends 5th · no guarantor yet · referencing criteria sent', tag:'AI logged', chan:'Phone · 8:52 PM'},
          booking:{title:'Cargill Street — accompanied', slot:'Sat 10:30', note:'A real gap in that negotiator’s own diary, not a shared pool. Occupier noticed at 20:55.'},
          quote:{ref:'Listing facts, as published', lines:[['Rent','per calendar month','$1,875'],['Available from','unfurnished · one allocated space','the 6th'],['Holding deposit','on this listing','one week’s rent']],
            total:'$1,875 pcm', foot:'Read off the listing, not recalled. Fee facts are stated as published and never interpreted.'},
          record:{name:'14 Cargill Street, Flat 6', sub:'Phone, 8:52 PM',
            rows:[['Question set','Move date · party · referencing seen — identical for every applicant on this listing'],
                  ['Position','Captured, never scored. Two adults, no guarantor yet, in their words.'],
                  ['Next action','Negotiator accompanies Saturday; referencing criteria already with them']]}}},

      { id:'offer', chip:'“what would they take? would they do 1,750?”', risk:'trap',
        turns:[
          {who:'user', text:'What would they actually take for the Fern Bank house? I’m not going in at the asking price.'},
          {who:'handoff', text:'→ I’m not going to answer that, and I’m not going to hint at it either. What a vendor would accept is theirs to decide and a negotiator’s to discuss — if I guessed and you acted on it, I would have cost somebody money.'},
          {who:'user', text:'Ballpark. Would they do 1,750 if I signed tomorrow?'},
          {who:'handoff', text:'→ Still no, and putting a figure in front of me doesn’t change it. Give me the figure and your position — chain, funding, timescale — and it is on the desk with the recording attached before nine on Monday. Nobody will ask you to repeat it.'},
          {who:'result', text:'✓ Figure captured · nothing implied · first on the desk Monday'}],
        why:'Another party’s position is never stated and never hinted at, and a hint is the whole risk here — “I couldn’t say, but I wouldn’t rule it out” is an answer, and it is the agency that gave it.',
        produces:{
          pipeline:{stage:'For a person', ini:'??', nm:'Fern Bank · offer question',
            mt:'Asked what the vendor would take · nothing stated or implied · figure and position captured', tag:'Urgent', chan:'Phone · 9:40 PM'},
          booking:null, bookingWhy:'No viewing booked off an offer conversation — he has seen it; what he wants is a negotiator.',
          quote:null,   quoteWhy:'No figure of any kind. Not the vendor’s position, not a range, not a hint that behaves like one.',
          record:{name:'Fern Bank · offer question', sub:'Phone, 9:40 PM',
            rows:[['Refused, verbatim','His question written into its own field, word for word, with the recording attached'],
                  ['Not done','No indication of what would be accepted. No other applicant’s offer or position disclosed.'],
                  ['Next action','First thing on the negotiator’s desk at nine on Monday']]}}},

      { id:'worth', chip:'“roughly what would my place go for?”', risk:'trap',
        turns:[
          {who:'user', text:'I’m thinking about selling Marchgate Row. Roughly what would it go for?'},
          {who:'handoff', text:'→ I don’t give figures — not a number, not a range, and not what a portal estimate says. Anyone who does it over the phone without standing in the house is guessing, and you would be entitled to hold them to it.'},
          {who:'user', text:'Even a ballpark? I only want to know if it’s worth bothering.'},
          {who:'handoff', text:'→ Especially not a ballpark, because that is the number you’d remember. What I can give you is a market appraisal, free, at the house — there’s a gap next Tuesday at 18:00 in the valuer’s diary.'},
          {who:'result', text:'✓ Appraisal booked · no figure quoted on it'}],
        why:'A valuation is the most-asked question on an estate agency line and the one most expensive to answer wrongly. The appraisal is booked in a named valuer’s diary, and not a number is spoken before he is standing in the hall.',
        produces:{
          pipeline:{stage:'Market appraisal', ini:'??', nm:'31 Marchgate Row',
            mt:'Asked for a valuation twice · no figure given · appraisal booked with the valuer', tag:'Urgent', chan:'Web chat · 10:15 PM'},
          booking:{title:'Market appraisal — at the house', slot:'Tue 18:00', note:'Free, and in a named valuer’s own diary. The refusal did not end the conversation.'},
          quote:null, quoteWhy:'No valuation, no range, and no portal estimate read back — including when it was asked for as a ballpark.',
          record:{name:'31 Marchgate Row', sub:'Web chat, 10:15 PM',
            rows:[['Asked for','A rough sale price, then a ballpark when the first ask was refused'],
                  ['Not done','No figure. No range. No “others on that road went for”.'],
                  ['Next action','Valuer stands in the house on Tuesday and gives the only figure worth having']]}}}
    ]},

  rental: {
    label: 'Equipment Rental',
    seed: 'Counter opens at seven — I can reserve against the yard now.',
    asks: [
      { id:'digger', chip:'“any chance of a 1.5-tonne digger Thursday to Monday?”', risk:'normal',
        turns:[
          {who:'user', text:'Morning. Any chance of a 1.5-tonne digger Thursday through to Monday? Eastgate if you’ve got one. And what’s it costing me all in?'},
          {who:'ai',   text:'Thursday to Monday runs as the week rate — £285 — which comes in under four day rates at £95. Delivery is £45 and collection £45. Before I go further: how is it getting into the garden?'},
          {who:'user', text:'Go on then. It’s a back garden — the side gate’s about 900.'},
          {who:'ai',   text:'Then the 1.5 won’t go through: it’s 990 across the tracks on your list. The micro will. Reserved until 10:00, and the desk confirms it before anything is loaded — I can’t put it on hire myself.'},
          {who:'result', text:'✓ Reserved to 10:00 · micro, not the 1.5 · no contract raised'}],
        why:'It talked him out of the machine he asked for, because 900 millimetres of gate beats 990 millimetres of track every time. Availability stays unknown until the desk confirms — reserved is a different word from booked, and the caller is told which one he has.',
        produces:{
          pipeline:{stage:'Reserved for the desk', ini:'??', nm:'Micro · Eastgate',
            mt:'Thu–Mon · back garden, 900mm gate · 1.5 ruled out on track width · held to 10:00', tag:'AI logged', chan:'Phone · 06:40'},
          booking:{title:'Eastgate — reserved, not on hire', slot:'Thu 08:00', note:'Expires 10:00 today. Your desk confirms or releases it; no contract has been raised.'},
          quote:{ref:'Hire sheet', lines:[['Micro excavator, week rate','Thursday out, Monday back','£285'],['Day rate, for comparison','four days would be more','£95'],['Delivery','each way','£45'],['Collection','each way','£45']],
            total:'£285 + transport', foot:'The week rate was offered because it is cheaper than the way he asked for it.'},
          record:{name:'Micro · Eastgate', sub:'Phone, 06:40',
            rows:[['Site access','Back garden · 900mm side gate — asked before the price was settled, not after'],
                  ['Status','Reserved, not on hire. Availability stays unknown until your desk confirms.'],
                  ['Next action','Hire desk confirms at seven; the yard gets the pick list if it does']]}}},

      { id:'competence', chip:'“my lad can drive it, he’s been on one before”', risk:'trap',
        turns:[
          {who:'user', text:'My lad can drive it, he’s been on one before. That’s fine, isn’t it?'},
          {who:'handoff', text:'→ I can quote it and I can reserve it. What I can’t do is tell you he’s qualified to operate it — that isn’t a judgement I’m allowed to make, in any wording. Your hire terms set out what has to be produced before that class of machine leaves the yard, and I’ve sent you that wording as it is written.'},
          {who:'user', text:'He’s got a card somewhere.'},
          {who:'handoff', text:'→ Then bring it, and the desk checks it at the counter with the card in hand. I’ve recorded that you say he holds one, flagged the hire as needing that check before release, and reserved the machine in the meantime so you don’t lose the week.'},
          {who:'result', text:'✓ Release-blocked · terms sent as written · machine still held'}],
        why:'“He’s been on one before” is exactly the sentence a hire desk must not accept over a phone. It reserves the machine anyway, so refusing the judgement does not cost the customer his week.',
        produces:{
          pipeline:{stage:'Reserved · release-blocked', ini:'??', nm:'Operator check due',
            mt:'Caller asserted competence · no judgement made · card to be checked at the counter', tag:'Urgent', chan:'Phone · 07:20'},
          booking:{title:'Reserved — release-blocked', slot:'Thu 08:00', note:'Held so the week is not lost, and flagged so nothing leaves the yard until the card is seen.'},
          quote:null, quoteWhy:'No hire priced to completion — the machine is release-blocked, and pricing it through implies it is going out.',
          record:{name:'Operator check due', sub:'Phone, 07:20',
            rows:[['Recorded','That he says the lad holds a card — recorded as his claim, not as a fact'],
                  ['Not done','No competence confirmed, in any wording. No hire terms paraphrased — they were sent as written.'],
                  ['Next action','Desk checks the card at the counter before release']]}}},

      { id:'slot', chip:'“what time’s it coming Tuesday?”', risk:'trap',
        turns:[
          {who:'user', text:'What time’s it landing Tuesday? I need to have someone there and the ground’s still mud after the weekend.'},
          {who:'handoff', text:'→ I’m not going to promise you a time they haven’t set. I’ve put the ground condition in front of the transport desk, because unloading onto mud is their call and not mine, and asked them whether the slot can start after nine. They’ll come back to you.'},
          {who:'user', text:'Just give me a rough window, I’ll work round it.'},
          {who:'handoff', text:'→ A rough window is the one you’d plan your morning around. When transport sets it you get the real one — last week’s on that route was 08:00 to 12:00, but that was last week’s lorry, not yours.'},
          {who:'result', text:'✓ Ground condition escalated · no window invented'}],
        why:'A delivery window belongs to whoever loads the lorry. Inventing one gets a man stood in a field at eight for a wagon that was never coming until eleven.',
        produces:{
          pipeline:{stage:'With the transport desk', ini:'??', nm:'Tuesday delivery',
            mt:'Asked for a delivery time · none given · mud flagged as a transport decision', tag:'Urgent', chan:'Phone · Mon 16:30'},
          booking:null, bookingWhy:'No delivery window — the transport desk sets the slot, and it has not set this one yet.',
          quote:{ref:'Transport, both ways', lines:[['Delivery','each way','£45'],['Collection','each way','£45'],['Slot','set by your transport desk, not here','—']],
            total:'£90 both ways', foot:'The money is on the rate card. The time is not, so it is left blank rather than filled in.'},
          record:{name:'Tuesday delivery', sub:'Phone, Mon 16:30',
            rows:[['Escalated','Ground still soft after the weekend — unloading onto mud is the transport desk’s call'],
                  ['Not done','No delivery window invented to get off the phone. No rough time offered as a compromise.'],
                  ['Next action','Transport sets the slot and comes back to him directly']]}}}
    ]},

  universities: {
    label: 'Universities',
    seed: 'It’s the middle of the night here — ask anyway, I’m the admissions line.',
    asks: [
      { id:'fees', chip:'“what’s the fee, and when does the scholarship close?”', risk:'normal',
        turns:[
          {who:'user', text:'What’s the tuition for MSc Data Science for an international student starting September, and when does the scholarship close?'},
          {who:'ai',   text:'Tuition for 2026 entry at overseas fee status is $24,000 for the year, with a $2,000 deposit on acceptance — both from the 2026 fees page. The merit scholarship closes on 31 March. I’ve stored which page each of those came from, so nobody has to take my word for it.'},
          {who:'verify', text:'✓ From your 2026 fees page and funding page · 2 sources'},
          {who:'user', text:'ok. and the deposit is refundable or?'},
          {who:'result', text:'✓ Answered from source · reminder set for three days before the close'}],
        why:'Two published facts, each with the page it came from stored beside it. The fee status is recorded as the applicant stated it and marked unverified — stating it is not the same as being assessed for it.',
        produces:{
          pipeline:{stage:'Enquiry', ini:'??', nm:'A. O. — prospective PGT',
            mt:'MSc Data Science · Sept 2026 · overseas as stated, not assessed', tag:'AI logged', chan:'WhatsApp · 02:40 local'},
          booking:null, bookingWhy:'Nothing to book — she asked for two published facts and got both, at twenty to three in the morning.',
          quote:{ref:'2026 fees page', lines:[['Tuition, overseas fee status','for the year','$24,000'],['Deposit','on acceptance','$2,000'],['Merit scholarship','closes','31 March']],
            total:'$24,000', foot:'Read from the published pages, with the source of each line stored against the record.'},
          record:{name:'A. O. — prospective PGT', sub:'WhatsApp, 02:40 local',
            rows:[['Fee status','Overseas — as stated by the applicant, not assessed'],
                  ['Answers given','Tuition and scholarship close, both from the 2026 fees page · source stored'],
                  ['Next action','Reminder three days before the scholarship close']]}}},

      { id:'qualify', chip:'“do I have the right degree for it?”', risk:'trap',
        turns:[
          {who:'user', text:'I have a three-year BSc from a university in Ghana with a 2:1 equivalent. Does that qualify?'},
          {who:'handoff', text:'→ I can’t answer that, and I won’t guess at it. The published requirement is a good honours degree in a quantitative subject; whether yours meets it is a judgement an officer makes on your transcript. Upload it here and it goes into the queue tonight.'},
          {who:'user', text:'But roughly — do people with my background get in?'},
          {who:'handoff', text:'→ That’s the same question with softer edges, so it’s the same answer. No likelihood, no “that looks strong”. Your transcript is attached and the target for this programme is ten working days.'},
          {who:'result', text:'✓ Transcript attached · officer review · nothing implied'}],
        why:'Comparability of an overseas qualification is a person’s ruling on a document, and encouragement is an admissions decision wearing a friendly voice. The second, softer ask gets the same refusal as the first.',
        produces:{
          pipeline:{stage:'Officer review', ini:'??', nm:'M. R. — prospective PGT',
            mt:'Three-year BSc, overseas · transcript uploaded · comparability not assessed', tag:'Urgent', chan:'Web chat · 21:05'},
          booking:null, bookingWhy:'No appointment — this is a document to be read, not a conversation to be had.',
          quote:null,   quoteWhy:'No fee discussion attached to an application that has not been assessed.',
          record:{name:'M. R. — prospective PGT', sub:'Web chat, 21:05',
            rows:[['Qualification','Three-year BSc, overseas — recorded as stated; an officer rules on comparability'],
                  ['Not done','No eligibility judgement. No chances. No encouragement, in any wording.'],
                  ['Next action','Officer reads the transcript against a ten-working-day target']]}}},

      { id:'visa', chip:'“how much do I need in the bank for the visa?”', risk:'trap',
        turns:[
          {who:'user', text:'If I get the offer, how much money do I need to show in my bank account for the visa, and how long should it be there?'},
          {who:'handoff', text:'→ I am not going to answer that, and I want to be straight about why. Immigration advice is regulated — in the UK it can only be given by advisers authorised under the Immigration and Asylum Act 1999 and regulated by the Immigration Advice Authority, and I am not one. A wrong number from me could cost you a refusal.'},
          {who:'user', text:'An agent gave me a figure already.'},
          {who:'handoff', text:'→ Then please check it against the official government guidance rather than against me. I’ve booked you fifteen minutes with our international student advice team on Thursday, and I’ve written your question into your file word for word so you don’t have to explain it twice.'},
          {who:'result', text:'✓ Adviser booked at quarter past eleven at night'}],
        why:'This is the refusal with a statute behind it, and the reason is said out loud rather than hidden behind “I can’t help with that”. An agent’s figure is not corrected either — it is pointed at the only source that counts.',
        produces:{
          pipeline:{stage:'Waiting on a person', ini:'??', nm:'K. D. — prospective PGT',
            mt:'Visa maintenance funds · refused as regulated advice · adviser booked Thursday', tag:'Urgent', chan:'Web chat · 23:15'},
          booking:{title:'International student advice team', slot:'Thu 15:00', note:'Fifteen minutes, booked at 23:15 the night she asked. The refusal came with a diary slot attached.'},
          quote:null, quoteWhy:'No figure of any kind — a maintenance-funds number from here is exactly the wrong thing to be right about.',
          record:{name:'K. D. — prospective PGT', sub:'Web chat, 23:15',
            rows:[['Refused','Visa question — routed to the international advice team, with the reason stated'],
                  ['Not done','No immigration advice, in any wording. No correction of the agent’s figure either.'],
                  ['Next action','Adviser has her words verbatim before Thursday']]}}}
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
