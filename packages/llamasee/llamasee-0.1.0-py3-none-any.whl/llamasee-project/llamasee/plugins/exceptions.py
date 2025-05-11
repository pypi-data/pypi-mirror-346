"""
Plugin exceptions for LlamaSee.

This module defines exceptions specific to plugin operations.
"""

class PluginError(Exception):
    """Base class for plugin exceptions."""
    pass

class PluginNotFoundError(PluginError):
    """Exception raised when a plugin is not found."""
    pass

class PluginLoadError(PluginError):
    """Exception raised when a plugin fails to load."""
    pass

class PluginInitializationError(PluginError):
    """Exception raised when a plugin fails to initialize."""
    pass

class PluginConfigurationError(PluginError):
    """Exception raised when there is a plugin configuration error."""
    pass

class PluginValidationError(PluginError):
    """Exception raised when plugin validation fails."""
    pass

class PluginDependencyError(PluginError):
    """Exception raised when a plugin dependency is missing or invalid."""
    pass

class PluginExecutionError(PluginError):
    """Exception raised when a plugin operation fails during execution."""
    pass

class PluginStateError(PluginError):
    """Exception raised when a plugin is in an invalid state."""
    pass

class PluginTypeError(PluginError):
    """Exception raised when a plugin type is invalid."""
    pass

class PluginRegistrationError(PluginError):
    """Exception raised when plugin registration fails."""
    pass

class PluginUnregistrationError(PluginError):
    """Exception raised when plugin unregistration fails."""
    pass

class PluginReloadError(PluginError):
    """Exception raised when plugin reload fails."""
    pass

class PluginCleanupError(PluginError):
    """Exception raised when plugin cleanup fails."""
    pass

class PluginDisabledError(PluginError):
    """Exception raised when attempting to use a disabled plugin."""
    pass

class PluginTimeoutError(PluginError):
    """Exception raised when a plugin operation times out."""
    pass

class PluginResourceError(PluginError):
    """Exception raised when a plugin resource is unavailable."""
    pass

class PluginPermissionError(PluginError):
    """Exception raised when a plugin lacks required permissions."""
    pass

class PluginVersionError(PluginError):
    """Exception raised when there is a plugin version mismatch."""
    pass

class PluginCompatibilityError(PluginError):
    """Exception raised when there is a plugin compatibility issue."""
    pass 