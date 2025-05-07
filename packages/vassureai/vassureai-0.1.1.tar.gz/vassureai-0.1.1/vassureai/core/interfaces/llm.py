"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
LLM interfaces for VAssureAI framework.

These interfaces define the contract for language model components, allowing
for different LLM providers while maintaining a consistent API.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class ILanguageModel(ABC):
    """Interface for language model interactions."""
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the language model."""
        pass
    
    @abstractmethod
    async def generate_with_context(self, prompt: str, context: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response with additional context."""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Get the LLM provider name."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Get the specific model name."""
        pass
    
    @abstractmethod
    def get_token_usage(self) -> Dict[str, int]:
        """Get token usage statistics."""
        pass


class ILLMFactory(ABC):
    """Factory interface for creating language model instances."""
    
    @abstractmethod
    def create_model(self, provider: str, model_name: Optional[str] = None, **kwargs) -> ILanguageModel:
        """Create a language model instance for a specific provider."""
        pass
    
    @abstractmethod
    def get_available_providers(self) -> List[str]:
        """Get a list of available LLM providers."""
        pass