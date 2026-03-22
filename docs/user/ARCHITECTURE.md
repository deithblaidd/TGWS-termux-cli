# Architecture

**tgws-manager** and **tg-ws-proxy** are two completely independent tools.

## How They Relate

```
tgws-manager (pip package)          tg-ws-proxy (cloned repo)
├── cli.py                          └── ~/.local/tg-ws-proxy/
├── manager.py   ──manages──>           proxy/tg_ws_proxy.py
├── config.py
└── utils.py

~/.tgws-manager/              ← manager state
├── config.json
└── proxy.pid
```

## Lifecycle

| Command | What happens |
|---------|-------------|
| `install` | `git clone Flowseal/tg-ws-proxy` → `~/.local/tg-ws-proxy/` |
| `start` | `subprocess.Popen(tg_ws_proxy.py)` → saves PID |
| `stop` | `os.kill(PID)` → deletes PID file |
| `update` | `git pull` in proxy dir → reinstall deps → restart |
| `self-update` | `pip install --upgrade tgws-manager` |

## Independence

- Removing tgws-manager does **not** affect the proxy installation
- Removing `~/.local/tg-ws-proxy/` does **not** affect tgws-manager
- You can run the proxy directly: `python ~/.local/tg-ws-proxy/proxy/tg_ws_proxy.py`
- You can update the proxy manually: `cd ~/.local/tg-ws-proxy && git pull`
