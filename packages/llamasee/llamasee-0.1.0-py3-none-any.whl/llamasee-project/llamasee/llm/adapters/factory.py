"""
Factory for creating LLM adapters.

This module provides a factory class for creating and managing LLM adapters.
"""

from typing import Dict, Any, Type
from .base import BaseLLMAdapter
from .openai_adapter import OpenAIAdapter

class LLMAdapterFactory:
    """
    Factory class for creating LLM adapters.
    
    This class manages the creation and configuration of LLM adapters,
    providing a centralized way to handle different LLM providers.
    """
    
    # Registry of available adapters
    _adapters: Dict[str, Type[BaseLLMAdapter]] = {
        "openai": OpenAIAdapter,
        # Add more adapters here as they are implemented
    }
    
    @classmethod
    def register_adapter(cls, name: str, adapter_class: Type[BaseLLMAdapter]) -> None:
        """
        Register a new adapter class.
        
        Args:
            name: Name of the adapter
            adapter_class: Adapter class to register
        """
        cls._adapters[name.lower()] = adapter_class
    
    @classmethod
    def create_adapter(cls, name: str, config: Dict[str, Any]) -> BaseLLMAdapter:
        """
        Create and initialize an adapter instance.
        
        Args:
            name: Name of the adapter to create
            config: Configuration for the adapter
            
        Returns:
            Initialized adapter instance
            
        Raises:
            ValueError: If adapter name is not registered
            ValueError: If configuration is invalid
        """
        name = name.lower()
        if name not in cls._adapters:
            raise ValueError(f"Unknown adapter: {name}")
        
        adapter_class = cls._adapters[name]
        adapter = adapter_class()
        
        if not adapter.validate_config(config):
            raise ValueError(f"Invalid configuration for adapter: {name}")
        
        adapter.initialize(config)
        return adapter
    
    @classmethod
    def get_available_adapters(cls) -> Dict[str, Type[BaseLLMAdapter]]:
        """
        Get all registered adapters.
        
        Returns:
            Dictionary of adapter names and their classes
        """
        return cls._adapters.copy()
    
    @classmethod
    def is_adapter_available(cls, name: str) -> bool:
        """
        Check if an adapter is available.
        
        Args:
            name: Name of the adapter to check
            
        Returns:
            True if adapter is available
        """
        return name.lower() in cls._adapters 