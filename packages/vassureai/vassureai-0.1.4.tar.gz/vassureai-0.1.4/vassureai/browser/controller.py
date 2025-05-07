"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
AI-powered browser controller implementation for VAssureAI framework.

Provides integration with browser-use for intelligent browser automation,
combining LLM capabilities with precise browser control.
"""

import os
import asyncio
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import browser_use
from playwright.async_api import Page
# Fix the import by using the full path to the installed package
from browser_use.controller.service import Controller
from browser_use.agent import prompts
from ..core.base.config import BaseConfig
from ..core.base.llm import BaseLLMModel
from .factory import BrowserFactory
from .recorder import BrowserRecorder
from .logger import ActionLogger, ActionContext, ActionResult

# Create our own wrapper class to isolate browser-use dependency
class BrowserController(browser_use.agent.controller.BrowserController):
    """Wrapper around browser-use BrowserController for VAssureAI."""
    
    # The wrapper inherits all functionality but can be extended with VAssureAI-specific features
    pass

# Main controller class that uses the wrapper
class AIBrowserController:
    """AI-powered browser controller for test automation."""
    
    def __init__(
        self,
        llm: BaseLLMModel,
        config: Optional[BaseConfig] = None,
        session_id: Optional[str] = None
    ):
        self._llm = llm
        self._config = config or BaseConfig.from_env()
        self._session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self._factory = BrowserFactory(config)
        self._controller: Optional[BrowserController] = None
        self._recorder: Optional[BrowserRecorder] = None
        self._logger: Optional[ActionLogger] = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize the browser controller."""
        if self._initialized:
            return
            
        # Create browser controller
        self._controller = await self._factory.create_controller()
        
        # Set up recorder and logger
        self._recorder = BrowserRecorder(
            self._controller.page,
            config=self._config
        )
        self._logger = ActionLogger(config=self._config)
        
        # Start recording and logging
        await self._recorder.start_recording()
        self._logger.start_session(self._session_id)
        
        # Initialize browser-use controller
        await self._setup_browser_use()
        
        self._initialized = True
    
    async def cleanup(self) -> None:
        """Clean up resources."""
        if not self._initialized:
            return
            
        try:
            # Stop recording and save
            if self._recorder:
                await self._recorder.stop_recording(self._session_id)
            
            # End logging session
            if self._logger:
                self._logger.end_session()
            
            # Clean up browser resources
            await self._factory.cleanup()
            
        finally:
            self._initialized = False
    
    async def _setup_browser_use(self) -> None:
        """Set up browser-use controller with custom configuration."""
        if not self._controller:
            return
            
        # Configure browser-use prompts
        custom_prompts = {
            'system': prompts.SYSTEM_PROMPT,
            'human': prompts.HUMAN_PROMPT,
            'error': prompts.ERROR_PROMPT
        }
        
        # Update prompts from config if provided
        if hasattr(self._config.llm, 'prompts'):
            custom_prompts.update(self._config.llm.prompts)
        
        # Set up controller
        self._controller.configure(
            temperature=self._config.llm.temperature,
            max_tokens=self._config.llm.max_tokens,
            custom_prompts=custom_prompts
        )
    
    async def execute_action(
        self,
        action: str,
        description: str,
        **kwargs
    ) -> Tuple[bool, Optional[str]]:
        """Execute an action with logging and analysis."""
        if not self._initialized:
            await self.initialize()
        
        start_time = datetime.now()
        error = None
        success = False
        
        try:
            # Build context
            context = ActionContext(
                url=await self._controller.page.url(),
                **kwargs
            )
            
            # Execute action through browser-use
            result = await self._controller.execute(action)
            success = True
            
        except Exception as e:
            error = str(e)
            result = None
            
        finally:
            duration = (datetime.now() - start_time).total_seconds()
            
            # Take screenshot if configured
            screenshot = None
            if self._config.debug.screenshot_on_action:
                snapshot = await self._recorder.take_snapshot(
                    f"{action}_{self._session_id}"
                )
                screenshot = snapshot.get('screenshot')
            
            # Log action
            if self._logger:
                self._logger.log_action(
                    action=action,
                    description=description,
                    context=context,
                    result=ActionResult(
                        success=success,
                        duration=duration,
                        error=error,
                        screenshot=screenshot,
                        details={'result': result} if result else None
                    )
                )
        
        return success, error
    
    async def navigate(self, url: str) -> Tuple[bool, Optional[str]]:
        """Navigate to a URL."""
        return await self.execute_action(
            f"navigate to {url}",
            f"Navigating to {url}",
            url=url
        )
    
    async def click(
        self,
        selector: str,
        description: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """Click an element."""
        return await self.execute_action(
            f"click {selector}",
            description or f"Clicking element: {selector}",
            selector=selector
        )
    
    async def type(
        self,
        selector: str,
        text: str,
        description: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """Type text into an element."""
        return await self.execute_action(
            f"type {text} into {selector}",
            description or f"Typing '{text}' into {selector}",
            selector=selector,
            text=text
        )
    
    async def wait_for_selector(
        self,
        selector: str,
        description: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """Wait for an element to be visible."""
        return await self.execute_action(
            f"wait for {selector}",
            description or f"Waiting for element: {selector}",
            selector=selector
        )
    
    async def extract_text(
        self,
        selector: str,
        description: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[str]]:
        """Extract text from an element."""
        success, error = await self.execute_action(
            f"extract text from {selector}",
            description or f"Extracting text from {selector}",
            selector=selector
        )
        
        if not success:
            return None, error
            
        try:
            element = await self._controller.page.wait_for_selector(selector)
            text = await element.text_content()
            return text, None
        except Exception as e:
            return None, str(e)
    
    async def take_screenshot(
        self,
        name: str,
        full_page: bool = False
    ) -> Tuple[Optional[str], Optional[str]]:
        """Take a screenshot."""
        try:
            snapshot = await self._recorder.take_snapshot(name)
            return snapshot.get('screenshot'), None
        except Exception as e:
            return None, str(e)
    
    async def evaluate(
        self,
        expression: str,
        description: Optional[str] = None
    ) -> Tuple[Any, Optional[str]]:
        """Evaluate JavaScript expression."""
        success, error = await self.execute_action(
            f"evaluate {expression}",
            description or f"Evaluating JavaScript: {expression}"
        )
        
        if not success:
            return None, error
            
        try:
            result = await self._controller.page.evaluate(expression)
            return result, None
        except Exception as e:
            return None, str(e)
    
    async def get_session_analysis(self) -> Dict[str, Any]:
        """Get analysis of current session."""
        if not self._logger:
            return {}
            
        return self._logger.analyze_session(self._session_id)
    
    @property
    def page(self) -> Optional[Page]:
        """Get the current page object."""
        return self._controller.page if self._controller else None