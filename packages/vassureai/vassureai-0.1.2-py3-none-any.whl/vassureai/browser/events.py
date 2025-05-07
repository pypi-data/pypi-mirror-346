"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Browser event system implementation for VAssureAI framework.

Provides event handling and communication between browser components.
"""

import asyncio
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass


class BrowserEventTypes(Enum):
    """Browser event types."""
    NAVIGATION_START = auto()
    NAVIGATION_COMPLETE = auto()
    CLICK = auto()
    TYPE = auto()
    CUSTOM_EVENT = auto()
    ERROR = auto()
    WARNING = auto()
    INFO = auto()


@dataclass
class BrowserEvent:
    """Browser event data structure."""
    type: BrowserEventTypes
    data: Dict[str, Any]
    timestamp: float
    source: Optional[str] = None


class EventBus:
    """Event bus for browser event handling."""
    
    def __init__(self):
        self._subscribers: Dict[BrowserEventTypes, List[Callable]] = {}
        self._queue: asyncio.Queue[BrowserEvent] = asyncio.Queue()
        self._running = False
        self._task: Optional[asyncio.Task] = None
    
    def subscribe(
        self,
        event_type: BrowserEventTypes,
        handler: Callable[[BrowserEvent], None]
    ) -> None:
        """Subscribe to an event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
    
    def unsubscribe(
        self,
        event_type: BrowserEventTypes,
        handler: Callable[[BrowserEvent], None]
    ) -> None:
        """Unsubscribe from an event type."""
        if event_type in self._subscribers:
            try:
                self._subscribers[event_type].remove(handler)
            except ValueError:
                pass
    
    async def publish(self, event_type: BrowserEventTypes, data: Dict[str, Any]) -> None:
        """Publish an event."""
        event = BrowserEvent(
            type=event_type,
            data=data,
            timestamp=asyncio.get_event_loop().time()
        )
        await self._queue.put(event)
    
    async def start(self) -> None:
        """Start the event processing loop."""
        if self._running:
            return
            
        self._running = True
        self._task = asyncio.create_task(self._process_events())
    
    async def stop(self) -> None:
        """Stop the event processing loop."""
        if not self._running:
            return
            
        self._running = False
        if self._task:
            await self._task
            self._task = None
    
    async def _process_events(self) -> None:
        """Process events from the queue."""
        while self._running:
            try:
                event = await self._queue.get()
                
                # Process event
                handlers = self._subscribers.get(event.type, [])
                for handler in handlers:
                    try:
                        await asyncio.create_task(handler(event))
                    except Exception as e:
                        # Log error but continue processing
                        print(f"Error in event handler: {e}")
                
                self._queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error processing event: {e}")
                # Continue processing after error
                continue
    
    def get_subscriber_count(self, event_type: BrowserEventTypes) -> int:
        """Get the number of subscribers for an event type."""
        return len(self._subscribers.get(event_type, []))
    
    async def wait_for_event(
        self,
        event_type: BrowserEventTypes,
        timeout: Optional[float] = None
    ) -> Optional[BrowserEvent]:
        """Wait for a specific event type."""
        future: asyncio.Future[Optional[BrowserEvent]] = asyncio.Future()
        
        def handler(event: BrowserEvent) -> None:
            if not future.done():
                future.set_result(event)
        
        self.subscribe(event_type, handler)
        
        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.TimeoutError:
            return None
        finally:
            self.unsubscribe(event_type, handler)
    
    def clear_subscribers(self, event_type: Optional[BrowserEventTypes] = None) -> None:
        """Clear subscribers for an event type or all event types."""
        if event_type:
            self._subscribers[event_type] = []
        else:
            self._subscribers.clear()
    
    async def drain(self) -> None:
        """Wait for all queued events to be processed."""
        await self._queue.join()