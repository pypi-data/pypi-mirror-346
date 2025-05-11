"""
Plugin registry for LlamaSee.

This module provides functionality for registering and managing plugins.
"""

import os
import logging
import importlib
import inspect
from typing import Dict, List, Type, Optional, Any, Set
from .base import BasePlugin
from .comparison.base import ComparisonPlugin
from .insight.base_insight_plugin import BaseInsightPlugin as InsightPlugin
from .loader import PluginLoader
from .config_manager import PluginConfigManager

# Import the centralized logger
from ..utils.logger import get_logger

class PluginRegistry:
    """
    Registry for LlamaSee plugins.
    """
    
    def __init__(self, plugin_dir: Optional[str] = None, config_dir: Optional[str] = None):
        """
        Initialize the plugin registry.
        
        Args:
            plugin_dir: Optional directory to load plugins from
            config_dir: Optional directory to load configurations from
        """
        self.logger = get_logger(__name__)
        self.plugin_dir = plugin_dir or os.path.join(os.path.dirname(__file__))
        self.config_dir = config_dir or os.path.join(os.path.dirname(__file__), "config")
        
        # Initialize the plugin components
        self.loader = PluginLoader(self.plugin_dir)
        self.config_manager = PluginConfigManager(self.config_dir)
        
        # Register plugins
        self.comparison_plugins: Dict[str, Type[ComparisonPlugin]] = {}
        self.insight_plugins: Dict[str, Type[InsightPlugin]] = {}
        self.comparison_plugin_info: Dict[str, Dict[str, Any]] = {}
        self.insight_plugin_info: Dict[str, Dict[str, Any]] = {}
        
        # Initialize plugin capabilities
        self.plugin_capabilities: Dict[str, Set[str]] = {
            "comparison": set(),
            "insight": set()
        }
        
        # Discover and register plugins
        self.discover_plugins()
    
    def discover_plugins(self, directory: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Discover plugins in a directory.
        
        Args:
            directory: Optional directory to discover plugins in
            
        Returns:
            Dictionary mapping plugin types to lists of discovered plugin names
        """
        directory = directory or self.plugin_dir
        self.logger.info(f"Discovering plugins in {directory}")
        
        # Discover comparison plugins
        comparison_plugins = self.loader.discover_comparison_plugins(directory)
        for plugin_name, plugin_class in comparison_plugins.items():
            self.register_comparison_plugin(plugin_name, plugin_class)
        
        # Discover insight plugins
        insight_plugins = self.loader.discover_insight_plugins(directory)
        for plugin_name, plugin_class in insight_plugins.items():
            self.register_insight_plugin(plugin_name, plugin_class)
        
        return {
            "comparison": list(comparison_plugins.keys()),
            "insight": list(insight_plugins.keys())
        }
    
    def register_comparison_plugin(self, plugin_name: str, plugin_class: Type[ComparisonPlugin]) -> None:
        """
        Register a comparison plugin.
        
        Args:
            plugin_name: The name of the comparison plugin
            plugin_class: The comparison plugin class
        """
        self.logger.info(f"Registering comparison plugin: {plugin_name}")
        
        # Check if the class is abstract
        is_abstract = False
        try:
            # Try to get the abstract methods
            abstract_methods = getattr(plugin_class, '__abstractmethods__', set())
            is_abstract = len(abstract_methods) > 0
            if is_abstract:
                self.logger.info(f"Plugin class {plugin_name} is abstract with abstract methods: {abstract_methods}")
                # For abstract classes, we'll still register them but mark them as abstract
                self.comparison_plugins[plugin_name] = plugin_class
                self.plugin_capabilities["comparison"].add(plugin_name)
                
                # Get basic plugin info
                plugin_info = self._get_plugin_info(plugin_class)
                self.comparison_plugin_info[plugin_name] = plugin_info
                
                self.logger.info(f"Successfully registered abstract comparison plugin {plugin_name}")
                return
        except Exception as e:
            self.logger.warning(f"Error checking if {plugin_name} is abstract: {str(e)}")
        
        # For non-abstract classes, check if the plugin has the required methods and attributes
        required_methods = ["compare", "get_comparison_types", "get_comparison_metrics", 
                           "get_supported_data_types", "get_supported_dimensions", "get_supported_aggregations"]
        missing_methods = [method for method in required_methods if not hasattr(plugin_class, method)]
        
        if missing_methods:
            self.logger.warning(f"Comparison plugin {plugin_name} missing required methods: {missing_methods}")
            return
        
        # Register the plugin
        self.comparison_plugins[plugin_name] = plugin_class
        self.plugin_capabilities["comparison"].add(plugin_name)
        
        # Get plugin info
        plugin_info = self._get_plugin_info(plugin_class)
        self.comparison_plugin_info[plugin_name] = plugin_info
        
        self.logger.info(f"Successfully registered comparison plugin {plugin_name}")
    
    def register_insight_plugin(self, plugin_name: str, plugin_class: Type[InsightPlugin]) -> None:
        """
        Register an insight plugin.
        
        Args:
            plugin_name: The name of the insight plugin
            plugin_class: The insight plugin class
        """
        self.logger.info(f"Registering insight plugin: {plugin_name}")
        
        # Check if the class is abstract
        is_abstract = False
        try:
            # Try to get the abstract methods
            abstract_methods = getattr(plugin_class, '__abstractmethods__', set())
            is_abstract = len(abstract_methods) > 0
            if is_abstract:
                self.logger.info(f"Plugin class {plugin_name} is abstract with abstract methods: {abstract_methods}")
                # For abstract classes, we'll still register them but mark them as abstract
                self.insight_plugins[plugin_name] = plugin_class
                self.plugin_capabilities["insight"].add(plugin_name)
                
                # Get basic plugin info
                plugin_info = self._get_plugin_info(plugin_class)
                self.insight_plugin_info[plugin_name] = plugin_info
                
                self.logger.info(f"Successfully registered abstract insight plugin {plugin_name}")
                return
        except Exception as e:
            self.logger.warning(f"Error checking if {plugin_name} is abstract: {str(e)}")
        
        # For non-abstract classes, check if the plugin has the required methods and attributes
        required_methods = ["generate_insights", "can_handle"]
        missing_methods = [method for method in required_methods if not hasattr(plugin_class, method)]
        
        if missing_methods:
            self.logger.warning(f"Insight plugin {plugin_name} missing required methods: {missing_methods}")
            return
        
        # Register the plugin
        self.insight_plugins[plugin_name] = plugin_class
        self.plugin_capabilities["insight"].add(plugin_name)
        
        # Get plugin info
        plugin_info = self._get_plugin_info(plugin_class)
        self.insight_plugin_info[plugin_name] = plugin_info
        
        self.logger.info(f"Successfully registered insight plugin {plugin_name}")
    
    def get_comparison_plugin(self, plugin_name: str, config: Optional[Dict[str, Any]] = None) -> Optional[ComparisonPlugin]:
        """
        Get a comparison plugin instance.
        
        Args:
            plugin_name: The name of the comparison plugin to get
            config: Optional configuration for the plugin
            
        Returns:
            The comparison plugin instance, or None if the plugin does not exist
        """
        if plugin_name not in self.comparison_plugins:
            self.logger.warning(f"Comparison plugin {plugin_name} not found")
            return None
        
        try:
            plugin_class = self.comparison_plugins[plugin_name]
            plugin_instance = plugin_class()
            if config:
                plugin_instance.configure(config)
            return plugin_instance
        except Exception as e:
            self.logger.error(f"Error creating comparison plugin {plugin_name}: {str(e)}")
            return None
    
    def get_insight_plugin(self, plugin_name: str, config: Optional[Dict[str, Any]] = None) -> Optional[InsightPlugin]:
        """
        Get an insight plugin instance.
        
        Args:
            plugin_name: The name of the insight plugin to get
            config: Optional configuration for the plugin
            
        Returns:
            The insight plugin instance, or None if the plugin does not exist
        """
        if plugin_name not in self.insight_plugins:
            self.logger.warning(f"Insight plugin {plugin_name} not found")
            return None
        
        try:
            plugin_class = self.insight_plugins[plugin_name]
            plugin_instance = plugin_class()
            if config:
                plugin_instance.configure(config)
            return plugin_instance
        except Exception as e:
            self.logger.error(f"Error creating insight plugin {plugin_name}: {str(e)}")
            return None
    
    def get_all_comparison_plugins(self) -> Dict[str, Type[ComparisonPlugin]]:
        """
        Get all registered comparison plugins.
        
        Returns:
            Dictionary mapping plugin names to plugin classes
        """
        return self.comparison_plugins
    
    def get_all_insight_plugins(self) -> Dict[str, Type[InsightPlugin]]:
        """
        Get all registered insight plugins.
        
        Returns:
            Dictionary mapping plugin names to plugin classes
        """
        return self.insight_plugins
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a plugin.
        
        Args:
            plugin_name: The name of the plugin to get information about
            
        Returns:
            Dictionary containing plugin information, or None if the plugin does not exist
        """
        if plugin_name in self.comparison_plugin_info:
            return self.comparison_plugin_info[plugin_name]
        elif plugin_name in self.insight_plugin_info:
            return self.insight_plugin_info[plugin_name]
        else:
            self.logger.warning(f"Plugin {plugin_name} not found")
            return None
    
    def get_all_plugin_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all registered plugins.
        
        Returns:
            Dictionary mapping plugin names to plugin information
        """
        all_plugin_info = {}
        all_plugin_info.update(self.comparison_plugin_info)
        all_plugin_info.update(self.insight_plugin_info)
        return all_plugin_info
    
    def get_plugin_capabilities(self) -> Dict[str, Set[str]]:
        """
        Get the capabilities of all registered plugins.
        
        Returns:
            Dictionary mapping capability types to sets of plugin names
        """
        return self.plugin_capabilities
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """
        Reload a plugin.
        
        Args:
            plugin_name: The name of the plugin to reload
            
        Returns:
            True if the plugin was reloaded successfully, False otherwise
        """
        self.logger.info(f"Reloading plugin: {plugin_name}")
        
        if plugin_name in self.comparison_plugins:
            try:
                module = importlib.import_module(f".comparison.{plugin_name}", package="llamasee.plugins")
                importlib.reload(module)
                plugin_class = getattr(module, plugin_name.capitalize())
                self.register_comparison_plugin(plugin_name, plugin_class)
                return True
            except Exception as e:
                self.logger.error(f"Error reloading comparison plugin {plugin_name}: {str(e)}")
                return False
        elif plugin_name in self.insight_plugins:
            try:
                module = importlib.import_module(f".insight.{plugin_name}", package="llamasee.plugins")
                importlib.reload(module)
                plugin_class = getattr(module, plugin_name.capitalize())
                self.register_insight_plugin(plugin_name, plugin_class)
                return True
            except Exception as e:
                self.logger.error(f"Error reloading insight plugin {plugin_name}: {str(e)}")
                return False
        else:
            self.logger.warning(f"Plugin {plugin_name} not found")
            return False
    
    def reload_all_plugins(self) -> Dict[str, bool]:
        """
        Reload all plugins.
        
        Returns:
            Dictionary mapping plugin names to reload success status
        """
        self.logger.info("Reloading all plugins")
        
        reload_results = {}
        
        # Reload comparison plugins
        for plugin_name in self.comparison_plugins:
            reload_results[plugin_name] = self.reload_plugin(plugin_name)
        
        # Reload insight plugins
        for plugin_name in self.insight_plugins:
            reload_results[plugin_name] = self.reload_plugin(plugin_name)
        
        self.logger.info(f"Plugin reload complete. Results: {reload_results}")
        return reload_results
    
    def clear_plugins(self) -> None:
        """Clear all registered plugins."""
        self.logger.info("Clearing all plugins")
        
        self.comparison_plugins.clear()
        self.insight_plugins.clear()
        self.comparison_plugin_info.clear()
        self.insight_plugin_info.clear()
        self.plugin_capabilities["comparison"].clear()
        self.plugin_capabilities["insight"].clear()
        
        self.logger.info("All plugins cleared")
    
    def _get_plugin_info(self, plugin_class: Type[BasePlugin]) -> Dict[str, Any]:
        """
        Get information about a plugin.
        
        Args:
            plugin_class: The plugin class to get information about
            
        Returns:
            Dictionary containing plugin information
        """
        self.logger.info(f"Getting plugin info for {plugin_class.__name__}")
        
        # Check if the class is abstract
        is_abstract = False
        try:
            # Try to get the abstract methods
            abstract_methods = getattr(plugin_class, '__abstractmethods__', set())
            is_abstract = len(abstract_methods) > 0
            if is_abstract:
                self.logger.info(f"Plugin class {plugin_class.__name__} is abstract with abstract methods: {abstract_methods}")
        except Exception as e:
            self.logger.warning(f"Error checking if {plugin_class.__name__} is abstract: {str(e)}")
        
        # Basic plugin info that doesn't require instantiation
        plugin_info = {
            "name": getattr(plugin_class, "name", plugin_class.__name__),
            "description": getattr(plugin_class, "description", ""),
            "version": getattr(plugin_class, "version", "0.0.0"),
            "capabilities": getattr(plugin_class, "capabilities", []),
            "characteristics": getattr(plugin_class, "characteristics", {}),
            "is_abstract": is_abstract
        }
        
        # If the class is abstract, return just the basic info
        if is_abstract:
            self.logger.info(f"Returning basic info for abstract plugin class {plugin_class.__name__}")
            return plugin_info
        
        try:
            # Create an instance of the plugin class to call instance methods
            plugin_instance = plugin_class()
            
            if issubclass(plugin_class, ComparisonPlugin):
                plugin_info.update({
                    "comparison_types": plugin_instance.get_comparison_types(),
                    "comparison_metrics": plugin_instance.get_comparison_metrics(),
                    "supported_data_types": plugin_instance.get_supported_data_types(),
                    "supported_dimensions": plugin_instance.get_supported_dimensions(),
                    "supported_aggregations": plugin_instance.get_supported_aggregations()
                })
            elif issubclass(plugin_class, InsightPlugin):
                plugin_info.update({
                    "insight_types": plugin_instance.get_insight_types(),
                    "insight_categories": plugin_instance.get_insight_categories(),
                    "scoring_factors": plugin_instance.get_scoring_factors()
                })
        except Exception as e:
            self.logger.error(f"Error getting plugin info for {plugin_class.__name__}: {str(e)}")
            # Return basic info without the additional details
            pass
        
        return plugin_info 