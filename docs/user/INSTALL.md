# Installation

## Requirements

- Python 3.8+, Git, pip

## Install tgws-manager

```bash
# From GitHub
git clone https://github.com/deithblaidd/TGWS-termux-cli
cd TGWS-termux-cli
pip install -e .

# Or directly
pip install git+https://github.com/deithblaidd/TGWS-termux-cli.git

# Once on PyPI
pip install tgws-manager
```

On Termux, install the base dependencies:
```bash
pkg update && pkg upgrade -y && pkg install -y python git
```

## Install tg-ws-proxy

After tgws-manager is installed, run once:
```bash
tgws-manager install
```

This clones [Flowseal/tg-ws-proxy](https://github.com/Flowseal/tg-ws-proxy) into `~/.local/tg-ws-proxy/` and installs its dependencies.

## Uninstall

```bash
tgws-manager uninstall        # remove proxy only
tgws-manager uninstall --purge  # remove proxy + config
pip uninstall tgws-manager    # remove tgws-manager itself
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `command not found` | `pip install -e .` |
| Port in use | `tgws-manager start --port 1081` |
| Permission denied | `chmod -R 755 ~/.local/tg-ws-proxy ~/.tgws-manager` |

## Advanced: Development Installation

For development/testing:

```bash
cd tgws-manager

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
```

## File Locations

- **Config directory**: `~/.tgws-manager/`
  - `config.json` - Main settings
  - `proxy.pid` - Process ID
  - `version.json` - Version info

- **Proxy installation**: `~/.local/tg-ws-proxy/`
  - Clone of the original tg-ws-proxy repository
  - All proxy code and dependencies

## Support

For issues or feature requests:
- [tg-ws-proxy issues](https://github.com/Flowseal/tg-ws-proxy/issues)
- [tgws-manager issues](https://github.com/deithblaidd/TGWS-termux-cli/issues)
