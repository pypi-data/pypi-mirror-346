"""
Plugin manager for LlamaSee.

This module provides a high-level interface for managing plugins.
"""

import os
import logging
from typing import Dict, List, Type, Optional, Any, Set
from .base import BasePlugin
from .comparison.base import ComparisonPlugin
from .insight.base_insight_plugin import BaseInsightPlugin as InsightPlugin
from .loader import PluginLoader
from .registry import PluginRegistry
from .config_manager import PluginConfigManager

# Import the centralized logger
from ..utils.logger import get_logger

class PluginManager:
    """
    Manager for LlamaSee plugins.
    """
    
    def __init__(self, plugin_dir: Optional[str] = None, config_dir: Optional[str] = None):
        """
        Initialize the plugin manager.
        
        Args:
            plugin_dir: Optional directory to load plugins from
            config_dir: Optional directory to load configurations from
        """
        self.logger = get_logger(__name__)
        self.logger.info("Initializing PluginManager")
        self.plugin_dir = plugin_dir or os.path.join(os.path.dirname(__file__))
        self.config_dir = config_dir or os.path.join(os.path.dirname(__file__), "config")
        
        self.logger.info(f"Plugin directory: {self.plugin_dir}")
        self.logger.info(f"Config directory: {self.config_dir}")
        
        # Initialize the plugin components
        self.logger.info("Initializing plugin components")
        self.loader = PluginLoader(self.plugin_dir)
        self.registry = PluginRegistry(self.plugin_dir, self.config_dir)
        self.config_manager = PluginConfigManager(self.config_dir)
        self.logger.info("Plugin components initialized")
    
    def discover_plugins(self) -> None:
        """
        Discover and register all available plugins.
        """
        self.logger.info("=== PLUGIN LIFECYCLE: DISCOVERY START ===")
        self.logger.info("Discovering plugins...")
        self.logger.debug("Starting plugin discovery process")
        
        # Discover insight plugins
        self.logger.info("Discovering insight plugins")
        insight_plugins = self.loader.discover_insight_plugins()
        self.logger.info(f"Discovered {len(insight_plugins)} insight plugins: {list(insight_plugins.keys())}")
        
        for plugin_name, plugin_class in insight_plugins.items():
            self.logger.info(f"Registering discovered insight plugin: {plugin_name}")
            self.register_plugin(plugin_name, plugin_class)
            
        self.logger.info(f"Plugin discovery complete. Registered {len(self.registry.insight_plugins)} insight plugins")
        self.logger.info("=== PLUGIN LIFECYCLE: DISCOVERY END ===")
    
    def get_comparison_plugin(self, plugin_name: str, config: Optional[Dict[str, Any]] = None) -> Optional[ComparisonPlugin]:
        """
        Get a comparison plugin instance.
        
        Args:
            plugin_name: The name of the comparison plugin to get
            config: Optional configuration for the plugin
            
        Returns:
            The comparison plugin instance, or None if the plugin does not exist
        """
        self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING COMPARISON PLUGIN '{plugin_name}' ===")
        plugin = self.registry.get_comparison_plugin(plugin_name, config)
        if plugin:
            self.logger.info(f"Successfully loaded comparison plugin: {plugin_name}")
        else:
            self.logger.warning(f"Failed to load comparison plugin: {plugin_name}")
        self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING COMPARISON PLUGIN END ===")
        return plugin
    
    def get_insight_plugin(self, plugin_name: str, config: Optional[Dict[str, Any]] = None) -> Optional[InsightPlugin]:
        """
        Get an insight plugin instance.
        
        Args:
            plugin_name: The name of the insight plugin to get
            config: Optional configuration for the plugin
            
        Returns:
            The insight plugin instance, or None if the plugin does not exist
        """
        self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING INSIGHT PLUGIN '{plugin_name}' ===")
        plugin = self.registry.get_insight_plugin(plugin_name, config)
        if plugin:
            self.logger.info(f"Successfully loaded insight plugin: {plugin_name}")
        else:
            self.logger.warning(f"Failed to load insight plugin: {plugin_name}")
        self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING INSIGHT PLUGIN END ===")
        return plugin
    
    def get_insight_plugins_by_type(self, insight_type: str) -> List[Type[InsightPlugin]]:
        """
        Get all insight plugins of a specific type.
        
        Args:
            insight_type: Type of insight to get plugins for. Use "all" to get all plugins.
            
        Returns:
            List of plugin classes
        """
        self.logger.info(f"=== PLUGIN LIFECYCLE: GETTING INSIGHT PLUGINS BY TYPE '{insight_type}' ===")
        self.logger.info(f"Getting insight plugins for type: {insight_type}")
        
        # Special case: if insight_type is "all", return all plugins without filtering
        if insight_type == "all":
            self.logger.info("Insight type is 'all', returning all plugins without filtering")
            all_plugins = list(self.registry.get_all_insight_plugins().values())
            self.logger.info(f"Found {len(all_plugins)} plugins of type 'all': {[p.__name__ for p in all_plugins]}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: GETTING INSIGHT PLUGINS BY TYPE END ===")
            return all_plugins
        
        plugins = []
        
        for plugin_name, plugin_class in self.registry.get_all_insight_plugins().items():
            self.logger.info(f"Checking plugin {plugin_name} for type {insight_type}")
            try:
                # Create an instance to check the insight_type attribute
                plugin_instance = plugin_class()
                if hasattr(plugin_instance, 'insight_type') and plugin_instance.insight_type == insight_type:
                    self.logger.info(f"Found matching plugin: {plugin_name}")
                    plugins.append(plugin_class)
            except Exception as e:
                self.logger.error(f"Error checking plugin {plugin_name}: {str(e)}")
                
        self.logger.info(f"Found {len(plugins)} plugins for type {insight_type}: {[p.__name__ for p in plugins]}")
        self.logger.info(f"=== PLUGIN LIFECYCLE: GETTING INSIGHT PLUGINS BY TYPE END ===")
        return plugins
    
    def get_insight_plugins_by_scope(self, scope_level: str, config: Optional[Dict[str, Any]] = None) -> List[InsightPlugin]:
        """
        Get insight plugins by scope level (whole, dimension, individual).
        
        Args:
            scope_level: The scope level of insight plugins to get
            config: Optional configuration for the plugins
            
        Returns:
            List of insight plugin instances supporting the specified scope level
        """
        plugins = []
        all_plugins = self.registry.get_all_insight_plugins()
        
        for plugin_name, plugin in all_plugins.items():
            plugin_config = config or self.get_plugin_config(plugin_name)
            if plugin_config and scope_level in plugin_config.get("characteristics", {}).get("scope_levels", []):
                plugins.append(self.get_insight_plugin(plugin_name, plugin_config))
        
        return plugins
    
    def get_insight_plugins_by_traceability(self, traceability_requirements: Dict[str, bool], 
                                           config: Optional[Dict[str, Any]] = None) -> List[InsightPlugin]:
        """
        Get insight plugins by traceability requirements.
        
        Args:
            traceability_requirements: Dictionary mapping traceability features to required values
            config: Optional configuration for the plugins
            
        Returns:
            List of insight plugin instances meeting the traceability requirements
        """
        plugins = []
        all_plugins = self.registry.get_all_insight_plugins()
        
        for plugin_name, plugin in all_plugins.items():
            plugin_config = config or self.get_plugin_config(plugin_name)
            if not plugin_config:
                continue
                
            traceability = plugin_config.get("characteristics", {}).get("traceability", {})
            meets_requirements = True
            
            for feature, required in traceability_requirements.items():
                if feature not in traceability or traceability[feature] != required:
                    meets_requirements = False
                    break
            
            if meets_requirements:
                plugins.append(self.get_insight_plugin(plugin_name, plugin_config))
        
        return plugins
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a plugin.
        
        Args:
            plugin_name: The name of the plugin to get information about
            
        Returns:
            Dictionary containing plugin information, or None if the plugin does not exist
        """
        return self.registry.get_plugin_info(plugin_name)
    
    def get_all_plugin_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all registered plugins.
        
        Returns:
            Dictionary mapping plugin names to plugin information
        """
        return self.registry.get_all_plugin_info()
    
    def get_plugin_capabilities(self) -> Dict[str, Set[str]]:
        """
        Get the capabilities of all registered plugins.
        
        Returns:
            Dictionary mapping capability types to sets of plugin names
        """
        return self.registry.get_plugin_capabilities()
    
    def load_plugin_config(self, plugin_name: str, config_file: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Load a configuration for a plugin.
        
        Args:
            plugin_name: The name of the plugin to load configuration for
            config_file: Optional specific configuration file to load
            
        Returns:
            The loaded configuration, or None if the configuration could not be loaded
        """
        return self.config_manager.load_config(plugin_name, config_file)
    
    def save_plugin_config(self, plugin_name: str, config: Dict[str, Any], config_file: Optional[str] = None) -> bool:
        """
        Save a configuration for a plugin.
        
        Args:
            plugin_name: The name of the plugin to save configuration for
            config: The configuration to save
            config_file: Optional specific configuration file to save to
            
        Returns:
            True if the configuration was saved successfully, False otherwise
        """
        return self.config_manager.save_config(plugin_name, config, config_file)
    
    def get_plugin_config(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a configuration for a plugin.
        
        Args:
            plugin_name: The name of the plugin to get configuration for
            
        Returns:
            The configuration, or None if the configuration does not exist
        """
        return self.config_manager.get_config(plugin_name)
    
    def validate_plugin_config(self, plugin: BasePlugin, config: Dict[str, Any]) -> bool:
        """
        Validate a configuration for a plugin.
        
        Args:
            plugin: The plugin to validate the configuration for
            config: The configuration to validate
            
        Returns:
            True if the configuration is valid, False otherwise
        """
        return self.config_manager.validate_config(plugin, config)
    
    def get_default_plugin_config(self, plugin: BasePlugin) -> Dict[str, Any]:
        """
        Get the default configuration for a plugin.
        
        Args:
            plugin: The plugin to get the default configuration for
            
        Returns:
            The default configuration
        """
        return self.config_manager.get_default_config(plugin)
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """
        Reload a plugin.
        
        Args:
            plugin_name: The name of the plugin to reload
            
        Returns:
            True if the plugin was reloaded successfully, False otherwise
        """
        return self.registry.reload_plugin(plugin_name)
    
    def reload_all_plugins(self) -> Dict[str, bool]:
        """
        Reload all plugins.
        
        Returns:
            Dictionary mapping plugin names to reload success status
        """
        return self.registry.reload_all_plugins()
    
    def clear_plugins(self) -> None:
        """Clear all registered plugins."""
        self.registry.clear_plugins()
        self.config_manager.clear_configs()
        
    def register_plugin(self, plugin: Any) -> None:
        """
        Register a plugin with the plugin manager.
        
        Args:
            plugin: Plugin instance to register
        """
        self.logger.info(f"=== PLUGIN LIFECYCLE: REGISTRATION START ===")
        self.logger.info(f"Registering plugin: {plugin.__class__.__name__}")
        
        if not hasattr(plugin, 'plugin_type'):
            self.logger.warning(f"Plugin {plugin.__class__.__name__} missing plugin_type attribute")
            self.logger.info(f"=== PLUGIN LIFECYCLE: REGISTRATION FAILED ===")
            return
        
        if not hasattr(plugin, 'insight_type'):
            self.logger.warning(f"Plugin {plugin.__class__.__name__} missing insight_type attribute")
            self.logger.info(f"=== PLUGIN LIFECYCLE: REGISTRATION FAILED ===")
            return
        
        # Convert class name to a more consistent format for config files
        # Replace camelCase with underscores, then convert to lowercase
        plugin_name = ''.join(['_' + c.lower() if c.isupper() else c for c in plugin.__class__.__name__]).lstrip('_')
        
        plugin_key = f"{plugin.plugin_type}_{plugin.insight_type}"
        self.logger.debug(f"Plugin key: {plugin_key}")
        
        # Register the plugin with the registry
        self.registry.register_plugin(plugin_name, plugin)
        self.logger.info(f"Successfully registered plugin {plugin.__class__.__name__} with key {plugin_key}")
        
        # Log plugin capabilities
        self.logger.debug(f"Plugin capabilities: {getattr(plugin, 'capabilities', 'Not specified')}")
        self.logger.debug(f"Plugin characteristics: {getattr(plugin, 'characteristics', 'Not specified')}")
        self.logger.info(f"=== PLUGIN LIFECYCLE: REGISTRATION END ===") 