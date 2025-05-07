"""
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
"""

"""
Plugin system interfaces for VAssureAI framework.

These interfaces define the contract for plugins and extension points,
allowing users to extend framework functionality without modifying core code.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar

T = TypeVar('T')


class IPlugin(ABC):
    """Base interface for all plugins."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the plugin."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Get the version of the plugin."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Get the description of the plugin."""
        pass
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin with configuration."""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up plugin resources."""
        pass


class IPluginManager(ABC):
    """Interface for plugin management."""
    
    @abstractmethod
    def register_plugin(self, plugin: IPlugin) -> None:
        """Register a plugin with the framework."""
        pass
    
    @abstractmethod
    def unregister_plugin(self, plugin_name: str) -> None:
        """Unregister a plugin from the framework."""
        pass
    
    @abstractmethod
    def get_plugin(self, plugin_name: str) -> Optional[IPlugin]:
        """Get a plugin by name."""
        pass
    
    @abstractmethod
    def get_plugins_by_type(self, plugin_type: Type[T]) -> List[T]:
        """Get all plugins of a specific type."""
        pass
    
    @abstractmethod
    def initialize_plugins(self, config: Dict[str, Any]) -> None:
        """Initialize all registered plugins."""
        pass


class ITestHook(IPlugin):
    """Interface for test execution hooks."""
    
    @abstractmethod
    async def before_test(self, test_name: str, context: Dict[str, Any]) -> None:
        """Called before a test starts."""
        pass
    
    @abstractmethod
    async def after_test(self, test_name: str, result: Dict[str, Any]) -> None:
        """Called after a test completes."""
        pass
    
    @abstractmethod
    async def before_step(self, test_name: str, step_name: str) -> None:
        """Called before a test step starts."""
        pass
    
    @abstractmethod
    async def after_step(self, test_name: str, step_name: str, result: Dict[str, Any]) -> None:
        """Called after a test step completes."""
        pass


class IReportPlugin(IPlugin):
    """Interface for report generation plugins."""
    
    @abstractmethod
    def format_report(self, test_results: Dict[str, Any], format_type: str) -> str:
        """Format test results into a report."""
        pass
    
    @abstractmethod
    def export_report(self, formatted_report: str, output_path: str) -> None:
        """Export the formatted report."""
        pass


class ITestGeneratorPlugin(IPlugin):
    """Interface for test generation plugins."""
    
    @abstractmethod
    def generate_test_case(self, specification: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a test case from a specification."""
        pass
    
    @abstractmethod
    def validate_test_case(self, test_case: Dict[str, Any]) -> List[str]:
        """Validate a generated test case and return any errors."""
        pass