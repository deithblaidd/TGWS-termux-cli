"""
tgws-manager: CLI tool for managing tg-ws-proxy on Termux
"""

__version__ = "1.0.0"
__author__ = "tg-ws-proxy-manager"

from .manager import ProxyManager

__all__ = ["ProxyManager"]
