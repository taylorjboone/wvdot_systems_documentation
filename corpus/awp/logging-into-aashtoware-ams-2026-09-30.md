# Logging into AASHTOWare AMS

> Instance: `wvdot-pr-prod` (WVDOT production) · Verified working: 2026-09-30

## Overview

The WVDOT instance of AASHTOWare AMS (web UI: `wvdot-pr-prod.infotechinc.com`, hosted by Infotech) exposes a REST API through the shared gateway at `https://api.aashtoware.org/ams`. Authentication has two parts:

1. **Subscription key** — an HTTP header sent on *every* request; identifies the integration to the API gateway.
2. **Integration authorization token** — obtained once by POSTing user credentials to `/integration_authorization_token`, then sent as a Bearer token on subsequent API calls.

## Credentials

All values live in `.env` in this folder — do not commit it (`.gitignore` already excludes it).

| Variable | Description |
|---|---|
| `AMS_API_BASE_URL` | API gateway base URL (`https://api.aashtoware.org/ams`) |
| `AMS_WEB_URL` | AMS web UI (`https://wvdot-pr-prod.infotechinc.com`) — not used by API calls |
| `AMS_SUBSCRIPTION_KEY` | Subscription / integration key (secret) |
| `AMS_INTEGRATION_NAME` | Instance name used in token requests (`wvdot-pr-prod`) |
| `AMS_USERNAME` | AMS account email (secret) |
| `AMS_PASSWORD` | AMS account password (secret) |

## The authorization endpoint

```
POST {AMS_API_BASE_URL}/integration_authorization_token
```

### Request headers

| Header | Value |
|---|---|
| `Content-Type` | `application/json` |
| `Ocp-Apim-Subscription-Key` | subscription key (`AMS_SUBSCRIPTION_KEY`) |

### Request body

| Field | Required | Description |
|---|---|---|
| `IntegrationName` | Yes | Instance name — `wvdot-pr-prod` |
| `IntegrationSecret` | Yes | The subscription key (same value as the header) |
| `Username` | Yes | AMS account email |
| `Password` | Yes | AMS account password |

```json
{
  "IntegrationName": "wvdot-pr-prod",
  "IntegrationSecret": "<AMS_SUBSCRIPTION_KEY>",
  "Username": "<AMS_USERNAME>",
  "Password": "<AMS_PASSWORD>"
}
```

Equivalent curl:

```bash
curl -X POST "https://api.aashtoware.org/ams/integration_authorization_token" \
  -H "Content-Type: application/json" \
  -H "Ocp-Apim-Subscription-Key: <AMS_SUBSCRIPTION_KEY>" \
  -d '{
    "IntegrationName": "wvdot-pr-prod",
    "IntegrationSecret": "<AMS_SUBSCRIPTION_KEY>",
    "Username": "<AMS_USERNAME>",
    "Password": "<AMS_PASSWORD>"
  }'
```

### Success response (200)

The body is a **raw base64-encoded string — not JSON**:

```
<base64-encoded-token>
```

Decoded, it has the form `instance:token`:

```
<instance-name>:<token-value>
```

Use the full base64 string as the Bearer token — pass it through unchanged.

### Error responses

| Status | Cause |
|---|---|
| 400 | Missing or wrongly named fields (e.g. `instanceName`, `integratorKey`) |
| 401 | Invalid credentials or subscription key |

A real 400 from using the wrong field names (`instanceName` / `integratorKey` instead of `IntegrationName` / `IntegrationSecret`):

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
  "title": "One or more validation errors occurred.",
  "status": 400,
  "errors": {
    "IntegrationName": ["The IntegrationName field is required."],
    "IntegrationSecret": ["The IntegrationSecret field is required."]
  }
}
```

## Using the token

Every subsequent API call needs **both** headers:

| Header | Value |
|---|---|
| `Ocp-Apim-Subscription-Key` | subscription key |
| `Authorization` | `Bearer <token>` |

## Token lifetime and caching

- Each call to the endpoint returns a fresh token — request one per session and cache it in memory; don't hardcode.
- Lifetime is about 8 hours; the sample service caches for 7.5 hours so it refreshes 30 minutes before expiry.

## Working Python example

`ams_auth.py` in this folder contains the full service:

```python
import base64
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import requests


class AmsAuthenticationService:
    """Handles authentication for AASHTOWare AMS API"""

    def __init__(self, subscription_key: str, base_url: str = "https://api.aashtoware.org/ams"):
        self.base_url = base_url
        self.subscription_key = subscription_key
        self.current_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None
        self.session = requests.Session()
        self.session.headers.update({
            "Ocp-Apim-Subscription-Key": subscription_key,
            "Content-Type": "application/json"
        })

    def get_token(self, username: str, password: str, instance: str) -> str:
        """Obtain authentication token from AMS API, with caching."""
        if (self.current_token and
                self.token_expiry and
                datetime.utcnow() < self.token_expiry):
            return self.current_token

        token_request = {
            "IntegrationName": instance,
            "IntegrationSecret": self.subscription_key,
            "Username": username,
            "Password": password
        }

        response = self.session.post(
            f"{self.base_url}/integration_authorization_token",
            json=token_request
        )

        if response.status_code == 200:
            self.current_token = response.text.strip().strip('"')
            self.token_expiry = datetime.utcnow() + timedelta(hours=7.5)
            return self.current_token
        raise Exception(f"Authentication failed: {response.status_code} - {response.text}")

    def get_authenticated_session(self, username: str, password: str, instance: str) -> requests.Session:
        """Returns a session with the Authorization header set."""
        token = self.get_token(username, password, instance)
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        return self.session
```

Usage with `.env` (with `python-dotenv`: `pip install python-dotenv`, then `from dotenv import load_dotenv; load_dotenv()`):

```python
import os
from ams_auth import AmsAuthenticationService

auth = AmsAuthenticationService(
    subscription_key=os.environ["AMS_SUBSCRIPTION_KEY"],
    base_url=os.environ["AMS_API_BASE_URL"],
)
session = auth.get_authenticated_session(
    username=os.environ["AMS_USERNAME"],
    password=<redacted>"AMS_PASSWORD"],
    instance=os.environ["AMS_INTEGRATION_NAME"],
)
response = session.get(f"{os.environ['AMS_API_BASE_URL']}/<endpoint>")
```

`test_env.py` verifies the `.env` end-to-end (loads it, gets a token, prints it truncated):

```bash
python3 test_env.py
```

## Gotchas

1. **Field names are PascalCase**: `IntegrationName`, `IntegrationSecret`, `Username`, `Password`. The commonly circulated sample code uses `instanceName` / `integratorKey` and fails with a 400.
2. **The subscription key is sent twice** — once in the `Ocp-Apim-Subscription-Key` header and once as `IntegrationSecret` in the body.
3. **The response is a raw base64 string**, not a JSON object — `response.json()["access_token"]` raises. Use `response.text.strip()`.
4. **The token decodes to `instance:token`**, but pass the full base64 string as the Bearer value.
5. **The instance name comes from the web domain**: `wvdot-pr-prod.infotechinc.com` → `wvdot-pr-prod`.
6. **Both the subscription key and Bearer token are required** on API calls — either alone is not enough.

## Files

| File | Purpose |
|---|---|
| `ams_auth.py` | Corrected `AmsAuthenticationService` (token caching + authenticated session) |
| `.env` | Credentials — never commit |
| `.gitignore` | Excludes `.env` |
| `test_env.py` | Verifies `.env` → token works end-to-end |
| `test_final.py` | Tests token retrieval, caching and session setup |
