# Quick Start

## Setup (one command)

```bash
pkg update && pkg upgrade -y && pkg install -y python git rust && export ANDROID_API_LEVEL=$(getprop ro.build.version.sdk) && git clone https://github.com/deithblaidd/TGWS-termux-cli && cd TGWS-termux-cli && pip install -e . && tgws-manager install && tgws-manager start
```

## Step-by-step

```bash
# Dependencies
pkg update && pkg upgrade -y
pkg install -y python git rust
export ANDROID_API_LEVEL=$(getprop ro.build.version.sdk)

# Install tgws-manager
git clone https://github.com/deithblaidd/TGWS-termux-cli
cd TGWS-termux-cli && pip install -e .

# Install & start proxy
tgws-manager install
tgws-manager start
```

## Essential Commands

```bash
tgws-manager start              # start (port 1080 default)
tgws-manager start --port 9999  # custom port
tgws-manager start --host 0.0.0.0  # all interfaces
tgws-manager status             # check if running
tgws-manager logs -f            # live logs
tgws-manager stop               # stop
tgws-manager update             # update proxy
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `command not found: tgws-manager` | `pip install -e .` |
| Rust errors during install | `pkg install -y rust` |
| Port in use | `tgws-manager start --port 9999` |

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

## Documentation

- [Installation Guide](INSTALL.md)
- [Usage Guide](USAGE.md)
- [Architecture](ARCHITECTURE.md)
- [Development Guide](../testing/DEVELOPMENT.md)
- [Docker Testing](DOCKER-QUICKSTART.md)
