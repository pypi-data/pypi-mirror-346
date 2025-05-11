"""
Logging utilities for LlamaSee.

This module provides a centralized logging system for the LlamaSee package,
ensuring consistent logging across all components.
"""

import os
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Union, List

# Default log levels
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_FILE_LOG_LEVEL = logging.DEBUG
DEFAULT_CONSOLE_LOG_LEVEL = logging.INFO

# Default log format
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class LlamaSeeLogger:
    """
    Centralized logger for LlamaSee.
    
    This class provides a singleton logger instance that can be used
    throughout the LlamaSee package to ensure consistent logging.
    """
    
    _instance = None
    _initialized = False
    _loggers = {}
    
    def __new__(cls, *args, **kwargs):
        """Ensure singleton pattern."""
        if cls._instance is None:
            cls._instance = super(LlamaSeeLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, 
                 log_dir: Optional[str] = None,
                 log_level: int = DEFAULT_LOG_LEVEL,
                 file_log_level: int = DEFAULT_FILE_LOG_LEVEL,
                 console_log_level: int = DEFAULT_CONSOLE_LOG_LEVEL,
                 log_format: str = DEFAULT_LOG_FORMAT,
                 date_format: str = DEFAULT_DATE_FORMAT,
                 log_to_file: bool = True,
                 log_to_console: bool = True):
        """
        Initialize the logger.
        
        Args:
            log_dir: Directory to store log files
            log_level: Overall log level
            file_log_level: Log level for file handler
            console_log_level: Log level for console handler
            log_format: Format string for log messages
            date_format: Format string for timestamps
            log_to_file: Whether to log to file
            log_to_console: Whether to log to console
        """
        if LlamaSeeLogger._initialized:
            return
            
        self.log_dir = log_dir or self._get_default_log_dir()
        self.log_level = log_level
        self.file_log_level = file_log_level
        self.console_log_level = console_log_level
        self.log_format = log_format
        self.date_format = date_format
        self.log_to_file = log_to_file
        self.log_to_console = log_to_console
        
        # Create log directory if it doesn't exist
        if self.log_to_file:
            os.makedirs(self.log_dir, exist_ok=True)
        
        # Set up root logger
        self._setup_root_logger()
        
        LlamaSeeLogger._initialized = True
    
    def _get_default_log_dir(self) -> str:
        """
        Get the default log directory.
        
        Returns:
            Path to the default log directory
        """
        # Try to use a logs directory in the current working directory
        cwd_log_dir = os.path.join(os.getcwd(), "logs")
        if os.path.exists(cwd_log_dir) or os.makedirs(cwd_log_dir, exist_ok=True):
            return cwd_log_dir
        
        # Fall back to user's home directory
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, ".llamasee", "logs")
    
    def _setup_root_logger(self) -> None:
        """Set up the root logger with appropriate handlers."""
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        
        # Remove existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Add console handler if requested
        if self.log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.console_log_level)
            console_formatter = logging.Formatter(self.log_format, self.date_format)
            console_handler.setFormatter(console_formatter)
            root_logger.addHandler(console_handler)
        
        # Add file handler if requested
        if self.log_to_file:
            log_file = os.path.join(self.log_dir, f"llamasee_{datetime.now().strftime('%Y%m%d')}.log")
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(self.file_log_level)
            file_formatter = logging.Formatter(self.log_format, self.date_format)
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a logger with the specified name.
        
        Args:
            name: Name of the logger
            
        Returns:
            Logger instance
        """
        if name not in self._loggers:
            logger = logging.getLogger(name)
            self._loggers[name] = logger
        return self._loggers[name]
    
    def set_log_level(self, level: Union[int, str]) -> None:
        """
        Set the log level for all loggers.
        
        Args:
            level: Log level (integer or string)
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        
        self.log_level = level
        logging.getLogger().setLevel(level)
    
    def set_file_log_level(self, level: Union[int, str]) -> None:
        """
        Set the log level for file handlers.
        
        Args:
            level: Log level (integer or string)
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        
        self.file_log_level = level
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                handler.setLevel(level)
    
    def set_console_log_level(self, level: Union[int, str]) -> None:
        """
        Set the log level for console handlers.
        
        Args:
            level: Log level (integer or string)
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        
        self.console_log_level = level
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                handler.setLevel(level)
    
    def add_file_handler(self, filename: str, level: Optional[int] = None) -> None:
        """
        Add a new file handler.
        
        Args:
            filename: Name of the log file
            level: Log level for the handler
        """
        if level is None:
            level = self.file_log_level
        
        log_file = os.path.join(self.log_dir, filename)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(self.log_format, self.date_format)
        file_handler.setFormatter(file_formatter)
        logging.getLogger().addHandler(file_handler)
    
    def log_llm_request(self, 
                       provider: str, 
                       model: str, 
                       prompt: str, 
                       response: str, 
                       duration: float,
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an LLM request.
        
        Args:
            provider: LLM provider name
            model: Model name
            prompt: Input prompt
            response: Generated response
            duration: Request duration in seconds
            metadata: Additional metadata
        """
        logger = self.get_logger("llm")
        
        log_data = {
            "provider": provider,
            "model": model,
            "prompt_length": len(prompt),
            "response_length": len(response),
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        
        if metadata:
            log_data.update(metadata)
        
        logger.info(f"LLM Request: {log_data}")
        
        # Log detailed request/response to debug level
        logger.debug(f"LLM Request - Provider: {provider}, Model: {model}")
        logger.debug(f"Prompt: {prompt[:1000]}..." if len(prompt) > 1000 else f"Prompt: {prompt}")
        logger.debug(f"Response: {response[:1000]}..." if len(response) > 1000 else f"Response: {response}")
        logger.debug(f"Duration: {duration:.2f}s")
    
    def log_insight_generation(self, 
                              insight_type: str, 
                              source_data: Dict[str, Any], 
                              generated_insight: Dict[str, Any],
                              duration: float) -> None:
        """
        Log insight generation.
        
        Args:
            insight_type: Type of insight
            source_data: Source data used for generation
            generated_insight: Generated insight
            duration: Generation duration in seconds
        """
        logger = self.get_logger("insights")
        
        log_data = {
            "insight_type": insight_type,
            "source_data_keys": list(source_data.keys()),
            "insight_id": generated_insight.get("id", "unknown"),
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Insight Generation: {log_data}")
        
        # Log detailed insight to debug level
        logger.debug(f"Generated Insight: {generated_insight}")
    
    def log_storage_operation(self, 
                             operation: str, 
                             storage_type: str, 
                             entity_type: str, 
                             entity_id: str,
                             success: bool,
                             duration: float,
                             error: Optional[str] = None) -> None:
        """
        Log a storage operation.
        
        Args:
            operation: Operation type (create, read, update, delete)
            storage_type: Type of storage (file, csv, sqlite)
            entity_type: Type of entity (insight, report, etc.)
            entity_id: ID of the entity
            success: Whether the operation was successful
            duration: Operation duration in seconds
            error: Error message if operation failed
        """
        logger = self.get_logger("storage")
        
        log_data = {
            "operation": operation,
            "storage_type": storage_type,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "success": success,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        
        if error:
            log_data["error"] = error
        
        if success:
            logger.info(f"Storage Operation: {log_data}")
        else:
            logger.error(f"Storage Operation Failed: {log_data}")
    
    def log_config_change(self, 
                         component: str, 
                         config_type: str, 
                         changes: Dict[str, Any]) -> None:
        """
        Log a configuration change.
        
        Args:
            component: Component name
            config_type: Type of configuration
            changes: Dictionary of changes
        """
        logger = self.get_logger("config")
        
        log_data = {
            "component": component,
            "config_type": config_type,
            "changes": changes,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Configuration Change: {log_data}")

# Global logger instance
logger = LlamaSeeLogger()

# Convenience function to get a logger
def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Name of the logger
        
    Returns:
        Logger instance
    """
    return logger.get_logger(name) 