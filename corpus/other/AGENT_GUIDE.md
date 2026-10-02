# Email Relay Gateway — How To Use It

A guide for an agent (or developer) that needs to **send email through this
service**. It covers the API contract, the rules that will get a request
rejected, and how to run the service locally if you need one to test against.

If you are changing the service itself rather than calling it, read
`README.md` — it covers architecture, deployment, and the security model.

---

## 1. What this service does

It is a small HTTP → SMTP gateway. You POST a JSON message to it with an API
key; it validates the message and hands it to an internal SMTP relay. It exists
so app servers that can only reach the network over 443/80 can still send mail.

Key consequences for you as a caller:

- **A fixed schema.** Plain text plus an optional HTML alternative, `cc`/`bcc`,
  and attachments limited to `csv`/`xlsx`/`pdf`/`png`/`jpg`/`jpeg`. Images can
  be embedded in the HTML as `cid:` parts. No custom headers, no reply-to, no
  other file types. Unknown fields are rejected.
- **Sending is synchronous.** You get `200` only after the relay accepted the
  message. There is no queue and no server-side retry.
- **It is not an open relay.** The `sender` address must be pre-approved by the
  operator, and the recipient count is capped.

---

## 2. Base URL

All routes live under a base route, `/email_service` by default. The operator
can change it with the `URL_PREFIX` env var (empty = served at the root), so
**confirm the base URL with whoever gave you the API key** rather than assuming.

```
https://<host>/email_service
```

Everything below is relative to that base.

---

## 3. Authentication

Send your key in the `X-API-Key` header on every request to `/send`:

```
X-API-Key: <your key>
```

- Keys are issued per client app server. Do not share or hardcode one — read it
  from the environment (e.g. `EMAIL_GATEWAY_KEY`).
- Never log the key, and never echo it back in output.
- `/healthz` needs no auth. Everything else does.

---

## 4. Endpoints

### `GET /healthz`

No auth. Returns `200`:

```json
{ "status": "ok" }
```

Use it to check the gateway is up. Note it does **not** check the SMTP relay —
a healthy `/healthz` with a failing `/send` means the relay is the problem.

### `POST /send`

Headers:

| Header         | Value                | Required |
| -------------- | -------------------- | -------- |
| `X-API-Key`    | your key             | yes      |
| `Content-Type` | `application/json`   | yes — a missing or wrong content type is read as a non-JSON body and rejected with `422` |

Body — only these fields, no more:

```json
{
  "sender":  "noreply@example.com",
  "to":      ["someone@example.com"],
  "cc":      ["manager@example.com"],
  "bcc":     ["archive@example.com"],
  "subject": "Hello",
  "body":    "Plain-text message body",
  "html":    "<p>Optional HTML alternative</p>",
  "attachments": [
    { "filename": "report.pdf", "content_b64": "JVBERi0xLjQK..." }
  ]
}
```

| Field         | Type            | Rules |
| ------------- | --------------- | ----- |
| `sender`      | string (email)  | Required. Must be a valid address **and** on the operator's allow-list. |
| `to`          | array of emails | Optional on its own, but `to` + `cc` + `bcc` must total **at least 1** and at most `MAX_RECIPIENTS` (default 10) **combined**. `to` and `cc` recipients see each other. |
| `cc`          | array of emails | Optional. Visible in the `Cc:` header. |
| `bcc`         | array of emails | Optional. Delivered but **not** in the transmitted headers — other recipients cannot see them. |
| `subject`     | string          | Required, 1–500 chars. No control characters (no `\n`, `\r`, tabs, etc.). |
| `body`        | string          | Required (may be empty), up to 1,000,000 chars. Always sent as the plain-text part. |
| `html`        | string          | Optional, up to 1,000,000 chars. Sent as an HTML alternative alongside `body`, so always write a sensible `body` too — it is what non-HTML clients show. **Not sanitized**: never interpolate user-supplied content into it. |
| `attachments` | array of objects | Optional. At most `MAX_ATTACHMENTS` (default 5) downloadable files **plus** at most `MAX_INLINE_IMAGES` (default 50) inline images — the two are counted separately. See below. |

Each attachment object:

| Field          | Type    | Rules |
| -------------- | ------- | ----- |
| `filename`     | string  | Required. 1–128 chars, letters/digits/spaces/`.`/`_`/`-`/`()` only, starting with a letter or digit. Must end in `.csv`, `.xlsx`, `.pdf`, `.png`, `.jpg` or `.jpeg` — **no other file types are accepted**. |
| `content_type` | string  | Optional. If given it must match the extension (see the table below). Leave it out and the gateway infers it. |
| `content_b64`  | string  | Required. Standard base64 of the file bytes. Line breaks are tolerated. Decoded size must be ≤ `MAX_ATTACHMENT_MB` (default 5MB) per file and ≤ `MAX_ATTACHMENTS_TOTAL_MB` (default 10MB) across all files, inline images included. |
| `content_id`   | string  | Optional. 1–128 chars of letters, digits, `.`, `_` and `-` only — **no angle brackets, whitespace or control characters**; the gateway adds the `<` `>` itself. Must be unique within the message. Required when `inline` is true. |
| `inline`       | boolean | Optional, default `false`. When true the part is embedded in the HTML rather than offered as a download. Only valid on images (`png`/`jpg`/`jpeg`) and only with a `content_id`. |

Extension → the only `content_type` accepted for it:

| Extension | Content-Type |
| --------- | ------------ |
| `.csv`    | `text/csv` |
| `.xlsx`   | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| `.pdf`    | `application/pdf` |
| `.png`    | `image/png` |
| `.jpg`, `.jpeg` | `image/jpeg` |

### Embedding images in HTML (cid)

Mark each image `"inline": true`, give it a `content_id`, and reference that
same value from the HTML as `cid:<value>`. Angle brackets go in the header, not
in your JSON and not in the `src`:

```json
{
  "sender":  "noreply@example.com",
  "to":      ["ops@example.com"],
  "subject": "Worst potholes - weekly digest",
  "body":    "Plain-text fallback listing each segment.",
  "html":    "<table><tr><td>US-19 seg 01</td><td><img src=\"cid:seg01\"></td></tr></table>",
  "attachments": [
    { "filename": "seg01.jpg", "content_b64": "/9j/4AAQSk...",
      "content_id": "seg01", "inline": true }
  ]
}
```

The gateway does **not** read or rewrite your HTML. It embeds whatever you mark
inline and leaves cid matching to you: a `cid:` with no matching part shows as a
broken image, and an inline part no HTML references travels along invisibly.

Inline images are embedded with `Content-Disposition: inline`, so mail clients
render them in place instead of showing a paperclip. Anything without
`"inline": true` — images included — is a normal downloadable attachment.

Unknown fields are **rejected**, not ignored. Sending `"from"` or `"reply_to"`
will fail the whole request with `422`.

Success — `200`:

```json
{ "status": "sent", "recipients": 1 }
```

If the relay accepted the message but refused some addresses, you still get
`200`, with the refused ones listed and `recipients` counting only the accepted:

```json
{ "status": "sent", "recipients": 2, "refused": ["bad@example.com"] }
```

---

## 5. Error responses

Every error is JSON with an `error` key. Validation failures also carry
`details`.

| Status | Meaning | What to do |
| ------ | ------- | ---------- |
| `401` | Missing or wrong `X-API-Key`. | Fix the key. Do not retry — retrying will never succeed. |
| `403` | `sender` is not on the allow-list. | Use an approved `From` address, or ask the operator to add yours. Do not retry. |
| `413` | Whole request over `MAX_REQUEST_MB` (default 20MB). | Shorten the body or send fewer/smaller attachments. Remember base64 inflates a file by ~33%. Do not retry as-is. |
| `422` | Body wasn't JSON, failed the schema, too many recipients, or an attachment was rejected (bad base64, disallowed type, over a size or count cap, bad/duplicate `content_id`, `inline` on a non-image). | Read `details` (schema failures) or `error` (count and size failures) and fix the payload. Do not retry as-is. |
| `502` | The SMTP relay was unreachable or refused the message. | **This is the one worth retrying** — see below. |

A `422` validation failure looks like:

```json
{
  "error": "validation failed",
  "details": [
    { "field": "to.0", "message": "value is not a valid email address: ..." }
  ]
}
```

### Retry guidance

- Retry **only** on `502` (and on network/timeout errors), with exponential
  backoff — e.g. 3 attempts at 1s, 4s, 16s.
- Never retry `4xx`. The request is malformed or unauthorized; it will fail
  identically every time.
- **Sends are not idempotent.** If a request times out client-side, the relay
  may still have accepted the message. A retry can produce a duplicate email.
  For anything where duplicates matter, log the attempt and surface it to a
  human rather than retrying blindly.

---

## 6. Examples

### curl

```bash
curl -sS -w '\n%{http_code}\n' https://mail-gateway.example.com/email_service/send \
  -H "X-API-Key: $EMAIL_GATEWAY_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "sender": "noreply@example.com",
        "to": ["ops@example.com"],
        "subject": "Deploy finished",
        "body": "All good."
      }'
```

### Python

```python
import base64
import os
import requests

BASE = "https://mail-gateway.example.com/email_service"

def send_email(sender, to, subject, body, cc=None, bcc=None, html=None, files=()):
    payload = {"sender": sender, "to": to, "subject": subject, "body": body}
    if cc:
        payload["cc"] = cc
    if bcc:
        payload["bcc"] = bcc
    if html:
        payload["html"] = html
    if files:  # paths to .csv / .xlsx / .pdf files
        payload["attachments"] = [
            {
                "filename": os.path.basename(path),
                "content_b64": base64.b64encode(open(path, "rb").read()).decode(),
            }
            for path in files
        ]
    resp = requests.post(
        f"{BASE}/send",
        headers={
            "X-API-Key": os.environ["EMAIL_GATEWAY_KEY"],
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,  # the gateway waits on the relay; allow more for attachments
    )
    if resp.status_code != 200:
        raise RuntimeError(f"send failed [{resp.status_code}]: {resp.text}")
    return resp.json()
```

### Node

```js
const res = await fetch(`${BASE}/send`, {
  method: "POST",
  headers: {
    "X-API-Key": process.env.EMAIL_GATEWAY_KEY,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ sender, to, subject, body }),
});
if (!res.ok) throw new Error(`send failed [${res.status}]: ${await res.text()}`);
```

---

## 7. Common mistakes

- **Passing `to` as a string.** It must be an array, even for one recipient.
- **Forgetting `Content-Type: application/json`.** You get a `422` saying the
  body must be JSON, which looks like a payload bug but isn't.
- **Putting a newline in `subject`.** Rejected — it's a header-injection guard.
  Newlines belong in `body`.
- **Adding unsupported fields.** `from` and `reply_to` fail the request
  outright. The service does not support them.
- **Sending HTML with no `body`.** `body` is still required and is what
  non-HTML clients display. An empty one means those recipients see nothing.
- **Attaching the wrong file type.** Only `csv`, `xlsx`, `pdf`, `png`, `jpg`
  and `jpeg` are accepted; anything else is a `422`. Zip it? No — `.zip` isn't
  on the list either.
- **Writing `<...>` into `content_id`.** Send the bare value (`"seg01"`), not
  `"<seg01>"`. The gateway adds the angle brackets when it writes the
  `Content-ID` header; including them yourself is a `422`.
- **Referencing a cid with no matching part.** `<img src="cid:seg01">` with no
  attachment carrying `content_id: "seg01"` sends successfully and renders as a
  broken image. Nothing validates the pairing — generate both from the same
  list. The same applies in reverse: `cid:` in the `src` is the whole reference,
  so `src="cid:<seg01>"` or `src="seg01"` will not resolve.
- **Sending raw bytes in `content_b64`.** It must be base64-encoded text, not
  the file's bytes or a data URI.
- **Assuming the base route.** It's `/email_service` by default, but `/send`
  alone will 404 if the prefix is in place.
- **Putting untrusted content in `html`.** It is passed through unsanitized.

---

## 8. Running it locally (only if you need a test target)

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env    # then edit it
.venv/bin/flask --app app run     # the app package is the entry point
```

`.env` must define `SMTP_HOST`, `API_KEYS`, and `ALLOWED_SENDERS` — the app
raises at startup if any are missing, so misconfiguration fails immediately
rather than at the first send.

For a relay that prints mail instead of delivering it, run Python's debugging
SMTP server in another terminal and point `SMTP_HOST`/`SMTP_PORT` at it:

```bash
python -m aiosmtpd -n -l 127.0.0.1:1025   # pip install aiosmtpd
```

```
SMTP_HOST=127.0.0.1
SMTP_PORT=1025
API_KEYS=local-test-key
ALLOWED_SENDERS=noreply@example.com
```

`insomnia_collection.json` in the repo root imports into Insomnia with the full
set of requests — success, 401, 403, and 422 cases, including cc/bcc, HTML and
attachment coverage — against `{{ base_url }}`. Each request is named with the
status code it should return. Set `base_url`, `api_key`, `sender`, `recipient`,
`cc_recipient` and `bcc_recipient` in the Base Environment first.

---

## 9. Quick reference

```
GET  {base}/healthz                       -> 200 {"status":"ok"}
POST {base}/send   X-API-Key + JSON body  -> 200 {"status":"sent","recipients":N}
                                                 (+ "refused":[...] if partial)
                                             401 bad/missing key
                                             403 sender not allowed
                                             413 request > 20MB
                                             422 bad JSON / schema / >10 recipients
                                                 / bad or disallowed attachment
                                                 / >5 files or >50 inline images
                                             502 relay unreachable   (retry this one)

body: {"sender": "<allowed email>",
       "to": ["<email>", ...], "cc": [...], "bcc": [...],   # >=1 across all three, <=10 total
       "subject": "<1-500 chars, no control chars>",
       "body": "<plain text>",
       "html": "<optional HTML alternative, not sanitized>",
       "attachments": [{"filename": "x.pdf",          # csv|xlsx|pdf|png|jpg|jpeg
                        "content_b64": "<base64>"},    # <=5MB each, <=10MB total
                       {"filename": "pic.jpg",         # embedded in the html as
                        "content_b64": "<base64>",     #   <img src="cid:pic1">
                        "content_id": "pic1",          # bare value, no < >
                        "inline": true}]}              # images only; <=50 inline
```
