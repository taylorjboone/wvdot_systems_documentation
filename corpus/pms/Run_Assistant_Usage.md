# Run Assistant — usage

The **Run Assistant** answers planning questions about the pavement (PMS) and bridge (BMS) networks by
running the analyses itself. Ask it something like *"How much do we need to spend to keep non-Interstate NHS
at ≤5% Poor and ≥45% Good every year for 10 years?"* and it:

1. works out what the question needs (network, targets, years, configuration);
2. writes Python that runs the real optimizer on today's network and starting condition (the same engine as
   the runs on the Runs page);
3. looks at the result and decides whether it answers the question well. For example, a minimum total cost
   that spends almost everything in the first four years is a true minimum but not a budget anyone would
   adopt, so it goes on to find the smallest **flat** annual budget, or checks a longer horizon;
4. explains what it found, with the figures, the charts and the limits of the analysis;
5. saves the analyses worth keeping as ordinary runs you can open, compare and validate.

It is available to **admins**. Years are calendar years: Year 1 is the run's start year (for example 2026).

## Opening, resizing and closing

- The **Run Assistant** button is at the top right of the blue bar, left of your avatar. Click it (or press
  **Alt+Shift+A**) to open the panel on the right; click it again, the **×** in the panel, or the shortcut to
  close it.
- The panel sits beside the page rather than over it: the page narrows to make room, so you can keep working
  on a run or a Validate board while the assistant works.
- **Drag the panel's left edge** to make it wider or narrower (from 360 px up to 70% of the window).
  Double-click the edge to go back to the standard width. With the edge focused, the ← and → keys resize it.
- The panel stays open as you move between pages, and remembers its width and the chat you were in.

## Asking

- Type a question and press **Enter** (Shift+Enter starts a new line), or pick one of the examples on a new
  chat.
- The assistant knows which page you asked from. On a run's page, "this run" means that run; on a bridge
  page, that bridge.
- Be as specific as you like about the network (Interstate, NHS, non-Interstate NHS, Non-NHS, a district,
  WVDOT-owned bridges), the targets (% Good, % Poor, LISA, deck area in Poor), the years and the
  configuration. Anything you leave out, it chooses and says what it chose.
- Follow-up questions continue the same chat: "now do it over 15 years", "what if we held it to $60M a
  year?", "save that one as a run".

## What you see while it works

The panel is a dark "flight deck" where colour means state: **cyan** is the assistant working, **amber** is
Python running in the analysis worker, **green** a step that finished, **red** one that failed.

- The **status strip** under the header says what is happening now: *Engaged* with the step on the go
  ("Step 3: Running Python in the analysis worker", or "Thinking") and a clock since you asked (`T+ 03:12`).
  Idle, it says *Standing by* and whether the analysis worker is up (without it the assistant can talk but
  can't run Python).
- The working steps of each answer hang off a **rail** on the left. Every tool call the assistant makes is a
  numbered step, lit in its state's colour and pulsing while it runs.
- Each step names the tool it called, beside a plain-language title: `run_python` (Python in the sandboxed
  worker: it reads the database but can't change it, and has no internet), `save_pms_run → POST /api/runs`,
  `save_bms_run → POST /api/bms/runs`, `get_run`, `wait_for_run` or `list_runs`.
- A **Python step** shows:
  - What the job is for.
  - The parts of the AMPS library its code calls, in words (for example `pms.load_network()` "Load the
    pavement network" and `pms.optimize() ×2` "Run the MILP optimizer").
  - While it runs: an amber progress bar, a **progress log** where every progress line the job reports is
    stamped with the clock since the step began (`T+ 00:13  MILP step 1 · feasibility …`), and the live tail
    of its output.
  - When it ends: whether it succeeded and how long it took, any charts inline and any tables as downloads.
    **Code**, **Progress** and **Output** unfold the code (with a copy button), the whole progress log and
    the full output.
- A **saved run** is a green link on its step (`Run 384`, `BMS run 12`). Runs the assistant saves are tagged
  **Run Assistant**. The quick checks it runs along the way (feasibility probes, budget searches) stay in the
  chat.
- **Reasoning** (collapsed) is the model's working; open it to see why it chose a step.
- The answer follows, clear of the rail, with the figures in tables. Links in it open the run or page they
  name (the panel stays open), and a link to a file one of its steps saved (`routes_404_vs_395.xlsx`)
  downloads that file. The line under the answer says how long the question took and what it cost.

A single optimization can take from a few seconds to tens of minutes. The assistant runs one Python job at a
time per chat; if every analysis slot on the server is busy, its job waits its turn.

## It keeps working in the background

The analysis runs on the server, not in your browser:

- Close the panel, go to another page, or close the browser: the analysis carries on.
- While one of your analyses is running, a gold ring turns around the **Run Assistant** button. When one
  finishes while the panel is closed, a gold dot waits on the button until you open it.
- Reopen the panel and the chat catches up with everything that happened.
- If the server restarts during an analysis (for example a deploy), the chat says it was **interrupted**; ask
  again to continue (the chat keeps everything it had found).

You can have one analysis running at a time. Starting another while one runs tells you which chat is busy.

## Stopping

While it works, the **Send** button becomes **Stop**. Stopping ends the question at the next step and stops a
running Python job; what it had finished stays in the chat, and runs it had already saved stay saved.

## Your chats

The chat name under **Run Assistant** in the panel header opens **Your chats**: every conversation, newest
first, with the running one marked. Pick one to open it, or use the pencil to rename it and the bin to delete
it (a running chat can't be deleted). **New chat** (the speech-bubble button) starts a fresh conversation.
The small badge in the header shows the model answering, as on the Brgzrd page: **DS-low** is DeepSeek at
low effort, **GK-low** is Grok at low effort, **SN-high** is Claude Sonnet at high effort (hover for the effort).

## What it can and can't do

- It reads the pavement and bridge data **read-only**. Its Python runs in a separate, locked-down worker with
  no internet access, so it can't change inventory, configurations or anyone's runs. The only thing it
  creates is new runs, through the same path as **New Run**.
- Its analyses use the same condition models, costs and optimizer as the app, so a result it reports and the
  run it saves agree.
- Its answers are as good as the question and the model: check the saved runs before using a figure in a
  budget request. The limits it states (for example "one treatment per joint over the horizon",
  "nominal dollars at 2% inflation") matter.

## Settings (System → Run Assistant)

Admins choose, on **System → Run Assistant**:

- **Model**: DeepSeek on Fireworks (the default), Claude, or Grok (xAI Grok 4.7 on OCI Generative AI), each
  provider's model and effort, and extra
  instructions for each. A switch applies from the next question.
- **Limits**: the most tool calls per question, the longest output, the **longest Python job** (1–60
  minutes), whether it may **save runs**, and whether Claude answers when DeepSeek or Grok fails to start.
  For Grok, also **Grok max output tokens** and **Grok tokens per minute** (the OCI limit calls are paced under;
  while waiting, the chat shows "Pacing Grok…").
- **Analysis worker**: whether it is running and how many job slots are busy.
- **Prices** used to cost each question, and the **change history** (who changed what, when).

Every change saves by itself.
