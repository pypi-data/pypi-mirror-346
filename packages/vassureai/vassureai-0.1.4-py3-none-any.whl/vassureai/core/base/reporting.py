"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Base reporting implementation for VAssureAI framework.

Provides the default implementation of reporting interfaces,
supporting HTML, JSON, and console output formats.
"""

import os
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from jinja2 import Environment, FileSystemLoader
from ..interfaces.reporting import ITestReport, IMetricsCollector, IReportFormatter


class BaseReportFormatter(IReportFormatter):
    """Base implementation of report formatter."""
    
    def format_test_case(self, test_case: Dict[str, Any]) -> str:
        """Format a test case result."""
        template = """
Test Case: {name}
Description: {description}
Status: {status}
Duration: {duration:.2f}s
Start Time: {start_time}
End Time: {end_time}

Steps:
{steps}
        """.strip()
        
        steps_text = "\n".join(
            f"  {i+1}. {step['name']} - {step['status']}"
            + (f"\n     Error: {step['error']}" if step.get('error') else "")
            for i, step in enumerate(test_case.get('steps', []))
        )
        
        return template.format(
            name=test_case['name'],
            description=test_case.get('description', 'No description'),
            status='Success' if test_case.get('success', False) else 'Failed',
            duration=test_case.get('duration', 0),
            start_time=test_case.get('start_time', 'Unknown'),
            end_time=test_case.get('end_time', 'Unknown'),
            steps=steps_text or '  No steps recorded'
        )
    
    def format_step_result(self, step_result: Dict[str, Any]) -> str:
        """Format a test step result."""
        template = "{name} - {status}"
        if step_result.get('error'):
            template += " (Error: {error})"
        return template.format(**step_result)
    
    def format_error(self, error: Dict[str, Any]) -> str:
        """Format an error message."""
        template = """
Error Type: {type}
Message: {message}
Timestamp: {timestamp}
Suggestion: {suggestion}
        """.strip()
        
        return template.format(
            type=error.get('type', 'Unknown'),
            message=error.get('message', 'No message'),
            timestamp=error.get('timestamp', datetime.now().isoformat()),
            suggestion=error.get('suggestion', 'No suggestion available')
        )
    
    def format_metrics(self, metrics: Dict[str, Any]) -> str:
        """Format metrics data."""
        template = """
Test Metrics Summary:
Total Tests: {total_tests}
Passed: {passed_tests}
Failed: {failed_tests}
Success Rate: {success_rate:.1f}%
Total Duration: {total_duration:.2f}s
Average Duration: {avg_duration:.2f}s
        """.strip()
        
        return template.format(
            total_tests=metrics.get('total_tests', 0),
            passed_tests=metrics.get('passed_tests', 0),
            failed_tests=metrics.get('failed_tests', 0),
            success_rate=metrics.get('success_rate', 0.0),
            total_duration=metrics.get('total_duration', 0.0),
            avg_duration=metrics.get('avg_duration', 0.0)
        )


class BaseTestReport(ITestReport):
    """Base implementation of test report."""
    
    def __init__(
        self,
        formatter: Optional[IReportFormatter] = None,
        output_dir: str = "reports"
    ):
        self._formatter = formatter or BaseReportFormatter()
        self._output_dir = output_dir
        self._test_cases = {}
        self._screenshots = {}
        self._errors = {}
        
        os.makedirs(output_dir, exist_ok=True)
    
    def add_test_case(self, test_case: Dict[str, Any]) -> None:
        """Add a test case result to the report."""
        self._test_cases[test_case['name']] = test_case
    
    def add_step_result(self, test_name: str, step_result: Dict[str, Any]) -> None:
        """Add a test step result to the report."""
        if test_name not in self._test_cases:
            self._test_cases[test_name] = {'name': test_name, 'steps': []}
        
        if 'steps' not in self._test_cases[test_name]:
            self._test_cases[test_name]['steps'] = []
            
        self._test_cases[test_name]['steps'].append(step_result)
    
    def add_screenshot(self, test_name: str, step_name: str, screenshot_path: str) -> None:
        """Add a screenshot to the report."""
        if test_name not in self._screenshots:
            self._screenshots[test_name] = {}
        self._screenshots[test_name][step_name] = screenshot_path
    
    def add_error(self, test_name: str, error: Dict[str, Any]) -> None:
        """Add an error to the report."""
        if test_name not in self._errors:
            self._errors[test_name] = []
        self._errors[test_name].append(error)
    
    def generate(self, output_path: Optional[str] = None) -> str:
        """Generate the report and return the path to the generated file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_path or os.path.join(
            self._output_dir,
            f"test_report_{timestamp}.html"
        )
        
        # Load and render HTML template
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("report_template.html")
        
        html_content = template.render(
            timestamp=timestamp,
            test_cases=self._test_cases.values(),
            screenshots=self._screenshots,
            errors=self._errors,
            metrics=self._calculate_metrics()
        )
        
        # Write HTML report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def _calculate_metrics(self) -> Dict[str, Any]:
        """Calculate overall metrics for the report."""
        total_tests = len(self._test_cases)
        passed_tests = sum(1 for tc in self._test_cases.values() if tc.get('success', False))
        total_duration = sum(tc.get('duration', 0) for tc in self._test_cases.values())
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'total_duration': total_duration,
            'avg_duration': total_duration / total_tests if total_tests > 0 else 0
        }