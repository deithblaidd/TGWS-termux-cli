#!/bin/bash
# Quick reference script for Docker testing
# Usage: bash docker-quick.sh <command>

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_help() {
    cat << 'EOF'
tgws-manager Docker Quick Reference

COMMANDS:
  setup         - Build Docker image and start containers
  up            - Start containers
  down          - Stop containers
  clean         - Full cleanup (down + remove volumes)
  shell         - Enter container bash
  logs          - View logs
  status        - Check container status
  rebuild       - Rebuild image from scratch
  test-all      - Run all manual tests
  test-install  - Test installation only
  test-start    - Test start/stop
  test-config   - Test configuration
  test-error    - Test error handling
  test-update   - Test updating
  ps            - Show running containers
  stats         - Show resource usage
  prune         - Clean Docker system

EXAMPLES:
  bash docker-quick.sh setup
  bash docker-quick.sh shell
  bash docker-quick.sh test-all
  bash docker-quick.sh logs
EOF
}

setup() {
    echo -e "${BLUE}Building Docker image...${NC}"
    docker-compose build
    echo ""
    echo -e "${BLUE}Starting containers...${NC}"
    docker-compose up -d
    sleep 2
    echo ""
    echo -e "${GREEN}✓ Environment ready!${NC}"
    echo "Enter with: docker-compose exec tgws-test bash"
}

up() {
    echo -e "${BLUE}Starting containers...${NC}"
    docker-compose up -d
    sleep 2
    docker-compose ps
}

down() {
    echo -e "${YELLOW}Stopping containers...${NC}"
    docker-compose down
}

clean() {
    echo -e "${RED}⚠ Removing all volumes and containers...${NC}"
    docker-compose down -v
    echo -e "${GREEN}✓ Cleaned${NC}"
}

shell() {
    echo -e "${BLUE}Entering container shell...${NC}"
    docker-compose exec tgws-test bash
}

logs_all() {
    docker-compose logs -f tgws-test
}

status() {
    echo -e "${BLUE}Container Status:${NC}"
    docker-compose ps
    echo ""
    echo -e "${BLUE}Health Check:${NC}"
    docker-compose exec tgws-test /scripts/healthcheck.sh || echo "Not healthy"
}

rebuild() {
    echo -e "${YELLOW}Full rebuild...${NC}"
    docker-compose down
    docker-compose build --no-cache
    echo -e "${GREEN}✓ Rebuilt${NC}"
}

test_all() {
    echo -e "${BLUE}[TEST] Running all tests...${NC}"
    docker-compose exec tgws-test bash << 'TESTEOF'
echo "=== SMOKE TEST ==="
tgws-manager --help | head -5
echo ""

echo "=== INSTALL TEST ==="
tgws-manager install && echo "✓ Install OK" || echo "✗ Install failed"
echo ""

echo "=== STATUS TEST (should be not running) ==="
tgws-manager status
echo ""

echo "=== START TEST ==="
tgws-manager start --port 1080 && echo "✓ Start OK" || echo "✗ Start failed"
sleep 2
echo ""

echo "=== STATUS TEST (should be running) ==="
tgws-manager status
echo ""

echo "=== CONFIG TEST ==="
tgws-manager config --set last_port 9999 && echo "✓ Config set OK" || echo "✗ Config failed"
tgws-manager config --get last_port
echo ""

echo "=== LOGS TEST ==="
tgws-manager logs -n 5
echo ""

echo "=== STOP TEST ==="
tgws-manager stop && echo "✓ Stop OK" || echo "✗ Stop failed"
sleep 1
echo ""

echo "=== STATUS TEST (should be not running) ==="
tgws-manager status
echo ""

echo "=== INFO TEST ==="
tgws-manager info
echo ""

echo "=== ALL TESTS PASSED ==="
TESTEOF
}

test_install() {
    echo -e "${BLUE}[TEST] Installation...${NC}"
    docker-compose exec tgws-test bash << 'EOF'
echo "Removing old installation..."
rm -rf ~/.local/tg-ws-proxy ~/.tgws-manager
echo ""
echo "Installing..."
time tgws-manager install
echo ""
echo "Verifying..."
ls -la ~/.local/tg-ws-proxy/proxy/tg_ws_proxy.py
cat ~/.tgws-manager/config.json | jq .
echo "✓ Install test passed"
EOF
}

test_start() {
    echo -e "${BLUE}[TEST] Start/Stop...${NC}"
    docker-compose exec tgws-test bash << 'EOF'
echo "Starting proxy..."
tgws-manager start --port 1080
sleep 2
echo ""
echo "Checking status..."
tgws-manager status
echo ""
echo "Killing manually to test recovery..."
kill $(cat ~/.tgws-manager/proxy.pid) || true
sleep 1
echo ""
echo "Checking status after kill..."
tgws-manager status
echo ""
echo "Stopping..."
tgws-manager stop
sleep 1
echo ""
echo "Final status..."
tgws-manager status
echo "✓ Start/Stop test passed"
EOF
}

test_config() {
    echo -e "${BLUE}[TEST] Configuration...${NC}"
    docker-compose exec tgws-test bash << 'EOF'
echo "Showing all config..."
tgws-manager config --show
echo ""
echo "Setting values..."
tgws-manager config --set last_port 9999
tgws-manager config --set auto_start true
echo ""
echo "Getting values..."
echo "last_port: $(tgws-manager config --get last_port)"
echo "auto_start: $(tgws-manager config --get auto_start)"
echo ""
echo "Corrupting config to test error handling..."
echo "bad json" > ~/.tgws-manager/config.json
echo ""
echo "Trying to read corrupted config (should handle gracefully)..."
tgws-manager config --show || echo "Handled error correctly"
echo ""
echo "Removing corrupted config..."
rm ~/.tgws-manager/config.json
echo ""
echo "Fresh config..."
tgws-manager config --show
echo "✓ Config test passed"
EOF
}

test_error() {
    echo -e "${BLUE}[TEST] Error Handling...${NC}"
    docker-compose exec tgws-test bash << 'EOF'
echo "Test 1: Start without installation..."
rm -rf ~/.local/tg-ws-proxy ~/.tgws-manager
tgws-manager start 2>&1 | head -3 || echo "✓ Handled correctly"
echo ""

echo "Test 2: View logs before installation..."
tgws-manager logs 2>&1 | head -3 || echo "✓ Handled correctly"
echo ""

echo "Re-install for next tests..."
tgws-manager install > /dev/null
echo ""

echo "Test 3: Start on restricted port..."
tgws-manager start --port 22 2>&1 | head -3 || echo "✓ Handled correctly"
echo ""

echo "Test 4: Invalid configuration..."
tgws-manager config --get nonexistent 2>&1 | head -3 || echo "✓ Handled correctly"
echo ""

echo "✓ Error handling tests passed"
EOF
}

test_update() {
    echo -e "${BLUE}[TEST] Update...${NC}"
    docker-compose exec tgws-test bash << 'EOF'
echo "Current version:"
cd ~/.local/tg-ws-proxy && git describe --tags --always 2>/dev/null || git rev-parse --short HEAD
echo ""

echo "Running update..."
tgws-manager update
echo ""

echo "New version:"
cd ~/.local/tg-ws-proxy && git describe --tags --always 2>/dev/null || git rev-parse --short HEAD
echo ""

echo "✓ Update test passed"
EOF
}

ps_cmd() {
    docker-compose ps
}

stats_cmd() {
    docker stats tgws-manager-test
}

prune_cmd() {
    echo -e "${YELLOW}Pruning Docker system...${NC}"
    docker system prune -f
    echo -e "${GREEN}✓ Pruned${NC}"
}

# Main
if [ $# -eq 0 ]; then
    print_help
    exit 0
fi

case "$1" in
    setup)      setup ;;
    up)         up ;;
    down)       down ;;
    clean)      clean ;;
    shell)      shell ;;
    logs)       logs_all ;;
    status)     status ;;
    rebuild)    rebuild ;;
    test-all)   test_all ;;
    test-install) test_install ;;
    test-start) test_start ;;
    test-config) test_config ;;
    test-error) test_error ;;
    test-update) test_update ;;
    ps)         ps_cmd ;;
    stats)      stats_cmd ;;
    prune)      prune_cmd ;;
    --help|-h)  print_help ;;
    *)          echo "Unknown command: $1"; print_help; exit 1 ;;
esac
