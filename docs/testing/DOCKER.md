# Docker Testing

Pre-configured Docker environment with Python 3.11, Git, port mappings (1080-1085, 9999).

## Setup

```bash
make setup     # build & start
make shell     # enter container
make clean     # stop & remove volumes
```

Or with docker-compose:
```bash
docker-compose up -d
docker-compose exec tgws-test bash
docker-compose down -v
```

## Basic Tests

```bash
tgws-manager install
tgws-manager start
tgws-manager status
tgws-manager stop
tgws-manager start --port 1081
tgws-manager config --show
tgws-manager logs -f
tgws-manager update
```

## Edge Cases

```bash
# Start without install (should error)
tgws-manager start

# Port conflict
tgws-manager start --port 80

# Kill process manually, check detection
kill $(cat ~/.tgws-manager/proxy.pid)
tgws-manager status
```

## Make Targets

| Target | Description |
|--------|-------------|
| `make setup` | Build image and start containers |
| `make shell` | Enter container bash |
| `make logs` | View container logs |
| `make test` | Run all tests |
| `make test-install` | Test install command |
| `make test-start` | Test start/stop lifecycle |
| `make test-config` | Test config management |
| `make clean` | Stop and remove volumes |
| `make rebuild` | Clean rebuild from scratch |


## Reset

```bash
# Reset proxy state inside container
docker-compose exec tgws-test rm -rf ~/.local/tg-ws-proxy ~/.tgws-manager
```

- Container runs as `testuser` (non-root) by default
- Proxy installations persist across container restarts (volume-backed)
- Source code changes auto-refresh (mounted volume)
- All test artifacts saved to `./test-artifacts/`
- Health checks run every 30 seconds

---

