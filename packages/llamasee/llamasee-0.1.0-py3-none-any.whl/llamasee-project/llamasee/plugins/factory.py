"""
Plugin factory for LlamaSee.

This module provides functionality for creating plugin instances.
"""

import logging
from typing import Dict, List, Type, Optional, Any
from .base import BasePlugin
from .comparison.base import ComparisonPlugin
from .insight.base_insight_plugin import BaseInsightPlugin as InsightPlugin
from .manager import PluginManager

# Import the centralized logger
from ..utils.logger import get_logger

class PluginFactory:
    """
    Factory for LlamaSee plugins.
    """
    
    def __init__(self, plugin_dir: Optional[str] = None, config_dir: Optional[str] = None):
        """
        Initialize the plugin factory.
        
        Args:
            plugin_dir: Optional directory to load plugins from
            config_dir: Optional directory to load configurations from
        """
        self.logger = get_logger(__name__)
        self.manager = PluginManager(plugin_dir, config_dir)
    
    def create_comparison_plugin(self, plugin_name: str, config: Optional[Dict[str, Any]] = None) -> Optional[ComparisonPlugin]:
        """
        Create a comparison plugin instance.
        
        Args:
            plugin_name: The name of the comparison plugin to create
            config: Optional configuration for the plugin
            
        Returns:
            The comparison plugin instance, or None if the plugin could not be created
        """
        # Get the plugin instance
        plugin = self.manager.get_comparison_plugin(plugin_name, config)
        
        if plugin is None:
            self.logger.warning(f"Failed to create comparison plugin: {plugin_name}")
            return None
        
        return plugin
    
    def create_insight_plugin(self, plugin_name: str, config: Optional[Dict[str, Any]] = None) -> Optional[InsightPlugin]:
        """
        Create an insight plugin instance.
        
        Args:
            plugin_name: The name of the insight plugin to create
            config: Optional configuration for the plugin
            
        Returns:
            The insight plugin instance, or None if the plugin could not be created
        """
        # Get the plugin instance
        plugin = self.manager.get_insight_plugin(plugin_name, config)
        
        if plugin is None:
            self.logger.warning(f"Failed to create insight plugin: {plugin_name}")
            return None
        
        return plugin
    
    def create_plugin(self, plugin_name: str, plugin_type: str, config: Optional[Dict[str, Any]] = None) -> Optional[BasePlugin]:
        """
        Create a plugin instance.
        
        Args:
            plugin_name: The name of the plugin to create
            plugin_type: The type of the plugin to create (comparison or insight)
            config: Optional configuration for the plugin
            
        Returns:
            The plugin instance, or None if the plugin could not be created
        """
        if plugin_type == "comparison":
            return self.create_comparison_plugin(plugin_name, config)
        elif plugin_type == "insight":
            return self.create_insight_plugin(plugin_name, config)
        else:
            self.logger.error(f"Unknown plugin type: {plugin_type}")
            return None
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a plugin.
        
        Args:
            plugin_name: The name of the plugin to get information about
            
        Returns:
            Dictionary containing plugin information, or None if the plugin does not exist
        """
        return self.manager.get_plugin_info(plugin_name)
    
    def get_all_plugin_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all registered plugins.
        
        Returns:
            Dictionary mapping plugin names to plugin information
        """
        return self.manager.get_all_plugin_info()
    
    def get_plugin_capabilities(self) -> Dict[str, List[str]]:
        """
        Get the capabilities of all registered plugins.
        
        Returns:
            Dictionary mapping capability types to lists of plugin names
        """
        return self.manager.get_plugin_capabilities()
    
    def discover_plugins(self, directory: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Discover plugins in a directory.
        
        Args:
            directory: Optional directory to discover plugins in
            
        Returns:
            Dictionary mapping plugin types to lists of discovered plugin names
        """
        return self.manager.discover_plugins(directory)
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """
        Reload a plugin.
        
        Args:
            plugin_name: The name of the plugin to reload
            
        Returns:
            True if the plugin was reloaded successfully, False otherwise
        """
        return self.manager.reload_plugin(plugin_name)
    
    def reload_all_plugins(self) -> Dict[str, bool]:
        """
        Reload all plugins.
        
        Returns:
            Dictionary mapping plugin names to reload success status
        """
        return self.manager.reload_all_plugins()
    
    def clear_plugins(self) -> None:
        """Clear all registered plugins."""
        self.manager.clear_plugins() 