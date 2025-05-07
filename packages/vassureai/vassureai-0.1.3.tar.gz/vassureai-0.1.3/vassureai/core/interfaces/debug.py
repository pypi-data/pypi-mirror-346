"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Debugging interfaces for VAssureAI framework.

These interfaces define the contract for debugging components, allowing
for different debugging implementations while maintaining a consistent API.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime

from .plugin import IPlugin


class IDebugEvent(ABC):
    """Interface for debug events."""
    
    @property
    @abstractmethod
    def type(self) -> str:
        """Get the type of the debug event."""
        pass
    
    @property
    @abstractmethod
    def timestamp(self) -> str:
        """Get the timestamp of when the event occurred."""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary format."""
        pass


class IBrowserDebugger(IPlugin):
    """Interface for browser debugging capabilities."""
    
    @abstractmethod
    async def start_monitoring(self) -> None:
        """Start monitoring browser events."""
        pass
    
    @abstractmethod
    async def stop_monitoring(self, session_id: str) -> str:
        """Stop monitoring and save debug data."""
        pass
    
    @abstractmethod
    def get_slow_requests(self, threshold: float = 1.0) -> List[Dict[str, Any]]:
        """Get network requests that exceeded threshold."""
        pass
    
    @abstractmethod
    def get_failed_requests(self) -> List[Dict[str, Any]]:
        """Get failed network requests."""
        pass
    
    @abstractmethod
    def get_errors(self) -> List[Dict[str, Any]]:
        """Get console error messages."""
        pass
    
    @abstractmethod
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance metrics summary."""
        pass