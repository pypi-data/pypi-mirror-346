"""
PDF processor interfaces for VAssureAI framework.

These interfaces define the contract for PDF processing components, allowing
for different PDF extraction methods while maintaining a consistent API.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union


class IPDFParser(ABC):
    """Interface for parsing PDF files."""
    
    @abstractmethod
    def extract_text(self, pdf_path: str) -> str:
        """Extract all text from a PDF file."""
        pass
    
    @abstractmethod
    def extract_test_blocks(self, pdf_path: str) -> List[str]:
        """Extract test case blocks from a PDF file."""
        pass


class ITestCaseExtractor(ABC):
    """Interface for extracting test cases from text blocks."""
    
    @abstractmethod
    def extract_test_cases(self, text_blocks: List[str]) -> List[Dict]:
        """Extract structured test cases from text blocks."""
        pass
    
    @abstractmethod
    def extract_test_name(self, block: str) -> str:
        """Extract test name from a test block."""
        pass
    
    @abstractmethod
    def extract_description(self, block: str) -> str:
        """Extract test description from a test block."""
        pass
    
    @abstractmethod
    def extract_steps(self, block: str) -> List[Dict]:
        """Extract test steps from a test block."""
        pass


class IPDFTestProcessor(ABC):
    """Interface for processing PDF test specifications."""
    
    @abstractmethod
    def process_pdf(self, pdf_path: str) -> Dict:
        """Process a PDF file and extract test specifications."""
        pass
    
    @abstractmethod
    def get_test_cases(self, pdf_path: str) -> List[Dict]:
        """Get all test cases from a PDF file."""
        pass
    
    @abstractmethod
    def compare_with_previous(self, pdf_path: str, test_registry: Dict) -> Dict:
        """Compare PDF with previous version to detect changes."""
        pass