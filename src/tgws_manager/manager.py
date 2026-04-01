"""Core proxy management logic"""

import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .config import ConfigManager, ManagerConfig
from .utils import (
    ensure_dir,
    expand_path,
    is_port_available,
    kill_pid,
    print_error,
    print_info,
    print_success,
    print_warning,
    read_file,
    run_command,
    write_file,
)


def _is_termux() -> bool:
    """Detect if running inside Termux on Android."""
    return os.path.isdir("/data/data/com.termux")


def _termux_install_deps(proxy_path: Path) -> tuple:
    """
    Install tg-ws-proxy dependencies on Termux/Android.

    On Android, psutil and pillow cannot be built from source by pip.
    We use Termux's pkg manager for those, then pip for pure-Python deps.
    cryptography is installed via pip in step 4 (pre-built wheel available
    for aarch64-linux-android on PyPI, no Rust compilation required).
    pystray is intentionally skipped (requires desktop display server).

    Returns:
        Tuple of (exit_code, stdout, stderr) from the final pip step.
    """
    # Step 1: Install Android-compatible builds via Termux pkg
    print_info("Termux detected - installing native packages via pkg...")
    pkg_code, _, pkg_err = run_command(["pkg", "install", "-y", "python-psutil", "python-pillow"])
    if pkg_code != 0:
        print_warning(f"pkg install failed (continuing): {pkg_err}")

    # Step 2: Install build backend deps needed for --no-build-isolation editable install
    print_info("Installing build backend dependencies...")
    be_code, _, be_err = run_command(["pip", "install", "hatchling", "editables"])
    if be_code != 0:
        print_warning(f"Build backend install failed (continuing): {be_err}")

    # Step 3: Install the proxy package itself, skip deps (handled above)
    print_info("Installing tg-ws-proxy package (no-deps)...")
    exit_code, stdout, stderr = run_command(
        ["pip", "install", "--no-build-isolation", "--no-deps", "-e", "."],
        cwd=str(proxy_path),
    )
    if exit_code != 0:
        return exit_code, stdout, stderr

    # Step 4: Install remaining pure-Python deps that pip can handle on Android
    print_info("Installing pure-Python dependencies...")
    pip_code, pip_out, pip_err = run_command(
        ["pip", "install", "cryptography==46.0.5", "customtkinter==5.2.2", "pyperclip==1.9.0"]
    )
    if pip_code != 0:
        print_warning(f"Some pure-Python deps failed to install: {pip_err}")
        # Non-fatal: proxy core still works without tray/clipboard deps

    return exit_code, stdout, stderr


class ProxyManager:
    """Manages tg-ws-proxy installation and lifecycle"""

    def __init__(self, config_dir: Optional[str] = None):
        self.config_manager = ConfigManager(config_dir)
        self.config = self.config_manager.load()

    def install(self, path: Optional[str] = None, rebuild: bool = False) -> bool:
        """
        Install or update tg-ws-proxy
        
        Args:
            path: Custom installation path
            rebuild: Force rebuild of dependencies
            
        Returns:
            True if successful
        """
        if path:
            self.config.proxy_path = expand_path(path).as_posix()
            self.config_manager.save(self.config)
        
        proxy_path = Path(self.config.proxy_path)
        
        print_info(f"Installing tg-ws-proxy to {self.config.proxy_path}...")
        
        # Check if valid installation exists (has proxy script)
        proxy_script = proxy_path / "proxy" / "tg_ws_proxy.py"
        
        if proxy_path.exists() and proxy_script.exists():
            print_info("Repository already exists, verifying...")
        else:
            # Clone repository (or reclone if invalid)
            if proxy_path.exists():
                print_info("Directory exists but invalid, attempting to clean...")
                try:
                    # Try to remove the directory
                    shutil.rmtree(proxy_path)
                except OSError as e:
                    # If it's a "Device or resource busy" error (mounted volume), clean contents
                    if e.errno == 16:  # EBUSY
                        print_info("Directory is mounted (Docker volume), cleaning contents instead...")
                        try:
                            for item in proxy_path.iterdir():
                                if item.is_dir():
                                    shutil.rmtree(item)
                                else:
                                    item.unlink()
                        except Exception as clean_err:
                            print_error(f"Failed to clean directory: {clean_err}")
                            return False
                    else:
                        print_error(f"Failed to remove directory: {e}")
                        return False
            
            ensure_dir(proxy_path.parent)
            print_info(f"Cloning {self.config.git_url}...")
            exit_code, stdout, stderr = run_command(
                ["git", "clone", self.config.git_url, str(proxy_path)]
            )
            if exit_code != 0:
                print_error(f"Failed to clone repository: {stderr}")
                return False
            print_success("Repository cloned")
            
            # Verify clone was successful
            if not proxy_script.exists():
                print_error(f"Clone failed - proxy script not found at {proxy_script}")
                return False
        
        # Install Python dependencies if they exist
        print_info("Checking for Python dependencies...")
        
        req_file = proxy_path / "requirements.txt"
        setup_file = proxy_path / "setup.py"
        pyproject_file = proxy_path / "pyproject.toml"
        
        if pyproject_file.exists():
            print_info("Installing from pyproject.toml...")
            if _is_termux():
                exit_code, stdout, stderr = _termux_install_deps(proxy_path)
            else:
                exit_code, stdout, stderr = run_command(
                    ["pip", "install", "-e", "."],
                    cwd=str(proxy_path),
                )
            if exit_code == 0:
                print_success("Dependencies installed from pyproject.toml")
            else:
                print_error(f"Failed to install dependencies: {stderr}")
                if not _is_termux():
                    print_warning("This might be due to Rust compilation. Try installing rust:")
                    print_warning("pkg install -y rust")
                return False
        
        elif req_file.exists():
            print_info("Installing from requirements.txt...")
            exit_code, stdout, stderr = run_command(
                ["pip", "install", "-r", "requirements.txt"],
                cwd=str(proxy_path),
            )
            if exit_code == 0:
                print_success("Dependencies installed from requirements.txt")
            else:
                print_error(f"Failed to install dependencies: {stderr}")
                return False
        
        elif setup_file.exists():
            print_info("Installing from setup.py...")
            exit_code, stdout, stderr = run_command(
                ["pip", "install", "-e", "."],
                cwd=str(proxy_path),
            )
            if exit_code == 0:
                print_success("Dependencies installed")
            else:
                print_error(f"Failed to install dependencies: {stderr}")
                return False
        else:
            print_info("No dependency files found (will assume pre-installed dependencies)")
        
        # Final verification
        if not proxy_script.exists():
            print_error(f"Installation incomplete - proxy script not found at {proxy_script}")
            return False
        
        print_success("Installation verified and complete")
        self._write_version_info(proxy_path)
        return True

    def start(
        self,
        port: int = 1080,
        host: str = "127.0.0.1",
        dc_ips: Optional[List[str]] = None,
        verbose: bool = False,
    ) -> bool:
        """
        Start the proxy service
        
        Args:
            port: Port to listen on
            host: Host to bind to
            dc_ips: Data center IPs (format: "2:ip" or "4:ip")
            verbose: Enable verbose logging
            
        Returns:
            True if successful
        """
        proxy_path = Path(self.config.proxy_path)
        if not proxy_path.exists():
            print_error("Proxy not installed. Run 'tgws-manager install' first.")
            return False
        
        # Check if already running
        if self._is_running():
            print_warning("Proxy is already running (PID: {self._read_pid()})")
            return False
        
        # Check port availability
        if not is_port_available(port):
            print_error(f"Port {port} is not available")
            return False
        
        print_info(f"Starting proxy on {host}:{port}...")
        
        # Build command
        cmd = [
            "python",
            str(proxy_path / "proxy" / "tg_ws_proxy.py"),
            "--port",
            str(port),
            "--host",
            host,
        ]
        
        if dc_ips:
            for dc_ip in dc_ips:
                cmd.extend(["--dc-ip", dc_ip])
        
        if verbose:
            cmd.append("-v")
            print_info("Verbose mode enabled")
        
        # Start process in background
        try:
            # In verbose mode, stream output to terminal; otherwise capture it
            if verbose:
                proc = subprocess.Popen(
                    cmd,
                    cwd=str(proxy_path),
                    text=True,
                )
            else:
                proc = subprocess.Popen(
                    cmd,
                    cwd=str(proxy_path),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
            
            # Give it a moment to start
            time.sleep(1)
            
            if proc.poll() is not None:
                # Process exited already
                if verbose:
                    print_error("Failed to start proxy")
                else:
                    _, stderr = proc.communicate()
                    print_error(f"Failed to start proxy: {stderr}")
                return False
            
            self._write_pid(proc.pid)
            self.config.last_port = port
            self.config.last_host = host
            self.config_manager.save(self.config)
            
            print_success(f"Proxy started (PID: {proc.pid})")
            print_info(f"Access at {host}:{port}")
            return True
            
        except Exception as e:
            print_error(f"Failed to start proxy: {e}")
            return False

    def stop(self) -> bool:
        """
        Stop the proxy service
        
        Returns:
            True if successful
        """
        pid = self._read_pid()
        if pid is None:
            print_warning("Proxy is not running")
            return False
        
        print_info(f"Stopping proxy (PID: {pid})...")
        
        # Try graceful shutdown first
        if kill_pid(pid):
            time.sleep(1)
            self._delete_pid()
            print_success("Proxy stopped")
            return True
        else:
            print_error(f"Failed to stop proxy (PID {pid})")
            self._delete_pid()
            return False

    def status(self) -> Tuple[bool, str]:
        """
        Get proxy status
        
        Returns:
            Tuple of (is_running, status_message)
        """
        pid = self._read_pid()
        
        if pid is None:
            return False, "Proxy is not running"
        
        if self._is_process_alive(pid):
            return True, f"Proxy is running (PID: {pid}, Port: {self.config.last_port})"
        else:
            self._delete_pid()
            return False, "Proxy PID file exists but process is not running"

    def logs(self, follow: bool = False, lines: int = 50) -> Optional[str]:
        """
        Get proxy logs
        
        Args:
            follow: Follow log output
            lines: Number of lines to show
            
        Returns:
            Log content as string
        """
        log_file = Path(self.config.proxy_path) / ".tgws-manager" / "proxy.log"
        
        if not log_file.exists():
            print_warning("No logs available yet")
            return None
        
        if follow:
            # Use tail -f behavior
            import time as time_module
            
            try:
                with open(log_file, "r") as f:
                    # Jump to end
                    f.seek(0, 2)
                    while True:
                        line = f.readline()
                        if line:
                            print(line, end="")
                        else:
                            time_module.sleep(0.1)
            except KeyboardInterrupt:
                print("\n[*] Log following stopped")
                return None
        else:
            # Read last N lines
            content = read_file(log_file)
            lines_list = content.split("\n")
            return "\n".join(lines_list[-lines:])

    def update(self, rebuild: bool = False) -> bool:
        """
        Update proxy to latest version
        
        Args:
            rebuild: Force rebuild
            
        Returns:
            True if successful
        """
        proxy_path = Path(self.config.proxy_path)
        
        if not proxy_path.exists():
            print_error("Proxy not installed. Run 'tgws-manager install' first.")
            return False
        
        was_running = self._is_running()
        if was_running:
            print_info("Stopping proxy for update...")
            self.stop()
        
        print_info("Updating repository...")
        exit_code, stdout, stderr = run_command(
            ["git", "pull"],
            cwd=str(proxy_path),
        )
        
        if exit_code != 0:
            print_error(f"Failed to update: {stderr}")
            return False
        
        print_success("Repository updated")
        
        if rebuild:
            print_info("Rebuilding dependencies...")
            if _is_termux():
                exit_code, stdout, stderr = _termux_install_deps(proxy_path)
            else:
                exit_code, stdout, stderr = run_command(
                    ["pip", "install", "--upgrade", "-e", "."],
                    cwd=str(proxy_path),
                )
            if exit_code != 0:
                print_error(f"Failed to rebuild: {stderr}")
                return False
            print_success("Dependencies rebuilt")
        
        self._write_version_info(proxy_path)
        
        if was_running:
            print_info("Restarting proxy...")
            return self.start(port=self.config.last_port, host=self.config.last_host)
        
        return True

    def uninstall(self, purge: bool = False) -> bool:
        """
        Uninstall proxy
        
        Args:
            purge: Also remove configuration
            
        Returns:
            True if successful
        """
        proxy_path = Path(self.config.proxy_path)
        
        if self._is_running():
            print_info("Stopping proxy...")
            self.stop()
        
        if proxy_path.exists():
            print_info(f"Removing {self.config.proxy_path}...")
            import shutil
            try:
                shutil.rmtree(proxy_path)
                print_success("Proxy uninstalled")
            except Exception as e:
                print_error(f"Failed to uninstall: {e}")
                return False
        
        if purge:
            print_info("Removing configuration...")
            self.config_manager.delete()
            print_success("Configuration removed")
        
        return True

    @staticmethod
    def _is_process_alive(pid: int) -> bool:
        """Check if process is still alive"""
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    def _is_running(self) -> bool:
        """Check if proxy is running"""
        pid = self._read_pid()
        return pid is not None and self._is_process_alive(pid)

    def _read_pid(self) -> Optional[int]:
        """Read PID from file"""
        pid_file = Path(self.config.proxy_path) / ".tgws-manager" / "proxy.pid"
        content = read_file(pid_file)
        try:
            return int(content.strip())
        except (ValueError, AttributeError):
            return None

    def _write_pid(self, pid: int) -> None:
        """Write PID to file"""
        pid_file = Path(self.config.proxy_path) / ".tgws-manager" / "proxy.pid"
        ensure_dir(pid_file.parent)
        write_file(pid_file, str(pid))

    def _delete_pid(self) -> None:
        """Delete PID file"""
        pid_file = Path(self.config.proxy_path) / ".tgws-manager" / "proxy.pid"
        try:
            if pid_file.exists():
                pid_file.unlink()
        except Exception:
            pass

    def _write_version_info(self, proxy_path: Path) -> None:
        """Write version information"""
        version_file = proxy_path / ".tgws-manager" / "version.json"
        ensure_dir(version_file.parent)
        
        exit_code, stdout, stderr = run_command(
            ["git", "describe", "--tags", "--always"],
            cwd=str(proxy_path),
            capture_output=True,
        )
        
        version_info = {
            "installed_at": time.time(),
            "version": stdout.strip() if exit_code == 0 else "unknown",
        }
        
        try:
            ensure_dir(version_file.parent)
            version_file.write_text(json.dumps(version_info, indent=2))
        except Exception:
            pass

    def get_version(self) -> str:
        """Get installed version"""
        version_file = Path(self.config.proxy_path) / ".tgws-manager" / "version.json"
        try:
            with open(version_file) as f:
                data = json.load(f)
                return data.get("version", "unknown")
        except Exception:
            return "unknown"
