"""
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
"""

"""
Pytest plugin implementation for VAssureAI framework.

Provides pytest integration for collecting and running tests,
supporting both synchronous and asynchronous execution.
"""

import os
import pytest
import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime

from ..core.base.config import BaseConfig
from ..core.base.testing import BaseTestCase
from ..core.base.reporting import BaseTestReport
from ..core.base.metrics import BaseMetricsCollector


def pytest_configure(config):
    """Configure pytest for VAssureAI integration."""
    config.addinivalue_line(
        "markers",
        "vassure: mark test as a VAssureAI test case"
    )


def pytest_collection_modifyitems(session, config, items):
    """Modify test collection to handle VAssureAI test cases."""
    for item in items:
        if isinstance(item.obj, type) and issubclass(item.obj, BaseTestCase):
            item.add_marker(pytest.mark.vassure)
            item.add_marker(pytest.mark.asyncio)


@pytest.fixture(scope="session")
def vassure_config():
    """Provide VAssureAI configuration."""
    return BaseConfig.from_env()


@pytest.fixture(scope="session")
def vassure_report(vassure_config):
    """Provide test report manager."""
    return BaseTestReport(
        output_dir=vassure_config.report_dir
    )


@pytest.fixture(scope="session")
def vassure_metrics(vassure_config):
    """Provide metrics collector."""
    return BaseMetricsCollector(
        metrics_dir=vassure_config.metrics_dir
    )


@pytest.fixture(autouse=True)
def vassure_test_setup(request, vassure_report, vassure_metrics):
    """Set up test environment for each test."""
    test_name = request.node.name
    vassure_metrics.start_test(test_name)
    
    def finalizer():
        result = getattr(request.node, 'vassure_result', {})
        status = 'passed' if result.get('success', False) else 'failed'
        
        vassure_metrics.end_test(test_name, status)
        vassure_report.add_test_case(result)
        
        if result.get('screenshots'):
            for step_name, screenshot in result['screenshots'].items():
                vassure_report.add_screenshot(test_name, step_name, screenshot)
        
        if result.get('errors'):
            for error in result['errors']:
                vassure_report.add_error(test_name, error)
    
    request.addfinalizer(finalizer)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Process test results for reporting."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        if hasattr(item, 'vassure_result'):
            # Transfer VAssureAI test results
            setattr(report, 'vassure_result', item.vassure_result)


def run_vassure_test(test_case: BaseTestCase) -> Dict[str, Any]:
    """Run a VAssureAI test case."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_run_test_async(test_case))


async def _run_test_async(test_case: BaseTestCase) -> Dict[str, Any]:
    """Run a test case asynchronously."""
    start_time = datetime.now()
    
    try:
        await test_case.setup()
        success = await test_case.execute()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        return {
            'name': test_case.name,
            'description': test_case.description,
            'success': success,
            'duration': duration,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'steps': [
                {
                    'name': step.name,
                    'status': step.status,
                    'error': step.error
                }
                for step in test_case.steps
            ]
        }
    
    except Exception as e:
        end_time = datetime.now()
        return {
            'name': test_case.name,
            'success': False,
            'error': str(e),
            'duration': (end_time - start_time).total_seconds()
        }
    
    finally:
        await test_case.cleanup()