"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Browser action logger implementation for VAssureAI framework.

Provides detailed logging of browser actions and interactions,
supporting debugging, analysis, and test reporting.
"""

import asyncio
import os
import json
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from ..core.base.config import BaseConfig
from .events import BrowserEvent, EventBus, BrowserEventTypes


@dataclass
class ActionContext:
    """Context information for a browser action."""
    url: str
    selector: Optional[str] = None
    text: Optional[str] = None
    timeout: Optional[float] = None
    options: Optional[Dict[str, Any]] = None


@dataclass
class ActionResult:
    """Result information for a browser action."""
    success: bool
    duration: float
    error: Optional[str] = None
    screenshot: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class ActionLogger:
    """Logger for browser actions and interactions."""
    
    def __init__(
        self,
        output_dir: str = "logs/actions",
        config: Optional[BaseConfig] = None
    ):
        self._output_dir = output_dir
        self._config = config or BaseConfig.from_env()
        self._session_id: Optional[str] = None
        self._actions: List[Dict[str, Any]] = []
        self._event_bus = EventBus()
        
        # Set up logging
        os.makedirs(output_dir, exist_ok=True)
        self._setup_logging()
        
        # Subscribe to browser events
        self._setup_event_handlers()
    
    def _setup_logging(self) -> None:
        """Set up file logging."""
        self._logger = logging.getLogger("action_logger")
        self._logger.setLevel(logging.DEBUG)
        
        # File handler
        log_file = os.path.join(self._output_dir, "actions.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Format
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        
        # Add handler
        self._logger.addHandler(file_handler)
    
    def _setup_event_handlers(self) -> None:
        """Set up browser event handlers."""
        self._event_bus.subscribe(
            BrowserEventTypes.NAVIGATION_START,
            self._handle_navigation_start
        )
        self._event_bus.subscribe(
            BrowserEventTypes.NAVIGATION_COMPLETE,
            self._handle_navigation_complete
        )
        self._event_bus.subscribe(
            BrowserEventTypes.CLICK,
            self._handle_interaction
        )
        self._event_bus.subscribe(
            BrowserEventTypes.TYPE,
            self._handle_interaction
        )
    
    def start_session(self, session_id: str) -> None:
        """Start a new logging session."""
        self._session_id = session_id
        self._actions = []
        self._logger.info(f"Started new session: {session_id}")
    
    def end_session(self) -> None:
        """End the current logging session."""
        if not self._session_id:
            return
            
        # Save session data
        self._save_session_data()
        
        self._logger.info(f"Ended session: {self._session_id}")
        self._session_id = None
        self._actions = []
    
    def _save_session_data(self) -> None:
        """Save session data to file."""
        if not self._session_id:
            return
            
        output_file = os.path.join(
            self._output_dir,
            f"session_{self._session_id}.json"
        )
        
        session_data = {
            'session_id': self._session_id,
            'start_time': self._actions[0]['timestamp']
            if self._actions else datetime.now().isoformat(),
            'end_time': datetime.now().isoformat(),
            'actions': self._actions
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2)
    
    def log_action(
        self,
        action: str,
        description: str,
        context: ActionContext,
        result: ActionResult
    ) -> None:
        """Log a browser action."""
        if not self._session_id:
            return
            
        # Create action entry
        action_data = {
            'action': action,
            'description': description,
            'timestamp': datetime.now().isoformat(),
            'context': asdict(context),
            'result': asdict(result)
        }
        
        # Add to actions list
        self._actions.append(action_data)
        
        # Log to file
        log_level = logging.ERROR if not result.success else logging.INFO
        self._logger.log(
            log_level,
            f"{action}: {description} - "
            f"{'Success' if result.success else f'Error: {result.error}'}"
        )
        
        # Publish event
        asyncio.create_task(
            self._event_bus.publish(
                BrowserEventTypes.CUSTOM_EVENT,
                {
                    'action': action,
                    'data': action_data
                }
            )
        )
    
    def _handle_navigation_start(self, event: BrowserEvent) -> None:
        """Handle navigation start events."""
        if not self._session_id:
            return
            
        self._logger.debug(
            f"Navigation started: {event.data.get('url', 'unknown')}"
        )
    
    def _handle_navigation_complete(self, event: BrowserEvent) -> None:
        """Handle navigation complete events."""
        if not self._session_id:
            return
            
        self._logger.debug(
            f"Navigation completed: {event.data.get('url', 'unknown')}"
        )
    
    def _handle_interaction(self, event: BrowserEvent) -> None:
        """Handle interaction events."""
        if not self._session_id:
            return
            
        self._logger.debug(
            f"Interaction {event.type}: "
            f"{event.data.get('selector', 'unknown')}"
        )
    
    def get_session_actions(
        self,
        session_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get actions for a session."""
        if session_id and session_id != self._session_id:
            # Load from file
            try:
                file_path = os.path.join(
                    self._output_dir,
                    f"session_{session_id}.json"
                )
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data.get('actions', [])
            except Exception:
                return []
        
        return self._actions
    
    def analyze_session(
        self,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze session actions."""
        actions = self.get_session_actions(session_id)
        
        if not actions:
            return {}
            
        # Calculate statistics
        total_actions = len(actions)
        successful_actions = sum(
            1 for action in actions
            if action['result']['success']
        )
        failed_actions = total_actions - successful_actions
        
        # Calculate timing stats
        durations = [
            action['result']['duration']
            for action in actions
        ]
        avg_duration = sum(durations) / len(durations)
        max_duration = max(durations)
        
        # Group by action type
        action_types: Dict[str, int] = {}
        for action in actions:
            action_type = action['action']
            action_types[action_type] = action_types.get(action_type, 0) + 1
        
        return {
            'total_actions': total_actions,
            'successful_actions': successful_actions,
            'failed_actions': failed_actions,
            'success_rate': successful_actions / total_actions,
            'average_duration': avg_duration,
            'max_duration': max_duration,
            'action_types': action_types,
            'start_time': actions[0]['timestamp'],
            'end_time': actions[-1]['timestamp']
        }
    
    def get_failed_actions(
        self,
        session_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get failed actions from a session."""
        actions = self.get_session_actions(session_id)
        return [
            action for action in actions
            if not action['result']['success']
        ]
    
    def get_slow_actions(
        self,
        threshold: float = 1.0,
        session_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get actions that took longer than threshold."""
        actions = self.get_session_actions(session_id)
        return [
            action for action in actions
            if action['result']['duration'] > threshold
        ]