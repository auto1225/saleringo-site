# Saleringo — verified photo assets

All URLs below returned **HTTP 200** and were **visually inspected** (downloaded + viewed) or came from a
subject-specific Pexels search with a matching caption. Source: Pexels — free to use commercially,
no attribution required, hotlinking the `images.pexels.com` CDN is permitted.

**Usage pattern** — always append sizing params and always set `loading`, `decoding`, `alt`:

```html
<img class="ph" src="https://images.pexels.com/photos/18441167/pexels-photo-18441167.jpeg?auto=compress&cs=tinysrgb&w=1600"
     alt="A city skyline lit up at night" loading="lazy" decoding="async" width="1600" height="1000">
```

- Hero / above-the-fold images: `loading="eager"` + `fetchpriority="high"`.
- Widths: hero `w=1800`, section `w=1200`, card `w=800`, portrait `w=400`.
- Never use a photo without a gradient scrim behind text (see `.photo-scrim` in scenes.css).

---

## Hero / atmosphere

| key | URL (append `?auto=compress&cs=tinysrgb&w=…`) | Subject | Verified |
|---|---|---|---|
| `hero-night-city` | `https://images.pexels.com/photos/18441167/pexels-photo-18441167.jpeg` | Downtown skyline at night, lit towers + freeway light trails | ✅ viewed |
| `night-city-2` | `https://images.pexels.com/photos/11677347/pexels-photo-11677347.jpeg` | LA towers glowing at night, aerial | search-matched |
| `night-city-3` | `https://images.pexels.com/photos/29123790/pexels-photo-29123790.jpeg` | Seattle twilight skyline | search-matched |

## Industry — Home services

| key | URL | Subject | Verified |
|---|---|---|---|
| `hvac-tech` | `https://images.pexels.com/photos/6471913/pexels-photo-6471913.jpeg` | Technician with manifold gauges servicing an outdoor AC unit | ✅ viewed |
| `hvac-tech-2` | `https://images.pexels.com/photos/5463575/pexels-photo-5463575.jpeg` | Technician repairing air conditioner with gauge set | search-matched |
| `hvac-rooftop` | `https://images.pexels.com/photos/5463587/pexels-photo-5463587.jpeg` | Worker repairing rooftop AC unit | search-matched |

## Industry — Dental

| key | URL | Subject | Verified |
|---|---|---|---|
| `dentist-consult` | `https://images.pexels.com/photos/6627325/pexels-photo-6627325.jpeg` | Dentist in scrubs discussing a treatment plan with a patient | search-matched |
| `dentist-treat` | `https://images.pexels.com/photos/6627447/pexels-photo-6627447.jpeg` | Dentist adjusting overhead lamp during a procedure | search-matched |
| `dentist-exam` | `https://images.pexels.com/photos/8413334/pexels-photo-8413334.jpeg` | Dentist examining a patient under clinic lighting | search-matched |

## Industry — Clinics

| key | URL | Subject | Verified |
|---|---|---|---|
| `clinic-reception` | `https://images.pexels.com/photos/33812025/pexels-photo-33812025.jpeg` | Warm medical-centre reception, wood panelling | search-matched |
| `clinic-interior` | `https://images.pexels.com/photos/7108324/pexels-photo-7108324.jpeg` | Modern clinic interior, teal + white | search-matched |

## Industry — Boutique stays

| key | URL | Subject | Verified |
|---|---|---|---|
| `hotel-lobby` | `https://images.pexels.com/photos/31080810/pexels-photo-31080810.jpeg` | Luxury hotel lobby, modern design, cosy seating — no masks | search-matched |
| `hotel-lobby-2` | `https://images.pexels.com/photos/18117651/pexels-photo-18117651.jpeg` | Bottleworks Hotel lobby, natural light | search-matched |
| `hotel-miami` | `https://images.pexels.com/photos/34607320/pexels-photo-34607320.jpeg` | Miami Beach boutique hotel reception | search-matched |

⚠️ **Do not use** `photos/7820360` (hotel check-in) — subjects wear COVID masks, reads dated.

## Industry — Wedding & event venues

| key | URL | Subject | Verified |
|---|---|---|---|
| `venue-night` | `https://images.pexels.com/photos/30562607/pexels-photo-30562607.jpeg` | Courtyard event set at night under warm string lights | ✅ viewed |
| `venue-hall` | `https://images.pexels.com/photos/17001844/pexels-photo-17001844.jpeg` | Luxurious wedding hall, set tables, florals | search-matched |
| `venue-chandelier` | `https://images.pexels.com/photos/12689014/pexels-photo-12689014.jpeg` | Indoor event with crystal chandeliers | search-matched |

## Small business owners (on the phone)

| key | URL | Subject | Verified |
|---|---|---|---|
| `owner-shop-call` | `https://images.pexels.com/photos/8475194/pexels-photo-8475194.jpeg` | Man in apron taking a business call outside his store | search-matched |
| `owner-florist-call` | `https://images.pexels.com/photos/5414327/pexels-photo-5414327.jpeg` | Florist in apron on a smartphone by the counter | search-matched |
| `owner-bakery-call` | `https://images.pexels.com/photos/8902305/pexels-photo-8902305.jpeg` | Baker packing cupcakes while on a call | search-matched |
| `owner-boutique-call` | `https://images.pexels.com/photos/6665032/pexels-photo-6665032.jpeg` | Designer on the phone in a boutique | search-matched |

## Portraits — testimonials, avatars, about

| key | URL | Subject | Verified |
|---|---|---|---|
| `portrait-w1` | `https://images.pexels.com/photos/8171192/pexels-photo-8171192.jpeg` | Woman, warm smile, close-up office headshot | ✅ viewed |
| `portrait-m1` | `https://images.pexels.com/photos/29995649/pexels-photo-29995649.jpeg` | Man in blue suit with glasses, grey backdrop | search-matched |
| `portrait-w2` | `https://images.pexels.com/photos/27086761/pexels-photo-27086761.jpeg` | Woman in business suit, welcoming | search-matched |
| `portrait-m2` | `https://images.pexels.com/photos/17582358/pexels-photo-17582358.jpeg` | Man in blue suit at a desk | search-matched |
| `portrait-w3` | `https://images.pexels.com/photos/29086752/pexels-photo-29086752.jpeg` | Woman in striped blazer | search-matched |
| `portrait-m3` | `https://images.pexels.com/photos/37218479/pexels-photo-37218479.jpeg` | Man in white shirt, dark backdrop | search-matched |

## People on the phone at night (mood)

| key | URL | Subject | Verified |
|---|---|---|---|
| `night-caller` | `https://images.pexels.com/photos/17735127/pexels-photo-17735127.jpeg` | Woman on a phone at dusk, blurred city lights | search-matched |
| `night-payphone` | `https://images.pexels.com/photos/19061187/pexels-photo-19061187.jpeg` | Person at a lit payphone at night, moody profile | search-matched |

---

## Real delivered dimensions — copy these, never guess

Machine-measured from the CDN on 2026-08-18 (`?auto=compress&cs=tinysrgb&w=…`). The delivered
height for a given `w=` is deterministic: **height = round(w × h/w)**. `width`/`height` attributes
must match the row below, or the tag misreports the aspect ratio to crawlers and will cause real
CLS the moment the photo leaves an absolutely-positioned or aspect-locked container.

| key | photo id | shape | h/w | height @ w=1900 | @1200 | @800 |
|---|---|---|---|---|---|---|
| `night-city-2` | 11677347 | landscape | 0.5626 | 1069 | 675 | 450 |
| `night-city-3` | 29123790 | landscape | 0.6642 | 1262 | 797 | 531 |
| `dentist-exam` | 8413334 | landscape | 0.6663 | 1266 | 800 | 533 |
| `owner-bakery-call` | 8902305 | landscape | 0.6663 | 1266 | 800 | 533 |
| `portrait-w1` | 8171192 | landscape | 0.6663 | 1266 | 800 | 533 |
| `hotel-lobby-2` | 18117651 | landscape | 0.6667 | 1267 | 800 | 533 |
| `hotel-miami` | 34607320 | landscape | 0.6667 | 1267 | 800 | 533 |
| `venue-chandelier` | 12689014 | landscape | 0.6667 | 1267 | 800 | 533 |
| `venue-hall` | 17001844 | landscape | 0.6667 | 1267 | 800 | 533 |
| `dentist-consult` | 6627325 | landscape | 0.6668 | 1267 | 800 | 533 |
| `venue-night` | 30562607 | landscape | 0.6668 | 1267 | 800 | 533 |
| `owner-shop-call` | 8475194 | landscape | 0.6675 | 1268 | 801 | 534 |
| `clinic-interior` | 7108324 | landscape | 0.6679 | 1269 | 801 | 534 |
| `hvac-tech-2` | 5463575 | landscape | 0.7100 | 1349 | 852 | 568 |
| `night-caller` | 17735127 | landscape | 0.7168 | 1362 | 860 | 573 |
| `hero-night-city` | 18441167 | landscape | 0.7500 | 1425 | 900 | 600 |
| `hvac-rooftop` | 5463587 | landscape | 0.8263 | 1570 | 992 | 661 |
| `clinic-reception` | 33812025 | portrait | 1.3332 | 2533 | 1600 | 1067 |
| `dentist-treat` | 6627447 | portrait | 1.5000 | 2850 | 1800 | 1200 |
| `hotel-lobby` | 31080810 | portrait | 1.5000 | 2850 | 1800 | 1200 |
| `hvac-tech` | 6471913 | portrait | 1.5000 | 2850 | 1800 | 1200 |
| `night-payphone` | 19061187 | portrait | 1.5000 | 2850 | 1800 | 1200 |
| `owner-boutique-call` | 6665032 | portrait | 1.5000 | 2850 | 1800 | 1200 |
| `owner-florist-call` | 5414327 | portrait | 1.5000 | 2850 | 1800 | 1200 |
| `portrait-m1` | 29995649 | portrait | 1.5000 | 2850 | 1800 | 1200 |
| `portrait-m2` | 17582358 | portrait | 1.5000 | 2850 | 1800 | 1200 |
| `portrait-w2` | 27086761 | portrait | 1.5000 | 2850 | 1800 | 1200 |
| `portrait-w3` | 29086752 | portrait | 1.5000 | 2850 | 1800 | 1200 |

**Nine of these are 2:3 portraits.** A portrait inside `.photohero` (full width × `min(88vh,860px)`,
≈1.67:1) shows only a ~40% horizontal band. Either pick a landscape row, or set
`object-position` on that page's `.bgimg img` and check the crop at 1440×860 and at 768px.
Heroes already tuned this way: `clinics`, `stays`, `whatsapp`, `home-services`, `voice`, `verified-ai`.

**Avatars must be cropped by the CDN, not the browser.** Use
`?auto=compress&cs=tinysrgb&fit=crop&w=160&h=160` and declare `width="160" height="160"` —
a landscape frame in a 40px circle otherwise centre-crops onto background instead of a face.
Same trick builds social cards: `fit=crop&w=1200&h=630` returns an exact 1200×630.

### Frames to place with care
- `hvac-tech` (6471913) and `hvac-tech-2` (5463575) — the technician wears a face mask. Fine at
  card and thumbnail scale where it is illegible; avoid at hero scale. `hvac-rooftop` (5463587)
  is the mask-free HVAC frame and the only landscape one.
- `clinic-reception` (33812025) — a real clinic's name and logo are on the wall. Never let that
  signage sit in frame; `clinics.html` crops to the desk (`object-position:center 92%`) for exactly
  this reason. Stock must never read as a named customer.

---

### Honesty rule
Stock people are **never** captioned as named customers or shown as testimonial authors with invented quotes.
Portraits may be used for: the founding-cohort invitation, "who this is for" audience shots, and
about/team context. Reserved testimonial cards stay visibly empty until real quotes exist.

---

## Reuse budget (enforced — added 2026-08-18 after the design audit)

The audit measured **29 unique images across 207 placements — 7.1× average reuse**. One
headshot (`photos/8171192`) appeared on **13 of 20 pages**; 16 of 29 images appeared on 5+.
A visitor walking index → voice → pricing → dental met the same four faces four times, and
the library read as stock-on-shuffle rather than art direction.

- Target: no image on more than **4** pages. **Currently achieved: 6.** Stating the real number
  rather than the aspiration — 41 verified images across 24 pages, minus category constraints
  (a hotel concierge cannot stand in on an academy page, a masked technician cannot appear at
  hero scale), leaves 6 as today's ceiling. Before this pass one headshot sat on **14 of 20**
  pages. Getting to 4 needs roughly 15 more verified frames, weighted toward generic business
  people at ~3:2 landscape, which is the shape most card slots want.
- No image may appear on both a channel page (voice / webchat / whatsapp) and `index`.
- Portraits: each industry page gets its **own** facepile set — never the global four.
- Check before shipping; the top count must be ≤ 3:

```bash
grep -rho 'photos/[0-9]*' en ko | sort | uniq -c | sort -rn | head
```

### Grading is now doing half this work
`scenes.css` defines a per-page photographic grade driven by `data-grade` on `<body>`
(`voice · chat · msg · stays · clinic · dental · venues · home · trust`). A reused frame
graded 26° warm on `stays` and 206° cool on `webchat` reads as two different photographs.
**The hero image is deliberately left ungraded** so every page keeps exactly one
full-colour moment. Grading applies to `.photocard`, `.photosplit .media`, `.photo-scrim`
and `.audcard`, and lifts back toward true colour on hover.

### Responsive delivery is mandatory
0 of 167 images shipped `srcset` before this pass — a phone downloaded the `w=1600` hero.
Pexels honours arbitrary `w=`, so this costs nothing but characters:

```html
srcset="…&w=640 640w, …&w=1024 1024w, …&w=1600 1600w, …&w=2200 2200w"
sizes="100vw"                                  <!-- hero -->
sizes="(max-width:900px) 100vw, 33vw"          <!-- card -->
```

Exactly **one** `fetchpriority="high"` per page — the hero background. Facepile and other
decorative avatars are `loading="lazy"` with `alt=""`: they name no real person, and the
adjacent caption already carries the meaning.

---

## Pool expansion — 2026-08-18 (round 2)

The reuse budget above could not be met with 29 images: after the first remediation pass one
headshot still appeared on **14 pages**. Twenty-three more were sourced, each fetched from the
Pexels CDN (HTTP 200) and measured; the ones marked ✅ were downloaded and **looked at**.

### Owners & operators — the faces this product is actually for
| key | photo id | h/w | subject | verified |
|---|---|---|---|---|
| `owner-grocer` | `8422729` | 1.4975 | Man in a brown apron, arms folded, in his own village grocery — shelves, straw hats, real stock | ✅ viewed |
| `owner-cafe-pair` | `34164498` | 0.6675 | Two café owners behind their counter with a laptop, both smiling | ✅ viewed |
| `owner-shoeshop` | `6888761` | 1.5000 | Mature owner, arms crossed, in a bright shoe shop | search-matched |
| `owner-florist-2` | `3933017` | 0.6675 | Young woman, arms crossed, at the entrance of her flower shop | search-matched |
| `owner-retail-elder` | `8201198` | 0.6675 | Older man in glasses leaning on his shop counter, smiling | search-matched |
| `owner-grocers-two` | `8475204` | 0.6675 | Two shopkeepers in aprons in a local grocery | search-matched |
| `owner-coffee-man` | `8344819` | 1.5000 | Man standing in a modern coffee-shop workspace | search-matched |
| `owner-open-sign` | `4473356` | 1.3950 | Woman holding a "Welcome — We Are Open" sign in a doorway | search-matched |
| `owner-cafe-wide` | `36729739` | 0.5625 | Café owner, arms crossed, in a rustic coffee shop — wide crop, good for bands | search-matched |
| `owner-waiter` | `5920775` | 1.5000 | Smiling waiter in an apron outside a city-park café | search-matched |

### Desk portraits — for about / team / audience strips
| key | photo id | h/w | subject | verified |
|---|---|---|---|---|
| `portrait-desk-m` | `10376250` | 0.6675 | Bearded man with braided hair at his desk with a laptop | search-matched |
| `portrait-suit-m` | `7413964` | 1.5000 | Man in a tailored grey suit on a black leather couch | search-matched |

### Dental — mask-free frames (the existing HVAC/dental set is masked)
| key | photo id | h/w | subject | verified |
|---|---|---|---|---|
| `dental-explain` | `4270095` | 1.5000 | Dentist showing a jaw model to a seated patient, assistant behind — **no masks, faces visible** | ✅ viewed |
| `dental-tablet` | `3952124` | 0.6675 | Dentist showing a tablet screen to an assistant beside a patient | search-matched |
| `dental-clinic` | `4270379` | 0.6675 | Dentist attending a patient in a modern clinic | search-matched |
| `dental-xray` | `7800669` | 1.5000 | Two dentists reviewing an X-ray | search-matched |

### Hospitality front desk
| key | photo id | h/w | subject | verified |
|---|---|---|---|---|
| `hotel-desk-staff` | `36684286` | 0.6675 | Receptionist at a hotel front desk, lobby board behind | ✅ viewed |
| `hotel-checkin` | `3771811` | 0.6675 | Receptionist smiling across the desk, map spread out | search-matched |
| `hotel-guests` | `5378703` | 0.6675 | Guests at a luxurious hotel reception desk | search-matched |
| `hotel-concierge` | `5371677` | 1.5000 | Concierge in uniform welcoming guests | search-matched |
| `hotel-concierge-2` | `6474532` | 1.5000 | Uniformed concierge in a luxurious lobby | search-matched |
| `hotel-checkin-2` | `3215519` | 0.6675 | Guest checking in at a reception desk | search-matched |
| `hospitality-team` | `37304285` | 1.3325 | Three hospitality staff in a luxurious interior | search-matched |

⚠️ **Do not use** the `78203xx` hotel-reception series (7820379 · 7820327 · 7820375 · 7820358 ·
7820355 · 7820377 · 7820322 · 7820380 · 7820323 · 7820308 · 7820311 · 7820316) — subjects wear
COVID face masks, same reason `7820360` was already banned.

**Height for a given width = round(w × h/w)** using the ratio column. Set `width`/`height` to match
or the tag misreports the aspect ratio and causes real CLS.

---

## Scene replacements — 2026-08-18 (round 3)

The site shipped **46 illustrated SVG scenes**. About half depict a *place or a moment* — a
house at night, an empty banquet hall, a closed shop, a clinic desk after hours. Those are
photographs pretending to be drawings, and the owner rejected them on sight. The other half are
genuine information design (world maps, invoices, timelines, funnels) and stay vector.

**Rule going forward:** if the `aria-label` describes something a camera could have photographed,
it must be a photograph. If it describes a relationship, a process or a number, it stays a diagram.

| key | photo id | h/w | subject | verified |
|---|---|---|---|---|
| `house-night-lit` | `9592437` | 0.6675 | Modern house at night, upper windows glowing warm against a black sky | ✅ viewed |
| `house-night-2` | `3684943` | 0.8575 | Apartment facade at night, a single lit window | search-matched |
| `townhouse-night` | `38007967` | 1.2500 | Classic London townhouse, illuminated windows | search-matched |
| `apartment-one-window` | `5748112` | 1.5000 | Dim apartment block, one window lit | search-matched |
| `house-entrance-night` | `9890735` | 1.5000 | Warmly lit house entrance at night | search-matched |
| `banquet-empty` | `19569865` | 0.6675 | Empty banquet hall, chandeliers, round tables set and waiting | ✅ viewed |
| `venue-ceremony-ready` | `16105890` | 0.6675 | Indoor wedding venue, chairs and chandeliers, ready | search-matched |
| `banquet-stage-lit` | `14646741` | 0.6675 | Empty banquet hall under stage lighting, tables laid | search-matched |
| `banquet-florals` | `12688995` | 0.6675 | Banquet hall set with chandeliers and floral arrangements | search-matched |
| `dental-reception` | `38055772` | 0.6675 | Spacious modern dental reception, contemporary fit-out | ✅ viewed |
| `dental-reception-2` | `38055773` | 0.6675 | Dental office reception with staff at the desk | search-matched |
| `dental-desk-wait` | `6193192` | 0.6675 | A patient waiting at a dental reception counter | search-matched |
| `clinic-reception-clean` | `6809645` | 1.4975 | Clean minimalist dental clinic reception, stylish lighting | search-matched |
| `shop-closed-sign` | `1793031` | 0.6675 | A CLOSED sign hanging on a glass shop door | ✅ viewed |
| `storefront-night` | `30320851` | 0.6675 | Lit storefront on a quiet street at night | search-matched |
| `store-entrance-night` | `8859645` | 0.5625 | Store entrance at night, warm and rustic — wide crop | search-matched |

None of these appears on any page yet, so all sixteen start at zero pages against the reuse budget.
