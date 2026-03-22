# tgws-manager Documentation

**Welcome to tgws-manager** — a lightweight CLI tool that manages the `tg-ws-proxy` SOCKS5 proxy on Termux.

The tool and proxy are **completely independent**. You can update, remove, or modify each one without affecting the other.

## Documentation Structure

```
docs/
├── user/          ← For people using tgws-manager
│   ├── QUICKSTART.md          (30 seconds to running)
│   ├── INSTALL.md             (installation guide)
│   ├── USAGE.md               (all commands with examples)
│   ├── ARCHITECTURE.md        (how the tool and proxy relate)
│   └── DOCKER-QUICKSTART.md   (local testing with Docker)
│
└── testing/       ← For developers and contributors
    ├── DEVELOPMENT.md         (code structure and extending)
    ├── DOCKER.md              (comprehensive testing guide)
    ├── REPOSITORY_STRUCTURE.md (project org and publishing)
    └── DOCKER-FILES.md        (Docker implementation details)
```

## Quick Navigation

### I just want to use it

1. **[QUICKSTART.md](user/QUICKSTART.md)** — Get running in 30 seconds
2. **[USAGE.md](user/USAGE.md)** — All commands and options with examples
3. **[ARCHITECTURE.md](user/ARCHITECTURE.md)** — Understand how everything works

### I want to test it locally

1. **[DOCKER-QUICKSTART.md](user/DOCKER-QUICKSTART.md)** — Quick Docker setup (5 minutes)
2. **[DOCKER.md](testing/DOCKER.md)** — Full testing guide with advanced scenarios

### I want to contribute or extend

1. **[DEVELOPMENT.md](testing/DEVELOPMENT.md)** — Code structure and contributing guidelines
2. **[REPOSITORY_STRUCTURE.md](testing/REPOSITORY_STRUCTURE.md)** — Project layout and publishing to PyPI
3. **[DOCKER.md](testing/DOCKER.md)** — How to test your changes

## Document Overview

| Document | Audience | Read Time | Best For |
|----------|----------|-----------|----------|
| [QUICKSTART.md](user/QUICKSTART.md) | Everyone | 3 min | Getting started fast |
| [INSTALL.md](user/INSTALL.md) | Users | 5 min | Detailed installation steps |
| [USAGE.md](user/USAGE.md) | Users | 10 min | Command reference with flags |
| [ARCHITECTURE.md](user/ARCHITECTURE.md) | Everyone | 5 min | Understanding the design |
| [DOCKER-QUICKSTART.md](user/DOCKER-QUICKSTART.md) | Testers | 5 min | Testing locally |
| [DEVELOPMENT.md](testing/DEVELOPMENT.md) | Developers | 5 min | Code structure and extending |
| [DOCKER.md](testing/DOCKER.md) | Developers | 30 min | Advanced testing scenarios |
| [REPOSITORY_STRUCTURE.md](testing/REPOSITORY_STRUCTURE.md) | Contributors | 10 min | Project organization |

## About tgws-manager

- **What it is**: A CLI tool for managing tg-ws-proxy on Termux (Android)
- **What it manages**: Downloads, starts/stops, updates, and configures the proxy
- **Key feature**: Completely independent from the proxy — can be updated separately
- **Installation target**: `~/.local/tg-ws-proxy/` (for the proxy), `~/.tgws-manager/` (for config)

## Links

- **GitHub**: [deithblaidd/TGWS-termux-cli](https://github.com/deithblaidd/TGWS-termux-cli)
- **Managed Project**: [Flowseal/tg-ws-proxy](https://github.com/Flowseal/tg-ws-proxy)
- **License**: MIT
