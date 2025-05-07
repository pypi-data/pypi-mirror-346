"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Browser recorder implementation for VAssureAI framework.

Provides functionality to record browser actions, network traffic,
and console logs for advanced debugging and analysis.
"""

import os
import json
import asyncio
from typing import Any, Dict, List, Optional, Set
from datetime import datetime
from playwright.async_api import Page, ConsoleMessage, Request, Response

from ..core.base.config import BaseConfig


class BrowserRecorder:
    """Records browser actions and debug information."""
    
    def __init__(
        self,
        page: Page,
        output_dir: str = "reports/recordings",
        config: Optional[BaseConfig] = None
    ):
        self._page = page
        self._output_dir = output_dir
        self._config = config or BaseConfig.from_env()
        self._recording = False
        self._actions: List[Dict] = []
        self._console_logs: List[Dict] = []
        self._network_logs: List[Dict] = []
        self._seen_requests: Set[str] = set()
        self._start_time: Optional[datetime] = None
        
        os.makedirs(output_dir, exist_ok=True)
    
    async def start_recording(self) -> None:
        """Start recording browser activity."""
        if self._recording:
            return
            
        self._recording = True
        self._start_time = datetime.now()
        self._actions.clear()
        self._console_logs.clear()
        self._network_logs.clear()
        self._seen_requests.clear()
        
        # Set up event listeners
        self._page.on("console", self._handle_console)
        self._page.on("request", self._handle_request)
        self._page.on("response", self._handle_response)
        
        # Start tracing if enabled
        if self._config.debug.trace_browser:
            await self._page.context.tracing.start(
                screenshots=True,
                snapshots=True
            )
    
    async def stop_recording(self, session_id: str) -> str:
        """Stop recording and save results."""
        if not self._recording:
            return ""
            
        self._recording = False
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save browser trace if enabled
        if self._config.debug.trace_browser:
            trace_path = os.path.join(
                self._output_dir,
                f"trace_{session_id}_{timestamp}.zip"
            )
            await self._page.context.tracing.stop(path=trace_path)
        
        # Save recorded data
        data = {
            'session_id': session_id,
            'start_time': self._start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'actions': self._actions,
            'console_logs': self._console_logs,
            'network_logs': self._network_logs
        }
        
        output_path = os.path.join(
            self._output_dir,
            f"recording_{session_id}_{timestamp}.json"
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return output_path
    
    def record_action(
        self,
        action_type: str,
        description: str,
        details: Optional[Dict] = None
    ) -> None:
        """Record a browser action."""
        if not self._recording:
            return
            
        action = {
            'type': action_type,
            'description': description,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        
        self._actions.append(action)
    
    async def take_snapshot(self, name: str) -> Dict[str, str]:
        """Take a snapshot of the current browser state."""
        if not self._recording:
            return {}
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {}
        
        # Take screenshot
        screenshot_path = os.path.join(
            self._output_dir,
            f"snapshot_{name}_{timestamp}.png"
        )
        await self._page.screenshot(path=screenshot_path)
        result['screenshot'] = screenshot_path
        
        # Save page HTML
        html_path = os.path.join(
            self._output_dir,
            f"snapshot_{name}_{timestamp}.html"
        )
        content = await self._page.content()
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        result['html'] = html_path
        
        return result
    
    def _handle_console(self, message: ConsoleMessage) -> None:
        """Handle console messages."""
        if not self._recording:
            return
            
        log = {
            'type': message.type,
            'text': message.text,
            'timestamp': datetime.now().isoformat(),
            'location': {
                'url': message.location.get('url', ''),
                'lineNumber': message.location.get('lineNumber', 0),
                'columnNumber': message.location.get('columnNumber', 0)
            }
        }
        
        self._console_logs.append(log)
    
    def _handle_request(self, request: Request) -> None:
        """Handle network requests."""
        if not self._recording:
            return
            
        # Skip if we've seen this request
        request_id = request.url + str(request.timestamp)
        if request_id in self._seen_requests:
            return
            
        self._seen_requests.add(request_id)
        
        log = {
            'type': 'request',
            'url': request.url,
            'method': request.method,
            'headers': dict(request.headers),
            'timestamp': datetime.now().isoformat(),
            'resourceType': request.resource_type,
            'postData': request.post_data
        }
        
        self._network_logs.append(log)
    
    def _handle_response(self, response: Response) -> None:
        """Handle network responses."""
        if not self._recording:
            return
            
        log = {
            'type': 'response',
            'url': response.url,
            'status': response.status,
            'statusText': response.status_text,
            'headers': dict(response.headers),
            'timestamp': datetime.now().isoformat()
        }
        
        self._network_logs.append(log)
    
    @property
    def actions(self) -> List[Dict]:
        """Get recorded actions."""
        return self._actions.copy()
    
    @property
    def console_logs(self) -> List[Dict]:
        """Get console logs."""
        return self._console_logs.copy()
    
    @property
    def network_logs(self) -> List[Dict]:
        """Get network logs."""
        return self._network_logs.copy()