"""
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
"""

"""
PDF watcher implementation for VAssureAI framework.

Provides functionality to monitor PDF test specifications for changes
and automatically update test cases.
"""

import os
import json
import asyncio
import logging
import re
from typing import Any, Dict, List, Optional, Set
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from ..core.base.pdf import BasePDFTestProcessor
from ..core.base.config import BaseConfig


logger = logging.getLogger(__name__)


class PDFEventHandler(FileSystemEventHandler):
    """Event handler for PDF file changes."""
    
    def __init__(
        self,
        processor: BasePDFTestProcessor,
        registry_path: str,
        test_dir: str
    ):
        self._processor = processor
        self._registry_path = registry_path
        self._test_dir = test_dir
        self._registry = self._load_registry()
        self._pending_updates: Set[str] = set()
    
    def on_created(self, event):
        """Handle PDF file creation."""
        if not event.is_directory and self._is_pdf(event.src_path):
            logger.info(f"New PDF detected: {event.src_path}")
            self._schedule_update(event.src_path)
    
    def on_modified(self, event):
        """Handle PDF file modification."""
        if not event.is_directory and self._is_pdf(event.src_path):
            logger.info(f"PDF modified: {event.src_path}")
            self._schedule_update(event.src_path)
    
    def on_deleted(self, event):
        """Handle PDF file deletion."""
        if not event.is_directory and self._is_pdf(event.src_path):
            logger.info(f"PDF deleted: {event.src_path}")
            self._remove_from_registry(event.src_path)
    
    def process_pending_updates(self) -> None:
        """Process any pending PDF updates."""
        for pdf_path in list(self._pending_updates):
            try:
                self._process_pdf(pdf_path)
                self._pending_updates.remove(pdf_path)
            except Exception as e:
                logger.error(f"Failed to process {pdf_path}: {str(e)}")
    
    def _is_pdf(self, path: str) -> bool:
        """Check if a file is a PDF."""
        return path.lower().endswith('.pdf')
    
    def _schedule_update(self, pdf_path: str) -> None:
        """Schedule a PDF for processing."""
        self._pending_updates.add(pdf_path)
    
    def _process_pdf(self, pdf_path: str) -> None:
        """Process a PDF file and update test cases."""
        try:
            # Get changes since last version
            changes = self._processor.compare_with_previous(
                pdf_path,
                self._registry.get('pdfs', {})
            )
            
            if not any(changes.values()):
                logger.info(f"No changes detected in {pdf_path}")
                return
            
            # Update test registry
            result = self._processor.process_pdf(pdf_path)
            if 'pdfs' not in self._registry:
                self._registry['pdfs'] = {}
            self._registry['pdfs'][pdf_path] = result
            
            # Generate or update test files
            self._update_test_files(pdf_path, result['test_cases'], changes)
            
            # Save registry
            self._save_registry()
            
            logger.info(
                f"Processed {pdf_path} - Added: {len(changes['added'])}, "
                f"Modified: {len(changes['modified'])}, "
                f"Removed: {len(changes['removed'])}"
            )
            
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {str(e)}")
            raise
    
    def _update_test_files(
        self,
        pdf_path: str,
        test_cases: List[Dict],
        changes: Dict[str, List[str]]
    ) -> None:
        """Update test files based on PDF changes."""
        os.makedirs(self._test_dir, exist_ok=True)
        
        # Create/update test files
        for test_case in test_cases:
            if (test_case['name'] in changes['added'] or
                test_case['name'] in changes['modified']):
                self._create_test_file(test_case)
        
        # Remove deleted test files
        for removed in changes['removed']:
            self._remove_test_file(removed)
    
    def _create_test_file(self, test_case: Dict) -> None:
        """Create or update a test file."""
        test_name = test_case['name']
        safe_name = self._safe_filename(test_name)
        file_path = os.path.join(self._test_dir, f"test_{safe_name}.py")
        
        template = self._get_test_template()
        test_content = template.format(
            test_name=test_name,
            description=test_case['description'],
            steps=self._format_steps(test_case['steps'])
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
    
    def _remove_test_file(self, test_name: str) -> None:
        """Remove a test file."""
        safe_name = self._safe_filename(test_name)
        file_path = os.path.join(self._test_dir, f"test_{safe_name}.py")
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def _safe_filename(self, name: str) -> str:
        """Convert test name to safe filename."""
        return re.sub(r'[^\w\s-]', '', name).strip().lower().replace(' ', '_')
    
    def _get_test_template(self) -> str:
        """Get the test file template."""
        return '''"""
{test_name}

{description}
"""

import pytest
import asyncio
from vassureai.core.base.testing import BaseTestCase
from utils.api_client import get_model_client


class Test{test_name}(BaseTestCase):
    """Test implementation for {test_name}."""
    
    def __init__(self):
        super().__init__(
            name="{test_name}",
            description="""{description}""",
            steps={steps}
        )
        self.model_client = get_model_client()  # Initialize AI model client
        
    async def setup_test(self):
        """Setup test environment."""
        await super().setup_test()
        # Add any test-specific setup here
        
    async def run_step(self, step: dict):
        """Execute a test step with AI assistance if needed."""
        # Use AI model for dynamic verification if specified
        if step.get('use_ai_verification'):
            result = await self.model_client.generate_text(
                f"Verify step: {step['description']}"
            )
            self.log_info(f"AI Verification: {result}")
            
        await super().run_step(step)
        
    async def cleanup_test(self):
        """Cleanup after test execution."""
        await super().cleanup_test()
        # Add any test-specific cleanup here
'''
    
    def _format_steps(self, steps: List[Dict]) -> str:
        """Format steps for test file."""
        formatted_steps = []
        for step in steps:
            formatted_steps.append(
                f'{{"name": "{step["name"]}", '
                f'"take_screenshot": {str(step["take_screenshot"]).lower()}}}'
            )
        return f"[\n        {',\n        '.join(formatted_steps)}\n    ]"
    
    def _load_registry(self) -> Dict:
        """Load the test registry."""
        if os.path.exists(self._registry_path):
            with open(self._registry_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_registry(self) -> None:
        """Save the test registry."""
        with open(self._registry_path, 'w') as f:
            json.dump(self._registry, f, indent=2)
    
    def _remove_from_registry(self, pdf_path: str) -> None:
        """Remove a PDF from the registry."""
        if 'pdfs' in self._registry and pdf_path in self._registry['pdfs']:
            del self._registry['pdfs'][pdf_path]
            self._save_registry()


class PDFWatcher:
    """PDF watcher for monitoring test specifications."""
    
    def __init__(
        self,
        watch_dir: str = "input_pdfs",
        registry_path: str = "input_pdfs/test_registry.json",
        test_dir: str = "tests",
        config: Optional[BaseConfig] = None
    ):
        self._watch_dir = watch_dir
        self._registry_path = registry_path
        self._test_dir = test_dir
        self._config = config or BaseConfig.from_env()
        
        self._processor = BasePDFTestProcessor()
        self._handler = PDFEventHandler(
            processor=self._processor,
            registry_path=registry_path,
            test_dir=test_dir
        )
        self._observer = Observer()
    
    async def start(self, daemon: bool = False) -> None:
        """Start watching for PDF changes."""
        os.makedirs(self._watch_dir, exist_ok=True)
        os.makedirs(self._test_dir, exist_ok=True)
        
        self._observer.schedule(
            self._handler,
            self._watch_dir,
            recursive=False
        )
        self._observer.start()
        
        try:
            logger.info(f"Started watching {self._watch_dir} for PDF changes")
            while True:
                # Process any pending updates
                self._handler.process_pending_updates()
                
                if not daemon and not self._handler._pending_updates:
                    # If not in daemon mode and no pending updates, exit
                    break
                    
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Stopping PDF watcher")
        finally:
            self._observer.stop()
            self._observer.join()