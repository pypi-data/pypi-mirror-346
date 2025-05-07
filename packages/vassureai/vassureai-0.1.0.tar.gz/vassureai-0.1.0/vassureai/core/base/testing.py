"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Base test execution implementation for VAssureAI framework.

Provides the default implementation of test execution interfaces,
supporting test steps, test cases, and browser automation.
"""

import os
import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from ..interfaces.testing import ITestStep, ITestCase, IBrowserController, ITestRunner
from ..interfaces.llm import ILanguageModel
from .config import BaseConfig


class BaseTestStep(ITestStep):
    """Base implementation of a test step."""
    
    def __init__(
        self,
        name: str,
        clean_name: Optional[str] = None,
        take_screenshot: bool = False
    ):
        self._name = name
        self._clean_name = clean_name or name
        self._take_screenshot = take_screenshot
        self._status = "pending"
        self._error = None
    
    @property
    def name(self) -> str:
        """Get the name of the test step."""
        return self._name
    
    @property
    def clean_name(self) -> str:
        """Get the clean name (without markers) of the test step."""
        return self._clean_name
    
    @property
    def status(self) -> str:
        """Get the status of the test step."""
        return self._status
    
    @status.setter
    def status(self, value: str) -> None:
        """Set the status of the test step."""
        if value not in ["pending", "pass", "fail"]:
            raise ValueError(f"Invalid status: {value}")
        self._status = value
    
    @property
    def take_screenshot(self) -> bool:
        """Check if screenshot should be taken for this step."""
        return self._take_screenshot
    
    @property
    def error(self) -> Optional[str]:
        """Get the error message if the step failed."""
        return self._error
    
    @error.setter
    def error(self, value: str) -> None:
        """Set the error message."""
        self._error = value


class BaseTestCase(ITestCase):
    """Base implementation of a test case."""
    
    def __init__(
        self,
        name: str,
        description: str,
        steps: List[Dict[str, Any]],
        config: Optional[BaseConfig] = None,
        llm: Optional[ILanguageModel] = None
    ):
        self._name = name
        self._description = description
        self._config = config or BaseConfig.from_env()
        self._llm = llm
        self._steps = [
            BaseTestStep(
                name=step["name"],
                clean_name=step.get("clean_name"),
                take_screenshot=step.get("take_screenshot", False)
            )
            for step in steps
        ]
        self._controller = None
        self._test_start_time = None
        self._screenshot_dir = self._config.browser.screenshot_dir
        os.makedirs(self._screenshot_dir, exist_ok=True)
    
    @property
    def name(self) -> str:
        """Get the name of the test case."""
        return self._name
    
    @property
    def description(self) -> str:
        """Get the description of the test case."""
        return self._description
    
    @property
    def steps(self) -> List[ITestStep]:
        """Get the steps of the test case."""
        return self._steps
    
    async def setup(self) -> None:
        """Set up the test case."""
        if self._config.browser.record_video:
            os.makedirs(self._config.browser.video_dir, exist_ok=True)
        
        self._test_start_time = datetime.now()
        self._controller = await self._setup_controller()
    
    async def execute(self) -> bool:
        """Execute the test case."""
        if not self._controller:
            raise RuntimeError("Test case not properly initialized. Call setup() first.")
        
        success = True
        for step in self._steps:
            try:
                result = await self._controller.execute_steps([step.clean_name])
                
                if isinstance(result, dict) and not result.get("success", True):
                    step.status = "fail"
                    step.error = str(result.get("error", "Unknown error"))
                    success = False
                else:
                    step.status = "pass"
                
                if step.take_screenshot:
                    await self.take_screenshot(step.name, self._steps.index(step))
                
            except Exception as e:
                step.status = "fail"
                step.error = str(e)
                success = False
                
                if self._config.visual.screenshot_on_error:
                    await self.take_screenshot(f"{step.name}_error", self._steps.index(step))
                
                if not self._config.test.continue_on_failure:
                    break
        
        return success
    
    async def cleanup(self) -> None:
        """Clean up after the test case."""
        if self._controller:
            await self._controller.cleanup()
            self._controller = None
    
    async def take_screenshot(self, step_name: str, step_index: int) -> Optional[str]:
        """Take a screenshot for a specific step."""
        if not self._controller:
            return None
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.name}_{step_index}_{timestamp}.png"
            filepath = os.path.join(self._screenshot_dir, filename)
            
            screenshot = await self._controller.take_screenshot()
            if screenshot:
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "wb") as f:
                    f.write(screenshot)
                return filepath
                
        except Exception as e:
            print(f"Failed to take screenshot for step '{step_name}': {str(e)}")
            
        return None
    
    async def _setup_controller(self) -> IBrowserController:
        """Set up the browser controller."""
        # This should be implemented by specific test case implementations
        # that know which browser controller to use
        raise NotImplementedError("Browser controller setup must be implemented by subclass")