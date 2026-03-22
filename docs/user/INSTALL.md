# Installation Guide for tgws-manager

**Important**: tgws-manager is a **separate, independent tool** from tg-ws-proxy. It manages tg-ws-proxy as an external dependency that's installed separately.

## One-Command Installation

For a clean Termux system, run this single command:

```bash
pkg update && pkg upgrade -y && pkg install -y python git rust && export ANDROID_API_LEVEL=$(getprop ro.build.version.sdk) && git clone https://github.com/deithblaidd/TGWS-termux-cli && cd TGWS-termux-cli && pip install -e .
```

This will:
1. Update Termux package manager
2. Install Python and Git
3. Clone the tgws-manager repository
4. Install tgws-manager as a pip package

After installation, you're ready to use:
```bash
tgws-manager install
tgws-manager start
```

## Quick Start on Termux

### 1. Prerequisites

Make sure you have the required packages:

```bash
pkg update && pkg upgrade -y
pkg install -y python git rust
export ANDROID_API_LEVEL=$(getprop ro.build.version.sdk)
```

### 2. Install tgws-manager

Clone from GitHub and install:

```bash
# Clone the repository
git clone https://github.com/deithblaidd/TGWS-termux-cli
cd TGWS-termux-cli

# Install the CLI tool
pip install -e .
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/deithblaidd/TGWS-termux-cli.git
```

### Important: Two Completely Separate Things

- **tgws-manager** (this package) - Management tool for controlling the proxy
- **tg-ws-proxy** - The actual proxy software (will be installed automatically when you run `tgws-manager install`)

### 3. First-Time Setup

Once tgws-manager is installed, initialize the proxy:

```bash
tgws-manager install
```

This will:
- Clone tg-ws-proxy repository to `~/.local/tg-ws-proxy/` (separate installation)
- Install all tg-ws-proxy Python dependencies
- Create tgws-manager configuration at `~/.tgws-manager/`

**Key Point**: The actual proxy (`tg-ws-proxy`) is installed separately in its own location, completely independent from tgws-manager itself.

## Complete Usage Examples

### Start the proxy

```bash
# Default (port 1080, localhost)
tgws-manager start

# Custom port
tgws-manager start --port 1080

# Listen on all interfaces
tgws-manager start --host 0.0.0.0

# Custom data centers
tgws-manager start --dc-ip 2:149.154.167.220 --dc-ip 4:149.154.167.220

# Verbose logging
tgws-manager start -v
```

### Check status

```bash
tgws-manager status
```

### View logs

```bash
# Last 50 lines
tgws-manager logs

# Follow in real-time
tgws-manager logs -f

# Custom number of lines
tgws-manager logs -n 100
```

### Update to latest version

```bash
# Just update code
tgws-manager update

# Update and rebuild dependencies
tgws-manager update --rebuild
```

### Stop the proxy

```bash
tgws-manager stop
```

### Manage configuration

```bash
# Show all settings
tgws-manager config --show

# Get specific setting
tgws-manager config --get last_port

# Change setting
tgws-manager config --set auto_start true
```

### System information

```bash
tgws-manager info
```

### Uninstall

```bash
# Just remove proxy
tgws-manager uninstall

# Remove proxy + configuration
tgws-manager uninstall --purge
```

## Troubleshooting

### Error: Command not found: tgws-manager

Make sure the installation completed successfully:

```bash
pip list | grep tgws-manager
```

If not listed, reinstall:

```bash
pip install --upgrade e .
```

### Rust compilation errors during install

If you see errors about Rust:

```bash
pkg install -y rust
pip install --upgrade cryptography
tgws-manager install --rebuild
```

### Port already in use

```bash
# Stop running proxy
tgws-manager stop

# Start on different port
tgws-manager start --port 1081
```

### Permission denied

Ensure proper permissions:

```bash
chmod -R 755 ~/.local/tg-ws-proxy
chmod -R 755 ~/.tgws-manager
```

### View detailed error logs

```bash
# Check if proxy is actually running
tgws-manager status

# View full logs
tgws-manager logs -n 200

# Run with verbose mode
tgws-manager start -v
```

## Uninstalling tgws-manager

To completely remove tgws-manager:

```bash
# Uninstall with config
tgws-manager uninstall --purge

# Or just remove the package
pip uninstall tgws-manager
```

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
- [tgws-manager issues](https://github.com/Flowseal/tg-ws-proxy/issues)
