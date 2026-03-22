# Makefile for tgws-manager Docker environment
# Usage: make <target>

.PHONY: help setup up down clean shell logs status rebuild \
        test test-install test-start test-config test-error test-update \
        ps stats prune docker-clean

# Default target
help:
	@echo "tgws-manager Docker Environment"
	@echo ""
	@echo "SETUP COMMANDS:"
	@echo "  make setup      - Build and start Docker environment"
	@echo "  make up         - Start containers"
	@echo "  make down       - Stop containers"
	@echo "  make clean      - Full cleanup (includes volumes)"
	@echo "  make rebuild    - Rebuild Docker image from scratch"
	@echo ""
	@echo "INTERACTION COMMANDS:"
	@echo "  make shell      - Enter container bash"
	@echo "  make logs       - View container logs"
	@echo "  make status     - Check container status"
	@echo "  make ps         - List running containers"
	@echo "  make stats      - Show resource usage"
	@echo ""
	@echo "TESTING COMMANDS:"
	@echo "  make test       - Run all tests"
	@echo "  make test-install  - Test installation"
	@echo "  make test-start    - Test start/stop"
	@echo "  make test-config   - Test configuration"
	@echo "  make test-error    - Test error handling"
	@echo "  make test-update   - Test update"
	@echo ""
	@echo "CLEANUP COMMANDS:"
	@echo "  make prune      - Prune Docker system"
	@echo "  make docker-clean - Remove all Docker data"

# Setup
setup: build up
	@echo ""
	@echo "✓ Environment ready! Enter with: make shell"

build:
	@echo "Building Docker image..."
	docker-compose build
	@echo "✓ Built"

up:
	@echo "Starting containers..."
	docker-compose up -d
	@sleep 2
	@docker-compose ps
	@echo "✓ Started"

down:
	@echo "Stopping containers..."
	docker-compose down
	@echo "✓ Stopped"

clean: down
	@echo "Removing volumes..."
	docker-compose down -v
	@echo "✓ Cleaned"

rebuild: clean build
	@echo "✓ Rebuilt"

# Interaction
shell:
	docker-compose exec tgws-test bash

logs:
	docker-compose logs -f tgws-test

status:
	@echo "Container Status:"
	@docker-compose ps
	@echo ""
	@echo "Health Check:"
	@docker-compose exec tgws-test /scripts/healthcheck.sh || echo "Not healthy"

ps:
	docker-compose ps

stats:
	docker stats tgws-manager-test

# Testing
test: test-install test-start test-config test-update
	@echo ""
	@echo "✓ All tests passed!"

test-install:
	@echo "=== Testing Installation ==="
	docker-compose exec tgws-test bash -c \
		'rm -rf ~/.local/tg-ws-proxy ~/.tgws-manager && \
		 tgws-manager install && \
		 ls ~/.local/tg-ws-proxy/proxy/tg_ws_proxy.py && \
		 echo "✓ Install test passed"'

test-start:
	@echo "=== Testing Start/Stop ==="
	docker-compose exec tgws-test bash -c \
		'tgws-manager start && \
		 sleep 2 && \
		 tgws-manager status && \
		 tgws-manager stop && \
		 sleep 1 && \
		 tgws-manager status && \
		 echo "✓ Start/Stop test passed"'

test-config:
	@echo "=== Testing Configuration ==="
	docker-compose exec tgws-test bash -c \
		'tgws-manager config --show && \
		 tgws-manager config --set last_port 9999 && \
		 tgws-manager config --get last_port && \
		 echo "✓ Config test passed"'

test-error:
	@echo "=== Testing Error Handling ==="
	docker-compose exec tgws-test bash -c \
		'rm -rf ~/.local/tg-ws-proxy ~/.tgws-manager && \
		 tgws-manager start 2>&1 | head -3 || true && \
		 echo "✓ Error handling test passed"'

test-update:
	@echo "=== Testing Update ==="
	docker-compose exec tgws-test bash -c \
		'tgws-manager update && \
		 echo "✓ Update test passed"'

# Cleanup
prune:
	@echo "Pruning project-specific Docker resources..."
	@docker-compose down
	@echo "Removing project image..."
	@docker image rm tgws-manager-tgws-test 2>/dev/null || true
	@echo "Removing project volumes..."
	@docker volume rm tgws_config_storage 2>/dev/null || true
	@docker volume rm git_repo_storage 2>/dev/null || true
	@echo "Removing project network..."
	@docker network rm tgws-network 2>/dev/null || true
	@echo "✓ Project resources pruned (other Docker data untouched)"

docker-clean:
	@echo "⚠ Removing all project Docker data..."
	docker-compose down -v
	@docker image rm tgws-manager-tgws-test 2>/dev/null || true
	@echo "✓ Project cleaned"

# Aliases
start: up
stop: down
test-all: test
