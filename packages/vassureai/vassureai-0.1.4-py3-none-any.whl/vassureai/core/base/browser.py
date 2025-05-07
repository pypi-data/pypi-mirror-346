"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Base browser automation implementation for VAssureAI framework.

Provides the default implementation of browser controller interfaces,
supporting browser-use and AI-powered browser automation.
"""

import asyncio
from typing import Any, Dict, List, Optional
# Import browser-use through wrapper modules instead of directly
from ...browser.agent import Agent
from ...browser.controller import BrowserController

from ..interfaces.testing import IBrowserController
from ..interfaces.llm import ILanguageModel
from .config import BaseConfig


class BaseBrowserController(IBrowserController):
    """Base implementation of browser controller using browser-use."""
    
    def __init__(
        self,
        llm: ILanguageModel,
        config: Optional[BaseConfig] = None,
        **kwargs
    ):
        self._llm = llm
        self._config = config or BaseConfig.from_env()
        self._agent = None
        self._controller = None
        self._kwargs = kwargs
    
    async def setup(self, **kwargs) -> None:
        """Set up the browser controller."""
        merged_kwargs = {**self._kwargs, **kwargs}
        
        # Create browser-use agent
        self._agent = Agent(
            task="",  # Will be set during execution
            llm=self._llm,
            max_failures=self._config.retry.max_retries,
            retry_delay=self._config.retry.retry_delay,
            use_vision=self._config.visual.highlight,
            **merged_kwargs
        )
        
        # Set up browser controller
        self._controller = BrowserController(
            headless=self._config.browser.headless,
            **merged_kwargs
        )
        self._agent.controller = self._controller
    
    async def execute_steps(self, steps: List[str]) -> Dict[str, Any]:
        """Execute steps in the browser."""
        if not self._agent or not self._controller:
            raise RuntimeError("Browser controller not initialized. Call setup() first.")
        
        # Join steps into a single task for the agent
        self._agent.task = " ".join(steps)
        
        try:
            result = await self._agent.run()
            return self._process_result(result)
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def take_screenshot(self) -> Optional[bytes]:
        """Take a screenshot of the current browser state."""
        if not self._controller or not hasattr(self._controller, "page"):
            return None
            
        try:
            return await self._controller.page.screenshot()
        except Exception:
            return None
    
    async def cleanup(self) -> None:
        """Clean up browser resources."""
        if self._controller:
            try:
                if hasattr(self._controller, "page"):
                    await self._controller.page.close()
                if hasattr(self._controller, "browser"):
                    await self._controller.browser.close()
            except Exception:
                pass  # Ensure cleanup continues even if there are errors
            
            self._controller = None
            self._agent = None
    
    def _process_result(self, result: Any) -> Dict[str, Any]:
        """Process the result from browser-use agent."""
        if result is None:
            return {"success": False, "error": "No result from agent"}
            
        if isinstance(result, dict):
            return result
            
        if isinstance(result, bool):
            return {"success": result}
            
        if isinstance(result, str):
            return {
                "success": "error" not in result.lower() and "failed" not in result.lower(),
                "message": result
            }
            
        return {"success": True, "result": str(result)}