# Quick Start: tgws-manager on Termux

**tgws-manager** is a standalone tool that **independently manages** tg-ws-proxy.

## 30-Second Setup

```bash
# 1. Install tgws-manager (the management tool)
git clone https://github.com/deithblaidd/TGWS-termux-cli
cd TGWS-termux-cli
pip install -e .

# 2. Install the proxy
tgws-manager install

# 3. Start it
tgws-manager start

# 4. Done! Check status
tgws-manager status
```

## Daily Commands

```bash
# Start proxy (runs in background)
tgws-manager start

# Check if running
tgws-manager status

# View live logs
tgws-manager logs -f

# Stop when done
tgws-manager stop

# Update to latest
tgws-manager update
```

## Common Scenarios

### Custom Port
```bash
tgws-manager start --port 9999
```

### Listen on All Interfaces
```bash
tgws-manager start --host 0.0.0.0
```

### Custom Data Centers
```bash
tgws-manager start --dc-ip 2:149.154.167.220 --dc-ip 4:149.154.167.220
```

### Verbose/Debug Mode
```bash
tgws-manager start -v
```

### Check Logs
```bash
# Last 50 lines
tgws-manager logs

# Last 100 lines
tgws-manager logs -n 100

# Follow live
tgws-manager logs -f
```

## File Locations

```
Config:     ~/.tgws-manager/config.json
Proxy:      ~/.local/tg-ws-proxy/
PID file:   ~/.tgws-manager/proxy.pid
```

## Troubleshooting

### "Command not found: tgws-manager"
```bash
pip install -e .
```

### "Port already in use"
```bash
tgws-manager start --port 1081
```

### Rust compilation error
```bash
pkg install -y rust
tgws-manager install --rebuild
```

## What's Happening?

- **tgws-manager**: CLI tool (pip package)
- **~/.local/tg-ws-proxy/**: Your proxy installation (independent)
- **~/.tgws-manager/**: Configuration & state files

The CLI tool is completely independent from the proxy—you can update/remove one without affecting the other.

## Features

✅ Install from GitHub
✅ Start/stop service  
✅ View logs (real-time)
✅ Update to latest
✅ Manage config
✅ Process tracking
✅ Version info
✅ Full documentation

## Help

```bash
# See all commands
tgws-manager --help

# See command options
tgws-manager start --help
tgws-manager config --help
```

---

For detailed documentation, see:
- **Installation**: `INSTALL.md`
- **Usage Guide**: `USAGE.md`
- **Development**: `DEVELOPMENT.md`
- **Full README**: `README.md`
