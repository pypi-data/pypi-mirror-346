"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Browser factory implementation for VAssureAI framework.

Provides factory methods for creating and managing browser instances,
supporting multiple browser types and configurations.
"""

import os
import asyncio
from typing import Any, Dict, Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

# Import our wrapper instead of directly from browser_use
from .controller import BrowserController

from ..core.base.config import BaseConfig


class BrowserFactory:
    """Factory for creating browser instances."""
    
    def __init__(self, config: Optional[BaseConfig] = None):
        self._config = config or BaseConfig.from_env()
        self._browser_instances: Dict[str, Browser] = {}
        self._context_instances: Dict[str, BrowserContext] = {}
        self._page_instances: Dict[str, Page] = {}
        self._video_index = 0
    
    async def create_browser(
        self,
        browser_type: str = "chromium",
        **kwargs
    ) -> Browser:
        """Create a browser instance."""
        instance_id = f"{browser_type}_{len(self._browser_instances)}"
        
        if instance_id in self._browser_instances:
            return self._browser_instances[instance_id]
        
        async with async_playwright() as playwright:
            browser_class = getattr(playwright, browser_type)
            launch_args = {
                "headless": self._config.browser.headless,
                **kwargs
            }
            
            browser = await browser_class.launch(**launch_args)
            self._browser_instances[instance_id] = browser
            return browser
    
    async def create_context(
        self,
        browser: Browser,
        record_video: Optional[bool] = None,
        **kwargs
    ) -> BrowserContext:
        """Create a browser context."""
        instance_id = f"{id(browser)}_{len(self._context_instances)}"
        
        if instance_id in self._context_instances:
            return self._context_instances[instance_id]
        
        context_args = {}
        
        # Configure video recording
        should_record = (record_video if record_video is not None 
                        else self._config.browser.record_video)
        if should_record:
            video_dir = self._config.browser.video_dir
            os.makedirs(video_dir, exist_ok=True)
            
            self._video_index += 1
            video_path = os.path.join(
                video_dir,
                f"test_run_{self._video_index}.webm"
            )
            
            context_args["record_video_dir"] = video_dir
            context_args["record_video_size"] = {"width": 1280, "height": 720}
        
        # Merge with additional arguments
        context_args.update(kwargs)
        
        context = await browser.new_context(**context_args)
        self._context_instances[instance_id] = context
        return context
    
    async def create_page(
        self,
        context: BrowserContext,
        **kwargs
    ) -> Page:
        """Create a browser page."""
        instance_id = f"{id(context)}_{len(self._page_instances)}"
        
        if instance_id in self._page_instances:
            return self._page_instances[instance_id]
        
        page = await context.new_page()
        self._page_instances[instance_id] = page
        return page
    
    async def create_controller(
        self,
        browser_type: str = "chromium",
        **kwargs
    ) -> BrowserController:
        """Create a browser-use controller."""
        browser = await self.create_browser(browser_type, **kwargs)
        context = await self.create_context(browser)
        page = await self.create_page(context)
        
        controller = BrowserController()
        controller.browser = browser
        controller.context = context
        controller.page = page
        
        return controller
    
    async def cleanup(self) -> None:
        """Clean up all browser resources."""
        # Close pages
        for page in self._page_instances.values():
            try:
                await page.close()
            except:
                pass
        self._page_instances.clear()
        
        # Close contexts
        for context in self._context_instances.values():
            try:
                await context.close()
            except:
                pass
        self._context_instances.clear()
        
        # Close browsers
        for browser in self._browser_instances.values():
            try:
                await browser.close()
            except:
                pass
        self._browser_instances.clear()
    
    async def __aenter__(self):
        """Context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.cleanup()