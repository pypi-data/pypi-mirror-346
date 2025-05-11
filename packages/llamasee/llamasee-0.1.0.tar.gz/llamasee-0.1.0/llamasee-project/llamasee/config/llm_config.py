"""
Configuration for LLM-based insight generation.

This module provides configuration classes for LLM-based insight generation,
including model selection, prompt templates, and generation parameters.
"""

from typing import Dict, Any, List, Optional
import os

class LLMConfig:
    """
    Configuration class for LLM-based insight generation.
    
    This class provides configuration options for LLM-based insight generation,
    including model selection, prompt templates, and generation parameters.
    """
    
    def __init__(self, 
                 model_name: str = "gpt-4",
                 api_key: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: int = 1000,
                 top_p: float = 1.0,
                 frequency_penalty: float = 0.0,
                 presence_penalty: float = 0.0,
                 prompt_template: Optional[str] = None,
                 system_prompt: Optional[str] = None,
                 **kwargs):
        """
        Initialize the LLM configuration.
        
        Args:
            model_name: Name of the LLM model to use
            api_key: API key for the LLM service
            temperature: Temperature for text generation
            max_tokens: Maximum number of tokens to generate
            top_p: Top-p sampling parameter
            frequency_penalty: Frequency penalty parameter
            presence_penalty: Presence penalty parameter
            prompt_template: Template for generating prompts
            system_prompt: System prompt for the LLM
            **kwargs: Additional configuration options
        """
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.prompt_template = prompt_template or self._get_default_prompt_template()
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        
        # Store additional configuration options
        self.options = kwargs
    
    def _get_default_prompt_template(self) -> str:
        """
        Get the default prompt template.
        
        Returns:
            Default prompt template
        """
        return """
        Based on the following data comparison results, generate insights:
        
        {comparison_results}
        
        Scope: {scope}
        
        Context: {context}
        
        Please generate {num_insights} insights, focusing on the most important findings.
        For each insight, provide:
        1. A clear description of the finding
        2. The type of insight (anomaly, trend, difference, etc.)
        3. The scope level (global, dimension, individual)
        4. The importance score (0-10)
        5. The business impact (0-1)
        6. The uniqueness score (0-1)
        7. The magnitude score (0-1)
        8. The frequency score (0-1)
        """
    
    def _get_default_system_prompt(self) -> str:
        """
        Get the default system prompt.
        
        Returns:
            Default system prompt
        """
        return """
        You are an expert data analyst specializing in generating insights from data comparisons.
        Your task is to analyze the provided data and generate meaningful insights that highlight
        important patterns, anomalies, and trends. Focus on actionable insights that provide
        business value.
        """
    
    def get_model_name(self) -> str:
        """
        Get the name of the LLM model.
        
        Returns:
            Model name
        """
        return self.model_name
    
    def get_api_key(self) -> Optional[str]:
        """
        Get the API key for the LLM service.
        
        Returns:
            API key
        """
        return self.api_key
    
    def get_generation_params(self) -> Dict[str, Any]:
        """
        Get the parameters for text generation.
        
        Returns:
            Dictionary of generation parameters
        """
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty
        }
    
    def get_prompt_template(self) -> str:
        """
        Get the prompt template.
        
        Returns:
            Prompt template
        """
        return self.prompt_template
    
    def get_system_prompt(self) -> str:
        """
        Get the system prompt.
        
        Returns:
            System prompt
        """
        return self.system_prompt
    
    def format_prompt(self, comparison_results: str, scope: str, context: str, num_insights: int = 5) -> str:
        """
        Format the prompt with the provided data.
        
        Args:
            comparison_results: Results from data comparison
            scope: Scope information
            context: Additional context
            num_insights: Number of insights to generate
            
        Returns:
            Formatted prompt
        """
        return self.prompt_template.format(
            comparison_results=comparison_results,
            scope=scope,
            context=context,
            num_insights=num_insights
        )
    
    def get_option(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration option.
        
        Args:
            key: The option key
            default: Default value if the option is not set
            
        Returns:
            The option value
        """
        return self.options.get(key, default)

# Default configuration instance
default_config = LLMConfig() 