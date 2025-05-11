"""
Plugin interface for LlamaSee.

This module defines the common interface that all plugins must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class PluginInterface(ABC):
    """
    Interface that all LlamaSee plugins must implement.
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
        Validate a configuration for the plugin.
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            True if the configuration is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the plugin.
        
        Returns:
            The plugin name
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Get a description of the plugin.
        
        Returns:
            The plugin description
        """
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """
        Get the version of the plugin.
        
        Returns:
            The plugin version
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
    
    @abstractmethod
    def get_dependencies(self) -> List[str]:
        """
        Get the dependencies required by the plugin.
        
        Returns:
            List of dependency names
        """
        pass
    
    @abstractmethod
    def get_config_schema(self) -> Dict[str, Any]:
        """
        Get the configuration schema for the plugin.
        
        Returns:
            Dictionary describing the configuration schema
        """
        pass
    
    @abstractmethod
    def get_default_config(self) -> Dict[str, Any]:
        """
        Get the default configuration for the plugin.
        
        Returns:
            Dictionary containing default configuration values
        """
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the plugin.
        
        Returns:
            Dictionary containing plugin status information
        """
        pass
    
    @abstractmethod
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get metrics from the plugin.
        
        Returns:
            Dictionary containing plugin metrics
        """
        pass
    
    @abstractmethod
    def get_errors(self) -> List[Dict[str, Any]]:
        """
        Get any errors from the plugin.
        
        Returns:
            List of error dictionaries
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up any resources used by the plugin."""
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """Reset the plugin to its initial state."""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """
        Validate that the plugin is in a valid state.
        
        Returns:
            True if the plugin is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def is_enabled(self) -> bool:
        """
        Check if the plugin is enabled.
        
        Returns:
            True if the plugin is enabled, False otherwise
        """
        pass
    
    @abstractmethod
    def enable(self) -> None:
        """Enable the plugin."""
        pass
    
    @abstractmethod
    def disable(self) -> None:
        """Disable the plugin."""
        pass
    
    @abstractmethod
    def reload(self) -> bool:
        """
        Reload the plugin.
        
        Returns:
            True if the plugin was reloaded successfully, False otherwise
        """
        pass 