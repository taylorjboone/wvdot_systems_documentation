# DOT-12 User Analytics — Deep Dive

*1,034,359 events · 266 users · 14,020 sessions · May 20 – Aug 6, 2026 (90-day retention window) · prod, dev accounts excluded at ingest*

---

## 1. Adoption has gone vertical — and it's sticking

Weekly actives sat at **20–24 users** through the June pilot, then the July
rollout took them **122 → 168 → 199 → 226** in five weeks — a 10× jump with
week-over-week growth still positive. Retention is the stronger signal: **96%
of the 192 users first seen in July were still active in the last 14 days**
(June pilot cohort: 66%). Segmentation of the last 30 days: **122 daily
regulars** (15+ active days), 53 weekly, 81 occasional. Half the user base has
made this a daily ritual within weeks of first touch.

## 2. The workday has two humps — and they tell you who your users are

Cell-entry volume by hour (ET) is sharply bimodal: a **6–8 AM spike** (85k
entries) and a **2–4 PM spike** (77k), with a deep valley at 11 AM–noon.
That's the timekeeping rhythm of a road agency: office staff keying
yesterday's forms first thing, and crews/supervisors entering at end of shift
(7:00–3:30 schedules). The 5 AM column (6.4k entries from 40 users) is real —
early crews — and the 5–7 PM tail (29k entries) shows supervisors finishing
paperwork after crews go home. Nothing meaningful moves at 2–4 AM: no bots,
no offshore anomalies, just West Virginia's actual workday.

## 3. Tuesday is the system's heartbeat

Tuesday beats every other day — 230 distinct users and 1,341 submits over 60
days (vs ~950 midweek average) — and the daily pulse shows why: the Mon/Tue
after each pay-period close (07/27–28: 296+358 submits; 08/04: 362) are the
biggest days in the system. The **pay-period grace-week crunch is visible from
orbit**. Weekends aren't dead either: ~30 users file ~60 submits per Saturday
— summer crews entering same-day rather than saving it for Monday, which is
exactly the behavior the tool exists to enable.

## 4. A small clerical core carries the load — the $7.7M story, confirmed in behavior

The top decile of users (26 people) generates **43.6% of all events**; the top
two deciles, two-thirds. And the role table makes it concrete: 36
`time_entry_approval` users produced **247k events — nearly as much as all 134
creators combined** (6.9k events/user vs 3.2k). The people this app is
heaviest for are precisely the timekeeping clerical layer from the labor
analysis. Every workflow improvement aimed at them has ~25× the per-seat
leverage of one aimed at the median user.

## 5. The app already absorbs ~15 FTEs of working time

Measured page dwell over the last 30 days: **1,711 hours in the form editor**,
799 in the forms list, ~2,700 tracked hours total — ≈15 full-time-equivalents
of monthly working time now flowing through the interface. Median session is
4.8 minutes but the mean is 46 (p90 = 93 min): the population is bimodal —
quick check-ins and marathon timekeeping sessions — matching the two-hump day.

## 6. Forms are a team sport: ~10 opens per form

The median form takes 31 cell entries, but averages **9.9 separate opens** —
crew chief drafting, timekeeper correcting, approver reviewing, HRM entering.
The DOT-12 isn't a document, it's a *conversation*, and the workflow data
shows the conversation is fast: **92.6% of forms approved, median 4.6 hours
from prepared→approved**, and the median form is prepared **0.76 days after
the workday it covers**. Same-day truth is no longer aspirational — it's the
observed median. (The p90 of 65 hours = weekend gaps.)

## 7. What's winning and what's flopping, feature-wise

- **Winning:** search (95 users, 6.5k uses), templates (66 users applying,
  605 applies), Org View (112 users, 47 hours) — the daily-driver loop.
- **Quietly excellent:** rejections are just **1.7% of submits** (87 vs
  5,206) — validation and auto-fill are catching problems before approvers do.
- **Flopping:** the **Wizard (17 users, 24 opens)** — the guided-creation flow
  isn't earning its place; templates beat it 25:1. Report exports (16 users)
  and FMSUS (0.7h dwell) are niche. Accomplishment View (17 users) is doing
  its intended narrow dTIMS-keyer job.
- **Underused hand-off:** Timesheet Accounting logged only **7.2 hours across
  70 users** — the OASIS-facing surface is barely touched compared to the 1,711
  hours upstream of it. The re-entry burden still lives outside the app; this
  is the upstream-OASIS opportunity, quantified.

## 8. This is still mostly a District 7 story

D7 accounts for 163 of the ~250 org-linked active users; D4's second wave is 68;
D2 is nascent (11). Statewide numbers should be read as *D7+D4 at scale, eight
districts to go* — meaning current volume (≈4,000 forms and ~2,700 in-app hours
per month) plausibly **5–8×** at full rollout, and infrastructure and support
planning should assume it.

---

### Caveats
- 90-day event retention: "all-time" = since May 20.
- District figures join through org membership; multi-org users count in each.
- Dwell time = tracked page_time (tab-visible), an undercount of true usage.
- High retention partly reflects a mandated tool; the signal is in the *daily-regular* share and voluntary-feature uptake, which are strong on their own.
