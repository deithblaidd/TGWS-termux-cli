"""Utility functions for tgws-manager"""

import os
import signal
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple

try:
    from colorama import Fore, Style, init
    
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False


class Colors:
    """ANSI color codes"""

    SUCCESS = "\033[92m" if HAS_COLOR else ""
    ERROR = "\033[91m" if HAS_COLOR else ""
    INFO = "\033[94m" if HAS_COLOR else ""
    WARNING = "\033[93m" if HAS_COLOR else ""
    RESET = "\033[0m" if HAS_COLOR else ""


def print_success(msg: str) -> None:
    """Print success message"""
    print(f"{Colors.SUCCESS}[+]{Colors.RESET} {msg}")


def print_error(msg: str) -> None:
    """Print error message"""
    print(f"{Colors.ERROR}[!]{Colors.RESET} {msg}", file=sys.stderr)


def print_info(msg: str) -> None:
    """Print info message"""
    print(f"{Colors.INFO}[*]{Colors.INFO} {msg}")


def print_warning(msg: str) -> None:
    """Print warning message"""
    print(f"{Colors.WARNING}[?]{Colors.RESET} {msg}")


def run_command(
    cmd: list, cwd: Optional[str] = None, capture_output: bool = False
) -> Tuple[int, str, str]:
    """
    Run a shell command and return exit code, stdout, stderr
    
    Args:
        cmd: Command as list
        cwd: Working directory
        capture_output: Whether to capture output
        
    Returns:
        Tuple of (exit_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            timeout=300,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out after 300 seconds"
    except Exception as e:
        return 1, "", str(e)


def kill_pid(pid: int, signal_type: int = signal.SIGTERM) -> bool:
    """
    Kill a process by PID
    
    Args:
        pid: Process ID
        signal_type: Signal to send (default: SIGTERM)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        os.kill(pid, signal_type)
        return True
    except (ProcessLookupError, Permission):
        return False


def is_port_available(port: int) -> bool:
    """Check if a port is available"""
    try:
        import socket

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(("127.0.0.1", port))
        sock.close()
        return result != 0
    except Exception:
        return True


def expand_path(path: str) -> Path:
    """Expand user home directory and return Path object"""
    return Path(path).expanduser()


def ensure_dir(path: Path) -> None:
    """Ensure directory exists"""
    path.mkdir(parents=True, exist_ok=True)


def read_file(path: Path, default: str = "") -> str:
    """Safely read file contents"""
    try:
        if path.exists():
            return path.read_text()
        return default
    except Exception:
        return default


def write_file(path: Path, content: str) -> None:
    """Safely write file contents"""
    try:
        ensure_dir(path.parent)
        path.write_text(content)
    except Exception as e:
        print_error(f"Failed to write file {path}: {e}")


def is_termux() -> bool:
    """Check if running in Termux environment"""
    return os.path.exists("/data/data/com.termux") or "TERMUX_VERSION" in os.environ
