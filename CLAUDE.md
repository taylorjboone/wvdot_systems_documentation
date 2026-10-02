# WVDOT Systems Documentation

Markdown write-ups about WVDOT systems (TheHub, AWP, OASIS, engineering
databases, …). These docs are pushed to a shared remote, so they must never
carry credentials.

## Before every commit: check the Markdown for secrets

Do this every time you commit, without being asked. Do not commit until it
passes.

1. Look at what is staged — every `.md` file, the whole file if it is new,
   the added lines if it is modified:

   ```sh
   git diff --cached --name-only --diff-filter=ACMR -- '*.md'
   git diff --cached -U0 -- '*.md'
   ```

2. Grep the staged content for likely secrets, then read every hit in context
   (the grep is a first pass, not the check — also read the diff yourself):

   ```sh
   git diff --cached -U0 -- '*.md' | grep -nEi \
     'password|passwd|pwd *[=:]|secret|api[_-]?key|access[_-]?key|token|bearer |authorization:|client[_-]?secret|private key|BEGIN [A-Z ]*PRIVATE KEY|user id *=|uid *=|://[^/ :@]+:[^/ @]+@|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{10,}\.'
   ```

3. Treat as a secret, and block the commit on:
   - passwords, including ones inside connection strings
     (`Server=…;User Id=…;Password=…`, `postgres://user:pass@host/db`)
   - API keys, access keys, bearer/JWT/session tokens, cookies
   - OIDC/OAuth client secrets (e.g. for the identity broker at
     `ocidev.transportation.wv.gov`), SAML signing keys, certificates' private keys
   - anything copied from a `.env`, `appsettings*.json`, `web.config` or
     similar config file with real values in it

   Not secrets on their own — fine to commit: hostnames, server IPs,
   database / schema / table names, usernames without a password, and
   placeholder values like `<password>` or `****`.

4. If something is found: replace the value with a placeholder
   (`<redacted>`, `<THEHUB_SQL_PASSWORD>`), re-stage, re-run the check, and
   tell me what was redacted and where. If you are unsure whether a value is
   real, ask before committing.

5. If a secret was already committed in an earlier commit, editing the file
   is not enough — tell me so the credential can be rotated and the history
   cleaned. Do not rewrite history or force-push on your own.
