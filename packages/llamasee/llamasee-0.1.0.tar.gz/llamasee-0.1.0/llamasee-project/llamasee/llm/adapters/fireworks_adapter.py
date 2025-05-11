"""
Fireworks AI adapter implementation.

This module provides an adapter for Fireworks AI's API, implementing the BaseLLMAdapter interface.
"""

import os
from typing import Dict, Any, List, Optional
import requests
from .base import BaseLLMAdapter

class FireworksAdapter(BaseLLMAdapter):
    """
    Adapter for Fireworks AI's API.
    
    This adapter implements the BaseLLMAdapter interface for Fireworks AI's API,
    providing a consistent interface for interacting with Fireworks models.
    """
    
    def __init__(self):
        """Initialize the Fireworks adapter."""
        self.api_key = None
        self.default_model = "accounts/fireworks/models/llama-v2-7b-chat"
        self.base_url = "https://api.fireworks.ai/inference/v1"
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the Fireworks adapter with configuration.
        
        Args:
            config: Configuration dictionary containing:
                - api_key: Fireworks API key
                - default_model: Default model to use
                - base_url: Optional base URL for the API
        """
        self.api_key = config.get("api_key") or os.getenv("FIREWORKS_API_KEY")
        if not self.api_key:
            raise ValueError("Fireworks API key is required")
        
        self.default_model = config.get("default_model", self.default_model)
        self.base_url = config.get("base_url", self.base_url)
    
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
        Generate a completion using Fireworks AI's API.
        
        Args:
            prompt: The main prompt for the completion
            system_prompt: Optional system prompt to set context
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            top_p: Controls diversity via nucleus sampling
            frequency_penalty: Reduces repetition of token sequences
            presence_penalty: Reduces repetition of topics
            **kwargs: Additional Fireworks-specific parameters
            
        Returns:
            Generated text completion
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        return self.generate_chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            **kwargs
        )
    
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
        Generate a chat completion using Fireworks AI's API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            top_p: Controls diversity via nucleus sampling
            frequency_penalty: Reduces repetition of token sequences
            presence_penalty: Reduces repetition of topics
            **kwargs: Additional Fireworks-specific parameters
            
        Returns:
            Generated chat completion
        """
        if not self.api_key:
            raise RuntimeError("Fireworks adapter not initialized")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.default_model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            **kwargs
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"Fireworks API error: {response.text}")
        
        return response.json()["choices"][0]["message"]["content"]
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available models from Fireworks.
        
        Returns:
            List of model names/identifiers
        """
        if not self.api_key:
            raise RuntimeError("Fireworks adapter not initialized")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{self.base_url}/models",
            headers=headers
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"Fireworks API error: {response.text}")
        
        return [model["id"] for model in response.json()["data"]]
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get information about a specific Fireworks model.
        
        Args:
            model_name: Name/identifier of the model
            
        Returns:
            Dictionary containing model information
        """
        if not self.api_key:
            raise RuntimeError("Fireworks adapter not initialized")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{self.base_url}/models/{model_name}",
            headers=headers
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"Fireworks API error: {response.text}")
        
        return response.json()["data"]
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate the configuration for Fireworks adapter.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if configuration is valid
        """
        required_fields = ["api_key"]
        return all(field in config for field in required_fields) 