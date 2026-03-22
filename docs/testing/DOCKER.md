# Docker Testing Environment

Complete Docker setup for testing tgws-manager. Pre-configured with Python 3.11, Git, utilities, persistent volumes, and port mappings (1080-1085, 9999).

## Quick Start

```bash
# Build and start
docker-compose build
docker-compose up -d

# Enter container
docker-compose exec tgws-test bash

# Test commands
tgws-manager install
tgws-manager start
tgws-manager status
tgws-manager stop
```

## Basic Tests

```bash
# Install
tgws-manager install

# Start/stop
tgws-manager start
tgws-manager status
tgws-manager stop

# Custom port
tgws-manager start --port 1081

# Config
tgws-manager config --show
tgws-manager config --get proxy_path

# Logs
tgws-manager logs -n 50
tgws-manager logs -f

# Update
tgws-manager update
```

## Edge Cases

```bash
# Start without install → should error
tgws-manager start

# Port already in use
tgws-manager start --port 80

# Kill process manually
kill $(cat ~/.tgws-manager/proxy.pid)
tgws-manager status  # should detect death
```

## Commands

```bash
# Build & start
docker-compose build && docker-compose up -d

# Stop & cleanup
docker-compose down -v

# Logs
docker-compose logs -f tgws-test

# Reset proxy
docker-compose exec tgws-test rm -rf ~/.local/tg-ws-proxy ~/.tgws-manager

# Debug info
docker-compose exec tgws-test python --version
docker-compose exec tgws-test tgws-manager --version
```

## Port Mappings

`1080-1085, 9999` - for testing different sizes
tgws-manager logs -n 10
tgws-manager stop
sleep 1
tgws-manager status

echo "=== Testing Config ==="
tgws-manager config --show
tgws-manager config --set last_port 9999
tgws-manager config --get last_port

echo "=== Testing Info ==="
tgws-manager info

echo "=== All Tests Passed ==="
exit
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Docker Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: docker/setup-buildx-action@v2
      - run: docker-compose build
      - run: docker-compose run tgws-test /scripts/test-tgws-manager.sh
```

## Notes

- Container runs as `testuser` (non-root) by default
- Proxy installations persist across container restarts (volume-backed)
- Source code changes auto-refresh (mounted volume)
- All test artifacts saved to `./test-artifacts/`
- Health checks run every 30 seconds

---

**Happy Testing! 🚀**
