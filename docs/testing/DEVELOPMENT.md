# Development Guide

`tgws-manager` is an independent CLI tool managing tg-ws-proxy. Not part of tg-ws-proxy source — completely separate.

## Code Structure

```
src/tgws_manager/
├── cli.py           # Click commands (install, start, stop, status, logs, etc)
├── manager.py       # ProxyManager - core logic (git, subprocess, PID tracking)
├── config.py        # Pydantic config model + file I/O
└── utils.py         # Helpers (colors, subprocess, file ops, port checks)
```

## Key Files

```
~/.tgws-manager/         # Manager config & state
├── config.json
└── proxy.pid

~/.local/tg-ws-proxy/    # Proxy installation (managed by tgws-manager)
└── [full tg-ws-proxy repo clone]
```

## Components

**cli.py** - Click commands: install, start, stop, status, logs, update, config, info, uninstall
**manager.py** - ProxyManager class: git clone, subprocess.Popen, PID tracking, config state
**config.py** - Pydantic ManagerConfig model + file I/O (~/.tgws-manager/config.json)
**utils.py** - Helpers: colors, subprocess, file ops, port checks, Termux detection

## Dependencies

- **click** - CLI framework
- **colorama** - Cross-platform terminal colors
- **pydantic** - Config validation

Install: `pip install -e ".[dev]"` and `pytest`

## Flows

**Install**: Clone repo → install deps → create config
**Start**: Check if running → verify port → subprocess.Popen() → save PID
**Stop**: Read PID → os.kill() → delete PID file
**Update**: git pull → pip install → restart
