#!/usr/bin/env python3
"""Index recent markdown in ~/Downloads, then review it in the browser.

Run it with the environment beside this file, which has the OCI SDK it needs:

    .venv/bin/python corpus_indexer.py

    python corpus_indexer.py

That scans ~/Downloads, classifies anything new with Grok 4.7 at low effort, and
opens the review. Classification runs several files at once. By default it
looks back six months; pass --since to choose the
window, for instance --since 2y, --since 45d or --since 2024-01-01. It only
re-classifies a file when its content changes. Accepting a file imports it on
the spot, and one you have already accepted or rejected is not shown again.

`scan` walks ~/Downloads, skips
vendor documentation and generated trees, and asks Grok 4.7 (low effort, through
OCI Generative AI) to describe each file, name the system it concerns, say
what kind of writing it is, and judge whether it belongs in a corpus shared
with other people at the West Virginia DOT. Results land in corpus.sqlite,
keyed by the file's content hash, so re-running only classifies what is new or
edited. A plain-text log of every decision is appended to corpus.log.

`review` opens a browser on everything classified but not yet accepted or
rejected. Each file is rendered as markdown beside the model's judgement and
its reason. Accepting one imports it immediately — redacted, into corpus/,
with INDEX.md rewritten — and rejecting one records the decision so it is never
asked about again.

Grok is called with the OCI credentials in ~/.oci/config; the compartment id
comes from OCI_GENAI_COMPARTMENT_ID or from ~/Downloads/pms/.env. Nothing here is
committed; review the import, then commit it yourself.
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
DOWNLOADS = HOME / "Downloads"
REPO = Path(__file__).resolve().parent
DB_PATH = REPO / "corpus.sqlite"
LOG_PATH = REPO / "corpus.log"
INDEX_PATH = REPO / "INDEX.md"
CORPUS_DIR = REPO / "corpus"

WINDOW_DAYS = 183
MAX_FILE_BYTES = 750_000          # a markdown file bigger than this is a dump, not a write-up
MAX_DIR_MARKDOWN = 400            # a directory holding more than this many .md files is a doc tree
HEADING_BYTES = 24_000            # how much of a file the model sees

MODEL = "xai.grok-4.7"
EFFORT = "low"
OCI_ENDPOINT = "https://inference.generativeai.us-ashburn-1.oci.oraclecloud.com"
WORKERS = 6                       # files classified at once
PRICE_IN, PRICE_OUT = 2.0, 6.0   # $ per million tokens, OCI Grok 4.7, prompts under 200k

# Directory names that are never worth opening. Matched against any path component.
SKIP_DIRS = {
    "node_modules", ".git", "Pods", "site-packages", "dist", "build", "target",
    ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".dart_tool",
    ".runtime", "gurobi", "fixtures", "forum_dumps", "xdf_examples",
}
# Top-level Downloads directories that are someone else's documentation, shipped
# with a product rather than written here.
VENDOR_ROOTS = {"gurobi", "PcmHammer-develop", "Claim-Compass-extracted", "gmodb"}

SYSTEMS = [
    "thehub", "wvoasis", "dtims", "dot12", "pms", "bms", "inspecttech",
    "awp", "identity-broker", "projectwise", "nexuslrs", "lrs", "foia",
    "mms", "dashcam", "invoice-portal", "hpms", "timekeeper", "other",
]

KINDS = ["documentation", "reverse-engineering", "results", "plan",
         "analysis", "operations", "notes", "other"]

PROMPT = """You are classifying a markdown file from a West Virginia DOT engineer's working files.

Read the excerpt and answer with a single JSON object, nothing else, with exactly these keys:

- "description": one or two sentences on what the file actually says. Name the specific system, table, interface or format it is about. Do not restate the filename.
- "system": the WVDOT system it primarily concerns. One of: {systems}. Use "other" only if none fit.
- "kind": what the file is doing. One of:
    "documentation"        — explains how a system works, for someone else to read
    "reverse-engineering"  — works out an undocumented format, schema, protocol or vendor system
    "results"              — reports measurements, a comparison, an audit or a model run
    "plan"                 — proposes work that has not been done
    "analysis"             — interprets data or behaviour and draws a conclusion
    "operations"           — a runbook, setup guide or deployment checklist
    "notes"                — a scratch pad, a meeting note, a transcript, or a single person's working notes
    "other"
- "share": true only if this would be useful to other people at the West Virginia DOT who do not have the author's other files. A durable explanation, reference, interface spec or finding qualifies. A scratch note, a personal memo, a duplicate, a changelog, a transcript, or anything that names a private individual or quotes internal email does not.
- "share_reason": one sentence on why it should or should not be shared.
- "generated_by_author": true if a person wrote this (including with an assistant), false if it is generated output, a vendored README, a license, a data dump, or a transcript of someone else.

File: {name}
Path: {path}

---
{excerpt}
---"""


# --- logging -----------------------------------------------------------------

def log(msg: str) -> None:
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    print(line, flush=True)
    with LOG_PATH.open("a") as fh:
        fh.write(line + "\n")


# --- database ----------------------------------------------------------------

SCHEMA = """
CREATE TABLE IF NOT EXISTS files (
    sha256        TEXT PRIMARY KEY,
    path          TEXT NOT NULL,
    filename      TEXT NOT NULL,
    bytes         INTEGER NOT NULL,
    mtime         REAL NOT NULL,
    indexed_at    TEXT NOT NULL,
    model         TEXT,
    description   TEXT,
    system        TEXT,
    kind          TEXT,
    share         INTEGER,
    share_reason  TEXT,
    generated     INTEGER,
    prompt_tokens INTEGER,
    output_tokens INTEGER,
    error         TEXT
);
CREATE TABLE IF NOT EXISTS seen (
    path       TEXT PRIMARY KEY,
    sha256     TEXT NOT NULL,
    bytes      INTEGER NOT NULL,
    mtime      REAL NOT NULL,
    scanned_at TEXT NOT NULL,
    outcome    TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reviews (
    sha256      TEXT PRIMARY KEY,
    decision    TEXT NOT NULL,          -- accepted | rejected
    reviewed_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS imported (
    sha256        TEXT PRIMARY KEY,   -- hash of the source, as classified
    dest          TEXT NOT NULL,
    system        TEXT NOT NULL,
    imported_at   TEXT NOT NULL,
    redactions    INTEGER NOT NULL,
    imported_hash TEXT                -- hash of what was written, redaction included
);
"""


def connect() -> sqlite3.Connection:
    # check_same_thread is off because scan() writes from worker threads, each
    # holding the lock around its own statements.
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    return db


# --- discovery ---------------------------------------------------------------

def git_authored(root: Path) -> set[str] | None:
    """Paths this user has committed under root, or None if root is not a repo."""
    name = subprocess.run(["git", "-C", str(root), "config", "user.name"],
                          capture_output=True, text=True).stdout.strip()
    email = subprocess.run(["git", "-C", str(root), "config", "user.email"],
                           capture_output=True, text=True).stdout.strip()
    if not name and not email:
        return None
    who = email or name
    out = subprocess.run(
        ["git", "-C", str(root), "log", "--since", f"{WINDOW_DAYS} days ago",
         f"--author={who}", "--name-only", "--pretty=format:", "--", "*.md"],
        capture_output=True, text=True)
    if out.returncode != 0:
        return None
    return {line.strip() for line in out.stdout.splitlines() if line.strip()}


def parse_since(value: str) -> float:
    """A cutoff mtime from '6m', '45d', '2y', '90' (days) or 'YYYY-MM-DD'."""
    value = value.strip().lower()
    try:
        if value.endswith("d"):
            days = float(value[:-1])
        elif value.endswith("m"):
            days = float(value[:-1]) * 30.44
        elif value.endswith("y"):
            days = float(value[:-1]) * 365.25
        else:
            days = float(value)
    except ValueError:
        return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()
    if days < 0:
        raise argparse.ArgumentTypeError("--since must not be negative")
    return time.time() - days * 86400


def discover(cutoff: float) -> list[tuple[Path, str]]:
    """Markdown worth looking at: (path, why it qualified)."""
    found: dict[Path, str] = {}

    for dirpath, dirnames, filenames in os.walk(DOWNLOADS):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        here = Path(dirpath)
        if here.relative_to(DOWNLOADS).parts[:1] and here.relative_to(DOWNLOADS).parts[0] in VENDOR_ROOTS:
            dirnames.clear()
            continue
        markdown = [f for f in filenames if f.lower().endswith(".md")]
        if len(markdown) > MAX_DIR_MARKDOWN:
            log(f"skip  {here.relative_to(DOWNLOADS)}  ({len(markdown)} markdown files — a doc tree, not a project)")
            continue
        for name in markdown:
            path = here / name
            try:
                st = path.stat()
            except OSError:
                continue
            if st.st_size > MAX_FILE_BYTES or st.st_mtime < cutoff:
                continue
            found[path] = "modified in window"

    # Git knows about edits that did not touch the mtime, and about authorship.
    for root in [p for p in DOWNLOADS.iterdir() if p.is_dir()]:
        authored = git_authored(root)
        if not authored:
            continue
        for rel in authored:
            path = root / rel
            if path in found or not path.is_file():
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            found[path] = "committed by you"

    return sorted(found.items())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


# --- classification ----------------------------------------------------------

def load_env() -> None:
    """Fill in OCI settings from pms/.env when they are not already exported."""
    env = HOME / "Downloads" / "pms" / ".env"
    if not env.is_file():
        return
    for line in env.read_text(errors="replace").splitlines():
        if not line.startswith("OCI_") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        os.environ.setdefault(name.strip(), value.strip().strip('"').strip("'"))


def grok_client():
    """An OCI Generative AI client from ~/.oci/config, or from OCI_* in the environment."""
    import oci
    load_env()
    kw = {"service_endpoint": os.environ.get("OCI_GENAI_ENDPOINT") or OCI_ENDPOINT,
          "retry_strategy": oci.retry.NoneRetryStrategy(), "timeout": (30, 300)}
    env_keys = ("OCI_USER", "OCI_TENANCY", "OCI_FINGERPRINT", "OCI_REGION", "OCI_KEY_CONTENT")
    if all(os.environ.get(k) for k in env_keys):
        cfg = {"user": os.environ["OCI_USER"], "tenancy": os.environ["OCI_TENANCY"],
               "fingerprint": os.environ["OCI_FINGERPRINT"], "region": os.environ["OCI_REGION"],
               "key_content": os.environ["OCI_KEY_CONTENT"].replace("\\n", "\n")}
        return oci.generative_ai_inference.GenerativeAiInferenceClient(config=cfg, **kw)
    config_file = Path(os.environ.get("OCI_CONFIG_FILE") or "~/.oci/config").expanduser()
    if not config_file.is_file():
        sys.exit(f"no OCI credentials: set OCI_USER and friends, or create {config_file}")
    if not os.environ.get("OCI_GENAI_COMPARTMENT_ID"):
        sys.exit("OCI_GENAI_COMPARTMENT_ID is not set, and pms/.env does not have it")
    cfg = oci.config.from_file(str(config_file), os.environ.get("OCI_CONFIG_PROFILE") or "DEFAULT")
    return oci.generative_ai_inference.GenerativeAiInferenceClient(config=cfg, **kw)


def excerpt(path: Path) -> str:
    text = path.read_text(errors="replace")
    if len(text) <= HEADING_BYTES:
        return text
    head, tail = text[: HEADING_BYTES - 4000], text[-4000:]
    return f"{head}\n\n[... {len(text) - HEADING_BYTES:,} characters omitted ...]\n\n{tail}"


def classify(client, path: Path) -> dict:
    import oci
    from oci.generative_ai_inference import models as M
    content = PROMPT.format(systems=", ".join(SYSTEMS), name=path.name,
                            path=path.relative_to(DOWNLOADS), excerpt=excerpt(path))
    request = M.GenericChatRequest(
        api_format=M.BaseChatRequest.API_FORMAT_GENERIC,
        messages=[M.UserMessage(content=[M.TextContent(text=content)])],
        max_completion_tokens=4000, is_stream=False, reasoning_effort="LOW")
    details = M.ChatDetails(
        serving_mode=M.OnDemandServingMode(model_id=MODEL), chat_request=request,
        compartment_id=os.environ["OCI_GENAI_COMPARTMENT_ID"])
    last = None
    for attempt in range(5):
        try:
            response = client.chat(details)
            break
        except oci.exceptions.ServiceError as e:
            last = e
            if e.status not in (429, 500, 502, 503, 504) or attempt == 4:
                raise
            time.sleep((20 * (attempt + 1)) if e.status == 429 else min(30, 3 * 2 ** attempt))
    else:
        raise last
    chat = response.data.chat_response
    message = "".join(part.text for part in (chat.choices[0].message.content or [])
                      if getattr(part, "text", None))
    match = re.search(r"\{.*\}", message, re.S)
    if not match:
        raise ValueError(f"no JSON in reply: {message[:200]!r}")
    parsed = json.loads(match.group(0))
    usage = chat.usage or None
    parsed["_prompt_tokens"] = getattr(usage, "prompt_tokens", 0) or 0
    parsed["_output_tokens"] = getattr(usage, "completion_tokens", 0) or 0
    return parsed


def normalise(raw: dict) -> dict:
    system = str(raw.get("system", "other")).strip().lower()
    kind = str(raw.get("kind", "other")).strip().lower()
    return {
        "description": str(raw.get("description", "")).strip(),
        "system": system if system in SYSTEMS else "other",
        "kind": kind if kind in KINDS else "other",
        "share": 1 if raw.get("share") is True else 0,
        "share_reason": str(raw.get("share_reason", "")).strip(),
        "generated": 1 if raw.get("generated_by_author") is True else 0,
        "prompt_tokens": int(raw.get("_prompt_tokens", 0)),
        "output_tokens": int(raw.get("_output_tokens", 0)),
    }


def record(db: sqlite3.Connection, path: Path, digest: str, row: dict | None, error: str | None) -> None:
    st = path.stat()
    if error is not None:
        db.execute("INSERT OR REPLACE INTO files (sha256, path, filename, bytes, mtime,"
                   " indexed_at, error) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (digest, str(path), path.name, st.st_size, st.st_mtime,
                    datetime.now(timezone.utc).isoformat(), error))
    else:
        db.execute("INSERT OR REPLACE INTO files VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,NULL)",
                   (digest, str(path), path.name, st.st_size, st.st_mtime,
                    datetime.now(timezone.utc).isoformat(), MODEL, row["description"], row["system"],
                    row["kind"], row["share"], row["share_reason"], row["generated"],
                    row["prompt_tokens"], row["output_tokens"]))
    db.commit()


def scan(limit: int | None, cutoff: float) -> None:
    from concurrent.futures import ThreadPoolExecutor
    db = connect()
    grok_client()  # fail here, on the main thread, if OCI isn't configured
    candidates = discover(cutoff)
    todo = []
    for path, why in candidates:
        digest = sha256(path)
        st = path.stat()
        known = db.execute("SELECT 1 FROM files WHERE sha256 = ? AND error IS NULL", (digest,)).fetchone()
        db.execute("INSERT OR REPLACE INTO seen VALUES (?, ?, ?, ?, ?, ?)",
                   (str(path), digest, st.st_size, st.st_mtime,
                    datetime.now(timezone.utc).isoformat(), "known" if known else why))
        if not known:
            todo.append((path, digest))
    db.commit()
    if limit is not None:
        todo = todo[:limit]
    log(f"{len(candidates)} files in scope, {len(todo)} to classify across {WORKERS} workers")

    lock = threading.Lock()
    local = threading.local()

    def one(item: tuple[Path, str]) -> None:
        path, digest = item
        rel = path.relative_to(DOWNLOADS)
        # The OCI client holds a requests session, which isn't safe to share.
        if not getattr(local, "client", None):
            local.client = grok_client()
        try:
            row = normalise(classify(local.client, path))
        except Exception as e:  # noqa: BLE001 - one bad file must not stop the batch
            with lock:
                record(db, path, digest, None, f"{type(e).__name__}: {e}")
                log(f"FAIL  {rel}  {type(e).__name__}: {e}")
            return
        with lock:
            record(db, path, digest, row, None)
            cost = (row["prompt_tokens"] * PRICE_IN + row["output_tokens"] * PRICE_OUT) / 1e6
            log(f"{'SHARE' if row['share'] else 'keep ':<5} {row['system']:<16} "
                f"{row['kind']:<20} ${cost:.4f}  {rel}")
            log(f"       {row['description']}")

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        list(pool.map(one, todo))


# --- redaction ---------------------------------------------------------------
# A value is only replaced when it is a real credential shape, not merely a word
# like "password" near a placeholder. Hosts, database names and usernames alone
# are left alone, matching the policy in CLAUDE.md.

REDACTIONS = [
    ("private key block",
     re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S),
     "<redacted-private-key>"),
    ("connection string with a password",
     re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s/@:]+:[^\s/@]+@", re.I),
     "<redacted-connection-string>"),
    ("SQL password",
     re.compile(r"(?i)(password\s*=\s*)(?!<)[^\s;'\"]+"),
     r"\1<redacted>"),
    ("AWS access key",
     re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
     "<redacted-aws-key>"),
    ("JWT",
     re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
     "<redacted-jwt>"),
    ("bearer token",
     re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]{16,}"),
     r"\1<redacted>"),
    ("API key assignment",
     re.compile(r"(?i)((?:api[_-]?key|access[_-]?key|client[_-]?secret|secret)\s*[=:]\s*['\"]?)"
                r"(?!<)[A-Za-z0-9._~+/=-]{12,}"),
     r"\1<redacted>"),
]


def redact(text: str) -> tuple[str, list[str]]:
    hits = []
    for name, pattern, replacement in REDACTIONS:
        text, n = pattern.subn(replacement, text)
        if n:
            hits.append(f"{n} {name}")
    return text, hits


# --- import ------------------------------------------------------------------

def destination(system: str, filename: str, taken: set[Path]) -> Path:
    folder = CORPUS_DIR / system
    candidate = folder / filename
    if candidate not in taken:
        return candidate
    stem, suffix = Path(filename).stem, Path(filename).suffix
    for n in range(2, 100):
        candidate = folder / f"{stem}-{n}{suffix}"
        if candidate not in taken:
            return candidate
    raise RuntimeError(f"too many files named {filename} under {system}")


def place(db: sqlite3.Connection, row: sqlite3.Row) -> tuple[Path, list[str]] | str:
    """Copy one classified file into corpus/, redacted. Returns (dest, redactions),
    or a short string explaining why it was not copied."""
    src = Path(row["path"])
    if not src.is_file() or sha256(src) != row["sha256"]:
        return "changed on disk since it was classified — re-run scan"
    already = db.execute("SELECT dest, imported_hash FROM imported WHERE sha256 = ?",
                         (row["sha256"],)).fetchone()
    if already:
        dest = REPO / already["dest"]
        if dest.is_file() and already["imported_hash"] and sha256(dest) != already["imported_hash"]:
            return f"kept {already['dest']} — edited by hand since import"
        return f"already imported at {already['dest']}"
    text, hits = redact(src.read_text(errors="replace"))
    taken = {Path(r["dest"]) for r in db.execute("SELECT dest FROM imported")}
    dest = destination(row["system"] or "other", row["filename"], taken)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text)
    db.execute("INSERT INTO imported VALUES (?, ?, ?, ?, ?, ?)",
               (row["sha256"], str(dest.relative_to(REPO)), row["system"] or "other",
                datetime.now(timezone.utc).isoformat(), len(hits), sha256(dest)))
    db.commit()
    write_index(db)
    return dest, hits


def write_index(db: sqlite3.Connection) -> None:
    rows = db.execute("""
        SELECT i.dest, i.system, f.filename, f.kind, f.description, i.redactions
        FROM imported i JOIN files f ON f.sha256 = i.sha256
        ORDER BY i.system, f.filename
    """).fetchall()
    lines = ["# WVDOT Systems Documentation — Corpus Index", "",
             f"_Generated {datetime.now():%Y-%m-%d %H:%M} by `corpus_indexer.py`. "
             "Every file below was classified as worth sharing and scanned for credentials "
             "before it was copied in. Descriptions were written by DeepSeek V4.1 at low effort; "
             "correct one here if it is wrong._", "",
             "| System | File | Kind | What it is |",
             "|---|---|---|---|"]
    for r in rows:
        desc = r["description"].replace("|", "\\|").replace("\n", " ")
        if r["redactions"]:
            desc += f" _(redacted in {r['redactions']} place(s))_"
        link = f"[{r['filename']}]({r['dest']})"
        lines.append(f"| {r['system']} | {link} | {r['kind']} | {desc} |")
    lines += ["", f"_{len(rows)} files._", ""]
    INDEX_PATH.write_text("\n".join(lines))
    log(f"wrote {INDEX_PATH.relative_to(REPO)}  ({len(rows)} files)")


# --- status ------------------------------------------------------------------

def status() -> None:
    db = connect()
    total = db.execute("SELECT COUNT(*) c FROM files WHERE error IS NULL").fetchone()["c"]
    failed = db.execute("SELECT COUNT(*) c FROM files WHERE error IS NOT NULL").fetchone()["c"]
    shared = db.execute("SELECT COUNT(*) c FROM files WHERE share = 1 AND generated = 1").fetchone()["c"]
    imported = db.execute("SELECT COUNT(*) c FROM imported").fetchone()["c"]
    tokens = db.execute("SELECT COALESCE(SUM(prompt_tokens),0) p, COALESCE(SUM(output_tokens),0) o"
                        " FROM files").fetchone()
    cost = (tokens["p"] * PRICE_IN + tokens["o"] * PRICE_OUT) / 1e6
    print(f"classified {total}   failed {failed}   worth sharing {shared}   imported {imported}")
    print(f"tokens in {tokens['p']:,}   out {tokens['o']:,}   estimated cost ${cost:.2f}")
    print()
    for r in db.execute("""
            SELECT system, kind, COUNT(*) n, SUM(share) shared
            FROM files WHERE error IS NULL GROUP BY system, kind ORDER BY n DESC"""):
        print(f"  {r['system']:<16} {r['kind']:<20} {r['n']:>4}   {r['shared']} shareable")


# --- review -------------------------------------------------------------------

REVIEW_PAGE = """<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>Corpus review</title>
<style>
  :root { color-scheme: light dark; }
  * { box-sizing: border-box; }
  html, body { margin: 0; height: 100%; }
  body { font: 15px/1.5 "Iowan Old Style", Palatino, Georgia, serif;
         display: grid; grid-template-rows: auto auto 1fr; height: 100vh; }
  header { display: flex; gap: 18px; align-items: center; padding: 10px 18px;
           border-bottom: 1px solid #d0d0d0; background: #f7f5f1; }
  header .where { flex: 1; min-width: 0; }
  header .where b { display: block; font-size: 15px; }
  header .where span { display: block; color: #666; font: 12px/1.4 ui-monospace, Menlo, monospace;
                       word-break: break-all; }
  #count { color: #888; font-size: 13px; white-space: nowrap; }
  .verdict button { font: 600 13px/1 sans-serif; padding: 6px 12px; border-radius: 99px;
                    border: 1px solid #d0d0d0; background: transparent; cursor: pointer; }
  .verdict button.on { color: #fff; }
  .verdict button[data-v="share"].on { background: #166534; border-color: #166534; }
  .verdict button[data-v="keep"].on { background: #6b7280; border-color: #6b7280; }
  .verdict button[data-v="all"].on { background: #1d4ed8; border-color: #1d4ed8; }
  .folders { display: flex; gap: 6px; align-items: center; padding: 8px 18px;
             border-bottom: 1px solid #d0d0d0; overflow-x: auto; white-space: nowrap; }
  .folders b { font-size: 11px; letter-spacing: .06em; text-transform: uppercase;
               color: #888; margin-right: 6px; }
  .folders button { font: 13px/1 ui-sans-serif, sans-serif; padding: 5px 10px;
                    border-radius: 99px; border: 1px solid #d0d0d0; background: transparent;
                    cursor: pointer; }
  .folders button.on { background: #1d4ed8; color: #fff; border-color: #1d4ed8; }
  .folders button .n { opacity: .7; margin-left: 4px; }
  #stage { display: grid; grid-template-columns: 1fr 320px; min-height: 0; }
  #doc { overflow: auto; padding: 28px 48px 80px; }
  aside { overflow: auto; padding: 22px; border-left: 1px solid #d0d0d0; background: #f7f5f1; }
  @media (prefers-color-scheme: dark) {
    header, .folders, aside { background: #1d1c1a; border-color: #333; }
    body { background: #161513; color: #ece8e1; }
    .answer { background: #262421; }
    article pre { background: #221f1b; }
  }
  .answer { background: #fff; border-left: 3px solid #b45309; padding: 10px 14px; margin: 0 0 16px; }
  .answer b { display: block; font-size: 11px; letter-spacing: .06em;
              text-transform: uppercase; color: #b45309; }
  .answer.no { border-color: #6b7280; }
  .answer.no b { color: #6b7280; }
  dl { display: grid; grid-template-columns: 72px 1fr; gap: 3px 10px; font-size: 13px; margin: 0 0 18px; }
  dt { color: #888; }
  dd { margin: 0; }
  .actions { display: flex; gap: 8px; margin-top: 8px; }
  .actions button { flex: 1; font: 600 15px/1 sans-serif; padding: 12px 0; border-radius: 8px;
                    border: 1px solid #d0d0d0; cursor: pointer; }
  button.accept { background: #166534; color: #fff; border-color: #166534; }
  button.reject { background: transparent; }
  article { font-size: 16.5px; max-width: 820px; }
  article h1, article h2, article h3 { line-height: 1.25; }
  article pre { background: #f4f1ea; padding: 12px 14px; overflow: auto; border-radius: 6px; font-size: 13px; }
  article code { font-size: .9em; }
  article table { border-collapse: collapse; }
  article td, article th { border: 1px solid #ddd; padding: 4px 8px; }
  article img { max-width: 100%; }
  .empty { color: #888; padding: 30vh 0; text-align: center; }
</style>
<header>
  <div class="where"><b id="name">Loading…</b><span id="from"></span></div>
  <span class="verdict" id="verdict"></span>
  <span id="count"></span>
</header>
<nav class="folders" id="folders"></nav>
<div id="stage">
  <main id="doc"><p class="empty">Loading…</p></main>
  <aside id="side"></aside>
</div>
<script>
const doc = document.getElementById("doc"), side = document.getElementById("side");
let queue = [], current = null, busy = false, hidden = new Set(), verdictFilter = "share";

const topDir = (item) => item.relpath.includes("/") ? item.relpath.slice(0, item.relpath.indexOf("/")) : "(Downloads)";
const waiting = () => queue.filter((it) => !hidden.has(topDir(it)) &&
  (verdictFilter === "all" || (verdictFilter === "share") === it.share));
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

// A small markdown renderer. No external script, so the page works offline.
function inline(s) {
  return esc(s)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\\*\\*([^*]+)\\*\\*/g, "<strong>$1</strong>")
    .replace(/(^|\\s)\\*([^*]+)\\*(?=\\s|$)/g, "$1<em>$2</em>")
    .replace(/\\[([^\\]]+)\\]\\(([^)\\s]+)\\)/g, '<a href="$2">$1</a>');
}
function renderMarkdown(src) {
  const lines = String(src).replace(/\\r\\n/g, "\\n").split("\\n");
  let html = "", i = 0;
  const para = (buf) => buf.length ? "<p>" + inline(buf.join(" ")) + "</p>\\n" : "";
  while (i < lines.length) {
    const line = lines[i];
    if (/^```/.test(line)) {
      const buf = [];
      i++;
      while (i < lines.length && !/^```/.test(lines[i])) buf.push(lines[i++]);
      i++;
      html += "<pre><code>" + esc(buf.join("\\n")) + "</code></pre>\\n";
    } else if (/^#{1,6} /.test(line)) {
      const level = line.match(/^#+/)[0].length;
      html += "<h" + level + ">" + inline(line.replace(/^#+\\s+/, "")) + "</h" + level + ">\\n";
      i++;
    } else if (/^\\s*([-*]|\\d+\\.) /.test(line)) {
      const ordered = /^\\s*\\d+\\./.test(line), buf = [];
      while (i < lines.length && /^\\s*([-*]|\\d+\\.) /.test(lines[i]))
        buf.push("<li>" + inline(lines[i++].replace(/^\\s*([-*]|\\d+\\.) /, "")) + "</li>");
      html += (ordered ? "<ol>" : "<ul>") + buf.join("") + (ordered ? "</ol>\\n" : "</ul>\\n");
    } else if (/^\\s*\\|/.test(line)) {
      const rows = [];
      while (i < lines.length && /^\\s*\\|/.test(lines[i])) rows.push(lines[i++]);
      const cells = (r) => r.replace(/^\\||\\|$/g, "").split("|").map((c) => inline(c.trim()));
      const body = rows.filter((r) => !/^\\s*\\|?\\s*:?-+:?/.test(r));
      html += "<table>" + body.map((r, n) => "<tr>" + cells(r).map((c) =>
        (n ? "<td>" : "<th>") + c + (n ? "</td>" : "</th>")).join("") + "</tr>").join("") + "</table>\\n";
    } else if (/^> /.test(line)) {
      const buf = [];
      while (i < lines.length && /^> /.test(lines[i])) buf.push(lines[i++].replace(/^> /, ""));
      html += "<blockquote>" + inline(buf.join(" ")) + "</blockquote>\\n";
    } else if (/^---\\s*$/.test(line)) { html += "<hr>\\n"; i++;
    } else if (line.trim() === "") { i++;
    } else {
      const buf = [];
      while (i < lines.length && lines[i].trim() && !/^(#{1,6} |```|> |---\\s*$|\\s*\\|)/.test(lines[i]))
        buf.push(lines[i++]);
      html += para(buf);
    }
  }
  return html;
}

function folders() {
  const counts = new Map();
  for (const item of queue) counts.set(topDir(item), (counts.get(topDir(item)) || 0) + 1);
  const bar = document.getElementById("folders");
  bar.innerHTML = "<b>Folders</b>" + [...counts].sort((a, b) => b[1] - a[1]).map(([dir, n]) =>
    `<button data-dir="${esc(dir)}" class="${hidden.has(dir) ? "" : "on"}">${esc(dir)}<span class="n">${n}</span></button>`
  ).join("");
  bar.querySelectorAll("button").forEach((b) => b.onclick = () => {
    hidden.has(b.dataset.dir) ? hidden.delete(b.dataset.dir) : hidden.add(b.dataset.dir);
    render();
  });
}

function render() {
  folders();
  const counts = {all: queue.length, share: queue.filter((it) => it.share).length,
                  keep: queue.filter((it) => !it.share).length};
  document.getElementById("verdict").innerHTML = ["all", "share", "keep"].map((v) =>
    `<button data-v="${v}" class="${v === verdictFilter ? "on" : ""}">${
      {all: "All", share: "Share", keep: "Keep"}[v]} ${counts[v]}</button>`
  ).join(" ");
  document.getElementById("verdict").querySelectorAll("button").forEach((b) => b.onclick = () => {
    verdictFilter = b.dataset.v; render(); });
  const item = waiting()[0];
  current = item || null;
  document.getElementById("count").textContent = waiting().length + " left";
  if (!item) {
    document.getElementById("name").textContent = "Nothing left to review";
    document.getElementById("from").textContent = "";
    doc.innerHTML = `<p class="empty">Accepted files are in corpus/ and INDEX.md is current.</p>`;
    side.innerHTML = "";
    return;
  }
  document.getElementById("name").textContent = item.filename;
  document.getElementById("from").textContent = "Downloads/" + item.relpath;
  const says = item.share ? "Yes — share it" : "No — keep it private";
  side.innerHTML = `
    <div class="answer ${item.share ? "" : "no"}"><b>Model says</b>${esc(says)}</div>
    <p>${esc(item.share_reason || "")}</p>
    <dl>
      <dt>System</dt><dd>${esc(item.system || "—")}</dd>
      <dt>Kind</dt><dd>${esc(item.kind || "—")}</dd>
      <dt>Size</dt><dd>${item.kb} KB</dd>
    </dl>
    <p>${esc(item.description || "")}</p>
    <div class="actions">
      <button class="reject" id="no">Reject</button>
      <button class="accept" id="yes">Accept</button>
    </div>
    <p id="count" style="color:#888;font-size:12px">Y / N or arrow keys</p>`;
  doc.innerHTML = `<p class="empty">Loading ${esc(item.filename)}…</p>`;
  fetch("/file?sha=" + item.sha256).then((r) => r.text()).then((text) => {
    if (current !== item) return;
    doc.innerHTML = `<article>${renderMarkdown(text)}</article>`;
    doc.scrollTop = 0;
  }).catch((e) => { doc.innerHTML = `<p class="empty">Could not load the file: ${esc(e)}</p>`; });
  document.getElementById("yes").onclick = () => decide(true);
  document.getElementById("no").onclick = () => decide(false);
}

async function decide(accept) {
  if (!current || busy) return;
  busy = true;
  const res = await fetch("/decide", {method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({sha256: current.sha256, accept})});
  await res.json();
  queue.splice(queue.indexOf(current), 1);
  busy = false;
  render();
}

document.addEventListener("keydown", (e) => {
  if (e.metaKey || e.ctrlKey) return;
  if (e.key === "y" || e.key === "ArrowRight") decide(true);
  if (e.key === "n" || e.key === "ArrowLeft") decide(false);
});

fetch("/queue").then((r) => r.json()).then((items) => { queue = items; render(); })
  .catch((e) => { document.getElementById("name").textContent = "Failed to load the queue";
                  document.getElementById("from").textContent = String(e); });
</script>
</html>"""


def review_queue(db: sqlite3.Connection) -> list[dict]:
    """Files classified but not yet accepted or rejected, model's yes first.
    The markdown itself is fetched one file at a time, so this stays small."""
    rows = db.execute("""
        SELECT f.* FROM files f
        LEFT JOIN reviews r ON r.sha256 = f.sha256
        WHERE f.error IS NULL AND r.sha256 IS NULL
        ORDER BY f.share DESC, f.system, f.filename
    """).fetchall()
    items = []
    for r in rows:
        src = Path(r["path"])
        if not src.is_file():
            continue
        rel = src.relative_to(DOWNLOADS) if src.is_relative_to(DOWNLOADS) else src
        items.append({
            "sha256": r["sha256"], "filename": r["filename"], "relpath": str(rel),
            "system": r["system"], "kind": r["kind"], "share": bool(r["share"]),
            "share_reason": r["share_reason"], "description": r["description"],
            "kb": round(r["bytes"] / 1024),
        })
    return items


def serve_review() -> None:
    import webbrowser
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    db = connect()
    queue = review_queue(db)
    log(f"review  {len(queue)} files waiting")

    class Handler(BaseHTTPRequestHandler):
        def _send(self, code: int, body: bytes, content_type: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/":
                self._send(200, REVIEW_PAGE.encode(), "text/html; charset=utf-8")
            elif self.path == "/queue":
                items = review_queue(connect())
                self._send(200, json.dumps(items).encode(), "application/json")
            elif self.path.startswith("/file?"):
                from urllib.parse import parse_qs, urlparse
                sha = parse_qs(urlparse(self.path).query).get("sha", [""])[0]
                row = connect().execute("SELECT path FROM files WHERE sha256 = ?", (sha,)).fetchone()
                src = Path(row["path"]) if row else None
                if src is None or not src.is_file():
                    self._send(404, b"not found", "text/plain")
                else:
                    self._send(200, src.read_bytes(), "text/plain; charset=utf-8")
            else:
                self._send(404, b"not found", "text/plain")

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/decide":
                self._send(404, b"not found", "text/plain")
                return
            length = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(length) or b"{}")
            conn = connect()
            row = conn.execute("SELECT * FROM files WHERE sha256 = ?",
                               (req.get("sha256"),)).fetchone()
            if row is None:
                self._send(404, b'{"error": "unknown file"}', "application/json")
                return
            accept = bool(req.get("accept"))
            conn.execute("INSERT OR REPLACE INTO reviews VALUES (?, ?, ?)",
                         (row["sha256"], "accepted" if accept else "rejected",
                          datetime.now(timezone.utc).isoformat()))
            conn.commit()
            result: dict = {"ok": True}
            if accept:
                placed = place(conn, row)
                if isinstance(placed, str):
                    result["note"] = placed
                    log(f"accept {row['filename']}  ({placed})")
                else:
                    dest, hits = placed
                    result["dest"] = str(dest.relative_to(REPO))
                    result["redactions"] = hits
                    note = f"  redacted {', '.join(hits)}" if hits else ""
                    log(f"accept {dest.relative_to(REPO)}{note}")
            else:
                log(f"reject {row['filename']}")
            self._send(200, json.dumps(result).encode(), "application/json")

        def log_message(self, fmt: str, *args) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    host, port = server.server_address
    url = f"http://{host}:{port}/"
    log(f"review  {url}  — Y to accept, N to reject, Ctrl-C when you're done")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("review  closed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--since", type=parse_since, default=parse_since("6m"),
                        help="how far back to look: 45d, 6m, 2y, or 2024-01-01 (default 6m)")
    parser.add_argument("--limit", type=int, help="classify at most this many new files, then open the review")
    parser.add_argument("--status", action="store_true", help="print what's been indexed, and stop")
    parser.add_argument("--review", action="store_true", help="open the review without scanning again")
    args = parser.parse_args()
    if args.status:
        status()
        return
    if not args.review:
        log(f"window  back to {datetime.fromtimestamp(args.since):%Y-%m-%d}")
        scan(args.limit, args.since)
    serve_review()


if __name__ == "__main__":
    main()
