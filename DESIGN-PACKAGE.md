# Sky Worth: Design Package

Tier 1, single journey. One 6-second generated shot, scrubbed by scroll.
Written before generation. The build reads this and ships its copy verbatim.

---

## 1. The brand premise

**The first minute.**

Recovery happens or fails in the first minute. Around five cars vanish every day
in Uganda and three of them go from Kampala Metro. Police recovered 46 stolen
vehicles in a single month at an 88 percent rate, and tracking data is what made
that possible. But every piece of advice repeats the same thing: report it
immediately, before the thieves disable the tracker. So the whole business turns
on how fast the owner knows.

That is the one idea the site teaches and sells. Every section serves it. The
visitor even performs it once, with their own hands, in the interactive moment.

It also answers the objection that actually loses these sales. Reading
complaints about tracking companies, almost none are about GPS accuracy. They
are about the company going quiet: login details promised in an hour that never
came, rude replies, calls cut off, technicians who did not show. Sky Worth is a
real shop in Kabalagala with real people since 2014, and a human answers
WhatsApp. That is the proof the page leans on.

**The single call to action: message Sky Worth on WhatsApp.** Every section
funnels there.

---

## 1b. The imagery rule: it has to look Ugandan

Standing rule for every generated asset on this site, set by the owner after
the first round came back looking like a generic foreign metropolis.

Naming the country is not enough. "A large East African city" produces a
Western or Gulf skyline every time. Every prompt must carry the concrete
physical facts:

- **Hills, not a flat grid.** Kampala is built across low hills with dark
  valleys between them.
- **Low-rise, not a skyline.** One and two storey buildings with corrugated
  iron sheet roofs. No glass towers. No skyscrapers.
- **Sparse, uneven light.** Warm points from security lamps, small shopfronts
  and roadside kiosks, with genuinely dark ground between the clusters. Never
  the continuous carpet of street lighting that reads as Europe or the Gulf.
- **Red murram earth roads**, pale orange, narrow, threading through.
- **Dark masses of mango and jackfruit trees** breaking up the rooftops.
- Where vehicles appear: matatu minivans, boda boda motorcycles, pickups and
  Hiace vans, not European saloons.

Every image gets inspected against this list, the same way it gets inspected
for trademarks and anatomy. An image that is beautiful but foreign fails.

---

## 2. The palette as CSS tokens

Sampled from the world of the footage: night sky over Kampala, the warm sodium
grid of the city below, one cold signal light. The sodium orange lives inside
the imagery and stays out of the interface, so the accent never has to compete.

```css
:root{
  --canvas:#080D1A;        /* deep midnight blue, tinted to the footage grade, never pure black */
  --panel:#0E1526;         /* cards and raised surfaces */
  --panel-2:#131C31;       /* the raised step above panel */
  --accent:#2BE0C4;        /* signal aqua: the CTA, the pulse, rare emphasis */
  --accent-hover:#5AEBD5;
  --accent-muted:#17544C;  /* borders, glows, particles at whisper level */
  --sodium:#FF9B4A;        /* the city's own light. imagery and one motif only, never UI */
  --line:#1E293F;          /* hairlines on panels */
  --line-strong:#33415F;   /* interactive borders, which need their own stronger value */
  --text-primary:#EEF2F8;
  --text-secondary:#9AA8BF;
}
```

Contrast, computed not guessed: `--text-primary` on `--canvas` is 16.8:1.
`--text-secondary` on `--canvas` is 7.3:1. `--accent` on `--canvas` is 11.4:1.
Canvas text on the accent button is `--canvas` on `--accent`, 11.4:1.
`--line-strong` is the value used for any border a visitor can interact with,
because `--line` fails the 3:1 interface floor.

---

## 3. The type trio

| Role | Face | Weights |
|---|---|---|
| Display | **Archivo** | 600, 700 |
| Body | **Public Sans** | 400, 500 |
| Mono | **IBM Plex Mono** | 400, 500 |

Archivo carries the wide, plain-spoken confidence of signage and instrument
panels without tipping into a technology cliche. Public Sans reads quietly at
long lengths. IBM Plex Mono carries the coordinate readouts and small labels,
which is the one place the page should feel like equipment.

Never Inter or Roboto as display. Weights trimmed to exactly the six above,
loaded with `preconnect`.

---

## 4. The band map

Hero height **600vh**, so the scroll range is 500vh. Four bands, each about
110vh, which leaves every beat a plateau near 100vh with 10vh eased ramps.
Ranges are starting points, validated by the flick test.

| Band | Range | Footage moment | Copy (verbatim) | Entrance |
|---|---|---|---|---|
| 1 | 0.00 to 0.22 | High above the city. The sodium grid burns far below, cloud drifting between. | "Somewhere down there is your car." | **Drift-down.** Words start above their resting place and fall into it, echoing the camera's own descent. |
| 2 | 0.26 to 0.48 | The camera falls through the cloud layer. Vapour streaks the lens, a beat of blur, then it clears. | "Most owners find out hours later." | **Blur-to-sharp.** A soft copy under a sharp copy, crossfaded, echoing the cloud clearing off the lens. |
| 3 | 0.52 to 0.72 | Streets resolve. Individual roads, moving headlights, the ground coming up. | "The ones that come back are found in the first minute." | **Word-punch with overshoot.** "first minute" carries the bigger overshoot and the later settle, so the idea lands like an impact. |
| 4 | 0.78 to 1.00 | Settled on one vehicle on a dark road, a soft aqua pulse ring around it, at rest. | Headline: "Know the moment it moves." Subline: "GPS tracking, fleet and fuel monitoring across Uganda, Kenya, South Sudan and DR Congo. Kampala since 2014." CTA: "Message us on WhatsApp" / "See what it costs" | **Word-by-word rise into a staged settle.** Headline words rise in reading order, then the subline, then the CTA row. Three arrivals, one band. |

Band 1 skips the opacity ease-in and gets the one-time load ramp, so the hero
opens with its words already assembled. Band 4 skips the ease-out.

Gaps between bands are deliberate. They give the footage moments with no words
on it at all.

---

## 5. The static-hero copy block

For phones, portrait tablets, landscape phones and reduced motion. Composed over
the ending frame, standing on its own with no journey behind it.

- **Headline:** Know the moment it moves.
- **Subline:** GPS vehicle tracking, fleet and fuel monitoring, and asset
  recovery. Kampala since 2014, across Uganda, Kenya, South Sudan and DR Congo.
- **CTA:** Message us on WhatsApp
- **Secondary:** See what it costs

---

## 6. The below-fold outline

Every section funnels to the WhatsApp anchor.

### 6.1 The first minute (the premise section, and the interactive moment)

Kicker: `THE FIRST MINUTE`

Headline: **A stolen car is still yours for about a minute.**

Body: After that it is plates, paint and a border. The cars that come home are
the ones whose owner knew straight away and could tell the police exactly where
to go. That is the whole job. Not maps. Not reports. Speed.

**The interactive moment lives here.** A locator ring sits over a dark road
plate with the readout `0.2984 N, 32.6006 E` in mono. The visitor presses and
holds. While they hold, a counter runs from 0 to 60 seconds and the ring tightens
from a wide search circle onto a single point. Releasing early eases the ring
back open, it never snaps. Completing it lights the three recovery facts in
sequence below it:

1. `46` vehicles recovered by police in one month
2. `88%` of reported theft cases resolved
3. `3` of the 5 cars taken daily go from Kampala

Microcopy above it: `Press and hold to close the gap.`
Microcopy on completion: `Found. That is the whole idea.`

Reduced motion gets the completed state instantly, no hold required.

### 6.2 What we watch

Kicker: `WHAT WE WATCH`

Headline: **Five things, one screen.**

Five cards, each with a hand-drawn SVG icon, all styled identically so no card
reads as more finished than its neighbours.

| Card | Copy |
|---|---|
| Car tracking | Your own vehicle, live, on your phone. Movement alerts the moment it rolls without you. |
| Fleet management | Where every vehicle is, where it has been, how long it idled, who was driving. |
| Fuel monitoring | A sensor in the tank, not a number on a receipt. You see the level drop while it is dropping. |
| Asset tracking | Generators, containers, plant and machinery. Anything worth stealing is worth watching. |
| Vehicle finance | For lenders and dealers. Know the car is where the borrower says it is, before it is a bad debt. |

### 6.3 Fuel is the other theft

Kicker: `FOR FLEET OWNERS`

Headline: **Nobody breaks a window to steal diesel.**

Body: Four hundred litres can leave a tanker in twelve minutes through a pipe
and a row of jerrycans. On the Busia, Malaba and Mutukula routes around forty
tankers a night get hit. Uganda loses somewhere between two hundred and three
hundred billion shillings a year this way, and most of it never looks like a
crime on paper. It looks like a driver's fuel claim.

Body: A tank sensor changes the argument. You are not comparing receipts at the
end of the month. You get a message while the level is falling.

This section carries **generated still 1** (a tanker on a night corridor road
under sodium light).

### 6.4 Where we cover

Kicker: `COVERAGE`

Headline: **The routes your trucks actually run.**

Body: Kampala to Mombasa through Malaba and Nairobi. Kampala north to Juba.
South and west to Kigali and Goma. We track across the border, not up to it.

The **corridor map SVG**, drawn from real coordinates: Mombasa, Nairobi, Malaba,
Kampala, Gulu, Juba, Kigali, Goma, Mbarara, with the four real freight routes.
The route lines draw themselves on scroll. Kampala carries the pulse halo.

### 6.5 Why owners stay with us

Kicker: `WHY US`

Headline: **The tracker is the easy part.**

Body: Ask anyone who has lost a car with a tracker fitted. The device worked.
The problem was that nobody picked up. Our shop is at Kabalagala Market, Shop
15B. We have been there since 2014. When you message that WhatsApp number, a
person in Kampala reads it.

Four proof points, equally weighted:

- `2014` Trading in Kampala since then, at the same market.
- `4` countries covered: Uganda, Kenya, South Sudan, DR Congo.
- `1` WhatsApp number, answered by a person, not a queue.
- `15B` Kabalagala Market. A door you can walk through.

This section carries **generated still 2** (the fitting bay at night, hands at a
dashboard, kept distant and forgiving).

### 6.6 What it costs

Kicker: `PRICING`

Headline: **We quote per vehicle, and we say the number out loud.**

Body: What you pay depends on the unit, whether you want fuel sensing, and how
many vehicles. It is a short conversation, not a form with a hidden total. Send
us what you have and we will send you the price.

Three tiers, each ending in the same request-a-quote chip. **No figures are
invented anywhere on this page.** Every price reads `Request a quote` until Sky
Worth supplies real numbers.

| Tier | Copy |
|---|---|
| One vehicle | A tracker fitted, the app on your phone, movement and ignition alerts. For an owner with a car to protect. |
| Fleet | Everything above across your vehicles, plus trip history, idling, driver behaviour and reports. |
| Fleet with fuel | The fleet package plus tank sensors, so a drop in level reaches you while it is happening. |

### 6.7 The questions people actually ask

Kicker: `STRAIGHT ANSWERS`

Headline: **The five we get every week.**

| Question | Answer |
|---|---|
| What happens when it leaves network coverage? | The unit keeps recording while it is out of range and sends the whole trip the moment it finds signal again. You lose the live view for that stretch. You do not lose the history. |
| Can a thief just disable it? | They can find a unit if they have time and know where to look, which is exactly why the first minute matters so much. Fitting position is deliberately not standard, and movement alerts reach you before anyone has that time. |
| Is a monthly fee worth it when some sellers advertise none? | A tracker with no fee has no SIM and no server behind it, so it can log a trip but it cannot tell you anything while it is happening. You are buying the alert, not the box. |
| Who can see where my car is? | You can. We hold the data to run the service and we do not sell it or hand it to anyone without you or a police case. |
| How long does fitting take? | Most single vehicles are done inside an hour at the shop. For fleets we come to your yard and work through them. |

### 6.8 The close

Kicker: `TALK TO US`

Headline: **Tell us what you drive.**

Body: Send the vehicle and the town. We will tell you what fits it and what it
costs. No callback queue and no sales script.

- Primary: **Message us on WhatsApp** to `+256 703 664 233`, prefilled with
  `Hi Sky Worth, I would like a tracking quote for my vehicle.`
- Secondary: call `0703 664 233`, `0782 390 246`, `0414 671 986`
- The form: name, vehicle or fleet size, town, message.
  - Labels are plain: `Your name`, `What you drive`, `Your town`, `Anything else`
  - Button: `Send it`
  - **Handling: mailto** to `info@sky-worths.com`. There is no backend on a
    static site, so the form opens the visitor's own mail app addressed to Sky
    Worth. The microcopy says so honestly, right under the button: `This opens
    your email app. WhatsApp is faster.` A dead endpoint that silently swallows
    an enquiry is the worse option, and WhatsApp is the real primary anyway.

### 6.9 Footer

Sky Worth Ltd. Kabalagala Market, Shop 15B, Kampala, Uganda. The three phone
numbers, the email, the WhatsApp link. Trading since 2014. No fictional-brand
disclosure, because the brand is real. No AI-imagery note, by the owner's
decision.

---

## 7. The vector layer plan

Everything here is hand-drawn SVG or CSS. No image libraries, no icon fonts.

1. **The pulse, the signature element.** A locator ring with a mono coordinate
   readout beside it. It appears exactly four times: around the vehicle in the
   hero's ending frame, as the interactive moment's ring, on Kampala in the
   corridor map, and at whisper size beside the final CTA. Remove it and the
   page loses its spine and its one interaction, which is the test of a real
   signature. The boldness budget is spent here and nowhere else.
2. **The corridor map**, ported from real lon/lat coordinates. Four route paths
   draw themselves with `stroke-dasharray` as the section enters. City dots fade
   in behind them, staggered.
3. **The descent rule.** A hairline vertical line down the left gutter of the
   premise section that draws downward on scroll, echoing the hero's fall.
4. **Five service icons**, drawn as simple aqua line marks on a shared 24 grid so
   the five read as one set.
5. **The one environment.** A fixed background layer behind everything: a very
   slow drift of faint aqua points over a deep midnight radial, cycling at 90
   seconds, given a negative animation delay so it is mid-cycle at first paint.
   Paused off-screen and on hidden tabs.

All of it honours reduced motion: routes shown fully drawn, counters at target,
the hold interaction complete, every drive stopped.

---

## 8. The engineering list

The build implements all of it, from `scrub-pipeline.md`:

- Video fetched as a **Blob** so seeking works on hosts without Range support.
  Streamed behind an honest loading ring if it lands above about 8 MB, with the
  20-second no-progress watchdog and the still-image fallback.
- The poster painted first, the Blob fetch starting only once the poster is in
  or has failed, with a 4-second safety timer.
- **dt-normalized lerp** in a rAF loop that rests when converged and when the
  hero is off screen, tracked by IntersectionObserver.
- **Gated seeks**, coalescing to the newest target, with the `error` handler
  resetting the flag so the gate cannot deadlock.
- **Delta-gated DOM writes** everywhere, `--k` gated at 0.008, the counter
  throttled to 10Hz and written only when the string changes.
- Band pacing per the standard, validated by the **flick test** at 120, 240 and
  360px steps.
- The **four-layer legibility system**: global base scrim, per-band scrim riding
  `--k`, the three-layer text-shadow token, chip backing for small mono text.
  Audited to at least 3.5:1 against each band's worst frame.
- The **five static-hero gates**, character-for-character identical in CSS and
  JS, armed and disarmed from `change` listeners so a rotation or a preference
  flip never leaves a blank hero.
- **Complete without the video.** Tested by blocking the video URL.
- The quality floor: semantic landmarks, skip link, `aria-hidden` on the
  decorative video and every decoration, `:focus-visible` in the accent, 44px
  touch targets under coarse pointer, real title and meta description,
  `theme-color`, an inline SVG favicon of the pulse mark, and the
  `<!-- DEPLOY STEP -->` comment on the og tags.
- `overflow-x: clip` on both `html` and `body`, with `hidden` first.

---

## 9. The copy gate

Every viewer-facing line above ships **verbatim**. The build wires them in and
never paraphrases.

Before anyone sees the page it must pass the Phase 9 gate: zero em dashes, zero
instances of leverage, seamless, empower, unlock, robust, actionable,
data-driven or solutions, and a clean sweep for the quieter tells, meaning no
"it's not just X, it's Y", no false ranges, no vague attributions, no generic
big finishes, and none of testament, landscape, delve or elevate.

One deliberate device is craft and stays: the staccato triplet in 6.1, "Not
maps. Not reports. Speed." It was chosen here on purpose for this brand.
