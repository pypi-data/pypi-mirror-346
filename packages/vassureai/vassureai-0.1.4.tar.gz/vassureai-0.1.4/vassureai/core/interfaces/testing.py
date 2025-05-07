"""
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
"""

"""
Test execution interfaces for VAssureAI framework.

These interfaces define the contract for test execution components, allowing
for different test execution strategies while maintaining a consistent API.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import asyncio


class ITestStep(ABC):
    """Interface for a test step."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the test step."""
        pass
    
    @property
    @abstractmethod
    def clean_name(self) -> str:
        """Get the clean name (without markers) of the test step."""
        pass
    
    @property
    @abstractmethod
    def status(self) -> str:
        """Get the status of the test step (pending, pass, fail)."""
        pass
    
    @status.setter
    @abstractmethod
    def status(self, value: str) -> None:
        """Set the status of the test step."""
        pass
    
    @property
    @abstractmethod
    def take_screenshot(self) -> bool:
        """Check if screenshot should be taken for this step."""
        pass
    
    @property
    @abstractmethod
    def error(self) -> Optional[str]:
        """Get the error message if the step failed."""
        pass
    
    @error.setter
    @abstractmethod
    def error(self, value: str) -> None:
        """Set the error message."""
        pass


class ITestCase(ABC):
    """Interface for a test case."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the test case."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Get the description of the test case."""
        pass
    
    @property
    @abstractmethod
    def steps(self) -> List[ITestStep]:
        """Get the steps of the test case."""
        pass
    
    @abstractmethod
    async def setup(self) -> None:
        """Set up the test case."""
        pass
    
    @abstractmethod
    async def execute(self) -> bool:
        """Execute the test case."""
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up after the test case."""
        pass
    
    @abstractmethod
    async def take_screenshot(self, step_name: str, step_index: int) -> Optional[str]:
        """Take a screenshot for a specific step."""
        pass


class IBrowserController(ABC):
    """Interface for browser controller."""
    
    @abstractmethod
    async def setup(self, **kwargs) -> None:
        """Set up the browser controller."""
        pass
    
    @abstractmethod
    async def execute_steps(self, steps: List[str]) -> Dict[str, Any]:
        """Execute steps in the browser."""
        pass
    
    @abstractmethod
    async def take_screenshot(self) -> Optional[str]:
        """Take a screenshot of the current browser state."""
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up browser resources."""
        pass


class ITestRunner(ABC):
    """Interface for test runner."""
    
    @abstractmethod
    async def run_test(self, test_case: ITestCase) -> Dict[str, Any]:
        """Run a test case and return results."""
        pass
    
    @abstractmethod
    async def run_tests(self, test_cases: List[ITestCase]) -> List[Dict[str, Any]]:
        """Run multiple test cases and return results."""
        pass