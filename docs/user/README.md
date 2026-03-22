# tgws-manager

Independent CLI tool that manages `tg-ws-proxy` on Termux.

- **tgws-manager** — management tool (this repo)
- **tg-ws-proxy** — the actual SOCKS5 proxy ([Flowseal/tg-ws-proxy](https://github.com/Flowseal/tg-ws-proxy))

See [QUICKSTART.md](QUICKSTART.md) to get started.

## Quick Commands

```bash
tgws-manager install              # download & setup tg-ws-proxy
tgws-manager start                # start proxy (default port 1080)
tgws-manager status               # check if running
tgws-manager logs -f              # live logs
tgws-manager stop                 # stop proxy
tgws-manager update               # update proxy
tgws-manager config --show        # view config
```

**Full reference:** [USAGE.md](USAGE.md)

## Configuration

Settings stored at `~/.tgws-manager/config.json`:

```json
{
  "proxy_path": "~/.local/tg-ws-proxy",
  "git_url": "https://github.com/Flowseal/tg-ws-proxy",
  "auto_start": false,
  "last_port": 1080,
  "last_host": "127.0.0.1"
}
```

## File Locations

```
~/.local/tg-ws-proxy/      # Proxy installation (from GitHub)
~/.tgws-manager/           # Manager configuration
  ├── config.json
  ├── proxy.pid
  └── logs/
      └── proxy.log
```

## Architecture

Both components are completely independent:

```
Your Termux Device
│
├─ tgws-manager              ✓ Can be removed/updated separately
│  └─ Manages (git clone + process control)
│     └─ ~/.local/tg-ws-proxy/   ✓ Can run without manager
│        └─ Runs as background process
│
├─ ~/.tgws-manager/          ← Manager config only
│  ├── config.json
│  ├── proxy.pid
│  └── version.json
│
└─ ~/.local/tg-ws-proxy/     ← Proxy installation (independent)
   ├── proxy/
   │  └── tg_ws_proxy.py
   └── .tgws-manager/version.json
```

**Key point**: Removing tgws-manager or updating it won't affect the proxy installation. They're completely decoupled.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Rust build errors | `pkg install -y rust` |
| Port already in use | `tgws-manager start --port 9999` |
| Permission denied | `chmod -R 755 ~/.local/tg-ws-proxy ~/.tgws-manager` |
| Command not found | `pip install -e .` in tgws-manager directory |

## Testing with Docker

Quick local testing (requires Docker):

```bash
make setup       # Build & start
make shell       # Enter container
make test        # Run tests
make clean       # Cleanup
```

See [DOCKER-QUICKSTART.md](DOCKER-QUICKSTART.md) for details.

## Learn More

- [QUICKSTART.md](QUICKSTART.md) — 30 seconds to running
- [INSTALL.md](INSTALL.md) — Installation guide
- [USAGE.md](USAGE.md) — All commands & options
- [ARCHITECTURE.md](ARCHITECTURE.md) — Design & independence
- [DOCKER-QUICKSTART.md](DOCKER-QUICKSTART.md) — Docker testing

## License

MIT
