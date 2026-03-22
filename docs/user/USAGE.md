# tgws-manager Usage Guide

## Overview

`tgws-manager` is a CLI tool to manage tg-ws-proxy on Termux. It handles installation, running, stopping, updating, and configuration of your proxy.

## Command Reference

All available `tgws-manager` commands:

**Installation & Lifecycle:**
- `tgws-manager install` - Download and setup tg-ws-proxy
- `tgws-manager install --path PATH` - Install to custom location
- `tgws-manager install --rebuild` - Force rebuild dependencies
- `tgws-manager start` - Start the proxy service
- `tgws-manager stop` - Stop the proxy service
- `tgws-manager uninstall` - Remove proxy installation (keep config)
- `tgws-manager uninstall --purge` - Remove everything (config + installation)

**Status & Information:**
- `tgws-manager status` - Show proxy status
- `tgws-manager info` - Display system info and installation details
- `tgws-manager logs` - Show proxy logs
- `tgws-manager logs -n 100` - Show last 100 lines
- `tgws-manager logs -f` - Follow logs live (tail -f)

**Updates:**
- `tgws-manager update` - Update tg-ws-proxy code
- `tgws-manager update --rebuild` - Update and rebuild dependencies
- `tgws-manager self-update` - Update tgws-manager tool itself

**Configuration:**
- `tgws-manager config --show` - Display all settings
- `tgws-manager config --get SETTING` - Get specific setting
- `tgws-manager config --set SETTING VALUE` - Change setting

**Advanced Start Options:**
- `tgws-manager start --port PORT` - Listen on specific port (default: 1080)
- `tgws-manager start --host HOST` - Bind to host (default: 127.0.0.1)
- `tgws-manager start --dc-ip IP` - Set data center IP
- `tgws-manager start -v` - Enable verbose logging

**Help:**
- `tgws-manager --help` - Show all commands
- `tgws-manager COMMAND --help` - Show command help

## Basic Commands

### Initialize Installation

```bash
tgws-manager install
```

Downloads and sets up tg-ws-proxy to `~/.local/tg-ws-proxy/`. Only needs to be run once.

### Start the Proxy

```bash
# Simple start
tgws-manager start

# With options
tgws-manager start --port 1080 --host 0.0.0.0
```

The proxy will run in the background. Check status with:

```bash
tgws-manager status
```

### Stop the Proxy

```bash
tgws-manager stop
```

### View Logs

```bash
# Show last 50 lines
tgws-manager logs

# Show last 100 lines
tgws-manager logs -n 100

# Follow logs live (like tail -f)
tgws-manager logs -f
```

Press `Ctrl+C` to stop following logs.

### Update Proxy

```bash
# Just pull latest code from tg-ws-proxy
tgws-manager update

# Update and rebuild dependencies
tgws-manager update --rebuild
```

### Update tgws-manager Tool Itself

```bash
# Update the management tool only (not the proxy)
tgws-manager self-update

# Or manually
pip install --upgrade tgws-manager
```

**Important Distinction:**
- `tgws-manager update` — Updates tg-ws-proxy (the managed tool)
- `tgws-manager self-update` — Updates tgws-manager (the manager tool)

## Advanced Options

### Start with Custom Settings

```bash
# Listen on all interfaces
tgws-manager start --host 0.0.0.0

# Use different port
tgws-manager start --port 9999

# Set custom data centers
tgws-manager start --dc-ip 2:149.154.167.220 --dc-ip 4:149.154.167.220

# Enable verbose logging
tgws-manager start -v
```

### Configuration Management

```bash
# Show all settings
tgws-manager config --show

# Retrieve specific setting
tgws-manager config --get last_port

# Change a setting
tgws-manager config --set last_port 9999

# View system info
tgws-manager info
```

### Installation Options

```bash
# Custom installation path
tgws-manager install --path /path/to/custom/location

# Force rebuild of dependencies
tgws-manager install --rebuild
```

### Uninstallation

```bash
# Keep configuration files
tgws-manager uninstall

# Remove everything
tgws-manager uninstall --purge
```

## Typical Workflow

### First time setup

```bash
# Install tgws-manager
pip install -e tgws-manager/

# Install tg-ws-proxy
tgws-manager install

# Start it
tgws-manager start

# Check if running
tgws-manager status
```

### Daily usage

```bash
# Start proxy
tgws-manager start

# ... do your work ...

# Stop when done
tgws-manager stop
```

### Updating

```bash
# Stop
tgws-manager stop

# Update and rebuild
tgws-manager update --rebuild

# Resume
tgws-manager start
```

## Configuration File

Settings are stored in `~/.tgws-manager/config.json`:

```json
{
  "proxy_path": "/home/user/.local/tg-ws-proxy",
  "git_url": "https://github.com/Flowseal/tg-ws-proxy",
  "auto_start": false,
  "last_port": 1080,
  "last_host": "127.0.0.1",
  "check_updates": true
}
```

You can edit this directly or use `tgws-manager config` commands.

## Environment Variables

Currently no special environment variables, but Termux-specific settings are detected automatically.

## Troubleshooting

### Proxy won't start

```bash
# Check status
tgws-manager status

# View full logs
tgws-manager logs -n 500

# Try verbose start
tgws-manager start -v
```

### Port conflicts

```bash
# Kill the process manually if needed
kill $(cat ~/.tgws-manager/proxy.pid)

# Then start on different port
tgws-manager start --port 9999
```

### Dependency issues

```bash
# Reinstall everything
tgws-manager install --rebuild
```

### Update fails

Check that you have git and internet connection:

```bash
pkg install -y git
tgws-manager update --rebuild
```

## Tips & Tricks

### Alias for faster access

```bash
alias proxy-start='tgws-manager start'
alias proxy-stop='tgws-manager stop'
alias proxy-logs='tgws-manager logs -f'
```

### Monitor logs while running

In another terminal:

```bash
tgws-manager logs -f
```

### Check what's installed

```bash
tgws-manager info
```

### Get help

```bash
tgws-manager --help
tgws-manager start --help
tgws-manager config --help
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Command not found" | Run `pip install -e .` in tgws-manager directory |
| Port already in use | Use different port: `tgws-manager start --port 9999` |
| Rust compilation error | `pkg install -y rust` then retry |
| Process won't stop | `kill $(cat ~/.tgws-manager/proxy.pid)` |
| Permission denied | `chmod -R 755 ~/.local/tg-ws-proxy` |

## Performance Notes

- First start: May take time on first dependency installation
- Subsequent starts: Should be instant
- Updates with rebuild: Similar to first start time
- Logs: Real-time follow works but may be CPU intensive on slow devices

## Security

- Config and logs are stored locally only
- PID file is used for process management
- Git authentication uses standard SSH keys if configured
- No data sent to external services except git.com for updates

For more information, see README.md and INSTALL.md.
