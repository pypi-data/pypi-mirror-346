"""
OpenAI adapter implementation.

This module provides an adapter for OpenAI's API, implementing the BaseLLMAdapter interface.
"""

import os
from typing import Dict, Any, List, Optional
from openai import OpenAI
from .base import BaseLLMAdapter

class OpenAIAdapter(BaseLLMAdapter):
    """
    Adapter for OpenAI's API.
    
    This adapter implements the BaseLLMAdapter interface for OpenAI's API,
    providing a consistent interface for interacting with OpenAI models.
    """
    
    def __init__(self):
        """Initialize the OpenAI adapter."""
        self.client = None
        self.api_key = None
        self.default_model = "gpt-4"
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the OpenAI adapter with configuration.
        
        Args:
            config: Configuration dictionary containing:
                - api_key: OpenAI API key
                - default_model: Default model to use
        """
        self.api_key = config.get("api_key") or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.default_model = config.get("default_model", self.default_model)
        self.client = OpenAI(api_key=self.api_key)
    
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
        Generate a completion using OpenAI's API.
        
        Args:
            prompt: The main prompt for the completion
            system_prompt: Optional system prompt to set context
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            top_p: Controls diversity via nucleus sampling
            frequency_penalty: Reduces repetition of token sequences
            presence_penalty: Reduces repetition of topics
            **kwargs: Additional OpenAI-specific parameters
            
        Returns:
            Generated text completion
        """
        if not self.client:
            raise RuntimeError("OpenAI adapter not initialized")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.default_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            **kwargs
        )
        
        return response.choices[0].message.content
    
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
        Generate a chat completion using OpenAI's API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            top_p: Controls diversity via nucleus sampling
            frequency_penalty: Reduces repetition of token sequences
            presence_penalty: Reduces repetition of topics
            **kwargs: Additional OpenAI-specific parameters
            
        Returns:
            Generated chat completion
        """
        if not self.client:
            raise RuntimeError("OpenAI adapter not initialized")
        
        response = self.client.chat.completions.create(
            model=self.default_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available models from OpenAI.
        
        Returns:
            List of model names/identifiers
        """
        if not self.client:
            raise RuntimeError("OpenAI adapter not initialized")
        
        response = self.client.models.list()
        return [model.id for model in response.data]
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get information about a specific OpenAI model.
        
        Args:
            model_name: Name/identifier of the model
            
        Returns:
            Dictionary containing model information
        """
        if not self.client:
            raise RuntimeError("OpenAI adapter not initialized")
        
        response = self.client.models.retrieve(model_name)
        return {
            "id": response.id,
            "created": response.created,
            "owned_by": response.owned_by,
            "permission": response.permission,
            "root": response.root,
            "parent": response.parent
        }
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate the configuration for OpenAI adapter.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if configuration is valid
        """
        required_fields = ["api_key"]
        return all(field in config for field in required_fields) 