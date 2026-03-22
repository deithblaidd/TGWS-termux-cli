# Architecture

**tgws-manager is completely independent from tg-ws-proxy source code.**

## Two Separate Tools

**tgws-manager**: Python CLI package (pip install)
- Manages proxy lifecycle
- Dependencies: click, colorama, pydantic (NOT tg-ws-proxy)

**tg-ws-proxy**: SOCKS5 proxy implementation
- Cloned to `~/.local/tg-ws-proxy/` by manager
- Can be updated independently

## File Structure

```
User's System
│
├─ Python Environment
│  └─ tgws-manager (pip package)     ← Installed independently
│     ├── cli.py
│     ├── manager.py
│     └── utils.py
│
├─ Home Directory (~/)
│  ├─ .tgws-manager/                 ← tgws-manager's own state
│  │  ├── config.json                 (settings for the manager)
│  │  ├── proxy.pid                   (process tracking)
│  │  └── version.json                (proxy version info)
│  │
│  └─ .local/tg-ws-proxy/            ← tg-ws-proxy installation
│     ├─ proxy/
│     │  └─ tg_ws_proxy.py           (the actual proxy script)
│     ├─ README.md
│     ├─ pyproject.toml
│     └─ .tgws-manager/               (metadata created by manager)
│        ├─ proxy.pid
│        └─ version.json
```

## Independence Guarantee

### Removing tgws-manager
```bash
pip uninstall tgws-manager
```
**Result**: tg-ws-proxy in `~/.local/tg-ws-proxy/` continues to work perfectly.
You can even restart it manually.

### Removing tg-ws-proxy
```bash
rm -rf ~/.local/tg-ws-proxy/
```
**Result**: tgws-manager is still installed and functional.
You can reinstall proxy with `tgws-manager install`.

### Updating tgws-manager
Does NOT touch `~/.local/tg-ws-proxy/` or its configuration.

### Updating tg-ws-proxy
Does NOT require tgws-manager updates. In fact, you can:
```bash
cd ~/.local/tg-ws-proxy/
git pull
```
And tgws-manager will still work fine.

## How tgws-manager Manages tg-ws-proxy

### Installation
1. User: `tgws-manager install`
2. Manager: Clones `https://github.com/Flowseal/tg-ws-proxy` to `~/.local/tg-ws-proxy/`
3. Manager: Installs dependencies (pip install in that directory)
4. Manager: Writes version info to `~/.tgws-manager/version.json`
5. Result: Two separate, independent installations

### Running
1. User: `tgws-manager start`
2. Manager: Launches `~/.local/tg-ws-proxy/proxy/tg_ws_proxy.py` as subprocess
3. Manager: Writes PID to `~/.tgws-manager/proxy.pid`
4. Result: Proxy runs independently; manager tracks it via PID

### Updating Proxy
1. User: `tgws-manager update`
2. Manager: `git pull` in `~/.local/tg-ws-proxy/` directory
3. Manager: Installs dependencies again
4. Manager: Restarts proxy if it was running
5. Result: Proxy is updated; tgws-manager itself unchanged

### Updating Manager
1. User: `tgws-manager self-update` (OR `pip install --upgrade tgws-manager`)
2. pip: Updates the Python package in site-packages
3. Result: Only tgws-manager is updated; proxy untouched

## Command Reference

| Command | Affects What | Notes |
|---------|--------------|-------|
| `tgws-manager install` | tg-ws-proxy | Clones and sets up |
| `tgws-manager start` | tg-ws-proxy | Runs the proxy process |
| `tgws-manager stop` | tg-ws-proxy | Kills the proxy process |
| `tgws-manager update` | tg-ws-proxy | Git pull + install deps |
| `tgws-manager self-update` | tgws-manager | Updates the tool itself |
| `tgws-manager status` | tg-ws-proxy | Checks if running |
| `tgws-manager logs` | tg-ws-proxy | Views proxy logs |
| `tgws-manager config` | tgws-manager | Manages manager settings |
| `tgws-manager uninstall` | tg-ws-proxy | Removes proxy installation |

## Design Decisions

### Why Separate?
- **Modularity**: Manager can be improved without touching proxy code
- **Reusability**: Other proxies could use same manager pattern
- **Stability**: Proxy updates don't break manager
- **Flexibility**: Users can manage proxy manually if needed

### Why Clone to ~/.local/?
- **Standard**: Follows Unix convention for user-local software
- **Isolated**: Separate from system packages
- **Discoverable**: Users can inspect/modify if needed
- **Portable**: Works offline if cloned already

### Why Use Git?
- **Version Control**: Easy to track and update
- **Reproducible**: Can checkout specific versions
- **Source Available**: Users can inspect code
- **Works Offline**: Can update from local mirror

## Advanced Usage

### Direct Proxy Access
Users can work directly with the proxy if needed:
```bash
cd ~/.local/tg-ws-proxy/
python proxy/tg_ws_proxy.py --custom-flags
```

### Manual Updates
Proxy can be updated without tgws-manager:
```bash
cd ~/.local/tg-ws-proxy/
git pull
pip install -r requirements.txt
```

### Backup Strategy
Both are independent, so each has separate backup needs:
- **Backup tgws-manager**: Not critical (reinstall via pip)
- **Backup tg-ws-proxy**: Only if you've customized it

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    User's Terminal                       │
│                      (Termux)                            │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ runs command
                       ↓
        ┌──────────────────────────────┐
        │     tgws-manager CLI          │
        │  ($ tgws-manager start)       │
        └──────────┬───────────────────┘
                   │
        ┌──────────┴────────────┐
        │                       │
        ↓                       ↓
   ┌─────────────┐      ┌────────────────────┐
   │   Manager   │      │  Proxy Process     │
   │  (Python)   │      │  (~/.local/...)    │
   └─────────────┘      └────────────────────┘
        │                       │
        │                       │
        ├─→ tracks via PID      │
        ├─→ reads .config.json  │
        ├─→ manages .pid files  │
        │                       │
        └───────┬───────────────┘
                │
        ┌───────┴──────────────────────┐
        │   ~/.tgws-manager/           │
        │   (manager's state)          │
        └──────────────────────────────┘
                
        ┌────────────────────────────┐
        │   ~/.local/tg-ws-proxy/    │
        │  (proxy's installation)    │
        └────────────────────────────┘
```

## Troubleshooting Independence Issues

### "I want tg-ws-proxy but not tgws-manager"
Simply don't install tgws-manager. Manually:
```bash
git clone https://github.com/Flowseal/tg-ws-proxy
cd tg-ws-proxy
pip install -r requirements.txt
python proxy/tg_ws_proxy.py
```

### "I want tgws-manager but different proxy location"
```bash
tgws-manager install --path /custom/path
```

### "tgws-manager broke my proxy"
Unlikely, but if so:
```bash
# Restore proxy manually
cd ~/.local/tg-ws-proxy/
git status  # See what changed
git restore .  # Restore to clean state
```

### "I updated proxy manually, will tgws-manager work?"
Yes! tgws-manager just:
- Checks for running process by reading PID file
- Launches/kills the proxy script
- Reads git version info

It doesn't validate proxy integrity, so manual changes work fine.

## Future Enhancements

- [ ] Support for multiple proxy instances
- [ ] SystemD service integration
- [ ] Automatic restarts on crash
- [ ] Web dashboard (separate tool)
- [ ] Metrics/monitoring (separate tool)
- [ ] Config templates library

All of these would remain independent from both tgws-manager and tg-ws-proxy.
