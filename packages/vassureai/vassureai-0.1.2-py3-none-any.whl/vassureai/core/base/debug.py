"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Base debug implementation for VAssureAI framework.

Provides the default implementation of debugging interfaces,
supporting browser monitoring, network inspection, and performance analysis.
"""

import asyncio
import os
import json
from typing import Any, Dict, List, Optional, Set
from datetime import datetime
from dataclasses import dataclass, asdict
from playwright.async_api import Page, ConsoleMessage, Request, Response

from ..interfaces.debug import IDebugEvent, IBrowserDebugger
from ..interfaces.reporting import IMetricsCollector
from .plugin import BasePlugin
from .config import BaseConfig


@dataclass
class NetworkEvent(IDebugEvent):
    """Network event information."""
    type: str
    url: str
    method: str
    status: Optional[int]
    duration: Optional[float]
    request_headers: Dict[str, str]
    response_headers: Optional[Dict[str, str]]
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary format."""
        return asdict(self)


@dataclass
class ConsoleEvent(IDebugEvent):
    """Console event information."""
    type: str
    text: str
    location: Dict[str, Any]
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary format."""
        return asdict(self)


@dataclass
class PerformanceMetrics(IDebugEvent):
    """Performance metrics information."""
    type: str = "performance"
    metrics: Dict[str, float] = None
    timestamp: str = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary format."""
        return asdict(self)


class BaseBrowserDebugger(BasePlugin, IBrowserDebugger):
    """Base implementation of browser debugging capabilities."""
    
    def __init__(
        self,
        page: Page,
        metrics_collector: Optional[IMetricsCollector] = None,
        output_dir: str = "logs/browser_debug",
        config: Optional[BaseConfig] = None
    ):
        super().__init__(
            name="browser_debugger",
            version="1.0.0",
            description="Browser debugging and monitoring capabilities"
        )
        self._page = page
        self._metrics_collector = metrics_collector
        self._output_dir = output_dir
        self._config = config or BaseConfig.from_env()
        
        self._network_events: List[NetworkEvent] = []
        self._console_events: List[ConsoleEvent] = []
        self._performance_metrics: List[PerformanceMetrics] = []
        self._request_timings: Dict[str, float] = {}
        
        self._monitoring = False
        os.makedirs(output_dir, exist_ok=True)
    
    async def start_monitoring(self) -> None:
        """Start monitoring browser events."""
        if self._monitoring:
            return
            
        self._monitoring = True
        self._clear_events()
        
        # Set up event listeners
        self._page.on("console", self._handle_console)
        self._page.on("request", self._handle_request)
        self._page.on("response", self._handle_response)
        
        # Start performance monitoring
        await self._start_performance_monitoring()
    
    async def stop_monitoring(self, session_id: str) -> str:
        """Stop monitoring and save debug data."""
        if not self._monitoring:
            return ""
            
        self._monitoring = False
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save debug data
        debug_data = {
            'session_id': session_id,
            'timestamp': timestamp,
            'network_events': [e.to_dict() for e in self._network_events],
            'console_events': [e.to_dict() for e in self._console_events],
            'performance_metrics': [e.to_dict() for e in self._performance_metrics]
        }
        
        output_path = os.path.join(
            self._output_dir,
            f"debug_{session_id}_{timestamp}.json"
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(debug_data, f, indent=2)

        # Update metrics if collector is available
        if self._metrics_collector:
            summary = self.get_performance_summary()
            self._metrics_collector.record_performance_metrics(session_id, summary)
        
        return output_path
    
    def get_slow_requests(self, threshold: float = 1.0) -> List[Dict[str, Any]]:
        """Get network requests that exceeded threshold."""
        return [
            e.to_dict() for e in self._network_events
            if e.duration and e.duration > threshold
        ]
    
    def get_failed_requests(self) -> List[Dict[str, Any]]:
        """Get failed network requests."""
        return [
            e.to_dict() for e in self._network_events
            if e.status and e.status >= 400
        ]
    
    def get_errors(self) -> List[Dict[str, Any]]:
        """Get console error messages."""
        return [
            e.to_dict() for e in self._console_events
            if e.type == 'error'
        ]
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance metrics summary."""
        if not self._performance_metrics:
            return {}
            
        # Calculate averages
        metrics_count = len(self._performance_metrics)
        totals: Dict[str, float] = {}
        
        for metric in self._performance_metrics:
            for key, value in metric.metrics.items():
                if isinstance(value, (int, float)):
                    totals[key] = totals.get(key, 0) + value
        
        averages = {
            key: value / metrics_count
            for key, value in totals.items()
        }
        
        # Get latest metrics
        latest = self._performance_metrics[-1].metrics if self._performance_metrics else {}
        
        return {
            'averages': averages,
            'latest': latest,
            'total_requests': len(self._network_events),
            'failed_requests': len(self.get_failed_requests()),
            'slow_requests': len(self.get_slow_requests()),
            'errors': len(self.get_errors())
        }
    
    def _clear_events(self) -> None:
        """Clear stored events."""
        self._network_events.clear()
        self._console_events.clear()
        self._performance_metrics.clear()
        self._request_timings.clear()
    
    def _handle_console(self, message: ConsoleMessage) -> None:
        """Handle console messages."""
        if not self._monitoring:
            return
            
        event = ConsoleEvent(
            type=message.type,
            text=message.text,
            location={
                'url': message.location.get('url', ''),
                'lineNumber': message.location.get('lineNumber', 0),
                'columnNumber': message.location.get('columnNumber', 0)
            },
            timestamp=datetime.now().isoformat()
        )
        
        self._console_events.append(event)
    
    def _handle_request(self, request: Request) -> None:
        """Handle network requests."""
        if not self._monitoring:
            return
            
        self._request_timings[request.url] = datetime.now().timestamp()
    
    def _handle_response(self, response: Response) -> None:
        """Handle network responses."""
        if not self._monitoring:
            return
            
        start_time = self._request_timings.get(response.url)
        duration = None
        
        if start_time:
            duration = datetime.now().timestamp() - start_time
            del self._request_timings[response.url]
        
        event = NetworkEvent(
            type='xhr' if response.request.resource_type == 'xhr' else 'network',
            url=response.url,
            method=response.request.method,
            status=response.status,
            duration=duration,
            request_headers=dict(response.request.headers),
            response_headers=dict(response.headers),
            timestamp=datetime.now().isoformat()
        )
        
        self._network_events.append(event)
    
    async def _start_performance_monitoring(self) -> None:
        """Start monitoring performance metrics."""
        if not self._config.debug.monitor_performance:
            return
            
        async def monitor_metrics():
            while self._monitoring:
                try:
                    # Collect metrics using JavaScript
                    metrics = await self._page.evaluate("""() => {
                        const nav = performance.getEntriesByType('navigation')[0];
                        const paint = performance.getEntriesByType('paint');
                        
                        return {
                            navigationStart: nav ? nav.startTime : 0,
                            responseEnd: nav ? nav.responseEnd : 0,
                            domComplete: nav ? nav.domComplete : 0,
                            loadEventEnd: nav ? nav.loadEventEnd : 0,
                            firstPaint: paint.find(p => p.name === 'first-paint')?.startTime || 0,
                            firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0,
                            memory: performance.memory ? {
                                usedJSHeapSize: performance.memory.usedJSHeapSize,
                                totalJSHeapSize: performance.memory.totalJSHeapSize
                            } : null
                        };
                    }""")
                    
                    self._performance_metrics.append(PerformanceMetrics(
                        metrics=metrics,
                        timestamp=datetime.now().isoformat()
                    ))
                    
                except Exception:
                    pass
                
                await asyncio.sleep(1)
        
        asyncio.create_task(monitor_metrics())