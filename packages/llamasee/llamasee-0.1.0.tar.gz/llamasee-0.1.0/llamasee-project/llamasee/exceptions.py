"""
Exceptions module for LlamaSee.

This module defines custom exceptions used throughout the LlamaSee package.
"""

class LlamaSeeError(Exception):
    """Base exception class for LlamaSee errors."""
    pass

class ConfigurationError(LlamaSeeError):
    """Exception raised for configuration-related errors."""
    pass

class DataError(LlamaSeeError):
    """Exception raised for data-related errors."""
    pass

class ValidationError(LlamaSeeError):
    """Exception raised for validation errors."""
    pass

class PluginError(LlamaSeeError):
    """Exception raised for plugin-related errors."""
    pass

class LLMError(LlamaSeeError):
    """Exception raised for LLM-related errors."""
    pass

class StorageError(LlamaSeeError):
    """Exception raised for storage-related errors."""
    pass

class InsightError(LlamaSeeError):
    """Exception raised for insight generation errors."""
    pass 