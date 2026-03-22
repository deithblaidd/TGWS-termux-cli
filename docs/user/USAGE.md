# Usage

## Command Reference

### Installation

<table>
  <thead>
    <tr><th style="white-space:nowrap">Command</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td style="white-space:nowrap"><code>tgws-manager install</code></td><td>Download & setup tg-ws-proxy</td></tr>
  </tbody>
</table>

**Options:**

<table>
  <thead>
    <tr><th style="white-space:nowrap">Flag</th><th>Default</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td style="white-space:nowrap"><code>--path PATH</code></td><td><code>~/.local/tg-ws-proxy</code></td><td>Install to custom location instead of default</td></tr>
    <tr><td style="white-space:nowrap"><code>--rebuild</code></td><td><code>false</code></td><td>Force rebuild dependencies even if they're cached</td></tr>
  </tbody>
</table>

**Example:**
```bash
tgws-manager install --path /custom/location --rebuild
```

### Start/Stop

<table>
  <thead>
    <tr><th style="white-space:nowrap">Command</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td style="white-space:nowrap"><code>tgws-manager start</code></td><td>Start proxy (default port 1080, localhost)</td></tr>
    <tr><td style="white-space:nowrap"><code>tgws-manager stop</code></td><td>Stop running proxy</td></tr>
  </tbody>
</table>

**Options:**

<table>
  <thead>
    <tr><th style="white-space:nowrap">Flag</th><th>Default</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td style="white-space:nowrap"><code>--port PORT</code></td><td><code>1080</code></td><td>Listen on specific port instead of default</td></tr>
    <tr><td style="white-space:nowrap"><code>--host HOST</code></td><td><code>127.0.0.1</code></td><td>Bind to specific host (use <code>0.0.0.0</code> for all interfaces)</td></tr>
    <tr><td style="white-space:nowrap"><code>--dc-ip IP</code></td><td><em>none</em></td><td>Set custom data center IP address</td></tr>
    <tr><td style="white-space:nowrap"><code>-v</code></td><td><code>false</code></td><td>Enable verbose logging to see detailed output</td></tr>
  </tbody>
</table>

**Example:**
```bash
tgws-manager start --port 9999 --host 0.0.0.0 -v
tgws-manager start --dc-ip 149.154.167.220 --port 1081
```

### Status & Logs

<table>
  <thead>
    <tr><th style="white-space:nowrap">Command</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td style="white-space:nowrap"><code>tgws-manager status</code></td><td>Show if proxy is running and connection info</td></tr>
    <tr><td style="white-space:nowrap"><code>tgws-manager logs</code></td><td>Show proxy logs (last 50 lines by default)</td></tr>
  </tbody>
</table>

**Options:**

<table>
  <thead>
    <tr><th style="white-space:nowrap">Flag</th><th>Default</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td style="white-space:nowrap"><code>-n N</code></td><td><code>50</code></td><td>Show last N lines of logs instead of 50</td></tr>
    <tr><td style="white-space:nowrap"><code>-f</code></td><td><code>false</code></td><td>Follow logs live (like <code>tail -f</code>)</td></tr>
  </tbody>
</table>

**Example:**
```bash
tgws-manager logs -n 200 -f
```

### Updates

<table>
  <thead>
    <tr><th style="white-space:nowrap">Command</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td style="white-space:nowrap"><code>tgws-manager update</code></td><td>Update tg-ws-proxy code from GitHub</td></tr>
    <tr><td style="white-space:nowrap"><code>tgws-manager self-update</code></td><td>Update tgws-manager tool itself via pip</td></tr>
  </tbody>
</table>

**Options:**

<table>
  <thead>
    <tr><th style="white-space:nowrap">Flag</th><th>Default</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td style="white-space:nowrap"><code>--rebuild</code></td><td><code>false</code></td><td>Rebuild dependencies after pulling updates</td></tr>
  </tbody>
</table>

**Example:**
```bash
tgws-manager update --rebuild
```

### Configuration & Management

<table>
  <thead>
    <tr><th style="white-space:nowrap">Command</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td style="white-space:nowrap"><code>tgws-manager config</code></td><td>Manage proxy settings and configuration</td></tr>
    <tr><td style="white-space:nowrap"><code>tgws-manager info</code></td><td>Show system info and installation details</td></tr>
    <tr><td style="white-space:nowrap"><code>tgws-manager uninstall</code></td><td>Remove proxy installation</td></tr>
  </tbody>
</table>

**Options:**

<table>
  <thead>
    <tr><th style="white-space:nowrap">Flag</th><th>Default</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td style="white-space:nowrap"><code>--show</code></td><td><code>false</code></td><td>Display all current settings</td></tr>
    <tr><td style="white-space:nowrap"><code>--get KEY</code></td><td><em>none</em></td><td>Get value of specific setting</td></tr>
    <tr><td style="white-space:nowrap"><code>--set KEY VALUE</code></td><td><em>none</em></td><td>Change a setting value</td></tr>
    <tr><td style="white-space:nowrap"><code>--purge</code></td><td><code>false</code></td><td>Remove proxy AND all configuration (default keeps config)</td></tr>
  </tbody>
</table>

**Example:**
```bash
tgws-manager config --show
tgws-manager config --set last_port 9999
tgws-manager uninstall --purge
```

## Configuration

Stored at `~/.tgws-manager/config.json`:

```json
{
  "proxy_path": "~/.local/tg-ws-proxy",
  "git_url": "https://github.com/Flowseal/tg-ws-proxy",
  "auto_start": false,
  "last_port": 1080,
  "last_host": "127.0.0.1"
}
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Proxy won't start | `tgws-manager logs -n 500` or `tgws-manager start -v` |
| Port conflict | `kill $(cat ~/.tgws-manager/proxy.pid)` then use `--port 9999` |
| Dependency issues | `tgws-manager install --rebuild` |
| Update fails | `pkg install -y git` then retry |

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
