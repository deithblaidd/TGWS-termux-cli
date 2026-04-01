# tgws-manager

Independent CLI tool that manages `tg-ws-proxy` on Termux.  
**GitHub:** [deithblaidd/TGWS-termux-cli](https://github.com/deithblaidd/TGWS-termux-cli)

## What is tgws-manager?

**tgws-manager** is a lightweight management tool for running a SOCKS5 proxy (`tg-ws-proxy`) on Termux (Android). It handles:

- **Installation**: Downloads and sets up the proxy from GitHub
- **Lifecycle**: Start, stop, and monitor the proxy process
- **Configuration**: Manage proxy settings and ports
- **Updates**: Keep both the proxy and manager tool up-to-date
- **Independence**: The proxy and manager are completely separate — you can update or remove one without affecting the other

Both components are installed independently:
- **tgws-manager**: The management tool (installed in your Python environment)
- **tg-ws-proxy**: A git repository clone in `~/.local/tg-ws-proxy/` (the actual proxy)

## Quick Start

**Clean Termux setup (one line):**
```bash
pkg update && pkg upgrade -y && pkg install -y python git && git clone https://github.com/deithblaidd/TGWS-termux-cli && cd TGWS-termux-cli && pip install -e . && tgws-manager install && tgws-manager start
```

**Or step-by-step:** [QUICKSTART.md](docs/user/QUICKSTART.md)

## Install

```bash
git clone https://github.com/deithblaidd/TGWS-termux-cli
cd TGWS-termux-cli && pip install -e .
tgws-manager install   # downloads tg-ws-proxy
```

## Basic Commands

```bash
tgws-manager install              # download & setup tg-ws-proxy
tgws-manager start                # start proxy (default port 1080)
tgws-manager start --port 1081    # custom port
tgws-manager status               # check if running
tgws-manager logs -f              # live logs
tgws-manager stop                 # stop proxy
tgws-manager update               # update proxy
tgws-manager self-update          # update tgws-manager
tgws-manager config --show        # view config
tgws-manager uninstall            # remove proxy
```

See [USAGE.md](docs/user/USAGE.md) for complete reference with all flags and options.

## How It Works

1. **Install phase**: `tgws-manager install` clones the proxy repository to `~/.local/tg-ws-proxy/`
2. **Run phase**: `tgws-manager start` launches the proxy as a background subprocess and tracks it via PID file
3. **Config**: Settings stored in `~/.tgws-manager/config.json`
4. **Update phase**: Both components can be updated independently without affecting each other

**Key feature**: The proxy and manager are completely decoupled. You can:
- Remove tgws-manager while keeping the proxy running
- Run the proxy manually without the manager
- Update either component independently

## Documentation

| | |
|-|-|
| [QUICKSTART.md](docs/user/QUICKSTART.md) | Get running in 30 seconds |
| [INSTALL.md](docs/user/INSTALL.md) | Installation guide |
| [USAGE.md](docs/user/USAGE.md) | All commands & options |
| [ARCHITECTURE.md](docs/user/ARCHITECTURE.md) | How it works |
| [DOCKER-QUICKSTART.md](docs/user/DOCKER-QUICKSTART.md) | Local testing |
| [DEVELOPMENT.md](docs/testing/DEVELOPMENT.md) | Contributing |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Port in use | `tgws-manager start --port 9999` |
| Permission denied | `chmod -R 755 ~/.local/tg-ws-proxy ~/.tgws-manager` |

## License

MIT
