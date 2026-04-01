# tgws-manager Testing Environment
# Lightweight Docker image for manual testing and development

FROM python:3.11-slim

# Labels
LABEL maintainer="tgws-manager"
LABEL description="Testing environment for tgws-manager"

# Combine all setup into single RUN to reduce layers
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
    tzdata \
    && rm -rf /var/lib/apt/lists/* && \
    # Set timezone
    ln -sf /usr/share/zoneinfo/UTC /etc/localtime && \
    # Create test user (simulate Termux environment)
    useradd -m -s /bin/bash testuser && \
    # Create working directories
    mkdir -p /workspace/tgws-manager /workspace/tg-ws-proxy /home/testuser/.local /home/testuser/.tgws-manager /scripts && \
    chown -R testuser:testuser /workspace /home/testuser

# Set timezone env
ENV TZ=UTC \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /workspace/tgws-manager

# Copy source code
COPY --chown=testuser:testuser . /workspace/tgws-manager/

# Install Python dependencies and tgws-manager
RUN pip install --no-cache-dir --quiet \
    click>=8.0.0 \
    colorama>=0.4.4 \
    "pydantic>=1.10.0,<2.0" && \
    pip install --no-cache-dir -e /workspace/tgws-manager/

# Test script
RUN cat > /scripts/test-tgws-manager.sh << 'TESTEOF'
#!/bin/bash
set -e

echo "=========================================="
echo "  tgws-manager Testing Environment"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}[1] System Information${NC}"
echo "Python: $(python --version)"
echo "pip: $(pip --version | awk '{print $2}')"
echo "Git: $(git --version | awk '{print $3}')"
echo "User: $(whoami)"
echo "Home: $HOME"
echo ""

echo -e "${BLUE}[2] tgws-manager Installation${NC}"
if command -v tgws-manager &> /dev/null; then
    echo -e "${GREEN}✓ tgws-manager is installed${NC}"
    tgws-manager --version
else
    echo -e "${RED}✗ tgws-manager not found${NC}"
    exit 1
fi
echo ""

echo -e "${BLUE}[3] Checking Configuration${NC}"
if [ -d "$HOME/.tgws-manager" ]; then
    echo -e "${GREEN}✓ Config directory exists: $HOME/.tgws-manager${NC}"
else
    echo -e "${YELLOW}⚠ Config directory doesn't exist yet (will be created on first use)${NC}"
fi
echo ""

echo -e "${BLUE}[4] Available Commands${NC}"
echo "  tgws-manager install     - Download and setup tg-ws-proxy"
echo "  tgws-manager start       - Start the proxy"
echo "  tgws-manager stop        - Stop the proxy"
echo "  tgws-manager status      - Check proxy status"
echo "  tgws-manager logs        - View proxy logs"
echo "  tgws-manager update      - Update tg-ws-proxy"
echo "  tgws-manager config      - Manage settings"
echo "  tgws-manager info        - Show system info"
echo "  tgws-manager help        - Show all commands"
echo ""

echo -e "${BLUE}[5] Quick Test - Show Help${NC}"
tgws-manager --help | head -20
echo ""

echo -e "${GREEN}✓ Environment ready for testing!${NC}"
echo ""
echo "Next steps:"
echo "  1. Run: tgws-manager install"
echo "  2. Run: tgws-manager start --port 1080"
echo "  3. Run: tgws-manager status"
echo "  4. Run: tgws-manager logs -f"
echo "  5. Run: tgws-manager stop"
echo ""
TESTEOF

RUN chmod +x /scripts/test-tgws-manager.sh

# Initialization script using printf to avoid line ending issues
RUN printf '#!/bin/bash\nset -e\n\n# If running as root, switch to testuser\nif [ "$(id -u)" = "0" ]; then\n    mkdir -p /home/testuser/.local/tg-ws-proxy\n    mkdir -p /home/testuser/.tgws-manager\n    chown -R testuser:testuser /home/testuser\n    export HOME=/home/testuser\n    exec su - testuser "$@"\nfi\n\n# If no arguments, show banner and start shell\nif [ $# -eq 0 ]; then\n    /scripts/test-tgws-manager.sh\n    exec /bin/bash\nfi\n\n# Run provided command\nexec "$@"\n' > /scripts/entrypoint.sh && chmod +x /scripts/entrypoint.sh

# Health check script
RUN printf '#!/bin/bash\n\nif ! command -v tgws-manager &> /dev/null; then\n    echo "tgws-manager not installed"\n    exit 1\nfi\n\nif ! tgws-manager --version &> /dev/null; then\n    echo "tgws-manager not working"\n    exit 1\nfi\n\nif [ ! -d "$HOME/.tgws-manager" ]; then\n    echo "Config dir ready (will be created on first use)"\nelse\n    echo "Config dir exists"\nfi\n\necho "Healthy"\nexit 0\n' > /scripts/healthcheck.sh && chmod +x /scripts/healthcheck.sh

# Verify installation
RUN echo "=== Installation Verification ===" && \
    python -c "import click; print(f'click: {click.__version__}')" && \
    python -c "import colorama; print(f'colorama: {colorama.__version__}')" && \
    python -c "import pydantic; print(f'pydantic: {pydantic.__version__}')" && \
    tgws-manager --version && \
    echo "=== All verified ===" || exit 1

# Set default user
USER testuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD /scripts/healthcheck.sh

# Expose ports (for proxy testing)
EXPOSE 1080 1081 1082 1083 1084 1085 9999

# Entry point
ENTRYPOINT ["/scripts/entrypoint.sh"]
CMD ["/bin/bash"]
