"""
Utility functions for the export module.
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional

def generate_default_path(prefix: str, format: str) -> str:
    """
    Generate a default path for export files.
    
    Args:
        prefix: Prefix for the filename.
        format: File format extension.
        
    Returns:
        Default path for the export file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{format}"

def ensure_directory_exists(path: str) -> None:
    """
    Ensure that the directory for the given path exists.
    
    Args:
        path: Path to check.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def validate_export_path(path: Optional[str], default_prefix: str, format: str) -> str:
    """
    Validate and potentially generate an export path.
    
    Args:
        path: User-provided path or None.
        default_prefix: Prefix to use if path is None.
        format: File format extension.
        
    Returns:
        Validated or generated path.
    """
    if path is None:
        path = generate_default_path(default_prefix, format)
    
    ensure_directory_exists(path)
    return path 