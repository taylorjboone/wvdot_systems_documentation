# Proposal: Integrating DOT12 with wvOASIS

**Prepared for:** West Virginia Division of Highways
**Subject:** A safe, supervised path for getting DOT12 data into wvOASIS without waiting on a custom integration
**Status:** Draft for review

---

## Executive summary

DOT12 already collects, validates, and stores the field data the state needs in wvOASIS — labor hours, equipment usage, materials, and the supporting daily work reports. Today that data is keyed into wvOASIS by hand, a second time, by people who already entered it once.

We propose closing that gap with a **supervised data-entry assistant**: a small, audited piece of software that signs into wvOASIS the same way an employee does, fills in the screens using data that has already been validated in DOT12, and then **stops and waits for a human to press the approve button**. No transaction is ever finalized without a person reviewing it.

This is not a workaround or a hack. It is the same pattern the IRS, the U.S. Treasury, the Army, and GSA use for entering data into their own legacy financial systems. It is governed by published federal security standards. We are proposing to apply that same playbook here.

The result: the people who do the work key it once, into DOT12. The people who own the books keep their final approval authority in wvOASIS. The double entry goes away.

---

## A note on the planned wvOASIS upgrade

We are aware that wvOASIS has a platform upgrade on its roadmap. This proposal is still worth doing, for two reasons.

First, the value of removing double entry accrues every pay period between now and whenever the upgrade lands — and ERP upgrades of this size historically slip. Waiting forfeits real savings for an uncertain date.

Second, this approach **outlives the upgrade**. The assistant is built in deliberately thin layers: the part that knows DOT12, the part that knows how to safely sign in and type, and a small layer of "screen recipes" that describes what the wvOASIS pages look like. When the upgrade ships, only that last layer changes. The work to update it is on the order of days, not months — substantially less than building the integration in the first place. We have planned for this from day one rather than treating it as an afterthought.

In short: the upgrade is not a reason to delay; if anything, the upgrade is a reason to have a working pattern in place first, so the team has a known-good baseline to update against rather than starting fresh on a new platform.

---

## The problem we are solving

wvOASIS is West Virginia's enterprise system of record for finance, HR, timesheets, and procurement. Like most state ERPs of its generation, it does not expose a modern integration layer that an outside application can reliably push data into. The practical options today are:

1. Wait years and spend significantly for a custom integration project with the vendor.
2. Continue to have field staff or office staff key the same information twice — once into the systems where work actually happens, and again into wvOASIS.
3. **Bridge the two systems with a supervised, audited assistant that uses the existing wvOASIS web interface, exactly the way a person would.**

Option 3 is what large public-sector and private-sector organizations have been doing for the better part of a decade. It is well understood, well governed, and reversible.

---

## How it would work, in plain language

Think of it as hiring a very fast, very accurate, very tired-of-typing data-entry clerk, who:

- **Has their own employee ID.** The assistant signs in with its own account, not a borrowed login. Every action it takes is traceable to that account, and that account is registered to a named human supervisor.
- **Only works from data that has already been validated.** It pulls from DOT12, where the foreman, the timekeeper, and the supervisor have already reviewed the entries. It does not invent anything. It does not free-text anything.
- **Reads the entry back after it types it.** Every time it enters a row, it goes back and re-reads the screen to confirm wvOASIS recorded what it just typed. If anything is off by a penny or a digit, it stops and flags the row for a human.
- **Never presses "submit and finalize."** It can fill out screens. It can save drafts. It cannot post the transaction. The human who is accountable for the entry — the same person who would have approved a hand-keyed entry — clicks the final button.
- **Keeps a full receipt.** Every action is logged with timestamps, the source row in DOT12, the resulting record in wvOASIS, and a screenshot of the final screen before the human approved it. If an auditor ever asks "where did this number come from," we can show them the chain back to the original field report.

If wvOASIS is ever down, ever changes a screen, or ever sees something the assistant doesn't recognize, the assistant stops and hands off to a person. It does not guess.

---

## Why this is safe

We want to be direct about the risk question, because financial and timesheet data is rightly treated with care. Here is why this approach is not the scary version of automation people sometimes picture.

| Concern | How this proposal addresses it |
|---|---|
| "A bot is moving money / hours without oversight." | The assistant cannot finalize anything. The same human who approves a manual entry today still presses the approve button tomorrow. |
| "If it makes a mistake, we won't know." | Every entry is read back from wvOASIS and compared to the source. Mismatches halt the queue and notify a person. Nothing silent. |
| "We won't know who did what." | Each action is tied to a named bot account, which is in turn registered to a named human sponsor. Every action is logged with a screenshot. The audit trail is **better** than manual entry because nothing is forgotten. |
| "What if wvOASIS changes?" | A small daily "canary" run does a known round-trip every morning. If the vendor changes a field, we know within hours, before the nightly batch ever runs. |
| "What if the data in DOT12 is wrong?" | DOT12 already validates field data at entry time. The assistant only touches rows that have passed validation and been approved internally. Garbage in is caught before this stage, not after. |
| "Could it be hacked?" | The assistant runs in a dedicated, locked-down environment, not on a person's laptop. Its credentials are stored in a vault. It is treated, governed, and patched like any other production system. |

In short: the assistant has **less** authority than any state employee with a wvOASIS login, because it cannot complete a transaction. It is a typist, not a signatory.

---

## Who else does this

This is not novel. It is the operating model of the federal government's automation program, and it is the operating model of most large enterprises that depend on legacy ERPs. A short, deliberately public-sector list:

- **Internal Revenue Service.** The IRS publishes Privacy Impact Assessments for its automations. One of them, the SBSE AM18 / AMS Closure Tool, is documented as a bot that signs into the **Individual Master File** — the 1960s-vintage mainframe of record for every individual taxpayer account in the United States — and performs case actions by mimicking what a human agent would do. The IRS is on a published path of 35–50 new automations of this kind per year.
- **U.S. Department of the Treasury, Bureau of the Fiscal Service.** Has publicly reported that automating seven legacy reconciliation processes saved roughly 9,000 staff hours per year, equivalent to four full-time employees. The blog post is on `fiscal.treasury.gov`.
- **U.S. Army.** A documented automation logs into both the current and legacy Army ERP systems, downloads loan repayment program data from each, reconciles them, and emails the result to the program owner. Two ERPs, no API between them, bridged by an automation.
- **General Services Administration (GSA).** Runs an enterprise automation platform that other agencies can use as a shared service. A documented automation enters credit-card purchase data into GSA's financial system — about 22,000 transactions per year — only after a three-person human approval chain. This is structurally identical to what we are proposing here.
- **Government Accountability Office (GAO).** The federal government's own auditor is a customer of GSA's automation platform. If the agency that audits everyone else uses this pattern internally, the pattern is defensible.
- **Federal Automation Community of Practice.** A government-wide group with more than 1,700 members across 100-plus federal agencies. They publish an annual *State of Federal Automation* report and a use-case inventory that, in 2025, contained more than 3,000 documented automations of this general kind.

On the private side, the same pattern is the foundation of the entire Robotic Process Automation industry — UiPath, Automation Anywhere, and Blue Prism are publicly traded companies whose customers do exactly this against SAP, Oracle E-Business Suite, PeopleSoft, JD Edwards, Lawson, Infor, and a long list of other legacy systems. Banks do it for core banking systems. Hospitals do it for older electronic medical record systems. It is, at this point, a mainstream operating practice.

We are proposing to apply that same well-trodden pattern to a single, narrow, well-validated use case.

---

## What the assistant would actually do, end to end

A typical day, in order:

1. A foreman submits a daily work report in DOT12. Hours, equipment, materials, location.
2. The supervisor reviews and approves the report inside DOT12, the way they do today.
3. Overnight, the assistant pulls the approved reports from DOT12. Anything not approved is left alone.
4. For each report, the assistant signs into wvOASIS using its own account and enters the corresponding timesheet, equipment usage, and material consumption screens, line by line.
5. After each line, the assistant re-reads the saved screen and compares it to DOT12. If anything is off, it pauses that row and routes it to a person.
6. Once all the rows for a report are entered cleanly, the assistant leaves the entry in wvOASIS in **pending / unapproved** state and notifies the responsible approver.
7. The approver opens wvOASIS the next morning, reviews the pending entries — exactly as they would review a hand-keyed entry — and clicks approve.
8. The approval, the bot's actions, and the original DOT12 source are all stitched together in an audit log that the controller's office can pull at any time.

If anything goes wrong at any step, the system stops, not silently retries. Nothing is destructive. Nothing is irreversible.

---

## Implementation plan

We propose a phased rollout to keep risk low and let the controller's office build comfort.

**Phase 1 — Read-only shadow (1 week).**
The assistant signs into wvOASIS, navigates the screens, and reads back the entries that were keyed manually that day. It then checks them against DOT12 and produces a daily reconciliation report. Nothing is written. The only output is a report. This proves the assistant can navigate wvOASIS reliably and that DOT12 and wvOASIS agree on what they are seeing.

**Phase 2 — Single pilot district, single form (6–8 weeks).**
The assistant begins entering data for one district and one form type — most likely Form 148 timesheets — into wvOASIS, leaving everything in pending state. The district's existing approver clicks the final button. We measure: error rate, time saved per report, and exception rate.

**Phase 3 — Expansion (ongoing).**
Once the pilot is steady for a defined period (say, 60 days with no material exceptions), we expand to additional districts and additional form types — equipment usage, material consumption, and so on — one at a time, with a defined go / no-go gate at each step.

At any point, if the controller's office wants to pause, the assistant is turned off and the previous manual process resumes the next day. There is no lock-in.

---

## Governance and controls

To make this defensible to internal audit, the state auditor, and any future external review, the assistant will be operated under the following controls, which mirror federal practice (OMB Memorandum M-19-17 and the GSA RPA Security Guide CIO-IT-Security-19-97):

- **Named bot account, named human sponsor.** The assistant has its own wvOASIS user, not a person's. That account is registered to a specific named employee who is accountable for it.
- **Credential vault.** The bot's password and any tokens are stored in a managed secrets vault, not in code or on a workstation.
- **Dedicated host.** The assistant runs on a dedicated, hardened virtual machine, not on a staff laptop. It is patched on the same cadence as any production server.
- **Full audit log.** Every action is logged with the bot account, the human sponsor, the source DOT12 record, the destination wvOASIS record, timestamps, and a final screenshot.
- **Read-back verification.** Every write is followed by a read; any mismatch halts that item.
- **Human approval gate.** No transaction is finalized by the assistant. A human always presses the final button.
- **Daily canary.** A small known round-trip runs every morning to detect changes in wvOASIS before they affect production runs.
- **Kill switch.** A single configuration change disables the assistant. The manual process resumes immediately.
- **Quarterly control review.** The controller's office and IT review the audit log and exception report on a defined cadence.

---

## What we are asking for

1. **Approval to proceed with Phase 1.** A read-only shadow run is the cheapest way to confirm this works in our environment, and it carries no risk to wvOASIS data.
2. **A named sponsor in the controller's office** who will own the bot account and approve the audit-control package.
3. **A wvOASIS account for the assistant**, scoped to the minimum permissions needed for the targeted screens.
4. **A defined exception-routing process** — i.e., when the assistant pauses a row, who picks it up?

We are not asking for a budget commitment beyond Phase 1. The decision to expand is gated on the pilot's measured results.

---

## Recommendation

The data the state needs is already being collected, validated, and approved in DOT12. The only thing missing is a safe, supervised way to move it across the last mile into wvOASIS without asking people to type it twice.

The approach in this proposal is conservative by design. It cannot finalize a transaction. It cannot invent data. It cannot operate without an audit trail. It can be turned off in one step. And it is the same approach the IRS, the Treasury, the Army, GSA, and the GAO all use against their own legacy systems of record.

We recommend approving Phase 1 and beginning the read-only shadow run.

---

## References (for the curious)

- GSA RPA Playbook — `tech.gsa.gov/playbooks/rpa/`
- GSA RPA Security Guide, CIO-IT-Security-19-97 Rev 3 (Feb 2023) — `gsa.gov`
- OMB Memorandum M-19-17, *Enabling Mission Delivery through Improved Identity, Credential, and Access Management* — `whitehouse.gov`
- Federal Automation Community of Practice — `digital.gov/communities/rpa/`
- Federal RPA Use Case Inventory (3,000+ documented automations) — `gsa.gov` / `digital.gov`
- IRS Privacy Impact Assessment, SBSE AM18 / AMS Closure Tool RPA — `irs.gov/pub/irs-pia/`
- U.S. Treasury Bureau of the Fiscal Service, *Everything You Want to Know About RPA* — `fiscal.treasury.gov/fit/blog/`
- ACT-IAC, *RPA in Federal Agencies: How Federal Agencies Achieve More Through Robotic Process Automation* — `actiac.org`
- GSA Office of Inspector General, *GSA Should Strengthen the Security of Its Robotic Process Automation Program* (audit A230020) — `gsaig.gov`
