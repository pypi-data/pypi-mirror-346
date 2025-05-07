"""
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
"""

"""
Reporting interfaces for VAssureAI framework.

These interfaces define the contract for reporting components, allowing
for different reporting formats and methods while maintaining a consistent API.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


class ITestReport(ABC):
    """Interface for test execution reports."""
    
    @abstractmethod
    def add_test_case(self, test_case: Dict[str, Any]) -> None:
        """Add a test case result to the report."""
        pass
    
    @abstractmethod
    def add_step_result(self, test_name: str, step_result: Dict[str, Any]) -> None:
        """Add a test step result to the report."""
        pass
    
    @abstractmethod
    def add_screenshot(self, test_name: str, step_name: str, screenshot_path: str) -> None:
        """Add a screenshot to the report."""
        pass
    
    @abstractmethod
    def add_error(self, test_name: str, error: Dict[str, Any]) -> None:
        """Add an error to the report."""
        pass
    
    @abstractmethod
    def generate(self, output_path: Optional[str] = None) -> str:
        """Generate the report and return the path to the generated file."""
        pass


class IMetricsCollector(ABC):
    """Interface for collecting test execution metrics."""
    
    @abstractmethod
    def start_test(self, test_name: str) -> None:
        """Start collecting metrics for a test."""
        pass
    
    @abstractmethod
    def end_test(self, test_name: str, status: str) -> None:
        """End collecting metrics for a test."""
        pass
    
    @abstractmethod
    def record_step(self, test_name: str, step_name: str, duration: float, status: str) -> None:
        """Record metrics for a test step."""
        pass
    
    @abstractmethod
    def record_error(self, test_name: str, error: Dict[str, Any]) -> None:
        """Record an error occurrence."""
        pass
    
    @abstractmethod
    def record_performance_metrics(self, test_name: str, metrics: Dict[str, Any]) -> None:
        """Record performance metrics for a test."""
        pass
    
    @abstractmethod
    def get_test_metrics(self, test_name: str) -> Dict[str, Any]:
        """Get metrics for a specific test."""
        pass
    
    @abstractmethod
    def get_summary_metrics(self) -> Dict[str, Any]:
        """Get summary metrics for all tests."""
        pass


class IErrorAnalyzer(ABC):
    """Interface for analyzing and categorizing test errors."""
    
    @abstractmethod
    def analyze_error(self, error_message: str) -> Dict[str, Any]:
        """Analyze an error message and return categorized details."""
        pass
    
    @abstractmethod
    def get_error_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Get known error patterns and their solutions."""
        pass
    
    @abstractmethod
    def suggest_fix(self, error_type: str, context: Dict[str, Any]) -> str:
        """Suggest a fix for a given error type."""
        pass


class IReportFormatter(ABC):
    """Interface for formatting test reports in different output formats."""
    
    @abstractmethod
    def format_test_case(self, test_case: Dict[str, Any]) -> str:
        """Format a test case result."""
        pass
    
    @abstractmethod
    def format_step_result(self, step_result: Dict[str, Any]) -> str:
        """Format a test step result."""
        pass
    
    @abstractmethod
    def format_error(self, error: Dict[str, Any]) -> str:
        """Format an error message."""
        pass
    
    @abstractmethod
    def format_metrics(self, metrics: Dict[str, Any]) -> str:
        """Format metrics data."""
        pass