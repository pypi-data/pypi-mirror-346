"""
Plugin utilities for LlamaSee.

This module provides common utility functions for plugins.
"""

import os
import sys
import json
import yaml
import logging
import importlib
import importlib.util
from typing import Dict, List, Any, Optional, Type, Union
from .exceptions import (
    PluginError,
    PluginLoadError,
    PluginConfigurationError,
    PluginDependencyError,
    PluginResourceError,
    PluginVersionError
)

logger = logging.getLogger(__name__)

def load_plugin_module(plugin_path: str) -> Any:
    """
    Load a plugin module from a file path.
    
    Args:
        plugin_path: Path to the plugin file
        
    Returns:
        The loaded module
        
    Raises:
        PluginLoadError: If the plugin module cannot be loaded
    """
    try:
        # Get the module name from the file path
        module_name = os.path.splitext(os.path.basename(plugin_path))[0]
        
        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, plugin_path)
        if spec is None or spec.loader is None:
            raise PluginLoadError(f"Failed to load plugin: {plugin_path}")
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return module
    
    except Exception as e:
        raise PluginLoadError(f"Error loading plugin module {plugin_path}: {e}")

def load_plugin_config(config_path: str) -> Dict[str, Any]:
    """
    Load a plugin configuration from a file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        The loaded configuration
        
    Raises:
        PluginConfigurationError: If the configuration cannot be loaded
    """
    try:
        # Check if the file exists
        if not os.path.exists(config_path):
            raise PluginConfigurationError(f"Configuration file not found: {config_path}")
        
        # Load the configuration based on the file extension
        if config_path.endswith('.json'):
            with open(config_path, 'r') as f:
                config = json.load(f)
        elif config_path.endswith('.yaml') or config_path.endswith('.yml'):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        else:
            raise PluginConfigurationError(f"Unsupported configuration file format: {config_path}")
        
        return config
    
    except Exception as e:
        raise PluginConfigurationError(f"Error loading configuration from {config_path}: {e}")

def save_plugin_config(config: Dict[str, Any], config_path: str) -> None:
    """
    Save a plugin configuration to a file.
    
    Args:
        config: The configuration to save
        config_path: Path to save the configuration to
        
    Raises:
        PluginConfigurationError: If the configuration cannot be saved
    """
    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Save the configuration based on the file extension
        if config_path.endswith('.json'):
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
        elif config_path.endswith('.yaml') or config_path.endswith('.yml'):
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
        else:
            raise PluginConfigurationError(f"Unsupported configuration file format: {config_path}")
    
    except Exception as e:
        raise PluginConfigurationError(f"Error saving configuration to {config_path}: {e}")

def check_plugin_dependencies(dependencies: List[str]) -> None:
    """
    Check if plugin dependencies are installed.
    
    Args:
        dependencies: List of dependency names
        
    Raises:
        PluginDependencyError: If any dependencies are missing
    """
    missing_deps = []
    
    for dep in dependencies:
        try:
            importlib.import_module(dep)
        except ImportError:
            missing_deps.append(dep)
    
    if missing_deps:
        raise PluginDependencyError(f"Missing dependencies: {', '.join(missing_deps)}")

def get_plugin_resources(resource_dir: str) -> Dict[str, str]:
    """
    Get plugin resources from a directory.
    
    Args:
        resource_dir: Directory containing plugin resources
        
    Returns:
        Dictionary mapping resource names to file paths
        
    Raises:
        PluginResourceError: If the resource directory cannot be accessed
    """
    try:
        resources = {}
        
        # Check if the directory exists
        if not os.path.exists(resource_dir):
            raise PluginResourceError(f"Resource directory not found: {resource_dir}")
        
        # Get all files in the directory
        for root, _, files in os.walk(resource_dir):
            for file in files:
                file_path = os.path.join(root, file)
                resource_name = os.path.relpath(file_path, resource_dir)
                resources[resource_name] = file_path
        
        return resources
    
    except Exception as e:
        raise PluginResourceError(f"Error accessing resource directory {resource_dir}: {e}")

def check_plugin_version(plugin_version: str, required_version: str) -> bool:
    """
    Check if a plugin version meets the required version.
    
    Args:
        plugin_version: The plugin version
        required_version: The required version
        
    Returns:
        True if the plugin version meets the requirement, False otherwise
        
    Raises:
        PluginVersionError: If the version format is invalid
    """
    try:
        from packaging import version
        
        plugin_ver = version.parse(plugin_version)
        required_ver = version.parse(required_version)
        
        return plugin_ver >= required_ver
    
    except Exception as e:
        raise PluginVersionError(f"Error checking plugin version: {e}")

def merge_plugin_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two plugin configurations.
    
    Args:
        base_config: The base configuration
        override_config: The configuration to override with
        
    Returns:
        The merged configuration
    """
    merged_config = base_config.copy()
    
    for key, value in override_config.items():
        if key in merged_config and isinstance(merged_config[key], dict) and isinstance(value, dict):
            # Recursively merge dictionaries
            merged_config[key] = merge_plugin_configs(merged_config[key], value)
        else:
            # Override the value
            merged_config[key] = value
    
    return merged_config

def validate_plugin_config_schema(config: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """
    Validate a plugin configuration against a schema.
    
    Args:
        config: The configuration to validate
        schema: The schema to validate against
        
    Returns:
        True if the configuration is valid, False otherwise
    """
    try:
        from jsonschema import validate
        validate(instance=config, schema=schema)
        return True
    except Exception:
        return False

def get_plugin_metadata(plugin_dir: str) -> Dict[str, Any]:
    """
    Get metadata for a plugin.
    
    Args:
        plugin_dir: Directory containing the plugin
        
    Returns:
        Dictionary containing plugin metadata
        
    Raises:
        PluginError: If the metadata cannot be loaded
    """
    try:
        metadata_file = os.path.join(plugin_dir, 'metadata.json')
        
        if not os.path.exists(metadata_file):
            metadata_file = os.path.join(plugin_dir, 'metadata.yaml')
        
        if not os.path.exists(metadata_file):
            raise PluginError(f"Metadata file not found in {plugin_dir}")
        
        return load_plugin_config(metadata_file)
    
    except Exception as e:
        raise PluginError(f"Error loading plugin metadata from {plugin_dir}: {e}")

def get_plugin_documentation(plugin_dir: str) -> str:
    """
    Get documentation for a plugin.
    
    Args:
        plugin_dir: Directory containing the plugin
        
    Returns:
        The plugin documentation
        
    Raises:
        PluginError: If the documentation cannot be loaded
    """
    try:
        doc_file = os.path.join(plugin_dir, 'README.md')
        
        if not os.path.exists(doc_file):
            raise PluginError(f"Documentation file not found in {plugin_dir}")
        
        with open(doc_file, 'r') as f:
            return f.read()
    
    except Exception as e:
        raise PluginError(f"Error loading plugin documentation from {plugin_dir}: {e}")

def get_plugin_requirements(plugin_dir: str) -> List[str]:
    """
    Get requirements for a plugin.
    
    Args:
        plugin_dir: Directory containing the plugin
        
    Returns:
        List of plugin requirements
        
    Raises:
        PluginError: If the requirements cannot be loaded
    """
    try:
        req_file = os.path.join(plugin_dir, 'requirements.txt')
        
        if not os.path.exists(req_file):
            return []
        
        with open(req_file, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    except Exception as e:
        raise PluginError(f"Error loading plugin requirements from {plugin_dir}: {e}")

def install_plugin_requirements(requirements: List[str]) -> None:
    """
    Install requirements for a plugin.
    
    Args:
        requirements: List of requirements to install
        
    Raises:
        PluginDependencyError: If the requirements cannot be installed
    """
    try:
        import subprocess
        
        for req in requirements:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', req])
    
    except Exception as e:
        raise PluginDependencyError(f"Error installing plugin requirements: {e}")

def get_plugin_license(plugin_dir: str) -> Optional[str]:
    """
    Get the license for a plugin.
    
    Args:
        plugin_dir: Directory containing the plugin
        
    Returns:
        The plugin license text, or None if not found
    """
    try:
        license_file = os.path.join(plugin_dir, 'LICENSE')
        
        if not os.path.exists(license_file):
            return None
        
        with open(license_file, 'r') as f:
            return f.read()
    
    except Exception:
        return None 