# Run Assistant — Logic Reference

The Run Assistant is an admin chat that answers planning questions by running real PMS and BMS studies. It plans a
study, runs it in Python against the AMPS engine, judges the result, runs the next study when the first isn't what
the question needs, saves the runs worth keeping, and writes a short answer. The user guide is
[Run Assistant — Usage](/docs/Run_Assistant_Usage). This page covers how it works.

| Part | Where |
|---|---|
| Agent loop (model steps, tools, events) | `assistant/agent.py` |
| System prompt | `assistant/prompt.py` (+ `analysis_worker/API.md`, verbatim) |
| Run tools (save / read / wait / list) | `assistant/tools.py` |
| Persistence (conversations, turns, events, files) | `assistant/store.py`, migration `054_run_assistant.sql` |
| Settings | `assistant/settings.py`, System → Run Assistant |
| Analysis worker and the `amps` library | `assistant/worker.py`, `assistant/pgproxy.py`, `analysis_worker/` |
| REST + SSE | `api/routes/assistant.py` (`/api/assistant`, admins only) |
| Panel, button, settings page | `ui/src/components/assistant/`, `ui/src/pages/system/RunAssistantAdminPage.tsx` |

## 1. A turn

1. `POST /api/assistant/conversations/{id}/messages {text, context}` calls `agent.start`. It claims the
   conversation (`store.start_turn`: one running turn per conversation and per user, else **409**) and starts a
   daemon thread. The request returns `{turn_id}` at once.
2. The thread appends the question to the conversation's history. The history is kept in Anthropic's message
   format. The question is prefixed with today's date and the page the user is on (`agent.user_turn_text`), so
   the system prompt stays byte-identical and cached.
3. **Model steps.** Each step is one streamed call through Brgzrd's provider functions
   (`bridges/wizard/brigzard._fireworks_turn` for DeepSeek, `_anthropic_turn` for Claude, `_oci_turn` for Grok on
   OCI Generative AI). The step's text, reasoning and tool calls become events. If DeepSeek or Grok fails before
   its first step produced anything and
   *fallback to Claude* is on, Claude answers the question.
4. **Tools.** A step that calls tools runs them in order and appends their results to the history. Then the
   next step starts. The turn ends when a step answers without calling a tool, or on Stop, an error or the step
   limit (`max_tool_iterations`).
5. The thread writes the history after every step. It finishes the turn (status, token usage, cost), marks the
   conversation idle and emits **`done`**. Every exit path emits `done`.

**Stop** sets `assistant_turns.cancel_requested`. A heartbeat thread beats the turn every 3 s and picks up the
flag. The loop stops at the next event or step, and a running Python job is killed. The unanswered tool calls get
"Stopped by the user" results, so the history stays valid.

**Restarts.** A turn whose heartbeat is older than 90 s (`store.STALE_S`) was killed by a restart or deploy.
`store.reap_stale` claims it with one UPDATE, closes it as `interrupted` and emits an `error` and a `done` event.
It runs on the list, conversation and event routes and when a turn starts. The next question repairs any
dangling tool call (`agent.repair_history`).

## 2. Events and the stream

A turn's output exists only as rows in `public.assistant_events`, numbered by `seq` within the conversation.
Text, reasoning and job-output deltas are batched every 0.25 s (`agent.Emitter`), and each event carries `ts`
(epoch seconds).

| kind | data |
|---|---|
| `turn_start` | `{turn_id, question, context, provider, model_label}` |
| `status` | `{message}` |
| `thinking` / `thinking_end` | `{delta}` / `{}` |
| `text` | `{delta}` (markdown) |
| `tool_call_begin` / `tool_call` | `{id, name}` / `{id, name, input}` |
| `job_output` | `{id, text}`: live stdout of a Python job |
| `job_progress` | `{id, message, pct?}`: from `amps.progress()` |
| `tool_result` | `{id, name, ok, summary, elapsed_s, stdout?, error?, files[{file_id, name, mime}], result?, run?{kind, run_id, url, name}}` |
| `error` | `{message}` |
| `done` | `{turn_id, status, elapsed_s, usage, cost_usd}`, where status is `done`, `error`, `stopped` or `interrupted` |

The panel follows `GET /conversations/{id}/events?after=<seq>` (SSE, `id:` = seq):

1. The route replays the stored events after `after`, with consecutive deltas merged.
2. It then polls every 0.3 s while the conversation is running, with a keep-alive every 15 s.
3. It sends `idle` and closes 5 s after the conversation goes idle.

The panel reconnects with the last seq it saw. Because the events are rows, any uvicorn worker can serve the
stream, and closing the panel or the browser never stops an analysis.

How the panel draws them (`ui/src/components/assistant/`):

- Every tool call is a numbered step on the answer's rail (`Transcript.tsx`), titled in plain words with the
  tool's real name and endpoint beside it (`toolCalls.TOOLS`). A Python step lists the `amps` library calls
  found in its code (`toolCalls.libraryCalls`, a regex over `pms.` / `bms.` / `amps.` calls) and keeps every
  `job_progress` line as a log stamped with `ts` relative to the step's start. The status strip
  (`FlightStatus.tsx`) names the step on the go and runs a clock from the question's `turn_start`.
- Links in an answer resolve in `links.resolveHref`: an app path (with or without the base path or this
  host) goes through the router; a bare file name, or a path ending in one, that matches a file saved in this
  chat (`tool_result.files`, latest wins) becomes that file's download (`/api/assistant/files/{file_id}`);
  inline code that is exactly such a file name is linked the same way; other relative links are shown as
  text, not as links to a page that doesn't exist. The prompt tells the model to link files by name.

## 3. Tools

| Tool | What it does |
|---|---|
| `run_python(purpose, code, timeout_minutes)` | Runs the code in the analysis worker (section 4). Returns stdout (the tail, capped), `amps.result()` values, files (stored in `assistant_files`, served by `/api/assistant/files/{id}`) and any traceback. Limited by `max_python_minutes`. |
| `save_pms_run(request)` | `request` is the POST /api/runs body. It goes through `api.routes.runs.create_run` (the New Run dialog's path), so the app validates, stores and runs it. PMS executes one run at a time, so the save first waits until no other PMS run is executing (`tools.wait_for_pms_slot`). The run is then tagged `configuration.assistant = {conv_id, turn_id}`. |
| `save_bms_run(request)` | The POST /api/bms/runs body, through that route's handler. Tagged `config.assistant`. |
| `get_run(kind, run_id)` | A run's status, settings and headline results, per year with calendar years. |
| `wait_for_run(kind, run_id, timeout_minutes)` | Polls a saved run until it finishes. Stop ends the wait; the run keeps going. |
| `list_runs(kind, search, limit)` | Recent runs, and whether the assistant saved them. |

When saving is turned off (`allow_saving_runs`), the save tools refuse. Tool errors go back to the model as error
results, so it can fix the request and retry.

## 4. The analysis worker

The worker runs model-written Python. Nothing the model writes runs in the app process. Each job:

- runs in a fresh process with the repository's engine and BMS code importable and the `amps` helper package
  (`analysis_worker/amps/`, reference in `analysis_worker/API.md`);
- reads the PMS database **read-only**, through a read-only login when one is configured, and always with
  `default_transaction_read_only = on`;
- has no other network, CPU, memory, time and output limits, and no secrets in its environment;
- takes one of a limited number of slots; jobs beyond them queue.

Modes (`ASSISTANT_WORKER`): `off` (the default; `run_python` isn't offered, and the prompt says so), `local`
(development on a Mac, under `sandbox-exec`), and `socket:<path>` (production: the `amps-analysis` container,
with the database reached through the app's Unix-socket forwarder, `assistant/pgproxy.py`). See
`analysis_worker/README.md` for setup and deployment.

## 5. The system prompt

`assistant/prompt.py`. It covers:

- **The persona.** An analyst who restates the question as a study, judges every result and runs the next study
  when needed.
- **The minimum-spend playbook:**
  1. the baseline;
  2. the minimum total cost with MILP-assist `min_cost` and every-year targets;
  3. the smallest flat annual budget by bisection, then the cheapest plan within it;
  4. a horizon check;
  - even spending (`min_year_share`, `min_year_spend`) for "no thin years", and "lower the per-year cap
    until it's no longer feasible" (`pms.min_flat_budget` with every current rule passed through);
  5. saving the runs and reporting their limits.
- **Defaults:** configurations, network presets, federal targets and MIP gap.
- **Follow-ups:** the user's requirements accumulate; the answer shows a checklist of every one, met or not. It builds any linear requirement (`extra_rows`) and calls something impossible only when the solver proves it.
- **Rules:** every figure comes from a tool result; the database is read-only; probes run in Python, and only a plan that meets every requirement is saved;
  plain calendar years, never "FY".
- **The create-run request formats** for PMS and BMS.
- **`analysis_worker/API.md`**, included verbatim.

The prompt is built once per process and cached by the provider. What changes per question goes in the user turn.

## 6. Settings and costs

System → Run Assistant edits one JSON row (`public.assistant_settings`), merged over `assistant/settings.DEFAULTS`
and logged in `assistant_settings_log`:

- the provider, and each provider's model, effort and extra prompt;
- the step and output limits;
- `max_python_minutes`, `allow_saving_runs`, `fallback_to_anthropic`;
- the token prices.

The providers and credentials are Brgzrd's (`ANTHROPIC_API_KEY`, `FIREWORKS_API_KEY`, and for Grok
`OCI_GENAI_COMPARTMENT_ID` with the server's OCI credentials). The header badge reads DS-, GK- or SN-{effort}. Each turn records its
provider, model, token usage and cost in `assistant_turns`. Grok calls carry the chat's id for xAI's prompt cache, ask for `oci_max_output_tokens` (8,000) and are paced under `oci_tokens_per_minute`, as in Brgzrd (see [Bridge Wizard — Logic](/docs/Bridge_Wizard_Logic)).

## 7. Limits and access

- The Run Assistant is for admins only (`require_admin` on every route). Each admin sees only their own
  conversations and files.
- There is one running turn per conversation and per user. The worker's slots cap the Python jobs running at once.
- The studies inherit the engine's limits. For example, MILP-assist plans one treatment per joint over the
  horizon.
