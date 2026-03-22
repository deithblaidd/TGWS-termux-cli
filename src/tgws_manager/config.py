"""Configuration management for tgws-manager"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from pydantic import BaseModel, Field, validator
except ImportError:
    from pydantic.v1 import BaseModel, Field, validator


class ManagerConfig(BaseModel):
    """Configuration model for tgws-manager"""

    proxy_path: str = Field(default_factory=lambda: os.path.expanduser("~/.local/tg-ws-proxy"))
    git_url: str = "https://github.com/Flowseal/tg-ws-proxy"
    auto_start: bool = False
    last_port: int = 1080
    last_host: str = "127.0.0.1"
    check_updates: bool = True

    class Config:
        validate_assignment = True


class ConfigManager:
    """Manages configuration files"""

    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            config_dir = os.path.expanduser("~/.tgws-manager")
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_dir()

    def _ensure_config_dir(self) -> None:
        """Create config directory if it doesn't exist"""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load(self) -> ManagerConfig:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                return ManagerConfig(**data)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"[!] Error loading config: {e}. Using defaults.")
                return ManagerConfig()
        return ManagerConfig()

    def save(self, config: ManagerConfig) -> None:
        """Save configuration to file"""
        self._ensure_config_dir()
        with open(self.config_file, "w") as f:
            json.dump(config.dict(), f, indent=2)

    def update(self, **kwargs) -> ManagerConfig:
        """Update specific config values"""
        config = self.load()
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        self.save(config)
        return config

    def get(self, key: str) -> Optional[Any]:
        """Get a specific config value"""
        config = self.load()
        return getattr(config, key, None)

    def delete(self) -> None:
        """Delete configuration file"""
        if self.config_file.exists():
            self.config_file.unlink()
