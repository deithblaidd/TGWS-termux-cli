# Docker Quick Start

```bash
make setup && make shell
# or
docker-compose up -d && docker-compose exec tgws-test bash
```

## Inside the container

```bash
tgws-manager install
tgws-manager start
tgws-manager status
tgws-manager stop
```

## Make reference

| Command | Action |
|---------|--------|
| `make setup` | Build & start |
| `make shell` | Enter container |
| `make logs` | View logs |
| `make test` | Run all tests |
| `make clean` | Stop & remove volumes |

Ports 1080-1085 and 9999 are mapped for testing.