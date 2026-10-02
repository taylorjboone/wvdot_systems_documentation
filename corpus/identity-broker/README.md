# WVDOT portal — infrastructure

## Files

| Path on the boxes | Source here | Mode |
|---|---|---|
| `/etc/apache2/portal.conf` | `portal-apache.conf` | 644 |
| `/etc/apache2/portal-oidc.conf` | **not in git** — holds the client secret | **600** |
| `/var/www/portal/{index.html,apps.json,robots.txt,assets/}` | repo root | 644 / 755 |
| `~/ops/portal-sync.sh` | `portal-sync.sh` | 755 |

`portal.conf` is `Include`d in **five** vhosts, immediately before each catch-all
`ProxyPass /`: prod `:80` and `:443`; dev `:80` and both `:443` vhosts. The `:80`
vhosts do not redirect to HTTPS, and dev's `mms.transportation.wv.gov:443` is the
SNI default server — all five matter.

`portal-oidc.conf` is `IncludeOptional`-ed from `apache2.conf` (server scope,
because the OIDC provider settings are not per-vhost).

## Sign-in

The portal is an OIDC relying party of the identity broker at
`https://ocidev.transportation.wv.gov/auth`, which fronts Entra/SAML. The app
never speaks SAML — see `RELYING_PARTY_INTEGRATION.md`.

- Client name: **`wvdot-portal`**
- Client id: **`cl_LHwh3TN7B0dDMTS0`**
- Secret: issued once at registration; lives only in `/etc/apache2/portal-oidc.conf`
  on both boxes. If it is ever lost, register a new client — it cannot be re-read.
- Registered callbacks (strict equality, both pre-registered):
  - `https://mmsdev.transportation.wv.gov/portal-auth/callback`
  - `https://mms.transportation.wv.gov/portal-auth/callback`

`OIDCRedirectURI` is written as a **path**, so mod_auth_openidc builds the absolute
URL from whichever hostname the request arrived on. That is why one client serves
both environments.

Gated: `/` and `/apps.json`. Public on purpose: `/robots.txt` (a crawler must be
able to read the disallow) and `/portal-assets/` (fonts reveal nothing).

Everyone who signs in is treated as an administrator — the portal has no roles of
its own, and the card grid is the same for every user.

Requires `libapache2-mod-auth-openidc` (2.4.1 from focal/universe), installed on
both boxes. Two directives differ from the upstream docs on this version:
`OIDCPKCEMethod` has no `none` value (omit it to disable PKCE, which this broker
requires) and `OIDCCookieSameSite` takes `On`/`Off`, not `Lax`.

## Refreshing the card dates

```sh
~/ops/portal-sync.sh            # dry run
sudo ~/ops/portal-sync.sh --write
```

Uses `max(changelog date, deployed git commit date)`, falling back to the image
date. The max matters: MMS's `CHANGELOG.json` is frozen at 2026-05-16 while its
code ships monthly.

## Rollback

Remove the `Include /etc/apache2/portal.conf` lines (or restore the dated
`.bak.portal-*` backup of the vhost file) and `systemctl reload apache2`. `/`
returns to a gunicorn 404. To drop only the sign-in but keep the portal, delete
the three `<LocationMatch>`/`<Location>` blocks from `portal.conf`.
