"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Configuration interfaces for VAssureAI framework.

These interfaces define the contract for configuration components, allowing
for different configuration implementations while maintaining a consistent API.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class IConfig(ABC):
    """Base interface for configuration components."""
    
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key with optional default."""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        pass
    
    @abstractmethod
    def load(self, source: str) -> None:
        """Load configuration from a source (file, environment, etc.)."""
        pass
    
    @abstractmethod
    def save(self, destination: Optional[str] = None) -> None:
        """Save configuration to a destination."""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IConfig':
        """Create configuration from dictionary."""
        pass
    
    @classmethod
    @abstractmethod
    def from_env(cls) -> 'IConfig':
        """Create configuration from environment variables."""
        pass


class IConfigProvider(ABC):
    """Interface for configuration providers."""
    
    @abstractmethod
    def get_config(self) -> IConfig:
        """Get the configuration instance."""
        pass