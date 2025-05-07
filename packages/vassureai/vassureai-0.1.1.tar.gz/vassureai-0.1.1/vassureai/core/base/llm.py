"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Base LLM implementation for VAssureAI framework.

Provides the default implementation of language model interfaces,
supporting multiple LLM providers through a consistent API.
"""

from typing import Any, Dict, List, Optional, Union
from ..interfaces.llm import ILanguageModel, ILLMFactory
from langchain_core.language_models.llms import BaseLLM
from langchain_core.callbacks import CallbackManager
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


class BaseLLMModel(ILanguageModel):
    """Base implementation of the language model interface."""
    
    def __init__(
        self,
        provider: str,
        model_name: str,
        api_key: str,
        **kwargs
    ):
        self._provider = provider.lower()
        self._model_name = model_name
        self._api_key = api_key
        self._token_usage = {"input_tokens": 0, "output_tokens": 0}
        self._llm = self._initialize_llm(**kwargs)
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the language model."""
        try:
            response = await self._llm.agenerate([prompt])
            self._update_token_usage(response)
            return response.generations[0][0].text
        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")
    
    async def generate_with_context(self, prompt: str, context: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response with additional context."""
        formatted_context = "\n".join(
            f"{item.get('role', 'context')}: {item.get('content')}"
            for item in context
        )
        full_prompt = f"{formatted_context}\n\nUser: {prompt}"
        return await self.generate(full_prompt, **kwargs)
    
    @property
    def provider_name(self) -> str:
        """Get the LLM provider name."""
        return self._provider
    
    @property
    def model_name(self) -> str:
        """Get the specific model name."""
        return self._model_name
    
    def get_token_usage(self) -> Dict[str, int]:
        """Get token usage statistics."""
        return self._token_usage.copy()
    
    def _initialize_llm(self, **kwargs) -> BaseLLM:
        """Initialize the appropriate LLM based on provider."""
        if self._provider == "gemini":
            return ChatGoogleGenerativeAI(
                model=self._model_name,
                google_api_key=self._api_key,
                **kwargs
            )
        elif self._provider == "openai":
            return ChatOpenAI(
                model=self._model_name,
                api_key=self._api_key,
                **kwargs
            )
        elif self._provider == "anthropic":
            return ChatAnthropic(
                model=self._model_name,
                api_key=self._api_key,
                **kwargs
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self._provider}")
    
    def _update_token_usage(self, response: Any) -> None:
        """Update token usage statistics from response."""
        usage = getattr(response, "llm_output", {}).get("token_usage", {})
        self._token_usage["input_tokens"] += usage.get("prompt_tokens", 0)
        self._token_usage["output_tokens"] += usage.get("completion_tokens", 0)


class BaseLLMFactory(ILLMFactory):
    """Base implementation of the LLM factory."""
    
    def __init__(self, default_config: Optional[Dict[str, Any]] = None):
        self._default_config = default_config or {}
        self._providers = {
            "gemini": {
                "class": BaseLLMModel,
                "default_model": "gemini-pro"
            },
            "openai": {
                "class": BaseLLMModel,
                "default_model": "gpt-4"
            },
            "anthropic": {
                "class": BaseLLMModel,
                "default_model": "claude-3-sonnet-20240229"
            }
        }
    
    def create_model(
        self,
        provider: str,
        model_name: Optional[str] = None,
        **kwargs
    ) -> ILanguageModel:
        """Create a language model instance for a specific provider."""
        provider = provider.lower()
        if provider not in self._providers:
            raise ValueError(f"Unsupported provider: {provider}")
        
        provider_info = self._providers[provider]
        config = {**self._default_config, **kwargs}
        
        return provider_info["class"](
            provider=provider,
            model_name=model_name or provider_info["default_model"],
            **config
        )
    
    def get_available_providers(self) -> List[str]:
        """Get a list of available LLM providers."""
        return list(self._providers.keys())