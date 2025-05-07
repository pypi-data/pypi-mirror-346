"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Base PDF processor implementation for VAssureAI framework.

Provides the default implementation of PDF processing interfaces,
supporting test case extraction from PDF specifications.
"""

import os
import re
from typing import Any, Dict, List, Optional
import PyPDF2
from ..interfaces.pdf import IPDFParser, ITestCaseExtractor, IPDFTestProcessor


class BasePDFParser(IPDFParser):
    """Base implementation of PDF parser."""
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract all text from a PDF file."""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    
    def extract_test_blocks(self, pdf_path: str) -> List[str]:
        """Extract test case blocks from a PDF file."""
        full_text = self.extract_text(pdf_path)
        # Split text into blocks based on common test case markers
        blocks = []
        current_block = ""
        
        for line in full_text.split('\n'):
            # Detect test case start markers
            if (re.match(r'^Test\s+Case:', line, re.IGNORECASE) or
                re.match(r'^Test\s+ID:', line, re.IGNORECASE) or
                re.match(r'^\d+\.\s+Test\s+Case:', line, re.IGNORECASE)):
                if current_block:
                    blocks.append(current_block.strip())
                current_block = line
            else:
                current_block += "\n" + line
        
        # Add the last block
        if current_block:
            blocks.append(current_block.strip())
        
        return blocks


class BaseTestCaseExtractor(ITestCaseExtractor):
    """Base implementation of test case extractor."""
    
    def extract_test_cases(self, text_blocks: List[str]) -> List[Dict]:
        """Extract structured test cases from text blocks."""
        test_cases = []
        for block in text_blocks:
            test_case = {
                'name': self.extract_test_name(block),
                'description': self.extract_description(block),
                'steps': self.extract_steps(block)
            }
            test_cases.append(test_case)
        return test_cases
    
    def extract_test_name(self, block: str) -> str:
        """Extract test name from a test block."""
        # Try different patterns for test name
        patterns = [
            r'Test Case:\s*(.+?)(?:\n|$)',
            r'Test ID:\s*(.+?)(?:\n|$)',
            r'^\d+\.\s+Test\s+Case:\s*(.+?)(?:\n|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, block, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        return "Unnamed Test"
    
    def extract_description(self, block: str) -> str:
        """Extract test description from a test block."""
        # Look for description section
        patterns = [
            r'Description:\s*(.+?)(?=\n(?:Steps:|Prerequisites:|Test Steps:)|\Z)',
            r'Objective:\s*(.+?)(?=\n(?:Steps:|Prerequisites:|Test Steps:)|\Z)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, block, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def extract_steps(self, block: str) -> List[Dict]:
        """Extract test steps from a test block."""
        steps = []
        
        # Find the steps section
        step_section = re.search(
            r'(?:Steps:|Test Steps:)\s*(.+?)(?=\n(?:Expected|Verification|End)|\Z)',
            block,
            re.IGNORECASE | re.DOTALL
        )
        
        if not step_section:
            return steps
            
        step_text = step_section.group(1)
        
        # Extract individual steps
        step_pattern = r'(?:\d+\.|[-*•])\s*(.+?)(?=(?:\d+\.|[-*•])|\Z)'
        matches = re.finditer(step_pattern, step_text, re.DOTALL)
        
        for match in matches:
            step = match.group(1).strip()
            if step:
                steps.append({
                    'name': step,
                    'take_screenshot': 'screenshot' in step.lower()
                })
        
        return steps


class BasePDFTestProcessor(IPDFTestProcessor):
    """Base implementation of PDF test processor."""
    
    def __init__(
        self,
        parser: Optional[IPDFParser] = None,
        extractor: Optional[ITestCaseExtractor] = None
    ):
        self._parser = parser or BasePDFParser()
        self._extractor = extractor or BaseTestCaseExtractor()
        self._cache = {}
    
    def process_pdf(self, pdf_path: str) -> Dict:
        """Process a PDF file and extract test specifications."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        # Check cache
        pdf_mtime = os.path.getmtime(pdf_path)
        if pdf_path in self._cache:
            cached_time, cached_data = self._cache[pdf_path]
            if cached_time == pdf_mtime:
                return cached_data
        
        # Extract test cases
        blocks = self._parser.extract_test_blocks(pdf_path)
        test_cases = self._extractor.extract_test_cases(blocks)
        
        result = {
            'file_path': pdf_path,
            'last_modified': pdf_mtime,
            'test_cases': test_cases
        }
        
        # Update cache
        self._cache[pdf_path] = (pdf_mtime, result)
        
        return result
    
    def get_test_cases(self, pdf_path: str) -> List[Dict]:
        """Get all test cases from a PDF file."""
        result = self.process_pdf(pdf_path)
        return result['test_cases']
    
    def compare_with_previous(self, pdf_path: str, test_registry: Dict) -> Dict:
        """Compare PDF with previous version to detect changes."""
        current = self.process_pdf(pdf_path)
        current_tests = {tc['name']: tc for tc in current['test_cases']}
        
        if pdf_path not in test_registry:
            return {
                'added': list(current_tests.keys()),
                'modified': [],
                'removed': []
            }
        
        previous = test_registry[pdf_path]
        previous_tests = {tc['name']: tc for tc in previous['test_cases']}
        
        added = set(current_tests.keys()) - set(previous_tests.keys())
        removed = set(previous_tests.keys()) - set(current_tests.keys())
        modified = [
            name for name in set(current_tests.keys()) & set(previous_tests.keys())
            if current_tests[name] != previous_tests[name]
        ]
        
        return {
            'added': list(added),
            'modified': modified,
            'removed': list(removed)
        }