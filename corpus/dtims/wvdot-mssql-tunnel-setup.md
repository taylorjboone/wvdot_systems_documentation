# WVDOT MSSQL Tunnel — Setup Guide

A persistent SSH tunnel that lets tools on this box (`mms-dev`, `10.0.0.83`) reach the
WVDOT Data-Warehouse SQL Server, which is **not** directly reachable from here.

---

## 1. Why this is needed

The WVDOT Data-Warehouse lives at `10.69.0.44:1433` (named host `dotb6pwsql`, which does
not resolve here). That network (`10.69.0.0/16`) is reached over the VCN's DRG, but the
WVDOT-side firewall only trusts the source IP of **`cpu-test` (`10.0.0.172`)** — not this box.

| Path | Reachable? |
|------|-----------|
| this box (`10.0.0.83`) → `10.69.0.44:1433` | ❌ no |
| `cpu-test` (`10.0.0.172`) → `10.69.0.44:1433` | ✅ yes |
| this box → `cpu-test:22` (SSH) | ✅ yes |

So we relay through `cpu-test`: an SSH tunnel forwards a local port here to the SQL Server
*via* `cpu-test`.

> **Port note:** local port `1433` on this box is already taken by an **unrelated Docker
> SQL Server**. We therefore use **`11433`** for the tunnel to avoid the conflict.

### Architecture

```
  list.py / any client
        │  TCP 127.0.0.1:11433
        ▼
  ┌──────────────┐   SSH (22)   ┌───────────────┐  TCP 1433  ┌──────────────────┐
  │  mms-dev      │ ───────────▶ │  cpu-test      │ ─────────▶ │ WVDOT MSSQL       │
  │ 10.0.0.83     │              │ 10.0.0.172     │            │ 10.69.0.44:1433   │
  │ :11433 (local)│              │ (relay)        │            │ Data-Warehouse    │
  └──────────────┘              └───────────────┘            └──────────────────┘
```

---

## 2. Prerequisites

- SSH access from this box to `ubuntu@10.0.0.172` using key `~/.ssh/id_cputest`.
- The security list on the `ai_development` subnet must allow this box's IP
  (`10.0.0.83`) to reach `cpu-test` on **TCP 22**.
- `pymssql` installed for `list.py` (`pip install pymssql`).
- `sudo` on this box (to install the systemd service).
- `cpu-test` must be **running** — the whole tunnel depends on it.

Verify SSH and end-to-end reachability before building the service:

```bash
# 1. SSH to the relay works
ssh -i ~/.ssh/id_cputest -o BatchMode=yes ubuntu@10.0.0.172 'echo OK; hostname'

# 2. The relay can reach the WVDOT SQL Server
ssh -i ~/.ssh/id_cputest ubuntu@10.0.0.172 \
  'timeout 6 bash -c "cat </dev/null >/dev/tcp/10.69.0.44/1433" && echo REACHABLE'

# 3. Local 11433 is free (1433 is the Docker SQL Server — leave it alone)
ss -ltnp | grep ':11433' || echo "11433 free"
```

---

## 3. Create the systemd service

This makes the tunnel **start on boot** and **auto-reconnect** after drops.

Create `/etc/systemd/system/wvdot-mssql-tunnel.service`:

```ini
[Unit]
Description=SSH tunnel: localhost:11433 -> WVDOT MSSQL 10.69.0.44:1433 via cpu-test (10.0.0.172)
After=network-online.target
Wants=network-online.target

[Service]
User=ubuntu
# -N no shell, -T no tty. Keepalives detect dead links; ExitOnForwardFailure
# makes a failed/half-open forward exit so systemd restarts a clean tunnel.
ExecStart=/usr/bin/ssh -NT \
  -o BatchMode=yes \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -o ExitOnForwardFailure=yes \
  -o StrictHostKeyChecking=accept-new \
  -o TCPKeepAlive=yes \
  -i /home/ubuntu/.ssh/id_cputest \
  -L 127.0.0.1:11433:10.69.0.44:1433 \
  ubuntu@10.0.0.172
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Key options explained**

| Option | Purpose |
|--------|---------|
| `-L 127.0.0.1:11433:10.69.0.44:1433` | Bind local `11433`, forward to the SQL Server via the relay. Bound to `127.0.0.1` only — not exposed on the network. |
| `-N -T` | No remote command, no TTY — pure tunnel. |
| `ServerAliveInterval=30` / `CountMax=3` | Detect a dead link within ~90s and drop, so systemd restarts. |
| `ExitOnForwardFailure=yes` | If the forward can't bind, exit instead of sitting half-open. |
| `Restart=always` / `RestartSec=5` | systemd respawns the tunnel 5s after any exit. |

Enable and start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now wvdot-mssql-tunnel.service
sudo systemctl status wvdot-mssql-tunnel.service --no-pager
```

---

## 4. Point `list.py` at the tunnel

`list.py` defaults to the tunnel so a bare run "just works":

```python
p.add_argument("--server", default="127.0.0.1")   # local tunnel endpoint
p.add_argument("--port",   type=int, default=11433)
```

Run it:

```bash
python3 list.py            # lists tables/views via the tunnel
python3 list.py --counts   # include row counts
```

Expected first line: `Connected to Data-Warehouse @ 127.0.0.1:11433`.

Any other client works the same way — point it at `127.0.0.1,11433`, e.g.:

```bash
sqlcmd -S 127.0.0.1,11433 -U DTIMS_Transactions -P '<password>' -d Data-Warehouse
```

---

## 5. Verify

```bash
# listener present, bound to localhost
ss -ltnp | grep ':11433'

# end-to-end query through the tunnel
python3 list.py | head -3

# auto-restart works: kill the tunnel, confirm it returns within ~5s
sudo kill -9 "$(pgrep -f '11433:10.69.0.44:1433')"
sleep 8
ss -ltnp | grep ':11433' && echo "tunnel came back"
```

---

## 6. Managing the service

```bash
sudo systemctl status   wvdot-mssql-tunnel     # current state
sudo systemctl restart  wvdot-mssql-tunnel     # restart
sudo systemctl stop     wvdot-mssql-tunnel     # stop (and free 11433)
sudo systemctl start    wvdot-mssql-tunnel     # start
sudo systemctl disable  wvdot-mssql-tunnel     # don't start on boot
journalctl -u wvdot-mssql-tunnel -f            # live logs
```

---

## 7. Troubleshooting

| Symptom | Likely cause / fix |
|---------|--------------------|
| `CONNECT FAILED ... 127.0.0.1:11433` | Tunnel down. `systemctl status`; check `cpu-test` is running. |
| Tunnel won't start, logs show `connection refused`/`timeout` to `10.0.0.172` | `cpu-test` is stopped, or this box's IP was dropped from the subnet's port-22 allowlist. |
| `Login failed for user 'DTIMS_Transactions'` | You're hitting the **local Docker** SQL Server on `1433`, not the tunnel — make sure you use port **11433**. Or the WVDOT password changed. |
| Works, then dies after a while | Network blip; systemd should restart within 5s. Check `journalctl` for a restart loop. |
| `bind: Address already in use` | Something else grabbed `11433`. `ss -ltnp | grep 11433` and pick a new port (update the unit **and** `list.py`). |

---

## 8. Security notes

- The tunnel binds **`127.0.0.1` only** — not reachable from other hosts.
- The DB password is currently **hardcoded in `list.py`**. Consider an env var or a
  secrets file instead.
- `~/.ssh/id_cputest` is unencrypted (required for an unattended service). Keep it
  `chmod 600` and owned by `ubuntu`.
- This tunnel's reach is bounded to a single destination (`10.69.0.44:1433`), not a
  general SOCKS proxy — intentional, to limit blast radius.

---

*Endpoints: relay `ubuntu@10.0.0.172` (cpu-test) · target `10.69.0.44:1433` (WVDOT
Data-Warehouse) · local `127.0.0.1:11433` · service `wvdot-mssql-tunnel`.*
