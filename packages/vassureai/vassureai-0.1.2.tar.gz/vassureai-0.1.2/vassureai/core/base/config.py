"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Base configuration implementation for VAssureAI framework.

Provides the default implementation of configuration interfaces,
supporting environment variables, JSON files, and in-memory settings.
"""

import os
import json
from typing import Any, Dict, Optional
from dataclasses import asdict, dataclass, field
from ..interfaces.config import IConfig, IConfigProvider


@dataclass
class RetryConfig:
    """Retry configuration settings."""
    max_retries: int = 2
    retry_delay: int = 2
    retry_on_network_error: bool = True
    retry_only_on_failure: bool = True


@dataclass
class BrowserConfig:
    """Browser automation settings."""
    record_video: bool = True
    video_dir: str = "videos"
    screenshot_dir: str = "screenshots"
    headless: bool = True


@dataclass
class VisualConfig:
    """Visual verification settings."""
    highlight: bool = False
    screenshot_on_step: bool = True
    screenshot_on_error: bool = True


@dataclass
class BaseConfig(IConfig):
    """Base configuration implementation."""
    retry: RetryConfig = field(default_factory=RetryConfig)
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    visual: VisualConfig = field(default_factory=VisualConfig)
    log_dir: str = "logs"
    report_dir: str = "reports"
    metrics_dir: str = "metrics"
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key."""
        parts = key.split('.')
        value = self
        try:
            for part in parts:
                value = getattr(value, part)
            return value
        except AttributeError:
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        parts = key.split('.')
        target = self
        for part in parts[:-1]:
            if not hasattr(target, part):
                raise KeyError(f"Configuration key not found: {key}")
            target = getattr(target, part)
        setattr(target, parts[-1], value)
    
    def load(self, source: str) -> None:
        """Load configuration from a JSON file."""
        if not os.path.exists(source):
            raise FileNotFoundError(f"Configuration file not found: {source}")
        
        with open(source, 'r') as f:
            data = json.load(f)
            self._update_from_dict(data)
    
    def save(self, destination: Optional[str] = None) -> None:
        """Save configuration to a JSON file."""
        data = self.to_dict()
        dest = destination or "config.json"
        
        with open(dest, 'w') as f:
            json.dump(data, f, indent=2)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseConfig':
        """Create configuration from dictionary."""
        config = cls()
        config._update_from_dict(data)
        return config
    
    @classmethod
    def from_env(cls) -> 'BaseConfig':
        """Create configuration from environment variables."""
        config = cls()
        
        # Map environment variables to configuration
        env_mapping = {
            'VASSURE_MAX_RETRIES': ('retry.max_retries', int),
            'VASSURE_RETRY_DELAY': ('retry.retry_delay', int),
            'VASSURE_RETRY_ON_NETWORK': ('retry.retry_on_network_error', lambda x: x.lower() == 'true'),
            'VASSURE_RECORD_VIDEO': ('browser.record_video', lambda x: x.lower() == 'true'),
            'VASSURE_HEADLESS': ('browser.headless', lambda x: x.lower() == 'true'),
            'VASSURE_HIGHLIGHT': ('visual.highlight', lambda x: x.lower() == 'true'),
            'VASSURE_SCREENSHOT_ON_STEP': ('visual.screenshot_on_step', lambda x: x.lower() == 'true'),
            'VASSURE_SCREENSHOT_ON_ERROR': ('visual.screenshot_on_error', lambda x: x.lower() == 'true'),
            'VASSURE_LOG_DIR': ('log_dir', str),
            'VASSURE_REPORT_DIR': ('report_dir', str),
            'VASSURE_METRICS_DIR': ('metrics_dir', str)
        }
        
        for env_var, (config_key, convert) in env_mapping.items():
            if env_var in os.environ:
                try:
                    value = convert(os.environ[env_var])
                    config.set(config_key, value)
                except (ValueError, TypeError) as e:
                    raise ValueError(f"Invalid environment variable {env_var}: {e}")
        
        return config
    
    def _update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update configuration from dictionary."""
        for key, value in data.items():
            if isinstance(value, dict):
                current = getattr(self, key)
                for subkey, subvalue in value.items():
                    setattr(current, subkey, subvalue)
            else:
                setattr(self, key, value)


class BaseConfigProvider(IConfigProvider):
    """Default configuration provider implementation."""
    
    def __init__(self, config: Optional[BaseConfig] = None):
        self._config = config or BaseConfig.from_env()
    
    def get_config(self) -> IConfig:
        """Get the configuration instance."""
        return self._config