"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Agent wrapper for browser-use integration.

This module provides a clean wrapper around browser-use Agent functionality,
isolating external dependencies for better maintainability.
"""

from typing import Any, Dict, List, Optional, Union
from browser_use.agent.service import Agent as BrowserUseAgent

# Re-export the Agent class with our own wrapper
class Agent(BrowserUseAgent):
    """Wrapper around browser-use Agent class for VAssureAI."""
    
    # The wrapper inherits all functionality from browser-use Agent
    # but can be extended with VAssureAI-specific features
    
    async def execute_step(self, step: str) -> Any:
        """Execute a single test step."""
        self.task = step
        return await self.run()
        
    async def execute_steps(self, steps: List[str]) -> Any:
        """Execute multiple test steps in sequence."""
        self.task = " ".join(steps)
        return await self.run()