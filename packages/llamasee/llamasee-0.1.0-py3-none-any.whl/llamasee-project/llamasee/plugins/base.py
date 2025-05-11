"""
Base plugin interfaces for LlamaSee.

This module defines the base interfaces that all LlamaSee plugins must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
import pandas as pd
import logging

class BasePlugin(ABC):
    """
    Base interface for all LlamaSee plugins.
    
    All plugins must implement this interface to ensure
    consistent interaction with the LlamaSee system.
    """
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the plugin with configuration.
        
        Args:
            config: Configuration dictionary for the plugin
        """
        pass
    
    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate the configuration for this plugin.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if configuration is valid
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the plugin.
        
        Returns:
            Plugin name
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Get the description of the plugin.
        
        Returns:
            Plugin description
        """
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """
        Get the version of the plugin.
        
        Returns:
            Plugin version
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get the capabilities of the plugin.
        
        Returns:
            Dictionary of plugin capabilities
        """
        pass 