"""CLI interface for tgws-manager"""

import click
from pathlib import Path
from typing import Optional, Tuple

from .manager import ProxyManager
from .utils import (
    print_error,
    print_info,
    print_success,
    print_warning,
    is_termux,
    run_command,
)


@click.group()
@click.version_option()
def main() -> None:
    """
    tgws-manager: Independent CLI tool to manage tg-ws-proxy on Termux
    
    tgws-manager is a SEPARATE tool (not part of tg-ws-proxy).
    It manages tg-ws-proxy as an external dependency.
    Both can be installed, updated, and removed independently.
    """
    if not is_termux():
        print_warning("⚠ This tool is designed for Termux. Some features may not work properly.")


@main.command()
@click.option(
    "--path",
    default=None,
    help="Custom installation path (default: ~/.local/tg-ws-proxy)",
)
@click.option("--rebuild", is_flag=True, help="Force rebuild of dependencies")
def install(path: Optional[str], rebuild: bool) -> None:
    """Install tg-ws-proxy from GitHub"""
    manager = ProxyManager()
    
    if manager.install(path=path, rebuild=rebuild):
        print_success("Installation complete!")
        print_info(f"Run 'tgws-manager start' to start the proxy")
    else:
        print_error("Installation failed")
        raise SystemExit(1)


@main.command()
@click.option("--port", default=1080, type=int, help="Port to listen on")
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.option(
    "--dc-ip",
    multiple=True,
    help="Data center IP (format: 2:149.154.167.220 or 4:149.154.167.220)",
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging")
def start(port: int, host: str, dc_ip: Tuple[str, ...], verbose: bool) -> None:
    """Start the proxy service"""
    manager = ProxyManager()
    
    # Only install if not already installed
    proxy_path = Path(manager.config.proxy_path)
    proxy_script = proxy_path / "proxy" / "tg_ws_proxy.py"
    
    if not proxy_script.exists():
        # Proxy not installed, install it
        if not manager.install():
            print_error("Proxy not installed. Run 'tgws-manager install' first.")
            raise SystemExit(1)
    
    dc_ips = list(dc_ip) if dc_ip else None
    
    if manager.start(port=port, host=host, dc_ips=dc_ips, verbose=verbose):
        print_success(f"Proxy started on {host}:{port}")
    else:
        print_error("Failed to start proxy")
        raise SystemExit(1)


@main.command()
def stop() -> None:
    """Stop the proxy service"""
    manager = ProxyManager()
    
    if manager.stop():
        print_success("Proxy stopped")
    else:
        raise SystemExit(1)


@main.command()
def status() -> None:
    """Show proxy status"""
    manager = ProxyManager()
    is_running, message = manager.status()
    
    if is_running:
        print_success(message)
    else:
        print_info(message)


@main.command()
@click.option(
    "-f",
    "--follow",
    is_flag=True,
    help="Follow log output (like tail -f)",
)
@click.option(
    "-n",
    "--lines",
    default=50,
    type=int,
    help="Number of lines to display",
)
def logs(follow: bool, lines: int) -> None:
    """View proxy logs"""
    manager = ProxyManager()
    
    if follow:
        print_info("Following logs (Ctrl+C to stop)...")
    
    result = manager.logs(follow=follow, lines=lines)
    
    if result and not follow:
        print(result)


@main.command()
@click.option("--rebuild", is_flag=True, help="Rebuild dependencies")
def update(rebuild: bool) -> None:
    """Update proxy to latest version"""
    manager = ProxyManager()
    
    if manager.update(rebuild=rebuild):
        print_success("Proxy updated successfully")
        print_info("Run 'tgws-manager start' to start the proxy")
    else:
        print_error("Update failed")
        raise SystemExit(1)


@main.command()
@click.option(
    "--purge",
    is_flag=True,
    help="Also remove configuration files",
)
@click.confirmation_option(
    prompt="Are you sure you want to uninstall the proxy?",
    help="Confirm uninstallation",
)
def uninstall(purge: bool) -> None:
    """Uninstall the proxy"""
    manager = ProxyManager()
    
    if manager.uninstall(purge=purge):
        print_success("Proxy uninstalled")
    else:
        print_error("Uninstall failed")
        raise SystemExit(1)


@main.command()
@click.option(
    "--set",
    "set_config",
    nargs=2,
    help="Set config value: --set KEY VALUE",
)
@click.option(
    "--get",
    help="Get config value",
)
@click.option(
    "--show",
    is_flag=True,
    help="Show all configuration",
)
def config(set_config: Optional[Tuple[str, str]], get: Optional[str], show: bool) -> None:
    """Manage configuration"""
    manager = ProxyManager()
    
    if set_config:
        key, value = set_config
        try:
            # Try to parse as JSON for complex types
            import json
            try:
                parsed_value = json.loads(value)
            except json.JSONDecodeError:
                parsed_value = value
            
            manager.config_manager.update(**{key: parsed_value})
            print_success(f"Set {key} = {value}")
        except Exception as e:
            print_error(f"Failed to set config: {e}")
            raise SystemExit(1)
    
    elif get:
        value = manager.config_manager.get(get)
        if value is not None:
            print(f"{get}: {value}")
        else:
            print_error(f"Config key not found: {get}")
            raise SystemExit(1)
    
    elif show:
        cfg = manager.config_manager.load()
        print("\nConfiguration:")
        print("-" * 50)
        for key, value in cfg.dict().items():
            print(f"{key}: {value}")
        print("-" * 50)
    
    else:
        print_info("Use --set, --get, or --show to manage configuration")
        print_info("Example: tgws-manager config --show")


@main.command()
def info() -> None:
    """Show system, tgws-manager, and proxy information"""
    from . import __version__
    
    manager = ProxyManager()
    is_running, status_msg = manager.status()
    version = manager.get_version()
    
    print("\n" + "=" * 60)
    print("tgws-manager System Information")
    print("=" * 60)
    print(f"\n[tgws-manager Tool]")
    print(f"  Version: {__version__}")
    print(f"  Status: Ready")
    
    print(f"\n[tg-ws-proxy (Managed)]")
    print(f"  Installation: {manager.config.proxy_path}")
    print(f"  Status: {status_msg}")
    print(f"  Version: {version}")
    print(f"  Git URL: {manager.config.git_url}")
    
    print(f"\n[Configuration]")
    print(f"  Config Dir: ~/.tgws-manager/")
    print(f"  Auto Start: {manager.config.auto_start}")
    print("=" * 60 + "\n")


@main.command(name="self-update")
def self_update() -> None:
    """Update tgws-manager tool itself (not the proxy)"""
    print_info("Updating tgws-manager...")
    exit_code, stdout, stderr = run_command(
        ["pip", "install", "--upgrade", "tgws-manager"],
        capture_output=True,
    )
    
    if exit_code != 0:
        print_error(f"Failed to update tgws-manager: {stderr}")
        print_info("Try manual update: pip install --upgrade tgws-manager")
        raise SystemExit(1)
    
    print_success("tgws-manager updated successfully!")
    print_info("Run 'tgws-manager --version' to verify")


if __name__ == "__main__":
    main()
