# Repository Structure (After Independence Refactoring)

This shows how `tgws-manager` should be organized as a **completely separate repository**.

## Current State (PLANNED)

```
tgws-manager/  ← Separate GitHub Repository
├── README.md
├── QUICKSTART.md
├── INSTALL.md
├── USAGE.md
├── ARCHITECTURE.md               ← NEW: Architecture & independence docs
├── DEVELOPMENT.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── src/tgws_manager/
    ├── __init__.py
    ├── cli.py                     ← Updated: clarified independence
    ├── manager.py
    ├── config.py
    └── utils.py
```

## Related Repository

```
tg-ws-proxy/  ← Separate GitHub Repository (https://github.com/Flowseal/tg-ws-proxy)
├── proxy/
│   └── tg_ws_proxy.py
├── pyproject.toml
├── README.md
└── [other proxy files]
```

## Installation Flow (Independent)

### Step 1: Install tgws-manager
```bash
# User clones/installs tgws-manager separately
git clone https://github.com/[your-username]/tgws-manager
cd tgws-manager
pip install -e .
```

### Step 2: Install tg-ws-proxy (via tgws-manager)
```bash
# tgws-manager handles downloading tg-ws-proxy
tgws-manager install
```

Result:
- `~/.local/tg-ws-proxy/` — tg-ws-proxy installation (from Flowseal/tg-ws-proxy)
- `~/.tgws-manager/` — tgws-manager configuration (from your user's tgws-manager)

## Key Points

✅ **tgws-manager is NOT inside tg-ws-proxy repository**
✅ **tgws-manager doesn't import tg-ws-proxy code**
✅ **tgws-manager manages tg-ws-proxy as dependency via git clone**
✅ **Both can be updated independently**
✅ **Users can use tg-ws-proxy without tgws-manager**

## Update Commands (Clear Distinction)

```bash
# Update tg-ws-proxy (the managed tool)
tgws-manager update

# Update tgws-manager (the manager tool)
tgws-manager self-update
# OR
pip install --upgrade tgws-manager
```

## No Coupling

- tgws-manager doesn't depend on tg-ws-proxy source code
- tg-ws-proxy doesn't depend on tgws-manager
- tgws-manager just:
  - Clones the repo
  - Tracks processes
  - Manages configuration

## Next Steps (If Creating Separate Repo)

1. Create new GitHub repo: `tgws-manager`
2. Move this code there
3. Update git URLs from `[your-username]` placeholders
4. Update documentation examples
5. Publish to PyPI (optional)

## Publishing to PyPI

For users to easily install via `pip install tgws-manager`:

```bash
# Build distribution
python -m build

# Upload to PyPI (requires API token)
twine upload dist/*
```

Then users can simply:
```bash
pip install tgws-manager
tgws-manager install
```

## File Preparation Complete

All documentation, code, and structure have been updated to reflect:
- **Complete independence** from tg-ws-proxy
- **Clear separation** between manager and proxy
- **Independent update paths** for each component
- **Modular architecture** with no coupling
