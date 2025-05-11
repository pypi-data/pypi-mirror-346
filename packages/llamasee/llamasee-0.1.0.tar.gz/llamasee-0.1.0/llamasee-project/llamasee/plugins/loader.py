"""
Plugin loader for LlamaSee.

This module provides functionality for dynamically loading plugins from a directory.
"""

import os
import importlib
import importlib.util
import logging
import inspect
import sys
from typing import Dict, List, Type, Optional, Any
from .base import BasePlugin
from .comparison.base import ComparisonPlugin
from .insight.base_insight_plugin import BaseInsightPlugin as InsightPlugin

# Import the centralized logger
from ..utils.logger import get_logger

class PluginLoader:
    """
    Loader for LlamaSee plugins.
    """
    
    def __init__(self, plugin_dir: Optional[str] = None):
        """
        Initialize the plugin loader.
        
        Args:
            plugin_dir: Optional directory to load plugins from
        """
        self.logger = get_logger(__name__)
        self.logger.info("=== PLUGIN LIFECYCLE: LOADER INITIALIZATION ===")
        self.plugin_dir = plugin_dir or os.path.join(os.path.dirname(__file__))
        self.logger.info(f"Plugin directory: {self.plugin_dir}")
        self.loaded_plugins: Dict[str, Type[BasePlugin]] = {}
        self.logger.info("=== PLUGIN LIFECYCLE: LOADER INITIALIZATION END ===")
    
    def load_plugin(self, file_path: str) -> Optional[Type[BasePlugin]]:
        """
        Load a plugin from a file.
        
        Args:
            file_path: Path to the plugin file
            
        Returns:
            The loaded plugin class, or None if loading failed
        """
        self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING PLUGIN FROM FILE '{file_path}' ===")
        
        # Skip interface and base files
        file_name = os.path.basename(file_path)
        if file_name in ["interface.py", "base.py", "base_insight_plugin.py"]:
            self.logger.info(f"Skipping interface/base file: {file_path}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING PLUGIN FROM FILE SKIPPED ===")
            return None
        
        if not os.path.exists(file_path):
            self.logger.warning(f"Plugin file not found: {file_path}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING PLUGIN FROM FILE FAILED ===")
            return None
        
        try:
            # Get the module name from the file path
            rel_path = os.path.relpath(file_path, self.plugin_dir)
            module_name = os.path.splitext(rel_path)[0].replace(os.sep, ".")
            
            # Import the module
            module = importlib.import_module(f".{module_name}", package="llamasee.plugins")
            
            # Find plugin classes in the module
            plugin_classes = []
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BasePlugin) and obj != BasePlugin:
                    # Check if the class is abstract
                    try:
                        abstract_methods = getattr(obj, '__abstractmethods__', set())
                        if not abstract_methods:  # Only add non-abstract classes
                            plugin_classes.append(obj)
                    except Exception as e:
                        self.logger.warning(f"Error checking if {name} is abstract: {str(e)}")
                        continue
            
            if not plugin_classes:
                self.logger.info(f"No concrete plugin classes found in {file_path}")
                self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING PLUGIN FROM FILE SKIPPED ===")
                return None
            
            if len(plugin_classes) > 1:
                self.logger.warning(f"Multiple plugin classes found in {file_path}: {[c.__name__ for c in plugin_classes]}")
            
            # Return the first plugin class
            plugin_class = plugin_classes[0]
            self.loaded_plugins[plugin_class.__name__] = plugin_class
            self.logger.info(f"Loaded plugin: {plugin_class.__name__}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING PLUGIN FROM FILE SUCCESS ===")
            return plugin_class
        
        except Exception as e:
            self.logger.error(f"Error loading plugin from {file_path}: {str(e)}")
            self.logger.info(f"=== PLUGIN LIFECYCLE: LOADING PLUGIN FROM FILE FAILED ===")
            return None
    
    def discover_plugins(self) -> Dict[str, Type[BasePlugin]]:
        """
        Discover plugins in the plugin directory.
        
        Returns:
            Dictionary mapping plugin names to plugin classes
        """
        self.logger.info(f"Discovering plugins in {self.plugin_dir}")
        
        # Clear loaded plugins
        self.loaded_plugins.clear()
        
        # Files to skip
        skip_files = {
            "interface.py", "base.py", "base_insight_plugin.py",
            "factory.py", "loader.py", "registry.py", "config_manager.py",
            "__init__.py", "manager.py"
        }
        
        # Discover plugins in the plugin directory
        for root, dirs, files in os.walk(self.plugin_dir):
            # Skip __pycache__ directories
            if "__pycache__" in root:
                continue
                
            # Skip utility directories
            if any(util_dir in root for util_dir in ["utils", "tests", "config"]):
                continue
            
            for file_name in files:
                if file_name.endswith(".py") and file_name not in skip_files:
                    file_path = os.path.join(root, file_name)
                    self.load_plugin(file_path)
        
        self.logger.info(f"Discovered {len(self.loaded_plugins)} plugins")
        return self.loaded_plugins
    
    def discover_comparison_plugins(self, directory: Optional[str] = None) -> Dict[str, Type[ComparisonPlugin]]:
        """
        Discover comparison plugins in the plugin directory.
        
        Args:
            directory: Optional directory to discover plugins in
            
        Returns:
            Dictionary mapping plugin names to comparison plugin classes
        """
        self.logger.info("Discovering comparison plugins")
        
        comparison_plugins = {}
        
        # Use the provided directory or the default comparison directory
        comparison_dir = directory or os.path.join(self.plugin_dir, "comparison")
        if os.path.exists(comparison_dir):
            for file_name in os.listdir(comparison_dir):
                if file_name.endswith(".py") and not file_name.startswith("_"):
                    file_path = os.path.join(comparison_dir, file_name)
                    plugin_class = self.load_plugin(file_path)
                    if plugin_class and issubclass(plugin_class, ComparisonPlugin):
                        comparison_plugins[plugin_class.__name__] = plugin_class
        
        self.logger.info(f"Discovered {len(comparison_plugins)} comparison plugins")
        return comparison_plugins
    
    def discover_insight_plugins(self) -> Dict[str, Type[InsightPlugin]]:
        """
        Discover insight plugins in a directory.
        
        Returns:
            Dictionary mapping plugin names to plugin classes
        """
        self.logger.info("=== PLUGIN LIFECYCLE: DISCOVERING INSIGHT PLUGINS ===")
        self.logger.info(f"Discovering insight plugins in {self.plugin_dir}")
        
        insight_plugins = {}
        insight_dir = os.path.join(self.plugin_dir, "insight")
        
        if not os.path.exists(insight_dir):
            self.logger.warning(f"Insight plugin directory not found: {insight_dir}")
            self.logger.info("=== PLUGIN LIFECYCLE: DISCOVERING INSIGHT PLUGINS END ===")
            return insight_plugins
        
        # Get all Python files in the insight directory
        plugin_files = [f for f in os.listdir(insight_dir) 
                        if f.endswith('.py') and not f.startswith('__')]
        
        self.logger.info(f"Found {len(plugin_files)} potential insight plugin files")
        
        for plugin_file in plugin_files:
            file_path = os.path.join(insight_dir, plugin_file)
            self.logger.info(f"Processing plugin file: {plugin_file}")
            
            try:
                # Load the plugin
                plugin_class = self.load_plugin(file_path)
                
                if plugin_class is not None and issubclass(plugin_class, InsightPlugin):
                    # Get the plugin name
                    plugin_name = plugin_class.__name__.lower()
                    if plugin_name.endswith('plugin'):
                        plugin_name = plugin_name[:-6]  # Remove 'plugin' suffix
                    
                    # Format the plugin name for configuration files
                    plugin_name = ''.join(['_' + c.lower() if c.isupper() else c for c in plugin_name]).lstrip('_')
                    
                    self.logger.info(f"Registering insight plugin: {plugin_name}")
                    insight_plugins[plugin_name] = plugin_class
                else:
                    self.logger.warning(f"No valid insight plugin found in {plugin_file}")
            except Exception as e:
                self.logger.error(f"Error processing plugin file {plugin_file}: {str(e)}")
        
        self.logger.info(f"Discovered {len(insight_plugins)} insight plugins: {list(insight_plugins.keys())}")
        self.logger.info("=== PLUGIN LIFECYCLE: DISCOVERING INSIGHT PLUGINS END ===")
        return insight_plugins
    
    def get_plugin_class(self, plugin_name: str) -> Optional[Type[BasePlugin]]:
        """
        Get a plugin class by name.
        
        Args:
            plugin_name: The name of the plugin class
            
        Returns:
            The plugin class, or None if not found
        """
        if plugin_name in self.loaded_plugins:
            return self.loaded_plugins[plugin_name]
        
        self.logger.warning(f"Plugin class not found: {plugin_name}")
        return None
    
    def get_all_plugin_classes(self) -> Dict[str, Type[BasePlugin]]:
        """
        Get all loaded plugin classes.
        
        Returns:
            Dictionary mapping plugin names to plugin classes
        """
        return self.loaded_plugins
    
    def create_plugin_instance(self, plugin_name: str, config: Optional[Dict[str, Any]] = None) -> Optional[BasePlugin]:
        """
        Create a plugin instance.
        
        Args:
            plugin_name: The name of the plugin class
            config: Optional configuration for the plugin
            
        Returns:
            The plugin instance, or None if creation failed
        """
        plugin_class = self.get_plugin_class(plugin_name)
        if not plugin_class:
            return None
        
        try:
            plugin_instance = plugin_class()
            if config:
                plugin_instance.configure(config)
            return plugin_instance
        except Exception as e:
            self.logger.error(f"Error creating plugin instance {plugin_name}: {str(e)}")
            return None
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a plugin.
        
        Args:
            plugin_name: The name of the plugin class
            
        Returns:
            Dictionary containing plugin information, or None if not found
        """
        plugin_class = self.get_plugin_class(plugin_name)
        if not plugin_class:
            return None
        
        plugin_info = {
            "name": getattr(plugin_class, "name", plugin_class.__name__),
            "description": getattr(plugin_class, "description", ""),
            "version": getattr(plugin_class, "version", "0.0.0"),
            "capabilities": getattr(plugin_class, "capabilities", []),
            "characteristics": getattr(plugin_class, "characteristics", {})
        }
        
        if issubclass(plugin_class, ComparisonPlugin):
            plugin_info.update({
                "comparison_types": plugin_class.get_comparison_types(),
                "comparison_metrics": plugin_class.get_comparison_metrics(),
                "supported_data_types": plugin_class.get_supported_data_types(),
                "supported_dimensions": plugin_class.get_supported_dimensions(),
                "supported_aggregations": plugin_class.get_supported_aggregations()
            })
        
        return plugin_info
    
    def clear_loaded_plugins(self) -> None:
        """Clear all loaded plugins."""
        self.logger.info("Clearing all loaded plugins")
        self.loaded_plugins.clear()
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """
        Reload a plugin.
        
        Args:
            plugin_name: The name of the plugin class
            
        Returns:
            True if the plugin was reloaded successfully, False otherwise
        """
        self.logger.info(f"Reloading plugin: {plugin_name}")
        
        if plugin_name not in self.loaded_plugins:
            self.logger.warning(f"Plugin class not found: {plugin_name}")
            return False
        
        try:
            # Get the module name from the plugin class
            plugin_class = self.loaded_plugins[plugin_name]
            module_name = plugin_class.__module__
            
            # Reload the module
            module = importlib.import_module(module_name)
            importlib.reload(module)
            
            # Find the plugin class in the reloaded module
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and name == plugin_name:
                    self.loaded_plugins[plugin_name] = obj
                    self.logger.info(f"Reloaded plugin: {plugin_name}")
                    return True
            
            self.logger.warning(f"Plugin class not found in reloaded module: {plugin_name}")
            return False
        
        except Exception as e:
            self.logger.error(f"Error reloading plugin {plugin_name}: {str(e)}")
            return False
    
    def _setup_package_structure(self, plugin_path: str) -> None:
        """
        Set up the package structure for a plugin to handle relative imports.
        
        Args:
            plugin_path: The path to the plugin file
        """
        # Get the directory containing the plugin
        plugin_dir = os.path.dirname(plugin_path)
        
        # Get the parent directory (package root)
        parent_dir = os.path.dirname(plugin_dir)
        
        # Get the grandparent directory (project root)
        grandparent_dir = os.path.dirname(parent_dir)
        
        # Add all relevant directories to the Python path
        for directory in [grandparent_dir, parent_dir, plugin_dir]:
            if directory not in sys.path:
                sys.path.insert(0, directory)
        
        # Create __init__.py files in all directories if they don't exist
        for directory in [plugin_dir, parent_dir, grandparent_dir]:
            init_file = os.path.join(directory, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write('# Auto-generated __init__.py for plugin package\n')
        
        # Create __init__.py files in all subdirectories of the parent directory
        for root, dirs, files in os.walk(parent_dir):
            for dir_name in dirs:
                # Skip directories with hyphens as they can't be Python packages
                if '-' in dir_name:
                    continue
                init_file = os.path.join(root, dir_name, '__init__.py')
                if not os.path.exists(init_file):
                    with open(init_file, 'w') as f:
                        f.write('# Auto-generated __init__.py for package subdirectory\n')
        
        # Create __init__.py files in all subdirectories of the grandparent directory
        for root, dirs, files in os.walk(grandparent_dir):
            for dir_name in dirs:
                # Skip directories with hyphens as they can't be Python packages
                if '-' in dir_name:
                    continue
                init_file = os.path.join(root, dir_name, '__init__.py')
                if not os.path.exists(init_file):
                    with open(init_file, 'w') as f:
                        f.write('# Auto-generated __init__.py for project subdirectory\n') 