# Docker Quick Start

Pre-configured Docker environment for testing tgws-manager.

## 30 Seconds

```bash
# Makefile (easiest)
make setup && make shell

# Or docker-compose
docker-compose up -d && docker-compose exec tgws-test bash
```

## Test Commands

```bash
tgws-manager install
tgws-manager start
tgws-manager status
tgws-manager stop
```

## Quick Workflow

```bash
make setup      # Build & start
make shell      # Enter container
# run tests
exit
make clean      # Cleanup
```

## Common Tasks

- Setup: `make setup` or `docker-compose up -d`
- Enter: `make shell` or `docker-compose exec tgws-test bash`
- Logs: `make logs` or `docker-compose logs -f`
- Clean: `make clean` or `docker-compose down -v`

## Quick Tests

Install & start: `tgws-manager install && tgws-manager start`
Config: `tgws-manager config --show`
Custom port: `tgws-manager start --port 1081`
Logs: `tgws-manager logs -f`
Stop: `tgws-manager stop`

## Ports

1080-1085, 9999 available for testing.

## Cleanup

```bash
# Reset proxy installation
docker-compose exec tgws-test rm -rf ~/.local/tg-ws-proxy ~/.tgws-manager

# Full cleanup
make clean
```

## Make Commands Reference

**Setup & Lifecycle:**
- `make help` - Show available commands
- `make setup` - Build image and start containers
- `make up` - Start containers (use after cleanup)
- `make down` - Stop containers (keeps volumes)
- `make clean` - Stop containers and remove volumes
- `make rebuild` - Clean and rebuild Docker image from scratch

**Interaction:**
- `make shell` - Enter container bash shell
- `make logs` - View container logs (follow with `-f`)
- `make status` - Check container health and status
- `make ps` - List running containers
- `make stats` - Show CPU/memory usage

**Testing:**
- `make test` - Run all tests (install, start, config, update)
- `make test-install` - Test tgws-manager install command
- `make test-start` - Test start/stop lifecycle
- `make test-config` - Test configuration management
- `make test-error` - Test error handling
- `make test-update` - Test update command

**Cleanup:**
- `make prune` - Remove project Docker resources (containers, image, volumes, network)
- `make docker-clean` - Same as prune (alias)