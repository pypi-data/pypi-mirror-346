"""
Configuration for insight storage backends.

This module provides configuration classes for different storage backends,
including file-based, CSV-based, and SQLite-based storage.
"""

from typing import Dict, Any, Optional
from pathlib import Path
import os

class StorageConfig:
    """
    Base configuration class for insight storage.
    
    This class provides common configuration options for all storage backends.
    """
    
    def __init__(self, 
                 storage_dir: str = "insights",
                 create_dir: bool = True,
                 **kwargs):
        """
        Initialize the storage configuration.
        
        Args:
            storage_dir: Directory to store insights
            create_dir: Whether to create the storage directory if it doesn't exist
            **kwargs: Additional configuration options
        """
        self.storage_dir = Path(storage_dir)
        self.create_dir = create_dir
        
        # Create the storage directory if requested
        if self.create_dir:
            self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Store additional configuration options
        self.options = kwargs
    
    def get_storage_dir(self) -> Path:
        """
        Get the storage directory path.
        
        Returns:
            Path to the storage directory
        """
        return self.storage_dir
    
    def get_option(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration option.
        
        Args:
            key: The option key
            default: Default value if the option is not set
            
        Returns:
            The option value
        """
        return self.options.get(key, default)


class FileStorageConfig(StorageConfig):
    """
    Configuration for file-based insight storage.
    
    This class provides configuration options specific to file-based storage.
    """
    
    def __init__(self, 
                 storage_dir: str = "insights",
                 create_dir: bool = True,
                 file_extension: str = "json",
                 metadata_file: bool = True,
                 **kwargs):
        """
        Initialize the file storage configuration.
        
        Args:
            storage_dir: Directory to store insights
            create_dir: Whether to create the storage directory if it doesn't exist
            file_extension: Extension for insight files
            metadata_file: Whether to store metadata in a separate file
            **kwargs: Additional configuration options
        """
        super().__init__(storage_dir, create_dir, **kwargs)
        self.file_extension = file_extension
        self.metadata_file = metadata_file
    
    def get_file_extension(self) -> str:
        """
        Get the file extension for insight files.
        
        Returns:
            File extension
        """
        return self.file_extension
    
    def should_store_metadata(self) -> bool:
        """
        Check if metadata should be stored in a separate file.
        
        Returns:
            True if metadata should be stored separately
        """
        return self.metadata_file


class CSVStorageConfig(StorageConfig):
    """
    Configuration for CSV-based insight storage.
    
    This class provides configuration options specific to CSV-based storage.
    """
    
    def __init__(self, 
                 storage_dir: str = "insights",
                 create_dir: bool = True,
                 include_metadata: bool = True,
                 date_format: str = "%Y%m%d_%H%M%S",
                 **kwargs):
        """
        Initialize the CSV storage configuration.
        
        Args:
            storage_dir: Directory to store insights
            create_dir: Whether to create the storage directory if it doesn't exist
            include_metadata: Whether to include metadata in the CSV file
            date_format: Format for date strings in filenames
            **kwargs: Additional configuration options
        """
        super().__init__(storage_dir, create_dir, **kwargs)
        self.include_metadata = include_metadata
        self.date_format = date_format
    
    def should_include_metadata(self) -> bool:
        """
        Check if metadata should be included in the CSV file.
        
        Returns:
            True if metadata should be included
        """
        return self.include_metadata
    
    def get_date_format(self) -> str:
        """
        Get the date format for filenames.
        
        Returns:
            Date format string
        """
        return self.date_format


class SQLiteStorageConfig(StorageConfig):
    """
    Configuration for SQLite-based insight storage.
    
    This class provides configuration options specific to SQLite-based storage.
    """
    
    def __init__(self, 
                 storage_dir: str = "insights",
                 create_dir: bool = True,
                 db_name: str = "insights.db",
                 table_name: str = "insights",
                 **kwargs):
        """
        Initialize the SQLite storage configuration.
        
        Args:
            storage_dir: Directory to store insights
            create_dir: Whether to create the storage directory if it doesn't exist
            db_name: Name of the SQLite database file
            table_name: Name of the table to store insights
            **kwargs: Additional configuration options
        """
        super().__init__(storage_dir, create_dir, **kwargs)
        self.db_name = db_name
        self.table_name = table_name
    
    def get_db_path(self) -> Path:
        """
        Get the path to the SQLite database file.
        
        Returns:
            Path to the database file
        """
        return self.storage_dir / self.db_name
    
    def get_table_name(self) -> str:
        """
        Get the name of the table to store insights.
        
        Returns:
            Table name
        """
        return self.table_name

# Default storage configuration
default_config = FileStorageConfig() 