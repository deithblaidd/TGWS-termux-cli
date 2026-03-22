# Docker Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Python 3.11 image, installs tgws-manager in dev mode |
| `docker-compose.yml` | Orchestration with port mappings (1080-1085, 9999) and volumes |
| `Makefile` | Convenience targets (`make setup`, `make shell`, `make test`, etc) |
| `docker-quick.sh` | Alternative shell script with the same commands |

See [DOCKER.md](DOCKER.md) for usage.
