"""
Plugin configuration manager for LlamaSee.

This module provides functionality for managing plugin configurations, including
loading, saving, and validating configurations.
"""

import os
import json
import yaml
from typing import Dict, Any, Optional, List, Union
from .insight.base_insight_plugin import BaseInsightPlugin as InsightPlugin
from .comparison.base import ComparisonPlugin
from .base import BasePlugin

# Import the centralized logger
from ..utils.logger import get_logger

class PluginConfigManager:
    """
    Manager for LlamaSee plugin configurations.
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the plugin configuration manager.
        
        Args:
            config_dir: Optional directory to load configurations from
        """
        self.logger = get_logger(__name__)
        self.logger.info("=== PLUGIN LIFECYCLE: CONFIG MANAGER INITIALIZATION ===")
        self.config_dir = config_dir or os.path.join(os.path.dirname(__file__), "config")
        self.logger.info(f"Config directory: {self.config_dir}")
        self.configs: Dict[str, Dict[str, Any]] = {}
        
        # Create the config directory if it doesn't exist
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            self.logger.info(f"Created config directory: {self.config_dir}")
        
        self.logger.info("=== PLUGIN LIFECYCLE: CONFIG MANAGER INITIALIZATION END ===")
    
    def load_config(self, plugin_name: str, config_file: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Load configuration for a plugin.
        
        Args:
            plugin_name: Name of the plugin to load configuration for
            config_file: Optional specific configuration file to load
            
        Returns:
            Plugin configuration dictionary, or None if not found
        """
        self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING CONFIG FOR '{plugin_name}' ===")
        
        # Determine the configuration file path
        if config_file is None:
            # Try JSON first, then YAML
            config_file = os.path.join(self.config_dir, f"{plugin_name}.json")
            if not os.path.exists(config_file):
                config_file = os.path.join(self.config_dir, f"{plugin_name}.yaml")
                if not os.path.exists(config_file):
                    self.logger.warning(f"No configuration file found for plugin: {plugin_name}")
                    self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING CONFIG FAILED ===")
                    return None
        
        # Check if the configuration file exists
        if not os.path.exists(config_file):
            self.logger.warning(f"Configuration file not found: {config_file}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING CONFIG FAILED ===")
            return None
        
        try:
            # Load the configuration based on the file extension
            if config_file.endswith('.json'):
                with open(config_file, 'r') as f:
                    config = json.load(f)
            elif config_file.endswith('.yaml') or config_file.endswith('.yml'):
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
            else:
                self.logger.error(f"Unsupported configuration file format: {config_file}")
                self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING CONFIG FAILED ===")
                return None
            
            # Store the configuration
            self.configs[plugin_name] = config
            
            self.logger.info(f"Successfully loaded configuration for plugin: {plugin_name}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING CONFIG SUCCESS ===")
            return config
        
        except Exception as e:
            self.logger.error(f"Error loading configuration for plugin {plugin_name}: {str(e)}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING CONFIG FAILED ===")
            return None
    
    def get_config(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a plugin (alias for load_config).
        
        Args:
            plugin_name: Name of the plugin to get configuration for
            
        Returns:
            Plugin configuration dictionary, or None if not found
        """
        return self.load_config(plugin_name)
    
    def save_config(self, plugin_name: str, config: Dict[str, Any], config_file: Optional[str] = None, format: str = 'json') -> bool:
        """
        Save configuration for a plugin.
        
        Args:
            plugin_name: Name of the plugin to save configuration for
            config: Configuration dictionary to save
            config_file: Optional specific configuration file to save to
            format: Format to save in ('json' or 'yaml')
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info(f"=== PLUGIN LIFECYCLE: SAVING CONFIG FOR '{plugin_name}' ===")
        
        # Determine the configuration file path
        if config_file is None:
            config_file = os.path.join(self.config_dir, f"{plugin_name}.{format}")
        
        try:
            # Save the configuration based on the file extension
            if config_file.endswith('.json'):
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)
            elif config_file.endswith('.yaml') or config_file.endswith('.yml'):
                with open(config_file, 'w') as f:
                    yaml.safe_dump(config, f, default_flow_style=False)
            else:
                self.logger.error(f"Unsupported configuration file format: {config_file}")
                self.logger.info(f"=== PLUGIN LIFECYCLE: SAVING CONFIG FAILED ===")
                return False
            
            # Store the configuration
            self.configs[plugin_name] = config
            
            self.logger.info(f"Successfully saved configuration for plugin: {plugin_name}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: SAVING CONFIG SUCCESS ===")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to save configuration for plugin {plugin_name}: {str(e)}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: SAVING CONFIG FAILED ===")
            return False
    
    def validate_config(self, plugin: BasePlugin, config: Dict[str, Any]) -> bool:
        """
        Validate configuration for a plugin.
        
        Args:
            plugin: Plugin instance to validate configuration for
            config: Configuration dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        self.logger.info(f"=== PLUGIN LIFECYCLE: VALIDATING CONFIG FOR '{plugin.__class__.__name__}' ===")
        
        try:
            # Get required configuration keys
            required_keys = plugin.get_required_config_keys()
            
            # Check that all required keys are present
            for key in required_keys:
                if key not in config:
                    self.logger.error(f"Missing required configuration key: {key}")
                    self.logger.info(f"=== PLUGIN LIFECYCLE: VALIDATING CONFIG FAILED ===")
                    return False
            
            # Validate configuration values
            is_valid = plugin.validate_config(config)
            
            if is_valid:
                self.logger.info(f"Configuration for {plugin.__class__.__name__} is valid")
                self.logger.info(f"=== PLUGIN LIFECYCLE: VALIDATING CONFIG SUCCESS ===")
            else:
                self.logger.warning(f"Configuration for {plugin.__class__.__name__} is invalid")
                self.logger.info(f"=== PLUGIN LIFECYCLE: VALIDATING CONFIG FAILED ===")
            
            return is_valid
        
        except Exception as e:
            self.logger.error(f"Failed to validate configuration: {str(e)}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: VALIDATING CONFIG FAILED ===")
            return False
    
    def get_default_config(self, plugin: BasePlugin) -> Dict[str, Any]:
        """
        Get the default configuration for a plugin.
        
        Args:
            plugin: Plugin instance to get default configuration for
            
        Returns:
            Default configuration dictionary
        """
        self.logger.info(f"=== PLUGIN LIFECYCLE: GETTING DEFAULT CONFIG FOR '{plugin.__class__.__name__}' ===")
        
        try:
            # Get default configuration from the plugin
            default_config = plugin.get_default_config()
            
            self.logger.info(f"Successfully retrieved default configuration for {plugin.__class__.__name__}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: GETTING DEFAULT CONFIG SUCCESS ===")
            
            return default_config
        
        except Exception as e:
            self.logger.error(f"Failed to get default configuration: {str(e)}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: GETTING DEFAULT CONFIG FAILED ===")
            
            # Return an empty configuration as a fallback
            return {}
    
    def merge_configs(self, base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two configurations, with override_config taking precedence.
        
        Args:
            base_config: Base configuration dictionary
            override_config: Override configuration dictionary
            
        Returns:
            Merged configuration dictionary
        """
        self.logger.info("=== PLUGIN LIFECYCLE: MERGING CONFIGS ===")
        
        # Create a deep copy of the base configuration
        merged_config = base_config.copy()
        
        # Merge the override configuration
        for key, value in override_config.items():
            if key in merged_config and isinstance(merged_config[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                merged_config[key] = self.merge_configs(merged_config[key], value)
            else:
                # Override the value
                merged_config[key] = value
        
        self.logger.info("Successfully merged configurations")
        self.logger.info(f"=== PLUGIN LIFECYCLE: MERGING CONFIGS SUCCESS ===")
        
        return merged_config
    
    def get_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all plugin configurations.
        
        Returns:
            Dictionary mapping plugin names to configurations
        """
        self.logger.info("=== PLUGIN LIFECYCLE: GETTING ALL CONFIGS ===")
        
        # List all configuration files
        config_files = self.list_config_files()
        
        # Load all configurations
        for config_file in config_files:
            plugin_name = os.path.splitext(os.path.basename(config_file))[0]
            self.load_config(plugin_name, config_file)
        
        self.logger.info(f"Retrieved {len(self.configs)} configurations")
        self.logger.info(f"=== PLUGIN LIFECYCLE: GETTING ALL CONFIGS SUCCESS ===")
        
        return self.configs
    
    def clear_configs(self) -> None:
        """Clear all loaded configurations."""
        self.logger.info("=== PLUGIN LIFECYCLE: CLEARING ALL CONFIGS ===")
        self.configs.clear()
        self.logger.info("Successfully cleared all configurations")
        self.logger.info(f"=== PLUGIN LIFECYCLE: CLEARING ALL CONFIGS SUCCESS ===")
    
    def list_config_files(self) -> List[str]:
        """
        List all configuration files in the config directory.
        
        Returns:
            List of configuration file paths
        """
        self.logger.info("=== PLUGIN LIFECYCLE: LISTING CONFIG FILES ===")
        
        config_files = []
        
        # List all files in the config directory
        for file_name in os.listdir(self.config_dir):
            if file_name.endswith('.json') or file_name.endswith('.yaml') or file_name.endswith('.yml'):
                config_files.append(os.path.join(self.config_dir, file_name))
        
        self.logger.info(f"Found {len(config_files)} configuration files")
        self.logger.info(f"=== PLUGIN LIFECYCLE: LISTING CONFIG FILES SUCCESS ===")
        
        return config_files
    
    def delete_config(self, plugin_name: str) -> bool:
        """
        Delete a configuration file for a plugin.
        
        Args:
            plugin_name: Name of the plugin to delete configuration for
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info(f"=== PLUGIN LIFECYCLE: DELETING CONFIG FOR '{plugin_name}' ===")
        
        # Try to find the configuration file
        config_file = os.path.join(self.config_dir, f"{plugin_name}.json")
        if not os.path.exists(config_file):
            config_file = os.path.join(self.config_dir, f"{plugin_name}.yaml")
            if not os.path.exists(config_file):
                self.logger.warning(f"No configuration file found for plugin: {plugin_name}")
                self.logger.info(f"=== PLUGIN LIFECYCLE: DELETING CONFIG FAILED ===")
                return False
        
        try:
            # Delete the configuration file
            os.remove(config_file)
            
            # Remove the configuration from the cache
            if plugin_name in self.configs:
                del self.configs[plugin_name]
            
            self.logger.info(f"Successfully deleted configuration for plugin: {plugin_name}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: DELETING CONFIG SUCCESS ===")
            
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to delete configuration for plugin {plugin_name}: {str(e)}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: DELETING CONFIG FAILED ===")
            
            return False 