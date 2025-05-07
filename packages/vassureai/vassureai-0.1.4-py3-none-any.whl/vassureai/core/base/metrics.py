"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Base metrics implementation for VAssureAI framework.

Provides the default implementation of metrics collection interfaces,
supporting performance tracking and error analysis.
"""

import os
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from ..interfaces.reporting import IMetricsCollector, IErrorAnalyzer


class BaseMetricsCollector(IMetricsCollector):
    """Base implementation of metrics collector."""
    
    def __init__(self, metrics_dir: str = "metrics"):
        self._metrics_dir = metrics_dir
        self._test_metrics = {}
        self._current_test = None
        self._test_start_times = {}
        
        os.makedirs(metrics_dir, exist_ok=True)
        
    def start_test(self, test_name: str) -> None:
        """Start collecting metrics for a test."""
        self._current_test = test_name
        self._test_start_times[test_name] = datetime.now()
        self._test_metrics[test_name] = {
            'name': test_name,
            'status': 'running',
            'start_time': self._test_start_times[test_name].isoformat(),
            'steps': [],
            'errors': [],
            'performance': {
                'total_duration': 0.0,
                'step_durations': {},
                'error_count': 0,
                'browser_metrics': {},
                'network_stats': {}
            }
        }
    
    def end_test(self, test_name: str, status: str) -> None:
        """End collecting metrics for a test."""
        if test_name not in self._test_metrics:
            return
        
        end_time = datetime.now()
        duration = (end_time - self._test_start_times[test_name]).total_seconds()
        
        self._test_metrics[test_name].update({
            'status': status,
            'end_time': end_time.isoformat(),
            'duration': duration
        })
        
        self._test_metrics[test_name]['performance']['total_duration'] = duration
        
        # Save metrics to file
        self._save_metrics(test_name)
        
        if test_name == self._current_test:
            self._current_test = None
    
    def record_step(self, test_name: str, step_name: str, duration: float, status: str) -> None:
        """Record metrics for a test step."""
        if test_name not in self._test_metrics:
            return
            
        step = {
            'name': step_name,
            'status': status,
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        }
        
        self._test_metrics[test_name]['steps'].append(step)
        self._test_metrics[test_name]['performance']['step_durations'][step_name] = duration
    
    def record_error(self, test_name: str, error: Dict[str, Any]) -> None:
        """Record an error occurrence."""
        if test_name not in self._test_metrics:
            return
            
        self._test_metrics[test_name]['errors'].append({
            **error,
            'timestamp': datetime.now().isoformat()
        })
        self._test_metrics[test_name]['performance']['error_count'] += 1
    
    def record_performance_metrics(self, test_name: str, metrics: Dict[str, Any]) -> None:
        """Record performance metrics for a test."""
        if test_name not in self._test_metrics:
            return
            
        # Update browser performance metrics
        if 'latest' in metrics:
            self._test_metrics[test_name]['performance']['browser_metrics'].update(
                metrics['latest']
            )
        
        # Update network statistics
        self._test_metrics[test_name]['performance']['network_stats'].update({
            'total_requests': metrics.get('total_requests', 0),
            'failed_requests': metrics.get('failed_requests', 0),
            'slow_requests': metrics.get('slow_requests', 0)
        })
        
        # Save updated metrics
        self._save_metrics(test_name)
    
    def get_test_metrics(self, test_name: str) -> Dict[str, Any]:
        """Get metrics for a specific test."""
        return self._test_metrics.get(test_name, {})
    
    def get_summary_metrics(self) -> Dict[str, Any]:
        """Get summary metrics for all tests."""
        total_tests = len(self._test_metrics)
        if not total_tests:
            return {}
        
        total_duration = sum(
            m['performance']['total_duration']
            for m in self._test_metrics.values()
        )
        
        total_errors = sum(
            m['performance']['error_count']
            for m in self._test_metrics.values()
        )
        
        status_counts = {}
        for metrics in self._test_metrics.values():
            status = metrics['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            'total_tests': total_tests,
            'status_counts': status_counts,
            'total_duration': total_duration,
            'avg_duration': total_duration / total_tests,
            'error_rate': (total_errors / total_tests) if total_tests > 0 else 0,
            'total_errors': total_errors
        }
    
    def _save_metrics(self, test_name: str) -> None:
        """Save metrics for a test to a file."""
        metrics_file = os.path.join(
            self._metrics_dir,
            f"{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(self._test_metrics[test_name], f, indent=2)


class BaseErrorAnalyzer(IErrorAnalyzer):
    """Base implementation of error analyzer."""
    
    def __init__(self):
        self._error_patterns = {
            'network': {
                'patterns': ['network error', 'connection refused', 'timeout'],
                'type': 'network',
                'severity': 'high',
                'suggestion': 'Check network connectivity and retry'
            },
            'element': {
                'patterns': ['element not found', 'element not visible'],
                'type': 'ui',
                'severity': 'medium',
                'suggestion': 'Verify element selector and timing'
            },
            'assertion': {
                'patterns': ['assertion', 'expected', 'but got'],
                'type': 'validation',
                'severity': 'medium',
                'suggestion': 'Review test expectations'
            }
        }
    
    def analyze_error(self, error_message: str) -> Dict[str, Any]:
        """Analyze an error message and return categorized details."""
        error_message = error_message.lower()
        
        for category, info in self._error_patterns.items():
            if any(pattern in error_message for pattern in info['patterns']):
                return {
                    'type': info['type'],
                    'severity': info['severity'],
                    'suggestion': info['suggestion'],
                    'category': category
                }
        
        return {
            'type': 'unknown',
            'severity': 'low',
            'suggestion': 'Review error details for more information',
            'category': 'other'
        }
    
    def get_error_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Get known error patterns and their solutions."""
        return self._error_patterns
    
    def suggest_fix(self, error_type: str, context: Dict[str, Any]) -> str:
        """Suggest a fix for a given error type."""
        if error_type in self._error_patterns:
            pattern = self._error_patterns[error_type]
            suggestion = pattern['suggestion']
            
            if context:
                # Enhance suggestion with context
                if 'element' in context:
                    suggestion += f"\nElement: {context['element']}"
                if 'location' in context:
                    suggestion += f"\nLocation: {context['location']}"
                if 'timestamp' in context:
                    suggestion += f"\nTimestamp: {context['timestamp']}"
            
            return suggestion
        
        return "No specific fix suggestion available for this error type"