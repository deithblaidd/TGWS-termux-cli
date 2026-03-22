# Repository Structure

## tgws-manager

```
tgws-manager/                    https://github.com/deithblaidd/TGWS-termux-cli
├── src/tgws_manager/
│   ├── cli.py               Click commands
│   ├── manager.py           ProxyManager (git, subprocess, PID)
│   ├── config.py            Pydantic config + file I/O
│   └── utils.py             Helpers
├── docs/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── requirements.txt
```

## tg-ws-proxy (external dependency)

```
tg-ws-proxy/                     https://github.com/Flowseal/tg-ws-proxy
└── proxy/
    └── tg_ws_proxy.py
```
Installed by tgws-manager to `~/.local/tg-ws-proxy/`
