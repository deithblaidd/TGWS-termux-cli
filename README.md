# tgws-manager

**GitHub Repository:** [deithblaidd/TGWS-termux-cli](https://github.com/deithblaidd/TGWS-termux-cli)

**Tgws-manager** is an **independent, separate CLI tool** that manages `tg-ws-proxy` installations on Termux. It is **NOT part of tg-ws-proxy** — it's a standalone tool that controls tg-ws-proxy as an external dependency.

## 📚 Quick Navigation

👉 **New users**: [Quick Start (30 seconds)](docs/user/QUICKSTART.md)  
👉 **Want to install**: [Installation Guide](docs/user/INSTALL.md)  
👉 **Want to use it**: [Commands & Usage](docs/user/USAGE.md)  
👉 **Want to test locally**: [Docker Setup](docs/user/DOCKER-QUICKSTART.md)  
👉 **Contributing or developing**: [Developer Guide](docs/testing/DEVELOPMENT.md)  
👉 **All documentation**: [Complete Doc Index](docs/index.md)  

## Key Concepts

- **tgws-manager**: The management tool (this repo) — pip-installable package
- **tg-ws-proxy**: The actual proxy software — managed by tgws-manager
- **Completely independent**: Can be installed, updated, and removed separately

## Features

- ✅ **Install**: Download and setup tg-ws-proxy from GitHub
- ✅ **Update**: Pull latest changes and rebuild
- ✅ **Start/Stop**: Control the proxy service
- ✅ **Status**: Check if proxy is running
- ✅ **Logs**: View real-time logs
- ✅ **Config**: Manage proxy settings
- ✅ **Version Control**: Track installed version
- ✅ **Encapsulated**: Proxy runs independently

## 30-Second Quick Start

**One command on clean Termux:**
```bash
pkg update && pkg upgrade -y && pkg install -y python git && git clone https://github.com/deithblaidd/TGWS-termux-cli && cd TGWS-termux-cli && pip install -e . && tgws-manager install && tgws-manager start
```

**Or step-by-step:**
```bash
# 1. Install tgws-manager
git clone https://github.com/deithblaidd/TGWS-termux-cli
cd TGWS-termux-cli
pip install -e .

# 2. Install tg-ws-proxy
tgws-manager install

# 3. Start proxy
tgws-manager start

# 4. Check status
tgws-manager status
```

**For detailed instructions**, see [QUICKSTART.md](docs/user/QUICKSTART.md)

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

See [INSTALL.md](docs/user/INSTALL.md) for detailed installation guide.

### For Testing (Docker)

```bash
# Quick setup
make setup && make shell

# Inside container, test commands
tgws-manager install
tgws-manager start
```

Full guide: [DOCKER-QUICKSTART.md](docs/user/DOCKER-QUICKSTART.md)

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

See [USAGE.md](docs/user/USAGE.md) for complete command reference.

## Documentation Structure

All documentation is organized in the `docs/` folder:

### 👤 User Documentation (`docs/user/`)
For people who **want to use tgws-manager**:
- [README.md](docs/user/README.md) - Project overview
- [QUICKSTART.md](docs/user/QUICKSTART.md) - 30-second setup
- [INSTALL.md](docs/user/INSTALL.md) - Detailed installation
- [USAGE.md](docs/user/USAGE.md) - Command reference with examples
- [ARCHITECTURE.md](docs/user/ARCHITECTURE.md) - System design explanation
- [DOCKER-QUICKSTART.md](docs/user/DOCKER-QUICKSTART.md) - Docker testing setup

### 🧪 Developer/Testing Documentation (`docs/testing/`)
For people who **want to develop/test tgws-manager**:
- [DEVELOPMENT.md](docs/testing/DEVELOPMENT.md) - Developer guide
- [REPOSITORY_STRUCTURE.md](docs/testing/REPOSITORY_STRUCTURE.md) - Project organization
- [DOCKER.md](docs/testing/DOCKER.md) - Comprehensive testing guide
- [DOCKER-FILES.md](docs/testing/DOCKER-FILES.md) - Docker implementation details

### 📋 Documentation Index
- [docs/index.md](docs/index.md) - Central navigation hub with complete cross-references

## Project Structure

```
tgws-manager/
├── docs/                          # All documentation
│   ├── index.md                   # Doc index (start here!)
│   ├── user/                      # User documentation (6 files)
│   └── testing/                   # Developer documentation (4 files)
├── src/tgws_manager/              # Source code
│   ├── cli.py
│   ├── manager.py
│   ├── config.py
│   └── utils.py
├── Dockerfile                     # Docker image
├── docker-compose.yml             # Docker setup
├── Makefile                       # Make targets
├── docker-quick.sh                # Shell script
├── pyproject.toml                 # Package config
├── requirements.txt               # Dependencies
└── LICENSE                        # MIT License
```

## Common Commands

```bash
tgws-manager install              # Install tg-ws-proxy
tgws-manager start                # Start proxy (port 1080)
tgws-manager start --port 1081    # Custom port
tgws-manager status               # Check status
tgws-manager logs -f              # View logs
tgws-manager stop                 # Stop proxy
tgws-manager update               # Update to latest
tgws-manager config --show        # View config
tgws-manager uninstall            # Remove installation
```

See [USAGE.md](docs/user/USAGE.md) for complete reference.

## Configuration

Settings stored in `~/.tgws-manager/config.json`:

```json
{
    "proxy_path": "/home/user/.local/tg-ws-proxy",
    "auto_start": false,
    "last_port": 1080,
    "git_url": "https://github.com/Flowseal/tg-ws-proxy"
}
```

Full configuration guide: [USAGE.md](docs/user/USAGE.md#configuration)

## Architecture

```
User's Termux Device
├── tgws-manager (this tool)          [pip package]
│   └── Manages
│       └── ~/.local/tg-ws-proxy/     [independent installation]
│           └── Runs as separate process
├── ~/.tgws-manager/                  [manager config & state]
│   ├── config.json
│   └── proxy.pid
└── ~/.local/tg-ws-proxy/.version    [version tracking]
```

**Complete architecture explanation**: [ARCHITECTURE.md](docs/user/ARCHITECTURE.md)

## Troubleshooting

### Rust Compilation Error
Install Rust with: `pkg install -y rust`

### Port in Use
Use a different port: `tgws-manager start --port 9999`

### Permission Denied
Fix permissions:
```bash
chmod 755 ~/.local/tg-ws-proxy
chmod 755 ~/.tgws-manager
```

See [USAGE.md](docs/user/USAGE.md#troubleshooting) for more solutions.

## Testing & Development

### Local Testing with Docker

```bash
make setup       # Build and start environment
make shell       # Enter test container
make up          # Start services
make test-all    # Run all tests
make clean       # Cleanup
```

Full testing guide: [DOCKER.md](docs/testing/DOCKER.md)

### Contributing

Want to contribute? See [DEVELOPMENT.md](docs/testing/DEVELOPMENT.md) for:
- Development setup
- Code structure
- How to extend
- Testing guidelines

## License

MIT - See LICENSE file

---

## Next Steps

1. **Brand new?** → [QUICKSTART.md](docs/user/QUICKSTART.md)
2. **Installing?** → [INSTALL.md](docs/user/INSTALL.md)
3. **Using?** → [USAGE.md](docs/user/USAGE.md)
4. **Testing?** → [DOCKER-QUICKSTART.md](docs/user/DOCKER-QUICKSTART.md)
5. **Contributing?** → [DEVELOPMENT.md](docs/testing/DEVELOPMENT.md)
6. **Everything?** → [docs/index.md](docs/index.md)
