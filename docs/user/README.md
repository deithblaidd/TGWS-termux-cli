# tgws-manager

**Repository:** [deithblaidd/TGWS-termux-cli](https://github.com/deithblaidd/TGWS-termux-cli)

**Tgws-manager** is an **independent, separate CLI tool** that manages `tg-ws-proxy` installations on Termux. It is **NOT part of tg-ws-proxy** — it's a standalone tool that controls tg-ws-proxy as an external dependency.

## Key Concepts

- **tgws-manager**: The management tool (this repo) — pip-installable package
- **tg-ws-proxy**: The actual proxy software — managed by tgws-manager
- **Completely independent**: Can be installed, updated, and removed separately

## Features

- **Install**: Download and setup tg-ws-proxy from GitHub
- **Update**: Pull latest changes from tg-ws-proxy repo and rebuild
- **Start/Stop**: Control the proxy service
- **Status**: Check if proxy is running
- **Logs**: View real-time logs
- **Config**: Manage proxy settings
- **Version Control**: Track installed proxy version
- **Encapsulated**: Proxy runs independently in ~/.local/tg-ws-proxy/

## Installation

### On Termux

```bash
# Method 1: Install from GitHub (latest code)
git clone https://github.com/deithblaidd/TGWS-termux-cli
cd TGWS-termux-cli
pip install -e .

# Method 2: Install from PyPI (once published)
pip install tgws-manager
```

### For Testing (Docker)

```bash
# Quick setup
make setup
make shell

# Or using docker-compose directly
docker-compose up -d
docker-compose exec tgws-test bash

# See DOCKER-QUICKSTART.md for full testing guide
```

### Requirements

- Python 3.8+
- Git
- pip

## Usage

```bash
# Install tg-ws-proxy
tgws-manager install

# Start the proxy
tgws-manager start --port 1080

# Check status
tgws-manager status

# View logs
tgws-manager logs -f

# Update to latest version
tgws-manager update

# Stop the proxy
tgws-manager stop

# View all options
tgws-manager --help
```

## Configuration

Settings are stored in `~/.tgws-manager/config.json`:

```json
{
    "proxy_path": "/home/user/.local/tg-ws-proxy",
    "auto_start": false,
    "last_port": 1080,
    "git_url": "https://github.com/Flowseal/tg-ws-proxy"
}
```

## Commands

### `install`
Clone tg-ws-proxy and install dependencies.

```bash
tgws-manager install [--path PATH]
```

### `start`
Start the proxy service.

```bash
tgws-manager start [--port PORT] [--host HOST] [--dc-ip DC_IP]... [--verbose]
```

### `stop`
Stop the running proxy.

```bash
tgws-manager stop
```

### `status`
Show proxy status and PID.

```bash
tgws-manager status
```

### `logs`
Display proxy logs.

```bash
tgws-manager logs [-f] [-n LINES]
```

Options:
- `-f, --follow`: Follow log output (tail -f mode)
- `-n, --lines`: Show last N lines (default: 50)

### `update`
Pull latest from GitHub and rebuild.

```bash
tgws-manager update [--rebuild]
```

### `config`
Manage settings.

```bash
tgws-manager config [--set KEY VALUE] [--get KEY] [--show]
```

### `uninstall`
Remove the proxy installation.

```bash
tgws-manager uninstall [--purge]
```

Options:
- `--purge`: Also remove configuration files

## File Structure

```
~/.local/tg-ws-proxy/          # Proxy installation
~/.tgws-manager/               # Manager configuration
  └── config.json
  └── proxy.pid
  └── logs/
      └── proxy.log
```

## Troubleshooting

### Cryptography Rust Build Error
If you see Rust compilation errors during installation, ensure you have:
```bash
pkg install -y rust
```

### Port Already in Use
```bash
tgws-manager stop && tgws-manager start --port 1081
```

### Permission Denied
Ensure Termux has read/write permissions:
```bash
chmod 755 ~/.local/tg-ws-proxy
chmod 755 ~/.tgws-manager
```

## Architecture

```
User's Termux Device
├── tgws-manager (this tool)          [pip package]
│   └── Manages
│       └── ~/.local/tg-ws-proxy/     [independent tg-ws-proxy installation]
│           └── Runs as separate process
├── ~/.tgws-manager/                  [manager config & state]
│   ├── config.json
│   ├── proxy.pid
│   └── version.json
└── ~/.local/tg-ws-proxy/.tgws-manager/ [proxy metadata]
    └── version.json
```

## Separation of Concerns

- **tgws-manager** is about managing the lifecycle of a proxy
- **tg-ws-proxy** is the actual SOCKS5 proxy implementation
- They can be updated independently
- Removing tgws-manager doesn't affect tg-ws-proxy
- Updating tg-ws-proxy doesn't require tgws-manager changes

## Learn More

For detailed architecture and design information, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Testing

tgws-manager includes a complete Docker testing environment for development and testing:

```bash
# Quick start (requires Docker & Docker Compose)
make setup       # Build and start environment
make shell       # Enter test container
make test        # Run all automated tests
make clean       # Cleanup
```

**See [DOCKER-QUICKSTART.md](DOCKER-QUICKSTART.md)** for step-by-step testing guide.

The Docker environment includes:
- ✅ Complete Python environment with all dependencies
- ✅ Git and system utilities
- ✅ tgws-manager pre-installed
- ✅ Persistent volumes for testing
- ✅ Multiple port mapping for testing
- ✅ Helper scripts and health checks

## License

MIT - See LICENSE file
