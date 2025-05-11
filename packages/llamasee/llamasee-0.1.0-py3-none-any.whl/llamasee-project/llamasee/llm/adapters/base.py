"""
Base adapter interface for LLM providers.

This module defines the base interface that all LLM provider adapters must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union

class BaseLLMAdapter(ABC):
    """
    Base adapter interface for LLM providers.
    
    All LLM provider adapters must implement this interface to ensure
    consistent interaction with the LLM service.
    """
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the LLM adapter with configuration.
        
        Args:
            config: Configuration dictionary for the LLM provider
        """
        pass
    
    @abstractmethod
    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        **kwargs
    ) -> str:
        """
        Generate a completion from the LLM.
        
        Args:
            prompt: The main prompt for the completion
            system_prompt: Optional system prompt to set context
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            top_p: Controls diversity via nucleus sampling
            frequency_penalty: Reduces repetition of token sequences
            presence_penalty: Reduces repetition of topics
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated text completion
        """
        pass
    
    @abstractmethod
    def generate_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        **kwargs
    ) -> str:
        """
        Generate a chat completion from the LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            top_p: Controls diversity via nucleus sampling
            frequency_penalty: Reduces repetition of token sequences
            presence_penalty: Reduces repetition of topics
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated chat completion
        """
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """
        Get list of available models from the provider.
        
        Returns:
            List of model names/identifiers
        """
        pass
    
    @abstractmethod
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get information about a specific model.
        
        Args:
            model_name: Name/identifier of the model
            
        Returns:
            Dictionary containing model information
        """
        pass
    
    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate the configuration for this adapter.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if configuration is valid
        """
        pass 