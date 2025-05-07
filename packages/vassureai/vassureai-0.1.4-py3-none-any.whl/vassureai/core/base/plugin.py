"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Base plugin system implementation for VAssureAI framework.

Provides the default implementation of plugin interfaces,
supporting dynamic loading and management of framework extensions.
"""

from typing import Any, Dict, List, Optional, Type, TypeVar
from ..interfaces.plugin import (
    IPlugin, IPluginManager, ITestHook, 
    IReportPlugin, ITestGeneratorPlugin
)

T = TypeVar('T', bound=IPlugin)


class BasePluginManager(IPluginManager):
    """Base implementation of plugin manager."""
    
    def __init__(self):
        self._plugins = {}
        self._plugins_by_type = {}
    
    def register_plugin(self, plugin: IPlugin) -> None:
        """Register a plugin with the framework."""
        if plugin.name in self._plugins:
            raise ValueError(f"Plugin {plugin.name} is already registered")
        
        self._plugins[plugin.name] = plugin
        
        # Index plugin by its types
        for base in plugin.__class__.__mro__[:-1]:  # Exclude 'object'
            if base == IPlugin or not issubclass(base, IPlugin):
                continue
                
            if base not in self._plugins_by_type:
                self._plugins_by_type[base] = []
            self._plugins_by_type[base].append(plugin)
    
    def unregister_plugin(self, plugin_name: str) -> None:
        """Unregister a plugin from the framework."""
        if plugin_name not in self._plugins:
            return
            
        plugin = self._plugins[plugin_name]
        
        # Remove from type index
        for base in plugin.__class__.__mro__[:-1]:
            if base == IPlugin or not issubclass(base, IPlugin):
                continue
                
            if base in self._plugins_by_type:
                self._plugins_by_type[base].remove(plugin)
                if not self._plugins_by_type[base]:
                    del self._plugins_by_type[base]
        
        # Remove from main registry
        del self._plugins[plugin_name]
    
    def get_plugin(self, plugin_name: str) -> Optional[IPlugin]:
        """Get a plugin by name."""
        return self._plugins.get(plugin_name)
    
    def get_plugins_by_type(self, plugin_type: Type[T]) -> List[T]:
        """Get all plugins of a specific type."""
        return self._plugins_by_type.get(plugin_type, [])
    
    def initialize_plugins(self, config: Dict[str, Any]) -> None:
        """Initialize all registered plugins."""
        for plugin in self._plugins.values():
            try:
                plugin.initialize(config)
            except Exception as e:
                # Log error but continue with other plugins
                print(f"Failed to initialize plugin {plugin.name}: {str(e)}")


class BasePlugin(IPlugin):
    """Base implementation of plugin interface."""
    
    def __init__(self, name: str, version: str = "1.0.0", description: str = ""):
        self._name = name
        self._version = version
        self._description = description
        self._initialized = False
    
    @property
    def name(self) -> str:
        """Get the name of the plugin."""
        return self._name
    
    @property
    def version(self) -> str:
        """Get the version of the plugin."""
        return self._version
    
    @property
    def description(self) -> str:
        """Get the description of the plugin."""
        return self._description
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin with configuration."""
        self._initialized = True
    
    def cleanup(self) -> None:
        """Clean up plugin resources."""
        self._initialized = False


class BaseTestHook(BasePlugin, ITestHook):
    """Base implementation of test execution hook plugin."""
    
    async def before_test(self, test_name: str, context: Dict[str, Any]) -> None:
        """Called before a test starts."""
        pass
    
    async def after_test(self, test_name: str, result: Dict[str, Any]) -> None:
        """Called after a test completes."""
        pass
    
    async def before_step(self, test_name: str, step_name: str) -> None:
        """Called before a test step starts."""
        pass
    
    async def after_step(self, test_name: str, step_name: str, result: Dict[str, Any]) -> None:
        """Called after a test step completes."""
        pass


class BaseReportPlugin(BasePlugin, IReportPlugin):
    """Base implementation of report generation plugin."""
    
    def format_report(self, test_results: Dict[str, Any], format_type: str) -> str:
        """Format test results into a report."""
        raise NotImplementedError
    
    def export_report(self, formatted_report: str, output_path: str) -> None:
        """Export the formatted report."""
        raise NotImplementedError


class BaseTestGeneratorPlugin(BasePlugin, ITestGeneratorPlugin):
    """Base implementation of test generation plugin."""
    
    def generate_test_case(self, specification: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a test case from a specification."""
        raise NotImplementedError
    
    def validate_test_case(self, test_case: Dict[str, Any]) -> List[str]:
        """Validate a generated test case and return any errors."""
        raise NotImplementedError