"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Base test runner implementation for VAssureAI framework.

Provides the default implementation of test runner interfaces,
supporting sequential and parallel test execution with resource management.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from concurrent.futures import ThreadPoolExecutor

from ..interfaces.testing import ITestCase, ITestRunner
from ..interfaces.llm import ILanguageModel
from .config import BaseConfig


class BaseTestRunner(ITestRunner):
    """Base implementation of test runner."""
    
    def __init__(
        self,
        config: Optional[BaseConfig] = None,
        max_parallel_tests: int = 4,
        **kwargs
    ):
        self._config = config or BaseConfig.from_env()
        self._max_parallel_tests = max_parallel_tests
        self._kwargs = kwargs
        self._executor = ThreadPoolExecutor(max_workers=max_parallel_tests)
        self._running_tests = set()
    
    async def run_test(self, test_case: ITestCase) -> Dict[str, Any]:
        """Run a test case and return results."""
        start_time = datetime.now()
        
        try:
            # Initialize test
            await test_case.setup()
            self._running_tests.add(test_case.name)
            
            # Execute test
            success = await test_case.execute()
            
            # Collect results
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            results = {
                "name": test_case.name,
                "description": test_case.description,
                "success": success,
                "duration": duration,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "steps": [
                    {
                        "name": step.name,
                        "status": step.status,
                        "error": step.error
                    }
                    for step in test_case.steps
                ]
            }
            
            return results
            
        except Exception as e:
            return {
                "name": test_case.name,
                "success": False,
                "error": str(e),
                "duration": (datetime.now() - start_time).total_seconds()
            }
            
        finally:
            # Clean up
            await test_case.cleanup()
            self._running_tests.remove(test_case.name)
    
    async def run_tests(self, test_cases: List[ITestCase]) -> List[Dict[str, Any]]:
        """Run multiple test cases and return results."""
        if not self._config.test.parallel_execution:
            # Run tests sequentially
            results = []
            for test_case in test_cases:
                result = await self.run_test(test_case)
                results.append(result)
            return results
        
        # Run tests in parallel with resource limits
        async def run_test_with_semaphore(test_case: ITestCase) -> Dict[str, Any]:
            return await self.run_test(test_case)
        
        # Create semaphore to limit concurrent tests
        semaphore = asyncio.Semaphore(self._max_parallel_tests)
        
        async def run_with_semaphore(test_case: ITestCase) -> Dict[str, Any]:
            async with semaphore:
                return await run_test_with_semaphore(test_case)
        
        # Run tests in parallel with semaphore
        tasks = [run_with_semaphore(test_case) for test_case in test_cases]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results and handle any exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append({
                    "success": False,
                    "error": str(result)
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def __aenter__(self):
        """Context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self._executor.shutdown(wait=True)